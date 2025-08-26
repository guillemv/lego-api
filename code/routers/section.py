from fastapi import APIRouter, Depends
from ..db.client import Client
from ..db.models.section import Section
from ..db.schemas.sectionSchema import section_schema,sections_schema
from ..deps import get_db

router=APIRouter(prefix="/sections",tags=["section"],responses={404:{"message":"Not Found"}})

@router.get("/")
async def section(containerId:str=None,used:bool=None,uid:str=None,itemuid:str=None, db = Depends(get_db)):
    query={}
    if containerId:
        query["containerId"]=containerId
    if used:
        query["used"]=used
    if uid:
        query["uid"]=uid
    if itemuid:
        query["itemuid"]=itemuid
    if query:  # Si hay condiciones en el query
        if "id" in query and len(query) == 1:  # Si solo se busca por ID
            result = await db.sections.find_one(query)
            return section_schema(result) if result else None
        else:
            result = await db.sections.find(query).to_list(10000)
            return sections_schema(result)
    else:
        # Si no se pasó ningún parámetro, se devuelven todos los colores
        result = await db.sections.find({}).to_list(10000)
        return sections_schema(result)

@router.put("/{uid}")
async def update_section(uid: str, section: Section, db = Depends(get_db)):
    if section.itemuid is None:
        await db.sections.update_one(
            {"uid": uid},
            {"$unset": {"itemuid": ""}, "$set": {"used": section.used}}
        )
    else:
        await db.sections.update_one(
            {"uid": uid},
            {"$set": {"used": section.used, "itemuid": section.itemuid}}
        )

@router.post("/")
async def create_section(section:Section, db = Depends(get_db)):
    await db.sections.insert_one(section)