from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_crud_flow():
    # create
    resp = client.post("/shorten", json={"url": "https://example.com/test"})
    assert resp.status_code == 201
    data = resp.json()
    code = data["shortCode"]

    # get
    resp = client.get(f"/shorten/{code}")
    assert resp.status_code == 200
    assert resp.json()["url"] == "https://example.com/test"

    # stats initially
    resp = client.get(f"/shorten/{code}/stats")
    assert resp.status_code == 200
    assert resp.json()["accessCount"] >= 0

    # update
    resp = client.put(f"/shorten/{code}", json={"url": "https://example.com/updated"})
    assert resp.status_code == 200
    assert resp.json()["url"] == "https://example.com/updated"

    # delete
    resp = client.delete(f"/shorten/{code}")
    assert resp.status_code == 204

    # confirm deleted
    resp = client.get(f"/shorten/{code}")
    assert resp.status_code == 404
