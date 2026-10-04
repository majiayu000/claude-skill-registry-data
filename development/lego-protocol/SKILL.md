---
name: lego-protocol
description: LEGO Powered Up protocol context for the Megahub project. Use when working on LEGO device communication, lpfuart library, UART parsing, motor control, sensor modes, device initialization, or debugging UART noise/corruption issues.
---

# LEGO Powered Up Protocol — Megahub ESP32

## Hardware Setup

- **UART chip**: SC16IS752 (I²C-to-dual-UART bridge)
- **Ports**: 0–3 (physical LEGO connectors)
- **Baud rate**: negotiated per device during handshake (typically starts at low speed, switches to 115200)
- **Library**: `lib/lpfuart/` — `legodevice.cpp`, `lumpparser.cpp`, `SC16IS752serialadapter.cpp`

---

## Device Initialization Sequence

Devices send identification messages on connect. **Never skip any step.**

1. `LUMP_CMD_TYPE` — device reports its type ID and name
2. `LUMP_CMD_MODES` — device reports number of supported modes
3. `LUMP_CMD_SPEED` — device requests baud rate to switch to
4. `LUMP_CMD_VERSION` — device reports firmware + hardware versions
5. `LUMP_INFO_NAME/RAW/PCT/SI/UNITS/MAPPING/FORMAT` — per-mode metadata (repeats for each mode)
6. `LUMP_INFO_MODE_COMBOS` — supported mode combinations
7. `finishHandshake()` — switch to negotiated baud rate (e.g., 115200)
8. `selectMode()` — set default operating mode

**Example (BOOST Interactive Motor, device ID 0x26):**
- 4 modes: POWER (0), SPEED (1), POS (2), TEST (3)
- Default mode: 2 (POS — position feedback)
- Handshake takes ~3 seconds from connect to ready

---

## Protocol Rules

- **Command rate limit**: ~20ms minimum between commands for most devices
- **Device timeout**: some devices sleep if no command within ~1 second — send keepalives
- **Byte order**: LEGO uses **little-endian** in most messages
- **Port cleanup**: on disconnect, cancel all pending commands for that port
- **Mode selection**: always use device type to validate supported modes before `CMD_SELECT`

---

## UART Corruption from Motor Noise

**This is a known hardware issue.** When motors run, EMI corrupts the UART RX line.

### Symptoms
- `[WARN] LUMP sync lost after N good frames (checksum expected=0xXX actual=0xYY)`
- Repeated `0xD2` bytes in discarded data (spurious detections of LEGO header byte)
- `uartOvr=1` in parser stats — SC16IS752 FIFO overflow

### Root Cause
Motor control via M1/M2 generates high-frequency switching noise → current spikes → EMI coupling into UART RX trace → SC16IS752 FIFO fills faster than ESP32 reads via I²C.

### Software Mitigations (already implemented)
- UART read batch size increased to 64 bytes per call (reduces FIFO overrun probability)
- `delayMicroseconds(100)` after motor speed changes (allows transients to settle)
- FIFO overrun counter tracked and logged as `uartOvr`

### Hardware Fixes (if software mitigations are insufficient)

| Priority | Fix | Expected improvement |
|----------|-----|---------------------|
| 1 (best) | 68–100pF NP0/C0G ceramic cap on UART RX pin to GND | 50–70% error reduction |
| 2 | Clip-on ferrite bead on RX wire near PCB | 40–60% error reduction |
| 3 | 100Ω + 100pF RC filter on UART TX | 10–20% additional |
| 4 | 100nF decoupling cap on SC16IS752 VCC pin | standard practice |

**Target**: < 5 sync recoveries per minute with motor at 100% speed.

### Parser Recovery

The parser (`lumpparser.cpp`) handles corruption gracefully:
- Detects checksum mismatch
- Scans forward to find next valid frame header
- Logs discarded bytes
- Recovers without device reset

Good state: `Parser: ok=XXX csErr=0 discarded=0 recoveries=0 uartOvr=0`

---

## Debugging LEGO

Watch parser stats in serial log (logged every ~5 seconds):
```
[INFO] logParserStats() - Parser: ok=138 csErr=0 discarded=0 recoveries=0 overflow=0 unknownSys=0 invalidSize=0 uartOvr=1
```

| Field | Meaning |
|-------|---------|
| `ok` | Good frames parsed |
| `csErr` | Checksum errors |
| `discarded` | Bytes thrown away during resync |
| `recoveries` | Number of sync-loss recovery events |
| `uartOvr` | SC16IS752 FIFO overflow count |
