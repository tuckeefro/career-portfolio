"""Generate printable engineering case sheets from the retained career accounts."""
from __future__ import annotations

import json
from functools import lru_cache
from html import escape
from pathlib import Path

from matplotlib import font_manager
from PIL import ImageFont

INK, MUTED, BLUE, AMBER = "#142434", "#617285", "#1764C0", "#99520C"
PALE, BORDER = "#F2F6FA", "#D8E0E8"
ROOT_URL = "https://github.com/tuckeefro/career-portfolio/blob/main/"
WIDTH, HEIGHT = 1080, 1528

@lru_cache(maxsize=None)
def font(size, weight):
    filename = font_manager.findfont(font_manager.FontProperties(family="DejaVu Sans", weight=weight))
    return ImageFont.truetype(filename, size)

def text(x, y, value, size=28, weight="normal", color=INK, anchor="start"):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{escape(str(value))}</text>'

def wrapped(value, width, size=28, weight="normal"):
    lines, current = [], ""
    for word in value.split():
        candidate = f"{current} {word}".strip()
        if current and font(size, weight).getlength(candidate) > width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines

def paragraph(x, y, value, width, size=28, spacing=36, color=INK, weight="normal", max_lines=None):
    lines = wrapped(value, width, size, weight)
    if max_lines is not None and len(lines) > max_lines:
        raise ValueError(f"Case-sheet copy exceeds the allocated {max_lines} lines: {value}")
    return [text(x, y + index * spacing, line, size, weight, color) for index, line in enumerate(lines)]

def box(x, y, width, height, fill="white", stroke=BORDER, dashed=False):
    dash = ' stroke-dasharray="10 7"' if dashed else ""
    return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2"{dash}/>'

def path(points, color=BLUE, dashed=False, arrow=True):
    dash = ' stroke-dasharray="10 8"' if dashed else ""
    marker = f' marker-end="url(#{("command" if color == AMBER else "flow")})"' if arrow else ""
    return f'<path d="{points}" fill="none" stroke="{color}" stroke-width="5" stroke-linejoin="round"{dash}{marker}/>'

def svg(title, description, elements):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="297mm" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">\n'
        f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>\n'
        '<defs>'
        f'<marker id="flow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{BLUE}"/></marker>'
        f'<marker id="command" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{AMBER}"/></marker>'
        '</defs>\n'
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="white"/>\n'
        '<g font-family="DejaVu Sans, sans-serif">\n'
        + "\n".join(elements) + "\n</g></svg>\n"
    )

def footer(source, scope):
    elements = paragraph(60, 1420, scope, 960, 22, 29, MUTED, max_lines=2)
    elements.append(
        f'<a href="{ROOT_URL + escape(source)}">'
        + text(60, 1492, f"Source: {source}", 22, color=BLUE) + "</a>"
    )
    return elements

def common(case):
    elements = [
        text(60, 65, f'TUCKER VANA / CASE {case["number"]}', 24, "bold", MUTED),
        text(1020, 65, case["employer"], 26, "bold", BLUE, "end"),
        text(60, 146, case["title"][0], 52, "bold"),
        text(60, 210, case["title"][1], 52, "bold"),
    ]
    elements += paragraph(60, 267, case["contribution"], 960, 28, 37, max_lines=3)
    elements += [
        box(60, 386, 960, 106, "#EAF3FF", BLUE),
        text(84, 431, case["result"], 38, "bold", BLUE),
    ]
    elements += paragraph(84, 470, case["result_scope"], 910, 24, 31, MUTED, max_lines=1)
    elements.append(text(60, 547, case["diagram_heading"], 30, "bold"))
    return elements

def decisions(case, y, row_height=87):
    elements = [text(60, y, "What I found and did" if case["id"] == "waterjet" else "Decisions and contribution", 30, "bold")]
    for index, (label, value) in enumerate(case["decisions"]):
        row_y = y + 28 + index * row_height
        elements += [
            box(60, row_y, 960, row_height - 8, PALE),
            text(84, row_y + 34, label, 26, "bold", BLUE),
        ]
        elements += paragraph(287, row_y + 32, value, 705, 25, 31, max_lines=2)
    return elements

