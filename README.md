#  Secure MLOps Platform with IaC, CI/CD, and Kubernetes

An enterprise-style MLOps platform demonstrating secure machine learning deployment using Infrastructure as Code (Terraform), containerization (Docker), orchestration (Kubernetes + Helm), and CI/CD automation (GitHub Actions).

This project focuses on **platform engineering principles applied to ML systems**, including reproducibility, security, scalability, and observability.

---

## Architecture

```mermaid
flowchart TD
    A[Training Pipeline<br/>ml_pipeline/train.py] --> B[Model Artifact<br/>fraud_model.joblib]

    B --> C[FastAPI Inference Service<br/>app/main.py]
    C --> D[Health Endpoint<br/>/health]
    C --> E[Metrics Endpoint<br/>/metrics]
    C --> F[Prediction Endpoint<br/>/predict]

    C --> G[Docker Image]
    G --> H[Kubernetes Deployment]
    H --> I[Helm Release]

    J[Environment Config<br/>secrets/.env] --> C
    K[Kubernetes Secret / Vault Pattern] --> H

    L[GitHub Actions CI/CD] --> M[Run Training]
    L --> N[Run Tests]
    L --> O[Build Docker Image]
    O --> G

    P[Terraform IaC] --> Q[Resource Group / Cluster / Node Pool]
    Q --> H

    R[Prometheus / Monitoring Stack] --> E

---

#  Tech Stack

- **Python**
- **FastAPI**
- **Scikit-learn**
- **MLflow**
- **Pytest**
- **Docker**
- **Kubernetes**
- **Helm**
- **Terraform (IaC)**
- **GitHub Actions**
- **Prometheus Client**

---

#  Project Structure

```

mlops-platform-secure-deployment
│
├── app/
│   ├── main.py              # FastAPI service
│   ├── config.py            # Environment & config management
│
├── ml_pipeline/
│   └── train.py             # Model training pipeline
│
├── tests/
│   └── test_api.py          # API tests
│
├── model_artifacts/
│   └── fraud_model.joblib   # Trained model
│
├── k8s/
│   ├── deployment.yaml      # Kubernetes deployment
│   └── service.yaml         # Kubernetes service
│
├── helm/
│   └── secure-fraud-ml-api  # Helm chart
│
├── terraform/
│   ├── main.tf              # AKS cluster definition
│   ├── variables.tf
│   ├── providers.tf
│   └── outputs.tf
│
├── monitoring/
│   └── metrics              # Prometheus integration (via /metrics)
│
├── secrets/
│   ├── .env.example         # Example config
│   └── .env                 # Local secrets (not committed)
│
├── .github/workflows/
│   └── platform-ci.yml      # CI/CD pipeline
│
├── Dockerfile
├── requirements.txt
└── README.md

````

---

#  Running Locally

## 1. Install Dependencies

```bash
pip install -r requirements.txt
````

---

## 2. Set Environment Variables

Create:

```
secrets/.env
```

Example:

```env
APP_ENV=dev
MODEL_PATH=model_artifacts/fraud_model.joblib
API_KEY=local-dev-secret
```

---

## 3. Train Model

```bash
python ml_pipeline/train.py
```

This generates:

```
model_artifacts/fraud_model.joblib
```

---

## 4. Run API

```bash
uvicorn app.main:app --reload
```

---

## 5. Access API

* Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## Health Check

```
GET /health
```

Response:

```json
{
  "status": "ok",
  "environment": "dev"
}
```

---

## Metrics (Prometheus)

```
GET /metrics
```

Used for monitoring:

* request count
* latency

---

## Fraud Prediction

```
POST /predict
```

Headers:

```
x-api-key: local-dev-secret
```

Example request:

```json
{
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
```

Example response:

```json
{
  "fraud_prediction": 0,
  "fraud_probability": 0.23,
  "environment": "dev"
}
```

---

#  Running Tests

```bash
pytest
```

Tests include:

* API health check
* authentication validation
* prediction endpoint validation

---

#  Docker

## Build Image

```bash
docker build -t secure-fraud-ml-api .
```

## Run Container

```bash
docker run -p 8000:8000 --env-file secrets/.env secure-fraud-ml-api
```

---

#  Kubernetes Deployment

```bash
kubectl apply -f k8s/
```

Check:

```bash
kubectl get pods
kubectl get services
```

---

#  Helm Deployment

```bash
helm install fraud-api helm/secure-fraud-ml-api
```

---

#  Infrastructure as Code (Terraform)

```bash
cd terraform
terraform init
terraform plan
```

This defines:

* resource group
* AKS cluster
* node pool

---

#  Security & Secrets Management

* Environment variables externalized
* `.env` not committed to repo
* Kubernetes Secret reference used
* API key-based request authentication

Production-ready alternatives:

* Azure Key Vault
* HashiCorp Vault
* AWS Secrets Manager

---

#  CI/CD Pipeline

GitHub Actions pipeline performs:

* Checkout repository
* Install dependencies
* Run ML training pipeline
* Validate model artifact
* Execute tests (pytest)
* Build Docker image

---

#  Observability

* `/metrics` endpoint for Prometheus
* request tracking
* latency measurement
* health probes for Kubernetes

---

#  Scalability & Reliability

* Kubernetes replicas
* readiness & liveness probes
* resource limits/requests

Future improvements:

* Horizontal Pod Autoscaler (HPA)
* auto-scaling based on CPU or traffic

---

#  Performance Metrics

Model metrics tracked:

* accuracy
* precision
* recall
* F1-score
* ROC-AUC

System metrics:

* request count
* latency

---

#  Reproducibility

* version-controlled code
* requirements.txt
* Docker containerization
* CI/CD validation pipeline

---

#  Future Enhancements

* MLflow model registry
* Prometheus + Grafana dashboards
* Vault integration for secrets
* data drift detection
* feature store integration (Feast)
* GitOps deployment (ArgoCD)

---

#  Key Highlights

This project demonstrates:

* End-to-end ML system design
* Platform engineering principles
* Secure deployment practices
* Infrastructure automation (Terraform)
* Scalable orchestration (Kubernetes + Helm)
* CI/CD automation
* Observability and monitoring

---

#  Summary

This is a **production-style MLOps platform** designed to showcase how machine learning systems can be built, secured, deployed, and monitored at scale using modern DevOps and cloud-native tools.