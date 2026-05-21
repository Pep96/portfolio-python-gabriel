from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app import app


client = TestClient(app)
API_KEY = {"X-API-Key": "dev-secret-key"}
WEBHOOK_SECRET = {"X-Webhook-Secret": "webhook-secret"}


def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_homepage_renders():
    response = client.get("/")
    assert response.status_code == 200
    assert "PulseSend" in response.text


def test_whatsapp_send_and_lookup():
    response = client.post(
        "/api/v1/messages/whatsapp/send",
        headers=API_KEY,
        json={
            "to": "+5511999999999",
            "content": "Pedido confirmado",
            "template_name": "order_update",
            "metadata": {"order_id": "ord_1"},
        },
    )
    assert response.status_code == 200
    message_id = response.json()["message"]["id"]

    lookup = client.get(f"/api/v1/messages/{message_id}", headers=API_KEY)
    assert lookup.status_code == 200
    assert lookup.json()["message"]["template_name"] == "order_update"


def test_webhook_updates_status():
    sent = client.post(
        "/api/v1/messages/sms/send",
        headers=API_KEY,
        json={
            "to": "+5511988887777",
            "content": "Codigo 1234",
            "metadata": {"purpose": "otp"},
        },
    )
    message_id = sent.json()["message"]["id"]

    webhook = client.post(
        "/api/v1/webhooks/whatsapp/status",
        headers=WEBHOOK_SECRET,
        json={
            "message_id": message_id,
            "status": "delivered",
            "timestamp": datetime.now(UTC).isoformat(),
            "details": {"provider_status": "accepted"},
        },
    )
    assert webhook.status_code == 200
    assert webhook.json()["message"]["status"] == "delivered"
