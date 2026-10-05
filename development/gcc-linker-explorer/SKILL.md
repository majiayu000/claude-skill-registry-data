---
name: gcc-linker-explorer
description: >
  Analyze linking behavior for embedded GCC (S32Compiler 10.2/11.4). Explains how object
  files, libraries, and linker options produce the final ELF. Use when the user asks "why
  is this function still being linked", "why isn't dead code being removed", "why does
  printf pull in so much code", or "how are my sections laid out".
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: compiler
  tags: '[gcc, linker, embedded, elf, size, sections, arm, cortex-m, s32]'
---

# GCC Linker Explorer (Embedded / S32Compiler)

Analyze how GCC links object files into a final ELF binary and explain why certain code
or data is included, how sections are organized, and how linker options affect the result.
Targets S32Compiler GCC 10.2/11.4 for ARM Cortex-M/R/A.

## When to use

Use this skill when:
- User asks "why is this function still being linked?"
- User asks "why isn't dead code being removed?"
- User asks "why does printf pull in so much code?"
- User asks "where did this symbol come from?"
- User asks "how are my sections laid out?"

Do **not** use this skill for:
- Comparing optimization levels -> use `gcc-benchmark-optimization`
- Assembly output inspection -> use `gcc-compiler-explorer`
- Symbol-level size ranking of an existing ELF -> use `gcc-binary-analysis`

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
This skill uses the standardized `search_actions` + `execute_action` MCP tool surface.

| Action name | Purpose |
|------|------|
| `compiler.list_gcc_tools` | Discover toolchain; call first |
| `compiler.gcc_execute` | Run GCC, objdump, nm, and size |

## Quickstart

### 1. Compile with section flags (required for dead code elimination)

```
Tool:    gcc_execute, binary="arm-none-eabi-gcc"
Input:   "<target flags> -O2 -ffunction-sections -fdata-sections
          -ffreestanding -nostdlib -c -o main.o"
```

### 2. Link with gc-sections

```
Tool:    gcc_execute, binary="arm-none-eabi-gcc"
Input:   "<target flags> -Wl,--gc-sections --specs=nosys.specs -o output.elf main.o"
```

### 3. Inspect sections and rank symbols

```
Tool:    gcc_execute, binary="arm-none-eabi-objdump", args="-h output.elf"
Tool:    gcc_execute, binary="arm-none-eabi-nm",      args="-C --size-sort output.elf"
```

## Configuration

Dead code elimination requires **both** compiler and linker steps:
- Compile: `-ffunction-sections -fdata-sections`
- Link: `-Wl,--gc-sections`

Without both, dead code survives. `--specs=nano.specs` reduces libc footprint;
add `-u _printf_float` if float formatting is needed with nano.specs.

## Guardrails

**Scope**
- Only calls `list_gcc_compiler_tools` and `gcc_execute`. No user project files modified.

**Destructive actions**
- All output goes to the tool's isolated scratch directory.

**Refuse-and-escalate**
- If no GCC toolchain found, stop and tell the user.
- If target is ambiguous, ask before compiling.
- Never use `-Oz` for GCC 10/11.

**Resource limits**
- Do not run full `-D` disassembly on large ELFs without user confirmation.

**Secrets**
- Do not log source content that may contain sensitive material.

## Workflow

### Step 1 -- Discover toolchain
Call `list_gcc_compiler_tools()` and identify the binary prefix.

### Step 2 -- Compile with section flags
Always use `-ffunction-sections -fdata-sections` -- without these, the linker cannot
remove unused functions even with `--gc-sections`.

### Step 3 -- Link with multiple variants

| Mode | Args | Purpose |
|------|------|---------|
| Bare-metal | `--specs=nosys.specs` | Minimal runtime |
| Size-optimized | `--specs=nosys.specs --specs=nano.specs` | Reduced libc |
| Semihosting | `--specs=rdimon.specs` | Debug via host I/O |

When diagnosing size, test with and without `--specs=nano.specs` to show libc impact.

### Step 4 -- Inspect sections and measure size

```jsonc
{ "binary": "arm-none-eabi-objdump", "args": "-h output.elf" }
{ "binary": "arm-none-eabi-size",    "args": "output.elf"    }
```

### Step 5 -- Rank symbols and trace origins

```jsonc
{ "binary": "arm-none-eabi-nm",      "args": "-C --size-sort output.elf" }
{ "binary": "arm-none-eabi-objdump", "args": "-t output.elf"             }
```

### Inclusion cause analysis

| Cause | Signal |
|-------|--------|
| Direct reference | Symbol called directly by user code |
| Indirect reference | Pulled in through a call chain |
| libc pull | `printf` drags in formatting engine |
| Missing section flags | All functions share one `.text` block |
| Missing `--gc-sections` | Linker keeps all sections |

### Why dead code survives

| Cause | Fix |
|-------|-----|
| Missing `--gc-sections` | Add `-Wl,--gc-sections` |
| Missing `-ffunction-sections` | Recompile with both section flags |
| `__attribute__((used))` | Intentional -- explain to user |
| Function pointer reference | Linker cannot prove unused |

## Validation loop

1. `list_gcc_compiler_tools()` returns a non-empty toolchain list.
2. Compile and link both exit 0.
3. `arm-none-eabi-size` shows reduced `.text` when `--specs=nano.specs` is tested.
4. Each unexpected symbol is explained with a root cause and fix.

## Out of scope

- Optimization level comparison (use `gcc-benchmark-optimization`)
- LAX, or SPT targets

## See Also

- `gcc-binary-analysis` -- symbol-level size ranking of an existing ELF
- `gcc-benchmark-optimization` -- optimization level comparison with size measurements
- `gcc-compiler-explorer` -- assembly inspection at a single optimization level
