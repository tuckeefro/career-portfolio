"""Render source-linked quantitative air-storage figures and an A4 analysis supplement."""
from __future__ import annotations
import hashlib
import io
from html import escape
from pathlib import Path
import cairosvg
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from air_storage_model import verify_records
from career_pdf import normalized_pdf

INK, MUTED, BLUE, AMBER = "#142434", "#617285", "#1764C0", "#99520C"
NAMES = ("buffer-duration", "required-storage", "pressure-recovery")

def page(title, subtitle):
    fig = plt.figure(figsize=(210 / 25.4, 297 / 25.4), facecolor="white")
    fig.text(0.08, 0.958, "TUCKER VANA / CURRENT ENGINEERING STUDY", size=13, weight="bold", color=MUTED)
    fig.text(0.08, 0.905, title, size=28, weight="bold", color=INK)
    fig.text(0.08, 0.867, subtitle, size=16, color=MUTED)
    return fig

def axis_style(axis):
    axis.set_axisbelow(True)
    axis.grid(color="#D8E0E8", linewidth=0.7)
    axis.tick_params(labelsize=15, colors=MUTED)
    for side in ("top", "right"):
        axis.spines[side].set_visible(False)
    for side in ("bottom", "left"):
        axis.spines[side].set_color("#D8E0E8")

def footer(fig):
    fig.text(0.08, 0.080, "Illustrative inputs · constant-temperature ideal-gas inventory", size=13, color=MUTED)
    fig.text(0.08, 0.054, "Flow reference: 1 atm, 20°C · tank: 20°C · pressure band: 20 psi", size=12.5, color=MUTED)
    fig.text(0.08, 0.028, "Method: DOE sourcebook, Fact Sheet 6, p. 43 · AI-assisted analysis", size=12, color=MUTED,
             url="https://github.com/tuckeefro/career-portfolio/tree/main/artifacts/air-storage-study")

def export(fig, title, description):
    stream = io.StringIO()
    fig.savefig(stream, format="svg", metadata={"Date": None})
    plt.close(fig)
    content = stream.getvalue()
    content = content.replace("<svg ", '<svg role="img" aria-labelledby="study-title study-description" ', 1)
    start = content.index(">", content.index("<svg")) + 1
    return content[:start] + f'<title id="study-title">{escape(title)}</title><desc id="study-description">{escape(description)}</desc>' + content[start:]

def buffer_figure(inputs, record, rows):
    fig = page("Storage buys time.", "How long can storage cover a constant flow shortfall?")
    ax = fig.add_axes([0.14, 0.29, 0.79, 0.48])
    colors = ("#8B9BAA", AMBER, BLUE, "#24816E")
    for volume, color in zip(inputs["sweep"]["volumes_us_gal"], colors):
        data = [row for row in rows if row["volume_us_gal"] == volume]
        ax.plot([r["shortfall_ref_cfm"] for r in data], [r["time_to_floor_s"] for r in data],
                color=color, linewidth=2.6, label=f"{volume} US gal")
    ax.axhline(30, color=MUTED, linewidth=1.3, linestyle="--")
    ax.text(99, 34, "30-second event", ha="right", color=MUTED, size=14)
    ax.set_xlim(10, 100)
    ax.set_ylim(0, 210)
    ax.set_xticks([10, 20, 40, 60, 80, 100])
    ax.set_yticks([0, 30, 60, 120, 180])
    ax.set_xlabel("Net flow shortfall (reference ft³/min)", size=16, color=INK, labelpad=13)
    ax.set_ylabel("Time to minimum pressure (s)", size=16, color=INK, labelpad=12)
    axis_style(ax)
    ax.legend(title="Total effective storage", title_fontsize=14, fontsize=14, frameon=False, loc="upper right")
    for item, color in zip(record["worked_event"]["receivers"], (AMBER, BLUE)):
        ax.scatter([40], [item["time_to_floor_s"]], s=48, color=color, zorder=5)
    fig.text(0.08, 0.199, "At a 40-cfm shortfall:", size=18, weight="bold", color=INK)
    fig.text(0.08, 0.162, "80 gal provides 21.8 s; 120 gal provides 32.7 s.", size=17, color=INK)
    fig.text(0.08, 0.126, "Time scales with storage volume and usable pressure band.", size=15, color=MUTED)
    footer(fig)
    return export(fig, "Compressed-air storage buffer duration",
                  "Calculated time to the 80-psig floor from 100 psig for four total storage volumes and a range of reference-flow shortfalls. Illustrative inputs, not plant measurements.")


