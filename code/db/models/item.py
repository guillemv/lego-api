from pydantic import BaseModel

class Item(BaseModel):
    id:str
    color:str
    uid:str
    supracolor:str
    units:int
    box:str
    colorid:int
    section:list