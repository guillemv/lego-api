from typing import Union
from routers import  color,inventory,box,container,section
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
app.include_router(color.router)
app.include_router(inventory.router)
app.include_router(box.router)
app.include_router(container.router)
app.include_router(section.router)




