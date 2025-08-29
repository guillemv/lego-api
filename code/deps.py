# code/deps.py
import asyncio
from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorClient
from .settings import settings

_clients_by_loop: dict[int, AsyncIOMotorClient] = {}
_dbs_by_loop = {}

async def get_db(request: Request):
    loop_id = id(asyncio.get_running_loop())

    db = _dbs_by_loop.get(loop_id)
    if db is None:
        client = AsyncIOMotorClient(
            settings.MONGO_URI,
            uuidRepresentation="standard",
        )
        _clients_by_loop[loop_id] = client
        db = client[settings.MONGO_DB]
        _dbs_by_loop[loop_id] = db

        # opcional: útil en local, pero NO dependas de esto en Vercel
        request.app.state.mongo = client
        request.app.state.db = db

    return db
