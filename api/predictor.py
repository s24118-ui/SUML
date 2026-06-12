"""Load and validate the AutoGluon model used by the valauto API."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from autogluon.tabular import TabularPredictor

from .features import build_feature_row, load_inference_defaults
from .schemas import EvaluateRequest


def resolve_autogluon_model_dir(base_path: Path) -> Path:
    """AutoGluon zapisuje model w podkatalogu o tej samej nazwie co folder nadrzędny."""
    if (base_path / "predictor.pkl").is_file():
        return base_path

    nested = base_path / base_path.name
    if (nested / "predictor.pkl").is_file():
        return nested

    for child in base_path.iterdir():
        if child.is_dir() and (child / "predictor.pkl").is_file():
            return child

    raise FileNotFoundError(
            f"AutoGluon model (predictor.pkl) not found in: {base_path}"
    )


class AutoGluonValuationPredictor:
    """AutoGluon predictor wrapper used for model loading and inference."""

    def __init__(self, model_base_path: Path) -> None:
        self._model_dir = resolve_autogluon_model_dir(model_base_path)
        self._defaults = load_inference_defaults(self._model_dir)
        self._predictor = TabularPredictor.load(str(self._model_dir))

    @property
    def model_dir(self) -> Path:
        """Return the directory where the loaded AutoGluon model is stored."""
        return self._model_dir

    def validate_fit(self) -> None:
        """Validate that the loaded AutoGluon model is fit and ready for prediction."""
        if not getattr(self._predictor, "_is_fit", False):
            raise RuntimeError("Loaded AutoGluon model is not fitted.")

    def predict(self, payload: EvaluateRequest) -> int:
        """Predict the price for the provided evaluation request."""
        features = build_feature_row(payload, self._defaults)
        prediction = self._predictor.predict(features, model="RandomForestMSE")
        price = int(max(0, round(float(prediction.iloc[0]))))

        if not np.isfinite(price):
            raise ValueError("Model returned an invalid price value.")

        return price
