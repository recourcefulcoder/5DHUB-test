import pytest_asyncio

from database.engine import engine
from database.models import Base, Link

from src.main import app

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import async_sessionmaker

from httpx import ASGITransport, AsyncClient

from . import testvars


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        base_url=testvars.BASE_TEST_URL,
        transport=ASGITransport(app)
    ) as client1:
        yield client1


@pytest_asyncio.fixture
async def session():
    async with async_sessionmaker(engine)() as session1:
        yield session1


@pytest_asyncio.fixture(scope="module")
async def module_session():
    async with async_sessionmaker(engine)() as session1:
        yield session1


@pytest_asyncio.fixture(scope="session", autouse=True)
async def _setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest_asyncio.fixture(scope="module", autouse=True)
async def _teardown_db(module_session):
    yield
    await module_session.execute(delete(Link))
    await module_session.commit()

