# Sensor Testing Protocol

## Safety First!
- ⚠️ Never test with actual gas leaks
- ⚠️ Use safe alternatives for testing
- ⚠️ Work in well-ventilated area
- ⚠️ Have fire extinguisher nearby

## Safe Testing Methods:

### 1. MQ-2 Sensor (LPG/Smoke Detection)
**Safe Test Substances:**
- **Candle smoke:** Light candle, blow it out, wave smoke near sensor (from 1m distance)
- **Deodorant spray:** Brief spray from 2m distance
- **Alcohol swab:** Wave near sensor briefly

**Expected Results:**
- Normal air: 100-300
- With test substance: 500-2000+
- Should return to normal after 30-60 seconds

### 2. MQ-7 Sensor (CO Detection)
**Note:** CO is dangerous - use simulated tests only
**Alternative Tests:**
- **Breath:** Human breath contains CO2 (not same as CO, but detectable)
- **Vehicle exhaust:** From distance (OUTDOORS ONLY, very brief)

**Expected Results:**
- Normal air: 80-200
- With test: 300-800+

## Step-by-Step Testing Procedure:

### Day 1: Basic Functionality
1. Connect ESP32 + MQ-2 sensor only
2. Upload basic reading code
3. Verify serial monitor shows readings
4. Test with safe methods above

### Day 2: Calibration
1. Run calibration function
2. Update baseline values in code
3. Verify ratio calculations work

### Day 3: Multiple Sensors
1. Add MQ-7 sensor
2. Test both sensors simultaneously
3. Verify no interference

### Day 4: Alert System
1. Test LED alert functionality
2. Verify different threshold levels
3. Test automatic reset after danger passes

## Data Recording Template:
