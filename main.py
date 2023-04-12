import os
from app.debugged_devices import (
    new_key_debugged_devices,
    debugged_devices,
    count_key_debugged_devices,
)
from app.update_view_stadistics import refresh_view_count
import asyncio
from datetime import datetime as dt
from app.notifications.teams import send_by_team
from app.notifications.smsc import send_sms_by_smpp
from dotenv import load_dotenv
from app.utils.logger.log_config import get_logger

load_dotenv(override=True)

logger = get_logger(__name__)

enviroment = os.getenv("enviroment")

notification = {
    "set_new_key": {
        "started": False,
        "finished":False,
        "msg":"""Enviroment: {2}\n Error when trying set a new key '{0}' to debugged \n
        Error:{1}"""
    },
    "count_new_key":{
        "started": False,
        "finished": False,
        "msg": """Enviroment: {2}\n
        Error trying count the new key '{0}',
        urgent to verify right now because devices were
        set with de new key but were not debugged\n
        Error:{1}"""
    },
    "debugged_devices":{
        "started": False,
        "finished": False,
        "msg": """Enviroment: {2}\n
        Error trying debugged drone devices with key '{0}', 
        urgent to verify right now because devices were set with de new key but were not debugged\n
        Error: {1}"""
    },
    "archived_successful":{
        "started": False,
        "finished": False,
        "msg": """Enviroment: {2}\n
        error trying to mark debugged devices in devicedata2 table - key '{0}',
        in the next execution it will try to dial again \n
        Error: {1}"""
    },
    "refresh_view_successful":{
        "started": False,
        "finished": False,
        "msg": """Enviroment: {2}\n
        Error trying to refresh view to the dashboard,
        you can execute manually.\n
        Error: {1}"""
    },
    "debugged_successful":{
        "started": False,
        "finished": False,
        "msg": """Enviroment: {1}\n
        Debugged drone devices successful, \n
        Result: {0}"""
    },
    "debugged_empty":{
        "started": False,
        "finished": False,
        "msg": """Enviroment: {0}\n
        There were not data to debugg"""
    },
}

report_id = dt.now().strftime("%Y%m%d")

def debugged_start():
    count_debugged = None

    notification["set_new_key"]["started"] = True
    if new_key_debugged_devices(report_id=report_id):
        logger.debug(f"new_key_debugged_devices finished successfully")
        notification["set_new_key"]["finished"] = True

        notification["count_new_key"]["started"] = True
        count_debugged = count_key_debugged_devices(report_id=report_id)
        logger.debug(f"count_debugged: {count_debugged}")
        logger.debug(f"count_key_debugged_devices finished successfully")
        notification["count_new_key"]["finished"] = True

        notification["debugged_devices"]["started"] = True
        if debugged_devices(report_id=report_id, key="debugged"):
            logger.debug(f"debugged_devices finished successfully")
            notification["debugged_devices"]["finished"] = True

            notification["archived_successful"]["started"] = True
            if debugged_devices(report_id=report_id, key="archived"):
                logger.debug(f"archived_successful finished successfully")
                notification["archived_successful"]["finished"] = True

                notification["refresh_view_successful"]["started"] = True
                if refresh_view_count():
                    logger.debug(f"refresh_view_successful finished successfully")
                    notification["refresh_view_successful"]["finished"] = True

    return count_debugged

logger.debug(f"start debugging")
try:
    count_result = debugged_start()
    result = {row["brand"]: row["total"] for row in count_result["Total_debugged"]}

    if result:
        logger.info(result)
        msg = str(notification["debugged_successful"]["msg"]).format(result, enviroment)
    else:
        msg = str(notification["debugged_empty"]["msg"]).format(enviroment)
        
    # send notification
    logger.debug("sending notification...")
    send_by_team(message=msg)
    send_sms_by_smpp(text=msg)
    logger.debug("notification sent successfuly...")

except Exception as error:
    logger.debug(error)
    for key, value in notification.items():
        if value["finished"] == False and value["started"] == True:
            msg = str(notification[key]["msg"]).format(report_id, error, enviroment)
            send_by_team(message=msg, color="e84118")
            send_sms_by_smpp(text=msg)
            break

logger.debug(f"Ended debugging")

