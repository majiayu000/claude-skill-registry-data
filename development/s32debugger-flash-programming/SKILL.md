---
name: s32debugger-flash-programming
description: >
  Route S32Debugger flash requests to the correct specialized workflow. Use
  this whenever the user wants to flash, program, write, erase, verify, dump,
  or inspect flash contents, or wants to program an image and then continue
  debugging from flash in the same session, even if the user does not
  explicitly ask to choose between flash-only and debug-from-flash behavior.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32debugger
  depends_on: '[s32debugger-flash-only-operations, s32debugger-debug-from-flash]'
  tags: '[s32debugger, flash, routing]'
---

# S32Debugger Flash Programming

Route flash requests to the correct specialized S32Debugger workflow. This
skill classifies flash-only versus debug-from-flash intent, checks whether the
required live startup/probe context already exists, and preserves the key
behavioral difference between flows that end with `fl_close` and flows that
stay open for same-session debugging.

## When to use

Use this skill when:
- The user asks to flash, program, write, erase, verify, dump, or inspect
  flash contents through S32Debugger.
- The user wants to program an image and might also want to continue debugging
  from flash in the same session.
- The request needs routing before the flash leaf workflow is chosen.

Do **not** use this skill for:
- Detailed execution of an already classified flash-only request; use
  `s32debugger-flash-only-operations`.
- Detailed execution of an already classified same-session debug-from-flash
  request; use `s32debugger-debug-from-flash`.

## Quickstart

### 1. Mandatory reference read

Before using this skill, read:
- `references/authoring-procedure.md`
- `references/examples.md`

Do not continue until those files have been reviewed.

### 2. Classify the flash intent first

```
Scenario A: flash-only operation
Scenario B: flash now, then continue debugging from flash in the same session
Rule: keep end-with-fl_close and stay-open-for-debug clearly separated
```

### 3. Check whether required startup context already exists

```
Need: GTA before GDB, GDB with Python support, probe/session connection,
      valid bareboard init script for the flash path
```

### 4. Route to the correct leaf workflow

```
Flash-only:       s32debugger-flash-only-operations
Debug-from-flash: s32debugger-debug-from-flash
```

## Guardrails

**Mandatory reference rule**
- Read the listed reference files before selecting a branch, generating output,
  or producing the final answer.
- Treat the references as part of the skill, not as optional supplemental
  notes.
**Scope**
- Route flash requests only; do not blend the two leaf flows.
- Preserve the difference between a session that ends with `fl_close` and one
  that remains open for post-flash symbolic debug.
- Confirm whether required GDB/GTA/probe context already exists instead of
  pretending flash programming is always a zero-startup path.
- Defer low-level probe connection, init-script selection, and `board_init()` /
  `core_init()` mechanics to `s32debugger-connect-gdb-to-s32-debug-probe`.

**Destructive actions**
- Default to routing and classification rather than executing the flash leaf
  flow here.
- Do not merge flash-only and debug-from-flash into one vague sequence.
- Do not recommend `fl_close` for same-session debug-from-flash intent.

**Refuse-and-escalate**
- If the request is ambiguous about whether the session should end or remain
  open for debug, ask that specific question before routing.
- If startup/probe context is missing, say so explicitly instead of implying
  the leaf skill can start from nowhere.
- If a matching symbol file is required for debug-from-flash but not provided,
  treat that as a blocker for the debug-from-flash route.
- If the user really needs the low-level GDB connection procedure, hand off to
  `s32debugger-connect-gdb-to-s32-debug-probe`.

**Do**
- Use `s32flash.py` expectations as the shared flash substrate.
- Require a valid bareboard init script, not an attach script.
- Ask only for the smallest missing detail that blocks scenario classification.

**Do not**
- Use one blended flow for both scenarios.
- Skip `fl_close` for flash-only work.
- Use debug-from-flash continuation for generic erase, verify, read, or dump
  operations.

## Validation loop
0. Confirm the required reference files were reviewed before executing the
   workflow or finalizing the answer.
1. Confirm the request is classified as flash-only or debug-from-flash.
2. Verify the required startup context is checked: GTA before GDB, Python-capable
   GDB, probe/session connection, and valid bareboard init path.
3. Verify the chosen downstream skill matches the intended end state: close the
   flash session or keep the same GDB session open.
4. Verify any required artifacts are identified: image/binary/ELF and matching
   symbol file when debug-from-flash is requested.
5. Verify no low-level probe connection procedure is being restated here.
6. Return the classified scenario, chosen downstream skill, context readiness,
   intended end state, key next step, and any missing blocker.

## Out of scope

- Executing both flash leaf behaviors inside one blended skill body.
- Pretending required GDB/GTA/probe context already exists when it does not.
- Replacing the low-level probe connection skill.
- Guessing the user intent when the distinction between close-and-stop and
  continue-debugging is still unresolved.

## See Also

- `references/authoring-procedure.md` - scenario classification, shared
  prerequisites, and routing logic.
- `references/examples.md` - quick routing examples, anti-patterns, and
  response cues.
- Related skills: `s32debugger-flash-only-operations`,
  `s32debugger-debug-from-flash`,
  `s32debugger-connect-gdb-to-s32-debug-probe`,
  `s32debugger-error-resolution`
