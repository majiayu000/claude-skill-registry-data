---
name: gcc-benchmark-optimization
description: >
  Compare assembly output and final binary size across GCC optimization levels (-O0, -O1,
  -O2, -O3, -Os) for embedded ARM targets using S32Compiler GCC (10.2/11.4). Produces
  realistic size measurements using linked ELF binaries and explains performance vs size
  trade-offs. Use when the user asks "which optimization level should I use", "compare -O2
  vs -Os", or "why is my binary too large".
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: compiler
  tags: '[compiler, gcc, optimization, assembly, size, benchmark, arm, cortex-m, s32, embedded]'
---

# GCC Benchmark Optimization Levels (Embedded / S32Compiler)

Compile the same C/C++ source at multiple GCC optimization levels, link the final ELF,
measure real code size, disassemble each output, and explain trade-offs -- so the user can
pick the best optimization level for their embedded target.

## When to use

Use this skill when:
- User asks "which optimization level should I use for embedded?"
- User asks "why is my binary too large?"
- User wants to compare `-O2` vs `-Os`
- User wants size/performance trade-off analysis for ARM Cortex-M code

Do **not** use this skill for:
- LLVM/Clang benchmarking -> use `llvm-benchmark-optimization`
- Single optimization level inspection -> use `gcc-compiler-explorer`
- Symbol-level size analysis of an existing ELF -> use `gcc-binary-analysis`

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
This skill uses the standardized `search_actions` + `execute_action` MCP tool surface.

| Action name | Purpose |
|------|------|
| `compiler.list_gcc_tools` | Discover toolchain; call first |
| `compiler.gcc_execute` | Compile, link, disassemble, and measure size |

## Quickstart

### 1. Discover toolchain and detect GCC version

```
Tool:   list_gcc_compiler_tools  ->  get toolchain_bin_dir
Tool:   gcc_execute, binary="arm-none-eabi-gcc", args="--version"
```

### 2. Compile and link at each level (default: -O0, -O2, -Os)

```
Tool:    gcc_execute, binary="arm-none-eabi-gcc"
Input:   "<target flags> -<level> -ffunction-sections -fdata-sections
          -ffreestanding -nostdlib -c -o output_<level>.o"
Then:    gcc_execute to link:
         "<target flags> -Wl,--gc-sections --specs=nosys.specs
          -o output_<level>.elf output_<level>.o"
```

### 3. Measure and compare

```
Tool:    gcc_execute, binary="arm-none-eabi-size", args="output_<level>.elf"
Output:  .text / .data / .bss for each level
```

## Configuration

Key facts:
- `-Oz` is **not supported** in GCC 10/11 -- never use it
- Always link before measuring size; `.o` sizes are not representative
- Always use `-ffunction-sections -fdata-sections -Wl,--gc-sections`
- `--specs=nano.specs` reduces libc footprint significantly for size-critical targets

## Guardrails

**Scope**
- Only calls `list_gcc_compiler_tools` and `gcc_execute`. No project files modified.

**Destructive actions**
- Produces temporary files in the tool's scratch directory only.

**Refuse-and-escalate**
- If no GCC toolchain found, stop and tell the user.
- If target is ambiguous, ask before compiling.
- Never use `-Oz` for GCC 10/11 -- explain it is a Clang-only flag.

**Resource limits**
- Default sweep is `-O0`, `-O2`, `-Os` (3 compile+link cycles). Add `-O3` only when
  the user explicitly asks about performance vs size.

**Secrets**
- Do not log source content that may contain sensitive material.

## Workflow

### Step 1 -- Discover toolchain and detect version
Call `list_gcc_compiler_tools()`, then run `arm-none-eabi-gcc --version` to confirm the
GCC version. GCC <= 11: `-Oz` is not supported.

### Step 2 -- Map target to compiler flags (same table as gcc-compiler-explorer)

| Target | Binary | Flags |
|--------|--------|-------|
| Cortex-M7 / S32K3 | `arm-none-eabi-gcc` | `-mcpu=cortex-m7 -mthumb -mfpu=fpv5-d16 -mfloat-abi=hard` |
| Cortex-M4 | `arm-none-eabi-gcc` | `-mcpu=cortex-m4 -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=hard` |
| Cortex-M33 | `arm-none-eabi-gcc` | `-mcpu=cortex-m33 -mthumb` |
| Cortex-M0+ | `arm-none-eabi-gcc` | `-mcpu=cortex-m0plus -mthumb` |
| Cortex-R52 | `arm-none-eabi-gcc` | `-mcpu=cortex-r52` |
| Cortex-A53/A78 | `aarch64-none-elf-gcc` | `-mcpu=cortex-a53` |

### Step 3 -- Compile to object file at each level

```jsonc
{
  "binary": "arm-none-eabi-gcc",
  "args": "-mcpu=cortex-m7 -mthumb -mfpu=fpv5-d16 -mfloat-abi=hard -O2
           -ffunction-sections -fdata-sections -ffreestanding -nostdlib
           -c -o output_O2.o",
  "input_code": "<user source>"
}
```

Repeat for each level; output names: `output_O0.o`, `output_O2.o`, `output_Os.o`.

### Step 4 -- Link to ELF (critical -- always link before measuring)

```jsonc
{
  "binary": "arm-none-eabi-gcc",
  "args": "-mcpu=cortex-m7 -mthumb -mfpu=fpv5-d16 -mfloat-abi=hard
           -Wl,--gc-sections --specs=nosys.specs -o output_O2.elf output_O2.o"
}
```

Optionally also test with `--specs=nano.specs` for size-critical targets. Add
`-u _printf_float` if the code uses `printf` with `%f` and `nano.specs` is enabled.

### Step 5 -- Measure size, disassemble, and present comparison

```
Level   .text (bytes)   Instructions   Notes
------  -------------   ------------   -----
-O0     128             42             No optimization
-O2     48              16             Balanced -- inlining and constant folding
-Os     40              14             Smallest code
```

Explain differences: what optimizations were applied, why instruction count changed,
ARM-specific observations (Thumb-2 mix, FPU usage), and trade-offs.

### Step 6 -- Give a recommendation

| Goal | Recommendation |
|------|---------------|
| Debugging | `-O0` |
| Production firmware | `-O2` |
| Tight flash budget | `-Os` + `--specs=nano.specs` |
| Compute-heavy inner loop | `-O2` or `-O3` |

## Validation loop

1. `list_gcc_compiler_tools()` returns a non-empty toolchain list.
2. Each compile+link cycle exits 0.
3. `arm-none-eabi-size` produces a section size table for each linked ELF.
4. Summary comparison table is presented before detailed disassembly.
5. A concrete recommendation is given at the end.

## Out of scope

- Detailed symbol-level analysis of an existing ELF (use `gcc-binary-analysis`)
- LAX, or SPT targets
- Running / simulating the compiled code

## See Also

- `gcc-binary-analysis` -- deep symbol-level analysis of a linked ELF
- `gcc-linker-explorer` -- diagnose why specific symbols were linked
- `gcc-compiler-explorer` -- inspect assembly at a single optimization level
- `llvm-benchmark-optimization` -- same workflow for Clang
