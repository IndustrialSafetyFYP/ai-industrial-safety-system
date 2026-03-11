# World-Class Industrial Safety App Structure Creator
# Run this script in PowerShell as Administrator

# Set the project root directory
$ProjectRoot = "C:\Users\asus\ai-industrial-safety-system\mobile_app"

# Create main directories
$Directories = @(
    # Main structure
    "lib",
    "assets\images\icons",
    "assets\images\illustrations", 
    "assets\images\backgrounds",
    "assets\animations\lottie",
    "assets\animations\rive",
    "assets\fonts\poppins",
    "assets\fonts\inter",
    "test\unit",
    "test\widget",
    "test\integration",
    
    # App configuration
    "lib\app\config",
    "lib\app\localization",
    "lib\app\di",
    
    # Core architecture
    "lib\core\base",
    "lib\core\error",
    "lib\core\network",
    "lib\core\utils",
    
    # Data layer
    "lib\data\models\sensor",
    "lib\data\models\user", 
    "lib\data\models\system",
    "lib\data\repositories",
    "lib\data\datasources\local",
    "lib\data\datasources\remote",
    "lib\data\mappers",
    
    # Domain layer
    "lib\domain\entities",
    "lib\domain\repositories",
    "lib\domain\usecases\sensor_usecases",
    "lib\domain\usecases\user_usecases",
    "lib\domain\usecases\system_usecases",
    
    # Presentation layer
    "lib\presentation\providers",
    "lib\presentation\screens\dashboard\widgets\realtime_charts",
    "lib\presentation\screens\dashboard\widgets\sensor_grid",
    "lib\presentation\screens\dashboard\widgets\alert_panel",
    "lib\presentation\screens\dashboard\widgets\quick_actions",
    "lib\presentation\screens\history\widgets\timeline_charts",
    "lib\presentation\screens\history\widgets\export_panel",
    "lib\presentation\screens\history\widgets\filter_widgets",
    "lib\presentation\screens\alerts\widgets\alert_list",
    "lib\presentation\screens\alerts\widgets\alert_details",
    "lib\presentation\screens\alerts\widgets\notification_settings",
    "lib\presentation\screens\settings\widgets\profile_section",
    "lib\presentation\screens\settings\widgets\theme_selector",
    "lib\presentation\screens\settings\widgets\notification_settings",
    "lib\presentation\screens\settings\widgets\about_section",
    "lib\presentation\screens\auth\widgets\login_form",
    "lib\presentation\screens\auth\widgets\biometric_auth",
    "lib\presentation\widgets\common",
    "lib\presentation\widgets\charts",
    "lib\presentation\widgets\cards",
    "lib\presentation\widgets\inputs",
    "lib\presentation\theme",
    
    # Services
    "lib\services"
)

# Create all directories
Write-Host "Creating directory structure..." -ForegroundColor Green
foreach ($dir in $Directories) {
    $fullPath = Join-Path $ProjectRoot $dir
    if (!(Test-Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath -Force
        Write-Host "Created: $dir" -ForegroundColor Yellow
    }
}

# Create essential files with basic content
Write-Host "`nCreating essential files..." -ForegroundColor Green

# 1. pubspec.yaml (Comprehensive version)
$PubspecContent = @"
name: industrial_safety
description: World-Class Industrial Safety Monitoring App
publish_to: 'none'

version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
    
  # State Management
  flutter_bloc: ^8.1.3
  provider: ^6.1.1
  
  # UI & Animations
  lottie: ^2.5.0
  fl_chart: ^0.66.0
  
  # Networking
  dio: ^5.3.0
  web_socket_channel: ^3.0.0
  
  # Storage
  shared_preferences: ^2.2.2
  
  # Utilities
  get_it: ^7.6.0
  intl: ^0.18.1

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0

flutter:
  uses-material-design: true
  
  assets:
    - assets/images/
    - assets/animations/
    - assets/fonts/

  fonts:
    - family: Poppins
      fonts:
        - asset: assets/fonts/poppins/Poppins-Regular.ttf
        - asset: assets/fonts/poppins/Poppins-Bold.ttf
    - family: Inter
      fonts:
        - asset: assets/fonts/inter/Inter-Regular.ttf
"@

Set-Content -Path "$ProjectRoot\pubspec.yaml" -Value $PubspecContent

# 2. Main App File
$MainDartContent = @"
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'app/di/service_locator.dart';
import 'presentation/providers/theme_provider.dart';
import 'presentation/screens/dashboard/dashboard_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await setupServiceLocator();
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => ThemeProvider(),
      child: Consumer<ThemeProvider>(
        builder: (context, themeProvider, child) {
          return MaterialApp(
            title: 'Industrial Safety Monitor',
            theme: themeProvider.currentTheme,
            darkTheme: themeProvider.darkTheme,
            themeMode: themeProvider.themeMode,
            home: DashboardScreen(),
            debugShowCheckedModeBanner: false,
          );
        },
      ),
    );
  }
}
"@

