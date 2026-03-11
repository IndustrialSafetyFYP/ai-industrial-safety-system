"""
Industrial Safety System - MQTT Simulator v2.1
Fixed deprecation warning with correct Version 2 API
"""

import paho.mqtt.client as mqtt
import json
import random
import time
from datetime import datetime

# MQTT Configuration
BROKER = "localhost"
PORT = 1883
TOPIC = "sensors/gas"

def simulate_sensor_data(node_id):
    """Generate realistic sensor data for testing"""
    base_mq2 = 250  # Normal air reading
    base_mq7 = 200   # Normal CO reading
    
    # Simulate occasional gas leaks (15% chance)
    if random.random() < 0.15:
        mq2_value = base_mq2 + random.randint(500, 2000)
        mq7_value = base_mq7 + random.randint(400, 1000)
        status = "LEAK_SIMULATED"
        leak_detected = True
    else:
        mq2_value = base_mq2 + random.randint(-30, 30)
        mq7_value = base_mq7 + random.randint(-20, 20)
        status = "NORMAL"
        leak_detected = False
    
    return {
        "timestamp": datetime.now().isoformat(),
        "node_id": node_id,
        "mq2_value": mq2_value,
        "mq7_value": mq7_value,
        "temperature": 25 + random.randint(-3, 3),
        "humidity": 60 + random.randint(-15, 15),
        "status": status,
        "leak_detected": leak_detected
    }

def on_connect(client, userdata, flags, rc, properties=None):
    """Callback for when the client receives CONNACK response from the server"""
    if rc == 0:
        print("✅ Connected to MQTT broker successfully!")
        print(f"📡 Publishing to topic: {TOPIC}")
    else:
        print(f"❌ Connection failed with code {rc}")

def on_publish(client, userdata, mid, reason_code=None, properties=None):
    """Callback when message is published"""
    print(f"✅ Message {mid} published successfully")

def main():
    # Create MQTT client with updated API version 2
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_publish = on_publish
    
    try:
        # Connect to broker
        print("=== Industrial Safety System MQTT Simulator v2.1 ===")
        print("Connecting to MQTT broker...")
        client.connect(BROKER, PORT, 60)
        
        # Start background thread
        client.loop_start()
        
        print("🚀 Simulator started - Press Ctrl+C to stop")
        print("📊 Simulating multiple sensor nodes...")
        print("🔍 Leak simulation: 15% probability")
        print("=" * 50)
        
        counter = 0
        leak_count = 0
        
        while True:
            # Simulate data from multiple nodes
            nodes = ["sensor_node_01", "sensor_node_02", "sensor_node_03"]
            
            for node_id in nodes:
                sensor_data = simulate_sensor_data(node_id)
                
                # Count leaks for statistics
                if sensor_data["leak_detected"]:
                    leak_count += 1
                
                # Publish to MQTT
                result = client.publish(TOPIC, json.dumps(sensor_data))
                
                # Display data with emoji indicators
                status_emoji = "🔥" if sensor_data["leak_detected"] else "✅"
                print(f"{status_emoji} {sensor_data['node_id']} | " +
                      f"MQ2: {sensor_data['mq2_value']:4d} | " +
                      f"MQ7: {sensor_data['mq7_value']:4d} | " +
                      f"Temp: {sensor_data['temperature']:2d}°C")
                
                # Small delay between nodes
                time.sleep(0.5)
            
            counter += 1
            print(f"📦 Batch {counter} | Total leaks: {leak_count} | Waiting 3 seconds...")
            print("-" * 40)
            time.sleep(3)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping simulator...")
        client.loop_stop()
    except Exception as e:
        print(f"❌ Error: {e}")
        client.loop_stop()

if __name__ == "__main__":
    main()
