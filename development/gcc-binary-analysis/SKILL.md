---
name: gcc-binary-analysis
description: >
  Analyze compiled ELF binaries produced by GCC (S32Compiler 10.2/11.4). Identifies code
  size contributors, section layout, and symbol-level breakdown to diagnose large firmware
  and unexpected binary growth. Use when the user asks "why is my firmware so large",
  "which function takes the most flash", or "why did my binary grow".
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: compiler
  tags: '[gcc, binary, elf, size, analysis, embedded, arm, cortex-m, s32]'
---

# GCC Binary Analysis (Embedded / S32Compiler)

Analyze a compiled ELF binary to determine what contributes to code size, which functions
or libraries dominate, how sections (`.text`, `.data`, `.bss`) are structured, and why the
binary is larger than expected. Targets linked ELFs produced by S32Compiler GCC.

## When to use

Use this skill when:
- User asks "why is my firmware so large?"
- User asks "which function is taking up the most flash?"
- User asks "why did my binary grow after this change?"
- User asks "what got linked in unexpectedly?"
- User asks "why is libc so large in my binary?"

Do **not** use this skill for:
- Comparing optimization levels -> use `gcc-benchmark-optimization`
- Linking behavior and section placement -> use `gcc-linker-explorer`
- Assembly output inspection -> use `gcc-compiler-explorer`

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
This skill uses the standardized `search_actions` + `execute_action` MCP tool surface.

| Action name | Purpose |
|------|------|
| `compiler.list_gcc_tools` | Call first to discover toolchain paths |
| `compiler.gcc_execute` | Run `size`, `nm`, and `objdump` on the ELF |

## Quickstart

### 1. Discover the toolchain

```
Tool:   list_gcc_compiler_tools
Input:  (none)
Output: toolchain_bin_dir, binary prefix
```

### 2. Measure overall binary size

```
Tool:    gcc_execute
Input:   binary="arm-none-eabi-size", args="output.elf"
Output:  .text / .data / .bss sizes in bytes
```

### 3. Rank symbols by size

```
Tool:    gcc_execute
Input:   binary="arm-none-eabi-nm", args="-C --size-sort output.elf"
Output:  symbols sorted by size (largest at bottom)
```

## Configuration

S32Compiler GCC is discovered automatically via `list_gcc_compiler_tools`. No YAML
config is needed. Always analyze the **linked ELF** -- `.o` file sizes are not
representative of real flash usage (dead code is only removed at link time).

## Guardrails

**Scope**
- This skill analyzes existing ELF files. It does not recompile or modify source.
- Only calls `list_gcc_compiler_tools` and `gcc_execute`. No filesystem writes beyond
  the tool's own scratch directory.

**Destructive actions**
- No destructive operations. All analysis is read-only against the provided ELF.

**Refuse-and-escalate**
- If no GCC toolchain is found, stop and tell the user -- do not guess paths.
- If the user provides a `.o` file instead of a linked ELF, warn them that `.o` sizes
  are not representative and ask for the final ELF.
- If the ELF is for other target, explain this skill is ARM-only and stop.

**Resource limits**
- Do not run `objdump -D` on very large ELFs (> 10 MB) without user confirmation.

**Secrets**
- Do not log or expose content from data sections that may contain sensitive material.

## Workflow

### Step 1 -- Discover the toolchain
Call `list_gcc_compiler_tools()` and identify the binary prefix (e.g. `arm-none-eabi-`).

### Step 2 -- Measure overall binary size

```jsonc
{
  "toolchain_bin_dir": "<bin dir>",
  "binary": "arm-none-eabi-size",
  "args": "output.elf"
}
```

Explain sections:

| Section | Contents | Memory cost |
|---------|----------|-------------|
| `.text` | Executable code | Flash |
| `.rodata` | Read-only constants | Flash |
| `.data` | Initialized variables | Flash + RAM |
| `.bss` | Zero-initialized variables | RAM only |

### Step 3 -- Inspect section layout

```jsonc
{
  "binary": "arm-none-eabi-objdump",
  "args": "-h output.elf"
}
```

Look for unexpectedly large sections and constants in `.data` instead of `.rodata`.

### Step 4 -- Rank symbols by size (core step)

```jsonc
{
  "binary": "arm-none-eabi-nm",
  "args": "-C --size-sort output.elf"
}
```

The largest symbols appear at the bottom. Focus on top contributors to `.text` and
unexpected libc symbols (`printf`, `malloc`, `_printf_float`).

### Step 5 -- Trace symbol origins (optional)

```jsonc
{
  "binary": "arm-none-eabi-objdump",
  "args": "-t output.elf"
}
```

Use to trace unexpected symbols back to their source object or library.

### Analysis checklist
- Identify the largest functions and whether they are user code or libc
- Check for `printf` float formatting (`_printf_float` pulls in large float engine)
- Check for missing dead code elimination (no `--gc-sections` at link time)
- Check for constants in `.data` instead of `.rodata` (missing `const` keyword)

## Validation loop

1. `list_gcc_compiler_tools()` returns a non-empty toolchain list.
2. `arm-none-eabi-size output.elf` produces a section size table.
3. `arm-none-eabi-nm -C --size-sort output.elf` produces a ranked symbol list.
4. Each large symbol is explained with a root cause and actionable recommendation.

## Out of scope

- Recompiling or relinking (use `gcc-linker-explorer` for that workflow)
- Comparing optimization levels (use `gcc-benchmark-optimization`)
- LAX, or SPT targets

## See Also

- `gcc-linker-explorer` -- analyze why symbols are included and how to remove them
- `gcc-benchmark-optimization` -- compare size impact of different `-O` levels
- `gcc-compiler-explorer` -- inspect assembly for individual functions
