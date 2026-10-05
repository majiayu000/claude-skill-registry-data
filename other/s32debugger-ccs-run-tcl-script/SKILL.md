---
name: s32debugger-ccs-run-tcl-script
description: >
  Execute or validate a CCS Tcl script with the CCS executable (`ccs` on
  Linux, `ccs.exe` on Windows). Use this whenever the
  user wants to start CCS, run a CCS Tcl script headlessly or with a visible
  CCS workflow, prove whether a target-discovery or attach script actually ran,
  troubleshoot why CCS succeeded at probe setup but failed later at generic
  chain, family-specific chain, attach, or initialization steps, or run a
  family-specific attach/core-status sanity test. Use this for evidence-based
  CCS execution reporting, especially when comparing CCS results against a
  prior GDB failure.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32debugger
  tags: '[s32debugger, ccs, execution]'
---

# S32Debugger Run CCS Tcl Script

Execute a CCS Tcl script and report what was actually proven. This skill is for
runtime evidence: starting the CCS executable (`ccs` on Linux, `ccs.exe` on
Windows), choosing visible vs headless execution,
validating script progress, separating probe success from deeper chain/init
failures, and explaining what CCS results do and do not prove about a prior
GDB failure.

This skill is the single documented caller of the `control.run_ccs_tcl`
action. The router and generation skills classify and author the script; they
do not invoke the action themselves. The action is a thin mechanism: it
resolves `<ccs>` from the effective installation path, validates that `<ccs>`
and the `.tcl` script exist, launches `<ccs> -script <path>`, and returns the
result. This skill owns the workflow, evidence, and interpretation around that
call.

## When to use

Use this skill when:
- The user wants to run a CCS Tcl script through the CCS executable
  (`ccs` / `ccs.exe`).
- The user wants proof that a discovery, attach, or family-specific sanity
  script actually executed.
- The user wants CCS runtime evidence to isolate whether a failed GDB flow is
  below or above the GDB/session layer.

Do **not** use this skill for:
- Routing the request before the script shape is chosen; use
  `s32debugger-ccs-execution-router`.
- Generating the Tcl script body; use
  `s32debugger-ccs-generate-self-contained-tcl`.

## Quickstart

### 1. Mandatory reference read

Before using this skill, read:
- `references/authoring-procedure.md`
- `references/examples.md`

Do not continue until those files have been reviewed.

### 2. Search the S32Debugger MCP catalog first — mandatory

Before writing any shell command or locating `ccs.exe` manually, search the
S32Debugger MCP actions catalog:

```
s32debugger_search_actions(query="run_ccs_tcl")
```

If `control.run_ccs_tcl` is present (it always is when the S32Debugger MCP
server is active), use it exclusively. Do not fall back to `execute_command`
or any shell-level invocation of `ccs` / `ccs.exe`.

If `control.set_installation_path` has not been called yet in this session,
call it before `control.run_ccs_tcl`:

```
s32debugger_execute_action("control.set_installation_path",
                           {"installation_path": "<root>"})
s32debugger_execute_action("control.run_ccs_tcl",
                           {"tcl_script_path": "<absolute .tcl path>"})
```

### 3. Let the action resolve and validate the executable and script

Do not hardcode or re-derive the CCS path. The `control.run_ccs_tcl` action is
the single source of truth for path resolution: it selects `<ccs>` from the
effective installation path (`ccs.exe` on Windows, `ccs` on Linux) and
validates that both `<ccs>` and the `.tcl` script exist before launching.

```
Provide:  the absolute path to the .tcl script
Ensure:   an installation path is configured (set_installation_path) so the
          action can resolve <ccs>
Ensure:   any output/log directory the script writes to is writable
Consume:  the action's "Error:" string if <ccs> or the script is missing;
          do not reconstruct the CCS path yourself
```

### 3. Triage probe occupancy before CCS startup when probe IP is known

```
Check: reachability -> open telnet session -> run `who` inside it
Rule:  a `ccs` process in the `who` output == busy; no `ccs` process == ready
Rule:  stop immediately if a `ccs` process already owns the probe
```

