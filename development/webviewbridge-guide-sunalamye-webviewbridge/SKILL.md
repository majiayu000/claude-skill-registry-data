---
name: webviewbridge-guide
description: Guide for using WebViewBridge Swift package to build WebPage (macOS 26.0+) bridges with JavaScript injection and bidirectional communication. Use when integrating WebPage with Swift, injecting JavaScript, or handling JS↔Swift messaging.
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

# WebViewBridge Guide

This skill helps use the WebViewBridge Swift package for WebPage (macOS 26.0+) bidirectional communication.

## Package Overview

**WebViewBridge** is a Swift framework for WebPage API with JavaScript injection and bidirectional communication.

- **Repository**: https://github.com/Sunalamye/WebViewBridge
- **Platforms**: macOS 26.0+ (WebPage API)
- **License**: MIT

## Installation

```swift
// Package.swift
dependencies: [
    .package(url: "https://github.com/Sunalamye/WebViewBridge.git", from: "1.0.0"),
]

targets: [
    .target(
        name: "YourApp",
        dependencies: ["WebViewBridge"]
    ),
]
```

## Architecture

```
WebViewBridge/
├── Core/
│   └── WebViewBridge.swift    - Main bridge class
├── JavaScript/
│   └── bridge-core.js         - Core JS utilities
└── WebViewBridgeKit.swift     - Version info
```

## Quick Start

### 1. Create Bridge & Register Modules

```swift
import WebViewBridge
import WebKit

@available(macOS 26.0, *)
@MainActor
class MyViewController: NSViewController {
    let bridge = WebViewBridge(handlerName: "myBridge")
    var webPage: WebPage?

    override func viewDidLoad() {
        super.viewDidLoad()

        // Register core modules
        bridge.registerCoreModules()

        // Register custom module
        bridge.registerModule(JavaScriptModule(
            name: "my-module",
            source: """
                window.myApp = {
                    sendMessage: function(msg) {
                        window.__bridgeCore.sendToSwift('custom_message', { message: msg });
                    }
                };
            """
        ))

        // Handle messages
        bridge.onMessage = { type, data in
            print("Received: \(type) - \(data)")
        }

        // Configure WebPage
        var configuration = WebPage.Configuration()
        let userContentController = WKUserContentController()
        bridge.configure(contentController: userContentController)
        configuration.userContentController = userContentController

        // Create WebPage
        webPage = WebPage(configuration: configuration)
        bridge.configure(webPage: webPage!)
    }
}
```

### 2. JavaScript → Swift

```javascript
// Using bridge-core
window.__bridgeCore.sendToSwift('my_event', { key: 'value' });

// Using custom API
window.myApp.sendMessage('Hello!');
```

### 3. Swift → JavaScript

```swift
Task {
    // ⚠️ MUST use `return` statement!
    let title = try await bridge.callJavaScript("return document.title")
}
```

## ⚠️ Critical: Return Statement

**WebPage.callJavaScript() requires `return` statement!**

```swift
// ❌ WRONG - returns null
try await bridge.callJavaScript("document.title")

// ✅ CORRECT
try await bridge.callJavaScript("return document.title")
try await bridge.callJavaScript("return JSON.stringify({a: 1})")
```

## JavaScriptModule

```swift
let module = JavaScriptModule(
    name: "my-module",
    source: "window.myAPI = { ... };",
    injectAtStart: true,    // default: true
    mainFrameOnly: false    // default: false
)

// Load from bundle
let module = JavaScriptModule.fromBundle(named: "my-script", bundle: .main)
```

## WebViewBridgeDelegate

```swift
@available(macOS 26.0, *)
public protocol WebViewBridgeDelegate: AnyObject {
    func bridge(_ bridge: WebViewBridge, didReceiveMessage type: String, data: [String: Any])
    func bridge(_ bridge: WebViewBridge, webSocketStatusChanged connected: Bool)  // optional
    func bridge(_ bridge: WebViewBridge, didEncounterError error: Error)  // optional
}
```

## bridge-core.js API

```javascript
// Send to Swift
window.__bridgeCore.sendToSwift(type, data)

// Log
window.__bridgeCore.log(message)

// Base64
window.__bridgeCore.arrayBufferToBase64(buffer)
window.__bridgeCore.base64ToArrayBuffer(base64)
window.__bridgeCore.blobToBase64(blob, callback)

// WebSocket interceptor
window.__bridgeCore.installWebSocketInterceptor({
    shouldIntercept: (url) => url.includes('api.example.com')
})
```

## Message Types

| Type | Direction | Description |
|------|-----------|-------------|
| `websocket_open` | JS → Swift | WebSocket connecting |
| `websocket_connected` | JS → Swift | WebSocket connected |
| `websocket_message` | JS → Swift | WebSocket message |
| `websocket_closed` | JS → Swift | WebSocket closed |
| `console_log` | JS → Swift | Log message |

## Complete Example

```swift
@available(macOS 26.0, *)
@MainActor
class WebManager {
    let bridge = WebViewBridge(handlerName: "app")
    var webPage: WebPage?

    func setup() {
        bridge.registerCoreModules()
        bridge.registerModule(JavaScriptModule(
            name: "app-api",
            source: """
                window.App = {
                    notify: (msg) => __bridgeCore.sendToSwift('notify', {msg})
                };
            """
        ))

        bridge.onMessage = { type, data in
            if type == "notify", let msg = data["msg"] as? String {
                print("Notification: \(msg)")
            }
        }

        var config = WebPage.Configuration()
        let ucc = WKUserContentController()
        bridge.configure(contentController: ucc)
        config.userContentController = ucc

        webPage = WebPage(configuration: config)
        bridge.configure(webPage: webPage!)
    }

    func getTitle() async -> String? {
        try? await bridge.callJavaScript("return document.title") as? String
    }
}
```

## Checklist

- [ ] Using `@available(macOS 26.0, *)`
- [ ] Called `registerCoreModules()`
- [ ] Configured both `contentController` and `webPage`
- [ ] Using `return` in `callJavaScript()`
- [ ] Set `onMessage` or delegate

## Reference Documentation

- [WebViewBridge Reference](references/reference.md) - Full API and examples
