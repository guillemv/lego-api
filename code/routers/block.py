
# from fastapi import APIRouter,status,Body,HTTPException
# import motor.motor_asyncio
# from typing import Optional,List
# from pydantic import BaseModel,Field,ConfigDict
# from bson import ObjectId
# from typing_extensions import Annotated
# from pydantic.functional_validators import BeforeValidator
# router=APIRouter()


# PyObjectId = Annotated[str, BeforeValidator(str)]


# class ColorModel(BaseModel):
#     id: Optional[PyObjectId] = Field(alias="_id", default=None)
#     Name:str=Field(...)
#     Supracolor:str=Field(...)
#     ID:int=Field(...)
#     RGB:str=Field(...)
#     Bricklink:str=Field(...)
#     Lego:str=Field(...)
#     model_config=ConfigDict(
#         populate_by_name=True,
#         arbitrary_types_allowed=True,
#         json_schema_extra={
#             "example":{
#                 "brick_id":"2334",
#                 "Name":"Bright Green",
#                 "Supracolor":"Green",
#                 "ID":23,
#                 "RGB":"4B9F4A",
#                 "Bricklink":"36",
#                 "Lego":"37 ['Bright Green', 'BR.GREEN']"
#             }
#         }
#     )

# class UpdateBrickModel(BaseModel):
#     """
#     A set of optional updates to be made to a document in the database.
#     """

#     brick_id: Optional[str] = None
#     color: Optional[str] = None
#     box: Optional[str] = None
#     count: Optional[int] = None
#     model_config = ConfigDict(
#         arbitrary_types_allowed=True,
#         json_encoders={ObjectId: str},
#         json_schema_extra={
#             "example":{
#                 "brick_id":"2334",
#                 "color":"32",
#                 "box":"0-B-1",
#                 "count":23
#             }
#         },
#     )

# class BrickCollection(BaseModel):
#     bricks: List[ColorModel]


# @router.post("/bricks/",
#     response_description="Add new brick",
#     response_model=BrickModel,
#     status_code=status.HTTP_201_CREATED,
#     response_model_by_alias=False,
# )
# async def create_brick(brick: BrickModel = Body(...)):
#     """
#     Insert a new brick record.

#     A unique `id` will be created and provided in the response.
#     """
#     new_brick = await lego_collection.insert_one(
#         brick.model_dump(by_alias=True, exclude=["id"])
#     )
#     created_brick = await lego_collection.find_one(
#         {"_id": new_brick.inserted_id}
#     )
#     return created_brick

# @router.get(
#     "/bricks/",
#     response_description="List all bricks",
#     response_model=BrickCollection,
#     response_model_by_alias=False,
# )
# async def list_bricks(
#     color: Optional[str]=None
# ):
#     query_params={}
#     if color:
#         query_params['color']=color
#     return BrickCollection(bricks=await lego_collection.find(query_params).to_list(1000))


# @router.put(
#     "/bricks/{id}",
#     response_description="Update a brick",
#     response_model=BrickModel,
#     response_model_by_alias=False,
# )
# async def update_brick(id: str, brick: UpdateBrickModel = Body(...)):
#     """
#     Update individual fields of an existing brick record.

#     Only the provided fields will be updated.
#     Any missing or `null` fields will be ignored.
#     """
#     brick = {
#         k: v for k, v in brick.model_dump(by_alias=True).items() if v is not None
#     }

#     if len(brick) >= 1:
#         update_result = await lego_collection.find_one_and_update(
#             {"_id": ObjectId(id)},
#             {"$set": brick},
#             return_document=ReturnDocument.AFTER,
#         )
#         if update_result is not None:
#             return update_result
#         else:
#             raise HTTPException(status_code=404, detail=f"Brick {id} not found")

#     # The update is empty, but we should still return the matching document:
#     if (existing_brick := await lego_collection.find_one({"_id": id})) is not None:
#         return existing_brick

#     raise HTTPException(status_code=404, detail=f"Brick {id} not found")

