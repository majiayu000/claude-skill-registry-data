---
name: s32debugger-ccs-execution-router
description: >
  Route CCS execution requests to the correct standalone CCS Tcl workflow.
  Use this whenever the user mentions CCS, the CCS executable (`ccs` /
  `ccs.exe`), CCS Tcl, probe connection,
  target identification, get_target_info, debug lock status, core status,
  attach-ready targets, bring-up from reset, CCS as a fallback after failed
  GDB startup, or a family-specific CCS attach/core-status sanity check. This
  skill classifies the goal as generic discovery, attach-ready attach/control,
  needs initialization, post-GDB-failure diagnostic isolation, or
  family-specific CCS attach/core-status sanity validation, and treats CCS as the
  first path for sanity checks, target identification, and core-state requests
  when no interactive debug session is already active.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32debugger
  depends_on: '[s32debugger-ccs-generate-self-contained-tcl, s32debugger-ccs-run-tcl-script]'
  tags: '[s32debugger, ccs, routing]'
---

# S32Debugger CCS Execution Router

Route a CCS request to the narrowest correct standalone Tcl workflow before any
script is generated or executed. This skill separates generic discovery,
attach-ready control, bring-up, post-GDB-failure isolation, and
family-specific attach/core-status sanity validation so downstream CCS work is
chosen deliberately rather than guessed.

## When to use

Use this skill when:
- The user asks for CCS, the CCS executable (`ccs` / `ccs.exe`), or CCS Tcl
  generation/execution.
- The user wants target identification, target info, attach, core status, or a
  family-specific CCS attach sanity check.
- The user wants CCS used as a fallback to isolate whether a failed GDB flow is
  a lower-layer probe/target issue or a higher-layer GDB/session issue.
- The user wants a probe sanity check, target identification, or core-state
  collection and no interactive debug session is already active.

Do **not** use this skill for:
- Writing the Tcl body directly; route to
  `s32debugger-ccs-generate-self-contained-tcl`.
- Executing an already chosen script without routing/classification; use
  `s32debugger-ccs-run-tcl-script`.

## Quickstart

### 1. Mandatory reference read

Before using this skill, read:
- `references/authoring-procedure.md`
- `references/examples.md`

Do not continue until those files have been reviewed.

### 2. Triage probe occupancy first when a probe IP is known

```
Input:   probe IP
Check:   reachability -> open telnet session -> run `who` inside it
Rule:    a `ccs` process in the `who` output == busy; no `ccs` process == ready
Output:  stop immediately if a `ccs` process owns the probe; otherwise continue
```

### 3. Apply the CCS-first observational rule

Apply the **CCS-first observational rule**.
See `references/authoring-procedure.md`.

### 4. Keep the minimum ordered generic-discovery sequence inline

Use this exact order when routing or sketching the minimum generic CCS fallback:
1. basic probe reachability check
2. open a telnet session to `<probe-ip>` and issue `who` inside it
3. if the `who` output shows a `ccs` process, report the probe as busy and stop
   immediately; if no `ccs` process is listed, the probe is ready, so continue
4. `config cc s32dbg:<probe-ip>`
5. optional `ccs::config_server ...` only when a grounded flow supports it
6. set an init sequence before chain creation; minimum fallback:
   `ccs::config_init_action 1 2 0 0 0 0`
7. `ccs::config_chain {s32cc dap}`
8. `display ccs::get_target_info`

### 5. Keep the routing matrix inline

| User need / proven layer | Route |
| --- | --- |
| need Tcl body, script not yet written | `s32debugger-ccs-generate-self-contained-tcl` |
| existing Tcl should be run or validated | `s32debugger-ccs-run-tcl-script` |
| failed GDB flow, lower layers unproven | generic discovery first |
| generic discovery already succeeded, family chain still unproven | family-specific attach/core-status sanity |
| attach-ready target, no init needed | attach/control Tcl path |
| target clearly needs bring-up from reset | init/bring-up Tcl path |

### 6. Keep CCS output and transport rules visible

```
Prefer: `s32dbg:<probe-ip>` in new user-facing flows
Prefer: human-readable `display` forms for discovery/status
Rule:   generic `s32cc dap` discovery should stay the first CCS fallback after
        ambiguous GDB failure unless deeper family validation is already justified
Rule:   apply the **CCS-first observational rule**
```

### 7. Classify capture mode for observational checkpoints

```
Result-capture mode:  checkpoint returns a Tcl value
Display-capture mode: checkpoint prints through `display`, `puts`, or `cputs`
Default:              treat `ccs::all_run_mode` as display-capture mode
```

If later execution evidence is required, preserve the mandated checkpoint and
route to a downstream path that uses the correct capture mode.

## Guardrails

**Mandatory reference rule**
- Read the listed reference files before selecting a branch, generating output,
  or producing the final answer.
- Treat the references as part of the skill, not as optional supplemental
  notes.

