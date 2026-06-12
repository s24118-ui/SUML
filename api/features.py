from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from .mappings import map_fuel_type, map_transmission, normalize_brand
from .schemas import EvaluateRequest

FALLBACK_DEFAULTS: dict[str, Any] = {
    "Condition": "Used",
    "Type": "sedan",
    "Drive": "Unknown",
    "Colour": "gray",
    "Origin_country": "Other",
    "Vehicle_model": "Other",
    "First_owner": 0,
    "Displacement_cm3": 1600.0,
    "CO2_emissions": 140.0,
    "Doors_number": 5.0,
    "fuel_medians": {
        "Gasoline": {
            "Displacement_cm3": 1598.0,
            "CO2_emissions": 145.0,
            "Doors_number": 5.0,
        },
        "Diesel": {
            "Displacement_cm3": 1968.0,
            "CO2_emissions": 129.0,
            "Doors_number": 5.0,
        },
        "Hybrid": {
            "Displacement_cm3": 1798.0,
            "CO2_emissions": 110.0,
            "Doors_number": 5.0,
        },
        "Electric": {
            "Displacement_cm3": 0.0,
            "CO2_emissions": 0.0,
            "Doors_number": 5.0,
        },
        "Gasoline + LPG": {
            "Displacement_cm3": 1398.0,
            "CO2_emissions": 155.0,
            "Doors_number": 5.0,
        },
    },
}


def load_inference_defaults(model_dir: Path) -> dict[str, Any]:
    defaults_path = model_dir / "inference_defaults.json"
    if defaults_path.is_file():
        return json.loads(defaults_path.read_text(encoding="utf-8"))

    parent_defaults = model_dir.parent / "inference_defaults.json"
    if parent_defaults.is_file():
        return json.loads(parent_defaults.read_text(encoding="utf-8"))

    return FALLBACK_DEFAULTS


def _resolve_numeric_defaults(
    fuel_type: str, defaults: dict[str, Any]
) -> tuple[float, float, float]:
    fuel_medians = defaults.get("fuel_medians", {})
    fuel_values = fuel_medians.get(fuel_type, {})

    displacement = float(
        fuel_values.get("Displacement_cm3", defaults.get("Displacement_cm3", 1600.0))
    )
    co2 = float(fuel_values.get("CO2_emissions", defaults.get("CO2_emissions", 140.0)))
    doors = float(fuel_values.get("Doors_number", defaults.get("Doors_number", 5.0)))

    if fuel_type == "Electric":
        displacement = 0.0

    return displacement, co2, doors


def build_feature_row(
    payload: EvaluateRequest, defaults: dict[str, Any] | None = None
) -> pd.DataFrame:
    defaults = defaults or FALLBACK_DEFAULTS
    fuel_type = map_fuel_type(payload.rodzaj_paliwa)
    transmission = map_transmission(payload.typ_skrzyni_biegow)
    displacement, co2, doors = _resolve_numeric_defaults(fuel_type, defaults)

    if fuel_type == "Electric":
        transmission = "Automatic"

    condition = (
        "New"
        if payload.przebieg == 0
        else defaults.get("Condition", "Used")
    )

    row = {
        "Condition": condition,
        "Vehicle_brand": normalize_brand(payload.marka),
        "Vehicle_model": (payload.model_pojazdu or "Other").strip() or "Other",
        "Production_year": payload.rok_produkcji,
        "Mileage_km": float(payload.przebieg),
        "Power_HP": float(payload.moc_silnika),
        "Displacement_cm3": displacement,
        "CO2_emissions": co2,
        "Doors_number": doors,
        "Fuel_type": fuel_type,
        "Drive": defaults.get("Drive", "Unknown"),
        "Transmission": transmission,
        "Type": defaults.get("Type", "sedan"),
        "Colour": defaults.get("Colour", "gray"),
        "Origin_country": defaults.get("Origin_country", "Other"),
        "First_owner": defaults.get("First_owner", 0),
    }

    return pd.DataFrame([row])
