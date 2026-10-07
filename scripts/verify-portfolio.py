#!/usr/bin/env python3
"""Check local document links, SVG structure, and retained fixture consistency."""
from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
errors: list[str] = []
markdown_count = 0
svg_count = 0

for document in sorted(ROOT.rglob("*.md")):
    relative = document.relative_to(ROOT)
    if any(part.startswith(".") for part in relative.parts):
        continue
    markdown_count += 1
    for target in LINK.findall(document.read_text(encoding="utf-8")):
        target = target.strip().strip("<>")
        if target.startswith(("https://", "http://", "mailto:", "#")):
            continue
        target = unquote(target.split("#", 1)[0])
        if target and not (document.parent / target).exists():
            errors.append(f"{relative}: missing target {target}")

for figure in sorted((ROOT / "artifacts").rglob("*.svg")):
    svg_count += 1
    try:
        node = ET.parse(figure).getroot()
        if node.tag != "{http://www.w3.org/2000/svg}svg" or not node.get("viewBox"):
            errors.append(f"{figure.relative_to(ROOT)}: invalid SVG root or missing viewBox")
    except ET.ParseError as exc:
        errors.append(f"{figure.relative_to(ROOT)}: {exc}")

fixture_dir = ROOT / "artifacts" / "shiftforge"
inputs = json.loads((fixture_dir / "inputs.json").read_text(encoding="utf-8"))
output = json.loads((fixture_dir / "output.json").read_text(encoding="utf-8"))
checks = json.loads((fixture_dir / "scheduler-checks.json").read_text(encoding="utf-8"))
worker_ids = {worker["id"] for worker in inputs["employees"]}
if any(shift["employeeId"] not in worker_ids for shift in output["shifts"]):
    errors.append("ShiftForge output references a worker absent from the retained input")
if output["stats"]["totalShifts"] != len(output["shifts"]):
    errors.append("ShiftForge retained totalShifts disagrees with generated rows")
if output["stats"]["understaffedSlots"] != len(output["unassigned"]):
    errors.append("ShiftForge retained understaffedSlots disagrees with shortage rows")
if len(checks["assertions"]) != 12 or not all(item["passed"] is True for item in checks["assertions"]):
    errors.append("ShiftForge retained scheduler check record is incomplete or failed")
if errors:
    raise SystemExit("\n".join(errors))

print(f"Verified {markdown_count} Markdown documents, {svg_count} SVG figures, and retained ShiftForge records.")
