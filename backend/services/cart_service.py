from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from sqlalchemy.orm import selectinload
from models.cart import CartIn, CartModel
from models.item import ItemModel
from models.item_cart import item_cart


async def create_cart(db: AsyncSession, cart: CartIn):
    # Buscar todos los items por sus IDs primero
    result = await db.execute(select(ItemModel).where(ItemModel.id.in_(cart.items)))
    items = result.scalars().all()

    # Verificar que todos los IDs existen
    found_ids = {item.id for item in items}
    missing_ids = set(cart.items) - found_ids

    if missing_ids:
        raise HTTPException(
            status_code=404,
            detail=f"Items not found: {list(missing_ids)}",
            headers={"content-type": "application/json"},
        )

    # Crear un nuevo cart vacío
    new_cart = CartModel()
    db.add(new_cart)
    await db.flush()  # Flush para obtener el ID del cart

    # Insertar las asociaciones en la tabla intermedia
    for item_id in cart.items:
        await db.execute(insert(item_cart).values(cart_id=new_cart.id, item_id=item_id))

    await db.commit()

    # Recargar el cart con los items usando selectinload
    result = await db.execute(
        select(CartModel)
        .where(CartModel.id == new_cart.id)
        .options(selectinload(CartModel.items))
    )
    cart_with_items = result.scalar_one()

    return cart_with_items


async def get_cart(db: AsyncSession):
    # Cargar los carts con sus items usando selectinload
    result = await db.execute(select(CartModel).options(selectinload(CartModel.items)))
    cart_list = result.scalars().all()

    return cart_list


async def update_cart(db: AsyncSession, id: int, cart: CartIn):
    # 1. Verificar que el cart existe
    result = await db.execute(
        select(CartModel)
        .options(selectinload(CartModel.items))
        .where(CartModel.id == id)
    )
    fetched_cart = result.scalar_one_or_none()

    if not fetched_cart:
        raise HTTPException(
            status_code=404,
            detail="cart not found",
            headers={"content-type": "application/json"},
        )

    # 2. Validar que todos los nuevos items existen
    result = await db.execute(select(ItemModel).where(ItemModel.id.in_(cart.items)))
    existing_items = result.scalars().all()
    existing_item_ids = {item.id for item in existing_items}
    missing_ids = set(cart.items) - existing_item_ids

    if missing_ids:
        raise HTTPException(
            status_code=404,
            detail=f"Items not found: {list(missing_ids)}",
            headers={"content-type": "application/json"},
        )

    # 3. Obtener IDs actuales del cart
    current_item_ids = {item.id for item in fetched_cart.items}
    incoming_item_ids = set(cart.items)

    # 4. Calcular diferencias
    items_to_delete = current_item_ids - incoming_item_ids
    items_to_add = incoming_item_ids - current_item_ids

    # 5. Eliminar items que ya no están en el cart
    if items_to_delete:
        await db.execute(
            delete(item_cart).where(
                (item_cart.c.cart_id == id) & (item_cart.c.item_id.in_(items_to_delete))
            )
        )

    # 6. Agregar nuevos items al cart
    for item_id in items_to_add:
        await db.execute(insert(item_cart).values(cart_id=id, item_id=item_id))

    await db.commit()

    # 7. Expirar el cache de la sesión para forzar recarga desde la DB
    db.expire_all()

    # 8. Recargar el cart con los items actualizados
    result = await db.execute(
        select(CartModel)
        .where(CartModel.id == id)
        .options(selectinload(CartModel.items))
    )
    return result.scalar_one()



async def delete_cart(db: AsyncSession, id: int):
    result = await db.execute(select(CartModel).where(CartModel.id == id))

    cart_fetched = result.scalar_one_or_none()

    if not cart_fetched:
        raise HTTPException(
            status_code=404,
            detail="cart not found",
            headers={"content-type": "Application/json"},
        )
    await db.delete(cart_fetched)
    await db.commit()
    return 200, {"detail": "OK"}


async def cart_details(db: AsyncSession, id: int):
    result = await db.execute(
        select(CartModel)
        .options(selectinload(CartModel.items))
        .where(CartModel.id == id)
    )

    fetched_cart = result.scalar_one_or_none()

    if not fetched_cart:
        raise HTTPException(
            status_code=404,
            detail="cart not found",
            headers={"content-type": "application/json"},
        )

    return fetched_cart