### 4. Classify the proof command before choosing a capture path

```
Result-returning:       capture with `set x [command]`
Display/print-oriented: capture printed output, not only the Tcl result
Default:                treat `ccs::all_run_mode` as display-oriented
```

If the requested checkpoint is visible in CCS but empty in:
- `set x [command]`, or
- redirected stdout/stderr from the CCS executable's `-script` run

then treat the failure as an output-capture-path mismatch until proven
otherwise.

### 5. Keep the minimum ordered proof sequence inline

Run the script through the `control.run_ccs_tcl` action. The action invokes
the CCS executable with `-script <tcl_script_path>` (`ccs.exe` on Windows,
`ccs` on Linux) and returns a JSON envelope, or an `Error:` string when a
required path is missing:

```
execute_action(action_name="control.run_ccs_tcl",
               params={"tcl_script_path": "<absolute path to .tcl>"})
```

Use this order for the minimum evidence path when running a CCS Tcl script:
1. confirm the installation path is set, then pass the absolute `.tcl` path to
   the action (the action resolves and validates `<ccs>` and the script)
2. if a probe IP is known, do reachability -> telnet `who` -> stop if busy
3. launch the script via `control.run_ccs_tcl`
   unless the user explicitly wants visible CCS
4. verify the CCS process actually starts
5. verify the Tcl script is accepted and begins execution
6. identify the deepest proven checkpoint reached by the script
7. if this workflow started the CCS process, terminate it at request completion unless the user explicitly asks to keep CCS open

### 6. Keep proof thresholds and command policy inline

| Observed result | What it proves | What it does not prove |
| --- | --- | --- |
| CCS executable (`ccs` / `ccs.exe`) opens | process start | script success |
| `config cc` succeeds | probe path is partly alive | chain/init correctness |
| generic `config_chain` + target info succeed | lower-layer visibility | family attach/init or GDB health |
| family core-status succeeds | family chain readiness | ELF/load/run/reset behavior |
| script reaches requested display/status checkpoint | requested CCS layer executed | downstream debugger orchestration |

```
Prefer: `display` for user-visible discovery/status checkpoints
Prefer: headless `-script` proof first when evidence capture is the goal
Rule:   if this workflow starts the CCS executable (`ccs` / `ccs.exe`),
        terminate it at request completion
        unless the user explicitly asks to keep CCS open
Rule:   preserve the mandated checkpoint; change the capture method, not the
        target command sequence
```

## Guardrails

**Mandatory reference rule**
- Read the listed reference files before selecting a branch, generating output,
  or producing the final answer.
- Treat the references as part of the skill, not as optional supplemental
  notes.

**Scope**
- Execute or validate a CCS Tcl script only; do not generate the Tcl body here.
- Distinguish clearly between generic discovery, family-specific sanity,
  deeper attach/init behavior, and full bring-up.
- When interpreting syntax, family support, or init problems, rely on the
  knowledge DB and observed evidence rather than guessing.
- Stop at the first sufficient readable checkpoint unless the user explicitly
  asks for deeper work.
- Distinguish result-returning commands from display-oriented commands before
  deciding how proof will be captured.

**Destructive actions**
- Default to headless proof when the goal is evidence capture.
- If this workflow starts the CCS process (`ccs` / `ccs.exe`), terminate it at
  request completion unless the user explicitly asks to keep CCS open.
- If telnet `who` shows another CCS client on the probe, stop instead of
  retrying CCS startup.

**Refuse-and-escalate**
- If the `control.run_ccs_tcl` action returns an `Error:` string reporting a
  missing installation path, `<ccs>`, or Tcl script, surface that error
  directly and stop; do not reconstruct paths or retry blindly.
- If early probe triage was impossible and a later probe connect fails, require
  telnet `who` before concluding the failure is deeper than occupancy.
- If the script lacks enough logging to prove what happened and editing is
  allowed, prefer adding lightweight verification before execution.
- If family-specific attach/init failure is ambiguous, do not improvise syntax
  fixes; compare against KB-backed patterns first.
