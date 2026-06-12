from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_absolute_percentage_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "processed" / "car_ads_clean.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "random_forest_baseline.joblib"
METRICS_PATH = PROJECT_ROOT / "models" / "random_forest_baseline_metrics.csv"

TARGET = "Price"
RANDOM_STATE = 42
TEST_SIZE = 0.2

COLUMNS_TO_DROP = [
    "Index",
    "Currency",
    "Offer_publication_date",
    "Offer_location",
    "Features",
    "Vehicle_generation",
]

ONE_HOT_FEATURES = [
    "Condition",
    "Fuel_type",
    "Drive",
    "Transmission",
    "Type",
]

FREQUENCY_FEATURES = [
    "Colour",
    "Origin_country",
    "Vehicle_brand",
    "Vehicle_model",
]


def make_one_hot_encoder():
    params = {"handle_unknown": "ignore", "sparse_output": False}
    try:
        return OneHotEncoder(**params)
    except TypeError:
        params.pop("sparse_output")
        params["sparse"] = False
        return OneHotEncoder(**params)


def load_data():
    return pd.read_csv(DATA_PATH)


def prepare_features(data):
    X = data.drop(columns=[TARGET])
    y = data[TARGET]

    X = X.drop(columns=COLUMNS_TO_DROP, errors="ignore")

    return X, y


def validate_columns(X):
    required_columns = ONE_HOT_FEATURES + FREQUENCY_FEATURES
    missing_columns = [column for column in required_columns if column not in X.columns]

    if missing_columns:
        raise ValueError(f"Brakuje wymaganych kolumn: {missing_columns}")


def build_frequency_maps(X_train):
    frequency_maps = {}

    for column in FREQUENCY_FEATURES:
        frequency_maps[column] = X_train[column].value_counts(normalize=True).to_dict()

    return frequency_maps


def apply_frequency_encoding(X, frequency_maps):
    X_encoded = X.copy()

    for column, mapping in frequency_maps.items():
        X_encoded[column] = X_encoded[column].map(mapping).fillna(0.0)

    return X_encoded


def get_numeric_features(X):
    numeric_features = [column for column in X.columns if column not in ONE_HOT_FEATURES]

    non_numeric_columns = (
        X[numeric_features]
        .select_dtypes(exclude=["number"])
        .columns
        .tolist()
    )

    if non_numeric_columns:
        raise ValueError(
            f"Po encodingu nadal zostaly niezakodowane kolumny: {non_numeric_columns}"
        )

    return numeric_features


def build_model(numeric_features):
    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", "passthrough", numeric_features),
            ("one_hot", make_one_hot_encoder(), ONE_HOT_FEATURES),
        ],
        remainder="drop",
    )

    random_forest = RandomForestRegressor(
        n_estimators=80,
        max_depth=24,
        min_samples_leaf=2,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", random_forest),
        ]
    )

    model = TransformedTargetRegressor(
        regressor=pipeline,
        func=np.log1p,
        inverse_func=np.expm1,
    )

    return model


def evaluate_model(y_true, y_pred):
    metrics = pd.DataFrame(
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

    return metrics


def main():
    data = load_data()
    X, y = prepare_features(data)

    validate_columns(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
    )

    frequency_maps = build_frequency_maps(X_train)

    X_train = apply_frequency_encoding(X_train, frequency_maps)
    X_test = apply_frequency_encoding(X_test, frequency_maps)

    numeric_features = get_numeric_features(X_train)

    model = build_model(numeric_features)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    metrics = evaluate_model(y_test, y_pred)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    artifact = {
        "model": model,
        "frequency_maps": frequency_maps,
        "columns_to_drop": COLUMNS_TO_DROP,
        "one_hot_features": ONE_HOT_FEATURES,
        "frequency_features": FREQUENCY_FEATURES,
        "numeric_features": numeric_features,
        "target": TARGET,
    }

    joblib.dump(artifact, MODEL_PATH)
    metrics.to_csv(METRICS_PATH, index=False)

    print(metrics.round(4).to_string(index=False))
    print(f"Saved model to: {MODEL_PATH}")
    print(f"Saved metrics to: {METRICS_PATH}")


if __name__ == "__main__":
    main()