---
name: figma-to-flutter
description: This skill should be used when converting Figma designs to Flutter code. Trigger this skill when users say "convert this Figma design to Flutter", "run Figma workflow", "implement this Figma screen", or provide Figma links requesting Flutter UI implementation. The skill handles the complete workflow from extracting Figma metadata to implementing pixel-perfect Flutter UIs with iterative testing.
---

# Figma to Flutter Workflow

## Overview

Convert Figma designs into Flutter code through an automated workflow that extracts design metadata, generates reference code, exports assets, implements the UI, and iteratively tests until the implementation matches the design pixel-perfectly.

## When to Use This Skill

Trigger this workflow when users:
- Provide Figma design links and request Flutter implementation
- Say "convert this Figma design to Flutter code"
- Say "run Figma workflow" or "trigger flutter ui workflow"
- Say "implement this Figma screen"
- Request UI implementation from Figma designs

## Workflow Process

### Step 1: Preparation

#### Determine Feature Name

If not provided by the user, infer the feature name from:
- Branch name
- Conversation context
- Design content
- User's working directory

Ask the user if unclear.

#### Set Up Workspace Directory

Create the workspace structure at git repository root:

```bash
mkdir -p .ui-workspace/$FEATURE/{figma_screenshots,figma_images,figma_code,app_screenshots}
```

Ensure `.ui-workspace/` is in `.git/info/exclude`:

```bash
grep -q "^\.ui-workspace/$" .git/info/exclude || echo ".ui-workspace/" >> .git/info/exclude
```

#### Verify API Server

Check if the Figma API server is running:

```bash
curl -s http://localhost:3001/health
```

If server is not running, set it up (one-time):

```bash
# Check if already cloned
if [ ! -d ~/Documents/figma-api ]; then
  mkdir -p ~/Documents
  git clone https://github.com/prateekmedia/FigmaToCode-RestApi ~/Documents/figma-api
  echo "API server cloned. Please follow ~/Documents/figma-api/README to install dependencies and start the server."
else
  echo "API server exists but not running. Please start it: cd ~/Documents/figma-api && [start command from README]"
fi
```

Wait for user to start the server before proceeding.

### Step 2: Extract Figma Metadata

#### Analyze Asset Requirements First

Before making API calls, analyze the app's asset structure to determine which scales to download:

1. Check `assets/` directory structure
2. Search for `Image.asset` calls to identify scale parameters
3. Determine which scales are actually needed

See **Step 3: Asset Management** for detailed analysis instructions.

#### Run API Calls

Execute both API calls **in parallel** to extract all metadata from the Figma design.

**Screenshot API**:

```bash
curl -X POST http://localhost:3001/api/screenshot \
  -H "Content-Type: application/json" \
  -d "{
    \"url\": \"$FIGMA_URL\",
    \"format\": \"png\",
    \"scale\": 2,
    \"saveToFile\": true,
    \"directory\": \".ui-workspace/$FEATURE/figma_screenshots\"
  }"
```

**Convert API** (customize `scales` based on asset analysis):

```bash
# Default: Download all scales
curl -X POST http://localhost:3001/api/convert \
  -H "Content-Type: application/json" \
  -d "{
    \"url\": \"$FIGMA_URL\",
    \"settings\": {
      \"framework\": \"Flutter\"
    },
    \"exportImages\": true,
    \"exportImagesOptions\": {
      \"scales\": [\"1x\", \"2x\", \"3x\", \"4x\"],
      \"directory\": \".ui-workspace/$FEATURE/figma_images\"
    },
    \"output\": {
      \"saveToFile\": true,
      \"directory\": \".ui-workspace/$FEATURE/figma_code\"
    }
  }"
```

**Customize scales**: Modify the `scales` array based on your analysis (e.g., `[\"2x\", \"3x\"]` if app only uses those).

**Results**:
- Design screenshot: `.ui-workspace/$FEATURE/figma_screenshots/`
- Generated Flutter code: `.ui-workspace/$FEATURE/figma_code/`
- Exported assets: `.ui-workspace/$FEATURE/figma_images/{requested_scales}/`

