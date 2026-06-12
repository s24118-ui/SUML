"""Model loader and startup checks for the valauto API."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

from .predictor import AutoGluonValuationPredictor
from .schemas import EvaluateRequest


def _default_model_path() -> Path:
    valauto_models = (
        Path(__file__).resolve().parent.parent / "models" / "autogluon_price_model"
    )
    suml_models = (
        Path(__file__).resolve().parent.parent.parent
        / "SUML-main"
        / "models"
        / "autogluon_price_model"
    )

    if valauto_models.is_dir():
        return valauto_models
    if suml_models.is_dir():
        return suml_models
    return valauto_models


def _suml_root() -> Path:
    env_path = os.getenv("SUML_ROOT")
    if env_path:
        candidate = Path(env_path)
        if candidate.is_dir():
            return candidate

    local_suml = Path(__file__).resolve().parent.parent.parent / "SUML-main"
    if local_suml.is_dir():
        return local_suml

    raise FileNotFoundError(
        "SUML-main directory not found. Set SUML_ROOT or mount the SUML-main directory in Docker."
    )


def _is_git_lfs_pointer(path: Path) -> bool:
    if not path.is_file():
        return False

    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        first_line = handle.readline().strip()
    return first_line.startswith("version https://git-lfs.github.com/spec/v1")


def _find_predictor_dir(base_path: Path) -> Path | None:
    candidate = base_path / "predictor.pkl"
    if candidate.is_file() and not _is_git_lfs_pointer(candidate):
        return base_path

    nested = base_path / base_path.name
    candidate = nested / "predictor.pkl"
    if candidate.is_file() and not _is_git_lfs_pointer(candidate):
        return nested

    if base_path.is_dir():
        for child in base_path.iterdir():
            candidate = child / "predictor.pkl"
            if child.is_dir() and candidate.is_file() and not _is_git_lfs_pointer(candidate):
                return child

    return None


def _run_preprocess(suml_root: Path) -> None:
    preprocess_script = suml_root / "src" / "data" / "preprocess.py"
    processed_path = suml_root / "data" / "processed" / "car_ads_clean.csv"

    def _is_valid_csv(path: Path) -> bool:
        if not path.is_file():
            return False
        with path.open("r", encoding="utf-8", errors="ignore") as handle:
            first_line = handle.readline().strip()
        return not first_line.startswith("version https://git-lfs.github.com/spec/v1")

    if _is_valid_csv(processed_path):
        return

    if not preprocess_script.is_file():
        raise FileNotFoundError(
            f"Preprocessing script not found: {preprocess_script}"
        )

    subprocess.run(
        [sys.executable, str(preprocess_script)],
        cwd=str(suml_root),
        check=True,
    )

    if not _is_valid_csv(processed_path):
        raise FileNotFoundError(
            f"Processed data file was not generated: {processed_path}"
        )


def _ensure_processed_data(suml_root: Path) -> None:
    processed_path = suml_root / "data" / "processed" / "car_ads_clean.csv"
    if processed_path.is_file():
        with processed_path.open("r", encoding="utf-8", errors="ignore") as handle:
            first_line = handle.readline().strip()
        if not first_line.startswith("version https://git-lfs.github.com/spec/v1"):
            return

    _run_preprocess(suml_root)


def _train_model(suml_root: Path) -> None:
    train_script = suml_root / "src" / "model" / "train_autogluon.py"
    if not train_script.is_file():
        raise FileNotFoundError(
            f"Training script not found: {train_script}"
        )

    if MODEL_PATH.exists():
        if MODEL_PATH.is_dir():
            shutil.rmtree(MODEL_PATH)
        else:
            MODEL_PATH.unlink()

    _run_preprocess(suml_root)

    subprocess.run(
        [sys.executable, str(train_script)],
        cwd=str(suml_root),
        check=True,
    )


MODEL_PATH = Path(os.getenv("MODEL_PATH", str(_default_model_path())))

_cached_predictor: AutoGluonValuationPredictor | None = None


def _is_existing_model_fit() -> bool:
    """Check whether the configured model path contains a valid fitted AutoGluon model."""
    predictor_dir = _find_predictor_dir(MODEL_PATH)
    if predictor_dir is None:
        return False

    try:
        predictor = AutoGluonValuationPredictor(MODEL_PATH)
        predictor.validate_fit()
        return True
    except (RuntimeError, FileNotFoundError, AssertionError, OSError):
        return False


def _reset_predictor() -> None:
    """Clear the cached predictor so the model can be reloaded."""
    globals()["_cached_predictor"] = None


def _ensure_model_exists() -> None:
    if MODEL_PATH.is_dir():
        return

    if MODEL_PATH.exists() and not MODEL_PATH.is_dir():
        raise FileExistsError(
            f"MODEL_PATH istnieje, ale nie jest katalogiem: {MODEL_PATH}"
        )

    suml_root = _suml_root()
    _train_model(suml_root)

    if not MODEL_PATH.is_dir():
        raise FileNotFoundError(
            f"Model directory not found after training: {MODEL_PATH}"
        )


def get_predictor() -> AutoGluonValuationPredictor:
    """Return a cached predictor, loading or training the model if required."""
    if _cached_predictor is None:
        suml_root = _suml_root()
        _ensure_processed_data(suml_root)
        _ensure_model_exists()
        globals()["_cached_predictor"] = AutoGluonValuationPredictor(MODEL_PATH)

    return _cached_predictor


def predict_price(payload: EvaluateRequest) -> int:
    """Predict the price for a valuation request using the loaded model."""
    try:
        return get_predictor().predict(payload)
    except AssertionError as exc:
        if "Predictor is not fit" in str(exc):
            _reset_predictor()
            _ensure_model_exists()
            return get_predictor().predict(payload)
        raise
