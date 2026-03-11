import 'package:flutter/material.dart';
import '../../data/models/sensor_model.dart';
import '../widgets/sensor_card.dart';
class DashboardScreen extends StatefulWidget {
  const DashboardScreen({Key? key}) : super(key: key);
  @override
  _DashboardScreenState createState() => _DashboardScreenState();
}
class _DashboardScreenState extends State<DashboardScreen> {
  List<SensorData> sensors = [
    SensorData(
      id: "1",
      name: "MQ-2 Gas Sensor",
      value: 245.0,
      unit: "ppm",
      type: "gas",
      timestamp: DateTime.now(),
      status: "normal",
      minValue: 0,
      maxValue: 1000,
    ),
  ];
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Industrial Safety Monitor"),
        backgroundColor: Colors.blue,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            const Text(
              "Sensor Network",
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 10),
            Expanded(
              child: GridView.builder(
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2,
                  crossAxisSpacing: 12,
                  mainAxisSpacing: 12,
                ),
                itemCount: sensors.length,
                itemBuilder: (context, index) {
                  return SensorCard(sensor: sensors[index]);
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