Set-Content -Path "$ProjectRoot\lib\main.dart" -Value $MainDartContent

# 3. Service Locator
$ServiceLocatorContent = @"
import 'package:get_it/get_it.dart';
import 'package:shared_preferences/shared_preferences.dart';

final GetIt serviceLocator = GetIt.instance;

Future<void> setupServiceLocator() async {
  // Shared Preferences
  final sharedPreferences = await SharedPreferences.getInstance();
  serviceLocator.registerSingleton<SharedPreferences>(sharedPreferences);
  
  // Register other services here as we build them
}
"@

Set-Content -Path "$ProjectRoot\lib\app\di\service_locator.dart" -Value $ServiceLocatorContent

# 4. Theme Configuration
$ThemeConfigContent = @"
import 'package:flutter/material.dart';

class AppColors {
  // Primary Colors
  static const Color primary = Color(0xFF0066FF);
  static const Color primaryDark = Color(0xFF0047CC);
  static const Color primaryLight = Color(0xFF66A3FF);
  
  // Semantic Colors
  static const Color success = Color(0xFF00C853);
  static const Color warning = Color(0xFFFFAB00);
  static const Color error = Color(0xFFD32F2F);
  static const Color info = Color(0xFF2979FF);
  
  // Neutral Colors
  static const Color background = Color(0xFFFAFBFF);
  static const Color surface = Color(0xFFFFFFFF);
  static const Color onSurface = Color(0xFF1A1A1A);
  static const Color onBackground = Color(0xFF2D2D2D);
  
  // Gradient Colors
  static const Gradient primaryGradient = LinearGradient(
    colors: [Color(0xFF0066FF), Color(0xFF0052D4)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );
}

class TextStyles {
  static const TextStyle headline1 = TextStyle(
    fontSize: 32,
    fontWeight: FontWeight.bold,
    color: AppColors.onSurface,
  );
  
  static const TextStyle headline2 = TextStyle(
    fontSize: 24,
    fontWeight: FontWeight.w600,
    color: AppColors.onSurface,
  );
  
  static const TextStyle bodyLarge = TextStyle(
    fontSize: 16,
    fontWeight: FontWeight.normal,
    color: AppColors.onBackground,
  );
  
  static const TextStyle bodyMedium = TextStyle(
    fontSize: 14,
    fontWeight: FontWeight.normal,
    color: AppColors.onBackground,
  );
}

class AppThemes {
  static ThemeData get lightTheme {
    return ThemeData(
      primaryColor: AppColors.primary,
      scaffoldBackgroundColor: AppColors.background,
      appBarTheme: AppBarTheme(
        backgroundColor: AppColors.surface,
        elevation: 0,
        titleTextStyle: TextStyles.headline2,
      ),
      cardTheme: CardTheme(
        elevation: 2,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      ),
    );
  }
  
  static ThemeData get darkTheme {
    return ThemeData(
      primaryColor: AppColors.primaryLight,
      scaffoldBackgroundColor: Color(0xFF121212),
      appBarTheme: AppBarTheme(
        backgroundColor: Color(0xFF1E1E1E),
        elevation: 0,
      ),
      cardTheme: CardTheme(
        elevation: 2,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      ),
    );
  }
}
"@

Set-Content -Path "$ProjectRoot\lib\app\config\theme_config.dart" -Value $ThemeConfigContent

# 5. Base ViewModel
$BaseViewModelContent = @"
import 'package:flutter/foundation.dart';

abstract class BaseViewModel with ChangeNotifier {
  bool _isLoading = false;
  String _error = '';

  bool get isLoading => _isLoading;
  String get error => _error;
  
  void setLoading(bool loading) {
    _isLoading = loading;
    notifyListeners();
  }
  
  void setError(String error) {
    _error = error;
    notifyListeners();
  }
  
