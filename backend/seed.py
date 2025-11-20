"""
Seed script para inicializar la base de datos con datos de ejemplo.
Ejecutar con: python seed.py
"""

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from conf.database import engine, Base, AsyncSessionLocal
from models.item import ItemModel
from models.cart import CartModel


async def seed_items(session: AsyncSession) -> list[ItemModel]:
    """Crea items de ejemplo (productos) en la base de datos."""

    # Verificar si ya existen items
    result = await session.execute(select(ItemModel).limit(1))
    existing_items = result.scalars().first()

    if existing_items:
        print("⚠️  La base de datos ya contiene items. Omitiendo seed de items...")
        result = await session.execute(select(ItemModel))
        return result.scalars().all()

    # Datos de ejemplo para productos de e-commerce
    sample_items = [
        # Electrónicos
        ItemModel(name="Laptop HP Pavilion 15", value=899.99),
        ItemModel(name="Mouse Inalámbrico Logitech MX Master 3", value=99.99),
        ItemModel(name="Teclado Mecánico Corsair K95", value=199.99),
        ItemModel(name="Monitor LG UltraWide 34\"", value=499.99),
        ItemModel(name="Auriculares Sony WH-1000XM5", value=399.99),
        ItemModel(name="Webcam Logitech C920 HD", value=79.99),
        ItemModel(name="SSD Samsung 1TB NVMe", value=129.99),

        # Accesorios
        ItemModel(name="Mochila para Laptop", value=49.99),
        ItemModel(name="Hub USB-C 7 en 1", value=39.99),
        ItemModel(name="Cable HDMI 4K 2m", value=19.99),
        ItemModel(name="Soporte para Laptop Ajustable", value=34.99),
        ItemModel(name="Alfombrilla de Ratón XXL", value=24.99),

        # Gaming
        ItemModel(name="Xbox Series X", value=499.99),
        ItemModel(name="PlayStation 5", value=499.99),
        ItemModel(name="Nintendo Switch OLED", value=349.99),
        ItemModel(name="Control Xbox Elite Series 2", value=179.99),
        ItemModel(name="Headset Gaming HyperX Cloud II", value=99.99),

        # Smart Home
        ItemModel(name="Echo Dot (5ta Gen)", value=49.99),
        ItemModel(name="Google Nest Hub", value=99.99),
        ItemModel(name="Ring Video Doorbell", value=99.99),
        ItemModel(name="Philips Hue Starter Kit", value=79.99),

        # Smartphones & Tablets
        ItemModel(name="iPhone 15 Pro 256GB", value=1099.99),
        ItemModel(name="Samsung Galaxy S24 Ultra", value=1199.99),
        ItemModel(name="iPad Air 11\" 256GB", value=749.99),
        ItemModel(name="AirPods Pro (2da Gen)", value=249.99),

        # Cámaras
        ItemModel(name="Canon EOS R6 Mark II", value=2499.99),
        ItemModel(name="GoPro HERO 12 Black", value=399.99),
        ItemModel(name="DJI Mini 3 Pro Drone", value=759.99),

        # Wearables
        ItemModel(name="Apple Watch Series 9", value=399.99),
        ItemModel(name="Samsung Galaxy Watch 6", value=299.99),
        ItemModel(name="Fitbit Charge 6", value=159.99),
    ]

    # Agregar todos los items
    session.add_all(sample_items)
    await session.commit()

    print(f"✅ Se crearon {len(sample_items)} productos de ejemplo")

    # Refrescar para obtener los IDs
    for item in sample_items:
        await session.refresh(item)

    return sample_items


async def seed_carts(session: AsyncSession, items: list[ItemModel]):
    """Crea carritos de ejemplo (opcional)."""

    # Verificar si ya existen carritos
    result = await session.execute(select(CartModel).limit(1))
    existing_carts = result.scalars().first()

    if existing_carts:
        print("⚠️  La base de datos ya contiene carritos. Omitiendo seed de carritos...")
        return

    # Crear algunos carritos de ejemplo con diferentes productos
    if len(items) >= 5:
        # Carrito 1: Setup de oficina
        cart1 = CartModel()
        cart1.items = [items[0], items[1], items[2], items[3]]  # Laptop, Mouse, Teclado, Monitor

        # Carrito 2: Gaming setup
        cart2 = CartModel()
        cart2.items = [items[12], items[15], items[16]]  # Xbox, Control Elite, Headset Gaming

        # Carrito 3: Smart home starter
        cart3 = CartModel()
        cart3.items = [items[17], items[18], items[20]]  # Echo Dot, Nest Hub, Hue Kit

        session.add_all([cart1, cart2, cart3])
        await session.commit()

        print(f"✅ Se crearon 3 carritos de ejemplo")


async def clear_database():
    """Limpia todas las tablas de la base de datos."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        print("🗑️  Base de datos limpiada")


async def create_tables():
    """Crea todas las tablas en la base de datos."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("📋 Tablas creadas")


async def main(clear: bool = False, skip_carts: bool = False):
    """
    Función principal del seed.

    Args:
        clear: Si es True, limpia la base de datos antes de crear los datos
        skip_carts: Si es True, no crea carritos de ejemplo
    """

    print("\n🌱 Iniciando seed de la base de datos...\n")

    # Limpiar base de datos si se solicita
    if clear:
        await clear_database()
        await create_tables()
    else:
        # Asegurar que las tablas existen
        await create_tables()

    # Crear sesión de base de datos
    async with AsyncSessionLocal() as session:
        # Seed de items (productos)
        items = await seed_items(session)

        # Seed de carritos (opcional)
        if not skip_carts:
            await seed_carts(session, items)

    print("\n✨ Seed completado exitosamente!\n")


if __name__ == "__main__":
    import sys

    # Argumentos de línea de comandos
    clear = "--clear" in sys.argv or "-c" in sys.argv
    skip_carts = "--skip-carts" in sys.argv
    help_flag = "--help" in sys.argv or "-h" in sys.argv

    if help_flag:
        print("""
Uso: python seed.py [opciones]

Opciones:
  --clear, -c       Limpia la base de datos antes de hacer el seed
  --skip-carts      No crea carritos de ejemplo, solo productos
  --help, -h        Muestra este mensaje de ayuda

Ejemplos:
  python seed.py                  # Crea productos y carritos de ejemplo
  python seed.py --clear          # Limpia la DB y crea datos nuevos
  python seed.py --skip-carts     # Solo crea productos, no carritos
        """)
        sys.exit(0)

    # Ejecutar seed
    asyncio.run(main(clear=clear, skip_carts=skip_carts))
