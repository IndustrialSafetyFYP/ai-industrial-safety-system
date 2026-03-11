"""
Industrial Safety System - Data Receiver v2.1
Fixed deprecation warning with correct Version 2 API
"""

import paho.mqtt.client as mqtt
import json
import sqlite3
from datetime import datetime

# Database setup
def setup_database():
    conn = sqlite3.connect('sensor_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS readings
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  node_id TEXT,
                  mq2_value INTEGER,
                  mq7_value INTEGER,
                  temperature REAL,
                  humidity REAL,
                  status TEXT,
                  leak_detected INTEGER)''')  # 0=False, 1=True
    conn.commit()
    conn.close()
    print("✅ Database setup complete")

def get_database_stats():
    """Get current statistics from database"""
    conn = sqlite3.connect('sensor_data.db')
    c = conn.cursor()
    
    # Get total records and leak count
    c.execute("SELECT COUNT(*) FROM readings")
    total_records = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM readings WHERE leak_detected = 1")
    leak_records = c.fetchone()[0]
    
    conn.close()
    return total_records, leak_records

def on_connect(client, userdata, flags, rc, properties=None):
    """Callback when connected to MQTT broker"""
    if rc == 0:
        print("✅ Data Receiver Connected to MQTT Broker")
        client.subscribe("sensors/gas")
        print("📡 Subscribed to topic: sensors/gas")
        
        # Show database stats
        total, leaks = get_database_stats()
        print(f"💾 Database: {total} total records, {leaks} leak events")
    else:
        print(f"❌ Connection failed with code {rc}")

def on_message(client, userdata, msg):
    """Callback when message is received"""
    try:
        data = json.loads(msg.payload.decode())
        
        # Validate data
        required_fields = ['node_id', 'mq2_value', 'mq7_value', 'status']
        if not all(field in data for field in required_fields):
            print("❌ Invalid data received")
            return
        
        # Display received data with emoji
        status_emoji = "🔥" if data.get('leak_detected', False) else "📊"
        print(f"{status_emoji} {data['node_id']} | " +
              f"MQ2: {data['mq2_value']:4d} | " +
              f"MQ7: {data['mq7_value']:4d} | " +
              f"Status: {data['status']}")
        
        # Store in database
        conn = sqlite3.connect('sensor_data.db')
        c = conn.cursor()
        c.execute('''INSERT INTO readings 
                    (timestamp, node_id, mq2_value, mq7_value, temperature, humidity, status, leak_detected)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                 (data['timestamp'], data['node_id'], data['mq2_value'], 
                  data['mq7_value'], data['temperature'], data['humidity'], 
                  data['status'], 1 if data.get('leak_detected', False) else 0))
        conn.commit()
        conn.close()
        
        # Show updated stats every 10 messages
        total, leaks = get_database_stats()
        if total % 10 == 0:
            print(f"💾 Database updated: {total} records, {leaks} leaks")
        
    except Exception as e:
        print(f"❌ Error processing message: {e}")

def main():
    # Setup database
    setup_database()
    
    # Create MQTT client with updated API version 2
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        # Connect to broker
        print("=== Industrial Safety System - Data Receiver v2.1 ===")
        print("Connecting to MQTT broker...")
        client.connect("localhost", 1883, 60)
        
        print("🎯 Receiver started - Waiting for sensor data...")
        print("Press Ctrl+C to stop")
        print("=" * 50)
        
        # Loop forever
        client.loop_forever()
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping receiver...")
        
        # Final stats
        total, leaks = get_database_stats()
        print(f"📊 Final Stats: {total} total records, {leaks} leak events")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