  void clearError() {
    _error = '';
    notifyListeners();
  }
}
"@

Set-Content -Path "$ProjectRoot\lib\core\base\base_viewmodel.dart" -Value $BaseViewModelContent

# 6. Dashboard Screen (Basic)
$DashboardContent = @"
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../app/config/theme_config.dart';
import '../widgets/common/custom_app_bar.dart';
import '../widgets/cards/sensor_card.dart';

class DashboardScreen extends StatefulWidget {
  @override
  _DashboardScreenState createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomAppBar(
        title: 'Industrial Safety Monitor',
        actions: [
          IconButton(
            icon: Icon(Icons.notifications),
            onPressed: () {},
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // System Status Card
            Card(
              elevation: 4,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(16),
              ),
              child: Padding(
                padding: EdgeInsets.all(16),
                child: Column(
                  children: [
                    Row(
                      children: [
                        Icon(Icons.security, color: AppColors.success),
                        SizedBox(width: 8),
                        Text(
                          'System Status: Optimal',
                          style: TextStyles.headline2,
                        ),
                      ],
                    ),
                    SizedBox(height: 8),
                    LinearProgressIndicator(
                      value: 0.7,
                      backgroundColor: Colors.grey[200],
                      valueColor: AlwaysStoppedAnimation<Color>(AppColors.success),
                    ),
                  ],
                ),
              ),
            ),
            SizedBox(height: 20),
            
            // Sensor Grid
            GridView.count(
              crossAxisCount: 2,
              shrinkWrap: true,
              physics: NeverScrollableScrollPhysics(),
              mainAxisSpacing: 12,
              crossAxisSpacing: 12,
              children: [
                SensorCard(
                  title: 'MQ-2 Gas Sensor',
                  value: 245,
                  unit: 'ppm',
                  icon: Icons.air,
                  color: AppColors.primary,
                ),
                SensorCard(
                  title: 'MQ-7 CO Sensor', 
                  value: 198,
                  unit: 'ppm',
                  icon: Icons.co2,
                  color: AppColors.warning,
                ),
                SensorCard(
                  title: 'Temperature',
                  value: 25.6,
                  unit: '°C',
                  icon: Icons.thermostat,
                  color: AppColors.info,
                ),
                SensorCard(
                  title: 'Humidity',
                  value: 62.3,
                  unit: '%',
                  icon: Icons.water_drop,
                  color: AppColors.info,
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
"@

Set-Content -Path "$ProjectRoot\lib\presentation\screens\dashboard\dashboard_screen.dart" -Value $DashboardContent

# 7. Custom App Bar
$AppBarContent = @"
import 'package:flutter/material.dart';
import '../../app/config/theme_config.dart';

class CustomAppBar extends StatelessWidget implements PreferredSizeWidget {
  final String title;
  final List<Widget>? actions;
  final bool showBackButton;

  const CustomAppBar({
    required this.title,
    this.actions,
    this.showBackButton = false,
  });

  @override
  Size get preferredSize => Size.fromHeight(kToolbarHeight);

  @override
  Widget build(BuildContext context) {
    return AppBar(
      title: Text(
        title,
        style: TextStyles.headline2,
      ),
      actions: actions,
      backgroundColor: AppColors.surface,
      elevation: 0,
      foregroundColor: AppColors.onSurface,
      leading: showBackButton 
          ? IconButton(
              icon: Icon(Icons.arrow_back),
              onPressed: () => Navigator.of(context).pop(),
            )
          : null,
    );
  }
}
"@

Set-Content -Path "$ProjectRoot\lib\presentation\widgets\common\custom_app_bar.dart" -Value $AppBarContent

# 8. Sensor Card Widget
$SensorCardContent = @"
import 'package:flutter/material.dart';
import '../../app/config/theme_config.dart';

class SensorCard extends StatelessWidget {
  final String title;
  final double value;
  final String unit;
  final IconData icon;
  final Color color;

  const SensorCard({
    required this.title,
    required this.value,
    required this.unit,
    required this.icon,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
      ),
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, color: color, size: 24),
                SizedBox(width: 8),
                Text(
                  title,
                  style: TextStyles.bodyMedium.copyWith(
                    color: Colors.grey[600],
                  ),
                ),
              ],
            ),
            SizedBox(height: 12),
            Text(
              value.toStringAsFixed(1),
              style: TextStyle(
                fontSize: 28,
                fontWeight: FontWeight.bold,
                color: color,
              ),
            ),
            Text(
              unit,
              style: TextStyles.bodyMedium.copyWith(
                color: Colors.grey[500],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
"@

Set-Content -Path "$ProjectRoot\lib\presentation\widgets\cards\sensor_card.dart" -Value $SensorCardContent

# 9. Theme Provider
$ThemeProviderContent = @"
import 'package:flutter/material.dart';
import '../app/config/theme_config.dart';

class ThemeProvider with ChangeNotifier {
  ThemeMode _themeMode = ThemeMode.light;

  ThemeMode get themeMode => _themeMode;
  ThemeData get currentTheme => AppThemes.lightTheme;
  ThemeData get darkTheme => AppThemes.darkTheme;

  void toggleTheme(bool isDark) {
    _themeMode = isDark ? ThemeMode.dark : ThemeMode.light;
    notifyListeners();
  }
}
"@

Set-Content -Path "$ProjectRoot\lib\presentation\providers\theme_provider.dart" -Value $ThemeProviderContent

Write-Host "`n✅ World-Class App Structure Created Successfully!" -ForegroundColor Green
Write-Host "📍 Project Location: $ProjectRoot" -ForegroundColor Cyan
Write-Host "📱 Next: Run 'flutter pub get' to install dependencies" -ForegroundColor Yellow
