# core/wef_collector.py
import requests
import xml.etree.ElementTree as ET
import pandas as pd
import time
from datetime import datetime

# WEF Configuration
WEF_SERVER = "http://wef-server.contoso.com:5985/wsman"
WEF_COLLECTION_URI = "/subscription/Microsoft-Windows-Security-Auditing"
AUTH = ("admin", "SecurePass123!")  # Use Windows Auth in prod

def poll_wef_events():
    """
    Poll WEF server for new security events
    Uses WinRM (WS-Man) protocol
    """
    headers = {
        "Content-Type": "application/soap+xml; charset=UTF-8"
    }

    # SOAP request to pull events
    soap_body = """
    <Envelope xmlns="http://www.w3.org/2003/05/soap-envelope">
        <Body>
            <Pull xmlns="http://schemas.xmlsoap.org/ws/2005/02/transfer">
                <EnumerationContext>1</EnumerationContext>
            </Pull>
        </Body>
    </Envelope>
    """

    try:
        response = requests.post(
            WEF_SERVER + WEF_COLLECTION_URI,
            data=soap_body,
            headers=headers,
            auth=AUTH,
            timeout=10
        )

        if response.status_code == 200:
            return parse_wef_response(response.text)
        else:
            print(f"WEF Error: {response.status_code}")
            return []

    except Exception as e:
        print(f"Connection failed: {e}")
        return []

def parse_wef_response(xml_data):
    """Extract events from WEF SOAP response"""
    events = []
    root = ET.fromstring(xml_data)

    for item in root.findall(".//{*}Item"):
        event_data = {
            'timestamp': None,
            'event_id': None,
            'user': 'N/A',
            'domain': 'N/A',
            'ip': 'N/A',
            'source_host': 'N/A'
        }

        # Extract from Event XML
        event_node = item.find(".//{*}Event")
        if event_node is not None:
            system = event_node.find(".//{*}System")
            if system is not None:
                event_id = system.find(".//{*}EventID")
                if event_id is not None:
                    event_data['event_id'] = int(event_id.text)

                time_created = system.find(".//{*}TimeCreated")
                if time_created is not None:
                    event_data['timestamp'] = time_created.get("SystemTime")

            user_data = event_node.find(".//{*}UserData")
            if user_data is not None:
                user = user_data.find(".//{*}TargetUserName")
                if user is not None:
                    event_data['user'] = user.text

        events.append(event_data)

    return events

def stream_events_to_csv():
    """Continuously poll WEF and update CSV"""
    output_file = "../data/wef_events_live.csv"
    print("📡 Streaming events from WEF server...")

    while True:
        new_events = poll_wef_events()
        if new_events:
            df = pd.DataFrame(new_events)
            df.to_csv(output_file, mode='a', header=not pd.io.common.file_exists(output_file), index=False)
            print(f"📥 Received {len(new_events)} events at {datetime.now()}")
        time.sleep(30)  # Poll every 30 sec