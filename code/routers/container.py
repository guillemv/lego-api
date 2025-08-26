from fastapi import APIRouter,status,Body,HTTPException, Depends
from ..db.client import Client
from ..db.schemas.containerSchema import container_schema, containers_schema
from ..db.models.container import Container
from .section import Section as section
from ..deps import get_db

router=APIRouter(prefix="/containers",tags=["container"],responses={404:{"message":"Not Found"}})

@router.get("/")
async def containers(id:str=None,size:str=None, db = Depends(get_db)):
    if id:
        return container_schema(await db.containers.find_one({"id":id}))
    if size:
        return containers_schema(await db.containers.find({"size":size}).to_list(10000))
    else:
        return containers_schema(await db.containers.find({}).to_list(10000))

@router.post("/")
async def newContainer(container:Container, db = Depends(get_db)):
    await db.containers.insert_one(dict(container))
    c=dict(container)

    for i in range(0,int(c["size"])):
        await section.create_section({"containerId":c["id"],"used":False,"uid":f"{c['id']}-{i}"})
