import uuid
import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
from passlib.context import CryptContext

pwd_context = CryptContext(schemes= ["bcrypt"], deprecated = "auto")

#Database:
dbname = "shopify"
username = "postgres"
password = "9663168172"
DATABASE_URL = "postgresql://"+username+":"+password+"@127.0.0.1:5432/"+dbname+""
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

invents = sqlalchemy.Table(
    "py_users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("product_name", sqlalchemy.String),
    sqlalchemy.Column("category", sqlalchemy.String),
    sqlalchemy.Column("supplier_id", sqlalchemy.String),
    sqlalchemy.Column("inventory_status", sqlalchemy.String),
    sqlalchemy.Column("inventory_on_hand", sqlalchemy.INT),
    sqlalchemy.Column("warehouse_loc", sqlalchemy.String)
)
engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)

# Models
class InventoryList(BaseModel):
    id:str
    product_name:str
    category:str
    supplier_id:str
    inventory_status:str
    inventory_on_hand:int
    warehouse_loc:str

class InventoryAdd(BaseModel):
    product_name: str = Field(..., example = "Overwatch")
    category: str = Field(..., example = "Games")
    supplier_id: str = Field(..., example = "c85389ea-7129-11ec-a6c8-7e75a04c9795")
    inventory_status: str = Field(..., example = "Received/ Transit/ Order Placed")
    inventory_on_hand: int = Field(..., example = 100)
    warehouse_loc: str = Field(..., example = "Chicago")

class InventoryUpdate(BaseModel):
    id: str = Field(..., example = "Enter the item ID")
    product_name: str = Field(..., example="Overwatch")
    category: str = Field(..., example="Games")
    supplier_id: str = Field(..., example="c85389ea-7129-11ec-a6c8-7e75a04c9795")
    inventory_status: str = Field(..., example="Received/ Transit/ Order Placed")
    inventory_on_hand: int = Field(..., example=100)
    warehouse_loc: str = Field(..., example="Chicago")

class InventDelete(BaseModel):
    id: str = Field(..., exclude="Enter the item ID")


app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/inventory", response_model=List[InventoryList])
async def find_all_invents():
    query = invents.select()
    return await database.fetch_all(query)

@app.post("/inventory", response_model=InventoryList)
async def add_item(invent: InventoryAdd):
    gID = str(uuid.uuid1())
    query = invents.insert().values(
        id = gID,
        product_name = invent.product_name,
        category = invent.category,
        supplier_id = invent.supplier_id,
        inventory_status = invent.inventory_status,
        inventory_on_hand = invent.inventory_on_hand,
        warehouse_loc = invent.warehouse_loc
    )

    await database.execute(query)
    return {
        "id":gID,
        **invent.dict()
    }

@app.get("/inventory/{inventoryid}", response_model=InventoryList)
async def find_by_id(inventId : str):
    query = invents.select().where(invents.c.id == inventId)
    return await database.fetch_one(query)

@app.delete("/inventory/{inventoryid}")
async def delete_invent(invent:InventDelete):
    query = invents.delete().where(invents.c.id==invent.id)
    await database.execute(query)

    return {
        "status": True,
        "message": "Item was successfully deleted"
    }