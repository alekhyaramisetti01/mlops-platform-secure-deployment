import os
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split


MODEL_DIR = Path("model_artifacts")
MODEL_PATH = MODEL_DIR / "fraud_model.joblib"


def load_data():
    x, y = make_classification(
        n_samples=5000,
        n_features=10,
        n_informative=6,
        n_redundant=2,
        n_classes=2,
        weights=[0.85, 0.15],
        flip_y=0.01,
        random_state=42,
    )

    feature_names = [
        "transaction_amount",
        "account_age_days",
        "num_prev_transactions",
        "avg_transaction_amount",
        "location_risk_score",
        "device_risk_score",
        "merchant_risk_score",
        "payment_velocity",
        "chargeback_history",
        "failed_login_attempts",
    ]

    return pd.DataFrame(x, columns=feature_names), pd.Series(y, name="target")


def train():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    x, y = load_data()
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )

    mlflow.set_experiment("secure-fraud-risk-demo")

    with mlflow.start_run():
        model = LogisticRegression(max_iter=500, random_state=42)
        model.fit(x_train, y_train)

        predictions = model.predict(x_test)
        probabilities = model.predict_proba(x_test)[:, 1]

        metrics = {
            "accuracy": accuracy_score(y_test, predictions),
            "precision": precision_score(y_test, predictions),
            "recall": recall_score(y_test, predictions),
            "f1_score": f1_score(y_test, predictions),
            "roc_auc": roc_auc_score(y_test, probabilities),
        }

        mlflow.log_param("model_type", "LogisticRegression")
        mlflow.log_param("test_size", 0.2)
        mlflow.log_metrics(metrics)

        joblib.dump(model, MODEL_PATH)
        mlflow.log_artifact(str(MODEL_PATH))
        mlflow.sklearn.log_model(model, artifact_path="model")

        print("Training complete.")
        print(f"Model saved to: {MODEL_PATH}")
        print("Metrics:")
        for key, value in metrics.items():
            print(f"  {key}: {value:.4f}")


if __name__ == "__main__":
    os.environ.setdefault("MLFLOW_TRACKING_URI", "file:./mlruns")
    train()