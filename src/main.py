from contextlib import asynccontextmanager
from typing import Optional

from database.engine import engine
from database.models import Base, Link

from fastapi import Body, FastAPI, HTTPException, Request, Response, status

import pyshorteners

import sqlalchemy.exc as se
from sqlalchemy import select

import src.dependencies as dp
import src.pydmodels as pym


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

shortener = pyshorteners.Shortener()


@app.get("/hello-world")
async def hello_world():
    return {"message": "Hello, world!"}


@app.post("/")
async def shorten_link(
    payload: pym.LinkContent,
    session: dp.SessionDep,
    response: Response
):
    new_link = Link(
        address=str(payload.link),
        shortened=shortener.tinyurl.short(str(payload.link))
    )
    try:
        session.add(new_link)
        await session.commit()
        response.status_code = status.HTTP_201_CREATED
    except se.IntegrityError:
        await session.rollback()
        res = await session.execute(
            select(Link)
            .where(Link.address == new_link.address)
        )
        link = res.scalar()
        if link is not None:
            response.status_code = status.HTTP_409_CONFLICT
            return {
                "error": f"given link is already shortened (ID: {link.id})"
            }
        else:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"error": "unexpected error occurred, try again later"}
    return {"id": new_link.id, "shortened_link": new_link.shortened}


@app.get("/{shorten_url_id}")
async def redirect(
    session: dp.SessionDep,
    shorten_url_id: int,
    response: Response
):
    link = await session.get(Link, shorten_url_id)
    if link is None:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {"error": "given link not found"}
    response.status_code = status.HTTP_307_TEMPORARY_REDIRECT
    response.headers["Location"] = link.address
    return


@app.get("/make_request/{shorten_url_id}")
@app.post("/make_request/{shorten_url_id}")
async def request_service(
    request: Request,
    client: dp.ClientDep,
    session: dp.SessionDep,
    response: Response,
    shorten_url_id: int,
    data: Optional[dict] = Body(None),
):

    link = await session.get(Link, shorten_url_id)
    if link is None:
        response.status_code = status.HTTP_409_CONFLICT
        return {"error": "link with provided ID doesn't exist"}

    headers = dict(request.headers)
    headers.pop("content-length", None)

    if request.method == "GET":
        api_response = await client.get(
            link.address,
            headers=headers
        )
        # response.status_code = api_response.status_code

    if request.method == "POST":
        if data is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="POST request requires data to be sent!"
            )

        api_response = await client.post(
            link.address,
            json=data,
            headers=headers
        )

    return Response(
        content=api_response.content,
        status_code=api_response.status_code
    )
