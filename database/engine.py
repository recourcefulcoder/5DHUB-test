from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine

import src.settings as settings

DB_NAME = settings.TEST_POSTGRES_DB if settings.TESTING \
    else settings.POSTGRES_DB

url_object = URL.create(
    "postgresql+asyncpg",
    username=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    database=DB_NAME,
    host=settings.DB_HOST,
    port=settings.DB_PORT
)
engine = create_async_engine(url_object)
