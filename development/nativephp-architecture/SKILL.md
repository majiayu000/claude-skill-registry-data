---
name: NativePHP Architecture
description: This skill provides understanding of NativePHP Mobile internals. Use when the user asks about "how NativePHP works", "god method", "nativephp_call", "bridge functions", "bridge registration", "EDGE system", "element definition", "native events", "event dispatching", "WebView communication", or how PHP communicates with native iOS/Android code.
version: 1.0.0
---

# NativePHP Mobile Architecture

NativePHP Mobile enables Laravel developers to build native iOS and Android applications. This skill explains the core architecture.

## The God Method: `nativephp_call`

The foundation of NativePHP's native communication is the "god method" - `nativephp_call`. This single function handles ALL PHP-to-native communication.

### How It Works

```php
// PHP side - calling native functionality
$result = nativephp_call('Dialog.Alert', [
    'title' => 'Hello',
    'message' => 'Welcome to NativePHP!'
]);
```

The call flows through:
1. **PHP** calls `nativephp_call('Method.Name', $params)`
2. **JavaScript bridge** receives the call in the WebView
3. **Native code** (Kotlin/Swift) executes the registered bridge function
4. **Result** flows back through the same path

### Bridge Function Registration

Native bridge functions must be registered before they can be called. Registration maps method names to implementation classes.

**Android (Kotlin):**
```kotlin
fun registerBridgeFunctions(activity: FragmentActivity, context: Context) {
    val registry = BridgeFunctionRegistry.shared

    // Core NativePHP functions
    registry.register("Dialog.Alert", DialogFunctions.Alert(activity))
    registry.register("QrCode.Scan", QrCodeFunctions.Scan(activity))
    registry.register("Network.Status", NetworkFunctions.Status(context))

    // Plugin functions get registered here too
    registry.register("MyPlugin.Execute", MyPluginFunctions.Execute(activity))
}
```

**iOS (Swift):**
```swift
func registerBridgeFunctions() {
    let registry = BridgeFunctionRegistry.shared

    registry.register("Dialog.Alert", DialogFunctions.Alert())
    registry.register("QrCode.Scan", QrCodeFunctions.Scan())
    registry.register("Network.Status", NetworkFunctions.Status())

    // Plugin functions
    registry.register("MyPlugin.Execute", MyPluginFunctions.Execute())
}
```

### Method Naming Convention

Bridge function names follow `Namespace.Action` pattern:
- `Dialog.Alert` - Show an alert dialog
- `Camera.Capture` - Capture a photo
- `Haptics.Vibrate` - Trigger haptic feedback
- `MyPlugin.DoSomething` - Plugin-specific action

## EDGE: Element Definition and Generation Engine

EDGE is NativePHP's system for rendering native UI elements from PHP/Blade templates. Instead of rendering HTML, EDGE creates native iOS/Android UI.

### How EDGE Works

1. **Blade components** define native UI elements
2. **JSON representation** is passed via HTTP headers
3. **Native renderers** create actual native views

```php
// In a Blade template
<x-native::bottom-nav>
    <x-native::bottom-nav-item
        icon="home"
        label="Home"
        route="home"
    />
    <x-native::bottom-nav-item
        icon="settings"
        label="Settings"
        route="settings"
    />
</x-native::bottom-nav>
```

This generates a JSON structure that native code interprets to render a real native bottom navigation bar.

### EDGE vs WebView

| Aspect | EDGE (Native) | WebView |
|--------|---------------|---------|
| Rendering | Native UIKit/Jetpack | HTML/CSS |
| Performance | Native speed | Web performance |
| Look & Feel | Platform native | Web-like |
| Use Case | Navigation, tabs, dialogs | App content |

## Event Dispatching: Native to PHP

When native code needs to notify PHP (e.g., photo captured, scan completed), it dispatches events.

### The Flow

1. Native code completes an operation
2. Native dispatches event via JavaScript injection
3. Livewire/Alpine receives the event
4. PHP component handles the event

