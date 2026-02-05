---
name: NativePHP Events
description: This skill should be used when the user asks about "nativephp event", "native event handling", "OnNative attribute", "listen for native events", "PhotoTaken event", "event dispatching", "livewire native event", "javascript native event", "custom event class", or needs to handle responses from native device functionality.
version: 0.1.0
---

# NativePHP Events

This skill provides guidance for handling events dispatched from native device functionality to your Laravel application.

## Overview

NativePHP uses an event system to handle asynchronous native operations. When a user takes a photo, scans a QR code, or completes biometric authentication, native code dispatches events that your application can listen for.

## Synchronous vs Asynchronous Operations

**Synchronous** - Execute immediately, no event needed:
- `Haptics::vibrate()`
- `Device::flashlight()`
- `Dialog::toast('Hello!')`
- `SecureStorage::set()` / `get()` / `delete()`
- `System::isIos()` / `isAndroid()`

**Asynchronous** - Trigger native UI, dispatch event on completion:
- `Camera::getPhoto()` → `PhotoTaken` / `PhotoCancelled`
- `Camera::recordVideo()` → `VideoRecorded` / `VideoCancelled`
- `Camera::pickImages()` → `MediaSelected`
- `Scanner::scan()` → `CodeScanned`
- `Biometrics::prompt()` → `Completed`
- `Geolocation::getCurrentPosition()` → `LocationReceived`
- `Microphone::record()` → `MicrophoneRecorded` / `MicrophoneCancelled`
- `Dialog::alert()` → `ButtonPressed`
- `PushNotifications::enroll()` → `TokenGenerated`

## Event Dispatching Pattern

Native code (Kotlin/Swift) dispatches events via JavaScript injection to the WebView:

```javascript
window.Livewire.dispatch('native:Native\\Mobile\\Events\\Camera\\PhotoTaken', payload)
```

Events are broadcast to both frontend (Livewire/JavaScript) and backend (Laravel listeners).

## Listening in Livewire Components

### Using #[OnNative] Attribute (REQUIRED)

NativePHP provides a custom `#[OnNative]` attribute that MUST be used for listening to native events. This attribute automatically handles the `native:` prefix and event class resolution.

```php
use Livewire\Component;
use Native\Mobile\Attributes\OnNative;
use Native\Mobile\Events\Camera\PhotoTaken;
use Native\Mobile\Events\Camera\PhotoCancelled;

class PhotoUploader extends Component
{
    #[OnNative(PhotoTaken::class)]
    public function handlePhotoTaken(string $path, string $mimeType = 'image/jpeg', ?string $id = null)
    {
        // Handle the photo
        $this->photoPath = $path;
    }

    #[OnNative(PhotoCancelled::class)]
    public function handlePhotoCancelled(bool $cancelled = true, ?string $id = null)
    {
        // Handle cancellation
    }
}
```

**IMPORTANT**: Always use `#[OnNative(EventClass::class)]` - NEVER use the raw `#[On('native:...')]` syntax. The `OnNative` attribute from `Native\Mobile\Attributes\OnNative` is the required pattern for NativePHP applications.

## All Available Events

### Camera Events

**PhotoTaken** - `Native\Mobile\Events\Camera\PhotoTaken`
```php
public string $path;
public string $mimeType = 'image/jpeg';
public ?string $id;
```

**PhotoCancelled** - `Native\Mobile\Events\Camera\PhotoCancelled`
```php
public bool $cancelled = true;
public ?string $id;
```

**VideoRecorded** - `Native\Mobile\Events\Camera\VideoRecorded`
```php
public string $path;
public string $mimeType = 'video/mp4';
public ?string $id;
```

**VideoCancelled** - `Native\Mobile\Events\Camera\VideoCancelled`
```php
public bool $cancelled = true;
public ?string $id;
```

### Gallery Events

**MediaSelected** - `Native\Mobile\Events\Gallery\MediaSelected`
```php
public bool $success;
public array $files = [];
public int $count = 0;
public ?string $error;
public bool $cancelled = false;
public ?string $id;
```

### Scanner Events

**CodeScanned** - `Native\Mobile\Events\Scanner\CodeScanned`
```php
public string $data;
public string $format;
public ?string $id;
```

