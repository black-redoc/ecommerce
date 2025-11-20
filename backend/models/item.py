from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Mapped, relationship
from conf.database import Base
from pydantic import BaseModel


class ItemModel(Base):
    __tablename__ = "items"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String, nullable=False)
    value: Mapped[float] = Column(Float, nullable=False)

    # Relación muchos a muchos: un item puede estar en muchos carts
    carts = relationship("CartModel", secondary="item_cart", back_populates="items")


class ItemIn(BaseModel):
    name: str
    value: float


class ItemOptional(BaseModel):
    name: str | None = None
    value: float | None = None


class ItemOut(BaseModel):
    id: int
    name: str
    value: float
