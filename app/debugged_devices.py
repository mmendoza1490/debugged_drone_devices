import asyncio
from app.db.connections.connect import connect
from app.db.query import (
    set_debugged_devices,
    debbuged_devices,
    count_debugged_devices,
)
from app.utils.build_query_by_args import build_query_by_args
from enum import Enum
import json
from datetime import datetime as dt

class ReportReference(Enum):
    DRONE_DEVICES = {
        "id": 7,
        "total": int(),
        "count": count_debugged_devices,
        "update": debbuged_devices,
        "new_key": set_debugged_devices,
    }

def new_key_debugged_devices(report_id) -> bool:
    async def async_work():
        connection = await connect()

        report_type = ReportReference.DRONE_DEVICES
        
        report_payload = {
            "new_report_payload": json.dumps(
                {str(report_id): [report_type.value["id"]]}
            )  ,
            "new_status": json.dumps(report_type.value["id"]),
            "str_report_id": report_id,
        }


        query, params = build_query_by_args(report_type.value["new_key"], report_payload, report_id = f"'{{{str(report_id)}, -1}}'")

        await connection.execute(query, *params)

    try:
        asyncio.run(async_work())
        return True
    except Exception as error:
        raise Exception(error)


def count_key_debugged_devices(report_id) -> bool:
    async def async_work():
        connection = await connect()

        report_type = ReportReference.DRONE_DEVICES

        report_payload = {
            "new_status": json.dumps(report_type.value["id"]),
            "str_report_id": str(report_id),
        }

        query, params = build_query_by_args(report_type.value["count"], report_payload)

        total = await connection.fetch(query, *params)

        return total

    try:
        return {"Total_debugged": asyncio.run(async_work())}
    except Exception as error:
        raise Exception(error)


def debugged_devices(report_id) -> bool:
    async def async_work():
        connection = await connect()

        report_type = ReportReference.DRONE_DEVICES

        report_payload = {
            "new_status": json.dumps(report_type.value["id"]),
            "str_report_id": str(report_id),
        }

        query, params = build_query_by_args(report_type.value["update"], report_payload)

        await connection.execute(query, *params)

    try:
        asyncio.run(async_work())
        return True
    except Exception as error:
        raise Exception(error)