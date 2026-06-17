# Real-Time XAI-Based DDoS Intrusion Detection Framework

## Project Overview

This project implements a real-time network intrusion detection framework for detecting DDoS traffic using a trained XGBoost classifier. The system captures live network packets, extracts traffic-window features, performs machine learning-based inference, computes SHAP-based explainability values, and displays the detection output through a real-time web dashboard.

The framework is designed as an academic prototype for low-latency DDoS detection and explainable AI-based monitoring. It uses a shared `metrics.json` file to transfer the latest detection-window output from the backend detection engine to the Flask API and frontend dashboard.

---

## Core Components

| File | Purpose |
|---|---|
| `live_ids.py` | Real-time packet capture, feature extraction, XGBoost inference, SHAP computation, and `metrics.json` export engine. |
| `flood.py` | Academic UDP flood traffic injection simulator using 100 concurrent threads and 1 KB payload per packet. Used only for CRITICAL state simulation in a controlled lab environment. |
| `app.py` | Flask web server exposing the `/api/metrics` REST endpoint and serving the XAI monitoring dashboard. |
| `index.html` | Chart.js-powered real-time dashboard frontend. It polls the Flask API every 3 seconds for live metric updates. |
| `xgb_model.json` | Serialized XGBoost classifier trained on the CIC-DDoS2019 dataset and loaded at runtime by `live_ids.py`. |
| `metrics.json` | Shared state file containing the latest detection-window output, including status, SHAP values, traffic telemetry, and timestamp. |

---

## System Architecture

The system follows a lightweight real-time monitoring pipeline:

```text
Live Network Traffic
        |
        v
live_ids.py
(Packet Capture + Feature Extraction)
        |
        v
XGBoost Model Inference
        |
        v
SHAP Explainability Computation
        |
        v
metrics.json
        |
        v
app.py Flask API
/api/metrics
        |
        v
index.html Dashboard
(Chart.js Real-Time Visualization)
```

---

## Main Features

- Real-time network packet capture
- Time-window based traffic feature extraction
- XGBoost-based DDoS traffic classification
- SHAP-based explainable AI output
- Live telemetry export through `metrics.json`
- Flask REST API for serving detection metrics
- Chart.js dashboard with 3-second auto-refresh
- Academic UDP flood simulation for testing CRITICAL alert state

---

## Technology Stack

- Python
- Flask
- XGBoost
- SHAP
- Scapy / packet capture library
- Chart.js
- HTML, CSS, JavaScript
- JSON-based shared state communication

---

## Dataset and Model

The trained model file `xgb_model.json` is based on the CIC-DDoS2019 dataset. The dataset was used to train a multiclass DDoS traffic classifier capable of identifying benign and attack traffic patterns.

At runtime, `live_ids.py` loads the serialized XGBoost model and applies it to extracted traffic-window features.

---

## Runtime Workflow

### 1. Start the Flask Web Server

Run:

```bash
python app.py
```

This starts the Flask backend and exposes the following API endpoint:

```text
/api/metrics
```

The API reads the latest detection result from `metrics.json` and sends it to the frontend dashboard.

---

### 2. Run the Live IDS Engine

Run:

```bash
python live_ids.py
```

Depending on the operating system and packet capture configuration, this script may require administrator or root permission.

Example on Linux:

```bash
sudo python live_ids.py
```

The script continuously captures packets, extracts features, performs XGBoost inference, computes SHAP values, and updates `metrics.json`.

---

### 3. Open the Dashboard

Open the dashboard in a browser through the Flask server.

Example:

```text
http://127.0.0.1:5000
```

The dashboard polls the API every 3 seconds and updates the displayed traffic status, telemetry, and explainability values.

---

### 4. Optional: Run UDP Flood Simulation

The `flood.py` script is used only for academic simulation of a CRITICAL attack state.

Run it only in a controlled local test environment:

```bash
python flood.py
```

This script generates UDP flood traffic using 100 concurrent threads with a 1 KB payload per packet.

---

## `metrics.json` Output

The `metrics.json` file stores the latest computed detection-window result. It works as a shared communication layer between the IDS engine and the Flask API.

Typical information stored includes:

```json
{
  "status": "BENIGN or CRITICAL",
  "prediction": "Predicted traffic class",
  "confidence": "Model confidence score",
  "packets_per_second": "Traffic rate",
  "bytes_per_second": "Bandwidth usage",
  "shap_values": "Feature-level explanation values",
  "timestamp": "Last updated time"
}
```

The exact keys may vary depending on the implementation of `live_ids.py`.

---

## Alert Status Meaning

| Status | Meaning |
|---|---|
| `BENIGN` | Normal or safe traffic condition. |
| `WARNING` | Suspicious traffic pattern or rising traffic intensity. |
| `CRITICAL` | High-risk DDoS-like traffic detected. |

---

## Explainable AI Output

The system uses SHAP values to explain why the XGBoost model made a specific prediction. SHAP helps identify which traffic features contributed most to the final classification.

For example, during a UDP flood attack, features such as packet rate, byte rate, or flow intensity may have higher SHAP impact values. These values are displayed on the dashboard to make the detection decision more transparent.

---

## Safety and Ethical Use

This project is intended only for academic research, controlled simulation, and defensive cybersecurity learning.

The `flood.py` script must not be used against public networks, third-party servers, or any system without permission. It should only be executed in a local lab environment where all devices and network resources are owned or authorized by the researcher.

Misuse of traffic injection tools can violate laws, institutional policies, and ethical cybersecurity guidelines.

---

## Recommended Project Structure

```text
project-folder/
│
├── app.py
├── flood.py
├── live_ids.py
├── index.html
├── xgb_model.json
├── metrics.json
└── README.md
```

---

## Limitations

- The system is an academic prototype, not a production-grade IDS.
- Detection accuracy depends on the quality of the trained CIC-DDoS2019-based model.
- Live packet capture may require administrator privileges.
- The UDP flood simulator is only suitable for controlled testing.
- The shared `metrics.json` approach is simple and lightweight but may not be ideal for large-scale deployment.
- Performance may vary depending on hardware, network speed, and traffic volume.

---

## Future Improvements

- Add database logging for historical attack records
- Add authentication for the monitoring dashboard
- Replace `metrics.json` with WebSocket or message queue-based communication
- Add support for more attack classes
- Improve real-time feature extraction accuracy
- Deploy the system using Docker
- Add email or Telegram alert notifications
- Integrate model retraining pipeline

---

## Academic Use Case

This framework supports research on real-time DDoS detection, low-latency traffic classification, explainable AI, and lightweight security monitoring dashboards. It demonstrates how a trained machine learning model can be integrated into a live packet monitoring system with interpretable outputs.

---

## Author

Prepared as part of an academic research project on multiclass DDoS traffic detection and explainable intrusion detection systems.
