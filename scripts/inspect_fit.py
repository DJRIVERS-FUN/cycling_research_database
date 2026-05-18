from pathlib import Path
from fitparse import FitFile

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIT_DIR = PROJECT_ROOT / "raw" / "garmin_fit"

fit_file = next(FIT_DIR.glob("*.fit"))

print("Reading:", fit_file.name)

fit = FitFile(str(fit_file))

message_types = {}

for record in fit.get_messages():
    name = record.name
    message_types[name] = message_types.get(name, 0) + 1

print("\nMessage types:")
for k, v in sorted(message_types.items()):
    print(f"{k}: {v}")

print("\nFirst 5 record messages:\n")

count = 0

for record in fit.get_messages("record"):
    data = {}

    for field in record:
        data[field.name] = field.value

    print(data)

    count += 1

    if count >= 5:
        break
