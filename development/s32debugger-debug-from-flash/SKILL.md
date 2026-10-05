---
name: s32debugger-debug-from-flash
description: >
  Execute the S32Debugger workflow that programs an image and then continues
  debugging from flash in the same GDB session. Use this whenever the user
  wants to flash an ELF or image and keep the session alive for symbolic debug
  afterward, continue in the same GDB session after programming, or apply the
  post-flash reset/register-cache/PC/symbol sequence instead of ending the
  flow with `fl_close`.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32debugger
  tags: '[s32debugger, flash, debug]'
---

# S32Debugger Debug From Flash

Execute the same-session workflow that programs flash and then continues into
symbolic debugging from the flashed image. This skill is the leaf execution
path for debug-from-flash, not a generic flash-operation router, and it keeps
post-flash debug continuation explicit and ordered.

## When to use

Use this skill when:
- The user wants to program an image and then continue debugging from flash in
  the same GDB session.
- The user explicitly wants post-flash reset, register refresh, PC update, and
  `symbol-file` loading instead of a flash-only closeout.
- A matching ELF or symbol file is available for post-flash debug context.

Do **not** use this skill for:
- Ambiguous requests that may be flash-only; route through
  `s32debugger-flash-programming`.
- Generic read, erase, verify, dump, or flash-only write operations; use
  `s32debugger-flash-only-operations`.

## Quickstart

### 1. Mandatory reference read

Before using this skill, read:
- `references/authoring-procedure.md`
- `references/examples.md`

Do not continue until those files have been reviewed.

### 2. Confirm same-session debug-from-flash intent

```
Need: programmed artifact + matching ELF/symbol file + live GTA/GDB context
Rule: keep the same GDB session alive after flash programming
```

### 3. Source and run the flash programmer

```gdb
source "<S32Debugger>/Debugger/scripts/gdb_extensions/flash/s32flash.py"
# configure parameters from s32flash.py
# run the write/program operation
```

### 4. Continue into debug-from-flash in this exact order

1. `py reset()`
2. `flushregs`
3. `set $pc=$PC`
4. `symbol-file "<path_to_symbols>.elf"`

```gdb
py reset()
flushregs
set $pc=$PC
symbol-file "<path_to_symbols>.elf"
```

## Guardrails

**Mandatory reference rule**
- Read the listed reference files before selecting a branch, generating output,
  or producing the final answer.
- Treat the references as part of the skill, not as optional supplemental
  notes.
**Scope**
- Execute only the debug-from-flash leaf workflow.
- Keep flash programming and post-flash debug continuation in the same GDB
  session.
- Require valid symbol context for the debug continuation step.
- Keep the distinction from flash-only behavior explicit.

**Destructive actions**
- Default to same-session continuation only when the user clearly wants
  debug-from-flash.
- Do not end the flow with `fl_close`.
- Do not use `load` as a substitute for post-flash symbolic continuation.

**Refuse-and-escalate**
- If the request is still ambiguous between flash-only and debug-from-flash,
  stop and route through `s32debugger-flash-programming`.
- If no matching ELF or symbol file is available, stop rather than continuing
  without valid debug symbols.
- If GTA-before-GDB or live session prerequisites are missing, ask for the
  missing startup/session context before claiming the same-session flow is
  ready.
- For low-level probe connection, init-script selection, or `board_init()` /
  `core_init()` mechanics, defer to
  `s32debugger-connect-gdb-to-s32-debug-probe`.

**Do**
- Source `s32flash.py`.
- Take variable names and kwargs from `s32flash.py`.
- Keep the session open and debug-ready after flashing when requested.

**Do not**
- Behave like a generic flash-only workflow.
- Continue without a matching ELF/symbol file.
- Guess flash-only vs debug-from-flash when the user intent is unclear.

## Validation loop
0. Confirm the required reference files were reviewed before executing the
   workflow or finalizing the answer.
1. Confirm the user explicitly wants debug-from-flash in the same GDB session.
2. Verify GTA is started before GDB and a live GDB/Python session context is
   present.
3. Verify `s32flash.py` is sourced and the flash write operation completes.
4. Verify the post-flash sequence runs in order: `py reset()`, `flushregs`,
   `set $pc=$PC`, `symbol-file <matching-elf>`.
5. Verify `fl_close` is not used and the session remains open for follow-up
   debug actions.
6. Return the programmed artifact, flash-write status, symbol file used,
   whether continuation succeeded, and whether the session remains open.

## Out of scope

- Generic flash-only operations.
- Reclassifying ambiguous flash requests locally instead of routing.
- Using `load` instead of `symbol-file` after flashing.
- Continuing into symbolic debug without a matching ELF.

## See Also

- `references/authoring-procedure.md` - same-session debug-from-flash sequence
  and prerequisites.
- `references/examples.md` - quick examples, anti-patterns, and verification
  cues.
- Related skills: `s32debugger-flash-programming`,
  `s32debugger-flash-only-operations`,
  `s32debugger-connect-gdb-to-s32-debug-probe`,
  `s32debugger-error-resolution`
