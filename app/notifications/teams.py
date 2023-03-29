import os
import pymsteams

WEBHOOK = os.getenv("WEBHOOK")

def send_by_team(message, color:str = "4cd137"):
    team_message = pymsteams.connectorcard(WEBHOOK)
    team_message.color(color)
    team_message.title("Debugged DrOne devices from COTA V1")
    team_message.text(message)
    team_message.send()