def air(case):
    e = common(case)
    e += [
        box(60, 582, 294, 220, PALE),
        f'<circle cx="207" cy="633" r="28" fill="white" stroke="{BLUE}" stroke-width="3"/>',
        f'<path d="M198 618 L222 633 L198 648 z" fill="{BLUE}"/>',
        text(207, 699, "Rented package", 25, "bold", anchor="middle"),
        text(207, 739, "KAESER AIRCENTER", 25, anchor="middle"),
        box(408, 620, 174, 151),
        f'<path d="M449 645 H541 M463 645 L527 680" fill="none" stroke="{BLUE}" stroke-width="3"/>',
        text(495, 714, "Added", 25, "bold", anchor="middle"),
        text(495, 746, "filtration", 25, "bold", anchor="middle"),
        box(726, 580, 294, 158, "#EAF3FF", BLUE),
        text(873, 637, "First line", 32, "bold", BLUE, "middle"),
        text(873, 680, "Initial operation", 25, anchor="middle"),
        box(726, 824, 294, 158, "white", MUTED, True),
        text(873, 882, "Second line", 32, "bold", MUTED, "middle"),
        text(873, 925, "Not yet ordered", 25, color=MUTED, anchor="middle"),
        path("M354 660 H398"),
        path("M582 660 H716"),
        path("M646 660 V903 H716", MUTED, True, False),
        f'<circle cx="646" cy="660" r="6" fill="{BLUE}"/>',
        text(646, 779, "Planned", 24, color=MUTED, anchor="middle"),
        text(646, 811, "demand", 24, color=MUTED, anchor="middle"),
    ]
    e += paragraph(60, 1029, "Solid path: operated first-line load. Dashed path: expansion allowance.", 960, 25, 32, MUTED, max_lines=1)
    e += decisions(case, 1094)
    e += footer(case["source"], case["scope"])
    return svg("Pouch Factory air-supply engineering case", case["summary"] + " " + case["scope"], e)

def waterjet(case):
    e = common(case)
    e += [
        text(60, 595, "Cut travel →", 25, color=MUTED),
        box(60, 619, 960, 106, PALE),
        '<rect x="88" y="633" width="250" height="78" fill="#1764C0" opacity="0.30"/>',
        '<rect x="380" y="633" width="300" height="18" fill="#99520C" opacity="0.65"/>',
        '<rect x="724" y="633" width="268" height="78" fill="#1764C0" opacity="0.30"/>',
        text(213, 769, "Through-cut", 28, "bold", BLUE, "middle"),
        text(530, 763, "Surface removal", 27, "bold", AMBER, "middle"),
        text(530, 803, "~1 inch travel", 25, color=AMBER, anchor="middle"),
        text(858, 769, "Through-cut", 28, "bold", BLUE, "middle"),
        box(60, 851, 346, 151, PALE),
        text(233, 908, "High-pressure pump", 29, "bold", anchor="middle"),
        text(233, 957, "Inspected and rebuilt", 25, anchor="middle"),
        box(738, 851, 282, 151, "#EAF3FF", BLUE),
        text(879, 915, "Cutting process", 29, "bold", BLUE, "middle"),
        text(879, 958, "Cut result checked", 25, anchor="middle"),
        path("M406 922 H728"),
        text(572, 890, "Supply path", 25, color=BLUE, anchor="middle"),
    ]
    e += paragraph(60, 1046, "The colored strip sketches penetration; it is not a measured cut-depth trace.", 960, 24, 31, MUTED, max_lines=1)
    e += decisions(case, 1105)
    e += footer(case["source"], case["scope"])
    return svg("Waterjet pump repair engineering case", case["summary"] + " " + case["scope"], e)

