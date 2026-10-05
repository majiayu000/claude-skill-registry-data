---
name: s32debugger-error-resolution
description: >
  Diagnose standalone S32Debugger startup, bridge, probe, CCS, symbol, and
  live-session failures and turn vague debugger problems into a concrete
  recovery plan. Use this whenever a startup/connect/load/breakpoint flow
  fails, when the user pastes an error snippet or transcript, when an
  interactive session opens but does not behave correctly, or even when the
  user only says "it doesn't work" and the failing workflow stage still needs
  to be identified. Distinguish lower-layer probe and target-visibility issues
  from higher-layer GDB/session/configuration issues, and use CCS fallback when
  a failed GDB flow is ambiguous and the lower layers remain unproven.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32debugger
  depends_on: '[s32debugger-ccs-execution-router, s32debugger-ccs-run-tcl-script]'
  tags: '[s32debugger, troubleshooting, diagnostics]'
---

# S32Debugger Error Resolution

Diagnose standalone S32Debugger failures by classifying the failing stage,
separating shallow infrastructure problems from deeper debugger behavior, and
turning vague symptoms into a concrete recovery plan. This skill is for
structured troubleshooting, not blind retry advice.

## When to use

Use this skill when:
- A standalone S32Debugger startup, connect, load, bridge, breakpoint, or
  live-session flow fails.
- The user pastes an error snippet, transcript, or vague complaint such as
  "it doesn't work".
- A failed GDB flow needs to be separated from lower-layer probe or target
  visibility issues, possibly using CCS sanity fallback.
- A supposedly simple sanity-check, target-info, or core-state request was
  misrouted into GDB even though no interactive session was already active.

Do **not** use this skill for:
- Declaring a session healthy before the key validation point is reached.
- Treating source-path warnings as equivalent to connection or startup failure.

## Quickstart

### 1. Mandatory reference read

Before using this skill, read:
- `references/authoring-procedure.md`
- `references/examples.md`

Do not continue until those files have been reviewed.

### 2. Classify the failure by workflow stage first

```
Stages: config | GTA/local service | CCS/probe | bridge | target state |
        ELF/symbols | lower-layer ambiguity after failed GDB flow
Goal:   find the shallowest unproven layer before proposing retries
```

### 3. Keep the failure-layer model inline

| Layer | Meaning | Next proof step if unproven |
| --- | --- | --- |
| 0 | probe reachability / occupancy | reachability, telnet `who` |
| 1 | generic CCS / DAP visibility | generic CCS discovery |
| 2 | family-specific attach/core-status sanity | family sanity script |
| 3 | family-specific attach/init readiness beyond status | deeper family attach/init check |
| 4 | GDB bridge/session orchestration | bridge status, loader config, session diagnostics |
| 5 | ELF / symbol / breakpoint / run-control | `file`/`symbol-file`, load, breakpoints, PC/BT |

### 4. Apply the CCS-first observational rule when appropriate

Apply the **CCS-first observational rule**.
See `references/authoring-procedure.md`.

### 5. Keep blocking-vs-warning interpretation explicit

```
Blocking: connect/startup/bridge/load failures, missing symbols when required
Non-blocking: source lookup warnings after a correct symbolic stop
Rule: use the shallowest unproven layer to choose the next diagnostic action
```

### 6. Classify output-capture mismatches before changing target assumptions

If a user reports that a CCS command visibly prints useful output, but the
agent sees:
- an empty Tcl result from `set x [command]`, and
- empty redirected stdout/stderr from the CCS executable's `-script` run,

then treat this as a likely capture-path mismatch until proven otherwise.

## Guardrails

**Mandatory reference rule**
- Read the listed reference files before selecting a branch, generating output,
  or producing the final answer.
- Treat the references as part of the skill, not as optional supplemental
  notes.

**Scope**
- Diagnose standalone S32Debugger failures involving config generation, GTA,
  GDB, probe connectivity, bridge-backed interaction, ELF/symbol handling,
  breakpoint validation, and ambiguity between GDB failures and lower layers.
- Classify by workflow stage first, then by failure category and recovery step.
- Distinguish lower-layer probe and generic target visibility from higher-layer
  GDB/session/configuration behavior.
- Distinguish target/probe failures from output-capture-path failures when the
  requested CCS evidence is display-oriented.

**Destructive actions**
- Default to diagnosis and evidence-based next checks, not blind retries.
- Do not declare success before connect, bridge validation, or stop-state
  validation has actually been reached.
