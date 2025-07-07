# 🩺 AI-Powered Neonatal Vitals Monitoring System

A real-time neonatal vitals monitoring and alerting system powered by **ESP32**, **ECG and vital sensors**, and a **K-Nearest Neighbors (KNN) machine learning model**.  
The system continuously monitors vital signs, analyzes risk using AI, and sends **alerts to mobile devices via Twilio** when abnormalities are detected.  
A **web dashboard** displays real-time vitals trends through dynamic graphs.

---

## 🚀 Key Features

- 📊 Real-time vitals collection using:
  - **MAX30102**: Heart rate & SpO2
  - **DS18B20**: Body temperature
  - **AD8232 ECG Module**: Heart rhythm detection
  - **MPU6050**: Motion/position monitoring
- 📡 ESP32 sends data to a Flask server over Wi-Fi
- 🧠 **KNN AI model** predicts distress conditions
- 📈 Web dashboard shows real-time vitals & risk score graphs
- 🔔 Sends SMS alerts via **Twilio** when risk is detected
- 🕸️ REST API endpoints for easy data access
- Secure environment variable management (`.env`)

---

## 🛠️ Tech Stack

| Component         | Technology                |
|------------------|----------------------------|
| Microcontroller  | ESP32                      |
| Backend          | Python (Flask)             |
| Machine Learning | scikit-learn (KNN)         |
| Frontend         | HTML, Chart.js (Graphs)    |
| Communication    | HTTP (ESP32 ↔ Flask)      |
| Alerts           | Twilio SMS API             |
| Environment Mgmt | python-dotenv, .env        |

---

## 🧰 Hardware Components

- ESP32 Development Board
- MAX30102 Pulse Oximeter
- DS18B20 Temperature Sensor
- AD8232 ECG Sensor Module
- MPU6050 Accelerometer & Gyroscope
- Micro-USB Cable, Breadboard, Jumper Wires

---

## 📁 Project Structure
ai-neonatal-vital-monitoring-system/
├── app.py               # Flask server with API & ML logic
├── model_knn.pkl        # Trained KNN model
├── ecg_data/            # ECG data samples (optional)
├── templates/           # HTML templates for dashboard
├── static/              # CSS, JS (Chart.js)
├── esp32_code.ino       # ESP32 script to send vitals
├── .env                 # Secrets (Twilio)
├── .gitignore           # Ignores env and pycache
└── README.md            # This documentation


