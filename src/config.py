from pathlib import Path

def find_project_root(start=None):
    if start is None:
        start = Path.cwd().resolve()

    for p in [start, *start.parents]:
        if (p / "README.md").exists() and (p / "data").exists() and (p / "src").exists():
            return p
    raise FileNotFoundError("Khong tim thay project root.")

PROJECT_ROOT = find_project_root()

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
SUBMISSIONS_DIR = DATA_DIR / "submissions"

MASTER_DIR = RAW_DIR / "master"
TRANSACTION_DIR = RAW_DIR / "transaction"
OPERATIONAL_DIR = RAW_DIR / "operational"
ANALYTICAL_DIR = RAW_DIR / "analytical"

NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
FINAL_REPORT_DIR = REPORTS_DIR / "final"

ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
CLEANED_DATA_DIR = ARTIFACTS_DIR / "cleaned_data"

SRC_DIR = PROJECT_ROOT / "src"