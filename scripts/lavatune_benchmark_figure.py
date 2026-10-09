"""Plot the retained repeated Lavatune benchmark, without rerunning it."""
from __future__ import annotations

import io
import json
import math
from pathlib import Path
from statistics import median

import matplotlib.pyplot as plt

SOURCE_REVISION = "f79516e82b9b6383ea1d169be2937c9ba6a5a93d"

def load_record(root: Path):
    path = root / "artifacts" / "lavatune" / "renderer-benchmark.json"
    record = json.loads(path.read_text(encoding="utf-8"))
    if record["format"] != "career-portfolio-lavatune-render-benchmark-v1" or record["source_revision"] != SOURCE_REVISION:
        raise ValueError("Review the benchmark figure when its source or format changes.")
    method = record["method"]
    expected = {
        "repetitions": 5, "frames_per_path_per_run": 120,
        "terminal_width_cells": 120, "terminal_height_cells": 30, "configured_blobs": 4,
    }
    if any(method[key] != value for key, value in expected.items()) or len(record["runs"]) != 5:
        raise ValueError("Review figure labels when the benchmark workload changes.")
    if [run["repetition"] for run in record["runs"]] != list(range(1, 6)):
        raise ValueError("The five retained repetitions must be complete and ordered.")
    for run in record["runs"]:
        report = run["result"]
        if (report["frames"], report["width"], report["height"]) != (120, 120, 30):
            raise ValueError("Retained run workload disagrees with the method.")
        if report["python"] != record["environment"]["python"] or report["machine"] != record["environment"]["machine"]:
            raise ValueError("Retained run environment disagrees with the capture record.")
        for key in ("alpha_ms_per_frame", "contour_ms_per_frame"):
            if not isinstance(report[key], (int, float)) or not math.isfinite(report[key]) or report[key] <= 0:
                raise ValueError("A plotted measurement must be a positive finite cost.")
    return record

def build_figure(root: Path) -> str:
    record = load_record(root)
    costs = [
        [run["result"]["alpha_ms_per_frame"] for run in record["runs"]],
        [run["result"]["contour_ms_per_frame"] for run in record["runs"]],
    ]
    ink, muted, blue, grey = "#142434", "#617285", "#1764C0", "#8798AA"
    settings = {
        "font.family": "DejaVu Sans", "font.size": 15, "svg.fonttype": "none",
        "svg.hashsalt": "career-portfolio-lavatune-benchmark",
    }
    with plt.rc_context(settings):
        fig = plt.figure(figsize=(7.5, 8.4), facecolor="white")
        fig.text(0.08, 0.94, "Two rendering paths.", fontsize=26, weight="bold", color=ink)
        fig.text(0.08, 0.885, "One measured workload.", fontsize=26, weight="bold", color=ink)
        fig.text(0.08, 0.831, "Lavatune · 120 × 30 terminal cells", fontsize=15, color=muted)
        fig.text(0.08, 0.787, "5 runs × 120 synthetic frames per path", fontsize=14, color=ink)
        fig.text(0.08, 0.749, "Bars: median · dots: runs · whiskers: min–max", fontsize=13, color=muted)
        upper = max(value for values in costs for value in values) * 1.18
        for index, (label, values, color) in enumerate(zip(
            ("Scalar field + Fluid", "Analytic contour Fluid"), costs, (grey, blue)
        )):
            y = 0.68 - index * 0.206
            mid = median(values)
            fig.text(0.08, y, label, fontsize=18, weight="bold", color=ink)
            fig.text(0.92, y - 0.042, f"{mid:.2f} ms", fontsize=18, weight="bold", color=color, ha="right")
            axis = fig.add_axes([0.08, y - 0.15, 0.84, 0.081])
            axis.barh([0.5], [mid], height=0.45, color=color, alpha=0.75)
            axis.errorbar(
                [mid], [0.5], xerr=[[mid - min(values)], [max(values) - mid]],
                fmt="none", ecolor=ink, elinewidth=1.8, capsize=7, zorder=3,
            )
            for sample_index, value in enumerate(values):
                axis.scatter([value], [0.37 + sample_index * 0.065], s=25, color=ink, zorder=4)
            axis.set_xlim(0, upper)
            axis.set_ylim(0, 1)
            axis.set_yticks([])
            axis.set_axisbelow(True)
            axis.grid(axis="x", color="#D8E0E8", linewidth=0.6)
            axis.tick_params(axis="x", length=0, labelsize=12, labelbottom=index == 1, colors=muted)
            for spine in axis.spines.values():
                spine.set_visible(False)
        fig.text(0.08, 0.266, "Milliseconds / simulated frame", fontsize=14, color=ink)
        ratios = [a / c for a, c in zip(*costs)]
        fig.text(0.08, 0.21, f"Median paired cost ratio: {median(ratios):.2f}×", fontsize=19, weight="bold", color=blue)
        fig.text(0.08, 0.171, "Scalar-field cost ÷ contour cost in each run.", fontsize=12.5, color=muted)
        fig.text(0.08, 0.122, "Body simulation + material generation only.", fontsize=13, color=ink)
        fig.text(0.08, 0.086, "Live audio capture and terminal presentation excluded.", fontsize=12, color=muted)
        environment = record["environment"]
        fig.text(0.08, 0.051, f"Shared GitHub runner · Python {environment['python']} · {environment['machine']}", fontsize=11.5, color=muted)
        fig.text(0.08, 0.018, f"Source {SOURCE_REVISION[:12]} · raw measurements retained", fontsize=11.5, color=muted)
        stream = io.StringIO()
        fig.savefig(stream, format="svg", metadata={"Date": None})
        plt.close(fig)
    return stream.getvalue()
