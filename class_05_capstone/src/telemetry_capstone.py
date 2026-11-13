"""Week 9 Class 5: Drilling Telemetry Data Processing System."""
import csv
import sys
from pathlib import Path

PSI_TO_KPA = 6.8947572932


def convert_pressure(value, unit):
    """Return pressure in kPa; reject negative values or unsupported units."""
    if value < 0:
        raise ValueError("Negative pressure is not allowed")

    normalized_unit = unit.strip().lower()
    if normalized_unit == "psi":
        return value * PSI_TO_KPA
    if normalized_unit == "kpa":
        return float(value)

    raise ValueError(f"Unsupported pressure unit: {unit}")


def convert_temperature(value, unit):
    """Return temperature in degrees Celsius; reject unsupported units."""
    normalized_unit = unit.strip().upper()
    if normalized_unit == "F":
        return (value - 32.0) * 5.0 / 9.0
    if normalized_unit == "C":
        return float(value)

    raise ValueError(f"Unsupported temperature unit: {unit}")


def parse_record(raw_line):
    """Return normalized dictionary; raise ValueError for malformed records."""
    cleaned_line = raw_line.strip()
    parts = [part.strip() for part in cleaned_line.split("|")]

    if len(parts) != 7:
        raise ValueError(f"Expected 7 fields, got {len(parts)}")

    timestamp, well_id, pressure_raw, pressure_unit, temp_raw, temp_unit, status_raw = parts

    if not timestamp:
        raise ValueError("Blank timestamp")
    if not well_id:
        raise ValueError("Blank well ID")

    try:
        pressure_val = float(pressure_raw)
    except ValueError as exc:
        raise ValueError(f"Non-numeric pressure: {pressure_raw}") from exc

    try:
        temp_val = float(temp_raw)
    except ValueError as exc:
        raise ValueError(f"Non-numeric temperature: {temp_raw}") from exc

    status = status_raw.upper()
    if status not in ("ACTIVE", "INACTIVE"):
        raise ValueError(f"Invalid status: {status_raw}")

    pressure_kpa = round(convert_pressure(pressure_val, pressure_unit), 2)
    temperature_c = round(convert_temperature(temp_val, temp_unit), 2)

    return {
        "timestamp": timestamp,
        "well_id": well_id,
        "pressure_kpa": pressure_kpa,
        "temperature_c": temperature_c,
        "status": status,
    }


def process_lines(lines):
    """Return (accepted_records, rejected_records) preserving source line numbers."""
    accepted = []
    rejected = []

    for line_number, line in enumerate(lines, start=1):
        raw_record = line.rstrip("\r\n")
        if not raw_record.strip():
            continue

        try:
            record = parse_record(raw_record)
            accepted.append(record)
        except ValueError as err:
            rejected.append({
                "line_number": line_number,
                "reason": str(err),
                "raw_record": raw_record,
            })

    return accepted, rejected


def summarize_by_well(records):
    """Average pressure for ACTIVE records, sorted by well ID."""
    well_totals = {}

    for record in records:
        if record["status"] != "ACTIVE":
            continue
        well_id = record["well_id"]
        if well_id not in well_totals:
            well_totals[well_id] = [0.0, 0]
        well_totals[well_id][0] += record["pressure_kpa"]
        well_totals[well_id][1] += 1

    summary = []
    for well_id in sorted(well_totals.keys()):
        total_pressure, count = well_totals[well_id]
        summary.append({
            "well_id": well_id,
            "active_readings": count,
            "avg_pressure_kpa": round(total_pressure / count, 2),
        })

    return summary


def write_csv(path, fieldnames, records):
    """Create output CSV with a header row."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def run(input_path, output_dir):
    """Generate cleaned_telemetry.csv, rejected_records.csv, well_summary.csv."""
    source_path = Path(input_path)
    out_folder = Path(output_dir)

    with source_path.open("r", encoding="utf-8") as infile:
        accepted, rejected = process_lines(infile)

    well_summary = summarize_by_well(accepted)

    write_csv(
        out_folder / "cleaned_telemetry.csv",
        ["timestamp", "well_id", "pressure_kpa", "temperature_c", "status"],
        accepted,
    )
    write_csv(
        out_folder / "rejected_records.csv",
        ["line_number", "reason", "raw_record"],
        rejected,
    )
    write_csv(
        out_folder / "well_summary.csv",
        ["well_id", "active_readings", "avg_pressure_kpa"],
        well_summary,
    )

    return accepted, rejected, well_summary


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python src/telemetry_capstone.py <input_file> <output_dir>")
        sys.exit(1)

    accepted_rows, rejected_rows, summary_rows = run(sys.argv[1], sys.argv[2])
    print(
        f"Processed telemetry: {len(accepted_rows)} accepted, "
        f"{len(rejected_rows)} rejected, {len(summary_rows)} active wells summarized."
    )
