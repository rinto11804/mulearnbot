import psycopg2
import os
from dotenv import load_dotenv
from typing import Final

load_dotenv()

DB_URL: Final[str] = os.getenv("DB_URL")

try:
    connection = psycopg2.connect(dsn=DB_URL + "=disable")
except Exception as e:
    print(e)
