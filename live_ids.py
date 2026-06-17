import pyshark
import time
import pandas as pd
import numpy as np
import xgboost as xgb
import shap
import json
import os

try:
    xgb_model = xgb.XGBClassifier()
    xgb_model.load_model("xgb_model.json")
    print("[+] Machine Learning Model Loaded Successfully.")
    explainer = shap.TreeExplainer(xgb_model)
    print("[+] SHAP Explainable AI Engine Loaded Ready.")
except Exception as e:
    print(f"[-] Model loading failed: {e}.")
    xgb_model = None
    explainer = None

FEATURE_NAMES = [
    'Flow Duration', 'Total Fwd Packets', 'Total Backward Packets',
    'Total Length of Fwd Packets', 'Flow Bytes/s', 'Flow Packets/s'
]

def start_live_ids_engine(interface_name='en0', window_duration=10):
    print(f"\n==================================================================")
    print(f"    STARTING REAL-TIME DDOS ENGINE WITH SHAP EXPLAINABLE AI (XAI) ")
    print(f"==================================================================")
    
    window_count = 1
    
    while True:
        print(f"[INFO] Time-Window {window_count}: Capturing live network flows...")
        start_time = time.time()
        
        fwd_packets = 0
        bwd_packets = 0
        fwd_lengths = 0
        total_bytes = 0
        local_ip = "192.168.0.110" 
        
        capture = pyshark.LiveCapture(
            interface=interface_name,
            display_filter="ip and not dns"
        )
        
        for packet in capture.sniff_continuously():
            if time.time() - start_time > window_duration:
                break
                
            try:
                p_len = int(packet.length)
                total_bytes += p_len
                if hasattr(packet, 'ip'):
                    if packet.ip.src == local_ip:
                        fwd_packets += 1
                        fwd_lengths += p_len
                    else:
                        bwd_packets += 1
            except AttributeError:
                continue
                
        actual_duration = time.time() - start_time
        flow_packets_per_sec = (fwd_packets + bwd_packets) / actual_duration if actual_duration > 0 else 0
        flow_bytes_per_sec = total_bytes / actual_duration if actual_duration > 0 else 0
        
        raw_features = {
            'Flow Duration': actual_duration,
            'Total Fwd Packets': fwd_packets,
            'Total Backward Packets': bwd_packets,
            'Total Length of Fwd Packets': fwd_lengths,
            'Flow Bytes/s': flow_bytes_per_sec,
            'Flow Packets/s': flow_packets_per_sec
        }
        
        df_input = pd.DataFrame([raw_features], columns=FEATURE_NAMES)
        
        shap_contributions = {}
        status = "SAFE"
        primary_trigger = "None"
        
        if xgb_model:
            pred_encoded = xgb_model.predict(df_input)[0]
            
            if explainer:
                shap_values = explainer.shap_values(df_input)
                if len(shap_values.shape) == 3:
                    current_shap = shap_values[0, :, int(pred_encoded)]
                else:
                    current_shap = shap_values[0]
                
                top_feature_idx = np.argmax(np.abs(current_shap))
                primary_trigger = FEATURE_NAMES[top_feature_idx]
                
                for name, value in zip(FEATURE_NAMES, current_shap):
                    shap_contributions[name] = float(value)

            if pred_encoded != 0 or flow_packets_per_sec > 200:
                status = "CRITICAL"
                if pred_encoded == 0:
                    primary_trigger = "Flow Packets/s (Threshold Override)"
                    shap_contributions["Flow Packets/s"] = 1.5
            
        # Metrics এক্সপোর্ট করা JSON ফাইলে
        export_data = {
            "status": status,
            "packets_per_sec": round(flow_packets_per_sec, 2),
            "bytes_per_sec": round(flow_bytes_per_sec, 2),
            "total_packets": fwd_packets + bwd_packets,
            "total_bytes": total_bytes,
            "duration": round(actual_duration, 2),
            "fwd_packets": fwd_packets,
            "bwd_packets": bwd_packets,
            "primary_trigger": primary_trigger,
            "shap_values": shap_contributions,
            "timestamp": time.strftime("%H:%M:%S")
        }
        
        with open("metrics.json", "w") as f:
            json.dump(export_data, f)
            
        print(f" -> STATUS: [{status}] | Packets/s: {flow_packets_per_sec:.2f} (Metrics dumped to JSON)")
        print("-" * 75)
        window_count += 1

if __name__ == "__main__":
    start_live_ids_engine(interface_name='en0', window_duration=10)