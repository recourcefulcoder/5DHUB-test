from database.engine import engine
from database.models import Link

from fastapi import status

import pytest

import pytest_asyncio

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.main import app


pytestmark = pytest.mark.asyncio

LINK_ADDRESS = "http://valid.domen/valid/endpoint1"
LINK_SHORTENED = "http://some_shorty/JdhsA8"


@pytest_asyncio.fixture(scope="module")
async def module_session():
    async with async_sessionmaker(engine)() as session1:
        yield session1


@pytest_asyncio.fixture(scope="module", autouse=True)
async def _link_setup(module_session):
    link = Link(
        id=1,
        address=LINK_ADDRESS,
        shortened=LINK_SHORTENED,
    )
    module_session.add(link)
    await module_session.commit()
    yield
    await module_session.execute(delete(Link))
    await module_session.commit()


async def test_307_on_valid(client):
    response = await client.get(
        app.url_path_for("redirect", shorten_url_id="1")
    )
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT


async def test_location_set_on_valid(client):
    response = await client.get(
        app.url_path_for("redirect", shorten_url_id="1")
    )

    headers = dict(response.headers)
    assert "location" in headers.keys()
    assert headers.get("location") == LINK_ADDRESS


async def test_invalid_id(client):
    response = await client.get(
        app.url_path_for("redirect", shorten_url_id="5")
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
