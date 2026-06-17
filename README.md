# Computer-Security-Research-Paper-core-implementation-codes
This project implements a real-time network intrusion detection framework for detecting DDoS traffic using a trained XGBoost classifier. The system captures live network packets, extracts traffic-window features, performs machine learning-based inference, computes SHAP-based explainability values, and displays the detection output through a real-time web dashboard.

The framework is designed as an academic prototype for low-latency DDoS detection and explainable AI-based monitoring. It uses a shared metrics.json file to transfer the latest detection-window output from the backend detection engine to the Flask API and frontend dashboard.

Core Components
File	Purpose
live_ids.py	Real-time packet capture, feature extraction, XGBoost inference, SHAP computation, and metrics.json export engine.
flood.py	Academic UDP flood traffic injection simulator using 100 concurrent threads and 1 KB payload per packet. Used only for CRITICAL state simulation in a controlled lab environment.
app.py	Flask web server exposing the /api/metrics REST endpoint and serving the XAI monitoring dashboard.
index.html	Chart.js-powered real-time dashboard frontend. It polls the Flask API every 3 seconds for live metric updates.
xgb_model.json	Serialized XGBoost classifier trained on the CIC-DDoS2019 dataset and loaded at runtime by live_ids.py.
metrics.json	Shared state file containing the latest detection-window output, including status, SHAP values, traffic telemetry, and timestamp.
System Architecture
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
Main Features
Real-time network packet capture
Time-window based traffic feature extraction
XGBoost-based DDoS traffic classification
SHAP-based explainable AI output
Live telemetry export through metrics.json
Flask REST API for serving detection metrics
Chart.js dashboard with 3-second auto-refresh
Academic UDP flood simulation for testing CRITICAL alert state
Safety and Ethical Use

This project is intended only for academic research, controlled simulation, and defensive cybersecurity learning.

The flood.py script must not be used against public networks, third-party servers, or any system without permission. It should only be executed in a local lab environment where all devices and network resources are owned or authorized by the researcher.

Misuse of traffic injection tools can violate laws, institutional policies, and ethical cybersecurity guidelines.
:::
