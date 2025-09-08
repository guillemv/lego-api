# code/routers/section.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..db.models.section import Section
from ..db.schemas.sectionSchema import section_schema, sections_schema
from ..deps import get_db

router = APIRouter(prefix="/sections", tags=["section"], responses={404: {"message": "Not Found"}})

# --- GET /sections --- #
@router.get("/")
async def list_sections(
    containerId: str | None = None,
    used: bool | None = None,
    uid: str | None = None,
    itemuid: str | None = None,
    db = Depends(get_db),
):
    query: dict = {}
    if containerId is not None:
        query["containerId"] = containerId
    if used is not None:
        query["used"] = used
    if uid is not None:
        query["uid"] = uid
    if itemuid is not None:
        query["itemuid"] = itemuid

    if query:
        # Si solo buscas por UID, devuelve un único doc
        if "uid" in query and len(query) == 1:
            result = await db.sections.find_one(query)
            return section_schema(result) if result else None
        result = await db.sections.find(query).to_list(10000)
        return sections_schema(result)

    # Sin filtros: todas
    result = await db.sections.find({}).to_list(10000)
    return sections_schema(result)

# --- PATCH parcial para /sections/{uid} --- #
class SectionPatch(BaseModel):
    used: bool | None = None
    itemuid: str | None = None

@router.put("/{uid}")
async def update_section(uid: str, patch: SectionPatch, db = Depends(get_db)):
    data = patch.model_dump(exclude_unset=True)
    ops: dict = {}

    # itemuid: si viene y es None => UNSET, si es str => SET
    if "itemuid" in data:
        if data["itemuid"] is None:
            ops["$unset"] = {"itemuid": ""}
        else:
            ops.setdefault("$set", {})["itemuid"] = data["itemuid"]

    # used: si viene, se setea
    if "used" in data:
        ops.setdefault("$set", {})["used"] = data["used"]

    if not ops:
        return {"ok": True, "noop": True}

    res = await db.sections.update_one({"uid": uid}, ops)
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Section not found")
    return {"ok": True, "matched": res.matched_count, "modified": res.modified_count}

# --- POST /sections --- #
@router.post("/")
async def create_section(section: Section, db = Depends(get_db)):
    await db.sections.insert_one(section)
    return {"ok": True}
