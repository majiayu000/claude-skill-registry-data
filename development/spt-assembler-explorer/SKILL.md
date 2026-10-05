---
name: spt-assembler-explorer
description: >
  Interactive assemble-and-inspect workflow for the SPT3.8 toolchain (as-spt, objdump-spt).
  Assembles SPT3.8 source (.spt files), adds the correct .include directives and -I path
  for predefined memory symbols, and disassembles the ELF to show real SPT encoding. Use
  when the user asks "assemble this SPT snippet", "how does SPT encode this instruction",
  or "which address does OR_2_5_3 map to".
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: compiler
  tags: '[compiler, spt, spt3.8, as-spt, objdump-spt, assembler, disassembly, radar, dsp, s32r, embedded]'
---

# SPT3.8 Assembler Explorer (NXP SPT / Radar Signal Processing Toolbox)

Assemble SPT3.8 source code using a locally installed SPT3.8 toolchain, produce the ELF
output, and disassemble it with `objdump-spt`. Everything -- syntax, mnemonics, operand
order, `.include` directives -- must match the SPT3.8 Assembler Manual.

> SPT is a radar signal processing accelerator on S32R. There is **no C/C++ compiler**.
> Do not use `-mcpu=`, `-O*`, or any ARM flags.

## When to use

Use this skill when:
- User asks "assemble this SPT snippet"
- User asks "how does the SPT assembler encode this instruction?"
- User asks "which absolute address does `OR_2_5_3` map to?"
- User wants an example of an SPT instruction

Do **not** use this skill for:
- C/C++ compilation for LAX or ARM
- Section/symbol size analysis -> use `spt-binary-analysis`

## Available Capabilities

| Type | Name | Invocation |
|------|------|------------|
This skill uses the standardized `search_actions` + `execute_action` MCP tool surface.

| Action name | Purpose |
|------|------|
| `compiler.list_spt_tools` | Discover toolchain and inc/ folder; call first |
| `compiler.spt_execute` | Run `as-spt`, `objdump-spt`, and other SPT binutils |

## Quickstart

### 1. Discover toolchain

```
Tool:   list_spt_compiler_tools
Output: toolchain_bin_dir, path to inc/ folder (wr.inc, spr.inc, tram.inc, oram.inc)
```

### 2. Assemble

```
Tool:    spt_execute, binary="as-spt"
Input:   args="-I<path_to_inc>", input_code="<source with .include>", input_language="spt"
Output:  a.out (ELF)
```

### 3. Disassemble

```
Tool:    spt_execute, binary="objdump-spt", args="-Dr a.out"
Output:  128-bit instruction listing with 4x32-bit encoding words
```

## Configuration

Include-file mapping (always add the matching `.include` for symbols used):

| Symbol prefix | Include file |
|--------------|-------------|
| `WR_0..WR_63` | `wr.inc` |
| `SPR_*`, `HW_SPR_*`, `EVT_SPR_*`, `CHRP_SPR_*` | `spr.inc` |
| `TR_<bank>_<col>_<slice>` | `tram.inc` |
| `OR_<bank>_<col>_<slice>` | `oram.inc` |

Assembler key facts:
- Source files must use the `.spt` extension
- Immediates use `#` prefix on `add`, `cmp`, `loop`, `set`, `sub`
- Operand order is fixed per the manual; do not rearrange
- Output is ARM EABI compatible ELF (32-bit default, `-a64` for 64-bit)

## Guardrails

**Scope**
- Only calls `list_spt_compiler_tools` and `spt_execute`. No user files modified.

**Destructive actions**
- All output goes to the tool's isolated scratch directory.

**Refuse-and-escalate**
- If no SPT3.8 toolchain found, stop and tell the user.
- Do not invent mnemonics, operand values, or instruction forms not in the manual.
- Do not feed C/C++ source to `as-spt` -- it is assembly-only.
- Do not use stock GNU `objdump` on SPT ELFs -- use `objdump-spt`.

**Resource limits**
- Limit each assembly session to a single snippet or small file.

**Secrets**
- Do not log source content that may contain sensitive material.

## Workflow

### Step 1 -- Discover toolchain
Call `list_spt_compiler_tools()`. Identify `toolchain_bin_dir` and the `inc/` folder.

### Step 2 -- Draft the source
1. Identify every symbol prefix used (`WR_*`, `SPR_*`, `TR_*`, `OR_*`).
2. Add matching `.include "<file.inc>"` at the top.
3. Use `#<value>` for immediates on `add`, `cmp`, `loop`, `set`, `sub`.
4. Keep operand order exactly as in the manual.
5. Name the file `.spt` (set `input_language: "spt"`).

### Step 3 -- Assemble

```jsonc
{
  "toolchain_bin_dir": "<bin dir>",
  "binary": "as-spt",
  "args": "-I<path_to_inc>",
  "input_code": "<source with .include directives>",
  "input_language": "spt"
}
```

### Step 4 -- Disassemble

```jsonc
{
  "toolchain_bin_dir": "<bin dir>",
  "binary": "objdump-spt",
  "args": "-Dr <artifact_path>"
}
```

Each 128-bit SPT instruction prints on one line with 4 x 32-bit encoding words.
Omitted operands appear explicitly with their implicit encoded value.

### Step 5 -- Explain the result
Reprint the disassembly, cite field slicing from the manual, note which operands were
omitted and their implicit values, and explain which `.include` was needed and why.

## Validation loop

1. `list_spt_compiler_tools()` returns a non-empty toolchain list.
2. Every predefined symbol in the source has a matching `.include` at the top.
3. `as-spt` exits 0.
4. `objdump-spt -Dr` output is non-empty and encoding is explained.

## Out of scope

- C/C++ compilation (SPT3.8 has no C compiler)
- Section-level size analysis (use `spt-binary-analysis`)

## See Also

- `spt-binary-analysis` -- section and symbol size analysis
