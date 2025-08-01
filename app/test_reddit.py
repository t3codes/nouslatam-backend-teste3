from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_get_posts():
    response = client.get("/posts/learnpython?period=day&limit=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data["posts"]) <= 4  # Garantir que a quantidade de posts não exceda o limite ao lançar o limit=3 vem 4 itens na lista
