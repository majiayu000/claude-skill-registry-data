---
name: accessorysetupkit
description: "Discover and configure Bluetooth and Wi-Fi accessories using AccessorySetupKit. Use when presenting a privacy-preserving accessory picker, defining discovery descriptors for BLE or Wi-Fi devices, handling accessory session events, migrating from CoreBluetooth permission-based scanning, or setting up accessories without requiring broad Bluetooth permissions."
---

# AccessorySetupKit

Privacy-preserving accessory discovery and setup for Bluetooth and Wi-Fi
devices. Replaces broad Bluetooth/Wi-Fi permission prompts with a
system-provided picker that grants per-accessory access with a single tap.
Available iOS 18+ / Swift 6.3.

After setup, apps continue using CoreBluetooth and NetworkExtension for
communication. AccessorySetupKit handles only the discovery and authorization
step.

## Contents

- [Setup and Entitlements](#setup-and-entitlements)
- [Discovery Descriptors](#discovery-descriptors)
- [Presenting the Picker](#presenting-the-picker)
- [Event Handling](#event-handling)
- [Bluetooth Accessories](#bluetooth-accessories)
- [Wi-Fi Accessories](#wi-fi-accessories)
- [Migration from CoreBluetooth](#migration-from-corebluetooth)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Setup and Entitlements

### Info.plist Configuration

Add these keys to the app's Info.plist:

| Key | Type | Purpose |
|---|---|---|
| `NSAccessorySetupSupports` | `[String]` | Required. Array containing `Bluetooth` and/or `WiFi` |
| `NSAccessorySetupBluetoothServices` | `[String]` | Service UUIDs the app discovers (Bluetooth) |
| `NSAccessorySetupBluetoothNames` | `[String]` | Bluetooth names or substrings to match |
| `NSAccessorySetupBluetoothCompanyIdentifiers` | `[Number]` | Bluetooth company identifiers |

The Bluetooth-specific keys must match the values used in `ASDiscoveryDescriptor`.
If the app uses identifiers, names, or services not declared in Info.plist, the
app crashes at discovery time.

### No Bluetooth Permission Required

When an app declares `NSAccessorySetupSupports` with `Bluetooth`, creating a
`CBCentralManager` no longer triggers the system Bluetooth permission dialog.
The central manager's state transitions to `poweredOn` only when the app has
at least one paired accessory via AccessorySetupKit.

## Discovery Descriptors

`ASDiscoveryDescriptor` defines the matching criteria for finding accessories.
The system matches scanned results against all rules in the descriptor to
filter for the target accessory.

### Bluetooth Descriptor

```swift
import AccessorySetupKit
import CoreBluetooth

var descriptor = ASDiscoveryDescriptor()
descriptor.bluetoothServiceUUID = CBUUID(string: "12345678-1234-1234-1234-123456789ABC")
descriptor.bluetoothNameSubstring = "MyDevice"
descriptor.bluetoothRange = .immediate  // Only nearby devices
```

A Bluetooth descriptor requires `bluetoothCompanyIdentifier` or
`bluetoothServiceUUID`, plus at least one of:

- `bluetoothNameSubstring`
- `bluetoothManufacturerDataBlob` and `bluetoothManufacturerDataMask` (same length)
- `bluetoothServiceDataBlob` and `bluetoothServiceDataMask` (same length)

### Wi-Fi Descriptor

```swift
var descriptor = ASDiscoveryDescriptor()
descriptor.ssid = "MyAccessory-Network"
// OR use a prefix:
// descriptor.ssidPrefix = "MyAccessory-"
```

Supply either `ssid` or `ssidPrefix`, not both. The app crashes if both are set.
The `ssidPrefix` must have a non-zero length.

### Bluetooth Range

Control the physical proximity required for discovery:

| Value | Behavior |
|---|---|
| `.default` | Standard Bluetooth range |
| `.immediate` | Only accessories in close physical proximity |

### Support Options

Set `supportedOptions` on the descriptor to declare the accessory's capabilities:

```swift
descriptor.supportedOptions = [.bluetoothPairingLE, .bluetoothTransportBridging]
```

| Option | Purpose |
|---|---|
| `.bluetoothPairingLE` | BLE pairing support |
| `.bluetoothTransportBridging` | Bluetooth transport bridging |
| `.bluetoothHID` | Bluetooth HID device |

## Presenting the Picker

### Creating the Session

Create and activate an `ASAccessorySession` to manage discovery lifecycle:

```swift
import AccessorySetupKit

final class AccessoryManager {
    private let session = ASAccessorySession()

    func start() {
        session.activate(on: .main) { [weak self] event in
            self?.handleEvent(event)
        }
    }

    private func handleEvent(_ event: ASAccessoryEvent) {
        switch event.eventType {
        case .activated:
            // Session ready. Check session.accessories for previously paired devices.
            break
        case .accessoryAdded:
            guard let accessory = event.accessory else { return }
            handleAccessoryAdded(accessory)
        case .accessoryChanged:
            // Accessory properties changed (e.g., display name updated in Settings)
            break
        case .accessoryRemoved:
            // Accessory removed by user or app
            break
        case .invalidated:
            // Session invalidated, cannot be reused
            break
        default:
            break
        }
    }
}
```

### Showing the Picker

Create `ASPickerDisplayItem` instances with a name, product image, and
discovery descriptor, then pass them to the session:

```swift
func showAccessoryPicker() {
    var descriptor = ASDiscoveryDescriptor()
    descriptor.bluetoothServiceUUID = CBUUID(string: "ABCD1234-0000-1000-8000-00805F9B34FB")

    guard let image = UIImage(named: "my-accessory") else { return }

    let item = ASPickerDisplayItem(
        name: "My Bluetooth Accessory",
        productImage: image,
        descriptor: descriptor
    )

    session.showPicker(for: [item]) { error in
        if let error {
            print("Picker failed: \(error.localizedDescription)")
        }
    }
}
```

The picker runs in a separate system process. It shows each matching device
as a separate item. When multiple devices match a given descriptor, the picker
creates a horizontal carousel.

### Setup Options

Configure picker behavior per display item:

```swift
var item = ASPickerDisplayItem(
    name: "My Accessory",
    productImage: image,
    descriptor: descriptor
)
item.setupOptions = [.rename, .confirmAuthorization]
```

| Option | Effect |
|---|---|
| `.rename` | Allow renaming the accessory during setup |
| `.confirmAuthorization` | Show authorization confirmation before setup |
| `.finishInApp` | Signal that setup continues in the app after pairing |

### Product Images

The picker displays images in a 180x120 point container. Best practices:

- Use high-resolution images for all screen scale factors
- Use transparent backgrounds for correct light/dark mode appearance
- Adjust transparent borders as padding to control apparent accessory size
- Test in both light and dark mode

## Event Handling

### Event Types

The session delivers `ASAccessoryEvent` objects through the event handler:

| Event | When |
|---|---|
| `.activated` | Session is active, query `session.accessories` |
| `.accessoryAdded` | User selected an accessory in the picker |
| `.accessoryChanged` | Accessory properties updated (e.g., renamed) |
| `.accessoryRemoved` | Accessory removed from system |
| `.invalidated` | Session invalidated, create a new one |
| `.migrationComplete` | Migration of legacy accessories completed |
| `.pickerDidPresent` | Picker appeared on screen |
| `.pickerDidDismiss` | Picker dismissed |
| `.pickerSetupBridging` | Transport bridging setup in progress |
| `.pickerSetupPairing` | Bluetooth pairing in progress |
| `.pickerSetupFailed` | Setup failed |
| `.pickerSetupRename` | User is renaming the accessory |
| `.accessoryDiscovered` | New accessory found (custom filtering mode) |

### Coordinating Picker Dismissal

When the user selects an accessory, `.accessoryAdded` fires before
`.pickerDidDismiss`. To show custom setup UI after the picker closes, store the
accessory on the first event and act on it after dismissal:

```swift
private var pendingAccessory: ASAccessory?

private func handleEvent(_ event: ASAccessoryEvent) {
    switch event.eventType {
    case .accessoryAdded:
        pendingAccessory = event.accessory
    case .pickerDidDismiss:
        if let accessory = pendingAccessory {
            pendingAccessory = nil
            beginCustomSetup(accessory)
        }
    default:
        break
    }
}
```

## Bluetooth Accessories

After an accessory is added via the picker, use CoreBluetooth to communicate.
The `bluetoothIdentifier` on the `ASAccessory` maps to a `CBPeripheral`.

```swift
import CoreBluetooth

func handleAccessoryAdded(_ accessory: ASAccessory) {
    guard let btIdentifier = accessory.bluetoothIdentifier else { return }

    // Create CBCentralManager — no Bluetooth permission prompt appears
    let centralManager = CBCentralManager(delegate: self, queue: nil)

    // After poweredOn, retrieve the peripheral
    let peripherals = centralManager.retrievePeripherals(
        withIdentifiers: [btIdentifier]
    )
    guard let peripheral = peripherals.first else { return }
    centralManager.connect(peripheral, options: nil)
}
```

Key points:

- `CBCentralManager` state reaches `.poweredOn` only when the app has paired accessories
- Scanning with `scanForPeripherals(withServices:)` returns only
  accessories paired through AccessorySetupKit
- No `NSBluetoothAlwaysUsageDescription` is needed when using AccessorySetupKit
  exclusively

## Wi-Fi Accessories

For Wi-Fi accessories, the `ssid` on the `ASAccessory` identifies the network.
Use `NEHotspotConfiguration` from NetworkExtension to join it:

```swift
import NetworkExtension

func handleWiFiAccessoryAdded(_ accessory: ASAccessory) {
    guard let ssid = accessory.ssid else { return }

    let configuration = NEHotspotConfiguration(ssid: ssid)
    NEHotspotConfigurationManager.shared.apply(configuration) { error in
        if let error {
            print("Wi-Fi join failed: \(error.localizedDescription)")
        }
    }
}
```

Because the accessory was discovered through AccessorySetupKit, joining the
network does not trigger the standard Wi-Fi access prompt.

## Migration from CoreBluetooth

Apps with existing CoreBluetooth-authorized accessories can migrate them to
AccessorySetupKit using `ASMigrationDisplayItem`. This is a one-time operation
that registers known accessories in the new system.

```swift
func migrateExistingAccessories() {
    guard let image = UIImage(named: "my-accessory") else { return }

    var descriptor = ASDiscoveryDescriptor()
    descriptor.bluetoothServiceUUID = CBUUID(string: "ABCD1234-0000-1000-8000-00805F9B34FB")

    let migrationItem = ASMigrationDisplayItem(
        name: "My Accessory",
        productImage: image,
        descriptor: descriptor
    )
    // Set the peripheral identifier from CoreBluetooth
    migrationItem.peripheralIdentifier = existingPeripheralUUID

    // For Wi-Fi accessories:
    // migrationItem.hotspotSSID = "MyAccessory-WiFi"

    session.showPicker(for: [migrationItem]) { error in
        if let error {
            print("Migration failed: \(error.localizedDescription)")
        }
    }
}
```

Migration rules:

- If `showPicker` contains only migration items, the system shows an
  informational page instead of a discovery picker
- If migration items are mixed with regular display items, migration happens
  only when a new accessory is discovered and set up
- Do not initialize `CBCentralManager` before migration completes — doing so
  causes an error and the picker fails to appear
- The session receives `.migrationComplete` when migration finishes

## Common Mistakes

### DON'T: Omit Info.plist keys for Bluetooth discovery

The app crashes if it uses identifiers, names, or services in descriptors that
are not declared in Info.plist.

```swift
// WRONG — service UUID not in NSAccessorySetupBluetoothServices
var descriptor = ASDiscoveryDescriptor()
descriptor.bluetoothServiceUUID = CBUUID(string: "UNDECLARED-UUID")
session.showPicker(for: [item]) { _ in }  // Crash

// CORRECT — declare all UUIDs in Info.plist first
// Info.plist: NSAccessorySetupBluetoothServices = ["ABCD1234-..."]
var descriptor = ASDiscoveryDescriptor()
descriptor.bluetoothServiceUUID = CBUUID(string: "ABCD1234-...")
```

### DON'T: Set both ssid and ssidPrefix

```swift
// WRONG — crashes at runtime
var descriptor = ASDiscoveryDescriptor()
descriptor.ssid = "MyNetwork"
descriptor.ssidPrefix = "My"  // Cannot set both

// CORRECT — use one or the other
var descriptor = ASDiscoveryDescriptor()
descriptor.ssid = "MyNetwork"
```

### DON'T: Initialize CBCentralManager before migration

```swift
// WRONG — migration fails, picker does not appear
let central = CBCentralManager(delegate: self, queue: nil)
session.showPicker(for: [migrationItem]) { error in
    // error is non-nil
}

// CORRECT — wait for .migrationComplete before using CoreBluetooth
session.activate(on: .main) { event in
    if event.eventType == .migrationComplete {
        let central = CBCentralManager(delegate: self, queue: nil)
    }
}
```

### DON'T: Show the picker without user intent

```swift
// WRONG — picker appears unexpectedly on app launch
override func viewDidLoad() {
    super.viewDidLoad()
    session.showPicker(for: items) { _ in }
}

// CORRECT — bind picker to a user action
@IBAction func addAccessoryTapped(_ sender: UIButton) {
    session.showPicker(for: items) { _ in }
}
```

### DON'T: Reuse an invalidated session

```swift
// WRONG — session is dead after invalidation
session.showPicker(for: items) { _ in }  // No effect

// CORRECT — create a new session
let newSession = ASAccessorySession()
newSession.activate(on: .main) { event in
    // Handle events
}
```

## Review Checklist

- [ ] `NSAccessorySetupSupports` added to Info.plist with `Bluetooth` and/or `WiFi`
- [ ] Bluetooth-specific plist keys (`NSAccessorySetupBluetoothServices`, `NSAccessorySetupBluetoothNames`, `NSAccessorySetupBluetoothCompanyIdentifiers`) match descriptor values
- [ ] Session activated before calling `showPicker`
- [ ] Event handler uses `[weak self]` to avoid retain cycles
- [ ] All `ASAccessoryEventType` cases handled, including `@unknown default`
- [ ] Product images use transparent backgrounds and appropriate resolution
- [ ] `ssid` and `ssidPrefix` are never set simultaneously on a descriptor
- [ ] Picker presentation tied to explicit user action, not automatic
- [ ] `CBCentralManager` not initialized until after migration completes (if migrating)
- [ ] `bluetoothIdentifier` or `ssid` from `ASAccessory` used to connect post-setup
- [ ] Invalidated sessions replaced with new instances
- [ ] Accessory removal events handled to clean up app state

## References

- Extended patterns (custom filtering, batch setup, removal handling, error recovery): [references/accessorysetupkit-patterns.md](references/accessorysetupkit-patterns.md)
- [AccessorySetupKit framework](https://sosumi.ai/documentation/accessorysetupkit)
- [ASAccessorySession](https://sosumi.ai/documentation/accessorysetupkit/asaccessorysession)
- [ASDiscoveryDescriptor](https://sosumi.ai/documentation/accessorysetupkit/asdiscoverydescriptor)
- [ASPickerDisplayItem](https://sosumi.ai/documentation/accessorysetupkit/aspickerdisplayitem)
- [ASAccessory](https://sosumi.ai/documentation/accessorysetupkit/asaccessory)
- [ASAccessoryEvent](https://sosumi.ai/documentation/accessorysetupkit/asaccessoryevent)
- [ASMigrationDisplayItem](https://sosumi.ai/documentation/accessorysetupkit/asmigrationdisplayitem)
- [Discovering and configuring accessories](https://sosumi.ai/documentation/accessorysetupkit/discovering-and-configuring-accessories)
- [Setting up and authorizing a Bluetooth accessory](https://sosumi.ai/documentation/accessorysetupkit/setting-up-and-authorizing-a-bluetooth-accessory)
- [Meet AccessorySetupKit — WWDC24](https://sosumi.ai/videos/play/wwdc2024/10203/)
