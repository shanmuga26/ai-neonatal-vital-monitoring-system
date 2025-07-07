import os
import urllib.request
import http
import pandas as pd
from time import sleep
from datetime import datetime
import pickle
from twilio.rest import Client
from flask import Flask, render_template, jsonify
import threading
import json

app = Flask(__name__)

# Global variables to store latest readings
latest_data = {
    "bpm": "0",
    "spo2": "0",
    "ecg": "0",
    "respiration": "0",
    "sleep": "0",
    "temperature": "0",
    "prediction": "Normal",
    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "alerts": []
}

# Load the trained model
filename = 'model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

# Twilio credentials
import os
from dotenv import load_dotenv
from twilio.rest import Client

# Load environment variables from the .env file
load_dotenv()

# Get Twilio credentials from the environment
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

# Initialize Twilio client
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

TWILIO_PHONE = '+13194585419'  # Your Twilio number

# List of phone numbers to send alert to
TO_PHONES = ['+919344019590', '+919361356371']  # Doctor, Nurse (add more as needed)
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# ESP32 server base URL
base = "http://192.168.137.165/"

# Function to send/receive data
def transfer(my_url):
    try:
        n = urllib.request.urlopen(base + my_url).read()
        return n.decode("utf-8")
    except http.client.HTTPException as e:
        return str(e)
    except Exception as e:
        print(f"Error connecting to ESP32: {e}")
        return "0,0,0,0,0,0"

# Send Twilio alert to multiple numbers
def send_alert(message):
    for number in TO_PHONES:
        try:
            client.messages.create(
                body=message,
                from_=TWILIO_PHONE,
                to=number
            )
            print(f"Alert sent to {number}")
        except Exception as e:
            print(f"Failed to send alert to {number}: {e}")

# Data collection function - runs in background
def collect_data():
    global latest_data
    ct = 0
    
    # Historical data storage for graphs
    historical_data = {
        "bpm": [],
        "spo2": [],
        "temperature": [],
        "respiration": [],
        "timestamps": []
    }
    
    max_data_points = 60  # Store last 60 readings
    
    while True:
        try:
            res = transfer(str(ct))
            response = str(res)
            
            values = response.split(',')
            if len(values) == 6:
                bpm, spo2, te, mq, fl, rs = values
                
                # Update timestamp
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Store data for historical tracking
                historical_data["bpm"].append(float(bpm) if bpm.replace('.', '', 1).isdigit() else 0)
                historical_data["spo2"].append(float(spo2) if spo2.replace('.', '', 1).isdigit() else 0)
                historical_data["temperature"].append(float(rs) if rs.replace('.', '', 1).isdigit() else 0)
                historical_data["respiration"].append(float(mq) if mq.replace('.', '', 1).isdigit() else 0)
                historical_data["timestamps"].append(current_time)
                
                # Keep only the last max_data_points
                if len(historical_data["timestamps"]) > max_data_points:
                    for key in historical_data:
                        historical_data[key] = historical_data[key][-max_data_points:]
                
                # Run prediction model
                try:
                    reports = [[float(bpm), float(spo2), float(te), float(mq), float(fl), float(rs)]]
                    predicted = loaded_model.predict(reports)
                    result = predicted[0]
                except Exception as e:
                    print(f"Prediction error: {e}")
                    result = "Error"
                
                # Update latest data
                latest_data.update({
                    "bpm": bpm,
                    "spo2": spo2,
                    "ecg": te,
                    "respiration": mq,
                    "sleep": fl,
                    "temperature": rs,
                    "prediction": result,
                    "timestamp": current_time,
                    "historical": historical_data
                })
                
                print(f"bpm: {bpm}, spo2: {spo2}, ECG: {te}, Respiration: {mq}, Sleep: {fl}, Temp: {rs}")
                print(f"Prediction: {result}")
                
                # Handle alerts
                if result != "Normal":
                    alert_msg = (
                        f"⚠️ ALERT: {result} detected!\n"
                        f"HR: {bpm}, SpO2: {spo2}, ECG: {te}, Resp: {mq}, Sleep: {fl}, Temp: {rs}\n"
                        f"Time: {current_time}"
                    )
                    send_alert(alert_msg)
                    
                    # Add to alerts list (max 10 recent alerts)
                    latest_data["alerts"].insert(0, {
                        "message": f"{result} detected",
                        "details": f"HR: {bpm}, SpO2: {spo2}, ECG: {te}, Resp: {mq}, Sleep: {fl}, Temp: {rs}",
                        "timestamp": current_time,
                        "type": result
                    })
                    
                    if len(latest_data["alerts"]) > 10:
                        latest_data["alerts"] = latest_data["alerts"][:10]
                
            ct += 1
        except Exception as e:
            print(f"Error in data collection: {e}")
        
        sleep(1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    return jsonify(latest_data)

if __name__ == '__main__':
    # Start data collection in a separate thread
    data_thread = threading.Thread(target=collect_data)
    data_thread.daemon = True
    data_thread.start()
    
    # Start the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)