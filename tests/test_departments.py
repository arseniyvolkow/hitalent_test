import pytest


@pytest.mark.asyncio
async def test_create_department(client):
    response = await client.post("/departments/", json={"name": "Engineering"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Engineering"
    assert data["parent_id"] is None


@pytest.mark.asyncio
async def test_create_sub_department(client):
    parent_resp = await client.post("/departments/", json={"name": "HQ"})
    parent_id = parent_resp.json()["id"]

    response = await client.post(
        "/departments/", json={"name": "HR", "parent_id": parent_id}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "HR"
    assert data["parent_id"] == parent_id


@pytest.mark.asyncio
async def test_create_department_explicit_null(client):
    response = await client.post(
        "/departments/", json={"name": "Finance", "parent_id": None}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Finance"
    assert data["parent_id"] is None


@pytest.mark.asyncio
async def test_unique_department_name_under_parent(client):
    await client.post("/departments/", json={"name": "Finance"})
    response = await client.post("/departments/", json={"name": "Finance"})
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_get_department_tree(client):
    resp_a = await client.post("/departments/", json={"name": "Dept A"})
    id_a = resp_a.json()["id"]
    resp_b = await client.post(
        "/departments/", json={"name": "Dept B", "parent_id": id_a}
    )
    id_b = resp_b.json()["id"]
    await client.post("/departments/", json={"name": "Dept C", "parent_id": id_b})

    response = await client.get(f"/departments/{id_a}?depth=2")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Dept A"
    assert len(data["children"]) == 1
    assert data["children"][0]["name"] == "Dept B"
    assert len(data["children"][0]["children"]) == 1
    assert data["children"][0]["children"][0]["name"] == "Dept C"
