---
name: "bms"
version: "1.0.0"
description: "Battery Management System reference — cell balancing, SOC estimation, thermal management, and protection circuits. Use when designing BMS for lithium-ion packs, evaluating battery safety, or understanding cell monitoring."
author: "BytesAgain"
homepage: "https://bytesagain.com"
source: "https://github.com/bytesagain/ai-skills"
tags: [bms, battery, lithium-ion, cell-balancing, soc, thermal, energy-storage]
category: "energy"
---

# BMS — Battery Management System Reference

Quick-reference skill for battery management systems, cell monitoring, and pack safety.

## When to Use

- Designing a BMS for lithium-ion battery packs
- Understanding cell balancing (passive vs active)
- Implementing SOC/SOH estimation algorithms
- Setting up thermal management and protection thresholds
- Evaluating BMS ICs and architectures

## Commands

### `intro`

```bash
scripts/script.sh intro
```

Overview of BMS — functions, architecture, and why every Li-ion pack needs one.

### `cellbalance`

```bash
scripts/script.sh cellbalance
```

Cell balancing methods: passive (dissipative) vs active (redistributive).

### `soc`

```bash
scripts/script.sh soc
```

State of Charge estimation: coulomb counting, OCV lookup, Kalman filter, impedance.

### `protection`

```bash
scripts/script.sh protection
```

Protection circuits: overvoltage, undervoltage, overcurrent, short circuit, temperature.

### `thermal`

```bash
scripts/script.sh thermal
```

Thermal management — air cooling, liquid cooling, phase change, heating in cold.

### `communication`

```bash
scripts/script.sh communication
```

BMS communication protocols: CAN bus, SMBus, I²C, UART, and data frames.

### `topologies`

```bash
scripts/script.sh topologies
```

BMS architectures: centralized, distributed, modular — and IC selection.

### `safety`

```bash
scripts/script.sh safety
```

Safety standards, failure modes, and functional safety (ISO 26262, IEC 62619).

### `help`

```bash
scripts/script.sh help
```

### `version`

```bash
scripts/script.sh version
```

---

*Powered by BytesAgain | bytesagain.com | hello@bytesagain.com*
