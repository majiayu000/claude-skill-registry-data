---
name: "rfid"
version: "1.0.0"
description: "RFID technology reference — tag types, frequency bands, read ranges, EPC standards, inventory tracking. Use when designing RFID systems, selecting tags/readers, or implementing warehouse tracking solutions."
author: "BytesAgain"
homepage: "https://bytesagain.com"
source: "https://github.com/bytesagain/ai-skills"
tags: [rfid, nfc, epc, tag, reader, inventory, tracking, logistics]
category: "logistics"
---

# RFID — Radio-Frequency Identification Reference

Quick-reference skill for RFID technology, standards, and implementation.

## When to Use

- Selecting RFID tags and readers for warehouse or retail
- Understanding frequency bands and read range trade-offs
- Implementing EPC/SGTIN encoding for supply chain
- Designing RFID read zones and antenna placement
- Comparing RFID vs barcode for inventory management

## Commands

### `intro`

```bash
scripts/script.sh intro
```

Overview of RFID — how it works, components, active vs passive.

### `frequencies`

```bash
scripts/script.sh frequencies
```

Frequency bands — LF, HF, UHF, microwave, read range, use cases.

### `tags`

```bash
scripts/script.sh tags
```

Tag types — passive, semi-passive, active, inlays, hard tags, form factors.

### `standards`

```bash
scripts/script.sh standards
```

Standards — EPC Gen2, ISO 18000, NFC (ISO 14443/15693), GS1 encoding.

### `readers`

```bash
scripts/script.sh readers
```

Readers and antennas — fixed, handheld, portal, sensitivity, protocols.

### `applications`

```bash
scripts/script.sh applications
```

Applications — retail, warehouse, asset tracking, access control, healthcare.

### `challenges`

```bash
scripts/script.sh challenges
```

Challenges — metal/liquid interference, collision, privacy, cost analysis.

### `checklist`

```bash
scripts/script.sh checklist
```

RFID implementation planning checklist.

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
| `RFID_DIR` | Data directory (default: ~/.rfid/) |

---

*Powered by BytesAgain | bytesagain.com | hello@bytesagain.com*
