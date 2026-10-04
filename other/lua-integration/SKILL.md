---
name: lua-integration
description: Lua scripting context for the Megahub project. Use when working on Lua script execution, Lua bindings, libluahub, Lua error handling, Lua threads, or the Blockly-to-Lua code generation pipeline.
---

# Lua Integration — Megahub ESP32

## Overview

- **Lua 5.4** embedded interpreter
- All custom Lua bindings: `lib/megahub/src/libluahub.cpp`
- Lua state created in `lib/megahub/src/megahub.cpp` → `newLuaState()`
- Scripts stored on LittleFS/SD, loaded on demand
- Execution triggered via BLE command (app request type 6 = execute-lua)

---

## Execution Flow

```
BLE request (type 6, Lua code payload)
  → megahub.cpp: executeLUACode()
      → newLuaState()       (~20ms, opens standard libs + registers custom bindings)
      → lua_pcall()         (executes the script)
      → cleanup Lua state
```

From real device logs: execution of a motor control script completes in ~62ms.

---

## Lua Bindings (`libluahub.cpp`)

Key functions available in Lua scripts:

| Lua function | Purpose |
|-------------|---------|
| `hub.init(fn)` | Register initialization block (runs first) |
| `hub.startthread(name, fn, stackSize)` | Start a FreeRTOS task running a Lua coroutine |

**Threads**: `hub.startthread()` creates a FreeRTOS task. Stack size is specified in bytes (e.g., 4096). The thread runs as a Lua coroutine and should yield periodically.

---

## Critical Rules

- **Always** wrap Lua execution in `lua_pcall()` — never use `lua_call()` in production code
- **Always** install an error handler before pcall to get useful error messages
- **Never** let Lua errors propagate unhandled — they will crash the firmware
- **Lua threads via `hub.startthread()`** consume both FreeRTOS stack and Lua VM heap
- The Lua VM runs in the main heap; large scripts reduce heap available for BLE, LEGO, etc.
- Long-running scripts must yield periodically — a tight Lua loop will starve other tasks

---

## Error Handling Pattern

```cpp
// Safe Lua execution (in megahub.cpp)
lua_State* L = newLuaState();
if (!L) { ERROR("Failed to create Lua state"); return; }

int result = lua_pcall(L, 0, 0, 0);
if (result != LUA_OK) {
    ERROR("Lua error: %s", lua_tostring(L, -1));
    lua_pop(L, 1);
}
// Always close state when done
lua_close(L);
```

---

## Blockly → Lua Pipeline

1. User builds program in Blockly editor (browser)
2. Blockly generates Lua code (custom generators in `frontend/src/components/blockly/`)
3. Lua code sent to firmware via BLE (streaming upload or direct execute)
4. Firmware executes via `executeLUACode()`

The generated Lua code always follows a structure with `hub.init()` and optionally `hub.startthread()` for background monitoring loops.

---

## Memory Impact

From device logs:
- Creating a new Lua state: ~30KB heap consumed (~170KB → ~140KB)
- A script with `hub.startthread("Device monitor", fn, 4096)` adds another ~4KB stack + Lua coroutine overhead
