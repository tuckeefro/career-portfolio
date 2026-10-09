#!/usr/bin/env python3
"""Retain repeated results from Lavatune's unmodified public render benchmark."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys

SOURCE_REVISION = "f79516e82b9b6383ea1d169be2937c9ba6a5a93d"
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--checkout", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
parser.add_argument("--repetitions", type=int, default=5)
args = parser.parse_args()
if not 3 <= args.repetitions <= 10:
    parser.error("Use 3–10 repetitions.")
checkout = args.checkout.resolve()
revision = subprocess.check_output(
    ["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True
).strip()
if revision != SOURCE_REVISION:
    raise SystemExit("Source checkout differs from the pinned benchmark revision.")
environment = os.environ.copy()
environment["PYTHONPATH"] = str(checkout / "src")
command = [
    sys.executable, str(checkout / "scripts" / "benchmark_render.py"),
    "--frames", "120", "--width", "120", "--height", "30", "--json",
]
runs = []
started = datetime.now(timezone.utc).isoformat()
for repetition in range(1, args.repetitions + 1):
    result = subprocess.run(
        command, cwd=checkout, env=environment, text=True,
        capture_output=True, check=True, timeout=120,
    )
    report = json.loads(result.stdout)
    if (report["frames"], report["width"], report["height"]) != (120, 120, 30):
        raise SystemExit("Source benchmark reported a different workload.")
    for key in ("alpha_ms_per_frame", "contour_ms_per_frame"):
        value = report[key]
        if not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
            raise SystemExit(f"Invalid measured cost: {key}")
    runs.append({"repetition": repetition, "result": report})
    print(f"Measured repetition {repetition}/{args.repetitions}", flush=True)

cpu_model = platform.processor() or "unspecified"
cpu_info = Path("/proc/cpuinfo")
if cpu_info.exists():
    for line in cpu_info.read_text(encoding="utf-8").splitlines():
        if line.startswith("model name"):
            cpu_model = line.split(":", 1)[1].strip()
            break
payload = {
    "format": "career-portfolio-lavatune-render-benchmark-v1",
    "source_repository": "tuckeefro/lavatune",
    "source_revision": revision,
    "source_script": "scripts/benchmark_render.py",
    "started_at_utc": started,
    "completed_at_utc": datetime.now(timezone.utc).isoformat(),
    "environment": {
        "python": platform.python_version(),
        "machine": platform.machine(),
        "platform": platform.platform(),
        "cpu_model": cpu_model,
        "logical_cpus": os.cpu_count(),
        "runner_image": "ubuntu-24.04",
        "github_run_id": os.environ.get("GITHUB_RUN_ID"),
        "github_repository": os.environ.get("GITHUB_REPOSITORY"),
    },
    "method": {
        "repetitions": args.repetitions,
        "frames_per_path_per_run": 120,
        "terminal_width_cells": 120,
        "terminal_height_cells": 30,
        "configured_blobs": 4,
        "execution": "One fresh subprocess per repetition; original source benchmark and measurement order unchanged.",
        "warmup": "No additional warm-up; original script timing boundaries retained.",
        "input": "The original script's synthetic silence, speech, bass, music, and transient frame sequence.",
        "scope": "Body simulation and material generation. Live PCM capture, curses calls, terminal presentation, compositor overhead, display cadence, and power consumption are outside this measurement.",
    },
    "runs": runs,
}
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print("LAVATUNE_BENCHMARK_BEGIN")
print(json.dumps(payload, sort_keys=True))
print("LAVATUNE_BENCHMARK_END")
