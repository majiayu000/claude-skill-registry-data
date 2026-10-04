---
name: ble
description: Bluetooth context for the Megahub project. Use when working on BLE GATT server, Classic Bluetooth HID host, Web Bluetooth API integration, btremote library, connection handling, or any Bluetooth-related firmware code.
---

# Bluetooth Architecture — Megahub ESP32

The project uses **both** BLE and Classic Bluetooth simultaneously (BTDM dual-mode).

| Type | Purpose | Library |
|------|---------|---------|
| BLE (GATT server) | Web Bluetooth API ↔ firmware | `lib/btremote/` |
| Classic BT (HID host) | Gamepad/keyboard/mouse input | `lib/btremote/` |

---

## BLE GATT Server

**Service UUID**: `4fafc201-1fb5-459e-8fcc-c5c9c331914b`

| Characteristic | UUID | Direction | Type |
|----------------|------|-----------|------|
| REQUEST | `beb5483e-36e1-4688-b7f5-ea07361b26a8` | Browser → Firmware | Write |
| RESPONSE | `1c95d5e3-d8f7-413a-bf3d-7a2e5d7be87e` | Firmware → Browser | Notify |
| EVENT | `d8de624e-140f-4a22-8594-e2216b84a5f2` | Firmware → Browser | Notify |
| CONTROL | `f78ebbff-c8b7-4107-93de-889a6a06d408` | Firmware → Browser | Indicate |

- **Indications vs Notifications**: CONTROL uses indications (require client ACK). RESPONSE/EVENT use notifications.
- **MTU**: Default 23 bytes on connect. Firmware sends `MTU_INFO` notification immediately after connect, then again after negotiation (up to 517 bytes).
- From real device logs: MTU negotiates to 514/517 bytes reliably.

## BLE Rules (never violate)

- **Never block in BLE callbacks** — they run in the BLE stack task context
- **Always check `isConnected()`** before sending notifications/indications
- **Reconnection**: Browser handles reconnect via `device.gatt.connect()` — firmware must keep advertising
- **Multiple connections**: Each consumes ~30KB heap — the BT stack alone drops free heap from ~140KB to ~75KB
- **BLE callbacks** → post work to a queue, handle in `BTMsgProcessor` task
- **Indication failures** (status=132) during startup are normal — the client ACK pipeline needs time to stabilize after connect

## Classic Bluetooth (HID Host)

- Only for HID devices: gamepads, keyboards, mice
- Auto-pairing enabled (IO capability: NONE, PIN: "0000")
- HID events processed in `HIDEventTask` (priority 5, separate from BLE stack)
- **Never block in HID callback** — post to queue
- Pairing state is persisted in NVS; handle removal gracefully

## Startup Sequence

From real device logs, BT init order:
1. BT controller starts in BTDM dual-mode (`esp_bt_controller_enable`)
2. Classic GAP callback registered
3. Classic scan mode: connectable + discoverable
4. HID Host initialized → waits for `ESP_HIDH_INIT_EVT`
5. Bluedroid BLE init → waits for GATTS registration
6. GATT service + characteristics created (handles 40–51)
7. Advertising started
8. Total heap consumed by BT stack: ~65KB

## Message Protocol (BLE)

- **5-byte fragment header**: `[type, messageId, fragmentNum(2), flags]`
- **Fragmentation**: automatic for all requests/responses
- **Streaming file upload**: sliding window of 8 chunks, waits for ACK before advancing
- **App request types**: from logs — type 10=ready-for-events, type 7=get-projects, type 8=get-autostart, type 9=set-autostart, type 2=get-file, type 6=execute-lua

## Debugging BLE

```bash
# Enable HCI logs in ESP-IDF menuconfig for raw BLE packet capture
# Watch for these in serial log:
# [INFO] handleGattsConnect()   — client connected
# [INFO] handleGattsMTU()       — MTU negotiated
# [WARN] handleGattsConfirm()   — indication failed (status=132 at startup is normal)
```
