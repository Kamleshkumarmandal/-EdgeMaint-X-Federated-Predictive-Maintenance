from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_health_endpoint_reports_model_not_loaded():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["model_loaded"] is False


def test_signal_inspection_returns_descriptive_metrics():
    values = [0.5, -0.5] * 256
    response = client.post(
        "/api/v1/signals/inspect",
        json={"values": values, "sample_rate_hz": 12000, "source_label": "test-signal"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["summary"]["sample_count"] == 512
    assert payload["duration_seconds"] > 0
    assert "No trained fault-classification model" in payload["notice"]


def test_signal_inspection_rejects_short_input():
    response = client.post("/api/v1/signals/inspect", json={"values": [0.1, 0.2]})
    assert response.status_code == 422
