---
name: documentation
description: Documentation structure and maintenance rules for the Megahub project. Use whenever making user-facing changes — adding features, changing behavior, fixing hardware compatibility, or modifying configuration. Describes which files to update, the README structure, and writing style.
---

# Documentation — Megahub Project

## File Map

| File | Audience | Maintained by | Update trigger |
|------|----------|---------------|----------------|
| `README.md` | End users — builders, makers, beginners | AI (on every user-facing change) | Any change to features, hardware support, configuration, or user workflow |
| `BLOCKS.md` | End users — visual programmers | Auto-generated (`npm run generate-docs` in `frontend/`) | Any Blockly block added, removed, or modified |
| `HUBAPI.md` | Developers using WiFi/REST mode | Human or AI | Any REST endpoint added or changed in `lib/hubwebserver/` |
| `LUMP.md` | Protocol implementers | Human | LEGO UART protocol changes only |
| `CLAUDE.md` | AI assistant | Human | Architecture changes, new conventions |

**Never edit `BLOCKS.md` manually** — it is fully auto-generated and will be overwritten.

---

## README.md Structure

The README is the primary user document. It must always contain these sections in this order:

```
1. Introduction (project overview, 2–3 sentences)
2. Key Features (bullet list — what the device can do)
3. Screenshots (visual overview — keep current)
4. Hardware Photos
5. Getting Started
   5a. Prerequisites
   5b. Building the Firmware
   5c. Flashing the Board
   5d. First Boot and Connection
6. Hardware Reference
   6a. LEGO Device Ports (ports 0–3, connector type, LUMP protocol)
   6b. GPIO Pins (FastLED pin options, SD card pins, I2C)
   6c. Supported LEGO Devices
7. Using the IDE
   7a. Connecting (BT mode — Web Bluetooth, supported browsers)
   7b. Creating a Project
   7c. Programming with Blockly
   7d. Running and Stopping Programs
   7e. Autostart
8. WiFi Mode
   8a. Switching from BT to WiFi
   8b. config.json format
   8c. Accessing the Web UI
9. Gamepad Support
   9a. Pairing a gamepad
   9b. Supported gamepads (8BitDo M30 tested)
   9c. Blockly blocks available
10. Hardware Features
    10a. LEGO Powered Up support
    10b. FastLED/NeoPixel addressable LEDs
    10c. IMU (MPU6050) — yaw/pitch/roll, acceleration
    10d. SD Card storage
11. Troubleshooting
    11a. Bluetooth not connecting
    11b. Device not found
    11c. LEGO device not responding
    11d. Serial monitor for debugging
12. Documentation (links to BLOCKS.md, HUBAPI.md, LUMP.md)
13. License / Contributing (if applicable)
```

---

## Writing Style Rules

**Audience**: Makers and robotics enthusiasts. Assume they know hardware basics but not necessarily ESP32 or Bluetooth internals.

- **Active voice**: "Click Connect" not "The Connect button should be clicked"
- **Concrete steps**: Use numbered lists for procedures, not prose paragraphs
- **No jargon without explanation**: "BLE (Bluetooth Low Energy)" on first use, then "BLE"
- **No internal implementation details**: Users don't need to know about FreeRTOS tasks, GATTS, or `lua_pcall()`. Focus on what they can *do*, not how it works inside.
- **Code blocks for commands and config**: Always use fenced code blocks
- **Present tense**: "The device starts in Bluetooth mode" not "The device will start"
- **Remove stale "coming soon" notes**: If a feature doesn't exist yet, don't mention it

---

## Key Facts for README Content

### Hardware (verified from source code)

**LEGO ports**: 4 ports (0–3), via SC16IS752 I2C-to-UART bridge. LEGO Powered Up UART protocol. Motor speed: -127 to +127.

**FastLED GPIO options**: 13, 16, 17, 25, 26, 27, 32, 33 (NeoPixel/WS2812B compatible)

**SD card SPI pins**: CLK=18, MOSI=23, MISO=19, CS=4

**IMU outputs**: YAW, PITCH, ROLL (degrees), ACCELERATION_X/Y/Z (m/s²). Update rate: 100ms.

**Gamepad**: Bluetooth Classic HID. 16 buttons, D-pad, 2 analog sticks (left/right X/Y, range -32768..32767). Tested: 8BitDo M30.

### WiFi configuration (`/config.json` on SD card)
```json
{
  "bluetoothEnabled": true,
  "wifiEnabled": false,
  "ssid": "YourNetwork",
  "pwd": "YourPassword"
}
```
WiFi web server runs on port 80. Default: BT mode.

### Autostart (`/autostart.json` on SD card)
```json
{ "project": "your-project-id" }
```
Set via the IDE (project list → autostart toggle). Persists across reboots.

### Supported browsers (Web Bluetooth API)
Chrome, Edge, Opera — desktop only. Firefox and Safari are **not** supported.

---

## Update Rules for AI

When making **any** code change, check:

1. **New feature or changed behavior** → update the matching README section. Add the feature to "Key Features" if it's user-visible.
2. **New Blockly block** → run `npm run generate-docs` in `frontend/` to regenerate `BLOCKS.md`. Do not manually edit BLOCKS.md.
3. **New REST endpoint** → update `HUBAPI.md` with the endpoint signature, request/response format, and example.
4. **New configuration option** → update both README.md (user-facing explanation) and `HUBAPI.md` if it's exposed via API.
5. **Removed or renamed feature** → remove stale references from README. Never leave "coming soon" for something that was dropped.
6. **Bug fix with user-visible impact** → add to Troubleshooting if it was a common problem.

When updating README:
- Keep existing sections intact unless they're wrong
- Add new content in the correct section (use the structure above)
- Do not restructure the whole document for a small change — find the right section and update it
