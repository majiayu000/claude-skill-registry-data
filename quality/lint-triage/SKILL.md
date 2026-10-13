---
name: lint-triage
description: >
  Run RTL lint / methodology checks and triage each violation into a real fix vs
  a justified, documented waiver. Use when the user says "lint my RTL", "code
  quality", "review my RTL", "check my Verilog/VHDL", "any latches / unintended
  latches", "clean up warnings before synthesis", "is my design lint-clean", or
  asks for a code-quality / methodology report on an FPGA design.
  Requires the SynthPilot MCP server (Xilinx Vivado running with the Tcl server
  connected on TCP:9999). Methodology-stage checks additionally require an open
  synthesized design (open_synthesized_design / open_implemented_design).
---

# Lint Triage — RTL Lint & Methodology Violation Triage

A playbook for driving SynthPilot's lint/methodology tools to find real RTL
problems, then sorting every violation into one of three buckets: **fix it**,
**waive it (with a stated justification)**, or **ask the human**. The deliverable
is a triaged report, not a green number. A lint run that is "clean" because real
violations were silenced is a failure of this skill.

This skill follows one discipline above all: **measure → classify → fix the
smallest safe thing → re-measure**. It never invents a tool, never downgrades a
severity to hide a problem, and never claims "lint clean" without fresh tool
output proving it on the current source.

---

## When to use

- User asks to "lint my RTL", "review my RTL", "check code quality", "find
  unintended latches", "clean up warnings", or "is this design lint-clean".
- Before synthesis sign-off, before a design review, or before handing RTL to a
  teammate, to catch latches, incomplete sensitivity lists, width mismatches,
  unconnected ports, blocking/non-blocking misuse, and methodology violations.
- After an RTL edit, to confirm a class of violations is actually gone (not just
  moved or masked).
- To produce a defensible waiver list — each waiver tied to an explicit reason —
  for items that are intentional and safe.

## When NOT to use

- **Timing closure** (WNS/TNS negative, failing setup/hold). Lint is not timing.
  Use the timing-closure skill. `check_async_reset` here surfaces *reset-path
  methodology* issues, not slack.
- **Pure CDC sign-off** (metastability, gray-coding, handshake correctness).
  `check_cdc_lint` / `report_cdc` are a first screen only; deep CDC analysis is a
  separate playbook. Lint-triage flags CDC violations and hands them off.
- **Functional verification** (does the logic compute the right answer). That is
  simulation (`sim_*`), not lint. Lint cannot tell you a correct-looking design
  is functionally wrong.
- **DRC / route sign-off** (`report_drc` on a placed/routed design). Different
  stage, different tool.
- No project is open / Vivado is not reachable. Resolve Prerequisites first.

---

## Prerequisites (verify first)

Do not run any check until these pass. If one fails, stop and report it — do not
guess.

1. **MCP / Vivado reachable.** Call `test_connection`. If it fails, the Tcl
   server inside Vivado is not connected on TCP:9999 — report and stop.
2. **A project is open with sources.** Call `get_project_info` and
   `list_source_files`. If no project or no RTL sources, stop and ask the user to
   open the project / point at the files.
3. **Top module is set** (needed for elaboration-stage checks). If
   `get_project_info` shows no top, call `set_top_module` only with a name the
   user gave or that is unambiguous from `list_source_files`; otherwise ask.
4. **Know which stage you can reach.** Syntax-stage checks need only sources.
   Methodology-stage checks (`run_full_lint_check`, `report_methodology`,
   `get_lint_violations`, `check_latches`, `check_fsm`, `check_coding_style`,
   `check_cdc_lint`, `check_simulation_mismatch`) require an **open synthesized
   design**. Plan to reach that stage in Step 3 — do not call those tools before
   the design is open or they will error.

---

## Methodology (numbered, real tool calls)

Work the stages in order. Each stage is cheaper/earlier than the next; do not
skip ahead, because a syntax error makes every later check meaningless.

### Step 1 — Establish the file baseline

- `list_source_files` and (if useful) `check_compile_order`. A wrong compile
  order produces phantom "undefined module" / black-box noise downstream;
  fix ordering before trusting any later result.
- Record the file set and top module. This is the scope every later claim is
  bounded to ("lint-clean" means *these files, this top*, nothing more).

### Step 2 — Syntax-stage checks (no synthesis required)

Run the checks that work directly on source. These are fast and catch the errors
that would otherwise abort synthesis:

- `check_syntax` (all sources) — must be clean before anything else is trustworthy.
- `check_compile_order` — ordering / include problems.
- `check_black_box` — undefined modules (missing files, typo'd module names, or a
  genuinely intended black box / external IP).
- `check_port_width_mismatch` — connection width mismatches at instantiation.
- `check_unconnected_ports` — dangling/unconnected ports.

If `check_syntax` reports errors, **STOP the lint flow here**. Classify and
surface the syntax errors (Step 5 table) and do not pretend later stages are
clean — you cannot run them on broken source.