def sizing_figure(inputs, record, rows):
    fig = page("Size the usable buffer.", "Required total storage for each shortfall and event duration")
    shortfalls = inputs["sweep"]["grid_shortfalls_ref_cfm"]
    durations = inputs["sweep"]["durations_s"]
    values = np.array([[next(r["required_volume_us_gal"] for r in rows if r["shortfall_ref_cfm"] == q and r["duration_s"] == t)
                        for t in durations] for q in shortfalls])
    ax = fig.add_axes([0.16, 0.29, 0.77, 0.49])
    ax.imshow(values, origin="lower", aspect="auto", cmap="Blues", vmin=0, vmax=float(values.max()))
    for iy, ix in np.ndindex(values.shape):
        color = "white" if values[iy, ix] / values.max() > 0.55 else INK
        ax.text(ix, iy, f"{np.ceil(values[iy, ix]):.0f}", ha="center", va="center", size=15, color=color)
    ax.set_xticks(range(len(durations)), durations)
    ax.set_yticks(range(len(shortfalls)), shortfalls)
    ax.set_xlabel("Event duration (s)", size=17, color=INK, labelpad=14)
    ax.set_ylabel("Net shortfall (reference ft³/min)", size=16, color=INK, labelpad=12)
    ax.tick_params(labelsize=15, length=0, pad=9, colors=MUTED)
    ix, iy = durations.index(30), shortfalls.index(40)
    ax.add_patch(patches.Rectangle((ix - 0.5, iy - 0.5), 1, 1, fill=False, edgecolor=AMBER, linewidth=3))
    fig.text(0.08, 0.209, "Each cell: US gallons, rounded up to a whole gallon.", size=15, color=MUTED)
    fig.text(0.08, 0.170, "Worked case: 40 cfm × 30 s requires 109.9 US gal.", size=17, weight="bold", color=INK)
    fig.text(0.08, 0.129, "This is the idealized inventory requirement before design margin.", size=14.5, color=MUTED)
    footer(fig)
    return export(fig, "Compressed-air required storage matrix",
                  "Calculated required total storage in US gallons for ten net shortfalls and seven event durations, using a 20-psi pressure band. Cells round upward; unrounded values are retained.")

