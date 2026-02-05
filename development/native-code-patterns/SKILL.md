---
name: Native Code Patterns
description: This skill provides Kotlin and Swift code patterns for NativePHP plugins. Use when the user asks about "bridge function pattern", "kotlin bridge", "swift bridge", "BridgeFunction class", "BridgeResponse", "execute method", "parameter extraction", "dispatch event", "NativeActionCoordinator", "LaravelBridge", "Activity pattern", "ViewController pattern", threading in native code, or how to write native code for NativePHP plugins.
version: 1.0.0
---

# Native Code Patterns for NativePHP Plugins

This skill provides complete, production-ready patterns for Kotlin (Android) and Swift (iOS) bridge functions in NativePHP plugins.

---

## CRITICAL: BridgeResponse Helper

**BridgeResponse is a REAL helper object that EXISTS in NativePHP and MUST be used.**

Do NOT write code that returns plain `Map<String, Any>` or `[String: Any]` directly. Always use:

### Kotlin
```kotlin
import com.nativephp.mobile.bridge.BridgeResponse
import com.nativephp.mobile.bridge.BridgeError

// Success
return BridgeResponse.success(mapOf("key" to "value"))

// Error (always use BridgeError with code and message)
return BridgeResponse.error(BridgeError("ERROR_CODE", "Error message"))
```

**IMPORTANT: Android BridgeResponse.error requires a `BridgeError` object with both `code` and `message` parameters.**

### Swift
```swift
// Success
return BridgeResponse.success(data: ["key": "value"])

// Error (always include code and message)
return BridgeResponse.error(code: "ERROR_CODE", message: "Error message")
```

**IMPORTANT: iOS BridgeResponse.error ALWAYS requires both `code` and `message` parameters.**

**BridgeResponse is defined in:**
- Android: `com.nativephp.mobile.bridge.BridgeResponse` (BridgeResponse object)
- iOS: Built into the NativePHP bridge

**The official NativePHP plugin stubs use BridgeResponse. Follow this pattern.**

---

## Kotlin Bridge Function Pattern

### Basic Template

```kotlin
package com.myvendor.plugins.myplugin

import androidx.fragment.app.FragmentActivity
import android.content.Context
import com.nativephp.mobile.bridge.BridgeFunction
import com.nativephp.mobile.bridge.BridgeResponse
import com.nativephp.mobile.bridge.BridgeError

object MyPluginFunctions {

    /**
     * Brief description of what this function does.
     *
     * Parameters:
     * - paramName: Type - Description
     *
     * Returns:
     * - resultKey: Type - Description
     */
    class Execute(private val activity: FragmentActivity) : BridgeFunction {
        override fun execute(parameters: Map<String, Any>): Map<String, Any> {
            // 1. Extract and validate parameters
            val param1 = parameters["param1"] as? String
                ?: return BridgeResponse.error(BridgeError("INVALID_PARAMETERS", "param1 is required"))

            // 2. Perform the native operation
            try {
                val result = performOperation(param1)

                // 3. Return success response
                return BridgeResponse.success(mapOf(
                    "result" to result
                ))
            } catch (e: Exception) {
                return BridgeResponse.error(BridgeError("OPERATION_FAILED", e.message ?: "Unknown error"))
            }
        }

        private fun performOperation(param: String): String {
            // Implementation
            return "processed: $param"
        }
    }

    // All bridge functions use FragmentActivity - get context from it if needed
    class GetStatus(private val activity: FragmentActivity) : BridgeFunction {
        override fun execute(parameters: Map<String, Any>): Map<String, Any> {
            // If you need context: val context: Context = activity
            return BridgeResponse.success(mapOf(
                "status" to "ready",
                "version" to "1.0.0"
            ))
        }
    }
}
```

### Package Naming

Use your own vendor-namespaced package for your plugin code:

```kotlin
package com.myvendor.plugins.myplugin
```

Where `myvendor` is your vendor name and `myplugin` is your plugin name (lowercase, no hyphens - use underscores if needed). The `plugins` segment groups all your plugins together. This keeps your plugin code isolated from other plugins.

### Constructor Parameters - ALWAYS Use FragmentActivity

**Use `FragmentActivity` for ALL bridge functions.** The NativePHP bridge registration passes `activity` to all functions. You can always get `Context` from `activity`:

