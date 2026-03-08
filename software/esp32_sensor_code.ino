/*
 * Industrial Safety System - ESP32 Gas Sensor Code
 * Developer: Sulman Ahmad Cheema
 * Date: [Today's Date]
 * Description: Reads MQ-2 gas sensor and sends data via Serial
 */

// Sensor pin definitions
const int MQ2_PIN = 34;    // Analog pin for MQ-2
const int MQ7_PIN = 35;     // Analog pin for MQ-7
const int LED_PIN = 2;      // Built-in LED

// Sensor calibration values (adjust during testing)
float MQ2_BASELINE = 250.0;  // Normal air reading
float MQ7_BASELINE = 200.0;   // Normal air reading

// Variables for sensor readings
int mq2_value = 0;
int mq7_value = 0;
float mq2_ratio = 0.0;
float mq7_ratio = 0.0;

void setup() {
  // Initialize serial communication
  Serial.begin(115200);
  
  // Configure pins
  pinMode(MQ2_PIN, INPUT);
  pinMode(MQ7_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  
  // Welcome message
  Serial.println("=== Industrial Safety System ESP32 ===");
  Serial.println("Gas Sensor Monitoring Started");
  Serial.println("MQ-2 Pin: GPIO34, MQ-7 Pin: GPIO35");
  Serial.println("Waiting 60 seconds for sensor warm-up...");
  
  // Sensor warm-up period
  digitalWrite(LED_PIN, HIGH);  // LED on during warm-up
  delay(60000);                  // 60 seconds warm-up
  digitalWrite(LED_PIN, LOW);    // LED off after warm-up
  
  Serial.println("Sensor warm-up complete. Starting monitoring...");
  Serial.println("Time\tMQ2_Value\tMQ7_Value\tMQ2_Ratio\tMQ7_Ratio\tStatus");
}

void loop() {
  // Read sensor values
  mq2_value = analogRead(MQ2_PIN);
  mq7_value = analogRead(MQ7_PIN);
  
  // Calculate ratio (current reading / baseline)
  mq2_ratio = (float)mq2_value / MQ2_BASELINE;
  mq7_ratio = (float)mq7_value / MQ7_BASELINE;
  
  // Determine status
  String status = "NORMAL";
  if (mq2_ratio > 2.0 || mq7_ratio > 2.0) {
    status = "WARNING";
    digitalWrite(LED_PIN, HIGH);  // Alert LED
  } else if (mq2_ratio > 5.0 || mq7_ratio > 5.0) {
    status = "DANGER";
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);   // Normal LED
  }
  
  // Print data to serial monitor
  Serial.print(millis());
  Serial.print("\t");
  Serial.print(mq2_value);
  Serial.print("\t\t");
  Serial.print(mq7_value);
  Serial.print("\t\t");
  Serial.print(mq2_ratio, 2);
  Serial.print("\t\t");
  Serial.print(mq7_ratio, 2);
  Serial.print("\t\t");
  Serial.println(status);
  
  // Wait 2 seconds between readings
  delay(2000);
}

// Function to calibrate baseline (run once manually)
void calibrateSensors() {
  Serial.println("=== Sensor Calibration ===");
  Serial.println("Ensure clean air environment. Calibrating in 10 seconds...");
  delay(10000);
  
  int samples = 10;
  long mq2_sum = 0;
  long mq7_sum = 0;
  
  for (int i = 0; i < samples; i++) {
    mq2_sum += analogRead(MQ2_PIN);
    mq7_sum += analogRead(MQ7_PIN);
    delay(1000);
  }
  
  MQ2_BASELINE = (float)mq2_sum / samples;
  MQ7_BASELINE = (float)mq7_sum / samples;
  
  Serial.println("Calibration Complete:");
  Serial.print("MQ2 Baseline: "); Serial.println(MQ2_BASELINE);
  Serial.print("MQ7 Baseline: "); Serial.println(MQ7_BASELINE);
  Serial.println("Update these values in the code.");
}