def pressure_figure(inputs, record, rows):
    fig = page("Check the pressure floor.", "A 30-second burst followed by recovery")
    event = inputs["transient"]
    flow = fig.add_axes([0.15, 0.65, 0.77, 0.14])
    flow.step([0, 30, 90], [80, 20, 20], where="post", color=AMBER, linewidth=2.6, label="Demand")
    flow.plot([0, 90], [40, 40], color=BLUE, linewidth=2.6, label="Compressor supply")
    flow.set_xlim(0, 90)
    flow.set_ylim(0, 100)
    flow.set_yticks([20, 40, 80])
    flow.tick_params(labelbottom=False)
    flow.set_ylabel("Reference cfm", size=15, color=INK, labelpad=10)
    axis_style(flow)
    flow.legend(loc="upper right", fontsize=12.5, frameon=False)
    pressure = fig.add_axes([0.15, 0.31, 0.77, 0.26])
    pressure.axvspan(0, 30, color="#FFF3E1", zorder=0)
    pressure.axhline(80, color=MUTED, linestyle="--", linewidth=1.5)
    for volume, color in ((80, AMBER), (120, BLUE)):
        data = [row for row in rows if row["volume_us_gal"] == volume]
        pressure.plot([r["time_s"] for r in data], [r["pressure_psig"] for r in data], color=color, linewidth=2.7, label=f"{volume} US gal")
    hit = record["worked_event"]["receivers"][0]["time_to_floor_s"]
    pressure.scatter([hit], [80], color=AMBER, s=55, zorder=5)
    pressure.text(31, 79.5, "80 gal: model stops at the selected floor", size=12.5, color=AMBER, va="top")
    pressure.set_xlim(0, 90)
    pressure.set_ylim(76, 104)
    pressure.set_xticks([0, 15, 30, 60, 90])
    pressure.set_yticks([80, 90, 100])
    pressure.set_xlabel("Time from burst start (s)", size=16, color=INK, labelpad=12)
    pressure.set_ylabel("Storage pressure (psig)", size=16, color=INK, labelpad=12)
    axis_style(pressure)
    pressure.legend(loc="lower center", bbox_to_anchor=(0.5, 1.06), ncol=2, fontsize=13, frameon=False)
    fig.text(0.08, 0.228, "80 gal reaches the floor after 21.8 s.", size=17, weight="bold", color=AMBER)
    fig.text(0.08, 0.190, "120 gal ends the burst at 81.7 psig; recovery takes 60 s.", size=16, color=INK)
    fig.text(0.08, 0.145, "The burst uses 20 reference ft³; a 20-cfm margin restores it.", size=14.5, color=MUTED)
    footer(fig)
    return export(fig, "Compressed-air demand and pressure recovery",
                  "Illustrative supply and demand timeline above pressure traces for 80 and 120 US gallons. The smaller-volume trace stops at 80 psig after 21.8 seconds. The larger completes the burst and recovers in 60 seconds.")

def build_figures(root: Path):
    inputs, record, buffers, sizing, traces, _ = verify_records(root)
    expected = (
        inputs["reference"]["pressure_pa"] == 101325,
        inputs["reference"]["temperature_k"] == 293.15,
        inputs["receiver"]["temperature_k"] == 293.15,
        inputs["receiver"]["initial_gauge_psi"] == 100,
        inputs["receiver"]["minimum_gauge_psi"] == 80,
        inputs["sweep"]["volumes_us_gal"] == [40, 80, 120, 240],
        inputs["transient"]["volumes_us_gal"] == [80, 120],
        inputs["transient"]["compressor_ref_cfm"] == 40,
        inputs["transient"]["burst_demand_ref_cfm"] == 80,
        inputs["transient"]["post_burst_demand_ref_cfm"] == 20,
        inputs["transient"]["burst_duration_s"] == 30,
    )
    if not all(expected):
        raise ValueError("Example inputs changed; review figure labels, annotations, and axes")
    figures = (buffer_figure(inputs, record, buffers), sizing_figure(inputs, record, sizing), pressure_figure(inputs, record, traces))
    return {f"artifacts/air-storage-study/{name}.svg": content for name, content in zip(NAMES, figures)}

def build_study_pdf(root, generated_sources):
    exports, pages = {}, []
    combined = hashlib.sha256()
    for name in NAMES:
        relative = f"artifacts/air-storage-study/{name}.svg"
        source = generated_sources[root / relative].read_bytes()
        raw = cairosvg.svg2pdf(bytestring=source)
        combined.update(relative.encode("utf-8") + b"\0" + source + b"\0")
        exports[f"artifacts/air-storage-study/{name}.pdf"] = normalized_pdf([raw], "Tucker Vana / " + name, hashlib.sha256(source).hexdigest())
        pages.append(raw)
    exports["artifacts/air-storage-study/air-storage-analysis.pdf"] = normalized_pdf(
        pages, "Tucker Vana / Illustrative compressed-air storage analysis", combined.hexdigest())
    return exports