```kotlin
// CORRECT - works with the bridge registration
class MyFunction(private val activity: FragmentActivity) : BridgeFunction {
    override fun execute(parameters: Map<String, Any>): Map<String, Any> {
        // Get context when needed
        val context: Context = activity
        val prefs = context.getSharedPreferences("my_prefs", Context.MODE_PRIVATE)
        // ...
    }
}
```

**Do NOT use `Context` as constructor parameter** - the bridge registers functions with `activity`, not `context`.

### Parameter Extraction Patterns

```kotlin
// Required string
val name = parameters["name"] as? String
    ?: return BridgeResponse.error(BridgeError("INVALID_PARAMETERS", "name is required"))

// Required number (always comes as Number)
val count = (parameters["count"] as? Number)?.toInt()
    ?: return BridgeResponse.error(BridgeError("INVALID_PARAMETERS", "count is required"))

// Optional with default
val quality = (parameters["quality"] as? Number)?.toInt() ?: 80
val enabled = parameters["enabled"] as? Boolean ?: false

// Double/Float
val amount = (parameters["amount"] as? Number)?.toDouble() ?: 0.0

// Arrays/Lists
val items = (parameters["items"] as? List<*>)?.filterIsInstance<String>() ?: emptyList()
val numbers = (parameters["numbers"] as? List<*>)?.mapNotNull { (it as? Number)?.toInt() } ?: emptyList()

// Nested objects
val config = parameters["config"] as? Map<*, *>
val configValue = config?.get("key") as? String ?: "default"
```

### Response Patterns

```kotlin
// Success with data
return BridgeResponse.success(mapOf(
    "path" to filePath,
    "size" to fileSize,
    "metadata" to mapOf(
        "width" to width,
        "height" to height
    )
))

// Success with array
return BridgeResponse.success(mapOf(
    "items" to listOf(
        mapOf("id" to 1, "name" to "Item 1"),
        mapOf("id" to 2, "name" to "Item 2")
    )
))

// Error (always use BridgeError with code and message)
return BridgeResponse.error(BridgeError("OPERATION_FAILED", "Something went wrong"))

// Error with specific code
return BridgeResponse.error(BridgeError("FILE_NOT_FOUND", "The specified file does not exist"))
```

### Event Dispatching (Kotlin)

Events notify PHP when async operations complete:

```kotlin
import android.os.Handler
import android.os.Looper
import org.json.JSONObject
import com.nativephp.mobile.NativeActionCoordinator

// MUST dispatch on main thread for JavaScript execution
Handler(Looper.getMainLooper()).post {
    val payload = JSONObject().apply {
        put("path", filePath)
        put("mimeType", mimeType)
        put("id", operationId)
    }
    NativeActionCoordinator.dispatchEvent(
        activity,
        "Vendor\\MyPlugin\\Events\\OperationCompleted",
        payload.toString()
    )
}
```

### Async Operations (Kotlin)

For long-running operations, return immediately and dispatch event when done:

```kotlin
import kotlinx.coroutines.*
import java.util.UUID

class AsyncOperation(private val activity: FragmentActivity) : BridgeFunction {
    override fun execute(parameters: Map<String, Any>): Map<String, Any> {
        val id = UUID.randomUUID().toString()

        CoroutineScope(Dispatchers.IO).launch {
            try {
                val result = performLongOperation()

                // Dispatch event on main thread
                withContext(Dispatchers.Main) {
                    val payload = JSONObject().apply {
                        put("id", id)
                        put("result", result)
                        put("success", true)
                    }
                    NativeActionCoordinator.dispatchEvent(
                        activity,
                        "Vendor\\MyPlugin\\Events\\OperationCompleted",
                        payload.toString()
                    )
                }
            } catch (e: Exception) {
                withContext(Dispatchers.Main) {
                    val payload = JSONObject().apply {
                        put("id", id)
                        put("error", e.message)
                        put("success", false)
                    }
                    NativeActionCoordinator.dispatchEvent(
                        activity,
                        "Vendor\\MyPlugin\\Events\\OperationFailed",
                        payload.toString()
                    )
                }
            }
        }

        // Return immediately with tracking ID
        return BridgeResponse.success(mapOf("id" to id))
    }

    private suspend fun performLongOperation(): String {
        delay(1000) // Simulate work
        return "completed"
    }
}
```

