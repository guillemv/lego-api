from fastapi import APIRouter
from db.client import Client
from db.schemas.boxSchema import box_schema,boxes_schema
router=APIRouter(prefix="/boxes",tags=["box"],responses={404:{"message":"Not Found"}})
client = Client("mongodb+srv://guille1987:wLww2PLk6h8dX34m@legodb.i4gbpgo.mongodb.net/", "Legodb")

@router.get("/")
async def boxes(id:str=None,size:str=None,supracolor:str=None):
    if id:
        return box_schema(client.find_one("boxes",{"id":id}))
    if size:
        return boxes_schema(client.find_many("boxes",{"size":size}))
    if supracolor:
        return boxes_schema(client.find_many("boxes", {"supracolor":supracolor}))
    else:
        return boxes_schema(client.find_many("boxes",{}))

