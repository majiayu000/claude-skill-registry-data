---
name: ios-simulator
description: "Manages iOS Simulator devices and tests app behavior using xcrun simctl. Covers device lifecycle (create, boot, shutdown, erase, delete), app install and launch, push notification simulation, location simulation, permission grants via privacy subcommand, deep link testing via openurl, status bar overrides, screenshot and video recording, log streaming with os_log filtering, get_app_container paths, and #if targetEnvironment(simulator) compile-time checks. Use when creating or managing simulator devices, testing push notifications without APNs, simulating GPS locations, granting or resetting privacy permissions, capturing screenshots or screen recordings from the command line, streaming device logs, debugging simulator boot failures, troubleshooting CoreSimulator issues, or checking simulator hardware limitations."
---

# iOS Simulator

Manage iOS Simulator devices and test app behavior from the command line using `xcrun simctl`. Covers the full device lifecycle, app deployment, push and location simulation, permission control, screenshot and video recording, log streaming, and compile-time simulator detection.

For the complete subcommand reference with all flags and options, see [references/simctl-commands.md](references/simctl-commands.md).

## Contents

- [Device Lifecycle](#device-lifecycle)
- [App Install and Launch](#app-install-and-launch)
- [Testing Workflows](#testing-workflows)
- [Screenshot and Video Recording](#screenshot-and-video-recording)
- [Log Streaming](#log-streaming)
- [Compile-Time Simulator Detection](#compile-time-simulator-detection)
- [Simulator Limitations](#simulator-limitations)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Device Lifecycle

### Listing Devices and Runtimes

```bash
# List all available simulators grouped by runtime
xcrun simctl list devices available

# List installed runtimes
xcrun simctl list runtimes

# List only booted devices
xcrun simctl list devices booted

# JSON output for scripting
xcrun simctl list -j devices available
```

Parse JSON output to find a specific device programmatically. See [references/simctl-commands.md](references/simctl-commands.md) for `jq` parsing examples.

### Creating a Device

```bash
# Find available device types and runtimes
xcrun simctl list devicetypes
xcrun simctl list runtimes

# Create a device — returns the new UDID
xcrun simctl create "My Test Phone" "iPhone 16 Pro" "com.apple.CoreSimulator.SimRuntime.iOS-18-4"
```

Device types and runtime identifiers in examples throughout this skill are illustrative. Run `simctl list devicetypes` and `simctl list runtimes` to find the identifiers available on your system.

The returned UDID identifies the device for all subsequent commands. Use descriptive names to distinguish devices in `simctl list` output.

### Boot, Shutdown, Erase, Delete

```bash
# Boot a specific device
xcrun simctl boot <UDID>

# Shutdown a running device
xcrun simctl shutdown <UDID>

# Factory reset — wipes all data, keeps the device
xcrun simctl erase <UDID>

# Delete a specific device
xcrun simctl delete <UDID>

# Delete all devices not available in the current Xcode
xcrun simctl delete unavailable

# Shutdown everything
xcrun simctl shutdown all
```

Use `booted` as a UDID shorthand when exactly one simulator is running:

```bash
xcrun simctl shutdown booted
```

If multiple simulators are booted, `booted` picks one of them non-deterministically. Prefer explicit UDIDs when running parallel simulators.

## App Install and Launch

### Installing an App

```bash
# Build for simulator first
xcodebuild build \
    -scheme MyApp \
    -destination 'platform=iOS Simulator,name=iPhone 16 Pro' \
    -derivedDataPath build/

# Install the .app bundle
xcrun simctl install booted build/Build/Products/Debug-iphonesimulator/MyApp.app
```

The path must point to a `.app` directory built for the simulator architecture, not a `.ipa` file.

### Launching and Terminating

```bash
# Launch by bundle ID
xcrun simctl launch booted com.example.MyApp

# Launch and stream stdout/stderr to the terminal
xcrun simctl launch --console booted com.example.MyApp

# Pass launch arguments
xcrun simctl launch booted com.example.MyApp --reset-onboarding -AppleLanguages "(fr)"

# Terminate a running app
xcrun simctl terminate booted com.example.MyApp
```

`--console` is useful for debugging — it shows `print()` and `os_log` output directly in the terminal.

### App Container Paths

```bash
# App bundle location
xcrun simctl get_app_container booted com.example.MyApp app

# Data container (Documents, Library, tmp)
xcrun simctl get_app_container booted com.example.MyApp data

# Shared app group container
xcrun simctl get_app_container booted com.example.MyApp group.com.example.shared
```

Use these paths to inspect sandboxed files, databases, or UserDefaults during debugging.

## Testing Workflows

### Push Notification Simulation

Create a JSON payload file:

```json
{
    "aps": {
        "alert": {
            "title": "New Message",
            "body": "You have a new message from Alice"
        },
        "badge": 3,
        "sound": "default"
    },
    "customKey": "customValue"
}
```

Send it to the Simulator:

```bash
# Send push payload from file
xcrun simctl push booted com.example.MyApp payload.json

# Pipe payload from stdin
echo '{"aps":{"alert":"Quick test"}}' | xcrun simctl push booted com.example.MyApp -
```

This simulates local delivery only — no APNs connection is involved. Use this to test payload handling, notification display, and notification actions. Always verify on a real device before shipping to confirm APNs delivery works end to end.

### Location Simulation

```bash
# Set a fixed coordinate (latitude, longitude)
xcrun simctl location booted set 37.3349,-122.0090

# List available predefined scenarios
xcrun simctl location booted list

# Run a predefined scenario
xcrun simctl location booted run "City Run"

# Clear the simulated location
xcrun simctl location booted clear
```

The `run` subcommand accepts predefined scenario names (e.g., "City Run", "Freeway Drive"), not GPX file paths. Use Xcode's Debug > Simulate Location menu for GPX-based routes.

Location simulation affects all apps using Core Location on the booted device. Clear the location when done to avoid unexpected test results.

### Privacy Permissions

```bash
# Grant a permission
xcrun simctl privacy booted grant photos com.example.MyApp

# Revoke a permission
xcrun simctl privacy booted revoke microphone com.example.MyApp

# Reset all permissions for the app
xcrun simctl privacy booted reset all com.example.MyApp
```

Common service names: `photos`, `microphone`, `contacts`, `calendar`, `reminders`, `location`, `location-always`, `motion`, `siri`. See [references/simctl-commands.md](references/simctl-commands.md) for the full list.

Pre-granting permissions in CI avoids system permission dialogs that block automated test runs.

### Deep Links and URLs

```bash
# Open a URL (triggers universal links or custom URL schemes)
xcrun simctl openurl booted "https://example.com/product/123"

# Custom URL scheme
xcrun simctl openurl booted "myapp://settings/notifications"
```

For universal links, the app's associated domains entitlement must be configured. The Simulator uses the `apple-app-site-association` file from the domain.

### Status Bar Overrides

```bash
# Set a clean status bar for screenshots
xcrun simctl status_bar booted override \
    --time "9:41" \
    --batteryState charged \
    --batteryLevel 100 \
    --cellularMode active \
    --cellularBars 4 \
    --wifiBars 3 \
    --operatorName ""

# Clear all overrides
xcrun simctl status_bar booted clear
```

Use status bar overrides to produce consistent App Store screenshots. Always clear overrides after capturing to avoid confusing other testing.

## Screenshot and Video Recording

```bash
# Capture a screenshot
xcrun simctl io booted screenshot screenshot.png

# Record video (press Ctrl+C to stop)
xcrun simctl io booted recordVideo recording.mov

# Screenshot with specific display mask
xcrun simctl io booted screenshot --mask black screenshot.png
```

`--mask` options: `ignored` (default, no mask), `alpha` (transparent corners), `black` (black corners). Use `alpha` or `black` when capturing screenshots that show the device shape. The `alpha` mask is only supported for screenshots — video recording falls back to `black`.

Video recording continues until the process receives SIGINT (Ctrl+C). The recording is saved only after stopping — killing the process with SIGKILL loses the file.

## Log Streaming

### Basic Log Stream

```bash
# Stream all logs at debug level and above
xcrun simctl spawn booted log stream --level debug

# Filter by subsystem
xcrun simctl spawn booted log stream --level debug \
    --predicate 'subsystem == "com.example.app"'

# Filter by subsystem and category
xcrun simctl spawn booted log stream --level debug \
    --predicate 'subsystem == "com.example.app" AND category == "networking"'

# Filter by process name
xcrun simctl spawn booted log stream \
    --predicate 'process == "MyApp"'
```

### Combining with os.Logger

Design subsystems and categories for filterability:

```swift
import os

let networkLogger = Logger(subsystem: "com.example.app", category: "networking")
let uiLogger = Logger(subsystem: "com.example.app", category: "ui")

func fetchData() async throws -> Data {
    networkLogger.debug("Starting request to /api/data")
    let (data, response) = try await URLSession.shared.data(from: url)
    networkLogger.info("Received \(data.count) bytes, status: \((response as? HTTPURLResponse)?.statusCode ?? 0)")
    return data
}
```

Then filter the log stream to see only networking output:

```bash
xcrun simctl spawn booted log stream --level debug \
    --predicate 'subsystem == "com.example.app" AND category == "networking"'
```

## Compile-Time Simulator Detection

Use `#if targetEnvironment(simulator)` to exclude code that cannot run in the Simulator:

```swift
func registerForPush() {
    #if targetEnvironment(simulator)
    logger.info("Skipping APNs registration — running in Simulator")
    #else
    UIApplication.shared.registerForRemoteNotifications()
    #endif
}
```

Runtime detection via environment variables:

```swift
var isSimulator: Bool {
    ProcessInfo.processInfo.environment["SIMULATOR_DEVICE_NAME"] != nil
}
```

Prefer compile-time checks (`#if targetEnvironment(simulator)`) over runtime checks. The compiler strips excluded code entirely, preventing linker errors from unavailable symbols.

## Simulator Limitations

| Capability | Simulator Support |
|-----------|------------------|
| APNs push delivery | No — use `simctl push` for local simulation |
| Metal GPU family parity | Partial — host GPU, not device GPU; some shaders differ |
| Camera hardware | No — use photo library injection or mock `AVCaptureSession` |
| Microphone | No hardware mic — audio input is routed from Mac microphone |
| Secure Enclave | No — `kSecAttrTokenIDSecureEnclave` operations fail |
| App Attest (DCAppAttestService) | No — `isSupported` returns `false` |
| DockKit motor control | No — no physical accessory connection |
| Accelerometer / Gyroscope | No real sensors — use `CMMotionManager` simulation in Xcode |
| Barometer | No |
| NFC (Core NFC) | No |
| Bluetooth (Core Bluetooth) | No — use a real device for BLE testing |
| CarPlay hardware | No — use the separate CarPlay Simulator companion app |
| Face ID / Touch ID hardware | No hardware — use Features > Face ID / Touch ID menu in Simulator |
| Cellular network conditions | No — use Network Link Conditioner on Mac |

## Common Mistakes

### DON'T: Hardcode simulator UDIDs in scripts

UDIDs change when simulators are deleted and recreated. Hardcoded values break on other machines and CI.

```bash
# WRONG — hardcoded UDID
xcrun simctl boot "A1B2C3D4-E5F6-7890-ABCD-EF1234567890"

# CORRECT — look up by name and runtime
UDID=$(xcrun simctl list -j devices available | \
    jq -r '.devices["com.apple.CoreSimulator.SimRuntime.iOS-18-4"][] | select(.name == "iPhone 16 Pro") | .udid')
xcrun simctl boot "$UDID"

# CORRECT — use "booted" when one simulator is running
xcrun simctl install booted MyApp.app
```

### DON'T: Install or launch on a shutdown simulator

`simctl install` and `simctl launch` require a booted device. They fail silently or with an unhelpful error on a shutdown device.

```bash
# WRONG — device is not booted
xcrun simctl install <UDID> MyApp.app  # fails

# CORRECT — boot first, then install
xcrun simctl boot <UDID>
xcrun simctl install <UDID> MyApp.app
xcrun simctl launch <UDID> com.example.MyApp
```

### DON'T: Leave zombie simulators running in CI

Each booted simulator consumes memory and CPU. CI pipelines that create simulators without cleanup accumulate zombie devices.

```bash
# WRONG — CI script creates and boots but never cleans up
xcrun simctl create "CI Phone" "iPhone 16 Pro" "com.apple.CoreSimulator.SimRuntime.iOS-18-4"
xcrun simctl boot "$UDID"
# ... tests run, pipeline exits ...

# CORRECT — always clean up in CI teardown
cleanup() {
    xcrun simctl shutdown all
    xcrun simctl delete "$UDID"
}
trap cleanup EXIT
```

### DON'T: Assume simctl push validates APNs delivery

`simctl push` bypasses the entire APNs infrastructure. It tests payload parsing and notification UI, not token registration, entitlements, or server-side delivery.

```bash
# WRONG — only testing with simctl, shipping without real device testing
xcrun simctl push booted com.example.MyApp payload.json
# "Push works!" — no, it only proves the app handles the payload

# CORRECT — use simctl for development iteration, then verify end-to-end on a real device
# 1. simctl push during development for fast iteration
# 2. Real device + APNs sandbox for integration testing before release
```

### DON'T: Keep retrying boot on a stuck simulator

A simulator stuck in the "Booting" state will not recover by retrying `boot`. The underlying CoreSimulator state is corrupted.

```bash
# WRONG — retry loop on a stuck device
xcrun simctl boot "$UDID"  # "Unable to boot device in current state: Booting"
xcrun simctl boot "$UDID"  # same error, forever

# CORRECT — shut down, erase, and retry
xcrun simctl shutdown "$UDID"
xcrun simctl erase "$UDID"
xcrun simctl boot "$UDID"

# If that fails, reset CoreSimulator entirely
xcrun simctl shutdown all
xcrun simctl erase all
# Last resort: rm -rf ~/Library/Developer/CoreSimulator/Caches
```

## Review Checklist

- [ ] Simulator devices created with explicit device type and runtime identifiers
- [ ] Scripts use `booted` or parsed UDID from JSON output, not hardcoded values
- [ ] Push notification payloads tested via `simctl push` during development
- [ ] Push notification delivery verified on a real device before release
- [ ] Location simulation tested with both fixed coordinates and predefined scenarios
- [ ] Privacy permissions pre-granted in CI to avoid blocking dialogs
- [ ] `#if targetEnvironment(simulator)` guards around APIs unavailable in Simulator
- [ ] Status bar overrides cleared after capturing screenshots
- [ ] CI pipelines shut down and delete simulators in teardown
- [ ] Log streaming configured with subsystem/category predicates for focused debugging
- [ ] App container paths used for inspecting sandboxed data during debugging

## References

- [Running your app in Simulator or on a device](https://sosumi.ai/documentation/xcode/running-your-app-in-simulator-or-on-a-device)
- [Downloading and installing additional Xcode components](https://sosumi.ai/documentation/xcode/installing-additional-simulator-runtimes)
- simctl command reference: [references/simctl-commands.md](references/simctl-commands.md)
