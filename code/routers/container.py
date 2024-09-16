from fastapi import APIRouter,status,Body,HTTPException
from db.client import Client
from db.schemas.containerSchema import container_schema, containers_schema
router=APIRouter(prefix="/containers",tags=["container"],responses={404:{"message":"Not Found"}})
client = Client("mongodb+srv://guille1987:wLww2PLk6h8dX34m@legodb.i4gbpgo.mongodb.net/", "Legodb")

@router.get("/")
async def containers(id:str=None,size:str=None,supracolor:str=None):
    if id:
        return container_schema(client.find_one("containers",{"id":id}))
    if size:
        return containers_schema(client.find_many("containers",{"size":size}))
    if supracolor:
        return containers_schema(client.find_many("containers",{"Supracolor":supracolor}))
    else:
        return containers_schema(client.find_many("containers",{}))