### Step 3 — Reach a synthesized design for methodology checks

Most high-value RTL lint (latches, FSM health, coding style, CDC, sim/synth
mismatch) requires an elaborated/synthesized netlist.

- If a synthesized design is not already open, run synthesis. For anything beyond
  a tiny design prefer the async pattern: `run_synthesis_async`, then poll
  `get_run_status` until complete (multi-minute operations must not block).
- Then `open_synthesized_design`. (An already-open `open_implemented_design` also
  satisfies the prerequisite.)
- Also pull `get_synthesis_warnings` — synthesis warnings frequently *are* the
  lint findings (inferred latch, truncation, dropped logic) and corroborate the
  dedicated checks.

If synthesis fails, the failure itself is the top-priority violation: capture it,
classify it (Step 5), and stop — there is nothing to lint on a netlist that
doesn't exist.

### Step 4 — Methodology / RTL-quality checks (on the open synth design)

Run the methodology suite and the targeted RTL checks:

- `run_full_lint_check` — full syntax + methodology pass; the broad sweep.
- `report_methodology` then `get_lint_violations` — the structured violation list
  you will triage (each item has a check name / ID).
- `check_latches` — **inferred latches**, the single most important RTL lint
  signal; an unintended latch is almost always a real bug.
- `check_fsm` — FSM encoding / unreachable-state / dead-state health.
- `check_coding_style` — synthesis-relevant coding issues.
- `check_cdc_lint` — first-screen clock-domain-crossing flags (hand deep CDC off).
- `check_simulation_mismatch` — constructs that simulate differently than they
  synthesize (the worst class: it works in sim, fails in hardware).

For any violation you do not understand, pull detail with
`report_lint_violation_detail(violation_id=...)` before deciding what to do with
it. Never triage blind.

### Step 5 — Triage every violation

For **each** violation, read its detail and place it in exactly one bucket using
the table below. Do not batch-waive. Do not batch-ignore. One verdict per item,
each with a one-line reason.

### Step 6 — Apply the smallest safe change, one class at a time

- **Fixes are recommended, not silently applied.** Latches, width mismatches, and
  sim/synth mismatches are RTL bugs — describe the exact edit (which signal, which
  always/process block, default assignment vs full case, blocking vs non-blocking)
  and let the human approve before you touch source with `update_file` /
  `replace_in_file`. Use `read_file_lines` to ground the recommendation in the
  real code.
- **Waivers require a stated assumption.** Only after the item is confirmed
  intentional do you call
  `waive_lint_violation(check_name=..., reason="<why this is safe and intended>", objects=...)`.
  The reason string is mandatory and must be a real justification, not "waived".
- Change **one class per iteration** (e.g. fix latches, OR waive a reviewed style
  rule — not both), so the re-measure attributes cause to effect.

### Step 7 — Re-measure (close the loop)

After each change class, re-run the relevant check on the **current** source/
netlist (re-synthesize if RTL changed) and diff the violation list. A fix is only
"done" when the violation it targeted is gone from fresh tool output and no new
violation appeared. Record before/after counts.

---

## Classification / decision table

Map each violation to a cause and the **smallest safe** response. The default
verdict is **FIX**; **WAIVE** is allowed only with an explicit, true
justification; **ASK** when intent is unknown.

| Symptom / check                         | Likely cause                                              | Smallest safe response                                                                 | Default verdict |
|-----------------------------------------|-----------------------------------------------------------|----------------------------------------------------------------------------------------|-----------------|
| `check_latches` finds inferred latch    | Incomplete `if`/`case` or missing default in comb logic    | Recommend full assignment (default value / `else` / `default:`); confirm with `read_file_lines` | **FIX (RTL)**   |
| `check_port_width_mismatch`             | Instantiation port width ≠ signal width                    | Recommend resizing the signal/port; never widen blindly — verify intent                | **FIX (RTL)** / ASK |
| `check_unconnected_ports`               | Dangling port                                              | If functionally required → FIX (connect); if intentionally unused → tie-off/`objects` waiver with reason | FIX / WAIVE     |
| `check_black_box`                        | Missing file, typo'd name, OR intended external IP/stub    | If missing → add file / fix `check_compile_order`; if intended → WAIVE with reason      | FIX / WAIVE     |
| `check_simulation_mismatch`              | Init values, `#delay`, sensitivity-list, X-pessimism gaps  | RTL fix — these are silent hardware bugs                                                | **FIX (RTL)**   |
| `check_fsm` unreachable/dead state       | Unhandled case / wrong reset / dead code                   | Recommend handling or removing the state; do not waive a reachable hole                 | **FIX (RTL)**   |
| `check_coding_style` violation           | Blocking/non-blocking misuse, mixed assigns, style rule    | If functional risk → FIX; if cosmetic & team-approved → WAIVE with reason               | FIX / WAIVE     |
| `check_cdc_lint` flag                    | Unsynchronized crossing / missing handshake                | Hand to CDC sign-off; **never** waive a real crossing to clear lint                     | **ASK / FIX**   |
| `report_methodology` / `get_lint_violations` generic item | Vivado methodology rule (e.g. SYNTH-/TIMING- family) | Read `report_lint_violation_detail`; fix or justify per the item                        | depends → triage |
| Rule is a **known false positive** for this design | Tool over-reports a safe pattern                  | WAIVE the specific `check_name`/`objects` with a reason naming why it's safe            | **WAIVE**       |
| Intent genuinely unknown                 | Can't tell if the construct is deliberate                  | Present the finding + options; hand back to human                                       | **ASK**         |

