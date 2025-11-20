from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from conf.database import engine, Base
from routes import cart_route, item_route

app = FastAPI()

origins = ("http://localhost", "http://localhost:8000", "http://localhost:5173")

allow_methods = ("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS")
allow_headers = ("Authorization", "Content-Type", "Accept", "X-Requested-With")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=allow_methods,
    allow_headers=allow_headers,
)


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
