from fastapi import APIRouter, Depends
from ..db.client import Client
from ..db.schemas.colorSchema import colors_schema, color_schema
from ..deps import get_db

router=APIRouter(prefix="/colors",tags=["color"],responses={404:{"message":"Not Found"}})

@router.get("/")
async def colors(id:str=None,name:str=None,bl:str=None,supracolor:str=None, db = Depends(get_db)):
        # Crear un diccionario de filtro vacío
    query = {}

    # Agregar condiciones al filtro basadas en los parámetros proporcionados
    if id:
        query["ID"] = int(id)
    if name:
        query["Name"] = name
    if bl:
        query["Bricklink"] = bl
    if supracolor:
        query["Supracolor"] = supracolor
    # Decidir si se busca un solo color o múltiples colores
    if query:  # Si hay condiciones en el query
        if "ID" in query and len(query) == 1:  # Si solo se busca por ID
            result = await db.colors.find_one(query)
            return color_schema(result) if result else None
        else:
            result = await db.colors.find(query).to_list(10000)
            return colors_schema(result)
    else:
        # Si no se pasó ningún parámetro, se devuelven todos los colores
        result = await db.colors.find({}).to_list(10000)
        return colors_schema(result)


@router.get("/supracolor")
async def supracolor(db = Depends(get_db)):
    result=await db.colors.find({}).to_list(10000)
    supracolors=[]
    for r in result:
        if r["Supracolor"] not in supracolors:
            supracolors.append(r["Supracolor"])
    return supracolors