**Scope**
- Route CCS requests only; do not generate the Tcl body here.
- Keep generation and execution as separate decisions.
- Preserve the five-state classification: generic discovery, attach-ready,
  needs initialization, post-GDB-failure isolation, and family-specific
  attach/core-status sanity validation.
- For family-specific attach or init behavior, rely on the knowledge DB rather
  than invented CCS syntax or guessed initialization sequences.
- Apply the **CCS-first observational rule** for observational requests.
- Distinguish routing by target state from routing by capture mode.

**Destructive actions**
- Default to routing and script selection, not execution.
- If a downstream flow starts the CCS executable (`ccs` / `ccs.exe`), it should terminate that process at
  request completion unless the user explicitly asks to keep CCS open.
- If telnet `who` shows another CCS client, stop immediately instead of trying
  repeated CCS connects.

**Refuse-and-escalate**
- If target state is unclear and it changes the Tcl shape, ask whether the user
  wants generic discovery, attach-ready control, family-specific attach/status,
  full bring-up from reset, or post-GDB-failure sanity isolation.
- If the **CCS-first observational rule** applies, do not detour into a fresh
  GDB live-session path before CCS Layers 0-2 are considered.
- If a failed GDB flow has not yet proven lower layers, route to fast probe
  triage plus generic discovery before any deeper attach/init path.
- If family-specific chain support appears missing locally, fall back to
  generic discovery unless the user explicitly needs KB-backed bring-up logic.
- If early probe triage was impossible and a later CCS connect fails, require
  telnet `who` before concluding anything deeper.
- If the mandated checkpoint is display-oriented, do not substitute a different
  command just to simplify capture.

**Do**
- Prefer `s32dbg:<probe-ip>` in new user-facing flows.
- Prefer human-readable `display` forms for discovery and status output when
  CCS supports them.
- Stop at generic `s32cc dap` discovery when that already answers the request.
- Route `ccs::all_run_mode` requests as display-capture mode unless grounded
  local evidence proves otherwise.

**Do not**
- Invoke `ccs` / `ccs.exe` directly via `execute_command` or any shell command;
  always route script execution through the `control.run_ccs_tcl` MCP action.
  Search the S32Debugger MCP catalog (`s32debugger_search_actions`) before
  attempting any shell-level CCS invocation — if the action is present, use it.
- Jump directly to family-specific attach or full bring-up after a failed GDB
  session when generic visibility is still unproven.
- Treat `config cc` success as proof that attach/init will succeed.
- Use KB helper proc names as if they are live runtime commands without proof.
- Start, prepare, or inspect a fresh GDB live-session path when the
  **CCS-first observational rule** applies.
- Change the family-status checkpoint instead of changing the capture method.

### Clarifying-question priority

Ask only what blocks route choice:
1. generate or run?
2. generic discovery or family-specific sanity?
3. attach-ready or needs initialization?
4. all-core status or one-core status, if family-specific sanity is requested?
5. if execution evidence is required, is the proof command expected to be
   result-captured or display-captured?

### Result contract

A good routing result should contain:
- normalized CCS goal
- target-state classification
- chosen downstream skill or CCS layer
- chosen capture mode when relevant
- smallest missing blocker
- short reason for the route

## Validation loop
0. Confirm the required reference files were reviewed before executing the
   workflow or finalizing the answer.
1. Confirm the request is normalized as generate, run, generate-and-run,
   inspect CCS failure, diagnose failed GDB via CCS, or family-specific sanity.
2. Confirm target state is classified as one of the five supported states.
3. If a probe IP is known, verify the fast path was considered: reachability,
   telnet `who`, busy vs free.
4. Verify the **CCS-first observational rule** was applied correctly.
5. Verify the chosen route is the narrowest downstream skill that fits the
   proven layer: generation vs execution, generic vs family-specific, attach vs
   bring-up.
6. Verify the capture mode is identified when the request depends on later
   machine-readable execution evidence.
7. Verify no hidden file-path, family-support, or init-sequence assumptions were
   introduced.
8. Return a short routing summary with normalized goal, target-state
   classification, chosen path, capture mode if relevant, reason, smallest
   missing input, and any GDB-layer isolation hypothesis.

## Out of scope

- Authoring the full Tcl script body.
- Executing a script before routing/classification is settled.
- Treating family-specific core-status validation as proof of load/run or full
  bring-up behavior.
- Skipping probe occupancy checks when the probe IP is already known.
- Violating the **CCS-first observational rule**.

## See Also

- `references/authoring-procedure.md` - routing decision tree, capability
  ladder, output-semantics routing, and classification guidance.
- `references/examples.md` - common triggers, anti-patterns, and concise
  question templates.
- Related skills: `s32debugger-ccs-generate-self-contained-tcl`,
  `s32debugger-ccs-run-tcl-script`, `s32debugger-error-resolution`
