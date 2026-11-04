def test_create_salon(client):
    response = client.post("/salons", json={"name": "Juniper Hair Studio"})

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Juniper Hair Studio"
    assert "id" in data


def test_list_salons(client):
    client.post("/salons", json={"name": "Juniper"})
    client.post("/salons", json={"name": "Maple"})

    response = client.get("/salons")

    assert response.status_code == 200
    assert [s["name"] for s in response.json()] == ["Juniper", "Maple"]


def test_get_missing_salon_returns_404(client):
    response = client.get("/salons/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Salon not found"


def test_empty_name_is_rejected(client):
    response = client.post("/salons", json={"name": ""})

    assert response.status_code == 422


def test_add_and_list_stylists(client):
    salon_id = client.post("/salons", json={"name": "Juniper"}).json()["id"]

    created = client.post(f"/salons/{salon_id}/stylists", json={"name": "Aisha"})
    assert created.status_code == 201
    assert created.json()["salon_id"] == salon_id

    stylists = client.get(f"/salons/{salon_id}/stylists").json()
    assert [s["name"] for s in stylists] == ["Aisha"]


def test_stylist_for_missing_salon_returns_404(client):
    response = client.post("/salons/999/stylists", json={"name": "Aisha"})

    assert response.status_code == 404