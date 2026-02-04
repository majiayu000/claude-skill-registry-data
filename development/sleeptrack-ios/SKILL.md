---
name: sleeptrack-ios
description: This skill helps iOS developers integrate the Asleep SDK for sleep tracking functionality. Use this skill when building native iOS apps with Swift/SwiftUI that need sleep tracking capabilities, implementing delegate patterns, configuring iOS permissions (microphone, notifications, background modes), managing tracking lifecycle, integrating Siri Shortcuts, or working with Combine framework for reactive state management.
---

# Sleeptrack iOS

## Overview

This skill provides comprehensive guidance for integrating the Asleep SDK into native iOS applications using Swift and SwiftUI. It covers SDK setup, iOS-specific permissions, delegate-based architecture, tracking lifecycle management, Combine framework integration, and Siri Shortcuts support.

Use this skill when:
- Building native iOS sleep tracking applications
- Implementing SwiftUI-based tracking interfaces
- Managing iOS permissions and background modes
- Working with delegate patterns for SDK callbacks
- Integrating Siri Shortcuts for voice-activated tracking
- Using Combine framework for reactive state management

**Prerequisites**: Developers should first review the `sleeptrack-foundation` skill to understand core Asleep concepts, authentication, data structures, and error handling before implementing iOS-specific integration.

## Quick Start

### 1. Installation

Add AsleepSDK to your Xcode project using Swift Package Manager:

```swift
// In Xcode: File → Add Packages
// Enter package URL: https://github.com/asleep-ai/asleep-sdk-ios
```

Or add to `Package.swift`:

```swift
dependencies: [
    .package(url: "https://github.com/asleep-ai/asleep-sdk-ios", from: "2.0.0")
]
```

### 2. Configure iOS Permissions

Add required permissions to `Info.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- Microphone access for audio-based sleep tracking -->
    <key>NSMicrophoneUsageDescription</key>
    <string>This app uses your microphone to track sleep stages and detect snoring during sleep.</string>

    <!-- Background audio mode for continuous tracking -->
    <key>UIBackgroundModes</key>
    <array>
        <string>audio</string>
    </array>

    <!-- Optional: For notification reminders -->
    <key>NSUserNotificationsUsageDescription</key>
    <string>Get reminders to start and stop sleep tracking.</string>
</dict>
</plist>
```

### 3. Basic Setup

```swift
import SwiftUI
import AsleepSDK

@main
struct SleepTrackerApp: App {
    var body: some Scene {
        WindowGroup {
            MainView()
        }
    }
}
```

## SDK Architecture

The Asleep iOS SDK follows a delegate-based architecture with three main components:

### 1. AsleepConfig - Configuration and User Management

**Purpose**: Initialize SDK with API credentials and manage user lifecycle.

**Key Delegate**: `AsleepConfigDelegate`

```swift
protocol AsleepConfigDelegate {
    func userDidJoin(userId: String, config: Asleep.Config)
    func didFailUserJoin(error: Asleep.AsleepError)
    func userDidDelete(userId: String)
}
```

### 2. SleepTrackingManager - Tracking Lifecycle

**Purpose**: Control sleep tracking start, stop, and monitor session state.

**Key Delegate**: `AsleepSleepTrackingManagerDelegate`

```swift
protocol AsleepSleepTrackingManagerDelegate {
    func didCreate()                          // Session created
    func didUpload(sequence: Int)             // Data uploaded
    func didClose(sessionId: String)          // Tracking stopped
    func didFail(error: Asleep.AsleepError)  // Error occurred
    func didInterrupt()                       // Interrupted (e.g., phone call)
    func didResume()                          // Resumed after interruption
    func micPermissionWasDenied()             // Mic permission denied
    func analysing(session: Asleep.Model.Session) // Real-time data (optional)
}
```

### 3. Reports - Retrieving Sleep Data

**Purpose**: Fetch sleep reports and session lists after tracking completes.

```swift
// Reports API is async/await based, not delegate-driven
let reports = Asleep.createReports(config: config)

// Get single report
let report = try await reports.report(sessionId: "session_id")

// Get report list
let reportList = try await reports.reports(
    fromDate: "2024-01-01",
    toDate: "2024-01-31"
)
```

## Implementation Overview

### Minimal ViewModel Example

