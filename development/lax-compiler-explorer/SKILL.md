---
name: lax-compiler-explorer
description: >
  Interactive compile-and-inspect workflow using the local LAX C/C++ toolchain (laxcc,
  it3a-ds). Compiles C/C++ code for the NXP LAX vector signal processor, produces real
  assembly (.sl) or disassembly of the linked .eld, and explains VLIW/vector instructions.
  Use when the user asks "what assembly does LAX generate", "how does -O3 optimize this
  loop on LAX", or "is this code vectorized on LAX".
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: compiler
  tags: '[compiler, lax, laxcc, assembly, disassembly, compiler-explorer, vector, vspa, dsp, s32, embedded]'
---

# LAX Compiler Explorer (Embedded / S32 LAX VSP)

Compile C/C++ source using a locally installed LAX toolchain, inspect the real generated
assembly (`.sl`), and explain how the LAX compiler transforms source into VLIW/vector
instructions for the NXP LAX vector signal processor.

> LAX is a vector signal processor (DSP), not ARM or other target. The toolchain uses its own
> front-end (`laxcc`) and disassembler (`it3a-ds`). Do not use `-mcpu=`, `objdump`, or `nm`.

## When to use

Use this skill when:
- User asks "what assembly does LAX generate for this code?"
- User asks "how does `-O3` optimize this loop on LAX?"
- User asks "is this code vectorized on LAX?"
- User wants to compare `-O0` vs `-O3` vs `-Os` LAX output
- User wants to inspect how `#pragma loop_count` or `__restrict` changes codegen

Do **not** use this skill for:
- ARM output -> use `gcc-compiler-explorer` or `llvm-compiler-explorer`
- Benchmarking multiple `-O` levels -> use `lax-benchmark-optimization`
- Symbol-level size analysis of the linked `.eld` -> use `lax-binary-analysis`

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| MCP tool | `list_lax_compiler_tools` | Discover toolchain; call first |
| MCP tool | `lax_execute` | Run `laxcc` and `it3a-ds` |

## Quickstart

### 1. Discover the toolchain

```
Tool:   list_lax_compiler_tools
Input:  (none)
Output: toolchain_bin_dir containing laxcc and it3a-ds
```

### 2. Compile with --keep to produce the .sl assembly

If the source needs any LAX system header, add exactly **one** `-isystem`
pointing at `<LAX>/include` and spell the include with the `lax/` prefix
(see "System headers and include paths" below):

```
Tool:    lax_execute
Input:   binary="laxcc",
         args="-arch lax -au_count 16 -O3 -c --keep
               -isystem <LAX>/include
               -o main.eln",
         input_code="<source with #include <lax/intrinsics.h>>",
         input_language="c"
Output:  main.eln + main.sl in saved_to directory
```

For a pure-C snippet with no LAX headers, drop the `-isystem` argument.

### 3. Read and explain the .sl file

The `.sl` file in `saved_to` contains compiler-annotated assembly with source-line
back-references. Read it and explain VLIW bundles, hardware loops, and vector register
usage.

## Configuration

Key toolchain facts:
- Front-end: `laxcc` (compiles, assembles, and links)
- Disassembler: `it3a-ds` (for linked `.eld` only; no `objdump`/`nm`)
- Object extension: `.eln`, executable extension: `.eld`
- Assembly output: `.sl` (kept with `--keep`)
- AU variants: 16AU (`-au_count 16`) and 64AU (`-au_count 64`) -- always confirm
- Optimization levels: `-O0` to `-O4` and `-Os`; `-Oz` is **not supported**

### System headers and include paths

When compiling a source snippet with `lax_execute`, no include paths are on by
default -- if the source `#include`s any LAX system header (`intrinsics.h`,
`intrinsic_lax.h`, `math_vspa.h`, ...), you MUST add the LAX include directory
to the command line, otherwise `laxcc` fails with
`the file 'intrinsics.h' cannot be opened`.

**Rules:**

1. **Add exactly ONE include path**, pointing at `<LAX>/include`.
   Use `-isystem` (preferred; matches system-header semantics) or `-I`:
   ```
   -isystem C:/NXP/S32DS.<v>/S32DS/build_tools/LAX/include
   ```
   Pass the path as a separate token after `-isystem` / `-I`
   (no `-I=<path>` and no embedded `=`).

2. **In the source, spell LAX headers with the `lax/` prefix**, e.g.:
   ```c
   #include <lax/intrinsics.h>          /* correct - one -isystem is enough */
   ```
   Do NOT use the bare form:
   ```c
   #include <intrinsics.h>              /* wrong - forces a second -isystem */
   ```
   Rationale: `intrinsics.h` internally does `#include <lax/intrinsic_lax.h>`.
   If you added `-isystem <LAX>/include/lax`, the top-level header resolves but
   the nested `lax/intrinsic_lax.h` does not. Adding `-isystem <LAX>/include`
   AND spelling the top-level include as `<lax/intrinsics.h>` makes both the
   top-level and the nested header resolve with a single include path.

