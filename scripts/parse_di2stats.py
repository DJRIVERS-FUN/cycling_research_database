from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DI2_DIR = PROJECT_ROOT / "raw" / "di2stats"
PROCESSED_DIR = PROJECT_ROOT / "processed"
PROCESSED_DIR.mkdir(exist_ok=True)

file_path = next(DI2_DIR.glob("*.xlsx"))

ride_id = file_path.stem.replace("_di2", "")

# Gear summary: header row is Excel row 2 / pandas row 1
gear_summary = pd.read_excel(file_path, header=1, nrows=12)

gear_summary = gear_summary.rename(columns={
    "Gear": "gear_label",
    "GearInches": "gear_inches",
    "Total Time": "total_time_s",
    "Avg Time": "avg_time_s",
    "Count": "count",
    "Avg Grade": "avg_grade_decimal",
    "Avg HR": "avg_heart_rate_bpm",
    "Min HR": "min_heart_rate_bpm",
    "Max HR": "max_heart_rate_bpm",
    "Avg CAD": "avg_cadence_rpm",
    "Max CAD": "max_cadence_rpm",
    "Avg POW": "avg_power_w",
    "Max POW": "max_power_w",
    "Avg KPH": "avg_speed_kph",
    "Max KPH": "max_speed_kph",
})

gear_summary.insert(0, "ride_id", ride_id)

# Raw records: header row is Excel row 22 / pandas row 21
raw = pd.read_excel(file_path, header=21)

raw = raw.dropna(axis=1, how="all")

raw = raw.rename(columns={
    "TS": "timestamp_fit",
    "Gear": "gear_raw",
    "SPD": "speed_mps",
    "ELEV": "elevation_m",
    "GRADE": "grade_decimal",
    "CAD": "cadence_rpm",
    "POW": "power_w",
    "HR": "heart_rate_bpm",
    "DIST": "distance_m",
    "DegC": "temperature_c",
    "LAT": "latitude_semicircles",
    "LNG": "longitude_semicircles",
})

raw.insert(0, "ride_id", ride_id)
raw.insert(1, "sample_index", range(len(raw)))

# Derived readable fields
raw["speed_kph"] = raw["speed_mps"] * 3.6
raw["grade_percent"] = raw["grade_decimal"] * 100
raw["latitude_deg"] = raw["latitude_semicircles"] * 180 / 2**31
raw["longitude_deg"] = raw["longitude_semicircles"] * 180 / 2**31

# Parse gear string: e.g. 1x15,1,10
gear_parts = raw["gear_raw"].astype(str).str.extract(r"(?P<gear_label>[^,]+),(?P<front_gear_index>\d+),(?P<rear_gear_index>\d+)")
raw = pd.concat([raw, gear_parts], axis=1)

# Export
gear_out = PROCESSED_DIR / f"{ride_id}_gear_summary.csv"
raw_out = PROCESSED_DIR / f"{ride_id}_di2_samples.csv"

gear_summary.to_csv(gear_out, index=False)
raw.to_csv(raw_out, index=False)

print("Parsed Di2stats file:", file_path.name)
print("Ride ID:", ride_id)
print("Gear summary rows:", len(gear_summary))
print("Raw sample rows:", len(raw))
print("Saved:", gear_out)
print("Saved:", raw_out)
