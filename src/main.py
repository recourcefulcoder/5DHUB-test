from contextlib import asynccontextmanager

from database.engine import engine
from database.models import Base

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/hello-world")
async def hello_world():
    return {"message": "Hello, world!"}
