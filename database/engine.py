from sqlalchemy import URL, create_engine

import src.settings as settings

url_object = URL.create(
    "postgresql+psycopg2",
    username=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    database=settings.POSTGRES_DB,
    host=settings.DB_HOST,
    port=settings.DB_PORT
)
engine = create_engine(url_object)