### Biometric Events

**Completed** - `Native\Mobile\Events\Biometric\Completed`
```php
public bool $success;
public ?string $id;
```

### Dialog Events

**ButtonPressed** - `Native\Mobile\Events\Alert\ButtonPressed`
```php
public int $index;
public string $label;
public ?string $id;
```

### Microphone Events

**MicrophoneRecorded** - `Native\Mobile\Events\Microphone\MicrophoneRecorded`
```php
public string $path;
public string $mimeType = 'audio/m4a';
public ?string $id;
```

**MicrophoneCancelled** - `Native\Mobile\Events\Microphone\MicrophoneCancelled`
```php
public bool $cancelled = true;
public ?string $id;
```

### Geolocation Events

**LocationReceived** - `Native\Mobile\Events\Geolocation\LocationReceived`
```php
public bool $success;
public ?float $latitude;
public ?float $longitude;
public ?float $accuracy;
public ?int $timestamp;
public ?string $provider;
public ?string $error;
public ?string $id;
```

**PermissionStatusReceived** - `Native\Mobile\Events\Geolocation\PermissionStatusReceived`
```php
public string $location;
public string $coarseLocation;
public string $fineLocation;
public ?string $id;
```

**PermissionRequestResult** - `Native\Mobile\Events\Geolocation\PermissionRequestResult`
```php
public string $location;
public string $coarseLocation;
public string $fineLocation;
public ?string $error;
public ?string $id;
```

### Push Notification Events

**TokenGenerated** - `Native\Mobile\Events\PushNotification\TokenGenerated`
```php
public string $token;
public ?string $id;
```

### App Events

**UpdateInstalled** - `Native\Mobile\Events\App\UpdateInstalled`
```php
public string $version;
public int $timestamp;
```

## Custom Event Classes

Create custom events by extending built-in events:

```php
namespace App\Events;

use Native\Mobile\Events\Camera\PhotoTaken;

class ProfilePhotoTaken extends PhotoTaken
{
    // Add custom properties or methods
}
```

Use with fluent API:

```php
Camera::getPhoto()
    ->id('profile')
    ->event(ProfilePhotoTaken::class)
    ->start();
```

Listen for custom event:

```php
#[OnNative(ProfilePhotoTaken::class)]
public function handleProfilePhoto(string $path)
{
    // Handle profile photo specifically
}
```

## Tracking Requests with IDs

Use IDs to correlate requests with responses:

```php
// In your component
public function takePhoto()
{
    Camera::getPhoto()
        ->id('avatar-' . auth()->id())
        ->remember()
        ->start();
}

#[OnNative(PhotoTaken::class)]
public function handlePhoto(string $path, string $mimeType, ?string $id)
{
    if ($id === 'avatar-' . auth()->id()) {
        // This is the avatar photo
    }
}

// Or retrieve last ID from session
$lastId = Camera::getPhoto()->lastId();
```

## Backend Event Listeners

Listen in Laravel using standard listeners:

```php
// app/Listeners/ProcessPhotoUpload.php
namespace App\Listeners;

use Native\Mobile\Events\Camera\PhotoTaken;

class ProcessPhotoUpload
{
    public function handle(PhotoTaken $event): void
    {
        // Process the photo on the backend
        Storage::disk('s3')->put('photos/' . basename($event->path),
            file_get_contents($event->path));
    }
}
```

Register in `EventServiceProvider`:

```php
protected $listen = [
    PhotoTaken::class => [
        ProcessPhotoUpload::class,
    ],
];
```

## Event Class Structure

All events are simple POJOs (Plain Old Java Objects pattern):
- Use `Dispatchable` and `SerializesModels` traits
- Do NOT implement `ShouldBroadcast`
- Do NOT use broadcasting channels
- Properties are public for direct access

```php
namespace Native\Mobile\Events\Camera;

use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class PhotoTaken
{
    use Dispatchable, SerializesModels;

    public function __construct(
        public string $path,
        public string $mimeType = 'image/jpeg',
        public ?string $id = null
    ) {}
}
```

## Fetching Live Documentation

For detailed event documentation:

- **Events Overview**: `https://nativephp.com/docs/mobile/2/the-basics/events`

Use WebFetch to retrieve the latest event handling patterns.