- If a checkpoint is visible in CCS but empty in command substitution or
  redirected stdout/stderr, treat that as a capture-path problem first and
  switch to Tcl-side capture of printed output.

**Do**
- Treat this skill as the only documented caller of `control.run_ccs_tcl`; let
  the router and generation skills classify and author, not execute.
- Prefer `s32dbg:<probe-ip>` in new user-facing recommendations.
- Prefer readable `display` output for discovery and status checkpoints when
  supported by the script.
- Separate probe availability, chain configuration, target/core actions, and
  capture method in the final report.

**Do not**
- Re-derive or hardcode the CCS executable path; the action owns resolution and
  validation.
- Claim success because the CCS executable (`ccs` / `ccs.exe`) opened.
- Treat `config cc` success as proof that the whole CCS flow worked.
- Treat successful family-specific core-status output as proof of ELF/load,
  breakpoint, reset-run, or full bring-up behavior.
- Treat every visible CCS command as if it must return the displayed text as a
  Tcl result.
- Drift into help probing, stdin experiments, or lower-level substitutions
  before the mandated readable checkpoint.

### Common interpretation rules

- Visible CCS launch alone proves only UI/process launch, not script success.
- Generic discovery success after failed GDB suggests the lower generic path is
  healthy and the issue likely sits higher.
- Generic discovery success plus family-specific failure isolates the problem
  above generic visibility and below full debugger workflow.
- Family-specific core-status success proves attach readiness, not full
  load/run/reset or breakpoint behavior.
- Empty redirected stdout/stderr do not, by themselves, prove that a display-
  oriented CCS checkpoint failed to run.

### Result contract

The `control.run_ccs_tcl` action returns a JSON envelope on success:
`{"ccs_path", "tcl_script_path", "return_code", "stdout", "stderr"}`, or a
string beginning with `Error:` when the installation path, `<ccs>`, or the
script is missing. Read `return_code` together with `stdout`/`stderr` to
establish the deepest proven checkpoint, and surface any `Error:` string
directly instead of re-deriving paths.

A good execution result should contain:
- launch mode used
- deepest proven layer
- evidence checkpoints reached
- capture method used for the requested proof command
- interpretation of what remains unproven
- next best action

## Validation loop
0. Confirm the required reference files were reviewed before executing the
   workflow or finalizing the answer.
1. Confirm an installation path is configured so the action can resolve
   `<ccs>`, and confirm the absolute `.tcl` path and any writable output/log
   path are available; consume the action's `Error:` string if a path is
   missing rather than re-deriving it.
2. If a probe IP is known, verify the fast path was attempted or explicitly
   unavailable: reachability, telnet `who`, busy vs free.
3. Verify the chosen launch mode matches the goal: headless proof, visible UI,
   or alternate port for a concrete reason.
4. Classify the requested proof command as result-returning or display-oriented.
5. Capture execution evidence by layer: process start, script run, `config cc`,
   `ccs::config_server`, generic or family-specific `ccs::config_chain`, and
   requested target-info/status action.
6. If a display-oriented command is required, verify that the capture path is
   appropriate for printed output rather than relying only on command
   substitution or OS-level redirection.
7. Interpret results without collapsing layers: probe occupancy, probe
   connectivity, generic discovery, family-specific attach, and higher-level
   GDB implications.
8. Verify the first sufficient readable checkpoint was reached without
   exploratory detours.
9. Return launch mode, execution evidence, validation breakdown,
   interpretation, and next best action.

## Out of scope

- Choosing the CCS workflow before routing/classification.
- Authoring or rewriting the Tcl script body from scratch.
- Treating UI launch as execution proof.
- Guessing family-specific init or syntax corrections without KB evidence.

## See Also

- `references/authoring-procedure.md` - execution layering, command choice,
  output-capture procedure, and interpretation guidance.
- `references/examples.md` - common outcomes, capture-path patterns,
  anti-patterns, and reporting cues.
- Related skills: `s32debugger-ccs-execution-router`,
  `s32debugger-ccs-generate-self-contained-tcl`,
  `s32debugger-error-resolution`
