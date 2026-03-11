"""
Industrial Safety System - Real-time Data Visualizer
Displays sensor data in real-time using matplotlib
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sqlite3
from datetime import datetime, timedelta
import time

# Set up the plot
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Industrial Safety System - Real-time Monitoring', fontsize=16)

def update_plots(frame):
    """Update all plots with latest data"""
    try:
        # Get last 30 readings from database
        conn = sqlite3.connect('sensor_data.db')
        c = conn.cursor()
        c.execute('''SELECT timestamp, node_id, mq2_value, mq7_value, temperature, humidity, status 
                     FROM readings ORDER BY timestamp DESC LIMIT 30''')
        data = c.fetchall()
        conn.close()
        
        if not data:
            return
        
        # Reverse to show chronological order
        data.reverse()
        
        # Prepare data
        timestamps = [datetime.fromisoformat(row[0]) for row in data]
        mq2_values = [row[2] for row in data]
        mq7_values = [row[3] for row in data]
        temperatures = [row[4] for row in data]
        humidities = [row[5] for row in data]
        statuses = [row[6] for row in data]
        
        # Clear plots
        ax1.clear()
        ax2.clear()
        ax3.clear()
        ax4.clear()
        
        # Plot 1: MQ-2 Values (LPG/Smoke)
        ax1.plot(timestamps, mq2_values, 'b-', linewidth=2, label='MQ-2 (LPG/Smoke)')
        ax1.set_title('MQ-2 Gas Sensor Readings')
        ax1.set_ylabel('Sensor Value')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Highlight leak conditions
        for i, status in enumerate(statuses):
            if "LEAK" in status:
                ax1.axvline(x=timestamps[i], color='red', alpha=0.5, linestyle='--')
        
        # Plot 2: MQ-7 Values (Carbon Monoxide)
        ax2.plot(timestamps, mq7_values, 'r-', linewidth=2, label='MQ-7 (CO)')
        ax2.set_title('MQ-7 Carbon Monoxide Sensor')
        ax2.set_ylabel('Sensor Value')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Plot 3: Temperature
        ax3.plot(timestamps, temperatures, 'g-', linewidth=2, label='Temperature')
        ax3.set_title('Temperature Monitoring')
        ax3.set_ylabel('°C')
        ax3.set_xlabel('Time')
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        
        # Plot 4: Humidity
        ax4.plot(timestamps, humidities, 'purple', linewidth=2, label='Humidity')
        ax4.set_title('Humidity Levels')
        ax4.set_ylabel('Relative Humidity %')
        ax4.set_xlabel('Time')
        ax4.grid(True, alpha=0.3)
        ax4.legend()
        
        # Adjust layout
        plt.tight_layout()
        
    except Exception as e:
        print(f"Error updating plots: {e}")

def main():
    print("=== Industrial Safety System - Real-time Visualizer ===")
    print("Starting visualization...")
    print("Close the window to stop")
    
    # Create animation that updates every 2 seconds
    ani = animation.FuncAnimation(fig, update_plots, interval=2000, cache_frame_data=False)
    
    plt.show()

if __name__ == "__main__":
    main()
