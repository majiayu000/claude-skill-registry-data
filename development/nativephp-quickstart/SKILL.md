---
name: NativePHP Quickstart
description: This skill should be used when the user asks to "start a nativephp app", "create nativephp project", "setup nativephp mobile", "install nativephp", "new mobile app with laravel", "nativephp prerequisites", "environment setup for nativephp", "configure xcode for nativephp", "android studio setup", or needs help getting started with NativePHP Mobile development.
version: 0.1.0
---

# NativePHP Mobile Quickstart

This skill provides guidance for starting new NativePHP Mobile projects, including prerequisites, installation, environment setup, and initial configuration.

## Overview

NativePHP Mobile enables building native iOS and Android applications using PHP and Laravel. It embeds a PHP runtime directly into native app shells, eliminating the need for a web server.

## Prerequisites

### General Requirements
- PHP 8.3+
- Laravel 11+
- Valid NativePHP Mobile license from nativephp.com

### iOS Development
- macOS with Apple Silicon (M1 or later) - required
- Xcode 16.0 or later
- Xcode Command Line Tools
- Homebrew and CocoaPods
- Apple Developer Program ($99/year) for physical device testing and App Store distribution

### Android Development
- Android Studio 2024.2.1 or later
- Android SDK with API 33+ (recommended: Android 15/API 35)
- JDK 17
- Environment variables configured:
  - `JAVA_HOME` pointing to JDK
  - `ANDROID_HOME` pointing to Android SDK
  - PATH updated with Java and Android tools
- Windows only: 7zip utility

## Installation Steps

### 1. Configure Composer Repository

Add NativePHP repository to `composer.json`:

```json
{
  "repositories": [
    {
      "type": "composer",
      "url": "https://nativephp.composer.sh"
    }
  ]
}
```

Or use Composer 2.9+:
```bash
composer repo add nativephp composer https://nativephp.composer.sh
```

### 2. Set Required Environment Variables

Add to `.env` file:

```env
# Required - reverse domain notation
NATIVEPHP_APP_ID=com.yourcompany.yourapp

# Recommended
NATIVEPHP_APP_VERSION=1.0.0
NATIVEPHP_APP_VERSION_CODE=1

# iOS (if building for iOS)
NATIVEPHP_DEVELOPMENT_TEAM=YOUR_TEAM_ID

# Deep links (optional)
NATIVEPHP_DEEPLINK_SCHEME=yourapp
NATIVEPHP_DEEPLINK_HOST=yourapp.com
```

**Critical**: `NATIVEPHP_APP_ID` must use only lowercase letters, numbers, and periods. No hyphens, underscores, spaces, or emoji.

### 3. Install Package

```bash
composer require nativephp/mobile
php artisan native:install
```

### 4. Run the App

```bash
php artisan native:run android
# or
php artisan native:run ios
```

After installation, use the shorthand:
```bash
php native run android
./native run ios
```

## All Artisan Commands

| Command | Description |
|---------|-------------|
| `native:install [platform]` | Install NativePHP resources. Options: `--force`, `--with-icu`, `--without-icu`, `--skip-php` |
| `native:run [platform]` | Run app in emulator/simulator. Options: `--build=release` |
| `native:watch [platform]` | Watch for changes and hot reload |
| `native:package [platform]` | Package app for distribution |
| `native:release [platform]` | Create release build |
| `native:build-ios` | Build iOS app specifically |
| `native:check-build-number` | Check iOS build number |
| `native:credentials [action]` | Manage app signing credentials |
| `native:open-project [platform]` | Open in Xcode or Android Studio |
| `native:launch-emulator` | Launch Android emulator |
| `native:tail [platform]` | Tail native logs for debugging |
| `native:version` | Show NativePHP version |

## Environment Setup Details

### iOS Setup Checklist

1. Install Xcode from Mac App Store
2. Install Command Line Tools: `xcode-select --install`
3. Install Homebrew: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
4. Install CocoaPods: `brew install cocoapods`
5. For physical devices:
   - Enable Developer Mode on device
   - Register device with Apple Developer account

### Android Setup Checklist

1. Download and install Android Studio
2. Install Android SDK (API 33+) via SDK Manager
3. Install JDK 17 (not auto-installed in recent Android Studio)
4. Create at least one Android Virtual Device (AVD)
5. Configure environment variables:

**macOS/Linux** (`~/.zshrc` or `~/.bashrc`):
```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 17)
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/platform-tools
```

**Windows** (System Environment Variables):
- `JAVA_HOME` = `C:\Program Files\Java\jdk-17`
- `ANDROID_HOME` = `C:\Users\YourName\AppData\Local\Android\Sdk`
- Add to PATH: `%JAVA_HOME%\bin`, `%ANDROID_HOME%\platform-tools`

## Common Setup Issues

### "No AVDs found" Error
Create an Android Virtual Device in Android Studio's Device Manager before running.

### iOS Simulator Not Starting
Ensure Xcode Command Line Tools are selected: `sudo xcode-select -s /Applications/Xcode.app/Contents/Developer`

### Composer Authentication
When prompted, enter your NativePHP license key as the password.

## Fetching Live Documentation

For the most current information, fetch documentation from:

- **Quick Start**: `https://nativephp.com/docs/mobile/2/getting-started/quick-start`
- **Installation**: `https://nativephp.com/docs/mobile/2/getting-started/installation`
- **Environment Setup**: `https://nativephp.com/docs/mobile/2/getting-started/environment-setup`
- **Configuration**: `https://nativephp.com/docs/mobile/2/getting-started/configuration`

Use WebFetch to retrieve the latest documentation when users need detailed or updated information.

## Next Steps After Setup

1. Configure permissions in `config/nativephp.php`
2. Set up EDGE components for native UI
3. Implement native functionality using Facades
4. Test on physical devices before deployment