### Android Event Dispatching

```kotlin
import android.os.Handler
import android.os.Looper
import org.json.JSONObject

// MUST dispatch on main thread for JavaScript execution
Handler(Looper.getMainLooper()).post {
    val payload = JSONObject().apply {
        put("path", filePath)
        put("mimeType", "image/jpeg")
    }
    NativeActionCoordinator.dispatchEvent(
        activity,
        "Native\\Mobile\\Events\\Camera\\PhotoCaptured",
        payload.toString()
    )
}
```

### iOS Event Dispatching

```swift
// Already on main thread typically
let payload: [String: Any] = [
    "path": filePath,
    "mimeType": "image/jpeg"
]
LaravelBridge.shared.send?(
    "Native\\Mobile\\Events\\Camera\\PhotoCaptured",
    payload
)
```

### PHP Event Handling

```php
// Event class - simple POJO, no broadcasting
class PhotoCaptured
{
    use Dispatchable, SerializesModels;

    public function __construct(
        public string $path,
        public string $mimeType = 'image/jpeg'
    ) {}
}

// Livewire component listening for the event
class PhotoUploader extends Component
{
    #[On('native:Native\Mobile\Events\Camera\PhotoCaptured')]
    public function handlePhotoCaptured($path, $mimeType = null)
    {
        // Process the captured photo
        $this->photoPath = $path;
    }
}
```

### Critical Rules for Events

1. **Events dispatch via JavaScript injection** - NOT Laravel's event system
2. **Event classes are simple POJOs** - No `ShouldBroadcast`, no channels
3. **Main thread required** - JavaScript injection must run on UI thread
4. **Livewire listens with `#[On('native:...')]`** - The `native:` prefix is required

## WebView Architecture

NativePHP apps run inside a WebView that loads PHP-rendered HTML:

```
┌─────────────────────────────────────┐
│           Native App Shell          │
│  ┌───────────────────────────────┐  │
│  │     EDGE Native Elements      │  │
│  │  (Bottom Nav, Status Bar)     │  │
│  ├───────────────────────────────┤  │
│  │                               │  │
│  │         WebView               │  │
│  │   (PHP/Laravel Content)       │  │
│  │                               │  │
│  │   ┌─────────────────────┐    │  │
│  │   │   JavaScript Bridge  │    │  │
│  │   │   (nativephp_call)   │    │  │
│  │   └─────────────────────┘    │  │
│  │                               │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │   Bridge Function Registry    │  │
│  │   (Native Kotlin/Swift)       │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

## PHP Binaries

During NativePHP installation, PHP binaries are downloaded that contain:
- Compiled PHP runtime for iOS/Android
- All function definitions including `nativephp_call`
- Native bridge interface code

These binaries are platform-specific and handle the low-level communication between PHP and native code.

## Key Concepts Summary

| Concept | Purpose |
|---------|---------|
| `nativephp_call` | PHP function to invoke native code |
| Bridge Functions | Native classes that handle `nativephp_call` requests |
| Bridge Registry | Maps method names to bridge function classes |
| EDGE | Native UI rendering from Blade components |
| Event Dispatching | Native-to-PHP communication via JavaScript injection |
| WebView | Container for PHP-rendered content |

## Common Patterns

### Synchronous Call (returns immediately)
```php
$status = nativephp_call('Network.Status', []);
// Returns: ['connected' => true, 'type' => 'wifi']
```

### Asynchronous Operation (returns ID, dispatches event when done)
```php
$result = nativephp_call('Camera.Capture', ['quality' => 80]);
// Returns: ['id' => 'uuid-here']
// Later: native:Native\Mobile\Events\Camera\PhotoCaptured event fires
```

### Fire-and-Forget
```php
nativephp_call('Haptics.Vibrate', ['pattern' => 'success']);
// Returns: ['success' => true]
// No follow-up event
```