from pydantic import BaseModel

class Container(BaseModel):
    id:int
    size:str
