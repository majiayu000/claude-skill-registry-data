---
name: bluetooth-le
description: Use when assessing Bluetooth Low Energy devices on authorized
  engagements, such as beacons, locks, wearables, or IoT sensors in scope.
  Covers enabling and verifying the adapter with BlueZ, passive
  advertisement sniffing, active scanning, connecting to GATT servers,
  enumerating services and characteristics, reading and writing values
  safely, and capturing traffic for Wireshark analysis. Use when the scope
  includes BLE peripherals and you need to map their attack surface before
  protocol or firmware testing.
version: 1.0.0
domain: network
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [recon-active]
tools:
  - name: BlueZ
    version: "5.77"
  - name: Wireshark
    version: "4.4"
  - name: Python
    version: "3.12"
---

Bluetooth Low Energy (BLE) is the radio in door locks, asset tags, medical
sensors, and countless IoT gadgets. Many BLE devices trust any central that
connects: they expose readable characteristics, accept writes without
authentication, and leak identifiers in advertisements. This skill covers
authorized BLE assessment with BlueZ on Linux: verifying the adapter,
sniffing advertisements, scanning, connecting to GATT servers, enumerating
services and characteristics, and reading or writing values with care. It
stops at the GATT layer; firmware extraction and protocol reverse
engineering build on what you map here. All testing targets systems you have
written permission to test.

## Quick Workflow

1. Verify the Bluetooth adapter is present, powered, and supports BLE.
2. Sniff advertisements passively to list nearby devices without
   connecting.
3. Run an active scan to get names, addresses, and signal strength.
4. Pick the in-scope target and connect to its GATT server.
5. Enumerate primary services, characteristics, and descriptors.
6. Read readable characteristics and note identifiers, versions, and
   state.
7. Test writes only on characteristics where the scope allows it, and
   restore any changed value.
8. Save captures and notes for the report.

## 1. Verify the adapter

Use a Bluetooth 4.0 or newer adapter. Many built-in laptop radios work for
BLE, but a dedicated USB dongle gives better range and cleaner captures.

```bash
# Adapter presence and version
hciconfig -a
bluetoothctl show

# Power on and enable LE
bluetoothctl power on
sudo hciconfig hci0 up
sudo hciconfig hci0 leadv 2>/dev/null; echo "LE check done"

# Confirm the kernel sees BLE support
hciconfig hci0 | grep -i "BD Address"
btmon --version 2>/dev/null || echo "install bluez for btmon captures"
```

If `hciconfig` shows the interface DOWN, bring it up and retry. If the
adapter is Bluetooth 2.1 only (no LE), replace it; classic Bluetooth tools
do not speak BLE.

## 2. Sniff advertisements passively

BLE devices broadcast advertisements with their address, flags, local
name, and service UUIDs. Passive sniffing lists them without connecting,
which is the quietest possible recon.

```bash
# Live advertisement dump with btmon (best detail)
sudo btmon | tee /tmp/btmon-adv.log

# In another terminal, start a passive scan so advertisements flow
sudo hcitool lescan --passive > /tmp/lescan-passive.txt 2>&1 &
sleep 60; sudo pkill hcitool; cat /tmp/lescan-passive.txt | sort -u
```

Watch for: static addresses (a privacy problem), the complete local name
(often the product model), manufacturer specific data (sometimes contains
serial numbers or state), and service UUIDs that hint at the device role
(heart rate, battery, custom services).

```bash
# bettercap BLE passive recon as an alternative
sudo bettercap -iface hci0 -eval "ble.recon on; sleep 30; ble.show; ble.recon off"
```

MAC randomization note: modern phones and some peripherals rotate their
advertising address. If the target address keeps changing, identify the
device by its name and service UUIDs instead of the MAC, and note the
randomization as a (weak but real) privacy control.

## 3. Active scan and target selection

Active scanning asks each advertiser for its scan response, which often
adds the full device name.

```bash
# Active LE scan for 60 seconds, de-duplicated
sudo timeout 60 hcitool lescan | sort -u | tee /tmp/lescan.txt

# bluetoothctl interactive alternative
bluetoothctl scan on
# ... wait, then: bluetoothctl scan off; bluetoothctl devices
```

Match what you see against the scope: device name, address, or service
UUID. Record the target MAC, the RSSI (signal strength, closer to zero is
stronger), and the address type (public vs random) shown by btmon.

## 4. Connect and enumerate GATT

Connect with `bluetoothctl` or `gatttool`. Then list primary services and
walk each one for characteristics.

```bash
# Connect (replace with the target MAC)
bluetoothctl connect AA:BB:CC:DD:EE:FF

# gatttool interactive session alternative
gatttool -b AA:BB:CC:DD:EE:FF -I
# Inside gatttool: connect
```

```bash
# List primary services by UUID (handles 0x0001-0xffff)
gatttool -b AA:BB:CC:DD:EE:FF --primary

# Example output lines:
# attr handle: 0x0001, end grp handle: 0x0007 uuid: 00001800-0000-1000-8000-00805f9b34fb
# attr handle: 0x0008, end grp handle: 0x000b uuid: 0000180a-0000-1000-8000-00805f9b34fb

# List characteristics within one service handle range
gatttool -b AA:BB:CC:DD:EE:FF --characteristics --start-handle=0x0008 --end-handle=0x000b
```

Standard service UUIDs decode immediately: `0x1800` is Generic Access
(device name lives here), `0x1801` Generic Attribute, `0x180A` Device
Information (model, serial, firmware version), `0x180F` Battery. Custom
128-bit UUIDs are vendor specific and are where the interesting logic
hides.