---

## Iteration loop & STOP conditions

```
LOOP:
  1. Run the relevant check(s)            (Step 2 / Step 4)
  2. get_lint_violations  -> list
  3. For each item: report_lint_violation_detail -> classify (table)
  4. Apply ONE change class:
        - FIX  (recommend RTL edit, get approval, then update_file/replace_in_file)
        - WAIVE (waive_lint_violation with a real reason)   [reviewed items only]
  5. Re-synthesize if RTL changed; re-run the check          (Step 7)
  6. Diff before/after violation list
  -> repeat
```

**STOP the loop when any of these is true:**

- **Clean:** the targeted check returns zero violations on **fresh** output, and
  every remaining item is an explicit, justified waiver in `list_waivers`. This is
  the only "lint clean" you may claim — and only with the fresh output in hand.
- **All remaining items need human judgment** (ASK bucket): present options +
  trade-offs and hand back. Do not thrash trying to auto-resolve intent.
- **A fix would require unapproved RTL surgery** beyond the smallest safe change
  (architectural change, retiming logic, restructuring an FSM): surface the
  recommendation and stop; do not silently apply it.
- **No progress / oscillation:** the same violation count persists or a "fix"
  spawns new violations after two iterations. Stop, report the conflict, hand back.
- **An upstream blocker reappears** (syntax error, synthesis failure): drop back
  to that stage; the lower stage owns the fix.

---

## Safety rails (do not violate)

- **No fake-pass.** Never make the number green by hiding a real problem. Do
  **not** call `set_lint_severity` to downgrade a check, `disable_lint_rule`, or
  `waive_lint_violation` on an item that could be a genuine bug just to clear it.
  A latch, width mismatch, CDC crossing, or sim/synth mismatch is presumed real
  until proven intentional.
- **Waivers need a stated, true justification.** Every `waive_lint_violation`
  call carries a `reason` that explains *why the construct is safe and intended* —
  scoped with `objects` to the specific cell/net where possible, never a blanket
  waiver of an entire check. If you cannot articulate the justification, you may
  not waive it; ask the user.
- **Smallest safe change first.** Prefer connecting a port, fixing compile order,
  or scoping a waiver over rewriting RTL. Constraint/config/style fixes before
  source edits; source edits before architectural changes.
- **Recommend RTL edits; don't silently apply them.** Show the exact change
  (file, line range from `read_file_lines`, before/after) and get approval before
  `update_file` / `replace_in_file`. Latch and mismatch fixes especially must be
  reviewed.
- **Evidence before claims.** "Lint clean" / "no latches" / "violation fixed"
  REQUIRES fresh output from the relevant tool **after** the change, on the
  current source/netlist. Never infer it from "I made the edit." If RTL changed,
  re-synthesize before re-checking — stale netlist results are not evidence.
- **Stay in scope.** Lint-triage flags timing/CDC/DRC items and hands them to the
  right skill. It does not pretend a CDC waiver or a severity downgrade closes a
  timing/CDC issue.
- **Real tools only.** Use only the SynthPilot tool names referenced here. If a
  needed capability is missing, say so plainly rather than inventing a tool.

---

## Output

Deliver a triage report, not a verdict-by-assertion:

1. **Scope** — files (`list_source_files`) + top module + the stage reached
   (syntax-only vs synthesized). Every claim is bounded to this.
2. **Violation summary** — counts by severity/check, before vs after, from
   `get_lint_violations` / `get_synthesis_warnings` (fresh output, quoted/cited).
3. **Triage table** — one row per violation: `check / ID | location | cause |
   verdict (FIX / WAIVE / ASK) | action taken or recommended`.
4. **Fixes applied** — only those the user approved; show before/after snippet
   (`read_file_lines`) and the re-measured result proving the violation cleared.
5. **Waivers** — the current `list_waivers` output, each with its justification.
   Flag any waiver whose reason is weak so the human can revisit it.
6. **Open items / hand-offs** — ASK-bucket items with options + trade-offs, and
   anything routed to timing / CDC / DRC / simulation skills.
7. **Honest status line** — e.g. "Lint clean on <files>/<top> at synthesis stage:
   0 unwaived violations, N justified waivers (fresh `get_lint_violations` output
   attached)." Never state "clean" without that fresh evidence; if blocked, say
   exactly what blocks it and what decision you need from the user.
