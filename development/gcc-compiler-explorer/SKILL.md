---
name: gcc-compiler-explorer
description: >
  Interactive compile-and-inspect workflow using local GCC toolchains (S32Compiler GCC
  10.2/11.4). Compiles C/C++ code, produces real assembly, and explains how the compiler
  transforms source into instructions for embedded ARM Cortex-M/R/A targets. Use when the
  user asks "what assembly does GCC generate", "how does -O2 optimize this loop", or wants
  to inspect ARM code generation.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: compiler
  tags: '[compiler, gcc, assembly, disassembly, compiler-explorer, arm, cortex-m, cortex-r, cortex-a, s32, embedded]'
---

# GCC Compiler Explorer (Embedded / S32Compiler)

Compile C/C++ source using a locally installed S32Compiler GCC toolchain (10.2 or 11.4),
inspect the real assembly output, and explain how the compiler transforms source into ARM
instructions -- similar to godbolt.org but for embedded ARM targets.

## When to use

Use this skill when:
- User asks "what assembly does GCC generate for this code?"
- User asks "how does `-O2` optimize this loop?"
- User asks "is this code efficient for Cortex-M7?"
- User wants to compare `-O0` vs `-O2` vs `-Os` assembly output
- User asks "why is this instruction being emitted?"

Do **not** use this skill for:
- Benchmarking multiple optimization levels -> use `gcc-benchmark-optimization`
- LLVM/Clang output -> use `llvm-compiler-explorer`
- Other targets -> S32Compiler GCC is ARM-only; inform the user

## Available Capabilities

This skill uses the standardized `search_actions` + `execute_action` MCP tool surface.

| Action name | Purpose |
|------|------|
| `compiler.list_gcc_tools` | Call first to discover toolchain paths |
| `compiler.gcc_execute` | Compile, disassemble, inspect symbols and size |

Invoke via `execute_action(action_name="compiler.list_gcc_tools")` and
`execute_action(action_name="compiler.gcc_execute", params={...})`.

## Quickstart

### 1. Discover the toolchain

```
execute_action(action_name="compiler.list_gcc_tools")
Output: toolchain_bin_dir, available binaries
```

### 2. Compile source to object file

```
execute_action(action_name="compiler.gcc_execute", params={
  "toolchain_bin_dir": "<bin dir>", "binary": "arm-none-eabi-gcc",
         args="-mcpu=cortex-m7 -mthumb -mfpu=fpv5-d16 -mfloat-abi=hard
               -O2 -ffunction-sections -fdata-sections -ffreestanding
               -nostdlib -fno-builtin -g -c -o output.o",
         input_code="<source>"
Output:  output.o (object file)
```

### 3. Disassemble and inspect

```
execute_action(action_name="compiler.gcc_execute", params={
  "toolchain_bin_dir": "<bin dir>", "binary": "arm-none-eabi-objdump",
  "args": "-d -S -M no-aliases --no-show-raw-insn output.o"})
Output:  interleaved source/assembly listing
```

## Configuration

S32Compiler GCC is discovered automatically via `compiler.list_gcc_tools`. No YAML
config is needed. Key toolchain facts:
- GCC versions: 10.2 and 11.4
- Runtime: newlib / newlib-nano
- `-Oz` is **not supported** in GCC 10/11 (Clang-only flag)

## Guardrails

**Scope**
- This skill only calls `compiler.list_gcc_tools` and `compiler.gcc_execute` via
  `execute_action`. It does not write
  project files, modify the filesystem, or install toolchains.

**Destructive actions**
- Compilation produces temporary object files in an isolated scratch directory managed
  by the tool. No user project files are modified.

**Refuse-and-escalate**
- If no GCC toolchain is found by `compiler.list_gcc_tools`, stop and tell the user --
  do not guess or hard-code paths.
- If the user requests other target, stop and explain that S32Compiler GCC is
  ARM-only; suggest the `llvm-compiler-explorer` skill instead.
- If the target is ambiguous (no `-mcpu` specified), ask the user before compiling.

**Resource limits**
- Warn the user before compiling source files larger than 1000 lines, since output may be long.

**Secrets**
- Redact API keys, passwords, and tokens from any logged output or transcripts.

## Workflow

