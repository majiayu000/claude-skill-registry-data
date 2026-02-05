---
name: qt-release
description: Set up or troubleshoot GitHub Actions workflows for releasing cross-platform Qt applications. Use when building, signing, notarizing, or packaging Qt apps for macOS, Linux, or Windows.
---

# Cross-Platform Qt Release with GitHub Actions

## Overview

This skill helps set up and troubleshoot GitHub Actions workflows for releasing Qt applications on macOS, Linux, and Windows. It covers Qt installation, platform-specific bundling, code signing, notarization, and common pitfalls.

## Workflow Structure

A complete Qt release workflow should include:

```yaml
name: Build

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]

env:
  QT_VERSION: '6.8.0'
  BUILD_TYPE: Release

jobs:
  build:
    strategy:
      fail-fast: false
      matrix:
        include:
          - os: ubuntu-22.04  # NOT ubuntu-latest (see Linux section)
            name: Linux
          - os: macos-latest
            name: macOS
          - os: windows-latest
            name: Windows

    runs-on: ${{ matrix.os }}
```

## Qt Installation

Use `jurplel/install-qt-action@v4`:

```yaml
- name: Install Qt
  uses: jurplel/install-qt-action@v4
  with:
    version: ${{ env.QT_VERSION }}
    cache: true
    modules: 'qtimageformats'  # Add modules as needed
```

## Platform-Specific Instructions

### macOS

#### Qt Framework Bundling

```yaml
- name: Bundle Qt Frameworks (macOS)
  if: runner.os == 'macOS'
  run: |
    macdeployqt build/qt/myapp.app -verbose=2

    # Remove Headers and .prl files that can cause signing issues
    APP_PATH="build/qt/myapp.app"
    find "$APP_PATH/Contents/Frameworks" -name "Headers" -exec rm -rf {} + 2>/dev/null || true
    find "$APP_PATH/Contents/Frameworks" -name "*.prl" -delete
```

#### Code Signing

**Required GitHub Secrets:**
- `MACOS_CERTIFICATE`: Base64-encoded .p12 certificate
- `MACOS_CERTIFICATE_PWD`: Certificate password
- `MACOS_SIGNING_IDENTITY`: e.g., "Developer ID Application: Your Name (TEAMID)"
- `APPLE_ID`: Apple ID email for notarization
- `APPLE_APP_PASSWORD`: App-specific password
- `APPLE_TEAM_ID`: Your team ID

**Certificate Export Steps:**
1. Open Keychain Access
2. Find "Developer ID Application" certificate (must have private key)
3. Right-click > Export > Save as .p12
4. Base64 encode: `base64 -i certificate.p12 | pbcopy`

**Signing Workflow:**