### Launching an Activity (Kotlin)

For camera, scanners, complex UI:

```kotlin
import android.content.Intent

class OpenScanner(private val activity: FragmentActivity) : BridgeFunction {
    override fun execute(parameters: Map<String, Any>): Map<String, Any> {
        val config = parameters["config"] as? String

        val intent = Intent(activity, ScannerActivity::class.java).apply {
            putExtra("config", config)
        }
        activity.startActivity(intent)

        return BridgeResponse.success(mapOf("launched" to true))
    }
}
```

The Activity dispatches events when done:

```kotlin
class ScannerActivity : AppCompatActivity() {
    private fun onScanComplete(result: String) {
        Handler(Looper.getMainLooper()).post {
            val payload = JSONObject().apply {
                put("result", result)
            }
            NativeActionCoordinator.dispatchEvent(
                this,
                "Vendor\\MyPlugin\\Events\\ScanCompleted",
                payload.toString()
            )
        }
        finish()
    }
}
```

### Permission Checking (Kotlin)

```kotlin
import android.Manifest
import android.content.pm.PackageManager
import androidx.core.content.ContextCompat

class RequiresCamera(private val activity: FragmentActivity) : BridgeFunction {
    override fun execute(parameters: Map<String, Any>): Map<String, Any> {
        if (ContextCompat.checkSelfPermission(activity, Manifest.permission.CAMERA)
            != PackageManager.PERMISSION_GRANTED) {
            return BridgeResponse.error(BridgeError("PERMISSION_DENIED", "Camera permission required"))
        }

        // Proceed with camera operation
        return performCameraOperation()
    }
}
```

---

## Swift Bridge Function Pattern

### Basic Template

```swift
import Foundation

enum MyPluginFunctions {

    /// Brief description of what this function does.
    ///
    /// - Parameters:
    ///   - paramName: Description of parameter
    ///
    /// - Returns: Dictionary containing:
    ///   - resultKey: Description of return value
    class Execute: BridgeFunction {
        func execute(parameters: [String: Any]) throws -> [String: Any] {
            // 1. Extract and validate parameters
            guard let param1 = parameters["param1"] as? String else {
                return BridgeResponse.error(code: "INVALID_PARAMETERS", message: "param1 is required")
            }

            // 2. Perform the native operation
            do {
                let result = try performOperation(param1)

                // 3. Return success response
                return BridgeResponse.success(data: [
                    "result": result
                ])
            } catch {
                return BridgeResponse.error(code: "OPERATION_FAILED", message: error.localizedDescription)
            }
        }

        private func performOperation(_ param: String) throws -> String {
            return "processed: \(param)"
        }
    }

    class GetStatus: BridgeFunction {
        func execute(parameters: [String: Any]) throws -> [String: Any] {
            return BridgeResponse.success(data: [
                "status": "ready",
                "version": "1.0.0"
            ])
        }
    }
}
```

### File Structure

- One `{Namespace}Functions.swift` file per plugin
- Use `enum` as namespace container (prevents instantiation)
- Each bridge function is a `class` inside the enum

### Parameter Extraction Patterns

```swift
// Required string
guard let name = parameters["name"] as? String else {
    return BridgeResponse.error(code: "INVALID_PARAMETERS", message: "name is required")
}

// Required number
guard let count = parameters["count"] as? Int else {
    return BridgeResponse.error(code: "INVALID_PARAMETERS", message: "count is required")
}

// Optional with default
let quality = parameters["quality"] as? Int ?? 80
let enabled = parameters["enabled"] as? Bool ?? false

// Double/Float
let amount = parameters["amount"] as? Double ?? 0.0

// Arrays
let items = parameters["items"] as? [String] ?? []
let numbers = parameters["numbers"] as? [Int] ?? []

// Nested dictionary
if let config = parameters["config"] as? [String: Any],
   let configValue = config["key"] as? String {
    // Use configValue
}

// Array of dictionaries
let people = parameters["people"] as? [[String: Any]] ?? []
for person in people {
    if let name = person["name"] as? String,
       let age = person["age"] as? Int {
        // Process person
    }
}
```

### Response Patterns

