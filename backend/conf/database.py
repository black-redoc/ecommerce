from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from .settings import DATABASE_URL, IS_DEV


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL, echo=IS_DEV, future=True)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


# Dependency for FastAPI
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
