---
name: NativePHP JavaScript Integration
description: This skill should be used when the user asks about "javascript nativephp", "vue nativephp", "react nativephp", "#nativephp import", "Native.on", "js native function", "javascript camera", "javascript scanner", "inertia nativephp", "svelte nativephp", "frontend native api", or needs to use NativePHP native functionality in JavaScript/Vue/React applications.
version: 0.1.0
---

# NativePHP JavaScript Integration

This skill provides guidance for using NativePHP native functionality in JavaScript, Vue, React, Svelte, and other frontend frameworks.

## Overview

NativePHP provides a JavaScript library that mirrors the PHP APIs, enabling frontend frameworks to access native device functionality. The library is fully typed for excellent IDE support.

## Installation

Add the import map to your `package.json`:

```json
{
  "imports": {
    "#nativephp": "./vendor/nativephp/mobile/resources/dist/native.js"
  }
}
```

Or in Vite config:

```js
// vite.config.js
export default defineConfig({
  resolve: {
    alias: {
      '#nativephp': './vendor/nativephp/mobile/resources/dist/native.js'
    }
  }
});
```

## Basic Usage

```javascript
import { camera, dialog, scanner, Events, on, off } from '#nativephp';

// Take a photo
camera.getPhoto().id('my-photo').start();

// Show an alert
dialog.alert('Title', 'Message', ['OK', 'Cancel']).show();

// Listen for events
on(Events.Camera.PhotoTaken, handlePhotoTaken);
```

## Event Handling

### Subscribing to Events

```javascript
import { on, off, Events } from '#nativephp';

// Define handler as named function for cleanup
const handlePhotoTaken = (path, mimeType, id) => {
    console.log('Photo taken:', path);
};

// Subscribe to an event
on(Events.Camera.PhotoTaken, handlePhotoTaken);

// Later, unsubscribe using off() with the same handler reference
off(Events.Camera.PhotoTaken, handlePhotoTaken);
```

**Important**: `on()` does NOT return an unsubscribe function. You must use `off()` with the same handler reference to unsubscribe.

### Available Events

```javascript
import { Events } from '#nativephp';

// Camera events
Events.Camera.PhotoTaken
Events.Camera.PhotoCancelled
Events.Camera.VideoRecorded
Events.Camera.VideoCancelled

// Gallery events
Events.Gallery.MediaSelected

// Scanner events
Events.Scanner.CodeScanned

// Biometric events
Events.Biometric.Completed

// Dialog events
Events.Alert.ButtonPressed

// Microphone events
Events.Microphone.MicrophoneRecorded
Events.Microphone.MicrophoneCancelled

// Geolocation events
Events.Geolocation.LocationReceived
Events.Geolocation.PermissionStatusReceived
Events.Geolocation.PermissionRequestResult

// Push notification events
Events.PushNotification.TokenGenerated
```

## Camera API

```javascript
import { camera, Events, on } from '#nativephp';

// Take a photo
camera.getPhoto()
    .id('avatar')
    .remember()
    .start();

// Record video with max duration
camera.recordVideo()
    .maxDuration(30)
    .id('clip')
    .start();

// Pick from gallery
camera.pickImages()
    .images()           // or .videos() or .all()
    .multiple(true, 5)  // Allow up to 5 selections
    .id('gallery-pick')
    .start();

// Handle results
on(Events.Camera.PhotoTaken, (path, mimeType, id) => {
    if (id === 'avatar') {
        document.getElementById('avatar-img').src = path;
    }
});

on(Events.Gallery.MediaSelected, (success, files, count, error, cancelled, id) => {
    if (success) {
        files.forEach(file => console.log(file.path));
    }
});
```

## Scanner API

```javascript
import { scanner, Events, on } from '#nativephp';

// Start scanning
scanner.scan()
    .prompt('Scan QR code')
    .formats(['qr', 'ean13'])
    .continuous(true)
    .id('product-scan')
    .scan();

// Handle scanned codes
on(Events.Scanner.CodeScanned, (data, format, id) => {
    console.log(`Scanned ${format}: ${data}`);
});
```

## Biometrics API

```javascript
import { biometrics, Events, on } from '#nativephp';

// Prompt for authentication
biometrics.prompt()
    .id('secure-action')
    .prompt();

// Handle result
on(Events.Biometric.Completed, (success, id) => {
    if (success) {
        performSecureAction();
    } else {
        showAuthError();
    }
});
```

