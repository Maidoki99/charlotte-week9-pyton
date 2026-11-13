"""Unit tests for Week 9 Class 5 Drilling Telemetry Capstone."""
import csv
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from telemetry_capstone import (
    convert_pressure,
    convert_temperature,
    parse_record,
    process_lines,
    run,
    summarize_by_well,
)


class TelemetryCapstoneTests(unittest.TestCase):
    def test_pressure_known_value(self):
        self.assertAlmostEqual(convert_pressure(100, "psi"), 689.47572932, places=5)
        self.assertAlmostEqual(convert_pressure(2190, "kPa"), 2190.0, places=5)
        self.assertEqual(convert_pressure(0, "psi"), 0.0)

    def test_pressure_rejects_negative_and_bad_unit(self):
        with self.assertRaises(ValueError):
            convert_pressure(-10, "psi")
        with self.assertRaises(ValueError):
            convert_pressure(100, "bar")

    def test_temperature_known_value(self):
        self.assertAlmostEqual(convert_temperature(212, "F"), 100.0, places=5)
        self.assertAlmostEqual(convert_temperature(32, "F"), 0.0, places=5)
        self.assertAlmostEqual(convert_temperature(86, "C"), 86.0, places=5)

    def test_temperature_rejects_bad_unit(self):
        with self.assertRaises(ValueError):
            convert_temperature(210, "K")

    def test_parse_record_valid_and_rounding(self):
        line = " 2026-10-08T08:00:00 | WELL-101 | 3150 | psi | 194 | F | ACTIVE "
        parsed = parse_record(line)
        self.assertEqual(parsed["timestamp"], "2026-10-08T08:00:00")
        self.assertEqual(parsed["well_id"], "WELL-101")
        self.assertEqual(parsed["pressure_kpa"], 21718.49)
        self.assertEqual(parsed["temperature_c"], 90.0)
        self.assertEqual(parsed["status"], "ACTIVE")

    def test_parse_record_malformed_cases(self):
        malformed_lines = [
            "2026-10-08T08:55:00|WELL-106|3125|psi|199|F",
            "|WELL-101|3150|psi|194|F|ACTIVE",
            "2026-10-08T08:00:00||3150|psi|194|F|ACTIVE",
            "2026-10-08T08:30:00|WELL-104|bad|psi|202|F|ACTIVE",
            "2026-10-08T09:05:00|WELL-107|3000|psi||F|ACTIVE",
            "2026-10-08T09:35:00|WELL-110|3100|psi|198|F|PAUSED",
        ]
        for bad_line in malformed_lines:
            with self.subTest(bad_line=bad_line):
                with self.assertRaises(ValueError):
                    parse_record(bad_line)

    def test_process_lines_preserves_line_numbers_with_blank_lines(self):
        lines = [
            "2026-10-08T08:00:00|WELL-101|3150|psi|194|F|ACTIVE\n",
            "\n",
            "2026-10-08T08:30:00|WELL-104|bad|psi|202|F|ACTIVE\n",
        ]
        accepted, rejected = process_lines(lines)
        self.assertEqual(len(accepted), 1)
        self.assertEqual(len(rejected), 1)
        self.assertEqual(rejected[0]["line_number"], 3)

    def test_summarize_by_well_active_only_and_sorted(self):
        records = [
            {"well_id": "WELL-102", "pressure_kpa": 2000.0, "status": "ACTIVE"},
            {"well_id": "WELL-102", "pressure_kpa": 9999.0, "status": "INACTIVE"},
            {"well_id": "WELL-101", "pressure_kpa": 1000.0, "status": "ACTIVE"},
            {"well_id": "WELL-101", "pressure_kpa": 1500.0, "status": "ACTIVE"},
        ]
        summary = summarize_by_well(records)
        self.assertEqual(len(summary), 2)
        self.assertEqual(summary[0], {"well_id": "WELL-101", "active_readings": 2, "avg_pressure_kpa": 1250.0})
        self.assertEqual(summary[1], {"well_id": "WELL-102", "active_readings": 1, "avg_pressure_kpa": 2000.0})

    def test_end_to_end_run(self):
        dataset_path = Path(__file__).resolve().parents[1] / "data" / "drilling_telemetry_capstone.txt"
        with tempfile.TemporaryDirectory() as tmp_dir:
            accepted, rejected, summary = run(dataset_path, tmp_dir)
            self.assertEqual(len(accepted), 13)
            self.assertEqual(len(rejected), 7)
            self.assertEqual(len(summary), 5)

            out_path = Path(tmp_dir)
            self.assertTrue((out_path / "cleaned_telemetry.csv").exists())
            self.assertTrue((out_path / "rejected_records.csv").exists())
            self.assertTrue((out_path / "well_summary.csv").exists())

            with (out_path / "well_summary.csv").open("r", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
                self.assertEqual([r["well_id"] for r in rows], ["WELL-101", "WELL-102", "WELL-103", "WELL-104", "WELL-108"])


if __name__ == "__main__":
    unittest.main()
