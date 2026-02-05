---
name: android-app-icon
description: Generate app icon using IconKitchen and place in correct locations
category: android
version: 1.0.0
inputs:
  - icon_source: User's logo/image file path (optional)
  - app_name: App name for text-based icon (optional)
  - primary_color: Primary brand color hex (optional)
outputs:
  - app/src/main/res/mipmap-*/
  - fastlane/metadata/android/en-US/images/icon.png
  - docs/APP_ICON_SETUP.md
verify: "test -f fastlane/metadata/android/en-US/images/icon.png && file fastlane/metadata/android/en-US/images/icon.png | grep '512 x 512'"
---

# Android App Icon

Guide user through IconKitchen to generate app icons, then place assets in correct locations.

## Prerequisites

- Android project
- App name defined in `app/src/main/res/values/strings.xml`

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| icon_source | No | - | Path to logo/image file for icon |
| app_name | No | From strings.xml | App name for text-based icon |
| primary_color | No | From colors.xml | Primary brand color (hex) |

## Process

### Step 1: Analyze Project for Icon Suggestions

```bash
# Extract app name from strings.xml
APP_NAME=$(grep 'name="app_name"' app/src/main/res/values/strings.xml | sed 's/.*>\([^<]*\)<.*/\1/')
echo "App name: $APP_NAME"

# Extract primary color from colors.xml or themes.xml
if [ -f "app/src/main/res/values/colors.xml" ]; then
    PRIMARY_COLOR=$(grep 'name="colorPrimary"\|name="md_theme_light_primary"' app/src/main/res/values/colors.xml | head -1 | sed 's/.*>\([^<]*\)<.*/\1/')
    echo "Primary color: $PRIMARY_COLOR"
fi

# Check if icon resources already exist
if [ -d "app/src/main/res/mipmap-xxxhdpi" ]; then
    echo "Existing icon resources found:"
    ls app/src/main/res/mipmap-xxxhdpi/
fi
```

### Step 2: Generate Icon Setup Guide

Create `docs/APP_ICON_SETUP.md` with project-specific instructions.

### Step 3: IconKitchen Workflow

Direct user to **[https://icon.kitchen/](https://icon.kitchen/)**

**Recommended settings based on project:**
- **Platform:** Android
- **Icon Type:** Adaptive (for Android 8+)
- **Foreground:** User's logo or app name as text
- **Background Color:** Primary color from project
- **Shape:** Circle or Squircle (most common)

**Options:**
- **Option A: Image/Logo** - Upload PNG or SVG (ideally 512x512+)
- **Option B: Clipart** - Search for icon that represents the app
- **Option C: Text** - Use app name or initials

### Step 4: Download and Process Icon Assets

After generating in IconKitchen:
1. Click **"Download"** button
2. Select **"Android"** format
3. Save and extract the ZIP file

The ZIP contains:
```
android/
├── mipmap-mdpi/
├── mipmap-hdpi/
├── mipmap-xhdpi/
├── mipmap-xxhdpi/
├── mipmap-xxxhdpi/
└── play_store_512.png
```

### Step 5: Copy Assets to Project

```bash
# Copy mipmap resources (replace existing)
cp -r /path/to/extracted/android/mipmap-* app/src/main/res/

# Copy Play Store icon to Fastlane metadata
mkdir -p fastlane/metadata/android/en-US/images
cp /path/to/extracted/android/play_store_512.png \
   fastlane/metadata/android/en-US/images/icon.png
```

Or use the provided `scripts/process-icon.sh` helper script.

### Step 6: Verify AndroidManifest

Ensure `AndroidManifest.xml` references the icon:

```xml
<application
    android:icon="@mipmap/ic_launcher"
    android:roundIcon="@mipmap/ic_launcher_round"
    ...>
```

### Step 7: Build and Verify

```bash
# Clean and rebuild
./gradlew clean assembleDebug

# Install and check icon on device/emulator
./gradlew installDebug
```

## Icon Processing Script

A helper script `scripts/process-icon.sh` can automate asset placement:

```bash
#!/bin/bash
# Usage: ./scripts/process-icon.sh /path/to/iconkitchen-download.zip

ZIP_PATH="${1:-}"

if [ -z "$ZIP_PATH" ]; then
    echo "Usage: $0 <path-to-iconkitchen-zip>"
    exit 1
fi

# Extract and process icon assets
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

unzip -q "$ZIP_PATH" -d "$TEMP_DIR"

# Find android directory
ANDROID_DIR=$(find "$TEMP_DIR" -type d -name "android" | head -1)

# Copy mipmap resources
for density in mdpi hdpi xhdpi xxhdpi xxxhdpi; do
    SRC_DIR="$ANDROID_DIR/mipmap-$density"
    DEST_DIR="app/src/main/res/mipmap-$density"

    if [ -d "$SRC_DIR" ]; then
        mkdir -p "$DEST_DIR"
        cp -r "$SRC_DIR"/* "$DEST_DIR/"
        echo "  ✓ mipmap-$density"
    fi
done

# Copy Play Store icon
PLAY_STORE_ICON=$(find "$ANDROID_DIR" -name "play_store_*.png" | head -1)
if [ -n "$PLAY_STORE_ICON" ]; then
    mkdir -p fastlane/metadata/android/en-US/images
    cp "$PLAY_STORE_ICON" fastlane/metadata/android/en-US/images/icon.png
    echo "  ✓ Play Store icon (512x512)"
fi

echo "✅ Icon assets installed successfully!"
```

## Verification

**MANDATORY:** Run these commands:

```bash
# Check icon resources exist
ls -la app/src/main/res/mipmap-xxxhdpi/

# Check Play Store icon
ls -la fastlane/metadata/android/en-US/images/icon.png

# Verify icon dimensions
file fastlane/metadata/android/en-US/images/icon.png
# Should show: PNG image data, 512 x 512

# Build to verify
./gradlew assembleDebug
```

## Completion Criteria

- [ ] `docs/APP_ICON_SETUP.md` generated with project-specific instructions
- [ ] Mipmap resources copied to `app/src/main/res/mipmap-*/`
- [ ] Play Store icon at `fastlane/metadata/android/en-US/images/icon.png`
- [ ] Icon is 512x512 PNG
- [ ] `./gradlew assembleDebug` builds successfully with new icon

## Play Store Requirements

| Asset | Size | Format | Notes |
|-------|------|--------|-------|
| App Icon | 512 x 512 px | PNG | No transparency, no rounded corners |

IconKitchen's `play_store_512.png` meets these requirements.

## Troubleshooting

### "Icon looks pixelated"
**Cause:** Source image too small
**Fix:** Use source image at least 512x512, prefer SVG

### "Icon has wrong shape on some devices"
**Cause:** Android adaptive icons can be masked differently
**Fix:** Ensure important content is in center "safe zone" (66dp circle)

### "Monochrome icon not showing in Android 13"
**Cause:** Missing monochrome layer
**Fix:** IconKitchen generates this automatically, check `ic_launcher.xml`

## Next Steps

After completing this skill:
1. Run `/devtools:android-store-listing` to create feature graphic
2. Run `/devtools:android-screenshot-automation` to capture screenshots
3. Upload to Play Store: `bundle exec fastlane upload_metadata`
