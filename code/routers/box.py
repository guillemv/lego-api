from fastapi import APIRouter, HTTPException, Depends
from ..deps import get_db
from ..db.schemas.boxSchema import box_schema, boxes_schema
from ..db.models.box import Box

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
