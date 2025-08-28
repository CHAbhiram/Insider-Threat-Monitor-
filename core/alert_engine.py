# core/alert_engine.py
import pandas as pd
import json
import os
from datetime import datetime

# Get directory of the current script
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Dynamic paths
RULES_FILE = os.path.join(CURRENT_DIR, "..", "config", "rules.json")
RULES_FILE = os.path.abspath(RULES_FILE)

EVENTS_CSV = os.path.join(CURRENT_DIR, "..", "data", "events.csv")
EVENTS_CSV = os.path.abspath(EVENTS_CSV)

def load_rules():
    """Load detection rules from JSON"""
    if not os.path.exists(RULES_FILE):
        print(f"[❌] Rules file not found: {RULES_FILE}")
        sys.exit(1)
    with open(RULES_FILE, 'r') as f:
        return json.load(f)

def load_events(csv_file):
    """Load events CSV into DataFrame"""
    if not os.path.exists(csv_file):
        print(f"[⚠️] Event file not found: {csv_file}")
        return pd.DataFrame()
    try:
        df = pd.read_csv(csv_file, parse_dates=['timestamp'])
        print(f"✅ Loaded {len(df)} events from {csv_file}")
        return df
    except Exception as e:
        print(f"[❌] Failed to read CSV: {e}")
        return pd.DataFrame()

def generate_alerts(df, rules):
    """Generate alerts based on rules"""
    alerts = []

    # Rule 1: After-hours logins (2 AM - 5 AM)
    night_start = rules["after_hours_window"][0]
    night_end = rules["after_hours_window"][1]
    night_logins = df[
        (df['event_id'] == 4624) &
        (df['timestamp'].dt.hour >= night_start) &
        (df['timestamp'].dt.hour <= night_end)
    ]
    for _, row in night_logins.iterrows():
        alerts.append({
            'type': 'After-Hours Login',
            'user': row['user'],
            'time': row['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
            'risk': 'High',
            'details': f"Suspicious login at {row['timestamp'].hour}:00"
        })

    # Rule 2: Mass file access
    file_events = df[df['event_id'] == 4663].copy()
    file_events['hour_bucket'] = file_events['timestamp'].dt.floor('h')
    access_counts = file_events.groupby(['user', 'hour_bucket']).size().reset_index(name='count')
    bulk_access = access_counts[access_counts['count'] > rules["file_access_threshold"]]
    for _, row in bulk_access.iterrows():
        alerts.append({
            'type': 'Mass File Access',
            'user': row['user'],
            'time': row['hour_bucket'].strftime('%Y-%m-%d %H:%M:%S'),
            'risk': 'High',
            'details': f"Accessed {int(row['count'])} files in one hour"
        })

    # Rule 3: USB Device Access
    usb_events = df[df['event_id'] == 4664]
    for _, row in usb_events.iterrows():
        alerts.append({
            'type': 'USB Device Access',
            'user': row['user'],
            'time': row['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
            'risk': 'Medium',
            'details': 'Removable storage accessed'
        })

    return alerts

def save_alerts(alerts, output_file=None):
    """Save alerts to CSV"""
    if output_file is None:
        output_file = os.path.join(CURRENT_DIR, "..", "data", "alerts.csv")
        output_file = os.path.abspath(output_file)

    if alerts:
        df = pd.DataFrame(alerts)
        df.to_csv(output_file, index=False)
        print(f"🚨 {len(alerts)} alerts generated and saved to {output_file}")
    else:
        print("✅ No alerts generated.")

# --- Main Execution ---
if __name__ == "__main__":
    import sys  # Add this at top or here for exit()

    print("🚀 Starting Insider Threat Analysis...")

    # Load rules
    rules = load_rules()

    # Load events
    events_df = load_events(EVENTS_CSV)

    if not events_df.empty:
        alerts = generate_alerts(events_df, rules)
        save_alerts(alerts)
    else:
        print("No events to analyze.")
        sys.exit(1)