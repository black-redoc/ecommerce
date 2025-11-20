import pytest


@pytest.mark.asyncio
async def test_healthcheck(client):
    """Test healthcheck endpoint"""
    response = await client.get("/healthcheck")
    assert response.status_code == 200
    assert response.text == '"OK "'


@pytest.mark.asyncio
async def test_create_item_endpoint(client):
    """Test POST /item/ endpoint"""
    item_data = {"name": "Test Item", "value": 99.99}

    response = await client.post("/item/", json=item_data)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["value"] == 99.99
    assert "id" in data


@pytest.mark.asyncio
async def test_get_items_pagination(client):
    """Test GET /item/ endpoint with pagination"""
    # Create some items
    for i in range(15):
        await client.post("/item/", json={"name": f"Item {i}", "value": float(i * 10)})

    # Test first page
    response = await client.get("/item/?page=1")
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert len(data["data"]) == 10

    # Test second page
    response = await client.get("/item/?page=2")
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 2
    assert len(data["data"]) == 5


@pytest.mark.asyncio
async def test_get_item_by_id(client):
    """Test GET /item/{id} endpoint"""
    # Create an item
    create_response = await client.post(
        "/item/", json={"name": "Test Item", "value": 50.0}
    )
    created_item = create_response.json()

    # Get the item by ID
    response = await client.get(f"/item/{created_item['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_item["id"]
    assert data["name"] == "Test Item"
    assert data["value"] == 50.0


@pytest.mark.asyncio
async def test_get_item_not_found(client):
    """Test GET /item/{id} with non-existent ID"""
    response = await client.get("/item/9999")
    assert response.status_code == 404
    assert "item not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_update_item(client):
    """Test PUT /item/{id} endpoint"""
    # Create an item
    create_response = await client.post(
        "/item/", json={"name": "Original Item", "value": 100.0}
    )
    created_item = create_response.json()

    # Update the item
    update_data = {"name": "Updated Item", "value": 200.0}
    response = await client.put(f"/item/{created_item['id']}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_item["id"]
    assert data["name"] == "Updated Item"
    assert data["value"] == 200.0


@pytest.mark.asyncio
async def test_update_item_not_found(client):
    """Test PUT /item/{id} with non-existent ID"""
    update_data = {"name": "Updated Item", "value": 200.0}
    response = await client.put("/item/9999", json=update_data)

    assert response.status_code == 404
    assert "item not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_partial_update_item(client):
    """Test PATCH /item/{id} endpoint"""
    # Create an item
    create_response = await client.post(
        "/item/", json={"name": "Original Item", "value": 100.0}
    )
    created_item = create_response.json()

    # Partial update - only name
    response = await client.patch(
        f"/item/{created_item['id']}", json={"name": "Patched Item"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Patched Item"
    assert data["value"] == 100.0  # Value should remain unchanged


@pytest.mark.asyncio
async def test_partial_update_item_not_found(client):
    """Test PATCH /item/{id} with non-existent ID"""
    response = await client.patch("/item/9999", json={"name": "Patched Item"})

    assert response.status_code == 404
    assert "item not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_item_with_invalid_data(client):
    """Test POST /item/ with invalid data"""
    # Missing required field 'value'
    response = await client.post("/item/", json={"name": "Test Item"})

    assert response.status_code == 422  # Unprocessable Entity


@pytest.mark.asyncio
async def test_items_default_page(client):
    """Test GET /item/ without page parameter defaults to page 1"""
    # Create some items
    for i in range(3):
        await client.post("/item/", json={"name": f"Item {i}", "value": float(i * 10)})

    response = await client.get("/item/")
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert len(data["data"]) == 3
