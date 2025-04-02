import logging
import os
from pathlib import Path

from dotenv import load_dotenv


def load_environ():
    base_dir = Path(__file__).resolve().parent.parent
    env_file = base_dir / ".env"
    if os.path.isfile(env_file):
        load_dotenv(env_file)
    else:
        logging.warning(".env file not found!")


load_environ()


POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DB_HOST = os.getenv("DB_HOST", default="localhost")
DB_PORT = int(os.getenv("DB_PORT", default="5432"))

TEST_POSTGRES_DB = os.getenv("TEST_POSTGRES_DB")
TESTING = os.getenv("TESTING", default="False").lower() in [
    "true",
    "yes",
    "y",
    "1",
]