- Do not recommend repeated GDB retries when probe availability or generic
  target visibility is still unproven.
- Do not recommend starting a GDB live-session path when the
  **CCS-first observational rule** applies.

**Refuse-and-escalate**
- If the exact failing stage is unclear, ask for the precise error text or the
  last step that failed.
- If the **CCS-first observational rule** applies, route to CCS Layers 0-2
  before discussing GDB live-session setup.
- If a GDB attach/connect/startup failure is ambiguous, prefer probe triage and
  CCS generic discovery before deeper GDB/session speculation.
- If generic CCS discovery succeeds but family-chain readiness is still
  unproven, escalate to a family-specific attach/core-status sanity test before
  assuming full bring-up is needed.
- If the problem is clearly a path, ELF, symbol, or output-capture mismatch,
  keep the diagnosis at that layer instead of escalating to CCS init changes.

**Do**
- Identify the shallowest unproven layer.
- Cite observed evidence for the proposed cause category.
- Say what success should look like after retry.
- Apply the **CCS-first observational rule** before recommending a GDB path.
- Check whether a CCS proof command is result-returning or display-oriented
  before choosing a capture mechanism.

**Do not**
- Mix symbol/source warnings with connection/startup failures.
- Treat a successful family-specific core-status sanity check as proof that
  load/run/reset or full bring-up is already validated.
- Guess root causes without linking them to evidence.
- Prepare GDB live-session plumbing before proving whether a CCS quick check is
  sufficient.
- Diagnose a visible-in-CCS but empty-in-capture symptom as a family-init
  problem before checking whether the command is display-oriented.

### Core fallback sequence

If a GDB attach/connect/startup failure is ambiguous and lower layers are not
proven, use this order:
1. probe reachability check
2. telnet `who`
3. minimal CCS generic discovery
4. family-specific attach/core-status sanity only if generic discovery already
   succeeded and the next question is chain readiness
5. only then escalate upward to GDB bridge/session, loader config, or symbol
   handling hypotheses if the lower layers are already proven

If the **CCS-first observational rule** applies, start at steps 1-4 directly;
do not treat CCS as merely a post-GDB fallback.

### Interpretation rules

- CCS executable (`ccs` / `ccs.exe`) or probe visibility success does **not** prove GDB/session health.
- Generic CCS discovery success proves lower-layer visibility, not family init.
- Family-specific core-status success proves chain readiness, not ELF/load/run.
- A correct symbolic stop with source-path warning is often non-blocking.
- A command that is visible in CCS but empty via command substitution or
  redirected stdout/stderr may indicate a capture-path mismatch rather than a
  target failure.

### Result contract

A good troubleshooting result should contain:
- failure stage
- probable category
- evidence used
- next proof step
- recommended retry or fix sequence
- explicit success criterion after retry

## Validation loop
0. Confirm the required reference files were reviewed before executing the
   workflow or finalizing the answer.
1. Confirm the failure is classified by workflow stage: config, GTA/local
   service, CCS/probe, bridge, target execution state, ELF/symbols, or
   lower-layer ambiguity after failed GDB flow.
2. Verify the evidence cited actually supports the probable failure category.
3. Verify blocking vs non-blocking status is explicit where relevant.
4. If the failure is ambiguous, identify the shallowest unproven layer and the
   next diagnostic action intended to prove it.
5. Verify the **CCS-first observational rule** was applied correctly.
6. If visible CCS output is part of the complaint, verify whether the command is
   result-returning or display-oriented before changing target assumptions.
7. Verify the proposed fix or retry sequence is concrete and ordered.
8. Return the failure stage, probable category, evidence, likely causes, exact
   next checks, recommended recovery sequence, and what success should look
   like after retry.

## Out of scope

- Declaring a session ready without bridge validation, connect success, or
  stop-state verification.
- Blindly retrying GDB when lower layers remain unproven.
- Treating a successful generic CCS discovery run as proof that all later
  family-specific or GDB steps must also work.
- Treating non-blocking source warnings as infrastructure failures.
- Violating the **CCS-first observational rule**.

## See Also

- `references/authoring-procedure.md` - failure-layer model, fallback logic,
  capture-path mismatch handling, and common failure categories.
- `references/examples.md` - quick triage examples, interpretation matrix, and
  anti-patterns.
- Related skills: `s32debugger-ccs-execution-router`,
  `s32debugger-ccs-generate-self-contained-tcl`,
  `s32debugger-ccs-run-tcl-script`
