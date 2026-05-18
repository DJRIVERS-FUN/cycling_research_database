from pathlib import Path
import pandas as pd
from fitparse import FitFile

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIT_DIR = PROJECT_ROOT / "raw" / "garmin_fit"
PROCESSED_DIR = PROJECT_ROOT / "processed"
PROCESSED_DIR.mkdir(exist_ok=True)

fit_path = next(FIT_DIR.glob("*.fit"))
ride_id = fit_path.stem

fit = FitFile(str(fit_path))

records = []

for record in fit.get_messages("record"):
    row = {}
    for field in record:
        row[field.name] = field.value
    records.append(row)

df = pd.DataFrame(records)

# Rename to canonical database names
df = df.rename(columns={
    "timestamp": "timestamp_utc",
    "distance": "distance_m",
    "enhanced_speed": "speed_mps",
    "enhanced_altitude": "elevation_m",
    "cadence": "cadence_rpm",
    "power": "power_w",
    "heart_rate": "heart_rate_bpm",
    "temperature": "temperature_c",
    "position_lat": "latitude_semicircles",
    "position_long": "longitude_semicircles",
})

df.insert(0, "ride_id", ride_id)
df.insert(1, "sample_index", range(len(df)))

# Derived fields
if "speed_mps" in df.columns:
    df["speed_kph"] = df["speed_mps"] * 3.6

if "latitude_semicircles" in df.columns:
    df["latitude_deg"] = df["latitude_semicircles"] * 180 / 2**31

if "longitude_semicircles" in df.columns:
    df["longitude_deg"] = df["longitude_semicircles"] * 180 / 2**31

out_path = PROCESSED_DIR / f"{ride_id}_fit_samples.csv"
df.to_csv(out_path, index=False)

print("Parsed FIT file:", fit_path.name)
print("Ride ID:", ride_id)
print("Rows:", len(df))
print("Columns:")
for c in df.columns:
    print(" -", c)
print("Saved:", out_path)