def maybell(case):
    e = common(case)
    e += [
        box(60, 582, 358, 150, PALE),
        text(239, 635, "Lake Shore 372", 30, "bold", anchor="middle"),
        text(239, 678, "Instrument readout", 25, anchor="middle"),
        box(674, 582, 346, 150, PALE),
        text(847, 622, "System readouts", 29, "bold", anchor="middle"),
        text(847, 667, "Pressure · flow", 25, anchor="middle"),
        text(847, 704, "Heater output · valve state", 23, anchor="middle"),
        box(60, 795, 358, 115),
        text(239, 842, "LattePanda", 30, "bold", anchor="middle"),
        text(239, 883, "Readout integration", 24, anchor="middle"),
        box(488, 795, 532, 149, "#EAF3FF", BLUE),
        text(754, 850, "Shared operator GUI", 33, "bold", BLUE, "middle"),
        text(754, 901, "Readouts + valve controls", 27, anchor="middle"),
        path("M239 732 V785"),
        path("M418 850 H478"),
        path("M847 732 V785"),
        box(488, 1024, 232, 112, "#FFF3E1", AMBER),
        text(604, 1072, "Operator", 29, "bold", AMBER, "middle"),
        text(604, 1114, "Commands", 25, anchor="middle"),
        box(774, 1024, 246, 112, "#FFF3E1", AMBER),
        text(897, 1072, "Pneumatic", 27, "bold", AMBER, "middle"),
        text(897, 1111, "gas valves", 27, "bold", AMBER, "middle"),
        path("M604 1024 V954", AMBER),
        path("M897 944 V1014", AMBER),
        text(60, 1179, "Blue: readouts", 25, "bold", BLUE),
        text(488, 1179, "Orange: operator commands", 25, "bold", AMBER),
    ]
    e += decisions(case, 1230, 77)
    e += footer(case["source"], case["scope"])
    return svg("Maybell instrumentation and operator-control engineering case", case["summary"] + " " + case["scope"], e)

def overview(data):
    info = data["overview"]
    e = [
        text(60, 74, "ENGINEERING AND EQUIPMENT WORK", 24, "bold", MUTED),
        text(60, 152, info["title"][0], 66, "bold"),
        text(60, 214, info["title"][1], 38, "bold", BLUE),
    ]
    e += paragraph(60, 280, info["introduction"], 960, 29, 38, max_lines=3)
    for index, case in enumerate(data["cases"]):
        y = 412 + index * 264
        e += [
            box(60, y, 960, 242, PALE),
            text(84, y + 39, f'CASE {case["number"]} / {case["employer"]}', 24, "bold", BLUE),
            text(84, y + 84, {
                "air": "Production air supply",
                "waterjet": "Waterjet pump rebuild",
                "maybell": "Prototype instrumentation",
            }[case["id"]], 34, "bold"),
        ]
        e += paragraph(84, y + 128, case["summary"], 906, 28, 36, max_lines=2)
        e.append(text(84, y + 215, case["result"], 29, "bold", BLUE))
    e += paragraph(60, 1260, info["education"], 960, 25, 33, max_lines=2)
    e += paragraph(60, 1360, info["practical"], 960, 24, 32, MUTED, max_lines=3)
    e += [
        text(60, 1484, "Full experience and project sources:", 22, color=MUTED),
        f'<a href="{ROOT_URL}WORK_INDEX.md">' + text(508, 1484, "github.com/tuckeefro/career-portfolio", 22, color=BLUE) + "</a>",
    ]
    return svg("Tucker Vana engineering case packet overview", info["positioning"] + " " + info["introduction"], e)

def build_case_sheets(root: Path):
    directory = root / "artifacts" / "career-sheets"
    data = json.loads((directory / "case-records.json").read_text(encoding="utf-8"))
    if data["format"] != "career-portfolio-engineering-cases-v1":
        raise ValueError("Review the case-sheet generator when its record format changes.")
    if [case["id"] for case in data["cases"]] != ["air", "waterjet", "maybell"]:
        raise ValueError("The engineering packet expects its three selected paid-work cases in order.")
    for case in data["cases"]:
        source_path = root / case["source"]
        if not source_path.is_file():
            raise ValueError("Each case must retain its linked source account.")
        account = source_path.read_text(encoding="utf-8")
        if any(excerpt not in account for excerpt in case["source_excerpts"]):
            raise ValueError(f'Source account changed; review the {case["id"]} case-sheet claims.')
    builders = {"air": air, "waterjet": waterjet, "maybell": maybell}
    figures = {"artifacts/career-sheets/00-overview.svg": overview(data)}
    for case in data["cases"]:
        name = f'{case["number"]}-{case["id"]}'
        figures[f"artifacts/career-sheets/{name}.svg"] = builders[case["id"]](case)
    return figures
