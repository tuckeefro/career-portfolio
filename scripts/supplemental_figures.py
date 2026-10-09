#!/usr/bin/env python3
"""Build source-linked supplemental SVGs from retained portfolio records."""
from __future__ import annotations

import csv
import json
from datetime import date, datetime, time, timedelta
from html import escape
from pathlib import Path

INK = "#142434"
MUTED = "#617285"
BLUE = "#1764C0"
AMBER = "#99520C"
LINE = "#D8E0E8"
PALE_BLUE = "#EAF3FF"
PALE_AMBER = "#FFF3E1"

def text(x, y, value, size=32, weight="normal", color=INK, anchor="start"):
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
        f'fill="{color}" text-anchor="{anchor}">{escape(str(value))}</text>'
    )

def box(x, y, width, height, fill="white", stroke=LINE, radius=12):
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
        f'rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
    )

def svg(title, description, elements, height=1260):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="{height}" '
        f'viewBox="0 0 1080 {height}" role="img" aria-labelledby="title desc">\n'
        f'<title id="title">{escape(title)}</title>\n'
        f'<desc id="desc">{escape(description)}</desc>\n'
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{BLUE}"/></marker></defs>\n'
        f'<rect width="1080" height="{height}" fill="white"/>\n'
        '<g font-family="DejaVu Sans, sans-serif">\n'
        + "\n".join(elements)
        + "\n</g>\n</svg>\n"
    )

def date_label(day):
    return f'{day.strftime("%b")} {day.day}'

def shift_end(shift):
    start = datetime.combine(date.fromisoformat(shift["date"]), time.fromisoformat(shift["startTime"]))
    end = datetime.combine(start.date(), time.fromisoformat(shift["endTime"]))
    return end + timedelta(days=1) if end <= start else end

def exclusion(inputs, output, employee_id, day, start_time):
    for request in inputs["ptoRequests"]:
        if (
            request["employeeId"] == employee_id
            and request["status"] == "approved"
            and date.fromisoformat(request["dateFrom"]) <= day <= date.fromisoformat(request["dateTo"])
        ):
            return "Approved PTO", [date_label(day)]
    for availability in inputs["availabilityData"]:
        if availability["employeeId"] == employee_id and availability["date"] == day.isoformat() and availability["available"] is False:
            return "Unavailable", [date_label(day)]
    start = datetime.combine(day, time.fromisoformat(start_time))
    preceding = [
        shift_end(shift)
        for shift in inputs["currentSchedule"] + output["shifts"]
        if shift["employeeId"] == employee_id and shift_end(shift) <= start
    ]
    if preceding:
        hours = (start - max(preceding)).total_seconds() / 3600
        if hours < inputs["minRestHours"]:
            return "Rest limit", [f"{hours:g} h before start", f'{inputs["minRestHours"]:g} h minimum']
    return None

