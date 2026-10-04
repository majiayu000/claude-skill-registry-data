---
name: memory-freertos
description: Memory management and FreeRTOS context for the Megahub ESP32 project. Use when dealing with heap allocation, stack size, task creation, inter-task communication, semaphores, queues, or any ESP32 memory constraints.
---

# Memory Management & FreeRTOS — Megahub ESP32

## Memory Budget (real device measurements)

| Point in startup | Free heap |
|-----------------|-----------|
| After IMU init | ~170 KB |
| After Lua state creation | ~140 KB |
| After LEGO motor init | ~140 KB |
| After configuration load | ~139 KB |
| After BT stack start | ~76 KB |
| After BLE characteristics setup | ~76 KB |
| During BLE connection (connected) | ~63–73 KB |

**PSRAM**: ~4.1 MB available (confirmed present on this board — `ESP.getFreePsram()`).

BT stack alone consumes ~65 KB of heap. Every BLE connection consumes an additional ~30 KB.

---

## Memory Rules

- **Stack**: Never allocate large arrays as local variables. Use `static`, heap, or PSRAM.
- **Heap**: Minimize `new`/`malloc`. Every allocation needs a matching `delete`/`free`.
- **Strings**: Avoid `String +=` loops. Prefer `std::string::reserve()` or fixed `char[]` buffers.
- **PSRAM**: Available, but don't assume — always check. Use for large buffers if needed.
- **Constants**: Use `const` and `PROGMEM` for large constant data to keep it in flash.
- **Lua VM**: Runs in heap. Large scripts reduce available heap for everything else.

---

## FreeRTOS Task Reference

Known tasks and their stack high-water marks (from real device logs):

| Task | Priority | Stack HWM (words) | Notes |
|------|----------|-------------------|-------|
| `loopTask` | 1 | 272 | Arduino main loop |
| `BTMsgProcessor` | 2 | 2968–7528 | Processes BLE messages |
| `HIDEventTask` | 5 | 1920 | Classic BT HID events |
| `PortStatus` | 1 | 1420 | LEGO port status reporting |
| `StatusMonitor` | 1 | 2452 | Heap/task monitoring |
| `Device monitor` | 1 | 1776 | Lua thread for device monitoring |
| `BTU_TASK` | 20 | 3624–4988 | BT stack internal |
| `BTC_TASK` | 19 | 4328–4364 | BT stack internal |
| `hciT` | 22 | 1516–1544 | BT HCI layer |
| `btController` | 23 | 2088 | BT controller |
| `esp_timer` | 22 | 4048 | ESP timer service |
| `ipc0/1` | 24 | 356/476 | IPC (highest priority) |

⚠ `loopTask` HWM of 272 words is critically low — avoid adding stack usage to the main loop.

---

## FreeRTOS Rules

- **Mutexes**: Always use `xSemaphoreTake` with a timeout — never block indefinitely
- **Task stacks**: Monitor with `uxTaskGetStackHighWaterMark()`. Stack overflow = silent crash.
- **Inter-task communication**: Use queues or semaphores — not global variables without synchronization
- **BLE callbacks**: Run in BLE task context — post work to a queue, handle in application task
- **Never block** in BLE callbacks, HID callbacks, or ISRs
- **Task priorities**: BT stack tasks run at 19–24. Application tasks at 1–5. Don't starve the BT stack.

---

## Monitoring Pattern

```cpp
// Log heap + PSRAM
INFO("Free heap: %d bytes, Free PSRAM: %d bytes",
     ESP.getFreeHeap(), ESP.getFreePsram());

// Log task stack (for current task)
INFO("Stack HWM: %d words", uxTaskGetStackHighWaterMark(NULL));

// Log all task stacks (use vTaskList for full snapshot)
```
