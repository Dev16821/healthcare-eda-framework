"""Task 2 configuration. Points back to Task 1 cleaned outputs."""

from pathlib import Path

# Task 2 root
TASK2_DIR = Path(__file__).resolve().parent
OUTPUTS_DIR = TASK2_DIR / "outputs"
FIGURES_DIR = OUTPUTS_DIR / "figures"
REPORTS_DIR = OUTPUTS_DIR / "reports"

for d in [OUTPUTS_DIR, FIGURES_DIR, REPORTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Read cleaned data from Task 1
CLEANED_DATA = Path(
    TASK2_DIR.parent /
    "data-cleaning-pipeline-main" /
    "data" / "cleaned_data" /
    "cleaned_healthcare_messy_dataset.csv"
)

# If you also want to analyze engineering data:
ENGINEERING_CLEANED = Path(
    TASK2_DIR.parent /
    "data-cleaning-pipeline-main" /
    "data" / "cleaned_data" /
    "cleaned_engineering_messy_dataset.csv"
)

# Column groups (adjust if your Task 1 renamed columns)
NUMERIC_COLS = ["age", "bmi", "blood_pressure", "cholesterol", "glucose_level"]
CATEGORICAL_COLS = ["gender", "smoking_status", "health_risk"]
TARGET = "health_risk"

RISK_ORDER = ["low", "high"]

# Plotting
FIG_DPI = 300
FIG_STYLE = "seaborn-v0_8-whitegrid"
COLOR_MAP = "RdYlBu_r"