## Dialog API

```javascript
import { dialog, Events, on } from '#nativephp';

// Show alert with buttons
dialog.alert('Confirm', 'Delete this item?', ['Cancel', 'Delete'])
    .id('confirm-delete')
    .show();

// Handle button press
on(Events.Alert.ButtonPressed, (index, label, id) => {
    if (id === 'confirm-delete' && label === 'Delete') {
        deleteItem();
    }
});

// Show toast (no event)
dialog.toast('Item saved', 'short');
```

## Geolocation API

```javascript
import { geolocation, Events, on } from '#nativephp';

// Check permissions
geolocation.checkPermissions().get();

// Request permissions
geolocation.requestPermissions().get();

// Get current position
geolocation.getCurrentPosition()
    .fineAccuracy(true)
    .id('location')
    .get();

// Handle results
on(Events.Geolocation.LocationReceived, (success, lat, lng, accuracy, timestamp, provider, error, id) => {
    if (success) {
        console.log(`Location: ${lat}, ${lng}`);
    }
});

on(Events.Geolocation.PermissionStatusReceived, (location, coarse, fine, id) => {
    console.log(`Fine location permission: ${fine}`);
});
```

## Microphone API

```javascript
import { microphone, Events, on } from '#nativephp';

// Start recording
microphone.record()
    .id('voice-note')
    .start();

// Control recording
microphone.pause();
microphone.resume();
microphone.stop();

// Get status
const status = await microphone.getStatus(); // 'idle', 'recording', 'paused'
const path = await microphone.getRecording();

// Handle completion
on(Events.Microphone.MicrophoneRecorded, (path, mimeType, id) => {
    console.log('Recording saved:', path);
});
```

## Other APIs

```javascript
import { device, browser, share, secureStorage, network, system, pushNotifications } from '#nativephp';

// Device
const deviceId = await device.getId();
const info = await device.getInfo();
device.vibrate();
device.flashlight();

// Browser
browser.open('https://example.com');
browser.inApp('https://example.com');
browser.auth('https://oauth.example.com');

// Share
share.url('Check this out', 'Description', 'https://example.com');
share.file('Document', 'Here is the file', '/path/to/file.pdf');

// Secure Storage
await secureStorage.set('token', 'secret-value');
const token = await secureStorage.get('token');
await secureStorage.delete('token');

// Network
const status = await network.status();
console.log(status.connected, status.type);

// System
if (system.isMobile()) { /* mobile-specific code */ }
if (system.isIos()) { /* iOS-specific code */ }
if (system.isAndroid()) { /* Android-specific code */ }
system.appSettings();

// Push Notifications
pushNotifications.enroll().id('main').enroll();
const pushToken = await pushNotifications.getToken();
```

## Vue 3 Example

```vue
<template>
  <div class="photo-uploader">
    <img v-if="photoUrl" :src="photoUrl" alt="Photo" />
    <button @click="takePhoto">Take Photo</button>
    <button @click="pickPhoto">Choose from Gallery</button>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { camera, Events, on, off } from '#nativephp';

const photoUrl = ref(null);

const takePhoto = () => {
  camera.getPhoto()
    .id('vue-photo')
    .start();
};

const pickPhoto = () => {
  camera.pickImages()
    .images()
    .single()
    .id('vue-gallery')
    .start();
};

// Define handlers as named functions for cleanup
const handlePhotoTaken = (path, mimeType, id) => {
  photoUrl.value = path;
};

const handleMediaSelected = (success, files, count, error, cancelled, id) => {
  if (success && files.length > 0) {
    photoUrl.value = files[0].path;
  }
};

onMounted(() => {
  on(Events.Camera.PhotoTaken, handlePhotoTaken);
  on(Events.Gallery.MediaSelected, handleMediaSelected);
});

onUnmounted(() => {
  off(Events.Camera.PhotoTaken, handlePhotoTaken);
  off(Events.Gallery.MediaSelected, handleMediaSelected);
});
</script>
```

## React Example

