from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "processed"

GARMIN_EPOCH = pd.Timestamp("1989-12-31 00:00:00")
DI2_OFFSET_SECONDS = 631116007

fit_files = list(PROCESSED_DIR.glob("*_fit_samples.csv"))

if not fit_files:
    raise SystemExit("No FIT sample files found.")

for fit_file in fit_files:

    ride_id = fit_file.stem.replace("_fit_samples", "")
    di2_file = PROCESSED_DIR / f"{ride_id}_di2_samples.csv"

    if not di2_file.exists():
        print(f"Skipping {ride_id}: no matching Di2 file")
        continue

    print(f"\nMerging ride: {ride_id}")

    fit_df = pd.read_csv(fit_file)
    di2_df = pd.read_csv(di2_file)

    fit_df["timestamp_utc"] = pd.to_datetime(fit_df["timestamp_utc"])

    fit_df["timestamp_fit"] = (
        (fit_df["timestamp_utc"] - GARMIN_EPOCH)
        .dt.total_seconds()
        .astype(int)
        + DI2_OFFSET_SECONDS
    )

    fit_df = fit_df.sort_values("timestamp_fit")
    di2_df = di2_df.sort_values("timestamp_fit")

    merged = pd.merge_asof(
        fit_df,
        di2_df[[
            "timestamp_fit",
            "gear_raw",
            "gear_label",
            "front_gear_index",
            "rear_gear_index",
            "grade_percent"
        ]],
        on="timestamp_fit",
        direction="nearest",
        tolerance=10
    )

    out_file = PROCESSED_DIR / f"{ride_id}_merged.csv"
    merged.to_csv(out_file, index=False)

    matched = merged["gear_label"].notna().sum()

    print(f"Saved: {out_file}")
    print(f"Gear matches: {matched} / {len(merged)}")

print("\nAll merges complete.")
