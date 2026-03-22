from pathlib import Path

import joblib
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

from app.config import get_settings, get_model_path


app = FastAPI(title="Secure Fraud Risk Prediction API", version="1.0.0")

REQUEST_COUNT = Counter("prediction_requests_total", "Total prediction requests")
PREDICTION_LATENCY = Histogram("prediction_latency_seconds", "Prediction latency in seconds")


class FraudRequest(BaseModel):
    transaction_amount: float
    account_age_days: float
    num_prev_transactions: float
    avg_transaction_amount: float
    location_risk_score: float
    device_risk_score: float
    merchant_risk_score: float
    payment_velocity: float
    chargeback_history: float
    failed_login_attempts: float


class FraudResponse(BaseModel):
    fraud_prediction: int
    fraud_probability: float
    environment: str


def load_model():
    model_path: Path = get_model_path()
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found at {model_path}. Run training first.")
    return joblib.load(model_path)


settings = get_settings()
model = load_model()


@app.get("/health")
def health():
    return {"status": "ok", "environment": settings.app_env}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/predict", response_model=FraudResponse)
def predict(request: FraudRequest, x_api_key: str | None = Header(default=None)):
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Unauthorized")

    REQUEST_COUNT.inc()

    features = [[
        request.transaction_amount,
        request.account_age_days,
        request.num_prev_transactions,
        request.avg_transaction_amount,
        request.location_risk_score,
        request.device_risk_score,
        request.merchant_risk_score,
        request.payment_velocity,
        request.chargeback_history,
        request.failed_login_attempts,
    ]]

    with PREDICTION_LATENCY.time():
        probability = float(model.predict_proba(features)[0][1])
        prediction = int(model.predict(features)[0])

    return FraudResponse(
        fraud_prediction=prediction,
        fraud_probability=round(probability, 4),
        environment=settings.app_env,
    )