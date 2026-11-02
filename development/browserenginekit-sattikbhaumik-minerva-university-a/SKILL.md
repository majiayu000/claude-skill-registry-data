---
name: browserenginekit
description: "Build alternative browser engines using BrowserEngineKit. Use when developing a non-WebKit browser engine for iOS in the EU, managing web content rendering processes, configuring GPU and networking processes for browser functionality, checking device eligibility for alternative engines, or working with BrowserEngineKit entitlements."
---

# BrowserEngineKit

Framework for building web browsers with alternative (non-WebKit) rendering
engines on iOS and iPadOS. Provides process isolation, XPC communication,
capability management, and system integration for browser apps that implement
their own HTML/CSS/JavaScript engine. Targets Swift 6.3 / iOS 26+.

BrowserEngineKit is a specialized framework. Alternative browser engines are
currently supported for distribution in the EU. Japan requires Memory Integrity
Enforcement (MIE) for alternative browser engine distribution. Development and
testing can occur anywhere. The companion
frameworks BrowserEngineCore (low-level primitives) and BrowserKit (eligibility
checks, data transfer) support the overall browser engine workflow.

## Contents

- [Overview and Eligibility](#overview-and-eligibility)
- [Entitlements](#entitlements)
- [Architecture](#architecture)
- [Process Management](#process-management)
- [Extension Types](#extension-types)
- [Capabilities](#capabilities)
- [Layer Hosting and View Coordination](#layer-hosting-and-view-coordination)
- [Text Interaction](#text-interaction)
- [Sandbox and Security](#sandbox-and-security)
- [Downloads](#downloads)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Overview and Eligibility

### Eligibility Checking

Use `BEAvailability` from the BrowserKit framework to check whether the device
is eligible for alternative browser engines:

```swift
import BrowserKit

BEAvailability.isEligible(for: .webBrowser) { eligible, error in
    if eligible {
        // Device supports alternative browser engines
    } else {
        // Fall back or show explanation
    }
}
```

Eligibility depends on the device region and OS version. Do not hard-code
region checks; rely on the system API.

### Related Frameworks

| Framework | Purpose |
|---|---|
| BrowserEngineKit | Process management, extensions, text/view integration |
| BrowserEngineCore | Low-level primitives: kernel events, JIT tag, audio session |
| BrowserKit | Eligibility checks, browser data import/export |

## Entitlements

### Browser App (Host)

The host app requires two entitlements:

| Entitlement | Purpose |
|---|---|
| `com.apple.developer.web-browser` | Enables default-browser candidacy |
| `com.apple.developer.web-browser-engine.host` | Enables alternative engine extensions |

Both must be requested from Apple. The request process varies by region.

### Extension Entitlements

Each extension target requires its type-specific entitlement set to `true`:

| Extension Type | Entitlement |
|---|---|
| Web content | `com.apple.developer.web-browser-engine.webcontent` |
| Networking | `com.apple.developer.web-browser-engine.networking` |
| Rendering | `com.apple.developer.web-browser-engine.rendering` |

### Optional Entitlements

| Entitlement | Extension | Purpose |
|---|---|---|
| `com.apple.security.cs.allow-jit` | Web content | JIT compilation of scripts |
| `com.apple.developer.kernel.extended-virtual-addressing` | Web content | Required alongside JIT |
| `com.apple.developer.memory.transfer_send` | Rendering | Send memory attribution |
| `com.apple.developer.memory.transfer_accept` | Web content | Accept memory attribution |
| `com.apple.developer.web-browser-engine.restrict.notifyd` | Web content | Restrict notification daemon access |

### Embedded Browser Engine (Non-Browser Apps)

Apps that are not browsers but embed an alternative engine for in-app browsing
use different entitlements:

| Entitlement | Purpose |
|---|---|
| `com.apple.developer.embedded-web-browser-engine` | Enable embedded engine |
| `com.apple.developer.embedded-web-browser-engine.engine-association` | Declare engine ownership |

Embedded engines use `arm64` only (not `arm64e`), cannot include browser
extensions, and cannot use JIT compilation.

### Japan-Specific Requirements

Browser apps distributed in Japan must enable hardware memory tagging via
`com.apple.security.hardened-process.checked-allocations`. Apple strongly
recommends enabling this in the EU as well.

## Architecture

A browser built with BrowserEngineKit consists of four components running in
separate processes:

```
Host App (UI, coordination)
  |
  |-- XPC --> Web Content Extension (HTML parsing, JS, DOM)
  |-- XPC --> Networking Extension (URLSession, sockets)
  |-- XPC --> Rendering Extension (Metal, GPU, media)
```

The host app launches and manages all extensions. Extensions cannot launch
other extensions. Extensions communicate with each other through anonymous XPC
endpoints brokered by the host app.

### Bootstrap Sequence

1. Host launches web content, networking, and rendering extensions
2. Host creates XPC connections to each extension
3. Host requests anonymous XPC endpoints from networking and rendering
4. Host sends both endpoints to the web content extension via a bootstrap
   message
5. Web content extension connects directly to networking and rendering

This architecture follows the principle of least privilege: the web content
extension works with untrusted data but has no direct OS resource access.

## Process Management

### Launching Extensions

Each extension type has a corresponding process class in the host app:

```swift
import BrowserEngineKit

// Web content (one per tab or iframe)
let contentProcess = try await WebContentProcess(
    bundleIdentifier: nil,
    onInterruption: {
        // Handle crash or OS interruption
    }
)

// Networking (typically one instance)
let networkProcess = try await NetworkingProcess(
    bundleIdentifier: nil,
    onInterruption: {
        // Handle interruption
    }
)

// Rendering / GPU (typically one instance)
let renderingProcess = try await RenderingProcess(
    bundleIdentifier: nil,
    onInterruption: {
        // Handle interruption
    }
)
```

Pass `nil` for `bundleIdentifier` to use the default extension target. The
interruption handler fires if the extension crashes or is terminated by the OS.

### Creating XPC Connections

```swift
let connection = try contentProcess.makeLibXPCConnection()
// Use connection for inter-process messaging
```

Each process type provides `makeLibXPCConnection()` to create an
`xpc_connection_t` for communication.

### Stopping Extensions

```swift
contentProcess.invalidate()
```

After calling `invalidate()`, no further method calls on the process object
are valid.

## Extension Types

### Web Content Extension

Hosts the browser engine's HTML parser, CSS engine, JavaScript interpreter,
and DOM. Subclass `WebContentExtension` to handle incoming XPC connections:

```swift
import BrowserEngineKit

final class MyWebContentExtension: WebContentExtension {
    override func handle(xpcConnection: xpc_connection_t) {
        // Set up message handlers on the connection
    }
}
```

Configure via `WebContentExtensionConfiguration` in the extension's
`EXAppExtensionAttributes`.

### Networking Extension

Handles all network requests using `URLSession` or socket APIs. One instance
serves all tabs:

```swift
import BrowserEngineKit

final class MyNetworkingExtension: NetworkingExtension {
    override func handle(xpcConnection: xpc_connection_t) {
        // Handle network request messages
    }
}
```

Configure via `NetworkingExtensionConfiguration`.

### Rendering Extension

Accesses the GPU via Metal for video decoding, compositing, and complex
rendering. One instance typically serves the entire browser:

```swift
import BrowserEngineKit

final class MyRenderingExtension: RenderingExtension {
    override func handle(xpcConnection: xpc_connection_t) {
        // Handle rendering commands
    }
}
```

The rendering extension can enable optional features:

```swift
// Enable CoreML in the rendering extension
extension.enableFeature(.coreML)
```

Configure via `RenderingExtensionConfiguration`.

## Capabilities

Grant capabilities to extensions so the OS schedules them appropriately:

```swift
// Grant foreground priority to an extension
let grant = try contentProcess.grantCapability(.foreground)

// ... extension does foreground work ...

// Relinquish when done
grant.invalidate()
```

### Available Capabilities

| Capability | Use Case |
|---|---|
| `.foreground` | Active tab rendering, visible content |
| `.background` | Background tasks, prefetching |
| `.suspended` | Minimal activity, pending cleanup |
| `.mediaPlaybackAndCapture(environment:)` | Audio/video playback, camera/mic capture |

### Media Environment

For media capabilities, create a `MediaEnvironment` tied to a page URL.
The environment supports `AVCaptureSession` for camera/mic access and is
XPC-serializable for cross-process transport:

```swift
let mediaEnv = MediaEnvironment(webPage: pageURL)
let grant = try contentProcess.grantCapability(
    .mediaPlaybackAndCapture(environment: mediaEnv)
)
try mediaEnv.activate()
let captureSession = try mediaEnv.makeCaptureSession()
```

### Visibility Propagation

Attach a visibility propagation interaction to browser views so extensions
know when content is on screen. Both `WebContentProcess` and
`RenderingProcess` provide `createVisibilityPropagationInteraction()`.

## Layer Hosting and View Coordination

The rendering extension draws into a `LayerHierarchy`, whose content the
host app displays via `LayerHierarchyHostingView`. Handles are passed over
XPC. Use `LayerHierarchyHostingTransactionCoordinator` to synchronize layer
updates atomically across processes.

See [references/browserenginekit-patterns.md](references/browserenginekit-patterns.md) for detailed layer hosting
examples and transaction coordination.

## Text Interaction

Adopt `BETextInput` on custom text views to integrate with UIKit's text
system. This enables standard text selection, autocorrect, dictation, and
keyboard interactions.

Key integration points:

- `asyncInputDelegate` for communicating text changes to the system
- `handleKeyEntry(_:completionHandler:)` for keyboard events
- `BETextInteraction` for selection gestures, edit menus, and context menus
- `BEScrollView` and `BEScrollViewDelegate` for custom scroll handling

See [references/browserenginekit-patterns.md](references/browserenginekit-patterns.md) for detailed text interaction
implementation.

## Sandbox and Security

### Restricted Sandbox

After initialization, lock down content extensions using the restricted
sandbox:

```swift
// In the web content extension, after setup:
extension.applyRestrictedSandbox(revision: .revision2)
```

This removes access to resources the extension used during startup but no
longer needs. Use the latest revision (`.revision2`) for the strongest
restrictions.

### JIT Compilation

Web content extensions that JIT-compile JavaScript toggle memory between
writable and executable states. Use the `BE_JIT_WRITE_PROTECT_TAG` from
BrowserEngineCore:

```swift
import BrowserEngineCore

// BE_JIT_WRITE_PROTECT_TAG is used with pthread_jit_write_protect_np
// to control JIT memory page permissions
```

Requires the `com.apple.security.cs.allow-jit` and
`com.apple.developer.kernel.extended-virtual-addressing` entitlements on
the web content extension only.

### arm64e Requirement

All executables (host app and extensions) must be built with the `arm64e`
instruction set for distribution. Build as a universal binary to also support
`arm64` iPads.

In Xcode build settings or xcconfig:

```
ARCHS[sdk=iphoneos*]=arm64e
```

Do not use `arm64e` for Simulator targets.

## Downloads

Report download progress to the system using `BEDownloadMonitor`. Create an
access token, initialize the monitor with source/destination URLs and a
`Progress` object, then call `beginMonitoring()` to show the system download
UI. Use `resumeMonitoring(placeholderURL:)` to resume interrupted downloads.

See [references/browserenginekit-patterns.md](references/browserenginekit-patterns.md) for full download management
examples.

## Common Mistakes

### DON'T: Skip the bootstrap sequence

```swift
// WRONG - content extension has no path to other extensions
let contentProcess = try await WebContentProcess(
    bundleIdentifier: nil, onInterruption: {}
)
// Immediately start sending work without connecting to networking/rendering

// CORRECT - broker connections through the host app
let networkEndpoint = try await networkProxy.getEndpoint()
let renderEndpoint = try await renderProxy.getEndpoint()
try await contentProxy.bootstrap(
    renderingExtension: renderEndpoint,
    networkExtension: networkEndpoint
)
```

### DON'T: Launch extensions from other extensions

```swift
// WRONG - extensions cannot launch other extensions
// (inside a WebContentExtension)
let network = try await NetworkingProcess(...)

// CORRECT - only the host app launches extensions
// Host app creates all processes, then brokers connections
```

### DON'T: Use extension process objects after invalidation

```swift
// WRONG
contentProcess.invalidate()
let conn = try contentProcess.makeLibXPCConnection()  // Error

// CORRECT - create a new process if needed
let newProcess = try await WebContentProcess(
    bundleIdentifier: nil, onInterruption: {}
)
```

### DON'T: Apply JIT entitlements to non-content extensions

JIT compilation entitlements (`com.apple.security.cs.allow-jit`) are valid
only on web content extensions. Adding them to the host app, rendering
extension, or networking extension causes App Store rejection.

### DON'T: Hard-code region eligibility

```swift
// WRONG
if Locale.current.region?.identifier == "DE" {
    useAlternativeEngine()
}

// CORRECT - use the system eligibility API
BEAvailability.isEligible(for: .webBrowser) { eligible, _ in
    if eligible { useAlternativeEngine() }
}
```

### DON'T: Forget to set UIRequiredDeviceCapabilities

Without `web-browser-engine` in `UIRequiredDeviceCapabilities`, users on
unsupported devices can download the app and hit runtime failures.

## Review Checklist

- [ ] `com.apple.developer.web-browser-engine.host` entitlement on host app
- [ ] Each extension has its type-specific entitlement
- [ ] `UIRequiredDeviceCapabilities` includes `web-browser-engine`
- [ ] `arm64e` instruction set configured for all iOS device targets
- [ ] `arm64e` is not set for Simulator targets
- [ ] Swift packages built with `iOSPackagesShouldBuildARM64e` workspace setting
- [ ] Extension point identifiers set correctly in each extension's Info.plist
- [ ] Interruption handlers implemented for all process types
- [ ] Bootstrap sequence connects content extension to networking and rendering
- [ ] Capabilities granted before work begins and invalidated when done
- [ ] Visibility propagation interaction added to browser content views
- [ ] Restricted sandbox applied to content extensions after initialization
- [ ] `BEAvailability` used for eligibility checks instead of manual region logic
- [ ] Memory attribution configured if rendering extension memory is high
- [ ] Download progress reported via `BEDownloadMonitor` for active downloads
- [ ] Memory tagging enabled for Japan distribution (recommended for EU)

## References

- Extended patterns (text interaction, layer hosting, scroll views, XPC communication, content filtering): [references/browserenginekit-patterns.md](references/browserenginekit-patterns.md)
- [BrowserEngineKit framework](https://sosumi.ai/documentation/browserenginekit)
- [Designing your browser architecture](https://sosumi.ai/documentation/browserenginekit/designing-your-browser-architecture)
- [Creating browser extensions in Xcode](https://sosumi.ai/documentation/browserenginekit/creating-browser-extensions-in-xcode)
- [Managing the browser extension life cycle](https://sosumi.ai/documentation/browserenginekit/managing-the-browser-extension-lifecycle)
- [Using XPC to communicate with browser extensions](https://sosumi.ai/documentation/browserenginekit/using-xpc-to-communicate-with-browser-extensions)
- [Web Browser Engine Entitlement](https://sosumi.ai/documentation/bundleresources/entitlements/com.apple.developer.web-browser-engine.host)
- [BrowserKit framework](https://sosumi.ai/documentation/browserkit)
- [BrowserEngineCore framework](https://sosumi.ai/documentation/browserenginecore)
- [Sample: Developing a browser app with an alternative engine](https://sosumi.ai/documentation/browserenginekit/developing-a-browser-app-that-uses-an-alternative-browser-engine)