```jsx
import { useState, useEffect } from 'react';
import { camera, scanner, Events, on, off } from '#nativephp';

function QRScanner() {
  const [scannedData, setScannedData] = useState([]);

  useEffect(() => {
    // Define handler for cleanup reference
    const handleCodeScanned = (data, format, id) => {
      setScannedData(prev => [...prev, { data, format }]);
    };

    on(Events.Scanner.CodeScanned, handleCodeScanned);

    // Cleanup: use off() with same handler reference
    return () => off(Events.Scanner.CodeScanned, handleCodeScanned);
  }, []);

  const startScan = () => {
    scanner.scan()
      .prompt('Scan barcode')
      .formats(['qr', 'ean13', 'code128'])
      .continuous(true)
      .scan();
  };

  return (
    <div>
      <button onClick={startScan}>Start Scanning</button>
      <ul>
        {scannedData.map((item, i) => (
          <li key={i}>{item.format}: {item.data}</li>
        ))}
      </ul>
    </div>
  );
}

export default QRScanner;
```

## Inertia.js Example

When using Inertia with Vue/React, EDGE components (TopBar, BottomNav, etc.) go in your `app.blade.php` layout file, not in Vue components.

**resources/views/app.blade.php:**
```blade
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
    @vite(['resources/js/app.js'])
    @inertiaHead
</head>
<body class="nativephp-safe-area">
    {{-- EDGE components go here in the Blade layout --}}
    <native:top-bar title="My App" />

    @inertia

    <native:bottom-nav>
        <native:bottom-nav-item id="home" icon="home" label="Home" :url="route('home')" />
        <native:bottom-nav-item id="profile" icon="person" label="Profile" :url="route('profile')" />
    </native:bottom-nav>
</body>
</html>
```

**Vue Component (resources/js/Pages/SecureForm.vue):**
```vue
<template>
  <main class="p-4">
    <button @click="authenticateAndSubmit">Submit Securely</button>
  </main>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue';
import { router } from '@inertiajs/vue3';
import { biometrics, Events, on, off } from '#nativephp';

const formData = { /* your form data */ };

const authenticateAndSubmit = () => {
  biometrics.prompt().id('form-submit').prompt();
};

const handleBiometricCompleted = (success, id) => {
  if (success && id === 'form-submit') {
    router.post('/submit-form', formData);
  }
};

onMounted(() => {
  on(Events.Biometric.Completed, handleBiometricCompleted);
});

onUnmounted(() => {
  off(Events.Biometric.Completed, handleBiometricCompleted);
});
</script>
```

## Safe Area in JavaScript Apps

Apply safe area handling:

```html
<body class="nativephp-safe-area">
  <div id="app"></div>
</body>
```

Or use CSS variables:

```css
.my-header {
  padding-top: calc(16px + var(--inset-top));
}

.my-footer {
  padding-bottom: calc(16px + var(--inset-bottom));
}
```

## TypeScript Support

The library is fully typed:

```typescript
import { camera, Events, on, PhotoTakenEvent } from '#nativephp';

const handlePhoto = (path: string, mimeType: string, id: string | null) => {
  // Fully typed parameters
};

on(Events.Camera.PhotoTaken, handlePhoto);
```

## Best Practices

1. **Clean up event listeners with `off()`** - Always use `off()` with the same handler reference in component cleanup:
   ```javascript
   // Vue
   onMounted(() => on(Events.Camera.PhotoTaken, handlePhoto));
   onUnmounted(() => off(Events.Camera.PhotoTaken, handlePhoto));

   // React
   useEffect(() => {
     const handler = (path) => setPhoto(path);
     on(Events.Camera.PhotoTaken, handler);
     return () => off(Events.Camera.PhotoTaken, handler);
   }, []);
   ```

2. **Use IDs for tracking** - Correlate requests with responses when multiple operations may be in flight

3. **Builders are thenable** - All Pending* builders can be awaited directly without calling `.start()`, `.scan()`, etc:
   ```javascript
   // Both work:
   await camera.getPhoto().id('test').start();  // Explicit
   await camera.getPhoto().id('test');          // Implicit (thenable)
   ```

4. **Check for mobile context** - Use `system.isMobile()` before calling native APIs

5. **Graceful degradation** - Provide fallbacks for web-only testing

6. **EDGE components in Blade** - When using Inertia/Vue/React, EDGE components (TopBar, BottomNav, etc.) must go in `app.blade.php`, not in JS components

## Fetching Live Documentation

For detailed JavaScript integration:

- **Native Functions**: `https://nativephp.com/docs/mobile/2/the-basics/native-functions`
- **Events**: `https://nativephp.com/docs/mobile/2/the-basics/events`

Use WebFetch to retrieve the latest JavaScript patterns and API details.
