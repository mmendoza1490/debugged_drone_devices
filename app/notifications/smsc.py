
import os
import json
import smpplib.client
import smpplib.consts
import smpplib.gsm


SMSC_IP = os.getenv("SMSC_IP")
SMSC_PORT = os.getenv("SMSC_PORT")
SYSTEM_ID = os.getenv("SYSTEM_ID")
SYSTEM_PASS = os.getenv("SYSTEM_PASS")
SENDER_ID = os.getenv("SENDER_ID")
SYSTEM_TYPE= os.getenv("SYSTEM_TYPE")
PHONE= json.loads(os.getenv("MONITOR_PHONE"))

#.----------SMPP Notification ----------------------
def send_sms_by_smpp(text: str):
    text = "Debugged DrOne devices from COTA V1 - " + text
    # Two parts, GSM default / UCS2, SMS with UDH
    parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(text)

    # Connect to the remote SMSC gateway                                                                                                                      
    client = smpplib.client.Client(SMSC_IP, SMSC_PORT)
    client.connect()

    # Bind to the SMSC with the credential                                                                                                                    
    client.bind_transceiver(system_id=SYSTEM_ID, password=SYSTEM_PASS, system_type=SYSTEM_TYPE)
    for number in PHONE:
        for part in parts:
            client.send_message(
                source_addr_ton=smpplib.consts.SMPP_TON_INTL,
                source_addr=SENDER_ID,
                dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
                dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
                destination_addr=number,
                short_message=part,
                data_coding=encoding_flag,
                esm_class=msg_type_flag,
                registered_delivery=True,
            )
                                                                                                                       
    client.unbind()
    client.disconnect()
