from pydantic import BaseModel

class Color(BaseModel):
    id:int
    name:str
    supracolor:str
    rgb:str
    bricklink:str
    lego:str