### Step 1 -- Discover the toolchain
Call `execute_action(action_name="compiler.list_gcc_tools")`. From the output identify:
- `toolchain_bin_dir` for the target architecture
- Compiler binary prefix: `arm-none-eabi-gcc` (Cortex-M/R) or `aarch64-none-elf-gcc` (Cortex-A 64-bit)

If no matching toolchain is found, stop and tell the user.

### Step 2 -- Determine target architecture

| Target | Compiler binary | Flags |
|--------|----------------|-------|
| Cortex-M7 / S32K3 | `arm-none-eabi-gcc` | `-mcpu=cortex-m7 -mthumb -mfpu=fpv5-d16 -mfloat-abi=hard` |
| Cortex-M4 | `arm-none-eabi-gcc` | `-mcpu=cortex-m4 -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=hard` |
| Cortex-M33 | `arm-none-eabi-gcc` | `-mcpu=cortex-m33 -mthumb` |
| Cortex-M0+ | `arm-none-eabi-gcc` | `-mcpu=cortex-m0plus -mthumb` |
| Cortex-R52 | `arm-none-eabi-gcc` | `-mcpu=cortex-r52` |
| Cortex-A53 (GCC 10.2 + 11.4) | `aarch64-none-elf-gcc` | `-mcpu=cortex-a53` |
| Cortex-A78 (GCC 11.4 only) | `aarch64-none-elf-gcc` | `-mcpu=cortex-a78` |

The objdump/size/nm binaries follow the same prefix as the compiler.

### Step 3 -- Compile to object file

```jsonc
{
  "toolchain_bin_dir": "<bin dir>",
  "binary": "arm-none-eabi-gcc",
  "args": "-mcpu=cortex-m7 -mthumb -mfpu=fpv5-d16 -mfloat-abi=hard -O2
           -ffunction-sections -fdata-sections -ffreestanding -nostdlib
           -fno-builtin -g -c -o output.o",
  "input_code": "<user source>"
}
```

Add `-fno-exceptions -fno-rtti` for C++ source. If compilation fails, show the full
`stderr` and do not proceed to disassembly.

### Step 4 -- Disassemble

```jsonc
{
  "toolchain_bin_dir": "<bin dir>",
  "binary": "arm-none-eabi-objdump",
  "args": "-d -S -M no-aliases --no-show-raw-insn output.o"
}
```

### Step 5 -- Inspect symbols and size (optional)

```jsonc
{ "binary": "arm-none-eabi-size",  "args": "output.o" }
{ "binary": "arm-none-eabi-nm",    "args": "-C output.o" }
```

### Step 6 -- Explain the assembly
After disassembly always explain: arithmetic ops (`ADD`, `SUB`, `MUL`), memory accesses
(`LDR`, `STR`), function calls (`BL`, `BLX`), optimizations applied (constant folding,
inlining, dead code elimination), Thumb-2 instruction mix, FPU usage, and overall
efficiency (instruction count, memory accesses, branch patterns).

### Comparing optimization levels
Repeat Steps 3-4 for each level (`-O0`, `-O2`, `-Os`) and present side by side:

| Level | Typical behavior |
|-------|-----------------|
| `-O0` | Heavy stack usage, many loads/stores |
| `-O2` | Registers optimized, inlining applied |
| `-Os` | Fewer instructions, aggressive value reuse |

## Validation loop

1. `execute_action(action_name="compiler.list_gcc_tools")` returns a non-empty toolchain list -- if empty, stop.
2. Compile exits 0 and `stderr` is empty or only contains expected warnings.
3. Disassembly output is non-empty and contains the expected function labels.
4. Assembly explanation is provided in plain language alongside the output.

## Out of scope

- Linking to a final ELF (use `gcc-benchmark-optimization` or `gcc-linker-explorer`)
- Binary size analysis of linked firmware (use `gcc-binary-analysis`)
- LAX targets
- Running / simulating the compiled code

## See Also

- `gcc-benchmark-optimization` -- compare all optimization levels with size measurements
- `gcc-binary-analysis` -- analyze section and symbol size in a linked ELF
- `gcc-linker-explorer` -- analyze linking behavior and dead code elimination
- `llvm-compiler-explorer` -- same workflow for Clang