```swift
// Success with data
return BridgeResponse.success(data: [
    "path": filePath,
    "size": fileSize,
    "metadata": [
        "width": width,
        "height": height
    ]
])

// Success with array
return BridgeResponse.success(data: [
    "items": [
        ["id": 1, "name": "Item 1"],
        ["id": 2, "name": "Item 2"]
    ]
])

// Error (always include code and message)
return BridgeResponse.error(code: "OPERATION_FAILED", message: "Something went wrong")

// Error with specific code
return BridgeResponse.error(code: "FILE_NOT_FOUND", message: "The specified file does not exist")
```

### Event Dispatching (Swift)

```swift
// Dispatch on main thread (usually already there)
DispatchQueue.main.async {
    let payload: [String: Any] = [
        "path": filePath,
        "mimeType": mimeType,
        "id": operationId
    ]
    LaravelBridge.shared.send?(
        "Vendor\\MyPlugin\\Events\\OperationCompleted",
        payload
    )
}
```

### Async Operations (Swift)

```swift
class AsyncOperation: BridgeFunction {
    func execute(parameters: [String: Any]) throws -> [String: Any] {
        let id = UUID().uuidString

        // Dispatch to background
        DispatchQueue.global(qos: .userInitiated).async {
            do {
                let result = self.performLongOperation()

                // Dispatch event back on main thread
                DispatchQueue.main.async {
                    LaravelBridge.shared.send?(
                        "Vendor\\MyPlugin\\Events\\OperationCompleted",
                        [
                            "id": id,
                            "result": result,
                            "success": true
                        ]
                    )
                }
            } catch {
                DispatchQueue.main.async {
                    LaravelBridge.shared.send?(
                        "Vendor\\MyPlugin\\Events\\OperationFailed",
                        [
                            "id": id,
                            "error": error.localizedDescription,
                            "success": false
                        ]
                    )
                }
            }
        }

        // Return immediately with tracking ID
        return BridgeResponse.success(data: ["id": id])
    }

    private func performLongOperation() -> String {
        Thread.sleep(forTimeInterval: 1.0) // Simulate work
        return "completed"
    }
}

// Modern Swift concurrency version
class ModernAsyncOperation: BridgeFunction {
    func execute(parameters: [String: Any]) throws -> [String: Any] {
        let id = UUID().uuidString

        Task {
            let result = await performAsyncWork()

            await MainActor.run {
                LaravelBridge.shared.send?(
                    "Vendor\\MyPlugin\\Events\\OperationCompleted",
                    ["id": id, "result": result]
                )
            }
        }

        return BridgeResponse.success(data: ["id": id])
    }

    private func performAsyncWork() async -> String {
        try? await Task.sleep(nanoseconds: 1_000_000_000)
        return "completed"
    }
}
```

### Presenting a ViewController (Swift)

```swift
import UIKit

class OpenScanner: BridgeFunction {
    func execute(parameters: [String: Any]) throws -> [String: Any] {
        // Get the key window's root view controller
        guard let windowScene = UIApplication.shared.connectedScenes.first as? UIWindowScene,
              let rootVC = windowScene.windows.first?.rootViewController else {
            return BridgeResponse.error(code: "VIEW_CONTROLLER_ERROR", message: "Cannot present view controller")
        }

        // Find the topmost presented controller
        var topVC = rootVC
        while let presented = topVC.presentedViewController {
            topVC = presented
        }

        // Create and present your view controller
        let scannerVC = ScannerViewController()
        scannerVC.modalPresentationStyle = .fullScreen

        DispatchQueue.main.async {
            topVC.present(scannerVC, animated: true)
        }

        return BridgeResponse.success(data: ["presented": true])
    }
}

class ScannerViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
    }

    private func onScanComplete(result: String) {
        dismiss(animated: true) {
            LaravelBridge.shared.send?(
                "Vendor\\MyPlugin\\Events\\ScanCompleted",
                ["result": result]
            )
        }
    }
}
```

### Permission Handling (Swift)

