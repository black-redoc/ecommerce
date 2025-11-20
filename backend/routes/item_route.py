from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from conf.database import get_db
from services import item_service
from models.item import ItemIn, ItemOptional, ItemOut

router = APIRouter()


@router.get("/")
async def get_items(page: int = 1, db: AsyncSession = Depends(get_db)):
    return await item_service.list_items(db, page)


@router.get("/{id}", response_model=ItemOut)
async def item_details(id: int, db: AsyncSession = Depends(get_db)):
    item = await item_service.get_item(db, id)
    if not item:
        raise HTTPException(
            status_code=404,
            detail="item not found",
            headers={"content-type": "application/json"},
        )
    return item


@router.post("/", response_model=ItemOut)
async def create_item(item: ItemIn, db: AsyncSession = Depends(get_db)):
    return await item_service.create_item(db, item)


@router.put("/{id}", response_model=ItemOut)
async def update_item(id: int, item: ItemIn, db: AsyncSession = Depends(get_db)):
    return await item_service.update_item(db, id, item)


@router.patch("/{id}", response_model=ItemOut)
async def partial_update(
    id: int, item: ItemOptional, db: AsyncSession = Depends(get_db)
):
    return await item_service.partial_update(db, id, item)
