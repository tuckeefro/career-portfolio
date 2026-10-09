"""Reproduce an illustrative air-storage study with explicit flow and temperature bases."""
from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import io
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "artifacts" / "air-storage-study"
PSI_TO_PA = 6894.757293168
FT3_TO_M3 = 0.028316846592
US_GAL_TO_M3 = 0.003785411784
GAL_PER_FT3 = FT3_TO_M3 / US_GAL_TO_M3

def positive(value, name):
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be finite and positive")
    return value

def required_volume_gal(shortfall, seconds, pressure_band, reference_pa, tank_k, reference_k):
    if shortfall < 0 or seconds < 0:
        raise ValueError("Shortfall and event time cannot be negative")
    for value, name in ((pressure_band, "pressure band"), (reference_pa, "reference pressure"),
                        (tank_k, "tank temperature"), (reference_k, "reference temperature")):
        positive(value, name)
    return (reference_pa / PSI_TO_PA) * shortfall * (seconds / 60) / pressure_band * GAL_PER_FT3 * tank_k / reference_k

def buffer_seconds(volume_gal, shortfall, pressure_band, reference_pa, tank_k, reference_k):
    positive(volume_gal, "storage volume")
    if shortfall < 0:
        raise ValueError("Shortfall cannot be negative")
    if shortfall == 0:
        return None
    return volume_gal / required_volume_gal(shortfall, 1, pressure_band, reference_pa, tank_k, reference_k)