```swift
import AVFoundation

class RequiresCamera: BridgeFunction {
    func execute(parameters: [String: Any]) throws -> [String: Any] {
        let status = AVCaptureDevice.authorizationStatus(for: .video)

        switch status {
        case .authorized:
            return performCameraOperation()

        case .notDetermined:
            // Request permission asynchronously
            AVCaptureDevice.requestAccess(for: .video) { granted in
                DispatchQueue.main.async {
                    LaravelBridge.shared.send?(
                        "Vendor\\MyPlugin\\Events\\PermissionResult",
                        ["granted": granted, "permission": "camera"]
                    )
                }
            }
            return BridgeResponse.success(data: ["pending": true])

        case .denied, .restricted:
            return BridgeResponse.error(
                code: "PERMISSION_DENIED",
                message: "Camera permission denied. Please enable in Settings."
            )

        @unknown default:
            return BridgeResponse.error(code: "UNKNOWN_STATUS", message: "Unknown permission status")
        }
    }
}
```

---

## Common Patterns for Both Platforms

### Synchronous vs Asynchronous

**Synchronous** (returns data immediately):
```php
$status = nativephp_call('MyPlugin.GetStatus', []);
// Returns: ['status' => 'ready']
```

**Asynchronous** (returns ID, dispatches event later):
```php
$result = nativephp_call('MyPlugin.StartLongOperation', ['data' => $data]);
// Returns: ['id' => 'uuid-here']
// Later: native:Vendor\MyPlugin\Events\OperationCompleted fires
```

### Error Handling Best Practices

1. **Validate all required parameters** at the start
2. **Use try-catch** around operations that can fail
3. **Return meaningful error codes** for programmatic handling
4. **Include helpful error messages** for debugging
5. **Never throw exceptions** from bridge functions - always return error responses

### Threading Rules

**Android:**
- Bridge functions execute on main thread
- Use `Dispatchers.IO` for I/O operations
- Event dispatch MUST be on main thread: `Handler(Looper.getMainLooper()).post { }`

**iOS:**
- Bridge functions execute on main thread
- Use `DispatchQueue.global(qos: .userInitiated)` for background work
- Event dispatch should be on main thread: `DispatchQueue.main.async { }`

### File Paths

When returning file paths to PHP:

```kotlin
// Android
return BridgeResponse.success(mapOf(
    "path" to file.absolutePath  // Full path like /data/data/com.app/files/photo.jpg
))
```

```swift
// iOS
return BridgeResponse.success(data: [
    "path": fileURL.path  // Full path like /var/mobile/.../Documents/photo.jpg
])
```

PHP can then use these paths directly for file operations.

---

## Android Activity Lifecycle Events (NativePHPLifecycle Pattern)

Plugins that need to respond to Android Activity lifecycle events (FCM tokens, app state changes, deep links, etc.) should subscribe to NativePHP's `NativePHPLifecycle` event bus rather than modifying MainActivity directly.

### Available Events

MainActivity and PushNotificationService post these events that plugins can subscribe to:

| Event Name | Data | Description |
|------------|------|-------------|
| `didRegisterForRemoteNotifications` | `["token": String]` | FCM token received |
| `didFailToRegisterForRemoteNotifications` | `["error": String]` | FCM registration failed |
| `didReceiveRemoteNotification` | `["title", "body", "data": Map]` | Push notification received |
| `onResume` | none | Activity resumed (foreground) |
| `onPause` | none | Activity paused (background) |
| `onDestroy` | none | Activity destroyed |
| `onNewIntent` | `["url": String]` | Deep link received |
| `onPermissionResult` | `["permission", "granted", "requestCode"]` | Permission request result |

### Subscribing to Lifecycle Events (Kotlin)

Create a singleton that subscribes to the events it needs:

```kotlin
package com.myvendor.plugins.myplugin

import com.nativephp.mobile.lifecycle.NativePHPLifecycle

object MyPluginDelegate {
    private var initialized = false

    fun initialize() {
        if (initialized) return
        initialized = true

        // Subscribe to FCM token registration
        NativePHPLifecycle.on(NativePHPLifecycle.Events.DID_REGISTER_FOR_REMOTE_NOTIFICATIONS) { data ->
            val token = data["token"] as? String ?: return@on
            println("MyPluginDelegate: Received FCM token: $token")

            // Cache it, send to server, etc.
            // UserDefaults equivalent in Android
            // SharedPreferences.edit().putString("my_plugin_push_token", token).apply()
        }

        NativePHPLifecycle.on(NativePHPLifecycle.Events.DID_FAIL_TO_REGISTER_FOR_REMOTE_NOTIFICATIONS) { data ->
            val error = data["error"] as? String
            println("MyPluginDelegate: Failed to register: $error")
        }

        NativePHPLifecycle.on(NativePHPLifecycle.Events.ON_RESUME) { _ ->
            println("MyPluginDelegate: App resumed")
            // Refresh state, resume tasks, etc.
        }

        NativePHPLifecycle.on(NativePHPLifecycle.Events.ON_NEW_INTENT) { data ->
            val url = data["url"] as? String ?: return@on
            println("MyPluginDelegate: Deep link received: $url")
            // Handle OAuth callbacks, deep links, etc.
        }
    }
}
```

