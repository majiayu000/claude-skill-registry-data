---
name: NativePHP Configuration
description: This skill should be used when the user asks about "nativephp config", "nativephp.php", "nativephp permission", "enable camera permission", "NATIVEPHP_APP_ID", "environment variables", "app permissions", "config/nativephp.php", "deep link config", "status bar style", "orientation config", "cleanup config", or needs to configure their NativePHP Mobile application.
version: 0.1.0
---

# NativePHP Configuration

This skill provides guidance for configuring NativePHP Mobile applications through the config file and environment variables.

## Configuration File

The main configuration file is `config/nativephp.php`. Publish it with:

```bash
php artisan vendor:publish --tag=nativephp-config
```

## Essential Environment Variables

### Required

```env
# Unique app identifier (reverse domain notation)
# Only lowercase letters, numbers, and periods
# NO hyphens, underscores, spaces, or emoji
NATIVEPHP_APP_ID=com.yourcompany.yourapp
```

### Recommended

```env
# App version (semver)
NATIVEPHP_APP_VERSION=1.0.0

# Numeric version code (increment for each store upload)
NATIVEPHP_APP_VERSION_CODE=1

# Initial URL to load (default: "/")
NATIVEPHP_START_URL=/
```

### iOS-Specific

```env
# Apple Developer Team ID (from developer.apple.com)
NATIVEPHP_DEVELOPMENT_TEAM=ABC123XYZ

# App Store Connect credentials (for deployment)
APP_STORE_API_KEY=your-api-key
APP_STORE_API_KEY_ID=KEYID123
APP_STORE_API_ISSUER_ID=issuer-uuid
APP_STORE_APP_NAME=Your App Name
```

### Android-Specific

```env
# Gradle JDK path (if not using JAVA_HOME)
NATIVEPHP_GRADLE_PATH=/path/to/jdk

# Android SDK location
NATIVEPHP_ANDROID_SDK_LOCATION=/path/to/android/sdk

# Android emulator path
ANDROID_EMULATOR=/path/to/emulator

# Status bar icon style: 'auto', 'light', 'dark'
NATIVEPHP_ANDROID_STATUS_BAR_STYLE=auto

# Enable R8/ProGuard minification for release
NATIVEPHP_ANDROID_MINIFY_ENABLED=true

# Windows only: 7-Zip location
NATIVEPHP_7ZIP_LOCATION=C:\Program Files\7-Zip\7z.exe
```

### Deep Links

```env
# Custom URL scheme (e.g., myapp://path)
NATIVEPHP_DEEPLINK_SCHEME=myapp

# Associated domain for universal/app links (e.g., https://example.com/path)
NATIVEPHP_DEEPLINK_HOST=example.com
```

## Permissions Configuration

All permissions default to `false`. Enable only what your app needs in `config/nativephp.php`:

```php
'permissions' => [
    // Biometric authentication (Face ID, Touch ID, fingerprint)
    'biometric' => false,

    // Camera access for photos/video
    'camera' => false,

    // GPS location access
    'location' => false,

    // Microphone for audio recording
    'microphone' => false,

    // Background audio recording (iOS)
    'microphone_background' => false,

    // Network state monitoring (enabled by default)
    'network_state' => true,

    // NFC reader access
    'nfc' => false,

    // Push notification capability
    'push_notifications' => false,

    // QR code and barcode scanning
    'scanner' => false,

    // Read external storage
    'storage_read' => false,

    // Write external storage
    'storage_write' => false,

    // Haptic feedback
    'vibrate' => false,
],
```

### Custom iOS Permission Descriptions

Provide custom permission descriptions for iOS:

```php
'permissions' => [
    'camera' => 'We need camera access to scan documents',
    'location' => 'Location is used to show nearby stores',
    'microphone' => 'Record voice notes for your tasks',
],
```

## Display Configuration

### Orientation Settings

```php
'orientation' => [
    'iphone' => [
        'portrait',
        'landscape_left',
        'landscape_right',
        // 'upside_down' // Not recommended for iPhone
    ],
    'android' => [
        'portrait',
        'landscape_left',
        'landscape_right',
        'upside_down',
    ],
],
```

**Note**: iPad always supports all orientations regardless of settings.

### iPad Support

```php
// Enable iPad support
'ipad' => true,
```

**Warning**: Once an app with iPad support is published, removing it requires a new App ID.

### Status Bar Style (Android)

```php
// Options: 'auto', 'light' (for dark backgrounds), 'dark' (for light backgrounds)
'status_bar_style' => 'auto',
```

## App Identification

```php
// Unique app identifier (from NATIVEPHP_APP_ID)
'app_id' => env('NATIVEPHP_APP_ID', 'com.nativephp.app'),

// Version string (semver)
'version' => env('NATIVEPHP_APP_VERSION', '1.0.0'),

// Numeric version code for Play Store
'version_code' => env('NATIVEPHP_APP_VERSION_CODE', 1),

// Initial URL to load
'start_url' => env('NATIVEPHP_START_URL', '/'),
```

