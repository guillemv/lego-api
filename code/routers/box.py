from fastapi import APIRouter, HTTPException, Depends, status, Query
from ..deps import get_db
from ..db.schemas.boxSchema import box_schema, boxes_schema
from ..db.models.box import Box
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Literal
import re


router = APIRouter(prefix="/boxes", tags=["box"], responses={404: {"message": "Not Found"}})

@router.get("/")
async def boxes(
    id: str | None = None,
    size: str | None = None,
    supracolor: str | None = None,
    db = Depends(get_db),
):
    if id:
        doc = await db.boxes.find_one({"id": id})
        if not doc:
            raise HTTPException(404, "Box no encontrada")
        return box_schema(doc)

    filt: dict = {}
    if size: filt["size"] = size
    if supracolor: filt["supracolor"] = supracolor

    docs = await db.boxes.find(filt).to_list(1000)
    return boxes_schema(docs)

@router.post("/", status_code=201)
async def newBox(box: Box, db = Depends(get_db)):
    await db.boxes.insert_one(box.model_dump())

    # crear contenedores asociados (sin llamar a endpoints)
    if box.size == "3x3":
        target_size, filas, cols = 4, range(1, 4), "ABC"
    else:
        target_size, filas, cols = 3, range(1, 7), "ABCDE"

    payload = [{"id": f"{box.id}-{c}-{f}", "size": target_size} for f in filas for c in cols]
    if payload:
        await db.containers.insert_many(payload)
    return {"ok": True}

@router.put("/edit/{id}")
async def editBox(id: str, box: Box, db = Depends(get_db)):
    res = await db.boxes.update_one({"id": id}, {"$set": box.model_dump()})
    if res.matched_count == 0:
        raise HTTPException(404, "Box no encontrada")
    return {"ok": True, "modified": res.modified_count}

@router.delete("/{box_id}", status_code=status.HTTP_200_OK)
async def delete_box(
    box_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    dry_run: bool = Query(False, description="No borra nada; solo devuelve los contadores"),
    strategy: Literal["bulk", "loop"] = Query("bulk", description="bulk = 1 delete_many por nivel; loop = N deletes por contenedor"),
):
    # 1) Comprobar que la caja existe
    box = await db.boxes.find_one({"id": box_id})
    if not box:
        raise HTTPException(status_code=404, detail="Box not found")

    # Prefijo "<boxId>-" para containers.id y sections.containerId
    prefix = f"^{re.escape(box_id)}-"
    cont_q = {"id": {"$regex": prefix}}
    sect_q = {"containerId": {"$regex": prefix}}

    # 2) Dry-run (cuenta sin borrar)
    if dry_run:
        containers_count = await db.containers.count_documents(cont_q)
        sections_count   = await db.sections.count_documents(sect_q)
        return {
            "dry_run": True,
            "box_id": box_id,
            "would_delete": {
                "sections": sections_count,
                "containers": containers_count,
                "boxes": 1
            }
        }

    # 3) Transacción: sections -> containers -> box
    async with await db.client.start_session() as s:
        async with s.start_transaction():
            if strategy == "bulk":
                # Un delete_many para todas las sections y otro para todos los containers
                sect_res = await db.sections.delete_many(sect_q, session=s)
                cont_res = await db.containers.delete_many(cont_q, session=s)
            else:
                # loop: N eliminaciones de containers, y para cada container N eliminaciones de sections
                # (seguimos usando delete_many por container para sections; si quisieras 1 a 1, sería muy ineficiente)
                sect_deleted = 0
                cont_deleted = 0
                # Listamos los IDs de containers de esta box
                cur = db.containers.find(cont_q, projection={"id": 1}, session=s)
                container_ids = [doc["id"] async for doc in cur]
                for cid in container_ids:
                    s_res = await db.sections.delete_many({"containerId": cid}, session=s)
                    sect_deleted += s_res.deleted_count
                    c_res = await db.containers.delete_one({"id": cid}, session=s)
                    cont_deleted += c_res.deleted_count

                class _Res:  # mini contenedores de resultado para homogeneizar respuesta
                    def __init__(self, n): self.deleted_count = n
                sect_res = _Res(sect_deleted)
                cont_res = _Res(cont_deleted)

            box_res = await db.boxes.delete_one({"id": box_id}, session=s)
            if box_res.deleted_count != 1:
                # Carrera concurrente: alguien la borró entre medias
                raise HTTPException(status_code=409, detail="Concurrent modification; box no longer exists")

    return {
        "ok": True,
        "box_id": box_id,
        "deleted": {
            "sections": sect_res.deleted_count,
            "containers": cont_res.deleted_count,
            "boxes": 1
        },
        "strategy": strategy
    }