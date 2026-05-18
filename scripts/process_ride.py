"""
Core ingestion script for the Cycling Research Database.

Planned functionality:
- Import Strava JSON metadata
- Parse Garmin FIT files
- Parse GPX tracks
- Parse Di2stats Excel exports
- Merge time-series streams
- Generate processed CSV/SQLite/Parquet outputs
- Export lightweight website JSON
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DIR = PROJECT_ROOT / "raw"
PROCESSED_DIR = PROJECT_ROOT / "processed"
WEBSITE_JSON_DIR = PROJECT_ROOT / "website_json"


def main():
    print("Cycling Research Database")
    print("Project root:", PROJECT_ROOT)
    print("Ready for ingestion pipeline setup")


if __name__ == "__main__":
    main()
