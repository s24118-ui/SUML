#!/usr/bin/env python3

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "SUML-main" / "models" / "autogluon_price_model"
TARGET = Path(__file__).resolve().parents[1] / "models" / "autogluon_price_model"


def main() -> None:
    if not SOURCE.is_dir():
        raise SystemExit(f"Brak katalogu modelu: {SOURCE}")

    nested = SOURCE / "autogluon_price_model" / "predictor.pkl"
    if not nested.is_file() and not (SOURCE / "predictor.pkl").is_file():
        raise SystemExit(
            f"W {SOURCE} nie ma pliku predictor.pkl. "
            "Najpierw uruchom train_autogluon.py w SUML-main."
        )

    if TARGET.exists():
        shutil.rmtree(TARGET)

    shutil.copytree(SOURCE, TARGET)
    print(f"Skopiowano model do: {TARGET}")


if __name__ == "__main__":
    main()
