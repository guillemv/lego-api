from fastapi import APIRouter
from ..db.client import Client
from ..db.models.section import Section
from ..db.schemas.sectionSchema import section_schema,sections_schema
router=APIRouter(prefix="/sections",tags=["section"],responses={404:{"message":"Not Found"}})
client = Client("mongodb+srv://guille1987:wLww2PLk6h8dX34m@legodb.i4gbpgo.mongodb.net/", "Legodb")

@router.get("/")
async def section(containerId:str=None,used:bool=None,uid:str=None,itemuid:str=None):
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
            result = client.find_one("sections", query)
            return section_schema(result) if result else None
        else:
            result = client.find_many("sections", query)
            return sections_schema(result)
    else:
        # Si no se pasó ningún parámetro, se devuelven todos los colores
        result = client.find_many("sections", {})
        return sections_schema(result)

@router.put("/{uid}")
async def update_section(uid: str, section: Section):
    if section.itemuid is None:
        client.update_one(
            "sections",
            {"uid": uid},
            {"$unset": {"itemuid": ""}, "$set": {"used": section.used}}
        )
    else:
        client.update_one(
            "sections",
            {"uid": uid},
            {"$set": {"used": section.used, "itemuid": section.itemuid}}
        )

@router.post("/")
async def create_section(section:Section):
    client.insert_one("sections",section)