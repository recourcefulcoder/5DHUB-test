from typing import Annotated

from database.engine import engine

from httpx import AsyncClient

from fastapi import Depends

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


async def get_session():
    async with async_sessionmaker(
            engine,
            expire_on_commit=False
    )() as session:
        yield session


async def get_async_client():
    async with AsyncClient() as client:
        yield client


SessionDep = Annotated[AsyncSession, Depends(get_session)]
ClientDep = Annotated[AsyncClient, Depends(get_async_client)]