```swift
import Foundation
import Combine
import AsleepSDK

final class SleepTrackingViewModel: ObservableObject {
    private(set) var trackingManager: Asleep.SleepTrackingManager?
    private(set) var reports: Asleep.Reports?

    @Published var isTracking = false
    @Published var error: String?
    @Published private(set) var config: Asleep.Config?

    func initAsleepConfig(apiKey: String, userId: String) {
        Asleep.initAsleepConfig(
            apiKey: apiKey,
            userId: userId,
            delegate: self
        )
    }

    func startTracking() {
        trackingManager?.startTracking()
    }

    func stopTracking() {
        trackingManager?.stopTracking()
    }
}

// Implement delegates
extension SleepTrackingViewModel: AsleepConfigDelegate {
    func userDidJoin(userId: String, config: Asleep.Config) {
        Task { @MainActor in
            self.config = config
            self.trackingManager = Asleep.createSleepTrackingManager(
                config: config,
                delegate: self
            )
        }
    }

    func didFailUserJoin(error: Asleep.AsleepError) {
        Task { @MainActor in
            self.error = error.localizedDescription
        }
    }

    func userDidDelete(userId: String) {
        // Handle user deletion
    }
}

extension SleepTrackingViewModel: AsleepSleepTrackingManagerDelegate {
    func didCreate() {
        Task { @MainActor in
            self.isTracking = true
        }
    }

    func didClose(sessionId: String) {
        Task { @MainActor in
            self.isTracking = false
            // Initialize reports to fetch session data
            self.reports = Asleep.createReports(config: config!)
        }
    }

    func didFail(error: Asleep.AsleepError) {
        Task { @MainActor in
            self.error = error.localizedDescription
        }
    }

    // Implement other delegate methods as needed
}
```

For complete ViewModel implementation with all delegate methods, see [references/complete_viewmodel_implementation.md](references/complete_viewmodel_implementation.md)

## iOS-Specific Features

### 1. Siri Shortcuts

Enable voice-activated tracking with App Intents (iOS 16+). Users can say "Hey Siri, start sleep" or "Hey Siri, stop sleep".