def csv_record(fields, rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({key: f"{value:.9f}" if isinstance(value, float) else value for key, value in row.items()})
    return stream.getvalue()

def study(root=ROOT):
    directory = root / "artifacts" / "air-storage-study"
    raw_inputs = (directory / "inputs.json").read_bytes()
    inputs = json.loads(raw_inputs)
    if inputs["format"] != "career-portfolio-air-storage-inputs-v1" or inputs["historical_equipment_inputs"] is not False:
        raise ValueError("Review this standalone study when its input format or historical scope changes")
    reference, receiver, sweep, event = (inputs[key] for key in ("reference", "receiver", "sweep", "transient"))
    band = positive(receiver["initial_gauge_psi"] - receiver["minimum_gauge_psi"], "pressure band")
    arguments = (band, reference["pressure_pa"], receiver["temperature_k"], reference["temperature_k"])
    required = lambda shortfall, seconds: required_volume_gal(shortfall, seconds, *arguments)
    available = lambda volume, shortfall: buffer_seconds(volume, shortfall, *arguments)
    for values in (sweep["volumes_us_gal"], sweep["shortfalls_ref_cfm"], sweep["grid_shortfalls_ref_cfm"], sweep["durations_s"], event["volumes_us_gal"]):
        if len(values) != len(set(values)) or values != sorted(values):
            raise ValueError("Sweep values must be unique and increasing")
        for value in values:
            positive(value, "sweep input")
    deficit = positive(event["burst_demand_ref_cfm"] - event["compressor_ref_cfm"], "burst shortfall")
    surplus = positive(event["compressor_ref_cfm"] - event["post_burst_demand_ref_cfm"], "recovery margin")
    duration = positive(event["burst_duration_s"], "burst duration")
    for key in ("compressor_ref_cfm", "burst_demand_ref_cfm", "post_burst_demand_ref_cfm"):
        positive(event[key], key)
    recovery = duration * deficit / surplus
    required_event_volume = required(deficit, duration)
    buffers = [
        {"volume_us_gal": volume, "shortfall_ref_cfm": shortfall, "time_to_floor_s": available(volume, shortfall)}
        for volume in sweep["volumes_us_gal"] for shortfall in sweep["shortfalls_ref_cfm"]
    ]
    sizing = [
        {"shortfall_ref_cfm": shortfall, "duration_s": seconds, "required_volume_us_gal": required(shortfall, seconds)}
        for shortfall in sweep["grid_shortfalls_ref_cfm"] for seconds in sweep["durations_s"]
    ]
    traces, examples = [], []
    for volume in event["volumes_us_gal"]:
        time_to_floor = available(volume, deficit)
        meets_duration = time_to_floor >= duration
        drop_per_s = band / time_to_floor
        final_pressure = receiver["initial_gauge_psi"] - drop_per_s * duration
        stop = duration + recovery if meets_duration else time_to_floor
        times = sorted(set([float(t) for t in range(int(stop) + 1)] + [stop]))
        for seconds in times:
            if seconds <= duration:
                pressure = receiver["initial_gauge_psi"] - drop_per_s * seconds
                phase, flow = "burst", -deficit
            else:
                pressure = min(receiver["initial_gauge_psi"], final_pressure + drop_per_s * surplus / deficit * (seconds - duration))
                phase, flow = "recovery", surplus
            if pressure < receiver["minimum_gauge_psi"] - 1e-8:
                raise ValueError("Pressure trace escaped the modeled operating range")
            traces.append({"volume_us_gal": volume, "time_s": seconds, "phase": phase, "pressure_psig": pressure, "net_flow_ref_cfm": flow})
        examples.append({
            "volume_us_gal": volume, "time_to_floor_s": round(time_to_floor, 9),
            "meets_burst_duration_in_model": meets_duration,
            "burst_end_pressure_psig": round(final_pressure, 9) if meets_duration else None,
            "recovery_time_s": round(recovery, 9) if meets_duration else None,
            "trace_stops_at_floor": not meets_duration,
        })

    checks = []
    def check(name, condition):
        if not condition:
            raise ValueError(f"Air-storage model check failed: {name}")
        checks.append({"name": name, "passed": True})
    close = lambda left, right: math.isclose(left, right, rel_tol=1e-10, abs_tol=1e-8)
    check("US gallon / cubic-foot conversion", close(GAL_PER_FT3, 1728 / 231))
    check("80-gal reference case", close(buffer_seconds(80, 40, 20, 101325, 293.15, 293.15), 21.831413421084626))
    check("Volume-time inverse", close(required(deficit, available(80, deficit)), 80))
    check("Double volume doubles time", close(available(160, deficit), 2 * available(80, deficit)))
    check("Double shortfall halves time", close(available(80, 2 * deficit), available(80, deficit) / 2))
    check("Zero shortfall has no inventory depletion", available(80, 0) is None)
    check("Zero event duration requires no buffer", required(deficit, 0) == 0)
    check("Double pressure band doubles buffer time",
          close(buffer_seconds(80, deficit, band * 2, *arguments[1:]), 2 * available(80, deficit)))
    si_volume_m3 = reference["pressure_pa"] * (deficit * FT3_TO_M3 / 60) * duration / (band * PSI_TO_PA) * receiver["temperature_k"] / reference["temperature_k"]
    check("Independent SI volume agrees", close(si_volume_m3 / US_GAL_TO_M3, required_event_volume))
    check("Recovery conserves reference-air inventory", close(surplus * recovery / 60, deficit * duration / 60))
    check("Receiver-temperature factor",
          close(required_volume_gal(deficit, duration, band, reference["pressure_pa"], receiver["temperature_k"] * 1.1, reference["temperature_k"]), required_event_volume * 1.1))
    for example in examples:
        rows = [row for row in traces if row["volume_us_gal"] == example["volume_us_gal"]]
        endpoint = receiver["initial_gauge_psi"] if example["meets_burst_duration_in_model"] else receiver["minimum_gauge_psi"]
        check(f'{example["volume_us_gal"]}-gal trace endpoint', close(rows[-1]["pressure_psig"], endpoint))

    record = {
        "format": "career-portfolio-air-storage-results-v1",
        "inputs_sha256": hashlib.sha256(raw_inputs).hexdigest(),
        "scope": "Analytical outputs for illustrative inputs; no plant measurement or historical system validation.",
        "reference_pressure_psia": round(reference["pressure_pa"] / PSI_TO_PA, 12),
        "pressure_band_psi": band,
        "worked_event": {
            "shortfall_ref_cfm": deficit, "duration_s": duration,
            "reference_air_inventory_ft3": deficit * duration / 60,
            "required_total_volume_us_gal": round(required_event_volume, 9),
            "recovery_margin_ref_cfm": surplus, "recovery_time_s": round(recovery, 9),
            "receivers": examples,
        },
        "checks": checks,
    }
    records = {
        "results.json": json.dumps(record, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        "buffer-times.csv": csv_record(("volume_us_gal", "shortfall_ref_cfm", "time_to_floor_s"), buffers),
        "required-volumes.csv": csv_record(("shortfall_ref_cfm", "duration_s", "required_volume_us_gal"), sizing),
        "pressure-trace.csv": csv_record(("volume_us_gal", "time_s", "phase", "pressure_psig", "net_flow_ref_cfm"), traces),
    }
    return inputs, record, buffers, sizing, traces, records

def verify_records(root=ROOT):
    result = study(root)
    directory = root / "artifacts" / "air-storage-study"
    for name, content in result[-1].items():
        path = directory / name
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            raise ValueError(f"STALE_STUDY_RECORD {name}: run air_storage_model.py --write-records")
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write-records", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--emit-records", action="store_true")
    args = parser.parse_args()
    result = study() if args.write_records else verify_records()
    if args.write_records:
        for name, content in result[-1].items():
            (DIRECTORY / name).write_text(content, encoding="utf-8")
    if args.emit_records:
        for name, content in result[-1].items():
            encoded = base64.b64encode(content.encode("utf-8")).decode("ascii")
            print(f"PORTFOLIO_RECORD_BEGIN artifacts/air-storage-study/{name}")
            for offset in range(0, len(encoded), 120):
                print(encoded[offset:offset + 120])
            print("PORTFOLIO_RECORD_END")
    print(f'Verified air-storage calculations: {len(result[1]["checks"])} checks; required volume {result[1]["worked_event"]["required_total_volume_us_gal"]:.3f} US gal.')
