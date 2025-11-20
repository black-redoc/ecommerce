from fastapi import FastAPI
from conf.database import engine, Base
from routes import cart_route, item_route

app = FastAPI()


# Create tables on startup
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(cart_route.router, prefix="/cart")
app.include_router(item_route.router, prefix="/item")


@app.get("/healthcheck")
def healthcheck():
    return "OK "
