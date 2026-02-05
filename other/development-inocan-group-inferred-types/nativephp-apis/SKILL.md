---
name: NativePHP APIs
description: This skill should be used when the user asks about "nativephp api", "camera api", "device api", "biometrics", "geolocation", "scanner api", "microphone api", "nativephp_call", "god method", "bridge function", "SecureStorage", "Dialog api", "Share api", "PushNotifications api", "Network status", "Browser api", "Haptics", "File api", or needs to use any NativePHP native functionality in their app.
version: 0.1.0
---

# NativePHP Native APIs

This skill provides guidance for using NativePHP's native APIs to access device features like camera, biometrics, geolocation, and more.

## Overview

NativePHP provides PHP Facades that wrap native device functionality. All APIs are accessible via `Native\Mobile\Facades\*` namespace. Most async operations use a fluent "Pending*" builder pattern.

## Available Facades

| Facade | Purpose |
|--------|---------|
| `Camera` | Photos, videos, gallery picker |
| `Device` | Device ID, info, battery, vibration, flashlight |
| `Dialog` | Native alerts and toasts |
| `Scanner` | QR code and barcode scanning |
| `Biometrics` | Face ID, Touch ID, fingerprint |
| `Geolocation` | GPS location and permissions |
| `Microphone` | Audio recording |
| `Network` | Network status |
| `Browser` | Open URLs in browser or in-app |
| `Share` | Native share sheet |
| `SecureStorage` | Keychain/Keystore secure storage |
| `File` | Move and copy files |
| `PushNotifications` | Push notification enrollment |
| `System` | Platform detection, app settings |
| `Haptics` | Haptic feedback (deprecated, use Device) |

## Fluent Builder Pattern

Async operations return `Pending*` objects for configuration:

```php
use Native\Mobile\Facades\Camera;

Camera::getPhoto()
    ->id('profile-photo')      // Track this request
    ->event(MyPhotoEvent::class) // Custom event class
    ->remember()               // Store ID in session
    ->start();                 // Execute (or auto-executes on destruct)
```

Common fluent methods:
- `id(string $id)` - Unique identifier for tracking
- `event(string $class)` - Custom event class for response
- `remember()` - Flash ID to session for retrieval
- `lastId()` - Get last remembered ID from session

## Camera API

```php
use Native\Mobile\Facades\Camera;

// Take photo
Camera::getPhoto()->id('avatar')->start();

// Record video with max duration
Camera::recordVideo()->maxDuration(30)->start();

// Pick from gallery
Camera::pickImages()
    ->images()           // Only images (or ->videos(), ->all())
    ->multiple(true, 5)  // Allow up to 5 selections
    ->start();
```

**Events**: `PhotoTaken`, `PhotoCancelled`, `VideoRecorded`, `VideoCancelled`, `MediaSelected`

## Device API

```php
use Native\Mobile\Facades\Device;

$deviceId = Device::getId();
$info = Device::getInfo();      // Returns JSON with platform, model, etc.
$battery = Device::getBatteryInfo();
Device::vibrate();
Device::flashlight();           // Toggle flashlight
```

## Dialog API

```php
use Native\Mobile\Facades\Dialog;

// Alert with buttons
Dialog::alert('Title', 'Message', ['OK', 'Cancel'])
    ->id('confirm-delete')
    ->show();

// Toast notification
Dialog::toast('Operation complete', 'long'); // 'short' or 'long'
```

**Events**: `ButtonPressed` with `index` and `label` properties

## Scanner API

```php
use Native\Mobile\Facades\Scanner;

Scanner::scan()
    ->prompt('Scan product barcode')
    ->formats(['qr', 'ean13', 'code128']) // or 'all'
    ->continuous(true)  // Keep scanning
    ->id('product-scan')
    ->scan();
```

**Supported formats**: `qr`, `ean13`, `ean8`, `code128`, `code39`, `upca`, `upce`, `all`

**Events**: `CodeScanned` with `data` and `format` properties

## Biometrics API

```php
use Native\Mobile\Facades\Biometrics;

Biometrics::prompt()
    ->id('auth-check')
    ->prompt();
```

**Events**: `Completed` with `success` boolean

## Geolocation API

```php
use Native\Mobile\Facades\Geolocation;

// Get current position
Geolocation::getCurrentPosition()
    ->fineAccuracy(true)  // GPS-level accuracy
    ->id('location')
    ->get();

// Check permissions
Geolocation::checkPermissions()->get();

// Request permissions
Geolocation::requestPermissions()->get();
```

**Events**: `LocationReceived`, `PermissionStatusReceived`, `PermissionRequestResult`

