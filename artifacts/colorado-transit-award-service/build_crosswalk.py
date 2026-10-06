#!/usr/bin/env python3
"""Validate and summarize the transcribed official RTD service changes."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "route-service-crosswalk.csv"


def main() -> None:
    with INPUT.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        raise SystemExit("crosswalk is empty")
    routes = [r["route_key"] for r in rows]
    if len(routes) != len(set(routes)):
        raise SystemExit("duplicate normalized route key")

    measurable = 0
    for row in rows:
        before = row["derived_frequency_rate_before_per_hour"]
        after = row["derived_frequency_rate_after_per_hour"]
        delta = row["derived_rate_change_per_hour"]
        pct = row["derived_percent_change"]
        if before and after:
            b, a = float(before), float(after)
            if abs((a - b) - float(delta)) > 1e-4:
                raise SystemExit(f"incorrect rate delta for {row['route_key']}")
            if abs(((a / b - 1) * 100) - float(pct)) > 1e-4:
                raise SystemExit(f"incorrect rate percentage for {row['route_key']}")
            measurable += 1
        elif any((after, delta, pct)):
            raise SystemExit(f"partial frequency calculation for {row['route_key']}")

    june = {r["route_key"] for r in rows if r["rtd_june_award_linked_list"] == "yes"}
    september = {r["route_key"] for r in rows if r["rtd_sep9_funding_continuity_list"] == "yes"}
    overlap = june & september
    if (len(june), len(september), len(overlap)) != (12, 9, 8):
        raise SystemExit("route-list transcription changed: recheck official source lists")
    print(f"route rows={len(rows)}; June labels={len(june)}; Sep labels={len(september)}")
    print(f"normalized exact overlap={len(overlap)}: {', '.join(sorted(overlap))}")
    print(f"frequency-rate comparisons={measurable}; no aggregate vehicle-hours or grant cost/unit inferred")
    for r in rows:
        if r["derived_percent_change"]:
            print(f"{r['route_key']}: {r['derived_percent_change']}% implied scheduled frequency-rate change")


if __name__ == "__main__":
    main()