```yaml
- name: Import Code Signing Certificate
  id: codesign
  if: runner.os == 'macOS'
  env:
    MACOS_CERTIFICATE: ${{ secrets.MACOS_CERTIFICATE }}
    MACOS_CERTIFICATE_PWD: ${{ secrets.MACOS_CERTIFICATE_PWD }}
  run: |
    if [ -z "$MACOS_CERTIFICATE" ]; then
      echo "has_certificate=false" >> $GITHUB_OUTPUT
      exit 0
    fi
    echo "has_certificate=true" >> $GITHUB_OUTPUT

    KEYCHAIN_PATH=$RUNNER_TEMP/signing.keychain-db
    KEYCHAIN_PASSWORD=$(openssl rand -base64 32)

    security create-keychain -p "$KEYCHAIN_PASSWORD" "$KEYCHAIN_PATH"
    security set-keychain-settings -lut 21600 "$KEYCHAIN_PATH"
    security unlock-keychain -p "$KEYCHAIN_PASSWORD" "$KEYCHAIN_PATH"

    echo "$MACOS_CERTIFICATE" | base64 --decode > $RUNNER_TEMP/certificate.p12
    security import $RUNNER_TEMP/certificate.p12 -P "$MACOS_CERTIFICATE_PWD" \
      -A -t cert -f pkcs12 -k "$KEYCHAIN_PATH"
    security list-keychain -d user -s "$KEYCHAIN_PATH"
    security set-key-partition-list -S apple-tool:,apple:,codesign: \
      -s -k "$KEYCHAIN_PASSWORD" "$KEYCHAIN_PATH"

- name: Sign App Bundle
  if: runner.os == 'macOS' && steps.codesign.outputs.has_certificate == 'true'
  env:
    SIGNING_IDENTITY: ${{ secrets.MACOS_SIGNING_IDENTITY }}
  run: |
    APP_PATH="build/qt/myapp.app"

    # Sign Qt frameworks
    find "$APP_PATH/Contents/Frameworks" -name "*.framework" -type d | while read framework; do
      codesign --force --options runtime --sign "$SIGNING_IDENTITY" --timestamp "$framework"
    done

    # Sign Qt plugins
    find "$APP_PATH/Contents/PlugIns" -name "*.dylib" -type f | while read plugin; do
      codesign --force --options runtime --sign "$SIGNING_IDENTITY" --timestamp "$plugin"
    done

    # Sign dylibs in Frameworks
    find "$APP_PATH/Contents/Frameworks" -name "*.dylib" -type f | while read dylib; do
      codesign --force --options runtime --sign "$SIGNING_IDENTITY" --timestamp "$dylib"
    done

    # Sign main executable
    codesign --force --options runtime --sign "$SIGNING_IDENTITY" --timestamp "$APP_PATH/Contents/MacOS/myapp"

    # Sign app bundle
    codesign --force --options runtime --sign "$SIGNING_IDENTITY" --timestamp "$APP_PATH"

    # Verify
    codesign --verify --verbose=4 "$APP_PATH"
    spctl -a -vvv "$APP_PATH" || echo "spctl check completed"
```

#### Notarization

```yaml
- name: Notarize App Bundle
  if: runner.os == 'macOS' && steps.codesign.outputs.has_certificate == 'true' && startsWith(github.ref, 'refs/tags/v')
  env:
    APPLE_ID: ${{ secrets.APPLE_ID }}
    APPLE_APP_PASSWORD: ${{ secrets.APPLE_APP_PASSWORD }}
    APPLE_TEAM_ID: ${{ secrets.APPLE_TEAM_ID }}
  run: |
    APP_PATH="build/qt/myapp.app"
    ditto -c -k --keepParent "$APP_PATH" $RUNNER_TEMP/myapp-notarize.zip

    xcrun notarytool submit $RUNNER_TEMP/myapp-notarize.zip \
      --apple-id "$APPLE_ID" \
      --password "$APPLE_APP_PASSWORD" \
      --team-id "$APPLE_TEAM_ID" \
      --wait

    xcrun stapler staple "$APP_PATH"
```

#### Packaging (CRITICAL)

**Use `ditto`, NOT `zip`!** The `zip` command follows symlinks and creates copies, corrupting Qt framework structure.

```yaml
- name: Package (macOS)
  if: runner.os == 'macOS'
  run: |
    cd build/qt
    # ditto preserves symlinks, resource forks, and extended attributes
    ditto -c -k --sequesterRsrc --keepParent myapp.app myapp-macos.zip
```

### Linux

#### Use ubuntu-22.04, NOT ubuntu-latest

`linuxdeployqt` requires glibc 2.35 or older for broad compatibility:

```yaml
- os: ubuntu-22.04  # Required for linuxdeployqt
  name: Linux
```

#### Dependencies

```yaml
- name: Install Linux dependencies
  if: runner.os == 'Linux'
  run: |
    sudo apt-get update
    sudo apt-get install -y libgl1-mesa-dev libxkbcommon-dev libxkbcommon-x11-0 \
      imagemagick libfuse2 libxcb-cursor0
```

#### AppImage Creation

