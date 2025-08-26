from fastapi import APIRouter,status,Body,HTTPException
from ..db.client import Client
from ..db.schemas.containerSchema import container_schema, containers_schema
from ..db.models.container import Container
from .section import Section as section
router=APIRouter(prefix="/containers",tags=["container"],responses={404:{"message":"Not Found"}})
client = Client("mongodb+srv://guille1987:wLww2PLk6h8dX34m@legodb.i4gbpgo.mongodb.net/", "Legodb")

@router.get("/")
async def containers(id:str=None,size:str=None):
    if id:
        return container_schema(client.find_one("containers",{"id":id}))
    if size:
        return containers_schema(client.find_many("containers",{"size":size}))
    else:
        return containers_schema(client.find_many("containers",{}))

@router.post("/")
async def newContainer(container:Container):
    client.insert_one("containers",dict(container))
    c=dict(container)

    for i in range(0,int(c["size"])):
        await section.create_section({"containerId":c["id"],"used":False,"uid":f"{c['id']}-{i}"})
