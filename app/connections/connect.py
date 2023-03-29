import os
import asyncpg
from dotenv import load_dotenv

load_dotenv(override=True)

async def connect():
    return await asyncpg.connect(
        host=os.getenv("host"),
        database=os.getenv("database"),
        user=os.getenv("user"),
        port=os.getenv("port"),
        password=os.getenv("password"),
        ssl="disable",
    )