### Step 3: Implementation

#### Review Reference Materials

Examine the extracted materials:
1. **Figma screenshot**: Visual reference for the design
2. **Generated code**: Reference for text styles, dimensions, colors, layout
3. **Assets**: Images to integrate into the app

#### Implement Flutter UI

Using the reference materials:

**Text Styles**: Extract font families, sizes, weights, and colors from generated code
**Layout**: Reference container dimensions, padding, margins, and widget hierarchy
**Colors**: Use exact hex values from the design
**Spacing**: Match padding, margin, and gap values

**Important**: Write proper Flutter code following app conventions. Do not copy generated code directly—use it as a reference.

#### Asset Management

**1. Analyze Existing Asset Structure**

Before downloading or copying assets, examine the app's current asset organization:

- Check if `assets/` directory exists and how it's structured
- Identify the scaling strategy used in the codebase:
  - **Multi-directory approach**: Separate directories for each scale (e.g., `assets/`, `assets/2x/`, `assets/3x/`, `assets/4x/`)
  - **Single directory with scale parameter**: Single `assets/` directory with explicit `scale` parameter in `Image.asset()` calls
  - **No standard structure**: May need to establish one

**2. Determine Required Asset Scales**

Based on the analysis:

- **If multi-directory structure exists**: Check which scale directories are present (e.g., only `assets/2x/` and `assets/3x/`)
- **If using scale parameter**: Search for `Image.asset` calls to identify what scale values are used (e.g., `scale: 4`)
- **If no standard exists**: Default to downloading 3x scale assets

Only download the scales actually needed by the app to avoid unnecessary files.

**3. Download Required Scales from API**

Modify the Convert API call to download only necessary scales:

```bash
# Example: If app uses only 2x and 3x
curl -X POST http://localhost:3001/api/convert \
  -H "Content-Type: application/json" \
  -d "{
    \"url\": \"$FIGMA_URL\",
    \"settings\": {\"framework\": \"Flutter\"},
    \"exportImages\": true,
    \"exportImagesOptions\": {
      \"scales\": [\"2x\", \"3x\"],
      \"directory\": \".ui-workspace/$FEATURE/figma_images\"
    },
    \"output\": {
      \"saveToFile\": true,
      \"directory\": \".ui-workspace/$FEATURE/figma_code\"
    }
  }"
```

**4. Identify Required Assets**

Review generated code to find referenced image assets.

**5. Copy and Rename Assets**

Copy assets from `.ui-workspace/$FEATURE/figma_images/` following the app's existing structure:

**Multi-directory structure**:
```bash
# Copy to matching scale directories
cp .ui-workspace/$FEATURE/figma_images/2x/asset.png assets/2x/new_name.png
cp .ui-workspace/$FEATURE/figma_images/3x/asset.png assets/3x/new_name.png
```

**Single directory with scale parameter**:
```bash
# Copy only the required scale (e.g., 4x)
cp .ui-workspace/$FEATURE/figma_images/4x/asset.png assets/new_name.png
# Then use: Image.asset('assets/new_name.png', scale: 4)
```

**No standard structure**:
```bash
# Default to 3x scale in single directory
cp .ui-workspace/$FEATURE/figma_images/3x/asset.png assets/new_name.png
# Use with explicit scale: Image.asset('assets/new_name.png', scale: 3)
```

Rename assets to meaningful names using snake_case (e.g., `profile_avatar.png`, `feed_background.png`).

**6. Create Asset Mapping**

Maintain `.ui-workspace/$FEATURE/figma_images/mapping.json`:

```json
{
  "123:456_user_avatar.png": "assets/profile_avatar.png",
  "789:012_background.png": "assets/feed_background.png"
}
```

**7. Update pubspec.yaml**

Ensure assets are declared according to the app's structure:

**Multi-directory**:
```yaml
flutter:
  assets:
    - assets/
    - assets/2x/
    - assets/3x/
```

