from http import HTTPStatus

from database.models import Link

import pytest

from sqlalchemy import select

from src.main import app

ENDPOINT_LINK = app.url_path_for("shorten_link")


pytestmark = pytest.mark.asyncio


async def test_201_on_valid(client):
    payload = {
        "link": "http://valid.domen/valid/endpoint1"
    }
    response = await client.post(
        ENDPOINT_LINK,
        json=payload
    )
    assert response.status_code == HTTPStatus.CREATED


async def test_valid_return_json(client):
    payload = {
        "link": "http://valid.domen/valid/endpoint2"
    }
    response = await client.post(
        ENDPOINT_LINK,
        json=payload
    )

    keys = response.json().keys()
    assert "id" in keys
    assert "shortened_link" in keys
    assert len(keys) == 2


async def test_creates_link(client, session):
    payload = {
        "link": "http://valid.domen/valid/endpoint3"
    }
    await client.post(
        ENDPOINT_LINK,
        json=payload
    )
    res = await session.execute(
        select(Link).where(Link.address == payload["link"])
    )
    assert res.scalar() is not None


async def test_rejects_existing_link(client, session):
    payload = {
        "link": "http://valid.domen/valid/endpoint4"
    }
    new_link = Link(
        address=payload["link"],
        shortened="http://some_shorty/JdhsA8",
    )
    session.add(new_link)
    await session.commit()
    response = await client.post(
        ENDPOINT_LINK,
        json=payload
    )
    assert response.status_code == HTTPStatus.CONFLICT
