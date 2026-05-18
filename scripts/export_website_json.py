from pathlib import Path
import pandas as pd
import json

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PROCESSED_DIR = PROJECT_ROOT / "processed"
WEBSITE_JSON_DIR = PROJECT_ROOT / "website_json"

WEBSITE_JSON_DIR.mkdir(exist_ok=True)

merged_files = list(PROCESSED_DIR.glob("*_merged.csv"))

if not merged_files:
    raise SystemExit("No merged ride files found.")

ride_index = []

for file_path in merged_files:

    ride_id = file_path.stem.replace("_merged", "")

    print(f"Exporting: {ride_id}")

    df = pd.read_csv(file_path)

    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
    df[numeric_cols] = df[numeric_cols].round(3)

    df = df.astype(object).where(pd.notnull(df), None)

    summary = {
        "ride_id": ride_id,
        "samples": len(df),
        "distance_km": round(pd.read_csv(file_path)["distance_m"].max() / 1000, 2),
        "avg_power_w": round(pd.read_csv(file_path)["power_w"].mean(), 1),
        "avg_speed_kph": round(pd.read_csv(file_path)["speed_kph"].mean(), 1),
        "max_speed_kph": round(pd.read_csv(file_path)["speed_kph"].max(), 1),
        "avg_cadence_rpm": round(pd.read_csv(file_path)["cadence_rpm"].mean(), 1),
    }

    ride_index.append(summary)

    payload = {
        "summary": summary,
        "samples": df.to_dict(orient="records")
    }

    out_json = WEBSITE_JSON_DIR / f"{ride_id}.json"

    with open(out_json, "w") as f:
        json.dump(payload, f, allow_nan=False)

    print(f"Saved: {out_json}")

index_path = WEBSITE_JSON_DIR / "rides.json"

with open(index_path, "w") as f:
    json.dump(ride_index, f, allow_nan=False)

print(f"\nSaved ride index: {index_path}")
