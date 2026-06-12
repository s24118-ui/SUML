"""API FastAPI endpoints and startup lifecycle for the valauto backend."""

from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .model import get_predictor, predict_price
from .schemas import EvaluateRequest, ValuationResponse

app = FastAPI(title="valauto-api", version="0.2.0")

default_origins = [
    "https://localhost",
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
extra_origins = os.getenv("CORS_ORIGINS", "")
allowed_origins = default_origins + [
    origin.strip() for origin in extra_origins.split(",") if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    """Return basic health status for the API."""
    return {"status": "ok"}


@app.on_event("startup")
def startup() -> None:
    """Load or build the model when the application starts."""
    get_predictor()


@app.post("/evaluate", response_model=ValuationResponse)
def evaluate(payload: EvaluateRequest) -> ValuationResponse:
    """Evaluate a car valuation request and return the predicted price."""
    try:
        price = predict_price(payload)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return ValuationResponse(
        price=price,
        message="Wycena obliczona poprawnie.",
    )