## Microphone API

```php
use Native\Mobile\Facades\Microphone;

// Start recording
Microphone::record()->id('voice-note')->start();

// Control recording
Microphone::pause();
Microphone::resume();
Microphone::stop();

// Get status and recording
$status = Microphone::getStatus();  // 'idle', 'recording', 'paused'
$path = Microphone::getRecording(); // Path to last recording
```

**Events**: `MicrophoneRecorded`, `MicrophoneCancelled`

## Network API

```php
use Native\Mobile\Facades\Network;

$status = Network::status();
// Returns: { connected, type, isExpensive, isConstrained }
```

## Browser API

```php
use Native\Mobile\Facades\Browser;

Browser::open('https://example.com');     // Default browser
Browser::inApp('https://example.com');    // In-app browser
Browser::auth('https://oauth.example.com'); // Auth session
```

## Share API

```php
use Native\Mobile\Facades\Share;

Share::url('Check this out', 'Description', 'https://example.com');
Share::file('Document', 'Here is the file', '/path/to/file.pdf');
```

## SecureStorage API

SecureStorage is a **synchronous** API that stores data in the native keychain (iOS) or keystore (Android). It can be used directly in Blade templates and conditionals.

```php
use Native\Mobile\Facades\SecureStorage;

// Store in native keychain/keystore
SecureStorage::set('api_token', $token);
$token = SecureStorage::get('api_token');
SecureStorage::delete('api_token');
```

### Using in Blade Templates

Because SecureStorage is synchronous, you can use it directly in Blade conditionals:

```blade
@if(SecureStorage::get('api_token'))
    {{-- User is authenticated --}}
    <x-dashboard />
@else
    {{-- Show login --}}
    <x-login-form />
@endif
```

This is particularly useful for auth-gated content without needing to pass auth state through controllers.

## PushNotifications API

```php
use Native\Mobile\Facades\PushNotifications;

// Request permission and enroll
PushNotifications::enroll()->id('main')->enroll();

// Get token (APNS on iOS, FCM on Android)
$token = PushNotifications::getToken();
```

**Events**: `TokenGenerated` with `token` property

## System API

```php
use Native\Mobile\Facades\System;

if (System::isMobile()) { /* running on device */ }
if (System::isIos()) { /* iOS specific */ }
if (System::isAndroid()) { /* Android specific */ }

System::appSettings(); // Open native app settings
```

## File API

```php
use Native\Mobile\Facades\File;

File::move('/from/path', '/to/path');
File::copy('/from/path', '/to/path');
```

## The God Method (nativephp_call)

For advanced usage, call bridge functions directly:

```php
$result = nativephp_call('Camera.GetPhoto', json_encode(['id' => 'test']));
```

Bridge function names follow `Category.Action` pattern:
- `Camera.GetPhoto`, `Camera.RecordVideo`, `Camera.PickMedia`
- `Device.GetId`, `Device.GetInfo`, `Device.Vibrate`
- `Dialog.Alert`, `Dialog.Toast`
- `QrCode.Scan`
- `Biometric.Prompt`
- `Geolocation.GetCurrentPosition`, `Geolocation.CheckPermissions`
- `Network.Status`
- `Browser.Open`, `Browser.OpenInApp`, `Browser.OpenAuth`
- `Microphone.Start`, `Microphone.Stop`, `Microphone.Pause`, `Microphone.Resume`
- `SecureStorage.Set`, `SecureStorage.Get`, `SecureStorage.Delete`
- `Share.Url`, `Share.File`
- `System.OpenAppSettings`
- `PushNotification.RequestPermission`, `PushNotification.GetToken`

## Permission Requirements

Enable required permissions in `config/nativephp.php`:

```php
'permissions' => [
    'camera' => true,
    'microphone' => true,
    'biometric' => true,
    'location' => true,
    'push_notifications' => true,
    'scanner' => true,
    // etc.
],
```

## Fetching Live Documentation

For detailed API documentation, fetch from:

- **APIs Overview**: `https://nativephp.com/docs/mobile/2/apis/overview`
- **Camera**: `https://nativephp.com/docs/mobile/2/apis/camera`
- **Biometrics**: `https://nativephp.com/docs/mobile/2/apis/biometrics`
- **Geolocation**: `https://nativephp.com/docs/mobile/2/apis/geolocation`
- **Scanner**: `https://nativephp.com/docs/mobile/2/apis/scanner`
- **Push Notifications**: `https://nativephp.com/docs/mobile/2/apis/push-notifications`

Use WebFetch for the most current API details.