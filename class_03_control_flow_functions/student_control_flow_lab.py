"""
Charlotte Projects | Week 9 · Class 3
Synthetic Multi-Well Pressure Surveillance Lab

Note: Threshold categories (< 2500 low, 2500-3499 normal, >= 3500 high)
are fictional classroom examples, not real field safety limits.
"""

READINGS = [
    {"well_id": "WELL-07", "pressure_psi": 3100, "status": "active"},
    {"well_id": "WELL-08", "pressure_psi": 2750, "status": "active"},
    {"well_id": "WELL-09", "pressure_psi": 3000, "status": "inactive"},
    {"well_id": "WELL-10", "pressure_psi": 2895, "status": "active"},
    {"well_id": "WELL-11", "pressure_psi": None, "status": "active"},
    {"well_id": "WELL-07", "pressure_psi": 3260, "status": "active"},
    {"well_id": "WELL-12", "pressure_psi": 2600, "status": "inactive"},
    {"well_id": "WELL-08", "pressure_psi": 2840, "status": "active"},
    {"well_id": "WELL-13", "pressure_psi": -15,  "status": "active"},
    {"well_id": "WELL-10", "pressure_psi": 4100, "status": "active"},
]


# --- Part A: Decisions ---
def classify_pressure(pressure_psi):
    """Classify pressure_psi into fictional training categories."""
    if pressure_psi is None or pressure_psi < 0:
        return "invalid"
    if pressure_psi >= 3500:
        return "high"
    if pressure_psi >= 2500:
        return "normal"
    return "low"


# --- Part C: Reusable Conversion Function ---
def psi_to_kpa(pressure_psi):
    """Convert nonnegative pressure from psi to kPa; return None if invalid."""
    if pressure_psi is None or pressure_psi < 0:
        return None
    return pressure_psi * 6.8947572932


def main():
    # Part A boundary checks
    print("=== Boundary Checks ===")
    for test_val in [None, -1, 0, 2499, 2500, 3499, 3500]:
        print(f"Input: {test_val!r:>6} -> {classify_pressure(test_val)}")

    # Part B: Loop over all 10 readings (including inactive and repeated wells)
    print("\n=== All 10 Observations ===")
    for reading in READINGS:
        well_id = reading["well_id"]
        pressure = reading["pressure_psi"]
        label = classify_pressure(pressure)
        print(f"{well_id} | {pressure} psi | {label}")

    # Part C: Unit conversion check (parameter: pressure_psi, argument: 3150)
    print("\n=== Unit Conversion Check ===")
    converted_kpa = psi_to_kpa(3150)
    print(f"3150 psi = {converted_kpa:.2f} kPa")

    # Part D: Filter active valid readings and summarize by well
    print("\n=== Active Valid Well Summary ===")
    totals = {}
    counts = {}
    valid_count = 0
    skipped_count = 0

    for reading in READINGS:
        pressure = reading["pressure_psi"]
        if reading["status"] != "active" or pressure is None or pressure < 0:
            skipped_count += 1
            continue

        valid_count += 1
        well_id = reading["well_id"]
        totals[well_id] = totals.get(well_id, 0) + pressure
        counts[well_id] = counts.get(well_id, 0) + 1

    print(f"Active valid: {valid_count}; Skipped: {skipped_count}")
    for well_id in sorted(totals):
        avg_psi = totals[well_id] / counts[well_id]
        print(f"{well_id}: {avg_psi:.2f} psi")


if __name__ == "__main__":
    main()
