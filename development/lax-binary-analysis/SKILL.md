---
name: lax-binary-analysis
description: >
  Analyze linked LAX .eld binaries produced by the laxcc toolchain. Identifies per-function
  code size contributors, section layout, and hardware-loop / vectorization patterns to
  diagnose oversized LAX images. Use when the user asks "why is my LAX .eld so large",
  "which LAX function is the largest", or "why did my LAX binary grow".
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: compiler
  tags: '[lax, laxcc, it3a-ds, binary, eld, size, analysis, vector, vspa, dsp, s32, embedded]'
---

# LAX Binary Analysis (Embedded / LAX VSP)

Analyze a linked LAX `.eld` binary to determine what contributes to code size on the LAX
VSP, which functions dominate the image, and how sections are structured.

## When to use

Use this skill when:
- User asks "why is my LAX `.eld` so large?"
- User asks "which LAX function is the largest?"
- User asks "why did my LAX binary grow after this change?"

Do **not** use this skill for:
- Comparing optimization levels -> use `lax-benchmark-optimization`
- Linking behavior and section placement -> use `lax-linker-explorer`
- Assembly output only -> use `lax-compiler-explorer`

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| MCP tool | `list_lax_compiler_tools` | Discover toolchain; call first |
| MCP tool | `lax_execute` | Run `laxcc` and `it3a-ds` |

## Quickstart

### 1. Discover toolchain

```
Tool:   list_lax_compiler_tools  ->  toolchain_bin_dir
```

### 2. Disassemble .eld to enumerate sections

```
Tool:    lax_execute, binary="it3a-ds", args="output.eld"
Output:  per-function .text$<sym> sections with instruction listings
```

### 3. Rank functions by instruction count and explain findings

## Configuration

LAX has no `nm`/`size`/`objdump` -- use `it3a-ds` for all analysis. Always analyze the
linked `.eld`, not raw `.eln` files. Build with `--keep` to produce `.sl` files for
cross-reference.

## Guardrails

**Scope**
- Only calls `list_lax_compiler_tools` and `lax_execute`. No user files modified.

**Destructive actions**
- Read-only analysis of the provided `.eld` file.

**Refuse-and-escalate**
- If no LAX toolchain found, stop and tell the user.
- If the user provides a `.eln` instead of `.eld`, warn that sizes are not representative.
- Do not use ARM tools on LAX binaries.

**Resource limits**
- Do not disassemble very large `.eld` files without user confirmation.

**Secrets**
- Do not expose sensitive content from data sections.

## Workflow

### Step 1 -- Discover toolchain
Call `list_lax_compiler_tools()` and confirm `laxcc` and `it3a-ds` are present.

### Step 2 -- Disassemble .eld

```jsonc
{
  "toolchain_bin_dir": "<bin dir>",
  "binary": "it3a-ds",
  "args": "output.eld"
}
```

Each function appears as `.section .text$<symbol>, "ae", @progbits`. Count
instruction/data lines per section to rank contributors by size.

### Step 3 -- Rank functions by size
Sort `.text$<sym>` sections descending by instruction count. Focus on:
- Largest user functions and what they do
- Runtime/library helpers (`_fadd_soft` = double-precision math -- prefer `float`)
- Duplicated code that could be consolidated

### Step 4 -- Cross-reference with .sl files (optional)
If the `.eld` was built with `--keep`, open the `.sl` of the largest functions to
understand why they are large: unrolled loops, inlined callees, many `nopS`/`fnop` fills.

### Step 5 -- Identify data-side growth
For `.data`, `.rodata`, `.bss` sections:
- Large `.data` -> missing `const` on lookup tables (wastes DMEM and copy-down cost)
- Over-aligned buffers (`__attribute__((aligned(...)))`) adding padding

### Common size patterns

| Symptom | Cause | Fix |
|---------|-------|-----|
| Large `_fadd_soft` / `_fmul` | Software double-precision | Convert to `float` |
| Many `nopS`/`fnop` fills | Data dependencies | Add `__restrict`, `#pragma loop_count` |
| No hardware loop | Function call inside loop | Simplify / inline helper |
| Constants in `.data` | Missing `const` | Add `const` |

## Validation loop

1. `list_lax_compiler_tools()` returns a non-empty toolchain list.
2. `it3a-ds output.eld` produces section listings.
3. Each large symbol is explained with root cause and actionable recommendation.

## Out of scope

- ARM analysis
- Recompiling / relinking (use `lax-linker-explorer`)

## See Also

- `lax-benchmark-optimization` -- compare optimization levels
- `lax-linker-explorer` -- linking behavior and `.lcf` analysis
- `lax-compiler-explorer` -- per-function assembly inspection
