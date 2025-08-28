# core/log_parser.py
import os
import sys
from Evtx.Evtx import Evtx
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime

def parse_evtx_to_csv(evtx_path, output_csv):
    """Parse .evtx file and save to CSV"""
    print(f"🔍 Parsing: {evtx_path}")
    events = []

    try:
        with Evtx(evtx_path) as log:
            for record in log.records():
                try:
                    node = ET.fromstring(record.xml())
                    event_data = extract_event_data(node)
                    if event_data:
                        events.append(event_data)
                except Exception as e:
                    continue  # Skip malformed records

        df = pd.DataFrame(events)
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)
        df.to_csv(output_csv, index=False)
        print(f"✅ Saved {len(df)} events to {output_csv}")
        return df

    except Exception as e:
        print(f"❌ Error parsing {evtx_path}: {e}")
        return pd.DataFrame()

def extract_event_data(node):
    """Extract key fields from Windows Event XML"""
    data = {
        'timestamp': None,
        'event_id': None,
        'user': 'N/A',
        'domain': 'N/A',
        'ip': 'N/A',
        'source_host': 'N/A',
        'details': ''
    }

    # Timestamp
    time_elem = node.find(".//{*}TimeCreated")
    if time_elem is not None:
        data['timestamp'] = time_elem.get("SystemTime")

    # Event ID
    id_elem = node.find(".//{*}EventID")
    if id_elem is not None:
        try:
            data['event_id'] = int(id_elem.text)
        except:
            pass

    # User info
    user_elem = node.find(".//{*}TargetUserName")
    if user_elem is not None:
        data['user'] = user_elem.text or 'N/A'

    domain_elem = node.find(".//{*}TargetDomainName")
    if domain_elem is not None:
        data['domain'] = domain_elem.text or 'N/A'

    # Source IP
    ip_elem = node.find(".//{*}IpAddress")
    if ip_elem is not None and ip_elem.text:
        data['ip'] = ip_elem.text

    # Source Host
    host_elem = node.find(".//{*}WorkstationName")
    if host_elem is not None:
        data['source_host'] = host_elem.text or 'N/A'

    data['details'] = f"Event ID {data['event_id']}"

    return data

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python log_parser.py <logfile.evtx> [output.csv]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "../data/events.csv"

    if not os.path.exists(input_file):
        print(f"[❌] File not found: {input_file}")
        sys.exit(1)

    parse_evtx_to_csv(input_file, output_file)