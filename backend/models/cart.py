from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship, Mapped
from conf.database import Base
from pydantic import BaseModel, ConfigDict
from models.item import ItemModel, ItemOut


class CartModel(Base):
    __tablename__ = "carts"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)

    # Relación muchos a muchos: un cart tiene muchos items
    items: Mapped[list[ItemModel]] = relationship(
        "ItemModel", secondary="item_cart", back_populates="carts"
    )

    @property
    def total(self) -> float:
        """Calcula el total sumando el value de todos los items"""
        return round(sum(item.value for item in self.items), 2)
        # return " ".join(item.value for)


class CartIn(BaseModel):
    items: list[int]  # Lista de IDs de items


class CartOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    items: list[ItemOut]
    total: float