def build_shiftforge(root):
    directory = root / "artifacts" / "shiftforge"
    inputs = json.loads((directory / "inputs.json").read_text(encoding="utf-8"))
    output = json.loads((directory / "output.json").read_text(encoding="utf-8"))
    record = json.loads((directory / "scheduler-checks.json").read_text(encoding="utf-8"))
    first, last = date.fromisoformat(inputs["startDate"]), date.fromisoformat(inputs["endDate"])
    workers = inputs["employees"]
    if last - first != timedelta(days=1) or len(workers) != 3 or len(inputs["shiftTypes"]) != 1:
        raise ValueError("ShiftForge figure expects the retained two-day, three-worker, one-shift fixture; review a changed fixture.")
    if any(not worker["name"].startswith("Synthetic ") for worker in workers):
        raise ValueError("ShiftForge figure requires explicitly named synthetic workers.")
    shift = inputs["shiftTypes"][0]
    required = shift["requiredStaff"]
    if required != 2:
        raise ValueError("Review the two-seat ShiftForge illustration if staffing requirements change.")
    days = [first, last]
    pairs = [(row["date"], row["employeeId"]) for row in output["shifts"]]
    if len(pairs) != len(set(pairs)):
        raise ValueError("Duplicate retained assignments are inconsistent with the matrix.")
    if any(
        row["date"] not in {day.isoformat() for day in days}
        or row["employeeId"] not in {worker["id"] for worker in workers}
        or any(row[field] != shift[field] for field in ("startTime", "endTime", "hours"))
        or row["shiftType"] != shift["name"]
        for row in output["shifts"]
    ):
        raise ValueError("Retained assignments differ from the fixture's dates, workers, or shift.")
    shortages = {}
    for day in days:
        assigned = sum(row["date"] == day.isoformat() for row in output["shifts"])
        missing = required - assigned
        retained = [row for row in output["unassigned"] if row["date"] == day.isoformat() and row["shiftType"] == shift["name"]]
        if assigned > required or (missing and len(retained) != 1) or (not missing and retained):
            raise ValueError("Retained shortage rows disagree with assigned seats.")
        if missing and any(retained[0][key] != value for key, value in {"needed": required, "available": assigned, "shortage": missing}.items()):
            raise ValueError("Retained shortage values disagree with the matrix.")
        shortages[day] = (assigned, missing)
    total_missing = sum(missing for _, missing in shortages.values())
    elements = [
        text(60, 116, "One seat stays", 56, "bold"),
        text(60, 184, "explicitly unfilled.", 56, "bold"),
        text(60, 248, "ShiftForge · synthetic scheduler example", 32, color=MUTED),
        box(60, 288, 960, 90, "#F3F6F9"),
        text(84, 329, f'{shift["startTime"]}–{shift["endTime"]} · {required} workers required', 32),
        text(84, 363, f'Minimum rest: {inputs["minRestHours"]:g} hours · {first.year}', 26, color=MUTED),
        text(70, 435, "Worker", 28, color=MUTED),
    ]
    descriptions = []
    columns = [(270, 350), (650, 370)]
    for day, (x, width) in zip(days, columns):
        elements.append(text(x + width / 2, 435, date_label(day), 36, "bold", anchor="middle"))
    for row_index, worker in enumerate(workers):
        y = 470 + row_index * 154
        elements.extend([
            text(70, y + 49, "Synthetic", 25, color=MUTED),
            text(70, y + 104, worker["name"].removeprefix("Synthetic "), 46, "bold"),
        ])
        for day, (x, width) in zip(days, columns):
            assigned = (day.isoformat(), worker["id"]) in pairs
            reason = exclusion(inputs, output, worker["id"], day, shift["startTime"])
            if assigned and reason:
                raise ValueError("Retained assignment violates a displayed fixture constraint.")
            heading, lines = ("Assigned", [f'{shift["startTime"]}–{shift["endTime"]}']) if assigned else (reason or ("Not assigned", ["Eligible in these checks"]))
            descriptions.append(f'{worker["name"]} on {date_label(day)}: {heading}; ' + "; ".join(lines))
            fill, color = (PALE_BLUE, BLUE) if assigned else (PALE_AMBER, AMBER) if reason else ("#F3F6F9", MUTED)
            elements.extend([
                box(x, y, width, 138, fill, color),
                text(x + 24, y + 50, heading, 34, "bold", color),
            ])
            for index, value in enumerate(lines):
                elements.append(text(x + 24, y + 88 + index * 31, value, 27, color=color))
    elements.append(text(70, 998, "Coverage", 28, color=MUTED))
    for day, (x, width) in zip(days, columns):
        assigned, missing = shortages[day]
        elements.extend([
            text(x + width / 2, 992, f"{assigned} / {required} assigned", 34, "bold", anchor="middle"),
            text(x + width / 2, 1098, f"{missing} unfilled", 37, "bold", AMBER if missing else BLUE, "middle"),
        ])
        for seat in range(required):
            filled = seat < assigned
            seat_x = x + 24 + seat * (width - 48) / required
            dash = '' if filled else ' stroke-dasharray="8 5"'
            elements.append(
                f'<rect x="{seat_x:g}" y="1020" width="{(width - 64) / required:g}" height="38" '
                f'rx="5" fill="{BLUE if filled else "white"}" stroke="{BLUE if filled else AMBER}" '
                f'stroke-width="3"{dash}/>'
            )
    recorded = date.fromisoformat(record["recorded_on"])
    elements.extend([
        text(60, 1170, f"Retained scheduler run · {date_label(recorded)}, {recorded.year}", 26, color=MUTED),
        text(60, 1207, "Sources: inputs.json + normalized output.json", 26, color=MUTED),
        text(60, 1244, "Synthetic example; browser and integrations not exercised.", 25, color=MUTED),
    ])
    if total_missing != 1 or len(output["shifts"]) != 3:
        raise ValueError("Review the ShiftForge headline when assignments or total shortage change.")
    description = (
        "Actual normalized scheduler output for synthetic workers. "
        + ". ".join(descriptions) + ". "
        + "; ".join(f"{date_label(day)}: {assigned} of {required} assigned, {missing} unfilled" for day, (assigned, missing) in shortages.items())
        + ". This is a retained algorithm execution, not a deployed staffing result."
    )
    return svg("ShiftForge constraint matrix: one explicit shortage", description, elements, 1290)

