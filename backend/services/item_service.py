from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models.item import ItemIn, ItemModel, ItemOptional
from sqlalchemy import select

ITEM_QUERY_LIMIT = 10
PAGINATOR_FIRST_POSITION = 1


async def list_items(db: AsyncSession, page: int):
    offset = (page - PAGINATOR_FIRST_POSITION) * ITEM_QUERY_LIMIT
    result = await db.execute(select(ItemModel).offset(offset).limit(ITEM_QUERY_LIMIT))

    return {"page": page, "data": result.scalars().all()}


async def item_details(db: AsyncSession, id: int):
    result = await db.execute(select(ItemModel).where(ItemModel.id == id))
    return result.scalar_one_or_none()


async def get_item(db: AsyncSession, id: int):
    return await item_details(db, id)


async def create_item(db: AsyncSession, item: ItemIn):
    new_item = ItemModel(name=item.name, value=item.value)
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item


async def update_item(db: AsyncSession, id: int, item: ItemIn):
    result = await db.execute(select(ItemModel).where(ItemModel.id == id))
    existing_item = result.scalar_one_or_none()

    if not existing_item:
        raise HTTPException(
            status_code=404,
            detail="item not found",
            headers={"content-type": "Application/json"},
        )
    existing_item.name = item.name
    existing_item.value = item.value
    await db.commit()
    await db.refresh(existing_item)
    return existing_item


async def partial_update(db: AsyncSession, id: int, item: ItemOptional):
    result = await db.execute(select(ItemModel).where(ItemModel.id == id))
    fetched_item = result.scalar_one_or_none()

    if not fetched_item:
        raise HTTPException(
            status_code=404,
            detail="item not found",
            headers={"content-type": "Application/json"},
        )
    update_item = item.model_dump(exclude_unset=True)
    for key, value in update_item.items():
        setattr(fetched_item, key, value)

    await db.commit()
    await db.refresh(fetched_item)
    return fetched_item
