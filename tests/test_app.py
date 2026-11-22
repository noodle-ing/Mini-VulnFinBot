import pytest

from app import create_app


@pytest.fixture()
def client():
    return create_app({"TESTING": True}).test_client()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}


def test_chat_returns_mock_budget_tip(client):
    response = client.post("/api/chat", json={"message": "How can I save money?"})
    assert response.status_code == 200
    assert response.json == {"response": "You can start by tracking your income and expenses."}


@pytest.mark.parametrize("body", [{}, {"message": "  "}, {"message": 42}, {"message": "x" * 2001}])
def test_chat_rejects_invalid_message(client, body):
    assert client.post("/api/chat", json=body).status_code == 400


def test_chat_rejects_non_json(client):
    assert client.post("/api/chat", data="hello").status_code == 415


def test_chat_rejects_json_array(client):
    response = client.post("/api/chat", data="[]", content_type="application/json")
    assert response.status_code == 400


def test_chat_rejects_malformed_json(client):
    response = client.post("/api/chat", data="{", content_type="application/json")
    assert response.status_code == 400
    assert "Traceback" not in response.get_data(as_text=True)
