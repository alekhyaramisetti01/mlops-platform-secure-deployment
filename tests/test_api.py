from fastapi.testclient import TestClient
from app.main import app, settings

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict_unauthorized():
    payload = {
        "transaction_amount": 500,
        "account_age_days": 200,
        "num_prev_transactions": 30,
        "avg_transaction_amount": 200,
        "location_risk_score": 0.6,
        "device_risk_score": 0.4,
        "merchant_risk_score": 0.3,
        "payment_velocity": 2,
        "chargeback_history": 0,
        "failed_login_attempts": 1
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 401


def test_predict_authorized():
    payload = {
        "transaction_amount": 500,
        "account_age_days": 200,
        "num_prev_transactions": 30,
        "avg_transaction_amount": 200,
        "location_risk_score": 0.6,
        "device_risk_score": 0.4,
        "merchant_risk_score": 0.3,
        "payment_velocity": 2,
        "chargeback_history": 0,
        "failed_login_attempts": 1
    }

    response = client.post(
        "/predict",
        json=payload,
        headers={"x-api-key": settings.api_key}
    )
    assert response.status_code == 200
    data = response.json()
    assert "fraud_prediction" in data
    assert "fraud_probability" in data
    assert "environment" in data
    assert data["fraud_prediction"] in [0, 1]
    assert 0.0 <= data["fraud_probability"] <= 1.0