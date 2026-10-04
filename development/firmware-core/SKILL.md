---
name: firmware-core
description: Core firmware context for the Megahub ESP32 project. Use when working on PlatformIO configuration, build scripts, library structure, main.cpp, or general ESP32 firmware development. Covers build system, project structure, common pitfalls, and debugging.
---

# Firmware Core — Megahub ESP32

## Build System

**PlatformIO configuration** — see `platformio.ini`:
- Environment: `esp-wrover-kit`
- Framework: Arduino + ESP-IDF hybrid
- Partition table: `custom_4mb_noota.csv` (no OTA, maximizes app partition)
- Pre-build scripts (in order):
  1. `gitversion.py` — injects git hash into firmware
  2. `buildfrontend.py` — runs `npm run build` for the selected frontend mode
  3. `embedfiles.py` — gzips and embeds frontend files into firmware as C arrays

**Serial monitor**: 115200 baud. Log level controlled by `CORE_DEBUG_LEVEL` (currently 2).

**Logging macros** — always use these, never `Serial.print()`:
```cpp
INFO("Free heap: %d bytes", ESP.getFreeHeap());
WARN("Something unexpected: %d", value);
ERROR("Critical failure in %s", __func__);
```

---

## Library Structure

```
lib/
  btremote/       BLE server (Web Bluetooth API) + Classic BT HID host (gamepads)
  commands/       Command processing system — all device operations use this pattern
  configuration/  WiFi & system configuration persistence
  hubwebserver/   HTTP server using PsychicHttp library
  imu/            MPU6050 IMU — I²C, requires proper init sequence
  lpfuart/        LEGO Powered Up UART protocol implementation
  lua/            Lua 5.4 interpreter (embedded, constrained memory)
  megahub/        Main application — wires all libraries together
  portstatus/     Port status tracking and JSON serialization
  inputdevices/   Gamepad/HID input device abstraction
  statusmonitor/  System health monitoring (heap, tasks)
```

## Key Architecture: Command Pattern

All device operations go through `lib/commands/`. This provides:
- Serialization of requests from multiple sources (BLE, Web)
- Consistent error handling and response formatting
- Command queuing for rate-limited devices

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| BLE race condition | Use proper task synchronization (mutex/queue) |
| Stack overflow | Use `uxTaskGetStackHighWaterMark()`, move large vars to heap |
| String heap fragmentation | Use `std::string::reserve()` or fixed buffers |
| Blocking in BLE callback | Post to a queue, handle in application task |
| Lua crash | Wrap ALL Lua execution in `lua_pcall()` |
| LEGO device timeout | Send keepalive commands, handle wake-up sequence |
| IMU init failure | Always include required delays in MPU6050 init sequence |
| Memory leak | Every `new`/`malloc` must have matching `delete`/`free` |

---

## Debugging

```bash
pio device monitor --baud 115200   # Serial monitor
pio test                           # Run unit tests
pio run                            # Build only (no upload)
```

**Crash analysis**: Enable ESP32 exception decoder in PlatformIO. Stack traces decode to source lines.

**Runtime monitoring**:
```cpp
INFO("Free heap: %d bytes, Free PSRAM: %d bytes",
     ESP.getFreeHeap(), ESP.getFreePsram());
INFO("Task stack HWM: %d words", uxTaskGetStackHighWaterMark(NULL));
```

**Known heap budget** (from real device logs):
- After IMU init: ~170KB free heap
- After Lua state creation: ~140KB free heap
- After BT stack start: ~75KB free heap
- PSRAM: ~4.1MB available (confirmed present on this board)
