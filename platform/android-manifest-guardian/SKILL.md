---
name: Android Manifest Guardian
description: Rules and guidelines for safely modifying the AndroidManifest.xml.
---

# Android Manifest Guardian

This skill ensures `AndroidManifest.xml` modifications are safe, correct, and secure.

## Permissions
- **Request Minimization**: Only request permissions strictly needed.
- **Location**: Always use standard `<uses-permission android:name="android.permission.NAME" />`.
- **Runtime Permissions**: Remember that dangerous permissions (e.g., storage, location) require runtime requests in Java/Kotlin code, not just in Manifest.

## Services & Receivers
### IM Services
InputMethodServices must have:
```xml
<service
    android:name=".YourService"
    android:permission="android.permission.BIND_INPUT_METHOD"
    android:exported="true">
    <intent-filter>
        <action android:name="android.view.InputMethod" />
    </intent-filter>
    <meta-data
        android:name="android.view.im"
        android:resource="@xml/method" />
</service>
```

### Exported Flag
- Always explicitly set `android:exported="true"` or `"false"` for components with Intent Filters (required for Android 12+).
- **Security**: Set `exported="false"` unless the component *must* be accessible to other apps.

## Features
Define hardware requirements to prevent installation on incompatible devices:
```xml
<uses-feature android:name="android.hardware.touchscreen" android:required="true" />
```
