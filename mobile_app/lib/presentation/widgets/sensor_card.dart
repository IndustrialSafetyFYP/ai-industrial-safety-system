import 'package:flutter/material.dart';
import '../../data/models/sensor_model.dart';

class SensorCard extends StatelessWidget {
  final SensorData sensor;
  final VoidCallback? onTap;

  const SensorCard({
    Key? key,
    required this.sensor,
    this.onTap,
  }) : super(key: key);

  Color _getStatusColor() {
    switch (sensor.status) {
      case "critical":
        return Colors.red;
      case "warning":
        return Colors.orange;
      default:
        return Colors.green;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Add status indicator using the method
            Container(
              width: 12,
              height: 12,
              decoration: BoxDecoration(
                color: _getStatusColor(), // Now it's used!
                shape: BoxShape.circle,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              sensor.name,
              style: const TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w600,
              ),
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                Text(
                  sensor.value.toStringAsFixed(1),
                  style: TextStyle(
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                    color: _getStatusColor(), // Use it again for value color
                  ),
                ),
                const SizedBox(width: 4),
                Text(
                  sensor.unit,
                  style: const TextStyle(
                    fontSize: 14,
                    color: Colors.grey,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
