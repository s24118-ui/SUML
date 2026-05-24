"""FastAPI entry point for valauto-api."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .model import model
from .schemas import EvaluateRequest, ValuationResponse

app = FastAPI(title="valauto-api", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://localhost",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/evaluate", response_model=ValuationResponse)
def evaluate(payload: EvaluateRequest) -> ValuationResponse:
    price = model.predict()

    return ValuationResponse(
        price=price,
        message="Wycena obliczona poprawnie.",
    )