### Initializing the Delegate

Initialize the delegate in your first bridge function call:

```kotlin
object MyPluginFunctions {

    class Initialize(private val context: Context) : BridgeFunction {
        override fun execute(parameters: Map<String, Any>): Map<String, Any> {
            // Ensure delegate is initialized and listening
            MyPluginDelegate.initialize()

            return BridgeResponse.success(mapOf("initialized" to true))
        }
    }
}
```

### Why NativePHPLifecycle?

This pattern keeps MainActivity clean and generic:

1. **Decoupling**: Plugins don't modify MainActivity source code
2. **Multiple subscribers**: Multiple plugins can listen to the same events
3. **Thread-safe**: Callbacks run on the main thread automatically
4. **Easy testing**: Can post events in tests to simulate lifecycle events

### NativePHPLifecycle API

```kotlin
import com.nativephp.mobile.lifecycle.NativePHPLifecycle

// Subscribe to an event
val subscriptionId = NativePHPLifecycle.on("eventName") { data ->
    // Handle event
}

// Unsubscribe from an event
NativePHPLifecycle.off("eventName", callback)

// Remove all listeners for an event
NativePHPLifecycle.offAll("eventName")

// Check if there are listeners
val hasListeners = NativePHPLifecycle.hasListeners("eventName")

// Clear all listeners (cleanup)
NativePHPLifecycle.clear()

// Event name constants
NativePHPLifecycle.Events.DID_REGISTER_FOR_REMOTE_NOTIFICATIONS
NativePHPLifecycle.Events.DID_FAIL_TO_REGISTER_FOR_REMOTE_NOTIFICATIONS
NativePHPLifecycle.Events.DID_RECEIVE_REMOTE_NOTIFICATION
NativePHPLifecycle.Events.ON_RESUME
NativePHPLifecycle.Events.ON_PAUSE
NativePHPLifecycle.Events.ON_DESTROY
NativePHPLifecycle.Events.ON_NEW_INTENT
NativePHPLifecycle.Events.ON_PERMISSION_RESULT
```

---

## iOS AppDelegate Lifecycle Events (NotificationCenter Pattern)

Plugins that need to respond to iOS AppDelegate lifecycle events (push notification tokens, app state changes, etc.) should subscribe to NativePHP's NotificationCenter events rather than modifying AppDelegate directly.

### Available Notification Names

AppDelegate posts these notifications that plugins can subscribe to:

| Notification Name | userInfo | Description |
|-------------------|----------|-------------|
| `NativePHP.didRegisterForRemoteNotifications` | `["deviceToken": Data]` | APNS device token received |
| `NativePHP.didFailToRegisterForRemoteNotifications` | `["error": Error]` | APNS registration failed |
| `NativePHP.didReceiveRemoteNotification` | `["payload": [AnyHashable: Any]]` | Remote notification received |
| `NativePHP.didFinishLaunching` | `["launchOptions": [...]]` | App finished launching |
| `NativePHP.didBecomeActive` | none | App became active |
| `NativePHP.didEnterBackground` | none | App entered background |

### Subscribing to Lifecycle Events (Swift)

Create a singleton delegate class that subscribes to the notifications it needs:

