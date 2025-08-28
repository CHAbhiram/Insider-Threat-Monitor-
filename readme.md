Here’s a **professional README.md** for your **Insider Threat Monitor** project. It includes:

- 📝 **Installation Steps**
- 🏃‍♂️ **How to Run**
- ⚙️ **Dependencies**
- 🖼️ **Screenshots with Descriptions**
- 🛠️ **Code Customization Guide**

---

## 🌟 **README.md**

```markdown
# Insider Threat Monitor

> **Detect and analyze insider threats in real-time using Windows Event Logs (`.evtx`).**

This tool parses `.evtx` files, detects suspicious activities, and provides a web-based dashboard for monitoring login patterns, critical events, and detected threats.

---

## 🚀 Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [How to Run](#how-to-run)
4. [Dependencies](#dependencies)
5. [Screenshots](#screenshots)
6. [Customization](#customization)

---

## 🎯 Overview

The **Insider Threat Monitor** is designed to:
- Parse Windows Security Event Logs (`security.evtx`).
- Detect suspicious activities like after-hours logins, mass file access, and USB device usage.
- Provide a user-friendly dashboard with real-time alerts and analytics.

### Key Features:
- 🔒 **Authentication**: Secure admin login with default credentials (`admin / admin123`).
- 📊 **Dashboard**: Real-time stats and charts.
- 🚨 **Alerts**: Detailed list of detected threats.
- 🕐 **Live Feed**: Real-time event streaming.

---

## 🏁 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/Insider-Threat-Monitor.git
cd Insider-Threat-Monitor
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Prepare Data
Ensure you have a valid `.evtx` file in `data/security.evtx`.

---

## 🚀 How to Run

### 1. Parse Log File
```bash
python core/log_parser.py data/security.evtx data/events.csv
```

### 2. Generate Alerts
```bash
python core/alert_engine.py
```

### 3. Start the Dashboard
```bash
python app.py
```

Open: [http://localhost:5001](http://localhost:5001)

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| Flask   | Web framework |
| pandas  | Data processing |
| Evtx    | Parse `.evtx` logs |
| Flask-Login | Authentication |

Install all dependencies via:
```bash
pip install -r requirements.txt
```

---

## 🖼️ Screenshots

### 1. **Login Page**
![Admin Login](<img width="1880" height="971" alt="Screenshot 2025-08-28 180800" src="https://github.com/user-attachments/assets/7dc5a907-79bb-441b-9cb4-e1e102a17422" />
)
- **Default Credentials**: `admin / admin123`
- **Secure authentication** ensures only authorized users can access sensitive data.

### 2. **Dashboard Home**
![Dashboard Home](<img width="1880" height="973" alt="Screenshot 2025-08-28 180852" src="https://github.com/user-attachments/assets/73dad407-aa1d-4581-92dd-9a788b9744ae" />
)
- **Stats at a Glance**:
  - Total Events
  - Users
  - Critical Events
- **Login Activity Chart**: Shows non-zero hours with login activity.

### 3. **Detected Threats**
![Detected Threats](<img width="1879" height="971" alt="Screenshot 2025-08-28 180915" src="https://github.com/user-attachments/assets/e0ed4fb1-16aa-4cc5-a1e9-7704824000f2" />
)
- **Detailed Alerts**: Lists suspicious activities with timestamps, risk levels, and descriptions.
- **High-risk events** are highlighted for quick action.

### 4. **Live Feed**
![Live Feed](<img width="1886" height="969" alt="Screenshot 2025-08-28 181006" src="https://github.com/user-attachments/assets/d17364db-e6c8-4c3c-b273-3349a6efa08c" />
)
- **Real-time Updates**: Displays ongoing events as they occur.
- **Risk Levels**: Indicates severity for each event.

---

## 🛠️ Customization

### 1. **Change Default Credentials**
Edit `app.py`:
```python
USERS = {
    'admin': {
        'password': 'new_password',  # Change this!
        'id': 1
    }
}
```

### 2. **Modify Detection Rules**
Edit `config/rules.json`:
```json
{
  "after_hours_window": [2, 5],  # After-hours detection window
  "file_access_threshold": 50,    # Threshold for mass file access
  "critical_event_ids": [4624, 4663, 4664, 4688],
  "alert_emails": [],
  "description": "Detection rules for insider threat monitoring",
  "version": "1.0"
}
```

### 3. **Add New Alert Types**
In `core/alert_engine.py`, add new rules under `generate_alerts()`.

### 4. **Change Layout or Styling**
Edit `dashboard/static/style.css` for custom styling.

---

## 📜 License

MIT License © 2025 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, subject to the following conditions...

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 🌐 Deployment

Deploy to:
- Docker
- Heroku
- AWS Elastic Beanstalk


---
