import pytest


@pytest.mark.asyncio
async def test_create_cart_endpoint(client):
    """Test POST /cart/ endpoint"""
    # First create some items
    item1_response = await client.post("/item/", json={"name": "Item 1", "value": 10.0})
    item2_response = await client.post("/item/", json={"name": "Item 2", "value": 20.0})

    item1_id = item1_response.json()["id"]
    item2_id = item2_response.json()["id"]

    # Create cart with these items
    cart_data = {"items": [item1_id, item2_id]}
    response = await client.post("/cart/", json=cart_data)

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert len(data["items"]) == 2
    assert data["total"] == 30.0


@pytest.mark.asyncio
async def test_create_cart_with_nonexistent_items(client):
    """Test POST /cart/ with non-existent items"""
    cart_data = {"items": [9999, 8888]}
    response = await client.post("/cart/", json=cart_data)

    assert response.status_code == 404
    assert "Items not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_all_carts(client):
    """Test GET /cart/ endpoint"""
    # Create items
    item1_response = await client.post("/item/", json={"name": "Item 1", "value": 10.0})
    item2_response = await client.post("/item/", json={"name": "Item 2", "value": 20.0})

    item1_id = item1_response.json()["id"]
    item2_id = item2_response.json()["id"]

    # Create multiple carts
    await client.post("/cart/", json={"items": [item1_id]})
    await client.post("/cart/", json={"items": [item2_id]})

    # Get all carts
    response = await client.get("/cart/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert all("items" in cart for cart in data)
    assert all("total" in cart for cart in data)


@pytest.mark.asyncio
async def test_get_cart_by_id(client):
    """Test GET /cart/{id} endpoint"""
    # Create items
    item1_response = await client.post("/item/", json={"name": "Item 1", "value": 15.0})
    item1_id = item1_response.json()["id"]

    # Create cart
    create_response = await client.post("/cart/", json={"items": [item1_id]})
    cart_id = create_response.json()["id"]

    # Get cart by ID
    response = await client.get(f"/cart/{cart_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == cart_id
    assert len(data["items"]) == 1
    assert data["total"] == 15.0


@pytest.mark.asyncio
async def test_get_cart_not_found(client):
    """Test GET /cart/{id} with non-existent ID"""
    response = await client.get("/cart/9999")

    assert response.status_code == 404
    assert "cart not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_update_cart(client):
    """Test PUT /cart/{id} endpoint"""
    # Create items
    item1_response = await client.post("/item/", json={"name": "Item 1", "value": 10.0})
    item2_response = await client.post("/item/", json={"name": "Item 2", "value": 20.0})
    item3_response = await client.post("/item/", json={"name": "Item 3", "value": 30.0})

    item1_id = item1_response.json()["id"]
    item2_id = item2_response.json()["id"]
    item3_id = item3_response.json()["id"]

    # Create cart with items 1 and 2
    create_response = await client.post("/cart/", json={"items": [item1_id, item2_id]})
    cart_id = create_response.json()["id"]

    # Update cart to have items 2 and 3
    update_data = {"items": [item2_id, item3_id]}
    response = await client.put(f"/cart/{cart_id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == cart_id
    assert len(data["items"]) == 2

    # Verify item2 and item3 are in the cart
    item_ids = [item["id"] for item in data["items"]]
    assert item2_id in item_ids
    assert item3_id in item_ids
    assert item1_id not in item_ids

    # Verify total
    assert data["total"] == 50.0


@pytest.mark.asyncio
async def test_update_cart_not_found(client):
    """Test PUT /cart/{id} with non-existent cart"""
    response = await client.put("/cart/9999", json={"items": [1]})

    assert response.status_code == 404
    assert "cart not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_update_cart_with_invalid_items(client):
    """Test PUT /cart/{id} with non-existent items"""
    # Create item and cart
    item1_response = await client.post("/item/", json={"name": "Item 1", "value": 10.0})
    item1_id = item1_response.json()["id"]

    create_response = await client.post("/cart/", json={"items": [item1_id]})
    cart_id = create_response.json()["id"]

    # Try to update with non-existent items
    response = await client.put(f"/cart/{cart_id}", json={"items": [9999]})

    assert response.status_code == 404
    assert "Items not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_delete_cart(client):
    """Test DELETE /cart/{id} endpoint"""
    # Create item and cart
    item1_response = await client.post("/item/", json={"name": "Item 1", "value": 10.0})
    item1_id = item1_response.json()["id"]

    create_response = await client.post("/cart/", json={"items": [item1_id]})
    cart_id = create_response.json()["id"]

    # Delete cart
    response = await client.delete(f"/cart/{cart_id}")
    assert response.status_code == 200

    # Verify cart is deleted
    get_response = await client.get(f"/cart/{cart_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_cart_not_found(client):
    """Test DELETE /cart/{id} with non-existent cart"""
    response = await client.delete("/cart/9999")

    assert response.status_code == 404
    assert "cart not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_cart_total_calculation_integration(client):
    """Test that cart total is calculated correctly through API"""
    # Create items with specific values
    item1_response = await client.post(
        "/item/", json={"name": "Item 1", "value": 10.50}
    )
    item2_response = await client.post(
        "/item/", json={"name": "Item 2", "value": 20.25}
    )
    item3_response = await client.post(
        "/item/", json={"name": "Item 3", "value": 15.75}
    )

    item_ids = [
        item1_response.json()["id"],
        item2_response.json()["id"],
        item3_response.json()["id"],
    ]

    # Create cart
    create_response = await client.post("/cart/", json={"items": item_ids})
    data = create_response.json()

    assert data["total"] == 46.50


@pytest.mark.asyncio
async def test_create_empty_cart(client):
    """Test creating a cart with no items"""
    response = await client.post("/cart/", json={"items": []})

    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 0
    assert data["total"] == 0.0


@pytest.mark.asyncio
async def test_cart_operations_workflow(client):
    """Test complete workflow: create, read, update, delete"""
    # 1. Create items
    item1_response = await client.post("/item/", json={"name": "Item 1", "value": 10.0})
    item2_response = await client.post("/item/", json={"name": "Item 2", "value": 20.0})

    item1_id = item1_response.json()["id"]
    item2_id = item2_response.json()["id"]

    # 2. Create cart
    create_response = await client.post("/cart/", json={"items": [item1_id]})
    assert create_response.status_code == 200
    cart_id = create_response.json()["id"]

    # 3. Read cart
    get_response = await client.get(f"/cart/{cart_id}")
    assert get_response.status_code == 200
    assert get_response.json()["total"] == 10.0

    # 4. Update cart
    update_response = await client.put(
        f"/cart/{cart_id}", json={"items": [item1_id, item2_id]}
    )
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert len(updated_data["items"]) == 2
    # Verify total is calculated correctly
    assert updated_data["total"] == 30.0

    # 5. Delete cart
    delete_response = await client.delete(f"/cart/{cart_id}")
    assert delete_response.status_code == 200

    # 6. Verify deletion
    verify_response = await client.get(f"/cart/{cart_id}")
    assert verify_response.status_code == 404
