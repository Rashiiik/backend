CBC = {
    "code": "CBC",
    "name": "Complete Blood Count",
    "category": "Hematology",
    "price": 400,
}


def test_full_crud_lifecycle(client):
    # CREATE
    r = client.post("/tests", json=CBC)
    assert r.status_code == 201
    created = r.json()
    test_id = created["id"]
    assert created["code"] == "CBC"
    assert created["is_active"] is True

    # READ one
    r = client.get(f"/tests/{test_id}")
    assert r.status_code == 200
    assert r.json()["name"] == "Complete Blood Count"

    # READ list
    r = client.get("/tests")
    assert r.status_code == 200
    assert len(r.json()) == 1

    # UPDATE (only price)
    r = client.patch(f"/tests/{test_id}", json={"price": 450})
    assert r.status_code == 200
    assert r.json()["price"] == 450
    assert r.json()["name"] == "Complete Blood Count"  # unchanged

    # DELETE
    r = client.delete(f"/tests/{test_id}")
    assert r.status_code == 204

    # confirm it's gone
    r = client.get(f"/tests/{test_id}")
    assert r.status_code == 404


def test_list_is_empty_at_start(client):
    r = client.get("/tests")
    assert r.status_code == 200
    assert r.json() == []


def test_create_duplicate_code_returns_409(client):
    client.post("/tests", json=CBC)
    r = client.post("/tests", json=CBC)
    assert r.status_code == 409
    assert "already exists" in r.json()["detail"]


def test_create_negative_price_returns_422(client):
    r = client.post("/tests", json={**CBC, "price": -50})
    assert r.status_code == 422


def test_create_lowercase_code_returns_422(client):
    r = client.post("/tests", json={**CBC, "code": "cbc"})
    assert r.status_code == 422


def test_create_missing_name_returns_422(client):
    data = {k: v for k, v in CBC.items() if k != "name"}
    r = client.post("/tests", json=data)
    assert r.status_code == 422


def test_get_missing_test_returns_404(client):
    r = client.get("/tests/999")
    assert r.status_code == 404


def test_update_missing_test_returns_404(client):
    r = client.patch("/tests/999", json={"price": 100})
    assert r.status_code == 404


def test_update_with_invalid_price_returns_422(client):
    test_id = client.post("/tests", json=CBC).json()["id"]
    r = client.patch(f"/tests/{test_id}", json={"price": -1})
    assert r.status_code == 422


def test_delete_missing_test_returns_404(client):
    r = client.delete("/tests/999")
    assert r.status_code == 404