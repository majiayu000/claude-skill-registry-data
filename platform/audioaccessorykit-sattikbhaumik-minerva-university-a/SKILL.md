---
name: audioaccessorykit
description: "Support audio accessory features like automatic switching using AudioAccessoryKit. Use when implementing automatic audio routing for connected accessories, managing audio accessory sessions, registering device capabilities and placement, providing connected audio source identifiers, or configuring audio accessories connected to iOS devices."
---

# AudioAccessoryKit

Automatic audio switching and intelligent audio routing for third-party audio
accessories. Enables companion apps to register audio accessories with the
system, report device placement, and declare capabilities so the system can
seamlessly switch audio output. Available iOS 26.4+ / Swift 6.3.

> **Beta-sensitive.** AudioAccessoryKit is new in iOS 26.4 and may change before GM.
> Re-check current Apple documentation before relying on specific API details.

AudioAccessoryKit builds on top of AccessorySetupKit. The accessory must first
be paired via AccessorySetupKit before it can be registered for audio features.
The central type is `AccessoryControlDevice`, which manages registration,
capability declaration, and ongoing state updates.

## Contents

- [Setup](#setup)
- [Session Management](#session-management)
- [Audio Switching](#audio-switching)
- [Device Placement](#device-placement)
- [Connected Audio Sources](#connected-audio-sources)
- [Feature Discovery](#feature-discovery)
- [Error Handling](#error-handling)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Setup

### Prerequisites

1. Pair the accessory over Bluetooth using AccessorySetupKit. This yields an
   `ASAccessory` object.
2. Import both frameworks in the companion app:

```swift
import AccessorySetupKit
import AudioAccessoryKit
```

### Framework Availability

| Platform | Minimum Version |
|---|---|
| iOS | 26.4+ |
| iPadOS | 26.4+ |

## Session Management

### Registering an Accessory

After pairing via AccessorySetupKit, register the accessory with
`AccessoryControlDevice` by specifying the capabilities it supports:

```swift
let accessory: ASAccessory  // Obtained from AccessorySetupKit pairing

let capabilities: AccessoryControlDevice.Capabilities = [.audioSwitching, .placement]
try await AccessoryControlDevice.register(accessory, capabilities)
```

Registration activates the specified capabilities and tells the system to begin
routing audio to the accessory.

### Retrieving the Current Configuration

Access the device's current configuration at any time using the static
`current(for:)` method:

```swift
let device = try AccessoryControlDevice.current(for: accessory)
let currentConfig = device.configuration
```

This returns the `AccessoryControlDevice` instance associated with the paired
`ASAccessory`. The device exposes both the `accessory` reference and the
current `configuration`.

### Updating Configuration

Push configuration changes to the system with `update(_:)`:

```swift
let device = try AccessoryControlDevice.current(for: accessory)
var config = device.configuration

config.devicePlacement = .onHead
try await device.update(config)
```

The update call is async and can throw `AccessoryControlDevice.Error` on
failure.

## Audio Switching

Automatic audio switching lets the system intelligently route audio output to
the correct device based on placement and connected sources.

### Enabling Audio Switching

Declare the `.audioSwitching` capability during registration:

```swift
let capabilities: AccessoryControlDevice.Capabilities = [.audioSwitching]
try await AccessoryControlDevice.register(accessory, capabilities)
```

For full automatic switching (including placement-based routing), include both
capabilities:

```swift
let capabilities: AccessoryControlDevice.Capabilities = [.audioSwitching, .placement]
try await AccessoryControlDevice.register(accessory, capabilities)
```

### Capabilities

`AccessoryControlDevice.Capabilities` is an option set with two members:

| Capability | Purpose |
|---|---|
| `.audioSwitching` | Device supports automatic audio switching |
| `.placement` | Device can report its physical placement |

Both capabilities can be combined. Audio switching works without placement, but
providing placement enables more intelligent routing decisions.

## Device Placement

Report the physical position of the accessory to help the system make routing
decisions. Update placement whenever the accessory detects a position change.

### Placement Values

`AccessoryControlDevice.Placement` defines four cases:

| Placement | Meaning |
|---|---|
| `.inEar` | Accessory is seated in the ear (e.g., earbuds) |
| `.onHead` | Accessory is on the head (e.g., headband headphones) |
| `.overTheEar` | Accessory is over the ear (e.g., over-ear headphones) |
| `.offHead` | Accessory is not being worn |

### Updating Placement

```swift
let device = try AccessoryControlDevice.current(for: accessory)
var config = device.configuration

config.devicePlacement = .inEar
try await device.update(config)
```

Common transitions:

- `.offHead` to `.onHead` or `.inEar` when the user puts on the accessory
- `.onHead` or `.inEar` to `.offHead` when removed
- Update promptly on every detected change for responsive audio routing

## Connected Audio Sources

For accessories that connect to multiple Bluetooth devices simultaneously,
inform the system which devices are connected. This lets the system route audio
from the appropriate source.

### Setting Audio Source Identifiers

Provide the Bluetooth address of connected devices as `Data`:

```swift
let device = try AccessoryControlDevice.current(for: accessory)
var config = device.configuration

let primaryBTAddress = Data([0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC])
config.primaryAudioSourceDeviceIdentifier = primaryBTAddress

let secondaryBTAddress = Data([0xAB, 0xCD, 0xEF, 0x01, 0x23, 0x45])
config.secondaryAudioSourceDeviceIdentifier = secondaryBTAddress

try await device.update(config)
```

Update these identifiers when the Bluetooth connection state changes (new
device connects, existing device disconnects).

### Configuration Properties

`AccessoryControlDevice.Configuration` contains all configurable state:

| Property | Type | Purpose |
|---|---|---|
| `deviceCapabilities` | `Capabilities` | Declared device capabilities |
| `devicePlacement` | `Placement?` | Current physical placement |
| `primaryAudioSourceDeviceIdentifier` | `Data?` | Primary connected Bluetooth device address |
| `secondaryAudioSourceDeviceIdentifier` | `Data?` | Secondary connected Bluetooth device address |

## Feature Discovery

### Querying Capabilities

After registration, inspect the device's declared capabilities through its
configuration:

```swift
let device = try AccessoryControlDevice.current(for: accessory)
let caps = device.configuration.deviceCapabilities

if caps.contains(.audioSwitching) {
    // Device supports automatic audio switching
}

if caps.contains(.placement) {
    // Device reports physical placement
}
```

### Checking Placement

Read the current placement to determine if the accessory is being worn:

```swift
let device = try AccessoryControlDevice.current(for: accessory)

if let placement = device.configuration.devicePlacement {
    switch placement {
    case .inEar, .onHead, .overTheEar:
        // Accessory is being worn
        break
    case .offHead:
        // Accessory is not being worn
        break
    @unknown default:
        break
    }
}
```

## Error Handling

`AccessoryControlDevice.Error` covers failure cases during registration and
updates:

| Error | Cause |
|---|---|
| `.accessoryNotCapable` | Accessory does not support the requested capability |
| `.invalidRequest` | Request parameters are invalid |
| `.invalidated` | Device registration has been invalidated |
| `.unknown` | An unspecified error occurred |

Handle errors from registration and update calls:

```swift
do {
    try await AccessoryControlDevice.register(accessory, capabilities)
} catch let error as AccessoryControlDevice.Error {
    switch error {
    case .accessoryNotCapable:
        // Accessory hardware does not support requested capabilities
        break
    case .invalidRequest:
        // Check registration parameters
        break
    case .invalidated:
        // Re-register the device
        break
    case .unknown:
        // Log and retry
        break
    @unknown default:
        break
    }
}
```

## Common Mistakes

### DON'T: Register before pairing with AccessorySetupKit

```swift
// WRONG -- accessory not yet paired
let rawAccessory = ASAccessory()
try await AccessoryControlDevice.register(rawAccessory, [.audioSwitching])

// CORRECT -- use the ASAccessory from a completed pairing session
session.activate(on: .main) { event in
    if event.eventType == .accessoryAdded, let accessory = event.accessory {
        Task {
            try await AccessoryControlDevice.register(accessory, [.audioSwitching])
        }
    }
}
```

### DON'T: Declare placement capability without updating placement

```swift
// WRONG -- registers placement but never updates it
try await AccessoryControlDevice.register(accessory, [.audioSwitching, .placement])
// System never receives placement data, reducing switching accuracy

// CORRECT -- update placement promptly after registration
try await AccessoryControlDevice.register(accessory, [.audioSwitching, .placement])
let device = try AccessoryControlDevice.current(for: accessory)
var config = device.configuration
config.devicePlacement = .offHead
try await device.update(config)
```

### DON'T: Ignore connection state changes for multi-device accessories

```swift
// WRONG -- set audio source identifiers once and never update
config.primaryAudioSourceDeviceIdentifier = someAddress
try await device.update(config)
// Device disconnects, but system still thinks it's the primary source

// CORRECT -- update identifiers when connections change
func onDeviceDisconnected() {
    var config = device.configuration
    config.primaryAudioSourceDeviceIdentifier = nil
    Task { try await device.update(config) }
}
```

### DON'T: Forget to handle the invalidated error

```swift
// WRONG -- ignores invalidation, keeps using stale device reference
try await device.update(config)  // Throws .invalidated, unhandled

// CORRECT -- catch invalidation and re-register
do {
    try await device.update(config)
} catch AccessoryControlDevice.Error.invalidated {
    try await AccessoryControlDevice.register(accessory, capabilities)
}
```

## Review Checklist

- [ ] Accessory paired via AccessorySetupKit before AudioAccessoryKit registration
- [ ] Both `AccessorySetupKit` and `AudioAccessoryKit` imported
- [ ] Capabilities declared at registration match actual hardware support
- [ ] `.placement` capability accompanied by ongoing placement updates
- [ ] Placement transitions (on/off head) reported promptly
- [ ] Audio source device identifiers updated on Bluetooth connection changes
- [ ] All `AccessoryControlDevice.Error` cases handled, including `@unknown default`
- [ ] `update(_:)` calls use `try await` and handle errors
- [ ] Invalidated device references re-registered when needed
- [ ] Deployment target set to iOS 26.4+ or iPadOS 26.4+

## References

- Extended patterns (registration flow, placement monitoring, multi-device coordination): [references/audioaccessorykit-patterns.md](references/audioaccessorykit-patterns.md)
- [AudioAccessoryKit framework](https://sosumi.ai/documentation/audioaccessorykit)
- [Supporting automatic audio switching](https://sosumi.ai/documentation/audioaccessorykit/supporting-automatic-audio-switching)
- [AccessoryControlDevice](https://sosumi.ai/documentation/audioaccessorykit/accessorycontroldevice)
- [AccessoryControlDevice.Configuration](https://sosumi.ai/documentation/audioaccessorykit/accessorycontroldevice/configuration-swift.struct)
- [AccessoryControlDevice.Capabilities](https://sosumi.ai/documentation/audioaccessorykit/accessorycontroldevice/capabilities)
- [AccessoryControlDevice.Placement](https://sosumi.ai/documentation/audioaccessorykit/accessorycontroldevice/placement)
- [AccessorySetupKit framework](https://sosumi.ai/documentation/accessorysetupkit) (prerequisite for pairing)
