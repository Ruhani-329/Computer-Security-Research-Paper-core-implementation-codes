from flask import Flask, jsonify, render_template
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/metrics')
def get_metrics():
    if os.path.exists('metrics.json'):
        try:
            with open('metrics.json', 'r') as f:
                data = json.load(f)
                return jsonify(data)
        except:
            return jsonify({"error": "Read conflict"}), 500
    return jsonify({"status": "WAITING", "packets_per_sec": 0, "bytes_per_sec": 0, "shap_values": {}})

if __name__ == '__main__':
    app.run(debug=True, port=5001)