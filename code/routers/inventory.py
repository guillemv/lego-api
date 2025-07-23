from fastapi import APIRouter
import motor.motor_asyncio
from db.models.item import Item
from db.client import Client
from db.schemas.itemSchema import item_schema,items_schema
import logging
import sys
router=APIRouter(prefix="/item",tags=["item"],responses={404:{"message":"Not Found"}})
client = Client("mongodb+srv://guille1987:wLww2PLk6h8dX34m@legodb.i4gbpgo.mongodb.net/", "Legodb")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

@router.get("/inventory")
async def inventory():
    return items_schema(client.find_many("inventory",{}))

@router.get("/")
async def part(id:str=None,box:str=None,color:str=None,colorid:int=None,supracolor:str=None,uid:str=None,section:str=None):
    query={}
    if id:
        query["id"]=id
    if box:
        query["box"]=box
    if color:
        query["color"]=color
    if colorid:
        query["colorid"]=colorid
    if supracolor:
        query["supracolor"]=supracolor
    if uid:
        query["uid"]=uid
    if section:
        query["section"]=section
    if query:  # Si hay condiciones en el query
        if "id" in query and len(query) == 1:  # Si solo se busca por ID
            result = client.find_one("inventory", query)
            return item_schema(result) if result else None
        else:
            result = client.find_many("inventory", query)
            return items_schema(result)
    else:
        # Si no se pasó ningún parámetro, se devuelven todos los colores
        result = client.find_many("inventory", {})
        return items_schema(result)
    
@router.post("/",)
async def newItem(item:Item):
    client.insert_one("inventory",dict(item))
    
@router.put("/edit/{id}/{colorid}")
async def editItem(item:Item,id:str,colorid:str):
    client.update_one("inventory",{"id":id,"colorid":int(colorid)},{"$set":dict(item)} )
    
@router.delete("/delete/{id}/{colorid}")
async def editItem(id:str,colorid:str):
    client.delete_one("inventory",{"id":id,"colorid":int(colorid)})