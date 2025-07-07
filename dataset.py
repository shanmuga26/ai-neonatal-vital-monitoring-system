import pandas as pd
import numpy as np
import random

# Set seed for reproducibility
np.random.seed(42)

# Number of synthetic rows
n = 45000

# Define conditions with realistic medical ranges
conditions = {
    'Tachycardia': {
        'HeartRate': (150, 180),
        'SPO2': (95, 100),
        'ECG': (700, 850),
        'RespiratoryRate': (16, 20),
        'SleepActivity': [0, 1],
        'Temperature': (36.5, 37.5)
    },
    'Bradycardia': {
        'HeartRate': (60, 90),
        'SPO2': (93, 100),
        'ECG': (100, 300),
        'RespiratoryRate': (16, 20),
        'SleepActivity': [0, 1],
        'Temperature': (36.5, 37.5)
    },
    'Sleep Apnea': {
        'HeartRate': (120, 160),
        'SPO2': (85, 94),
        'ECG': (100, 300),
        'RespiratoryRate': (15, 19),
        'SleepActivity': [1],
        'Temperature': (36.0, 37.0)
    },
    'Hypoxemia': {
        'HeartRate': (110, 150),
        'SPO2': (70, 89),
        'ECG': (600, 850),
        'RespiratoryRate': (16, 22),
        'SleepActivity': [0, 1],
        'Temperature': (36.5, 37.2)
    },
    'Hypothermia': {
        'HeartRate': (100, 140),
        'SPO2': (92, 98),
        'ECG': (500, 700),
        'RespiratoryRate': (16, 18),
        'SleepActivity': [0, 1],
        'Temperature': (34.5, 35.5)
    },
    'Hyperthermia': {
        'HeartRate': (130, 170),
        'SPO2': (90, 98),
        'ECG': (700, 900),
        'RespiratoryRate': (17, 21),
        'SleepActivity': [0, 1],
        'Temperature': (38.0, 39.5)
    },
    'Normal': {
        'HeartRate': (110, 150),
        'SPO2': (95, 100),
        'ECG': (400, 700),
        'RespiratoryRate': (17, 20),
        'SleepActivity': [0, 1],
        'Temperature': (36.5, 37.5)
    }
}

# Class distribution
distribution = {
    'Tachycardia': 0.15,
    'Bradycardia': 0.10,
    'Sleep Apnea': 0.15,
    'Hypoxemia': 0.10,
    'Hypothermia': 0.10,
    'Hyperthermia': 0.10,
    'Normal': 0.30
}

# Generate dataset
data = []
for condition, percent in distribution.items():
    rows = int(n * percent)
    params = conditions[condition]

    for _ in range(rows):
        row = {
            'HeartRate': np.random.randint(*params['HeartRate']),
            'SPO2': np.random.randint(*params['SPO2']),
            'ECG': np.random.randint(*params['ECG']),
            'RespiratoryRate': round(np.random.uniform(*params['RespiratoryRate']), 2),
            'SleepActivity': random.choice(params['SleepActivity']),
            'Temperature': round(np.random.uniform(*params['Temperature']), 2),
            'Label': condition
        }
        data.append(row)

# Convert to DataFrame
df = pd.DataFrame(data)

# Shuffle the data
df = df.sample(frac=1).reset_index(drop=True)

# Save to CSV as 'dataset1.csv'
df.to_csv("dataset1.csv", index=False)

print("Synthetic dataset generated and saved as 'dataset1.csv'.")