def build_transit(root):
    path = root / "artifacts" / "colorado-transit-award-service" / "route-service-crosswalk.csv"
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    by_key = {row["route_key"]: row for row in rows}
    import re
    split = re.search(
        r"Split into Route (\d+) east segment and new Route (\d+) west segment",
        by_key["21"]["quantified_change"],
    )
    renamed = re.fullmatch(r"(\d+) \(formerly ([^)]+)\)", by_key["287 (formerly LD3)"]["route_key"])
    if not split or not renamed:
        raise ValueError("Transit identity records changed; review the split and rename drawing.")
    east, west = split.groups()
    new, old = renamed.groups()
    if (
        f"western segment of former Route {east}" not in by_key[west]["rtd_june_final_service_change"]
        or "East Evans segment" not in by_key[east]["rtd_june_final_service_change"]
        or f"{old} renamed Route {new}" not in by_key[f"{new} (formerly {old})"]["rtd_june_final_service_change"]
        or any("SRC-2378" not in by_key[key]["source_ids"].split(";") for key in (east, west, f"{new} (formerly {old})"))
    ):
        raise ValueError("Transit split/rename is not supported by the retained final-service records.")
    elements = [
        text(60, 112, "Route labels change.", 56, "bold"),
        text(60, 180, "Keep the service linked.", 56, "bold"),
        text(60, 244, "RTD · June 2026 route identity changes", 32, color=MUTED),
        text(70, 326, "01 / ROUTE SPLIT", 30, "bold", MUTED),
        text(70, 382, "Before", 28, color=MUTED),
        text(645, 382, "After", 28, color=MUTED),
        box(70, 440, 320, 180, "#F3F6F9"),
        text(98, 510, f"Route {east}", 44, "bold"),
        text(98, 558, "Combined route", 27, color=MUTED),
        box(645, 408, 365, 138, PALE_BLUE, BLUE),
        text(671, 463, f"Route {east}", 40, "bold", BLUE),
        text(671, 509, "East Evans segment", 28),
        box(645, 598, 365, 138, PALE_BLUE, BLUE),
        text(671, 653, f"Route {west}", 40, "bold", BLUE),
        text(671, 699, "Western segment", 28),
        f'<path d="M390 530 H510 V477 H635" fill="none" stroke="{BLUE}" stroke-width="5" marker-end="url(#arrow)"/>',
        f'<path d="M510 530 V667 H635" fill="none" stroke="{BLUE}" stroke-width="5" marker-end="url(#arrow)"/>',
        box(70, 777, 940, 103, "#F3F6F9"),
        text(96, 818, "Compare the same segment and service period.", 31, "bold"),
        text(96, 856, "A new label alone does not establish added corridor service.", 27, color=MUTED),
        text(70, 950, "02 / ROUTE RENAME", 30, "bold", MUTED),
        box(70, 990, 320, 148, "#F3F6F9"),
        text(98, 1050, old, 44, "bold"),
        text(98, 1099, "Previous label", 28, color=MUTED),
        box(645, 990, 365, 148, PALE_BLUE, BLUE),
        text(671, 1050, f"Route {new}", 40, "bold", BLUE),
        text(671, 1099, f"Formerly {old}", 28),
        f'<path d="M390 1064 H635" fill="none" stroke="{BLUE}" stroke-width="5" marker-end="url(#arrow)"/>',
        text(60, 1214, "Source: RTD final June changes · crosswalk rows 21, 22, 287", 25, color=MUTED),
        text(60, 1253, "Arrows show route identity; this is not a geographic map.", 26, color=MUTED),
    ]
    description = (
        f"The prior Route {east} split into an East Evans segment retaining Route {east} "
        f"and a western segment labeled Route {west}. {old} was renamed Route {new}. "
        "This figure follows the retained official-source crosswalk, and shows identity links "
        "rather than mapped route geometry, delivered service, or an added-route total."
    )
    return svg("RTD route identity: Route 21 split and LD3 rename", description, elements, 1300)

def build_figures(root):
    return {
        "artifacts/shiftforge/constraint-matrix.svg": build_shiftforge(root),
        "artifacts/colorado-transit-award-service/route-identity.svg": build_transit(root),
    }
