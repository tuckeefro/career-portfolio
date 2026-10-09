#!/usr/bin/env python3
"""Check document links, SVG structure, retained fixtures, and career-sheet PDFs."""
from __future__ import annotations

import json
from html import unescape
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HTML_LINK = re.compile(r"""(?:src|href)\s*=\s*["\']([^"\']+)["\']""", re.IGNORECASE)
errors: list[str] = []
markdown_count = 0
svg_count = 0

for document in sorted(ROOT.rglob("*.md")):
    relative = document.relative_to(ROOT)
    if any(part.startswith(".") for part in relative.parts):
        continue
    markdown_count += 1
    content = document.read_text(encoding="utf-8")
    for target in LINK.findall(content) + HTML_LINK.findall(content):
        target = unescape(target.strip().strip("<>"))
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
pdf_count = 0
pdf_groups = (
    ("career-sheets", ("00-overview", "01-air", "02-waterjet", "03-maybell"), "engineering-portfolio", 4),
    ("air-storage-study", ("buffer-duration", "required-storage", "pressure-recovery"), "air-storage-analysis", 3),
)
for directory, names, combined, combined_pages in pdf_groups:
    for name in names + (combined,):
        pdf_path = ROOT / "artifacts" / directory / f"{name}.pdf"
        pdf_count += 1
        try:
            reader = PdfReader(pdf_path, strict=True)
            expected_pages = combined_pages if name == combined else 1
            if len(reader.pages) != expected_pages:
                errors.append(f"{pdf_path.relative_to(ROOT)}: expected {expected_pages} pages")
            if not reader.metadata.get("/PortfolioSourceSHA256"):
                errors.append(f"{pdf_path.relative_to(ROOT)}: missing source fingerprint")
            for page in reader.pages:
                if abs(float(page.mediabox.width) - 595.276) > 0.1 or abs(float(page.mediabox.height) - 841.890) > 0.1:
                    errors.append(f"{pdf_path.relative_to(ROOT)}: expected A4 page dimensions")
        except Exception as exc:
            errors.append(f"{pdf_path.relative_to(ROOT)}: {exc}")

if errors:
    raise SystemExit("\n".join(errors))

print(f"Verified {markdown_count} Markdown documents, {svg_count} SVG figures, retained ShiftForge records, and {pdf_count} PDF exports.")
