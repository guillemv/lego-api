from fastapi import FastAPI, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from .settings import settings
from .security import get_current_user
from .routers import color, inventory, box, container, section
from .routers import auth  # <-- nuevo

app = FastAPI()

@app.on_event("startup")
async def startup():
    mongo = AsyncIOMotorClient(settings.MONGO_URI, uuidRepresentation="standard", serverSelectionTimeoutMS=5000)
    db = mongo[settings.MONGO_DB]
    await db.command("ping")
    await db.users.create_index("email", unique=True)
    app.state.mongo = mongo
    app.state.db = db

@app.on_event("shutdown")
async def shutdown():
    getattr(app.state, "mongo", None) and app.state.mongo.close()

# Endpoints de auth
app.include_router(auth.router)

# Endpoints protegidos (requieren Bearer token)
app.include_router(color.router,     dependencies=[Depends(get_current_user)])
app.include_router(inventory.router, dependencies=[Depends(get_current_user)])
app.include_router(box.router,       dependencies=[Depends(get_current_user)])
app.include_router(container.router, dependencies=[Depends(get_current_user)])
app.include_router(section.router,   dependencies=[Depends(get_current_user)])

