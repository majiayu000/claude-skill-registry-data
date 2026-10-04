---
name: reverse-engineering-arm-binaries
description: 'Reverse engineers ARM/AArch64 malware by identifying the architecture and instruction
  set state (ARM/Thumb), parsing ELF/Mach-O ARM headers, and orienting analysis around the ARM
  calling convention. Activates for requests to reverse ARM binaries, analyze AArch64 malware, or
  handle ARM/Thumb instruction-set decoding.'
domain: cybersecurity
subdomain: reverse-engineering
tags:
  - reverse-engineering
  - arm
  - aarch64
  - thumb
  - disassembly
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1027
  - T1059
  - T1587.001
d3fend:
  - D3-DA
  - D3-SDA
references:
  - 'Arm Architecture Reference Manual — https://developer.arm.com/documentation/'
  - 'ELF for the Arm Architecture (AAELF) — https://github.com/ARM-software/abi-aa'
---

# Reverse Engineering ARM Binaries

## When to Use

- You have an ARM (32-bit) or AArch64 (64-bit) binary — IoT/mobile/Linux malware — and need to
  identify the architecture, instruction-set state, and entry point before disassembly.
- You need to handle ARM/Thumb interworking correctly.

**Do not use** an x86 mindset for calling conventions/registers — ARM differs. This skill reads the
binary statically and executes nothing.

## Prerequisites

- The ARM binary (ELF or Mach-O), read inertly. Capstone optional for instruction decoding.

## Safety & Handling

- Read bytes statically; analyze on an isolated host (and emulate via QEMU separately if needed).

## Workflow

### Step 1: Identify architecture and format

```bash
python scripts/analyst.py identify sample.bin
```

Parses ELF/Mach-O headers to report ARM vs AArch64, endianness, entry point, and (for ELF) whether
the entry is Thumb (low bit set in `e_entry` or `$t` mapping symbols).

### Step 2: Set the correct disassembly mode

Disassemble AArch64 as A64; for 32-bit ARM, switch between ARM and Thumb per the entry/mapping
symbols.

### Step 3: Orient around the calling convention

Track arguments in `r0-r3`/`x0-x7`, return in `r0`/`x0`, and syscalls via `svc` with the syscall
number in `r7`/`x8`.

### Step 4: Proceed with analysis

Identify functions, strings, and syscalls; pair with emulation if dynamic insight is needed.

## Validation

- Architecture (ARM/AArch64) and endianness are read from the header.
- The entry point and ARM/Thumb state are reported.
- Disassembly mode matches the detected state.

## Pitfalls

- Missing Thumb state and decoding Thumb as ARM (garbage output).
- Big-endian ARM (rare but real) mis-parsed as little-endian.
- Statically linked musl/uClibc inflating the function set on IoT samples.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the identifier.
- Arm ARM and AAELF references (linked in frontmatter).
