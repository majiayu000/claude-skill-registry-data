---
name: "plc"
version: "1.0.0"
description: "PLC programming reference — ladder logic, structured text, function blocks, and IEC 61131-3 standards. Use when writing PLC programs, debugging rungs, or reviewing automation logic."
author: "BytesAgain"
homepage: "https://bytesagain.com"
source: "https://github.com/bytesagain/ai-skills"
tags: [plc, industrial, automation, ladder-logic, iec-61131, structured-text]
category: "industrial"
---

# PLC — Programmable Logic Controller Reference

Quick-reference skill for PLC programming concepts, IEC 61131-3 languages, common instruction sets, and troubleshooting patterns.

## When to Use

- Writing or reviewing ladder logic programs
- Debugging PLC faults and I/O issues
- Choosing between Structured Text, Function Block, or Ladder
- Looking up IEC 61131-3 data types and timer/counter instructions
- Setting up communication protocols (Modbus, EtherNet/IP, Profinet)

## Commands

### `intro`

```bash
scripts/script.sh intro
```

Overview of PLC architecture — CPU, I/O modules, scan cycle, memory areas.

### `languages`

```bash
scripts/script.sh languages
```

IEC 61131-3 programming languages: Ladder Diagram (LD), Structured Text (ST), Function Block Diagram (FBD), Instruction List (IL), Sequential Function Chart (SFC).

### `instructions`

```bash
scripts/script.sh instructions
```

Common PLC instructions — contacts, coils, timers (TON/TOF/TP), counters (CTU/CTD), math, comparison, move.

### `datatypes`

```bash
scripts/script.sh datatypes
```

IEC 61131-3 data types: BOOL, INT, DINT, REAL, STRING, TIME, arrays, structs.

### `faults`

```bash
scripts/script.sh faults
```

Common PLC fault codes and troubleshooting steps — CPU faults, I/O faults, communication errors.

### `protocols`

```bash
scripts/script.sh protocols
```

Industrial communication protocols — Modbus RTU/TCP, EtherNet/IP, Profinet, DeviceNet, OPC UA.

### `examples`

```bash
scripts/script.sh examples
```

Example programs: motor start/stop, traffic light sequence, tank level control, conveyor interlock.

### `checklist`

```bash
scripts/script.sh checklist
```

Pre-commissioning checklist — wiring, grounding, I/O mapping, safety circuit verification.

### `help`

```bash
scripts/script.sh help
```

### `version`

```bash
scripts/script.sh version
```

## Configuration

| Variable | Description |
|----------|-------------|
| `PLC_DIR` | Data directory (default: ~/.plc/) |

---

*Powered by BytesAgain | bytesagain.com | hello@bytesagain.com*
