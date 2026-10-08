#!/usr/bin/env python3
"""Generate the scheduled-frequency chart and export SVG figures for review."""
from __future__ import annotations

import argparse
import base64
import csv
from pathlib import Path

import cairosvg
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

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
    "16th Street FreeRide": ("16th Street FreeRide", "Weekdays", 4.5, 3),
    "43": ("Route 43", "Specified weekday peak segment", 15, 7.5),
    "ART": ("ART", "Weekdays", 60, 30),
}
if {row["route_key"] for row in rows} != set(labels):
    raise SystemExit("Frequency rows changed; review labels and scope before rendering.")
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 15, "svg.fonttype": "none", "svg.hashsalt": "career-portfolio"})
fig = plt.figure(figsize=(7.5, 8.4), facecolor="white")
ink, muted, blue, grey = "#142434", "#617285", "#1764C0", "#8798AA"
fig.text(0.08, 0.942, "More scheduled", fontsize=26, weight="bold", color=ink)
fig.text(0.08, 0.89, "departures per hour", fontsize=26, weight="bold", color=ink)
fig.text(0.08, 0.84, "RTD · announced June 2026 service changes", fontsize=14, color=muted)
fig.patches.extend([
    patches.Rectangle((0.08, 0.787), 0.022, 0.017, transform=fig.transFigure, facecolor=grey),
    patches.Rectangle((0.35, 0.787), 0.022, 0.017, transform=fig.transFigure, facecolor=blue),
])
fig.text(0.116, 0.785, "Before", fontsize=14, color=ink)
fig.text(0.385, 0.785, "Announced", fontsize=14, color=ink)
for index, row in enumerate(rows):
    name, period, old_headway, new_headway = labels[row["route_key"]]
    before = float(row["derived_frequency_rate_before_per_hour"])
    after = float(row["derived_frequency_rate_after_per_hour"])
    if abs(before * old_headway - 60) > 0.0001 or abs(after * new_headway - 60) > 0.0001:
        raise SystemExit(f"Headway labels disagree with retained rates: {name}")
    change = (after / before - 1) * 100
    heading_y = 0.729 - index * 0.206
    fig.text(0.08, heading_y, name, fontsize=18, weight="bold", color=ink)
    fig.text(0.92, heading_y, f"+{change:.0f}%", fontsize=21, weight="bold", color=blue, ha="right")
    fig.text(0.08, heading_y - 0.038, f"{period} · {old_headway:g} → {new_headway:g} min", fontsize=13, color=muted)
    axis = fig.add_axes([0.08, 0.56 - index * 0.206, 0.84, 0.108])
    axis.barh([0.72, 0.28], [before, after], height=0.27, color=[grey, blue])
    axis.set_xlim(0, 23)
    axis.set_ylim(0, 1)
    axis.set_yticks([])
    axis.set_xticks([0, 5, 10, 15, 20])
    axis.set_axisbelow(True)
    axis.grid(axis="x", color="#D8E0E8", linewidth=0.6)
    axis.tick_params(axis="x", length=0, labelsize=12, labelbottom=index == len(rows) - 1, colors=muted)
    for spine in axis.spines.values():
        spine.set_visible(False)
    for y, value in [(0.72, before), (0.28, after)]:
        label = f"{value:.2f}".rstrip("0").rstrip(".")
        axis.text(value + 0.28, y, label, va="center", fontsize=16, color=ink)
fig.text(0.08, 0.107, "Scheduled departures / hour / direction", fontsize=14, color=ink)
fig.text(0.08, 0.069, "Rate = 60 ÷ headway in minutes.", fontsize=12.5, color=muted)
fig.text(0.08, 0.040, "Assumes the stated headway applies per direction.", fontsize=12, color=muted)
fig.text(0.08, 0.011, "Source: RTD final June changes · retained route crosswalk", fontsize=11.5, color=muted)
chart = TRANSIT / "scheduled-frequency.svg"
fig.savefig(chart, format="svg", metadata={"Date": None})
plt.close(fig)

def emit(kind: str, relative: str, content: bytes) -> None:
    encoded = base64.b64encode(content).decode("ascii")
    print(f"PORTFOLIO_{kind}_BEGIN {relative}")
    for offset in range(0, len(encoded), 120):
        print(encoded[offset:offset + 120])
    print(f"PORTFOLIO_{kind}_END")

for figure in sorted((ROOT / "artifacts").rglob("*.svg")):
    relative = figure.relative_to(ROOT).as_posix()
    png_path = args.output / (figure.stem + ".png")
    phone_path = args.output / (figure.stem + "-phone.png")
    cairosvg.svg2png(url=str(figure), write_to=str(png_path), output_width=1440)
    cairosvg.svg2png(url=str(figure), write_to=str(phone_path), output_width=375)
    print(f"Rendered {relative} -> {png_path.name}; phone review at 375 px")
    if args.emit_preview_data:
        emit("PREVIEW", relative, png_path.read_bytes())
        emit("PHONE", relative, phone_path.read_bytes())

if args.emit_preview_data:
    emit("SVG", "artifacts/colorado-transit-award-service/scheduled-frequency.svg", chart.read_bytes())
