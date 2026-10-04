---
name: flutter-screenshots
description: Automate App Store & Google Play screenshot generation for Flutter apps. Scans routing and screens, scores high-value marketing screens, generates self-contained mock harness, runs native simulator captures (iPhone 6.9", iPad 13", Android Phone/Tablet), strips alpha channels, and validates exact store resolutions.
mcp: codebase-memory-mcp
---

# /supergraph:flutter-screenshots

Automated, store-compliant screenshot generator for Flutter apps. Guarantees native pixel accuracy, multi-device responsive fidelity, zero manual cropping, and zero UI distortion.

Announce: "📸 /supergraph:flutter-screenshots — preparing store screenshot pipeline..."

## Overview & Store Requirements Matrix

Apple App Store and Google Play Console enforce strict resolution and format rules:

| Target Device | Target Store | Exact Resolution | Ratio | Format & Rules |
|---|---|---|---|---|
| **iPhone 6.9" / 6.7"** | App Store (Required) | `1320 x 2868` (16 Pro Max) or `1290 x 2796` (15 Pro Max) | ~19.5:9 | 72 dpi, RGB, **NO alpha channel**, PNG/JPEG |
| **iPad Pro 13" / 12.9"** | App Store (If iPad enabled) | `2064 x 2752` (M4 13") or `2048 x 2732` (12.9") | 4:3 | 72 dpi, RGB, **NO alpha channel**, PNG/JPEG |
| **Android Phone** | Google Play (Required) | `1080 x 2400` (min side 1080px) | 16:9 to 9:20 | Max 8MB, 24-bit RGB PNG or JPEG |
| **Android Tablet (10")** | Google Play (If Tablet enabled) | `1600 x 2560` or `1200 x 1920` | 16:10 | Max 8MB, RGB PNG or JPEG |

> ⚠️ **CRITICAL APPLE STORE POLICY**: Apple App Store Connect automatically rejects any image containing an alpha (transparency) channel with the error: `Screenshots cannot contain alpha channels`. This skill strictly strips alpha channels via macOS `sips` before delivery.

---

## When to Use

- When preparing release assets for Apple App Store or Google Play Store.
- When finishing major UI redesigns or features and needing fresh marketing visuals.
- When needing authentic native screenshots without opening multiple simulators simultaneously.

---

## Step 1: Codebase Reconnaissance & Screen Selection

Scan the Flutter project to discover routes, screens, state management, and authentication barriers.

### 1a. Detect routing & screen catalog
```bash
# 1. Detect Router type & declared routes
rg -l "GoRoute|AutoRoute|GetPage|MaterialPageRoute|onGenerateRoute|routes:" lib/

# 2. List all screen/page files in the project
find lib -type f \( -name "*_screen.dart" -o -name "*_page.dart" -o -name "*_view.dart" \) | grep -v "/widgets/" | grep -v "/components/"
```

### 1b. Heuristic Screen Scoring (Marketing Selection)
Analyze discovered screens and rank the top **4 to 5 highest-value marketing screens**:

- **REJECT / SKIP (Low marketing value or gated)**:
  - Authentication: `LoginScreen`, `RegisterScreen`, `OtpVerifyScreen`, `ForgotPasswordScreen`
  - Utility/Legal: `SplashScreen`, `TermsScreen`, `PrivacyPolicyScreen`, `WebviewScreen`, `ErrorScreen`
  - Secondary Forms: `ChangePasswordScreen`, `EditProfileScreen`, `NotificationSettings`

- **SCORE HIGH (Store conversion drivers)**:
  1. **Hero / Dashboard / Home**: Main app hub showing rich content overview.
  2. **Core Value Proposition**: The primary feature (e.g. `AudioPlayerScreen`, `MapTrackingScreen`, `EditorScreen`, `BookingScreen`, `CheckoutScreen`).
  3. **Browse / Feed / Catalog**: Shows breadth of content (e.g. `ExploreScreen`, `ProductListScreen`, `FeedView`).
  4. **Analytics / Detail / Stats**: Visually complex charts or rich detail (e.g. `ReportScreen`, `StatsView`, `UserProfileScreen`).

### 1c. Detect State Management & DI Setup
```bash
# Check how DI, services, and state are wired
rg "GetIt|Provider|BlocProvider|Riverpod|GetX|HydratedBloc|Supabase|Firebase" lib/ pubspec.yaml | head -20
```

---

## Step 2: Generate Mock Test Harness

Do not run raw `main()` directly if it requires live backend auth, network tokens, or Firebase initialization.
Generate a self-contained test runner at `integration_test/store_screenshots_test.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

void main() {
  final binding = IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Store Marketing Screenshots', () {
    testWidgets('Capture Top 4 Screens', (WidgetTester tester) async {
      // 1. Setup mock bindings / providers if needed
      // 2. Screen 1: Dashboard / Home
      // Mount widget with mock data
      await tester.pumpWidget(const MaterialApp(home: MockDashboardScreen()));
      await tester.pumpAndSettle();
      await binding.takeScreenshot('01_dashboard');

      // 3. Screen 2: Primary Feature
      await tester.pumpWidget(const MaterialApp(home: MockPrimaryFeatureScreen()));
      await tester.pumpAndSettle();
      await binding.takeScreenshot('02_feature_primary');

      // 4. Screen 3: Explore / Catalog
      await tester.pumpWidget(const MaterialApp(home: MockCatalogScreen()));
      await tester.pumpAndSettle();
      await binding.takeScreenshot('03_catalog');

      // 5. Screen 4: Analytics / Detail
      await tester.pumpWidget(const MaterialApp(home: MockAnalyticsScreen()));
      await tester.pumpAndSettle();
      await binding.takeScreenshot('04_analytics');
    });
  });
}
```

---

## Step 3: Sequential Native Device Execution

Run simulators sequentially. **Never boot iPhone and iPad at the same time** (saves 6-8GB RAM and prevents system thermal throttling).

### 3a. Automated Test Execution on iOS Simulators
```bash
# Locate available Store-compliant simulators
IPHONE_UDID=$(xcrun simctl list devices available | grep -E "iPhone 16 Pro Max|iPhone 15 Pro Max|iPhone 14 Pro Max" | head -1 | grep -oE '[0-9A-F-]{36}')
IPAD_UDID=$(xcrun simctl list devices available | grep -E "iPad Pro 13-inch|iPad Pro \(12.9-inch\)" | head -1 | grep -oE '[0-9A-F-]{36}')

# 1. iPhone 6.9" capture
if [ -n "$IPHONE_UDID" ]; then
  xcrun simctl boot "$IPHONE_UDID" || true
  flutter test integration_test/store_screenshots_test.dart -d "$IPHONE_UDID"
  xcrun simctl shutdown "$IPHONE_UDID"
fi

# 2. iPad Pro 13" capture (Multi-column responsive layout)
if [ -n "$IPAD_UDID" ]; then
  xcrun simctl boot "$IPAD_UDID" || true
  flutter test integration_test/store_screenshots_test.dart -d "$IPAD_UDID"
  xcrun simctl shutdown "$IPAD_UDID"
fi
```

### 3b. Interactive Fallback Mode (For Live Apps & Native SDKs)
If integration tests cannot easily mock complex native hardware (e.g. Camera, Bluetooth, HealthKit):
Use the interactive capture tool:

```bash
# Run app in standard development mode on booted device
flutter run

# In a separate terminal, launch the interactive capture tool:
bash <(curl -s ...) or plugins/supergraph/skills/flutter-screenshots/scripts/capture-store-shots.sh interactive
```
Navigate to each screen on the simulator and press `[ENTER]` in terminal to capture directly into `screenshots/ios_iphone_6.9/` or `screenshots/ios_ipad_13/`.

---

## Step 4: Normalization & Compliance Gate

Verify all outputs meet strict store requirements:

```bash
# 1. Strip Alpha Channel from all images (Apple Requirement)
for file in screenshots/**/*.png; do
  [ -f "$file" ] || continue
  sips -s format png -s formatOptions default "$file" --out "$file"
done

# 2. Validate pixel dimensions
echo "=== Verifying iPhone 6.9\" (Expected 1320x2868 or 1290x2796) ==="
sips -g pixelWidth -g pixelHeight screenshots/ios_iphone_6.9/*.png

echo "=== Verifying iPad 13\" (Expected 2064x2752 or 2048x2732) ==="
sips -g pixelWidth -g pixelHeight screenshots/ios_ipad_13/*.png
```

---

## Step 5: Deliverables & Report

Report the final results to the user:

```
## 📸 Flutter Store Screenshots Complete
- Target Devices:
  - iPhone 16 Pro Max (6.9" — 1320 x 2868 px)
  - iPad Pro 13-inch (M4 — 2064 x 2752 px)
- Selected Screens:
  1. 01_dashboard.png — Dashboard / Hero overview
  2. 02_feature_primary.png — Main functional value
  3. 03_catalog.png — Product catalog & search
  4. 04_analytics.png — Data insights & profile
- Format Checks:
  - Alpha channel: STRIPPED (No transparency)
  - Color profile: RGB 24-bit
  - Aspect ratio: Native responsive (No scaling distortion)
- Output Location: ./screenshots/
```
