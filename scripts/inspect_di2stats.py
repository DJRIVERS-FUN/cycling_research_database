from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DI2_DIR = PROJECT_ROOT / "raw" / "di2stats"

files = list(DI2_DIR.glob("*.xlsx"))

print("Di2stats files found:")
for f in files:
    print(" -", f.name)

if not files:
    raise SystemExit("No Di2stats .xlsx file found.")

file_path = files[0]
print("\nReading:", file_path)

xls = pd.ExcelFile(file_path)
print("\nSheets:", xls.sheet_names)

for sheet in xls.sheet_names:
    print(f"\n--- Sheet: {sheet} ---")
    df = pd.read_excel(file_path, sheet_name=sheet, header=None)
    print(df.head(30).to_string())
