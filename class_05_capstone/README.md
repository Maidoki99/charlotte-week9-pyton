# Drilling Telemetry Data Processing System (Week 9 · Class 5 Capstone)

Command-line Python application that validates raw pipe-delimited drilling telemetry logs, converts pressure (`psi` to `kPa`) and temperature (`F` to `C`) using only the Python standard library, logs malformed records with 1-based line numbers, and generates per-well active pressure summaries.

## Project Structure
- `src/telemetry_capstone.py` — Core parser, unit converters, validator, and CSV exporter.
- `tests/test_telemetry_capstone.py` — `unittest` suite covering unit conversions, malformed records, line tracking, active well summaries, and end-to-end execution.
- `data/drilling_telemetry_capstone.txt` — Synthetic 20-line telemetry dataset.

## How to Run
From inside `class_05_capstone/`:
```bash
python src/telemetry_capstone.py data/drilling_telemetry_capstone.txt outputs
```

### Generated Output Files
- `outputs/cleaned_telemetry.csv` (`timestamp, well_id, pressure_kpa, temperature_c, status`)
- `outputs/rejected_records.csv` (`line_number, reason, raw_record`)
- `outputs/well_summary.csv` (`well_id, active_readings, avg_pressure_kpa`)

## How to Test
```bash
python -m unittest discover -s tests -v
```
