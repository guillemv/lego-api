
from .security import get_current_user
from .routers import color, inventory, box, container, section
from .routers import auth  # <-- nuevo
# code/main.py
import logging, time, uuid
from fastapi import FastAPI, Request,Depends
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from .settings import settings

# Configurar logging del proceso (stdout/stderr -> Vercel Runtime Logs)
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
log = logging.getLogger("lego-api")

app = FastAPI(debug=settings.DEBUG)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    rid = str(uuid.uuid4())
    request.state.rid = rid
    t0 = time.perf_counter()
    log.info("→ %s %s rid=%s ua=%s", request.method, request.url.path, rid, request.headers.get("user-agent","-"))
    try:
        resp = await call_next(request)
    except Exception:
        # Esto imprime el traceback completo en los logs de Vercel
        log.exception("¡¡ Unhandled exception !! rid=%s path=%s", rid, request.url.path)
        raise
    dt = (time.perf_counter() - t0) * 1000
    log.info("← %s %s %s %.1fms rid=%s", request.method, request.url.path, resp.status_code, dt, rid)
    resp.headers["X-Request-ID"] = rid
    return resp

# (Opcional) Devolver el rid en el cuerpo si hay 500
@app.exception_handler(Exception)
async def catch_all(request: Request, exc: Exception):
    rid = getattr(request.state, "rid", "-")
    # El traceback ya se imprimió arriba con log.exception(...)
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error", "rid": rid})

@app.on_event("startup")
async def startup():
    app.state.mongo = AsyncIOMotorClient(settings.MONGO_URI, uuidRepresentation="standard")
    app.state.db = app.state.mongo[settings.MONGO_DB]
    # Log útil al arrancar para verificar deps
    try:
        import importlib.metadata as md
        log.info("deps fastapi=%s pydantic=%s motor=%s python-multipart=%s",
                 md.version("fastapi"), md.version("pydantic"),
                 md.version("motor"), md.version("python-multipart"))
    except Exception:
        log.warning("No pude leer versiones de paquetes")

@app.on_event("shutdown")
async def shutdown():
    app.state.mongo.close()

# Endpoints de auth
app.include_router(auth.router)

# Endpoints protegidos (requieren Bearer token)
app.include_router(color.router,     dependencies=[Depends(get_current_user)])
app.include_router(inventory.router, dependencies=[Depends(get_current_user)])
app.include_router(box.router,       dependencies=[Depends(get_current_user)])
app.include_router(container.router, dependencies=[Depends(get_current_user)])
app.include_router(section.router,   dependencies=[Depends(get_current_user)])

