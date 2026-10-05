---
name: lax-linker-explorer
description: >
  Analyze linking behavior of the NXP LAX toolchain (laxcc + .lcf linker command file).
  Explains how .eln object files, the EWL runtime, and the .lcf script combine into a
  final .eld image. Use when the user asks "why is my LAX firmware large", "why is this
  function still linked", "how do my LAX sections lay out", or "how do I use a custom
  startup on LAX".
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: compiler
  tags: '[lax, laxcc, linker, lcf, eld, sections, size, vector, vspa, dsp, s32, embedded]'
---

# LAX Linker Explorer (Embedded / LAX VSP)

Analyze how the LAX toolchain links `.eln` object files into a final `.eld` image and
explain why certain code or data is included, how sections are organized, and how the
linker command file (`.lcf`) and startup files affect the result.

## When to use

Use this skill when:
- User asks "why is my LAX firmware so large?"
- User asks "why is this function still being linked into my `.eld`?"
- User asks "how are my LAX sections laid out?"
- User asks "how do I use a custom startup on LAX?"

Do **not** use this skill for:
- Comparing optimization levels -> use `lax-benchmark-optimization`
- Assembly inspection -> use `lax-compiler-explorer`
- Symbol-level size ranking -> use `lax-binary-analysis`

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
| MCP tool | `list_lax_compiler_tools` | Discover toolchain; call first |
| MCP tool | `lax_execute` | Run `laxcc` and `it3a-ds` |

## Quickstart

### 1. Compile with --keep

```
Tool:    lax_execute, binary="laxcc"
Input:   "-arch lax -au_count 16 -O3 -c --keep -o main.eln"
```

### 2. Link to .eld (default LCF for the chosen AU count)

Pass the default LCF for the chosen `-au_count` via `-mem <lcf>`. Without it,
`laxcc` invokes the linker (`it3a-ld`) which aborts with
`Fatal(F2000): no linker command file specified`.

```
Tool:    lax_execute, binary="laxcc"
Input:   "-arch lax -au_count 16
          -mem <LAX>/etc/vspa3_16au/lcf/vspa3_16au_max.lcf
          -o project.eld main.eln"
```

For 2 AU or 64 AU, swap the `.lcf` accordingly (see "Default LCF selection"
below). The `-au_count` and the `.lcf` must be from the same AU family.

### 3. Inspect sections via it3a-ds

```
Tool:    lax_execute, binary="it3a-ds", args="project.eld"
```

## Configuration

Key toolchain facts:
- Section placement is `.lcf`-driven, not compiler-flag-driven
- EWL runtime provides the default startup; override with `-nostartup-files`
- Do not use GCC-style linker flags (`-Wl,...`); LAX links via `laxcc`
- `.bss` must be cleared by startup code
- The linker command file is passed via `-mem <lcf>` (NOT `-T` and NOT `-Xlinker -T`).
  `-Xlinker -T` is accepted for a *custom* LCF, but the LAX default LCFs are
  designed to be passed with `-mem`.

### Default LCF selection

`laxcc` does not auto-pick an `.lcf`. You MUST pass exactly one via `-mem <path>`
and it MUST match the `-au_count`. The three defaults shipped with S32DS live
under `<LAX>/etc/`, where `<LAX>` is `toolchain_bin_dir` with the trailing `bin`
replaced by nothing (or explicitly: `<S32DS root>/build_tools/LAX`).

| AU count | Flag to laxcc | Default LCF (relative to `<LAX>`) |
|---------:|---------------|-----------------------------------|
|  2 AU    | `-au_count 2`  | `etc/vspa3_2au/lcf/vspa3_2au_max.lcf`   |
| 16 AU    | `-au_count 16` | `etc/vspa3_16au/lcf/vspa3_16au_max.lcf` |
| 64 AU    | `-au_count 64` | `etc/vspa3_64au/lcf/vspa3_64au_max.lcf` |

**Naming pattern (do not guess elsewhere):**
```
<LAX>/etc/vspa3_<N>au/lcf/vspa3_<N>au_max.lcf
```

**Deriving `<LAX>` from `toolchain_bin_dir`:** drop the trailing `bin`
component. Example: `C:/NXP/S32DS.3.5/S32DS/build_tools/LAX/bin`
-> `<LAX>` = `C:/NXP/S32DS.3.5/S32DS/build_tools/LAX`
-> LCF for 16 AU = `<LAX>/etc/vspa3_16au/lcf/vspa3_16au_max.lcf`.

**Consistency rule:** the AU number in the `.lcf` path must match the
`-au_count` value on the command line. Mixing them (e.g. `-au_count 16` with
`vspa3_64au_max.lcf`) produces silent misplacement, address-out-of-range
errors, or a broken image.

### EWL runtime pieces (when linking a program with `main`)

The default LCF alone is not enough to resolve `_start`, `___internal_done`,
and `___exec_staticinit` when linking a program with `int main(...)`. Add the
three EWL runtime sources to the link line (they live under `<LAX>/ewl/`):

```
<LAX>/ewl/EWL_Runtime/Runtime_VSPA/src/startup_vspa3.s   # provides _start
<LAX>/ewl/EWL_Runtime/Runtime_VSPA/src/done.asm          # provides ___internal_done
<LAX>/ewl/EWL_Runtime/Runtime_VSPA/src/staticinit.c      # provides ___exec_staticinit
```

