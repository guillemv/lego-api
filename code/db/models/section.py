from pydantic import BaseModel

class Section(BaseModel):
    containerId:str
    used:bool
    uid:str
    itemuid:str=None