For complete Siri Shortcuts implementation, see [references/ios_specific_features.md](references/ios_specific_features.md#siri-shortcuts-integration)

### 2. Background Audio Mode

Configure background audio to maintain tracking during sleep. Simply add `audio` to `UIBackgroundModes` in Info.plist - iOS handles the rest automatically.

For details, see [references/ios_specific_features.md](references/ios_specific_features.md#background-audio-mode)

### 3. Microphone Permission

Request microphone permission before starting tracking:

```swift
import AVFoundation

func requestMicrophonePermission() async -> Bool {
    switch AVAudioSession.sharedInstance().recordPermission {
    case .granted: return true
    case .denied: return false
    case .undetermined:
        return await AVAudioSession.sharedInstance().requestRecordPermission()
    @unknown default: return false
    }
}
```

For complete permission handling, see [references/ios_specific_features.md](references/ios_specific_features.md#microphone-permission-handling)

### 4. App Lifecycle Management

Handle app state transitions using SwiftUI's `scenePhase`:

```swift
struct SleepTrackingView: View {
    @Environment(\.scenePhase) private var scenePhase

    var body: some View {
        // ... view content ...
        .onChange(of: scenePhase) { newPhase in
            switch newPhase {
            case .active: print("App is active")
            case .inactive: print("App is inactive")
            case .background: print("App in background - tracking continues")
            @unknown default: break
            }
        }
    }
}
```

For advanced lifecycle patterns, see [references/ios_specific_features.md](references/ios_specific_features.md#app-lifecycle-management)

### 5. Persistent Storage

Store configuration using AppStorage:

```swift
struct SleepTrackingView: View {
    @AppStorage("sleepapp+apikey") private var apiKey = ""
    @AppStorage("sleepapp+userid") private var userId = ""
    // Values automatically persist across app launches
}
```

## Error Handling

### Common Error Patterns

```swift
func handleError(_ error: Asleep.AsleepError) {
    switch error {
    case .micPermission:
        // Guide user to Settings
        showMicPermissionAlert()

    case .audioSessionError:
        // Another app is using microphone
        showAudioUnavailableAlert()

    case let .httpStatus(code, _, message):
        switch code {
        case 403: // Session already active on another device
        case 404: // Session not found
        default: break
        }

    default:
        showGenericError(error.localizedDescription)
    }
}
```

### Retry with Exponential Backoff

```swift
func startTrackingWithRetry() {
    trackingManager?.startTracking()
}

func didFail(error: Asleep.AsleepError) {
    if isTransientError(error) && retryCount < maxRetries {
        retryCount += 1
        DispatchQueue.main.asyncAfter(deadline: .now() + pow(2.0, Double(retryCount))) {
            self.startTrackingWithRetry()
        }
    } else {
        handleError(error)
    }
}
```

For comprehensive error handling patterns, see [references/advanced_patterns.md](references/advanced_patterns.md#error-recovery-patterns)

## Best Practices

### 1. State Management

Use `@Published` properties for reactive UI updates:

```swift
final class SleepTrackingViewModel: ObservableObject {
    @Published var isTracking = false
    @Published var error: String?
    // UI automatically updates when values change
}
```

### 2. Main Thread Safety

Always update UI on main thread:

```swift
func didCreate() {
    Task { @MainActor in  // Ensures main thread
        self.isTracking = true
    }
}
```

### 3. Resource Cleanup

```swift
final class SleepTrackingViewModel: ObservableObject {
    deinit {
        trackingManager = nil
        reports = nil
    }
}
```

### 4. User Experience

Provide clear visual feedback with loading states, progress indicators, and error messages. Disable controls appropriately during tracking.

### 5. Testing Considerations

Use dependency injection for testable code:

```swift
protocol SleepTrackingManagerProtocol {
    func startTracking()
    func stopTracking()
}

// Production and mock implementations
```

For complete testing patterns, see [references/advanced_patterns.md](references/advanced_patterns.md#testing-patterns)

## Common Integration Patterns

### Pattern 1: Simple Single-View App

Best for basic sleep tracking with minimal features. Single view with tracking controls.

### Pattern 2: Multi-View App with Navigation

Best for apps with reports, settings, and history. Uses TabView for navigation between Track, History, and Settings.

### Pattern 3: Centralized SDK Manager

Best for complex apps sharing SDK instance across views. Single source of truth with `AsleepSDKManager.shared`.

For complete implementation of all patterns, see [references/advanced_patterns.md](references/advanced_patterns.md)

## Real-time Data Access

Access preliminary sleep data during tracking (available after sequence 10):

```swift
func analysing(session: Asleep.Model.Session) {
    Task { @MainActor in
        if let sleepStages = session.sleepStages {
            updateRealtimeChart(stages: sleepStages)
        }
    }
}

func didUpload(sequence: Int) {
    // Real-time data available every 10 sequences after sequence 10
    if sequence >= 10 && sequence % 10 == 0 {
        // SDK automatically calls analysing() delegate
    }
}
```

## Fetching Reports

Retrieve sleep session data after tracking:

```swift
func fetchReport(sessionId: String) async {
    do {
        let report = try await reports?.report(sessionId: sessionId)
        // Process report data
    } catch {
        // Handle error
    }
}

// Fetch multiple sessions
func fetchReportList() async {
    let reportList = try await reports?.reports(
        fromDate: "2024-01-01",
        toDate: "2024-01-31"
    )
}
```

## Troubleshooting

### Tracking Doesn't Start

**Causes**: Missing microphone permission, empty API key/user ID, another app using microphone

**Solution**: Validate configuration and check microphone permission before starting

### Background Tracking Stops

**Causes**: Background audio mode not configured, memory pressure, force-closed app

**Solution**: Ensure `UIBackgroundModes` includes `audio` in Info.plist

### Reports Not Available

**Causes**: Session processing incomplete (takes time), minimum duration not met (5 minutes), network issues

**Solution**: Implement retry logic with exponential backoff when fetching reports

For detailed troubleshooting, see the complete implementation examples in references/

## Sample Code Reference

This skill is based on the official Asleep iOS sample app:

- **MainViewModel.swift**: Complete ViewModel with all delegates
- **MainView.swift**: SwiftUI view with tracking controls
- **StartSleepIntent.swift / StopSleepIntent.swift**: Siri Shortcuts
- **ReportView.swift**: Sleep report display
- **Info.plist**: Required iOS permissions

Sample app: [Asleep iOS Sample App](https://github.com/asleep-ai/asleep-sdk-ios-sampleapp-public)

## Resources

### Official Documentation

- **iOS Get Started**: https://docs-en.asleep.ai/docs/ios-get-started.md
- **iOS Error Codes**: https://docs-en.asleep.ai/docs/ios-error-codes.md
- **AsleepConfig Reference**: https://docs-en.asleep.ai/docs/ios-asleep-config.md
- **SleepTrackingManager Reference**: https://docs-en.asleep.ai/docs/ios-sleep-tracking-manager.md
- **Sample App Guide**: https://docs-en.asleep.ai/docs/sample-app.md

### Apple Documentation

- **SwiftUI**: https://developer.apple.com/documentation/swiftui
- **Combine**: https://developer.apple.com/documentation/combine
- **AVAudioSession**: https://developer.apple.com/documentation/avfaudio/avaudiosession
- **App Intents**: https://developer.apple.com/documentation/appintents
- **Background Modes**: https://developer.apple.com/documentation/xcode/configuring-background-execution-modes

### Related Skills

- **sleeptrack-foundation**: Core Asleep concepts, authentication, and data structures
- **sleeptrack-android**: Android-specific implementation guide
- **sleeptrack-be**: Backend API integration

## Next Steps

After integrating the iOS SDK:

1. Test thoroughly across different iOS devices and versions
2. Implement proper error handling for all edge cases
3. Add user-friendly error messages and recovery flows
4. Consider HealthKit integration for data export
5. Implement notification reminders for tracking
6. Add data visualization for sleep trends
7. Consider Apple Watch companion app
8. Submit to App Store with proper privacy declarations
