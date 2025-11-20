from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from conf.database import get_db
from services import cart_service
from models.cart import CartIn, CartOut

router = APIRouter()


@router.get("/", response_model=list[CartOut])
async def list_cart(db: AsyncSession = Depends(get_db)):
    return await cart_service.get_cart(db)


@router.get("/{id}", response_model=CartOut)
async def cart_details(id: int, db: AsyncSession = Depends(get_db)):
    return await cart_service.cart_details(db, id)


@router.post("/", response_model=CartOut)
async def create_cart(cart: CartIn, db: AsyncSession = Depends(get_db)):
    return await cart_service.create_cart(db, cart)


@router.put("/{id}", response_model=CartOut)
async def update_cart(id: int, cart: CartIn, db: AsyncSession = Depends(get_db)):
    return await cart_service.update_cart(db, id, cart)


@router.delete("/{id}")
async def delete_cart(id: int, db: AsyncSession = Depends(get_db)):
    return await cart_service.delete_cart(db, id)
