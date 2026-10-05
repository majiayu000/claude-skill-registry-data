---
name: s32debugger-flash-only-operations
description: >
  Execute S32Debugger flash-programmer operations that end after the flash
  action completes. Use this whenever the user wants to flash, program, write,
  erase, verify, dump, read, or inspect flash contents without continuing into
  debug-from-flash in the same GDB session, and when the flash session must be
  closed correctly with `fl_close`.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32debugger
  depends_on: '[s32debugger-connect-gdb-to-s32-debug-probe]'
  tags: '[s32debugger, flash, execution]'
---

# S32Debugger Flash-Only Operations

Execute flash-programmer operations that end when the flash action is complete.
This is the leaf workflow for flash-only behavior: use the correct bareboard
flash setup, execute the requested operation, and close the flash session
cleanly with `fl_close` without drifting into debug-from-flash continuation.

## When to use

Use this skill when:
- The request is clearly flash-only: write, program, erase, verify, dump,
  read, or inspect flash contents.
- The user wants the flash action to complete and then the flash session to end
  cleanly.
- The correct end state is `fl_close`, not continued symbolic debug in the same
  GDB session.

Do **not** use this skill for:
- Requests that should continue into same-session debug-from-flash; use
  `s32debugger-debug-from-flash`.
- Ambiguous flash requests that still need routing; use
  `s32debugger-flash-programming`.

## Quickstart

### 1. Mandatory reference read

Before using this skill, read:
- `references/authoring-procedure.md`
- `references/examples.md`

Do not continue until those files have been reviewed.

### 2. Confirm the request is flash-only

```
Need: write/program | dump/read | erase | verify | info
Rule: flow ends after the flash action; no post-flash symbolic continuation
```

### 3. Source and configure the flash programmer

```gdb
source "<S32Debugger>/Debugger/scripts/gdb_extensions/flash/s32flash.py"
# set parameters from check_fp_global_parameters() and setup()
```

### 4. Execute the flash action and close in this exact order

1. run the requested flash command
2. verify the flash action completed successfully
3. execute `fl_close`
4. stop; do not continue into debug-from-flash steps in this workflow

```gdb
# run requested flash command
fl_close
```

## Guardrails

**Mandatory reference rule**
- Read the listed reference files before selecting a branch, generating output,
  or producing the final answer.
- Treat the references as part of the skill, not as optional supplemental
  notes.
**Scope**
- Execute only flash-only operations.
- Use a valid bareboard init script, not an attach script.
- Keep flash-only behavior distinct from debug-from-flash continuation.
- Use parameter names and variable expectations from `s32flash.py`.

**Destructive actions**
- Default to ending the flash session cleanly with `fl_close`.
- Do not continue into `py reset()`, `flushregs`, `set $pc=$PC`, or
  `symbol-file` unless the user explicitly wants debug-from-flash instead.
- Do not substitute partial cleanup for `fl_close`.

**Refuse-and-escalate**
- If the request is ambiguous between flash-only and same-session debug, stop
  and route through `s32debugger-flash-programming`.
- If a valid bareboard init script is missing, ask for it instead of using an
  attach script.
- If GTA-before-GDB or live session prerequisites are missing, ask for the
  missing startup/session context before claiming the flash-only workflow is
  ready.
- For low-level probe connection, init-script selection, or `board_init()` /
  `core_init()` mechanics, defer to
  `s32debugger-connect-gdb-to-s32-debug-probe`.

**Do**
- Source `s32flash.py`.
- Read required parameter names from `check_fp_global_parameters()` and
  `setup()`.
- Use a full absolute path for the bareboard init script.

**Do not**
- Skip `fl_close`.
- Use attach scripts as flash init scripts.
- Guess parameter names instead of grounding them in `s32flash.py`.

## Validation loop
0. Confirm the required reference files were reviewed before executing the
   workflow or finalizing the answer.
1. Confirm the operation is flash-only and not debug-from-flash.
2. Verify GTA is started before GDB and a GDB/Python session context is
   available.
3. Verify `s32flash.py` is sourced and a valid bareboard init script is used.
4. Verify the requested flash operation completes successfully.
5. Verify no post-flash debug continuation occurs.
6. Verify `fl_close` executes at the end and the flash session closes cleanly.

## Out of scope

- Post-flash symbolic continuation in the same session.
- Using attach scripts for flash execution.
- Guessing whether the request should be flash-only or debug-from-flash.
- Replacing `fl_close` with manual or partial cleanup.

## See Also

- `references/authoring-procedure.md` - flash-only execution sequence and
  init-script rules.
- `references/examples.md` - flash-only examples, anti-patterns, and checks.
- Related skills: `s32debugger-flash-programming`,
  `s32debugger-debug-from-flash`,
  `s32debugger-connect-gdb-to-s32-debug-probe`,
  `s32debugger-error-resolution`
