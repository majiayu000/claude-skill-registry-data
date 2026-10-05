---
name: spt-binary-analysis
description: >
  Analyze SPT3.8 ELF binaries using objdump-spt. Identifies section layout,
  per-function code size contributors, and diagnoses oversized SPT images.
  Use when the user asks "why is my SPT image so large", "which SPT function is
  biggest", or "why did my SPT ELF grow".
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: compiler
  tags: '[spt, spt3.8, objdump-spt, binary, elf, size, analysis, radar, s32r, embedded]'
---

# SPT3.8 Binary Analysis (NXP SPT / Radar Signal Processing Toolbox)

Analyze a SPT3.8 ELF binary to determine what contributes to code size on the SPT
accelerator, which functions dominate the image, and how sections are structured.
Uses `objdump-spt` -- the only binary analysis tool available in the SPT3.8 toolchain.

## When to use

Use this skill when:
- User asks "why is my SPT image so large?"
- User asks "which SPT function is the biggest?"
- User asks "why did my SPT ELF grow after this change?"

Do **not** use this skill for:
- Per-instruction encoding -> use `spt-assembler-explorer`

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
This skill uses the standardized `search_actions` + `execute_action` MCP tool surface.

| Action name | Purpose |
|------|------|
| `compiler.list_spt_tools` | Discover toolchain; call first |
| `compiler.spt_execute` | Run `objdump-spt` |

Note: SPT3.8 does **not** ship `size-spt`, `nm-spt`, or `readelf-spt`.
`objdump-spt` is the only binary inspection tool available.

## Quickstart

### 1. Discover toolchain

```
Tool:   list_spt_compiler_tools  ->  toolchain_bin_dir
```

### 2. Disassemble to enumerate sections and symbols

```
Tool:    spt_execute, binary="objdump-spt", args="-Dr image.elf"
Output:  section headers and per-symbol instruction listings
```

### 3. Rank functions by instruction count

Count instruction lines per labeled symbol block in the disassembly output.
Each SPT instruction is 16 bytes (128 bits); divide byte size by 16 for instruction count.

## Configuration

Key facts:
- Must use `objdump-spt`; stock GNU `objdump` does not decode SPT mnemonics
- No C/C++ compiler; every byte in `.text` came from `.spt` assembly source
- Every SPT instruction is 16 bytes (128 bits)

## Guardrails

**Scope**
- Only calls `list_spt_compiler_tools` and `spt_execute`. No user files modified.

**Destructive actions**
- Read-only analysis of the provided ELF.

**Refuse-and-escalate**
- If no SPT3.8 toolchain found, stop and tell the user.
- Do not use stock GNU `objdump`, `nm`, or `size` on SPT ELFs.
- Do not attempt to call `size-spt`, `nm-spt`, or `readelf-spt` -- they do not exist.

**Resource limits**
- Do not run full disassembly on very large ELFs without user confirmation.

**Secrets**
- Do not expose sensitive content from data sections.

## Workflow

### Step 1 -- Discover toolchain
Call `list_spt_compiler_tools()` and confirm `objdump-spt` is present.

### Step 2 -- Disassemble ELF

```jsonc
{
  "toolchain_bin_dir": "<bin dir>",
  "binary": "objdump-spt",
  "args": "-Dr image.elf"
}
```

Each labeled block in the output (e.g. `<function_name>:`) is one function.
Count instruction lines per block to rank contributors by size.

### Step 3 -- Rank functions by size
Sort labeled blocks descending by instruction count. Focus on:
- Largest user functions and what they do
- Repeated `copy.*` sequences or unrolled FFT stages that could use `loop`
- Large absolute-address symbol chains

### Step 4 -- Inspect section layout (optional)

```jsonc
{
  "binary": "objdump-spt",
  "args": "-h image.elf"
}
```

Check that sections are placed in the expected SPT memories:
- `.text` -> PMEM (program memory)
- `.rodata` -> TRAM (twiddle tables, FIR taps)
- `.data` / `.bss` -> OPRAM (operand buffers)

### Common SPT size patterns

| Symptom | Cause | Fix |
|---------|-------|-----|
| Very large `.text` for small algorithm | Fully unrolled FFT/FIR | Convert to `loop` + indirect variant |
| Repeated `copy.simple` | Per-slice explicit copies | Use one wider `copy.simple` with proper `vec_sz` |
| Constants in `.data` | Missing `.section .rodata` | Move to `.rodata` / TRAM |
| Redundant `set #imm, WR_x` blocks | Per-call context reload | Factor into shared setup label |

## Validation loop

1. `list_spt_compiler_tools()` returns a non-empty toolchain list.
2. `objdump-spt -Dr image.elf` produces a disassembly listing.
3. Each large symbol block is explained with root cause and actionable recommendation.

## Out of scope

- Per-instruction encoding (use `spt-assembler-explorer`)
- Linking / section placement analysis -- SPT3.8 has no linker tool in the MCP toolchain

## See Also

- `spt-assembler-explorer` -- per-instruction encoding and assembly examples
