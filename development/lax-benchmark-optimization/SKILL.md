---
name: lax-benchmark-optimization
description: >
  Compare assembly output and linked .eld size across LAX optimization levels (-O0 to -O4,
  -Os) for the NXP LAX vector signal processor using laxcc. Use when the user asks "which
  optimization level should I use for LAX", "why is my LAX binary too large", or wants to
  see how vectorization and hardware-loop generation change with -O level.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: compiler
  tags: '[compiler, lax, laxcc, optimization, assembly, size, benchmark, vector, vspa, dsp, s32, embedded]'
---

# LAX Benchmark Optimization Levels (Embedded / LAX VSP)

Compile the same C/C++ source at multiple LAX optimization levels, produce the `.sl`
assembly for each, link the final `.eld`, and explain trade-offs for the LAX VSP.

## When to use

Use this skill when:
- User asks "which optimization level should I use for LAX?"
- User asks "why is my LAX binary too large?"
- User wants to compare `-O3` vs `-Os` on LAX
- User wants to see how vectorization / hw-loops change with `-O` level

Do **not** use this skill for:
- ARM benchmarking -> use `gcc-benchmark-optimization` or `llvm-benchmark-optimization`
- Single optimization level view -> use `lax-compiler-explorer`
- Symbol-level size analysis -> use `lax-binary-analysis`

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| MCP tool | `list_lax_compiler_tools` | Discover toolchain; call first |
| MCP tool | `lax_execute` | Run `laxcc` and `it3a-ds` |

## Quickstart

### 1. Discover toolchain and confirm AU count

```
Tool:   list_lax_compiler_tools  ->  toolchain_bin_dir
Ask:    user for AU count (16 or 64) if not specified
Derive: LAX include root = <toolchain_bin_dir with trailing 'bin' replaced by 'include'>
        (only needed if the source uses LAX system headers)
```

### 2. Compile at each level with --keep

If the source needs any LAX system header, add exactly **one** `-isystem`
pointing at `<LAX>/include` and spell the include with the `lax/` prefix
(see "System headers and include paths" below). The **same** `-isystem`
argument MUST be applied uniformly to every `-O` level in the sweep so
comparisons are fair.

```
Tool:    lax_execute, binary="laxcc"
Input:   "-arch lax -au_count 16 -O0 -c --keep
          -isystem <LAX>/include
          -o kernel_O0.eln"
Repeat:  -O2, -O3, -Os (default sweep) with the SAME -isystem
```

For a pure-C snippet with no LAX headers, drop the `-isystem` argument from
every invocation.

### 3. Link each to .eld, disassemble, compare

```
Tool:    lax_execute, binary="laxcc", args="-arch lax -au_count 16 -o kernel_O3.eld kernel_O3.eln"
Tool:    lax_execute, binary="it3a-ds", args="kernel_O3.eld"
```

## Configuration

Key facts:
- `-Oz` is **not supported** on LAX
- Always compile with `--keep` to preserve `.sl` files for inspection
- Always link to `.eld` before measuring size; `.eln` is not representative
- Supported levels: `-O0` to `-O4` and `-Os`

### System headers and include paths

When compiling a source snippet with `lax_execute`, no include paths are on by
default -- if the source `#include`s any LAX system header (`intrinsics.h`,
`intrinsic_lax.h`, `math_vspa.h`, ...), you MUST add the LAX include directory
to every `-O`-level compile in the sweep, otherwise `laxcc` fails with
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

3. **Apply the SAME `-isystem` to every `-O` level in the sweep**. Differing
   include paths across levels invalidate the comparison (a header may resolve
   differently or not at all, producing incomparable `.sl` files or a broken
   sweep row).

4. **For a pure-C snippet with no LAX headers** (e.g. a scalar arithmetic test),
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
- If AU count is not specified, ask -- 16AU and 64AU produce different code.
- Never use `-Oz`, ARM flags.
- If the source `#include`s a LAX system header, add `-isystem <LAX>/include`
  AND ensure the include is spelled `<lax/HEADER.h>`. Do not pass two separate
  `-isystem` paths and do not use the bare `<HEADER.h>` form. The include
  argument must be identical across every `-O` level in the sweep.

**Resource limits**
- Default sweep: `-O0`, `-O2`, `-O3`, `-Os`. Add `-O4` only when user explicitly asks.

**Secrets**
- Do not log source content that may contain sensitive material.

## Workflow

### Step 1 -- Discover toolchain and confirm AU count
Call `list_lax_compiler_tools()`. Ask for AU count if not specified. If the source
uses LAX headers, derive the LAX include root by replacing the trailing `bin` in
`toolchain_bin_dir` with `include`.

### Step 2 -- Compile at each level

Base invocation (no LAX headers needed):

```jsonc
{
  "binary": "laxcc",
  "args": "-arch lax -au_count 16 -O3 -c --keep -o kernel_O3.eln",
  "input_code": "<user source>",
  "input_language": "c"
}
```

If the source uses any LAX system header (`intrinsics.h`, `intrinsic_lax.h`, etc.),
rewrite every affected `#include` to the `lax/`-prefixed form and add one
`-isystem` pointing at `<LAX>/include` -- to EVERY `-O` level in the sweep:

```jsonc
{
  "binary": "laxcc",
  "args": "-arch lax -au_count 16 -O3 -c --keep -isystem <LAX>/include -o kernel_O3.eln",
  "input_code": "#include <lax/intrinsics.h>\n<user source>",
  "input_language": "c"
}
```

Repeat with `-O0`, `-O2`, `-Os` (and optionally `-O4`), keeping every argument
identical except the `-O` level and the output name.

### Step 3 -- Link each object to .eld

```jsonc
{ "binary": "laxcc", "args": "-arch lax -au_count 16 -o kernel_O3.eld kernel_O3.eln" }
```

### Step 4 -- Measure size and disassemble

```jsonc
{ "binary": "it3a-ds", "args": "kernel_O3.eld" }
```

Count instruction bundles and `nopS`/`fnop` fills per level.

### Step 5 -- Read .sl assembly per level
The `.sl` in `saved_to` shows hardware-loop instructions, inlining markers, and vector
register usage (`v0..vN`). Compare between levels.

### Step 6 -- Present comparison and recommendation

```
Level   .eld bytes   ~instructions   HW loops   Notes
-O0     4096         180             no         debug only
-O2     2200          92             yes        basic scheduling
-O3     1800          64             yes        vectorized + unrolled
-Os     1650          70             yes        smallest, less vector reuse
```

| Goal | Recommendation |
|------|---------------|
| Debugging | `-O0` |
| Balanced production | `-O2` |
| DSP throughput-critical | `-O3` (try `-O4` for hot inner loops) |
| Tight code memory | `-Os` |

## Validation loop

1. `list_lax_compiler_tools()` returns a non-empty toolchain list.
2. If the source `#include`s a LAX header, verify it uses the `<lax/...>` prefix
   AND that every `-O`-level compile in the sweep contains the same
   `-isystem <LAX>/include` argument (exactly one).
3. Each compile+link exits 0 and `.sl` file is present in `saved_to`.
4. Summary comparison table is presented before detailed `.sl` output.
5. A concrete recommendation is given at the end.

## Out of scope

- ARM targets
- Symbol-level size analysis (use `lax-binary-analysis`)

## See Also

- `lax-binary-analysis` -- deep symbol-level analysis
- `lax-linker-explorer` -- linking behavior and `.lcf` analysis
- `lax-compiler-explorer` -- single optimization level inspection
- `gcc-benchmark-optimization` -- same workflow for ARM GCC
