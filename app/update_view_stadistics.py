import asyncio
from app.db.connections.connect import connect
from app.db.query import refresh_count_dasboard

def refresh_view_count() -> bool:
    async def async_work():
        connection = await connect()
        await connection.execute(refresh_count_dasboard)

    try:
        asyncio.run(async_work())
        return True
    except Exception as error:
        raise Exception(error)