## Deep Link Configuration

```php
// Custom URL scheme (e.g., myapp://path)
'deeplink_scheme' => env('NATIVEPHP_DEEPLINK_SCHEME', 'nativephp'),

// Domain for HTTPS deep links and NFC
'deeplink_host' => env('NATIVEPHP_DEEPLINK_HOST', ''),
```

### Associated Domain Setup

For HTTPS deep links (universal/app links), host verification files:

**iOS** - `/.well-known/apple-app-site-association`:
```json
{
  "applinks": {
    "apps": [],
    "details": [{
      "appID": "TEAMID.com.yourcompany.yourapp",
      "paths": ["*"]
    }]
  }
}
```

**Android** - `/.well-known/assetlinks.json`:
```json
[{
  "relation": ["delegate_permission/common.handle_all_urls"],
  "target": {
    "namespace": "android_app",
    "package_name": "com.yourcompany.yourapp",
    "sha256_cert_fingerprints": ["YOUR_CERT_FINGERPRINT"]
  }
}]
```

## Build Configuration (Android)

```php
'build' => [
    // Enable R8/ProGuard minification for release builds
    'minify_enabled' => env('NATIVEPHP_ANDROID_MINIFY_ENABLED', false),

    // Debug symbol level for Play Store crashes
    'debug_symbols' => 'none', // 'full', 'symbol_table', 'none'

    // Enable parallel Gradle builds
    'parallel_builds' => true,

    // Enable incremental builds
    'incremental_builds' => true,
],
```

## Hot Reload Configuration

```php
'hot_reload' => [
    // Paths to watch for changes
    'watch_paths' => [
        'app',
        'resources',
        'routes',
        'config',
    ],

    // Patterns to exclude from watch
    'exclude_patterns' => [
        'storage',
        'node_modules',
        'vendor',
    ],
],
```

## Cleanup Configuration

Remove sensitive data before bundling:

```php
// Environment variables to remove before bundling
'cleanup_env_keys' => [
    'AWS_ACCESS_KEY_ID',
    'AWS_SECRET_ACCESS_KEY',
    'STRIPE_SECRET',
    'PUSHER_APP_SECRET',
    // Add your sensitive keys
],

// Files/folders to exclude from bundle (reduces app size)
'cleanup_exclude_files' => [
    'tests',
    '.git',
    'node_modules',
    '.env.example',
    'README.md',
    // Add unnecessary files
],
```

## iOS-Specific Configuration

```php
// Apple Developer Team ID
'development_team' => env('NATIVEPHP_DEVELOPMENT_TEAM'),

// App Store Connect API credentials
'app_store_connect' => [
    'api_key' => env('APP_STORE_API_KEY'),
    'api_key_id' => env('APP_STORE_API_KEY_ID'),
    'issuer_id' => env('APP_STORE_API_ISSUER_ID'),
    'app_name' => env('APP_STORE_APP_NAME'),
],
```

## Version Configuration for Development

During development, use `DEBUG` to force fresh extraction:

```env
NATIVEPHP_APP_VERSION=DEBUG
```

This ensures code changes are always reflected without version comparison caching.

## Complete Example Configuration

```php
// config/nativephp.php
return [
    'app_id' => env('NATIVEPHP_APP_ID', 'com.nativephp.app'),
    'version' => env('NATIVEPHP_APP_VERSION', '1.0.0'),
    'version_code' => env('NATIVEPHP_APP_VERSION_CODE', 1),
    'start_url' => env('NATIVEPHP_START_URL', '/'),

    'deeplink_scheme' => env('NATIVEPHP_DEEPLINK_SCHEME', ''),
    'deeplink_host' => env('NATIVEPHP_DEEPLINK_HOST', ''),

    'development_team' => env('NATIVEPHP_DEVELOPMENT_TEAM'),
    'ipad' => false,

    'orientation' => [
        'iphone' => ['portrait'],
        'android' => ['portrait'],
    ],

    'status_bar_style' => 'auto',

    'permissions' => [
        'biometric' => false,
        'camera' => true,
        'location' => false,
        'microphone' => true,
        'push_notifications' => true,
        'scanner' => true,
        'network_state' => true,
        'vibrate' => true,
    ],

    'cleanup_env_keys' => [
        'AWS_SECRET_ACCESS_KEY',
        'STRIPE_SECRET',
    ],

    'cleanup_exclude_files' => [
        'tests',
        '.git',
        'node_modules',
    ],
];
```

## Fetching Live Documentation

For detailed configuration documentation:

- **Configuration**: `https://nativephp.com/docs/mobile/2/getting-started/configuration`
- **Deep Links**: `https://nativephp.com/docs/mobile/2/concepts/deep-links`
- **Web View & Safe Areas**: `https://nativephp.com/docs/mobile/2/the-basics/web-view`

Use WebFetch to retrieve the latest configuration options.
