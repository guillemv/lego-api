from fastapi import APIRouter
import motor.motor_asyncio
from db.client import Client
from db.schemas.colorSchema import colors_schema, color_schema
router=APIRouter(prefix="/colors",tags=["color"],responses={404:{"message":"Not Found"}})
client = Client("mongodb+srv://guille1987:wLww2PLk6h8dX34m@legodb.i4gbpgo.mongodb.net/", "Legodb")

@router.get("/")
async def colors(id:str=None,name:str=None,bl:str=None,supracolor:str=None):
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
            result = client.find_one("colors", query)
            return color_schema(result) if result else None
        else:
            result = client.find_many("colors", query)
            return colors_schema(result)
    else:
        # Si no se pasó ningún parámetro, se devuelven todos los colores
        result = client.find_many("colors", {})
        return colors_schema(result)


