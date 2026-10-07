#!/usr/bin/env python3
"""Generate the schedule chart and render supporting SVG figures to PNG."""
from __future__ import annotations

import argparse
import base64
import csv
from pathlib import Path

import cairosvg
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
TRANSIT = ROOT / "artifacts" / "colorado-transit-award-service"
parser = argparse.ArgumentParser()
parser.add_argument("--output", type=Path, default=ROOT / ".tmp" / "portfolio-rendered")
parser.add_argument("--emit-preview-data", action="store_true")
args = parser.parse_args()
args.output.mkdir(parents=True, exist_ok=True)

with (TRANSIT / "route-service-crosswalk.csv").open(newline="", encoding="utf-8") as stream:
    rows = [row for row in csv.DictReader(stream) if row["derived_frequency_rate_before_per_hour"] and row["derived_frequency_rate_after_per_hour"]]
labels = {
    "16th Street FreeRide": "16th Street FreeRide\nWeekdays",
    "43": "Route 43\nSpecified weekday peak segment",
    "ART": "ART\nWeekdays",
}
if {row["route_key"] for row in rows} != set(labels):
    raise SystemExit("Frequency comparison rows changed; review labels and scope before rendering.")
before = [float(row["derived_frequency_rate_before_per_hour"]) for row in rows]
after = [float(row["derived_frequency_rate_after_per_hour"]) for row in rows]
plt.rcParams.update({"font.size": 10, "svg.fonttype": "none", "svg.hashsalt": "career-portfolio"})
fig, axis = plt.subplots(figsize=(10.5, 4.7))
positions = list(range(len(rows)))
axis.barh([position - 0.16 for position in positions], before, height=0.28, color="#94a3b8", label="Before")
axis.barh([position + 0.16 for position in positions], after, height=0.28, color="#2563eb", label="After")
axis.set_yticks(positions, [labels[row["route_key"]] for row in rows])
axis.invert_yaxis()
axis.set_xlim(0, max(after) * 1.16)
axis.set_xlabel("Headway-derived scheduled departures per hour per direction")
axis.set_axisbelow(True)
axis.grid(axis="x", alpha=0.18)
for spine in ["top", "right", "left"]:
    axis.spines[spine].set_visible(False)
axis.tick_params(axis="y", length=0)
for position, value in zip(positions, before):
    axis.text(value + 0.25, position - 0.16, f"{value:.2f}".rstrip("0").rstrip("."), va="center", fontsize=10)
for position, value in zip(positions, after):
    axis.text(value + 0.25, position + 0.16, f"{value:.2f}".rstrip("0").rstrip("."), va="center", fontsize=10)
axis.legend(loc="lower right", frameon=False)
fig.suptitle("Three comparable scheduled-service frequency changes", fontsize=14, fontweight="bold", x=0.29, ha="left")
fig.text(0.29, 0.035, "Separate service/period comparisons. Assumes headway applies in the stated direction.\nScheduled rates; no actual operations, vehicle-hours, route grant dollars, or causal effects inferred.", fontsize=9, color="#475569")
fig.subplots_adjust(left=0.29, right=0.96, top=0.82, bottom=0.21)
chart = TRANSIT / "scheduled-frequency.svg"
fig.savefig(chart, format="svg", bbox_inches="tight", metadata={"Date": None})
plt.close(fig)

for figure in sorted((ROOT / "artifacts").rglob("*.svg")):
    png_path = args.output / (figure.stem + ".png")
    cairosvg.svg2png(url=str(figure), write_to=str(png_path), output_width=1440)
    print(f"Rendered {figure.relative_to(ROOT)} -> {png_path.name}")
    if args.emit_preview_data:
        encoded = base64.b64encode(png_path.read_bytes()).decode("ascii")
        print(f"PORTFOLIO_PREVIEW_BEGIN {figure.relative_to(ROOT).as_posix()}")
        for offset in range(0, len(encoded), 120):
            print(encoded[offset:offset + 120])
        print("PORTFOLIO_PREVIEW_END")

if args.emit_preview_data:
    encoded = base64.b64encode(chart.read_bytes()).decode("ascii")
    print("PORTFOLIO_SVG_BEGIN artifacts/colorado-transit-award-service/scheduled-frequency.svg")
    for offset in range(0, len(encoded), 120):
        print(encoded[offset:offset + 120])
    print("PORTFOLIO_SVG_END")
