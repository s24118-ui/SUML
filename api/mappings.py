"""Utilities for mapping vehicle metadata to the AutoGluon feature schema."""

from __future__ import annotations

FUEL_TYPE_MAP = {
    "Benzyna": "Gasoline",
    "Diesel": "Diesel",
    "Hybryda": "Hybrid",
    "Elektryczny": "Electric",
    "LPG": "Gasoline + LPG",
}

TRANSMISSION_MAP = {
    "Manualna": "Manual",
    "Automatyczna": "Automatic",
}

BRAND_ALIASES = {
    "Citroen": "Citroën",
    "Skoda": "Škoda",
}


def normalize_brand(marka: str) -> str:
    """Return normalized brand name for feature mapping."""
    return BRAND_ALIASES.get(marka, marka)


def map_fuel_type(rodzaj_paliwa: str) -> str:
    """Map Polish fuel type labels to the model's expected values."""
    try:
        return FUEL_TYPE_MAP[rodzaj_paliwa]
    except KeyError as exc:
        raise ValueError(f"Unsupported fuel type: {rodzaj_paliwa}") from exc


def map_transmission(typ_skrzyni_biegow: str) -> str:
    """Map Polish transmission labels to the model's expected values."""
    try:
        return TRANSMISSION_MAP[typ_skrzyni_biegow]
    except KeyError as exc:
        raise ValueError(
            f"Unsupported transmission type: {typ_skrzyni_biegow}"
        ) from exc