**Single directory**:
```yaml
flutter:
  assets:
    - assets/
```

### Step 4: Testing

#### Create Golden Tests

Write golden tests to capture widget screenshots:

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('FeatureName screen golden test', (WidgetTester tester) async {
    // Set device size to match Figma design
    await tester.binding.setSurfaceSize(Size(375, 812)); // Example: iPhone X

    await tester.pumpWidget(
      MaterialApp(
        home: YourImplementedScreen(),
      ),
    );

    await expectLater(
      find.byType(MaterialApp),
      matchesGoldenFile('goldens/feature_name.png'),
    );
  });
}
```

**Important Considerations**:
- Match device size to Figma design dimensions
- Ensure images render (use test image data)
- Ensure text is not obscured
- For scrollable content with finite height: capture complete area if possible
- For infinite/long scrollable content: capture multiple scroll states

Generate golden files:
```bash
flutter test --update-goldens
```

#### Capture App Screenshots

Take screenshots from the running app:

**iOS Simulator**:
```bash
xcrun simctl io booted screenshot .ui-workspace/$FEATURE/app_screenshots/ss_$(date +%Y-%m-%d_%H-%M-%S)_$description.png
```

**Android Emulator**:
```bash
adb shell screencap -p > .ui-workspace/$FEATURE/app_screenshots/ss_$(date +%Y-%m-%d_%H-%M-%S)_$description.png
```

**Real iOS Device**:
```bash
~/Documents/scripts/ios_screenshot.sh .ui-workspace/$FEATURE/app_screenshots/ss_$(date +%Y-%m-%d_%H-%M-%S)_$description.png
```

Replace `$description` with a brief description (e.g., `Feed_View`, `Profile_Edit`).

### Step 5: Comparison and Iteration

#### Compare Screenshots

Open side-by-side:
- **Figma screenshot**: `.ui-workspace/$FEATURE/figma_screenshots/`
- **App screenshot**: `.ui-workspace/$FEATURE/app_screenshots/`

#### Identify Differences

Check for discrepancies in:
- **Layout**: Widget positioning, alignment, constraints
- **Text**: Font family, size, weight, color, line height
- **Colors**: Exact hex values, opacity
- **Spacing**: Padding, margins, gaps
- **Assets**: Image rendering, scaling, paths
- **Styling**: Borders, shadows, border radius

#### Fix Issues

Update Flutter implementation based on identified differences.

Common issues:
- Incorrect constraints (Expanded/Flexible usage)
- Wrong font properties
- Color mismatches
- Padding/margin discrepancies
- Asset resolution or path errors

#### Retest

Hot reload or restart the app:
```bash
# Hot reload
kill -SIGUSR1 $(cat /tmp/flutter-figma-workflow.pid)

# Hot restart
kill -SIGUSR2 $(cat /tmp/flutter-figma-workflow.pid)
```

Take new app screenshots and compare again.

#### Iterate Until Perfect

Repeat the comparison → fix → retest cycle until app screenshots match Figma screenshots **exactly**.

**Iteration Strategy**:
1. Fix major layout and positioning issues first
2. Address styling (colors, fonts, sizes)
3. Fine-tune details (shadows, borders, spacing)
4. Test after each round of fixes

## Additional Resources

For detailed information, refer to the bundled references:

- **`references/api_setup.md`**: Complete API documentation, setup instructions, troubleshooting
- **`references/workflow_details.md`**: In-depth workflow details, asset management, testing strategies, common issues

## Tips for Success

**Use Reference Code Wisely**: Treat generated code as a reference for values (colors, sizes, spacing), not as production-ready code.

**Asset Organization**: Keep asset naming consistent and maintain the mapping file for future reference.

**Incremental Testing**: Test frequently during implementation rather than waiting until the end.

**Device Consistency**: Use the same device/simulator dimensions throughout testing for accurate comparison.

**Pixel-Perfect Goal**: The workflow is complete only when app screenshots and Figma screenshots are visually identical.
