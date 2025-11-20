import pytest
from fastapi import HTTPException
from models.item import ItemIn, ItemOptional
from services.item_service import create_item, list_items, get_item, update_item, partial_update


@pytest.mark.asyncio
async def test_create_item(test_db):
    """Test creating a new item"""
    item_data = ItemIn(name="Test Item", value=99.99)

    new_item = await create_item(test_db, item_data)

    assert new_item.id is not None
    assert new_item.name == "Test Item"
    assert new_item.value == 99.99


@pytest.mark.asyncio
async def test_list_items_pagination(test_db):
    """Test listing items with pagination"""
    # Create some test items
    for i in range(15):
        item_data = ItemIn(name=f"Item {i}", value=float(i * 10))
        await create_item(test_db, item_data)

    # Test first page
    result = await list_items(test_db, page=1)
    assert result["page"] == 1
    assert len(result["data"]) == 10

    # Test second page
    result = await list_items(test_db, page=2)
    assert result["page"] == 2
    assert len(result["data"]) == 5


@pytest.mark.asyncio
async def test_get_item_exists(test_db):
    """Test getting an existing item"""
    item_data = ItemIn(name="Test Item", value=50.0)
    created_item = await create_item(test_db, item_data)

    fetched_item = await get_item(test_db, created_item.id)

    assert fetched_item is not None
    assert fetched_item.id == created_item.id
    assert fetched_item.name == "Test Item"
    assert fetched_item.value == 50.0


@pytest.mark.asyncio
async def test_get_item_not_exists(test_db):
    """Test getting a non-existent item"""
    fetched_item = await get_item(test_db, 9999)
    assert fetched_item is None


@pytest.mark.asyncio
async def test_update_item_success(test_db):
    """Test updating an existing item"""
    # Create item
    item_data = ItemIn(name="Original Name", value=100.0)
    created_item = await create_item(test_db, item_data)

    # Update item
    update_data = ItemIn(name="Updated Name", value=200.0)
    updated_item = await update_item(test_db, created_item.id, update_data)

    assert updated_item.id == created_item.id
    assert updated_item.name == "Updated Name"
    assert updated_item.value == 200.0


@pytest.mark.asyncio
async def test_update_item_not_found(test_db):
    """Test updating a non-existent item raises HTTPException"""
    update_data = ItemIn(name="Updated Name", value=200.0)

    with pytest.raises(HTTPException) as exc_info:
        await update_item(test_db, 9999, update_data)

    assert exc_info.value.status_code == 404
    assert "item not found" in exc_info.value.detail


@pytest.mark.asyncio
async def test_partial_update_name_only(test_db):
    """Test partial update changing only the name"""
    # Create item
    item_data = ItemIn(name="Original Name", value=100.0)
    created_item = await create_item(test_db, item_data)

    # Partial update - only name
    update_data = ItemOptional(name="New Name")
    updated_item = await partial_update(test_db, created_item.id, update_data)

    assert updated_item.name == "New Name"
    assert updated_item.value == 100.0  # Value unchanged


@pytest.mark.asyncio
async def test_partial_update_value_only(test_db):
    """Test partial update changing only the value"""
    # Create item
    item_data = ItemIn(name="Original Name", value=100.0)
    created_item = await create_item(test_db, item_data)

    # Partial update - only value
    update_data = ItemOptional(value=250.0)
    updated_item = await partial_update(test_db, created_item.id, update_data)

    assert updated_item.name == "Original Name"  # Name unchanged
    assert updated_item.value == 250.0


@pytest.mark.asyncio
async def test_partial_update_not_found(test_db):
    """Test partial update on non-existent item raises HTTPException"""
    update_data = ItemOptional(name="New Name")

    with pytest.raises(HTTPException) as exc_info:
        await partial_update(test_db, 9999, update_data)

    assert exc_info.value.status_code == 404
    assert "item not found" in exc_info.value.detail