```swift
import Foundation
import UIKit

/// Singleton that handles AppDelegate lifecycle events via NotificationCenter
class MyPluginDelegate: NSObject {
    static let shared = MyPluginDelegate()

    private override init() {
        super.init()
        setupNotificationObservers()
    }

    // MARK: - NotificationCenter Observers

    private func setupNotificationObservers() {
        // Subscribe to APNS token registration
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(handleDidRegisterForRemoteNotifications(_:)),
            name: Notification.Name("NativePHP.didRegisterForRemoteNotifications"),
            object: nil
        )

        NotificationCenter.default.addObserver(
            self,
            selector: #selector(handleDidFailToRegisterForRemoteNotifications(_:)),
            name: Notification.Name("NativePHP.didFailToRegisterForRemoteNotifications"),
            object: nil
        )

        NotificationCenter.default.addObserver(
            self,
            selector: #selector(handleDidBecomeActive(_:)),
            name: Notification.Name("NativePHP.didBecomeActive"),
            object: nil
        )
    }

    @objc private func handleDidRegisterForRemoteNotifications(_ notification: Notification) {
        guard let deviceToken = notification.userInfo?["deviceToken"] as? Data else { return }

        // Convert token to string
        let tokenString = deviceToken.map { String(format: "%02x", $0) }.joined()
        print("MyPluginDelegate: Received APNS token: \(tokenString)")

        // Cache it, send to server, etc.
        UserDefaults.standard.set(tokenString, forKey: "my_plugin_push_token")

        // Dispatch event to PHP if needed
        LaravelBridge.shared.send?(
            "Vendor\\MyPlugin\\Events\\TokenReceived",
            ["token": tokenString]
        )
    }

    @objc private func handleDidFailToRegisterForRemoteNotifications(_ notification: Notification) {
        if let error = notification.userInfo?["error"] as? Error {
            print("MyPluginDelegate: Failed to register: \(error.localizedDescription)")
        }
    }

    @objc private func handleDidBecomeActive(_ notification: Notification) {
        print("MyPluginDelegate: App became active")
        // Refresh state, resume tasks, etc.
    }
}
```

### Initializing the Delegate

The delegate must be instantiated early so it can receive notifications. A common pattern is to reference `MyPluginDelegate.shared` in your first bridge function call:

```swift
enum MyPluginFunctions {

    class Initialize: BridgeFunction {
        func execute(parameters: [String: Any]) throws -> [String: Any] {
            // Ensure delegate is instantiated and listening
            _ = MyPluginDelegate.shared

            return BridgeResponse.success(data: ["initialized": true])
        }
    }
}
```

Or trigger it when setting up UNUserNotificationCenter delegate:

```swift
class RequestPermission: BridgeFunction {
    func execute(parameters: [String: Any]) throws -> [String: Any] {
        let center = UNUserNotificationCenter.current()
        center.delegate = MyPluginDelegate.shared  // Also instantiates if needed

        // ... rest of permission request logic
    }
}
```

### Why NotificationCenter?

This pattern keeps AppDelegate clean and generic:

1. **Decoupling**: Plugins don't modify AppDelegate source code
2. **Multiple subscribers**: Multiple plugins can listen to the same events
3. **Standard iOS pattern**: Uses built-in NotificationCenter, no swizzling needed
4. **Easy testing**: Can post notifications in tests to simulate lifecycle events

### Protocol Conformance in Delegates

Your delegate can also conform to iOS delegate protocols (UNUserNotificationCenterDelegate, MessagingDelegate, etc.):

```swift
class MyPluginDelegate: NSObject, UNUserNotificationCenterDelegate, MessagingDelegate {
    static let shared = MyPluginDelegate()

    private override init() {
        super.init()
        setupNotificationObservers()
    }

    // MARK: - UNUserNotificationCenterDelegate

    func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        willPresent notification: UNNotification,
        withCompletionHandler completionHandler: @escaping (UNNotificationPresentationOptions) -> Void
    ) {
        // Show notification even when app is in foreground
        completionHandler([.banner, .sound, .badge])
    }

    func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        didReceive response: UNNotificationResponse,
        withCompletionHandler completionHandler: @escaping () -> Void
    ) {
        // Handle notification tap
        let userInfo = response.notification.request.content.userInfo
        print("User tapped notification: \(userInfo)")
        completionHandler()
    }

    // MARK: - MessagingDelegate (Firebase)

    func messaging(_ messaging: Messaging, didReceiveRegistrationToken fcmToken: String?) {
        guard let fcmToken = fcmToken else { return }
        print("FCM token received: \(fcmToken)")

        LaravelBridge.shared.send?(
            "Vendor\\MyPlugin\\Events\\TokenGenerated",
            ["token": fcmToken]
        )
    }
}