"""
Generate Synthetic Training Data for AI Model
Creates realistic sensor patterns for normal and leak scenarios
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_normal_pattern(hours=48):
    """Generate normal sensor readings (48 hours of data)"""
    timestamps = []
    mq2_values = []
    mq7_values = []
    temperatures = []
    humidities = []
    labels = []
    
    base_time = datetime.now() - timedelta(hours=hours)
    
    for i in range(hours * 60):  # 1 reading per minute for 48 hours
        current_time = base_time + timedelta(minutes=i)
        
        # Normal patterns with slight variations
        mq2_base = 250 + random.randint(-30, 30)
        mq7_base = 200 + random.randint(-20, 20)
        temp_base = 25 + random.randint(-2, 2)
        humidity_base = 60 + random.randint(-10, 10)
        
        # Add daily patterns (lower at night, higher during day)
        hour = current_time.hour
        if 6 <= hour <= 18:  # Daytime
            mq2_base += random.randint(10, 30)
            mq7_base += random.randint(5, 15)
            temp_base += random.randint(1, 3)
        else:  # Nighttime
            mq2_base -= random.randint(5, 15)
            mq7_base -= random.randint(3, 8)
            temp_base -= random.randint(1, 2)
        
        timestamps.append(current_time)
        mq2_values.append(mq2_base)
        mq7_values.append(mq7_base)
        temperatures.append(temp_base)
        humidities.append(humidity_base)
        labels.append(0)  # 0 = normal
    
    return pd.DataFrame({
        'timestamp': timestamps,
        'mq2_value': mq2_values,
        'mq7_value': mq7_values,
        'temperature': temperatures,
        'humidity': humidities,
        'label': labels
    })

def generate_leak_pattern(leak_duration_minutes=30):
    """Generate sensor readings during a gas leak"""
    timestamps = []
    mq2_values = []
    mq7_values = []
    temperatures = []
    humidities = []
    labels = []
    
    base_time = datetime.now()
    
    # Pre-leak period (10 minutes of normal)
    for i in range(10):
        current_time = base_time + timedelta(minutes=i)
        timestamps.append(current_time)
        mq2_values.append(250 + random.randint(-20, 20))
        mq7_values.append(200 + random.randint(-15, 15))
        temperatures.append(25 + random.randint(-1, 1))
        humidities.append(60 + random.randint(-5, 5))
        labels.append(0)  # Normal
    
    # Leak period (30 minutes)
    for i in range(10, 40):
        current_time = base_time + timedelta(minutes=i)
        progress = (i - 10) / 30  # 0 to 1 during leak
        
        # Simulate leak buildup
        leak_intensity = progress * 1500  # Gradual increase
        
        timestamps.append(current_time)
        mq2_values.append(250 + int(leak_intensity) + random.randint(-100, 100))
        mq7_values.append(200 + int(leak_intensity * 0.7) + random.randint(-50, 50))
        temperatures.append(25 + random.randint(-2, 2))
        humidities.append(60 + random.randint(-10, 10))
        labels.append(1)  # 1 = leak
    
    # Post-leak (10 minutes of recovery)
    for i in range(40, 50):
        current_time = base_time + timedelta(minutes=i)
        recovery = (i - 40) / 10  # 0 to 1 during recovery
        
        timestamps.append(current_time)
        mq2_values.append(250 + int(800 * (1 - recovery)) + random.randint(-50, 50))
        mq7_values.append(200 + int(600 * (1 - recovery)) + random.randint(-30, 30))
        temperatures.append(25 + random.randint(-1, 1))
        humidities.append(60 + random.randint(-5, 5))
        labels.append(1)  # Still in leak status
    
    return pd.DataFrame({
        'timestamp': timestamps,
        'mq2_value': mq2_values,
        'mq7_value': mq7_value,
        'temperature': temperatures,
        'humidity': humidities,
        'label': labels
    })

def create_training_dataset():
    """Create complete training dataset"""
    print("Generating training data...")
    
    # Generate normal data (48 hours)
    normal_data = generate_normal_pattern(48)
    
    # Generate multiple leak scenarios
    leak_scenarios = []
    for _ in range(20):  # 20 different leak events
        leak_data = generate_leak_pattern()
        leak_scenarios.append(leak_data)
    
    # Combine all data
    all_data = pd.concat([normal_data] + leak_scenarios, ignore_index=True)
    
    # Shuffle the data
    all_data = all_data.sample(frac=1).reset_index(drop=True)
    
    # Save to CSV
    all_data.to_csv('training_data.csv', index=False)
    
    # Statistics
    normal_count = len(all_data[all_data['label'] == 0])
    leak_count = len(all_data[all_data['label'] == 1])
    
    print(f"✅ Training data generated!")
    print(f"📊 Dataset size: {len(all_data)} records")
    print(f"✅ Normal readings: {normal_count}")
    print(f"🔥 Leak readings: {leak_count}")
    print(f"📁 Saved as: training_data.csv")
    
    return all_data

if __name__ == "__main__":
    dataset = create_training_dataset()
