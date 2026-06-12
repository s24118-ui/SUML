"""Pydantic request and response schemas used by the valauto API."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

RodzajPaliwa = Literal["Benzyna", "Diesel", "Hybryda", "Elektryczny", "LPG"]
TypSkrzyniBiegow = Literal["Manualna", "Automatyczna"]


class EvaluateRequest(BaseModel):
    """Request body schema for valuation prediction."""

    marka: str = Field(..., min_length=1, max_length=120)
    model_pojazdu: str = Field(default="Other", min_length=1, max_length=120)
    moc_silnika: int = Field(..., ge=1, le=5000)
    przebieg: int = Field(..., ge=0, le=5_000_000)
    rodzaj_paliwa: RodzajPaliwa
    rok_produkcji: int = Field(..., ge=1886, le=2027)
    typ_skrzyni_biegow: TypSkrzyniBiegow


class ValuationResponse(BaseModel):
    """Response schema for valuation prediction results."""

    price: int | None = None
    detail: str | None = None
    error: str | None = None
    message: str | None = None