```yaml
- name: Package (Linux AppImage)
  if: runner.os == 'Linux'
  run: |
    mkdir -p AppDir/usr/bin
    mkdir -p AppDir/usr/share/applications
    mkdir -p AppDir/usr/share/icons/hicolor/256x256/apps

    cp build/qt/myapp AppDir/usr/bin/
    cp qt/myapp.desktop AppDir/usr/share/applications/
    cp qt/myapp.desktop AppDir/

    # Create placeholder icon (replace with real icon)
    convert -size 256x256 xc:'#6B46C1' AppDir/usr/share/icons/hicolor/256x256/apps/myapp.png
    cp AppDir/usr/share/icons/hicolor/256x256/apps/myapp.png AppDir/myapp.png

    wget -q https://github.com/probonopd/linuxdeployqt/releases/download/continuous/linuxdeployqt-continuous-x86_64.AppImage
    chmod +x linuxdeployqt-continuous-x86_64.AppImage

    ./linuxdeployqt-continuous-x86_64.AppImage AppDir/usr/share/applications/myapp.desktop -appimage -verbose=2

    mv MyApp*.AppImage myapp-linux.AppImage
```

#### Desktop File

Create `qt/myapp.desktop`:

```ini
[Desktop Entry]
Type=Application
Name=MyApp
Comment=Description of your app
Exec=myapp
Icon=myapp
Categories=Game;Utility;
Terminal=false
```

### Windows

#### OpenGL Linking

Add to CMakeLists.txt:

```cmake
if(WIN32)
    target_link_libraries(myapp PRIVATE opengl32)
endif()
```

#### Packaging

```yaml
- name: Package (Windows)
  if: runner.os == 'Windows'
  shell: pwsh
  run: |
    cd build/qt/Release
    mkdir package
    copy myapp.exe package/
    windeployqt --release --no-translations package/myapp.exe
    Compress-Archive -Path package/* -DestinationPath ../myapp-windows.zip
```

## Common Issues and Fixes

### macOS: "bundle format is ambiguous"

**Cause:** Framework symlinks were converted to copies (usually by `zip`).

**Fix:** Use `ditto` for packaging:
```bash
ditto -c -k --sequesterRsrc --keepParent myapp.app myapp.zip
```

### macOS: Gatekeeper warnings despite notarization

**Check:**
1. Verify stapling: `xcrun stapler validate myapp.app`
2. Check spctl: `spctl -a -vvv myapp.app`
3. Ensure using `ditto` not `zip` for packaging

### Linux: "host system is too new"

**Cause:** `linuxdeployqt` requires older glibc for compatibility.

**Fix:** Use `ubuntu-22.04` instead of `ubuntu-latest`.

### Linux: ImageMagick font errors

**Cause:** Font packages not installed.

**Fix:** Use simple icon without text:
```bash
convert -size 256x256 xc:'#6B46C1' icon.png
```

### Build: Missing includes

Add to source files as needed:
```cpp
#include <cstddef>    // for size_t
#include <string>     // for std::string
#include <algorithm>  // for std::find
```

### GitHub Actions: Can't check secrets in `if:`

**Wrong:**
```yaml
if: secrets.MY_SECRET != ''  # Doesn't work
```

**Right:**
```yaml
- id: check
  run: |
    if [ -n "$MY_SECRET" ]; then
      echo "has_secret=true" >> $GITHUB_OUTPUT
    fi
  env:
    MY_SECRET: ${{ secrets.MY_SECRET }}

- if: steps.check.outputs.has_secret == 'true'
```

## Release Job

```yaml
release:
  needs: build
  if: startsWith(github.ref, 'refs/tags/v')
  runs-on: ubuntu-latest
  permissions:
    contents: write

  steps:
    - name: Download all artifacts
      uses: actions/download-artifact@v4
      with:
        path: artifacts

    - name: Create Release
      uses: softprops/action-gh-release@v1
      with:
        files: |
          artifacts/myapp-linux/myapp-linux.AppImage
          artifacts/myapp-macos/myapp-macos.zip
          artifacts/myapp-windows/myapp-windows.zip
        draft: true
        generate_release_notes: true
```

## Verification Commands

After downloading a macOS release:

```bash
# Check code signature
codesign --verify --verbose=4 myapp.app

# Check Gatekeeper acceptance
spctl -a -vvv myapp.app

# Verify framework symlinks are intact
ls -la myapp.app/Contents/Frameworks/QtCore.framework/
# QtCore should be symlink -> Versions/Current/QtCore
```
