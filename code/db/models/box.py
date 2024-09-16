from pydantic import BaseModel

class Box(BaseModel):
    id:str
    size:str
    supracolor:str