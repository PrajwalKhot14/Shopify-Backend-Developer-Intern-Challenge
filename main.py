import datetime
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

users = sqlalchemy.Table(
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
class UserList(BaseModel):
    id:str
    product_name:str
    category:str
    supplier_id:str
    inventory_status:str
    inventory_on_hand:int
    warehouse_loc:str

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/users", response_model=List[UserList])
async def find_all_users():
    query = users.select()
    return await database.fetch_all(query)
