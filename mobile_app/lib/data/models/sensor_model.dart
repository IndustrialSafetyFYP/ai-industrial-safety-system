class SensorData {
  final String id;
  final String name;
  final double value;
  final String unit;
  final String type;
  final DateTime timestamp;
  final String status;
  final double minValue;
  final double maxValue;
  SensorData({
    required this.id,
    required this.name,
    required this.value,
    required this.unit,
    required this.type,
    required this.timestamp,
    required this.status,
    required this.minValue,
    required this.maxValue,
  });
  double get percentage => ((value - minValue) / (maxValue - minValue)).clamp(0.0, 1.0);
}
