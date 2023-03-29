from app.utils.debugged_devices import new_key_debugged_devices, debugged_devices, count_key_debugged_devices
import asyncio
from datetime import datetime as dt


def debugged_start():
    report_id = dt.now().strftime("%Y%m%d")
    print(report_id)

    if new_key_debugged_devices(report_id=report_id):
        print(f"new_key_debugged_devices finished {dt.now()}")
        print(count_key_debugged_devices(report_id=report_id))
        if debugged_devices(report_id=report_id):
            print("debugged drone devices sucessful")

print(f"start debugging {dt.now()}")
try:
    debugged_start()
except Exception as error:
    print(error)

print(f"Ended debugging {dt.now()}")
    