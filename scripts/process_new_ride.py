from pathlib import Path
import subprocess

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SCRIPTS = [
    "parse_di2stats.py",
    "parse_fit.py",
    "merge_fit_di2.py"
]

print("\n=== Cycling Research Database Pipeline ===\n")

for script in SCRIPTS:
    script_path = PROJECT_ROOT / "scripts" / script

    print(f"\nRunning: {script}")

    result = subprocess.run(
        ["python3", str(script_path)],
        cwd=PROJECT_ROOT
    )

    if result.returncode != 0:
        print(f"\nERROR in {script}")
        break

print("\nPipeline complete.\n")
