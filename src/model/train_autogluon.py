import json
from pathlib import Path

import numpy as np
import pandas as pd
from autogluon.tabular import TabularPredictor
from sklearn.metrics import (
    mean_absolute_error,
    mean_absolute_percentage_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split


import subprocess
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "processed" / "car_ads_clean.csv"
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "Car_sale_ads.csv"
PREPROCESS_SCRIPT = PROJECT_ROOT / "src" / "data" / "preprocess.py"
MODEL_PATH = PROJECT_ROOT / "models" / "autogluon_price_model"
METRICS_PATH = PROJECT_ROOT / "models" / "autogluon_metrics.csv"
LEADERBOARD_PATH = PROJECT_ROOT / "models" / "autogluon_leaderboard.csv"

TARGET = "Price"

COLUMNS_TO_DROP = [
    "Index",
    "Currency",
    "Offer_publication_date",
    "Offer_location",
    "Features",
    "Vehicle_generation",
]


def _is_valid_csv(path: Path) -> bool:
    if not path.is_file():
        return False

    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        first_line = handle.readline().strip()
    return not first_line.startswith("version https://git-lfs.github.com/spec/v1")


def _ensure_processed_data() -> None:
    if _is_valid_csv(DATA_PATH):
        return

    if not RAW_DATA_PATH.is_file():
        raise FileNotFoundError(
            f"Missing raw data file: {RAW_DATA_PATH}. "
            "Ensure that the SUML-main directory contains the full raw data CSV file."
        )

    if not PREPROCESS_SCRIPT.is_file():
        raise FileNotFoundError(
            f"Preprocessing script not found: {PREPROCESS_SCRIPT}"
        )

    subprocess.run(
        [sys.executable, str(PREPROCESS_SCRIPT)],
        cwd=str(PROJECT_ROOT),
        check=True,
    )

    if not _is_valid_csv(DATA_PATH):
        raise RuntimeError(
            f"Raw data processing failed: {DATA_PATH}"
        )


def load_data():
    _ensure_processed_data()
    return pd.read_csv(DATA_PATH)


def prepare_data(data):
    data = data.drop(columns=COLUMNS_TO_DROP, errors="ignore")
    return data


def build_inference_defaults(data: pd.DataFrame) -> dict:
    features = data.drop(columns=[TARGET], errors="ignore")
    fuel_medians = (
        features.groupby("Fuel_type")[["Displacement_cm3", "CO2_emissions", "Doors_number"]]
        .median()
        .to_dict(orient="index")
    )

    return {
        "Condition": "Used",
        "Type": "sedan",
        "Drive": "Unknown",
        "Colour": "gray",
        "Origin_country": "Other",
        "Vehicle_model": "Other",
        "First_owner": 0,
        "Displacement_cm3": float(features["Displacement_cm3"].median()),
        "CO2_emissions": float(features["CO2_emissions"].median()),
        "Doors_number": float(features["Doors_number"].median()),
        "fuel_medians": fuel_medians,
    }


def evaluate_model(y_true, y_pred):
    return pd.DataFrame(
        {
            "metric": ["MAE", "RMSE", "R2", "MAPE"],
            "value": [
                mean_absolute_error(y_true, y_pred),
                np.sqrt(mean_squared_error(y_true, y_pred)),
                r2_score(y_true, y_pred),
                mean_absolute_percentage_error(y_true, y_pred),
            ],
        }
    )


def main():
    data = load_data()
    data = prepare_data(data)

    train_data, test_data = train_test_split(
        data,
        test_size=0.2,
        random_state=42,
    )

    predictor = TabularPredictor(
        label=TARGET,
        problem_type="regression",
        eval_metric="mean_absolute_error",
        path=str(MODEL_PATH),
    ).fit(
        train_data=train_data,
        time_limit=3600,
        presets="good_quality",
        dynamic_stacking=False,
    )

    X_test = test_data.drop(columns=[TARGET])
    y_test = test_data[TARGET]

    y_pred = predictor.predict(X_test)

    metrics = evaluate_model(y_test, y_pred)
    leaderboard = predictor.leaderboard(test_data, silent=True)

    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)

    metrics.to_csv(METRICS_PATH, index=False)
    leaderboard.to_csv(LEADERBOARD_PATH, index=False)

    defaults_path = MODEL_PATH / "inference_defaults.json"
    defaults_path.write_text(
        json.dumps(build_inference_defaults(train_data), indent=2),
        encoding="utf-8",
    )

    print(metrics.round(4).to_string(index=False))
    print(f"Saved inference defaults to: {defaults_path}")
    print(f"Saved AutoGluon model to: {MODEL_PATH}")
    print(f"Saved metrics to: {METRICS_PATH}")
    print(f"Saved leaderboard to: {LEADERBOARD_PATH}")


if __name__ == "__main__":
    main()