3. **For a pure-C snippet with no LAX headers** (e.g. a scalar arithmetic test),
   omit the include path entirely -- adding it is harmless but unnecessary.

The LAX include root is directly derivable from `toolchain_bin_dir` (returned
by `list_lax_compiler_tools`): drop the trailing `bin` component and append
`include`, e.g. `<...>/LAX/bin` -> `<...>/LAX/include`.

## Guardrails

**Scope**
- Only calls `list_lax_compiler_tools` and `lax_execute`. No user files modified.

**Destructive actions**
- All output goes to the tool's isolated scratch directory.

**Refuse-and-escalate**
- If no LAX toolchain found, stop and tell the user.
- If the AU count (16 or 64) is not specified, ask before compiling -- it changes
  vectorization behavior.
- Never use ARM flags (`-mcpu=`, `-mthumb`, `-mfpu=`, `-march=`).
- Do not run `objdump` or `nm` on `.eln`/`.eld` files -- use `it3a-ds` instead.
- If the source `#include`s a LAX system header, add `-isystem <LAX>/include`
  AND ensure the include is spelled `<lax/HEADER.h>`. Do not pass two separate
  `-isystem` paths and do not use the bare `<HEADER.h>` form.

**Resource limits**
- Do not disassemble very large `.eld` files without user confirmation.

**Secrets**
- Do not log source content that may contain sensitive material.

## Workflow

### Step 1 -- Discover toolchain
Call `list_lax_compiler_tools()` and identify `laxcc` and `it3a-ds`. Derive the
LAX include root by replacing the trailing `bin` in `toolchain_bin_dir` with
`include` (needed for Step 3 if the source uses LAX headers).

### Step 2 -- Confirm AU count
Ask the user if not specified. 16AU and 64AU produce different code, different DMEM
alignment expectations, and different vector widths.

| Target hint | Flags |
|-------------|-------|
| S32R45 LAX / 16AU | `-arch lax -au_count 16` |
| Full-width / 64AU | `-arch lax -au_count 64` |

### Step 3 -- Compile to .eln with --keep

Base invocation (no LAX headers needed):

```jsonc
{
  "toolchain_bin_dir": "<bin dir>",
  "binary": "laxcc",
  "args": "-arch lax -au_count 16 -O3 -c --keep -o main.eln",
  "input_code": "<user source>",
  "input_language": "c"
}
```

If the source uses any LAX system header (`intrinsics.h`, `intrinsic_lax.h`, etc.),
rewrite every affected `#include` to the `lax/`-prefixed form and add one
`-isystem` pointing at `<LAX>/include`:

```jsonc
{
  "toolchain_bin_dir": "<bin dir>",
  "binary": "laxcc",
  "args": "-arch lax -au_count 16 -O3 -c --keep -isystem <LAX>/include -o main.eln",
  "input_code": "#include <lax/intrinsics.h>\n<user source>",
  "input_language": "c"
}
```

For C++, use `input_language: "c++"`. LAX C++ does not support RTTI, exceptions, or
most STL headers.

### Step 4 -- Read .sl assembly (preferred fast path)
The `.sl` file lives in the `saved_to` directory from the `LaxResult`. It contains
compiler-annotated assembly with `#[line,col]` source back-references.

### Step 5 (alternative) -- Link and disassemble .eld
If the user wants a full linked view, link the `.eln` first, then run `it3a-ds`:

```jsonc
{ "binary": "laxcc",    "args": "-arch lax -au_count 16 -o main.eld main.eln" }
{ "binary": "it3a-ds",  "args": "main.eld" }
```

### Step 6 -- Explain the assembly
Explain: scalar ops (`add`, `sub`, `mpy`), memory ops (`ld`, `st`), VLIW bundles
(multiple ops joined with `;`), hardware loops, vector register usage (`v0..vN`),
`nopS`/`fnop` slot fills (VLIW scheduling gaps), and key optimizations applied.

Helpful LAX annotations to suggest:
- `__restrict` on pointer arguments to enable parallel memory scheduling
- `#pragma loop_count (min, max, mod, rem)` for loop unrolling
- `__attribute__((aligned(2 * _AU_COUNT)))` for wide vector loads/stores

## Validation loop

1. `list_lax_compiler_tools()` returns a non-empty toolchain list.
2. If the source `#include`s a LAX header, verify it uses the `<lax/...>` prefix
   AND that the compile command contains exactly one `-isystem <LAX>/include`.
3. Compile exits 0 and the `.sl` file is present in `saved_to`.
4. `.sl` content is read and explained in plain language.
5. AU count was confirmed before compilation.

## Out of scope

- ARM targets
- Binary size analysis (use `lax-binary-analysis`)
- Linking behavior analysis (use `lax-linker-explorer`)

## See Also

- `lax-benchmark-optimization` -- compare all optimization levels
- `lax-binary-analysis` -- analyze symbol/section size in a linked `.eld`
- `lax-linker-explorer` -- analyze `.lcf` linking behavior
- `gcc-compiler-explorer` -- same workflow for ARM GCC