```bash
# Read the device name and appearance from Generic Access
gatttool -b AA:BB:CC:DD:EE:FF --char-read -a 0x0003

# Dump Device Information characteristics (firmware version is gold)
for h in 0x0009 0x000a 0x000b; do
  echo "=== handle $h ==="
  gatttool -b AA:BB:CC:DD:EE:FF --char-read -a $h 2>/dev/null | head -2
done
```

## 5. Read and write characteristics safely

Read every characteristic that allows it and decode the bytes. Writes go
only where the scope allows, one at a time, with the original value saved
first.

```bash
# Read a characteristic by handle, hex and ASCII
gatttool -b AA:BB:CC:DD:EE:FF --char-read -a 0x0012

# Read by UUID when you know it (example: battery level 0x2A19)
gatttool -b AA:BB:CC:DD:EE:FF --char-read --uuid 0x2A19

# Decode hex output locally
echo "4c 6f 63 6b 65 64" | xxd -r -p; echo
```

```bash
# Write test: read first, write a test value, read back, restore
gatttool -b AA:BB:CC:DD:EE:FF --char-read -a 0x0014 > /tmp/orig.txt
gatttool -b AA:BB:CC:DD:EE:FF --char-write-req -a 0x0014 -n "test"
gatttool -b AA:BB:CC:DD:EE:FF --char-read -a 0x0014
ORIG=$(cut -d: -f2 /tmp/orig.txt | tr -d ' ')
gatttool -b AA:BB:CC:DD:EE:FF --char-write-req -a 0x0014 -n "$ORIG"
```

Never write to characteristics that control physical state (locks, motors,
medical dosing) unless the scope explicitly authorizes it and the client
understands the risk. A write that unlocks a door in a live building is
not a finding, it is an incident.

Subscribe to notifications to watch live data:

```bash
# Enable notifications on a characteristic (write 0x0001 to its CCCD)
gatttool -b AA:BB:CC:DD:EE:FF --char-write-req -a 0x0013 -n 0100 --listen
```

## 6. Capture traffic for analysis

Capture the full session with btmon and open it in Wireshark for the
report and for deeper protocol work.

```bash
# Capture everything during your GATT session
sudo btmon -w /tmp/ble-session.log &
BTMON=$!
# ... run your gatttool session ...
sudo kill $BTMON

# Convert for Wireshark if needed, or open the log directly
wireshark /tmp/ble-session.log &
```

In Wireshark, filter `btatt` for GATT traffic and `btsmp` for pairing.
Look for: pairing requests with `NoInputNoOutput` (Just Works pairing,
vulnerable to MITM), long term keys exchanged in clear, and sensitive
data in notification payloads.

## Edge cases

- The adapter sees nothing. Confirm BLE support (`hciconfig hci0
  features`), move within a few meters, and check the device is actually
  advertising (many only advertise when a button is pressed or on boot).
- Connection drops immediately. The peripheral may enforce a bonded
  relationship or a short supervision timeout; retry, and check btmon for
  the disconnect reason code.
- `gatttool` is deprecated or missing. Modern BlueZ favors
  `bluetoothctl` with `menu gatt`; the concepts are identical, only the
  commands differ.
- Handles shift between connections. Some devices randomize attribute
  handles; re-run `--primary` each session instead of hardcoding handles.
- The device requires pairing. Try Just Works first (no PIN); if it
  demands a PIN or out-of-band pairing, note the requirement as a
  positive control and stop unless the scope covers pairing attacks.
- Encrypted characteristics return errors on read. That indicates real
  access control; document it as a good finding, not a failure.

## Escalation

- Reads reveal a debug or test service. Enumerate it fully; test services
  often lack the access checks the main services have.
- A characteristic accepts writes that change device behavior. Prove it
  with the smallest reversible change, restore the value, and report the
  impact precisely.
- Notifications leak sensitive data. Capture a session, decode the
  payloads, and show what a passive sniffer in range would learn.
- The device uses Just Works pairing. Demonstrate a MITM with two
  adapters only if the scope allows active attacks; otherwise report the
  weak pairing method with a capture as evidence.
- You need long range. A directional antenna or a higher gain dongle
  extends practical BLE range well beyond the nominal 10 meters; note the
  tested distance in the report.

## Detection and defender view

BLE attacks are hard to detect: passive sniffing is invisible, and
connection attempts look like normal central behavior. Defenders can watch
for repeated connection and pairing attempts from unknown centrals in
gateway logs, and for deauth-style interference on the 2.4 GHz band. The
durable fixes live in the device design: require authenticated pairing
(passkey or numeric comparison, never Just Works for sensitive actions),
encrypt characteristics that carry personal or control data, use resolvable
private addresses to stop tracking, minimize advertisement data, and strip
debug services from production firmware. For deployed fleets, monitor for
unknown centrals holding long connections to critical peripherals.

## Key references

- MITRE ATT&CK T1046 (Network Service Discovery): BLE scanning maps to
  service discovery on a radio medium.
- CWE-200 (Exposure of Sensitive Information): data in advertisements and
  readable characteristics.
- CWE-306 (Missing Authentication for Critical Function): unauthenticated
  GATT writes.
- CWE-327 (Use of a Broken or Risky Cryptographic Algorithm): Just Works
  pairing and unencrypted links.
- Bluetooth Core Specification 5.x, Vol 3 Part G (GATT) and Part H (SMP).
- BlueZ documentation: http://www.bluez.org/
- Wireshark Bluetooth wiki: https://wiki.wireshark.org/Bluetooth
