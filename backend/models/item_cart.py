from sqlalchemy import Column, Integer, ForeignKey, Table
from conf.database import Base

# Tabla de asociación para la relación muchos a muchos entre items y carts
item_cart = Table(
    "item_cart",
    Base.metadata,
    Column("item_id", Integer, ForeignKey("items.id"), primary_key=True),
    Column("cart_id", Integer, ForeignKey("carts.id"), primary_key=True),
)
