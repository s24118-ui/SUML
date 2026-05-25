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


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "processed" / "car_ads_clean.csv"
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


def load_data():
    return pd.read_csv(DATA_PATH)


def prepare_data(data):
    data = data.drop(columns=COLUMNS_TO_DROP, errors="ignore")
    return data


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

    print(metrics.round(4).to_string(index=False))
    print(f"Saved AutoGluon model to: {MODEL_PATH}")
    print(f"Saved metrics to: {METRICS_PATH}")
    print(f"Saved leaderboard to: {LEADERBOARD_PATH}")


if __name__ == "__main__":
    main()