For a **kernel-only** `.eln` (no `main`, meant to be called by a host), you
still need `-mem <lcf>` for placement but you do NOT need the three EWL
runtime files. The linker will report benign
`Warning(W2003): undefined input symbol '_start'` and can be treated as a
library-object build.

### Custom startup / custom LCF

Override the default startup with `-nostartup-files` and your own file:

```
laxcc -arch lax -au_count 16
      -mem <LAX>/etc/vspa3_16au/lcf/vspa3_16au_max.lcf
      -nostartup-files userdefined_startup.s test.c -o test.eld
```

Use a fully custom LCF by passing it via `-mem`:
```
-mem C:/path/to/project.lcf
```
(`-Xlinker -T project.lcf` is accepted but non-idiomatic on LAX.)

## Guardrails

**Scope**
- Only calls `list_lax_compiler_tools` and `lax_execute`. No user files modified.

**Destructive actions**
- All output goes to the tool's isolated scratch directory.

**Refuse-and-escalate**
- If no LAX toolchain found, stop and tell the user.
- If the AU count is not specified, ask before linking -- the LCF and the
  `-au_count` MUST match.
- Do not use GCC linker flags with `laxcc`.
- Do not run `nm`/`size`/`objdump` on `.eld` -- use `it3a-ds`.
- Never omit `-mem <lcf>` on a link step -- the linker aborts with
  `Fatal(F2000): no linker command file specified`.
- Never mix the AU number in the `.lcf` path with a different `-au_count`
  value on the command line.

**Resource limits**
- Do not disassemble very large `.eld` files without user confirmation.

**Secrets**
- Do not expose sensitive content from data sections.

## Workflow

### Step 1 -- Discover toolchain, confirm AU count, resolve LCF
Call `list_lax_compiler_tools()`. Ask for AU count if not specified. Derive
`<LAX>` from `toolchain_bin_dir` and compose the default LCF path:

```
<LAX>/etc/vspa3_<N>au/lcf/vspa3_<N>au_max.lcf
```

Compile each source file with `--keep` so `.sl` files are available for
cross-reference.

### Step 2 -- Link to .eld

Default link (kernel-only object -- no `main`):

```jsonc
{
  "binary": "laxcc",
  "args": "-arch lax -au_count 16
           -mem <LAX>/etc/vspa3_16au/lcf/vspa3_16au_max.lcf
           -o project.eld main.eln"
}
```

Full-program link (with `main` and EWL startup):

```jsonc
{
  "binary": "laxcc",
  "args": "-arch lax -au_count 16
           -mem <LAX>/etc/vspa3_16au/lcf/vspa3_16au_max.lcf
           -o project.eld main.eln
           <LAX>/ewl/EWL_Runtime/Runtime_VSPA/src/startup_vspa3.s
           <LAX>/ewl/EWL_Runtime/Runtime_VSPA/src/done.asm
           <LAX>/ewl/EWL_Runtime/Runtime_VSPA/src/staticinit.c"
}
```

Custom-startup link:

```jsonc
{
  "binary": "laxcc",
  "args": "-arch lax -au_count 16
           -mem <LAX>/etc/vspa3_16au/lcf/vspa3_16au_max.lcf
           -nostartup-files userdefined_startup.s test.c
           -o test.eld"
}
```

Custom-LCF link: replace the `-mem` path with the user's own `.lcf`.

### Step 3 -- Inspect sections
Run `it3a-ds project.eld`. Each section header is `.section .text$<symbol>`, `.data`,
`.bss`, or `.rodata`. Compare against the `.lcf` to confirm placement.

### Step 4 -- Rank contributors and trace origins
For top `.text$<sym>` sections:
- **Direct reference** -- user code calls the symbol
- **Transitive call** -- pulled in through another function
- **Runtime dependency** -- EWL startup, C++ ctors, math helpers
- **`.lcf` KEEP** -- linker command file forces retention

### Why binaries are large

| Contributor | How to identify | Fix |
|------------|-----------------|-----|
| Double-precision math | Large `_f*_soft` helpers | Convert to `float` |
| stdio / printf | printf symbols present | Avoid stdio in LAX code |
| Unused functions via KEEP | Section present with no callers | Trim `.lcf` KEEP |
| Constants in `.data` | Missing `const` | Add `const` |
| Loop unrolling | Large `.text$<sym>` at high `-O` | Try `-Os` |

## Validation loop

1. `list_lax_compiler_tools()` returns a non-empty toolchain list.
2. The link command includes exactly one `-mem <lcf>`, and the AU number in the
   `.lcf` path matches the `-au_count` argument.
3. Compile and link both exit 0 (kernel-only builds may show benign
   `Warning(W2003): undefined input symbol '_start'` -- acceptable when the
   `.eln` is intended to be called by a host, not booted standalone).
4. `it3a-ds project.eld` lists all sections.
5. Each unexpected section is explained with root cause and fix.

## Out of scope

- ARM linking
- Optimization level comparison (use `lax-benchmark-optimization`)

## See Also

- `lax-binary-analysis` -- symbol-level size ranking
- `lax-benchmark-optimization` -- optimization level comparison
- `lax-compiler-explorer` -- per-function assembly inspection
