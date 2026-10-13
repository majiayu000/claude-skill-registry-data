---
name: coverage-closure
description: >
  Measure RTL simulation code coverage (statement / branch / condition) and
  iteratively close it toward an explicit target by adding targeted testbench
  stimulus. Use when the user asks "what is my code coverage", "how much is
  covered", "coverage closure", "improve coverage to N%", "which lines aren't
  tested", "are there untested branches", or wants a sign-off-grade coverage
  report before tape-out / merge. Requires the SynthPilot MCP server with
  Vivado + the Tcl server running (xsim/xelab/xcrg, validated on Vivado 2024.2).
  PRO-tier tool sim_get_coverage. This is a methodology playbook, not code: it
  tells the AI which real SynthPilot tools to call, in what order, and how to
  decide what to do with the numbers.
---

# Coverage Closure (Simulation Code Coverage)

Measure statement / branch / condition coverage from an xsim run, find the
exact `file:line:type` that the testbench never exercised, and close the gap by
**adding stimulus** — not by deleting code, lowering the bar, or pragma-ing the
problem away. Coverage is a *necessary* signoff signal, not a *sufficient* one:
100% code coverage with a weak testbench is still a weak testbench. This skill
makes the number honest.

## When to use

- "What's my code coverage?" / "How much of the design is covered?"
- "Get coverage to 90% statement / 85% branch before I merge."
- "Which lines / branches are never hit by the testbench?"
- You need a downloadable coverage report for a code review or tape-out gate.
- A regression passes but you suspect it isn't exercising the whole design.

## When NOT to use

- **FSM state/transition coverage** — xsim code coverage has **no FSM
  dimension** (verified). Use SVA `cover property` / directed tests; that is out
  of scope for this skill. Say so explicitly rather than faking an FSM number.
- **Functional / assertion coverage** (covergroups, SVA cover) — `sim_get_coverage`
  reports *code* coverage only. Do not present code coverage as functional coverage.
- **Toggle coverage as a gate** — toggle is reported (percentage only) but is
  routinely dragged to single digits by reserved/constant-zero bits. Do not gate on it.
- "Is timing met / CDC clean / lint clean?" — wrong skill (timing-closure,
  cdc-analysis, lint-cleanup). Coverage says nothing about those.
- The user wants you to *delete untested RTL* to raise the percentage — refuse;
  see Safety rails.

## Prerequisites (verify first)

Run these before measuring. Do not assume state.

1. `test_connection` — confirm the Tcl server is live inside Vivado. If it
   fails, stop and tell the user to start Vivado + the Tcl server.
2. `get_license_status` — `sim_get_coverage` is a **PRO-tier** tool. If FREE,
   stop and report that coverage requires a Pro license.
3. `get_project_info` — confirm a project is open (or `open_project` first).
4. `list_simulation_files` — confirm the **testbench and DUT are in the sim
   fileset**. Coverage is only as good as the TB that drives it.
5. `set_simulation_top("<tb_top>")` — **mandatory.** `sim_compile` resolves the
   compile order relative to the sim-fileset top. If you skip this, xelab fails
   with `Cannot find design unit work.<tb>`. (Pitfall #1, verified.)

Only after all five succeed do you instrument and run.

## Methodology

One change-class per iteration so cause→effect stays attributable. Always
*measure with a tool* before and after acting.

### 1. Establish the target (ask if unstated)

Coverage closure is meaningless without a target. If the user gave none, ask, or
propose conventional pre-signoff gates and confirm:
- statement ≥ 90%, branch ≥ 85%, condition ≥ 80% (typical).
Record which **metrics** gate and which **modules** are in scope (third-party /
generated IP, `glbl`, and verification-only modules are normally excluded).

### 2. Instrument the compile

```
set_simulation_top("<tb_top>")                                 # step 5 above, re-assert
sim_compile(top_module="<tb_top>", coverage_types="sbc")       # s=stmt b=branch c=cond
```
- Use `"sbc"` for gating metrics. Add `t` only if the user explicitly wants
  toggle visibility — never to gate.
- If compile fails, read `sim_get_compile_log(stage="compile")`, fix the RTL/TB
  or fileset/order issue, and recompile. A coverage number from a partial
  compile is invalid.

### 3. Run the simulation (coverage flushes automatically)

- Short TB (< ~30 s expected): `sim_run()`.
- Long TB: `sim_run_async()` then poll `sim_get_sim_status()` until `COMPLETED`.
  Do not fetch coverage while it is still `RUNNING`.

No special flag is needed to flush coverage — the normal run/quit path records it
(verified). **Confirm the run actually completed and the TB passed** before
trusting coverage; a TB that aborts early under-counts coverage and the number is
a lie. If the TB has failures, fix those first — coverage of a broken run is meaningless.

### 4. Measure — get structured coverage

```
sim_get_coverage(detail_level=2, uncovered_limit=200)
```
Returns JSON:
- `summary` — global statement/branch/condition (and toggle if compiled).
- `per_module` — per source module, `{covered, total, pct}` for each metric.
  Counts are a **cross-instance union**: a line counts as hit if *any*
  instance hit it (verified). Parameterized modules appear as `name(PARAM=val)`.
- `uncovered` — `[{file, line, type, context}]`: the exact lines/branches/
  conditions never exercised. This is your worklist.
- `report_path` — `dashboard.html` for human review (download for PR/signoff).

Report the baseline before touching anything (Show your work).

### 5. Classify each gap before writing any stimulus

Read each `uncovered` entry against the source (`read_file_lines`) and classify
it using the table below. **Do not write a single line of TB code until every
in-scope gap is classified.** The fix is determined by the class, not by the
percentage.

### 6. Close the gap — smallest safe action first

In priority order:
1. **Reachable-but-untested** → add directed stimulus to the **testbench**
   (recommend the edit; show the new case to the user before/while applying).
2. **Reachable-only-from-another-config** → add a parameterization / second TB
   instance that exercises that branch.
3. **Genuinely unreachable defensive code / reserved bits** → do **not** fake it.
   xsim ignores inline `(* coverage_off *)` and `// xilinx coverage off` (both
   verified to have zero effect), so you cannot pragma it away. Surface it as a
   **documented exclusion** for the user's CI exclusion list (file:line:type),
   stated as an explicit assumption — never silently drop it.

Apply **one class of change per iteration** (e.g., "added reset-deassert case"),
then re-measure, so you can attribute the delta.

### 7. Re-measure (mandatory after every change)

Re-run steps 2→4 (`sim_compile` → run → `sim_get_coverage`). A coverage claim is
only valid against **fresh** `sim_get_coverage` output from the current TB+RTL.
Never report a projected or inferred percentage.

## Classification table (uncovered → cause → safe action)

| `uncovered` symptom | Likely cause | Smallest safe action |
|---|---|---|
| Statement in `else`/error branch never hit | TB never drives the error/edge input | Add directed TB case that forces that input; re-measure |
| Branch hit one direction only (e.g. `if` taken, `else` not) | Missing complementary stimulus | Drive both polarities of the condition in the TB |
| Condition term never both-T/both-F | Sub-expression of a compound `&&`/`\|\|` never toggled | Add stimulus toggling that specific operand |
| Reset/de-assert path uncovered | TB asserts reset but never exercises de-assert sequence | Extend TB reset sequence |
| Whole module 0% | DUT instance not driven, or TB top wrong | Re-check `set_simulation_top`, fileset, and that the module is instantiated/driven |
| `MISSING ELSE` with `line: null` | `if` with no `else` (synthetic branch) | Normal; add `else`-direction stimulus or document as N/A |
| Reserved/constant-zero bits, dead defensive default | Genuinely unreachable | Document as exclusion for the user's CI list — **do not pragma, do not gate**; ask before excluding if reachability is uncertain |
| `glbl` / generated IP / verification module uncovered | Out-of-scope module | Exclude from scope (state it); do not chase |
| Toggle very low | Reserved/idle bits | Expected; do not gate toggle |

## Loop + STOP conditions

```
measure (sim_get_coverage)
  └─ classify every in-scope uncovered entry
       └─ pick ONE class of reachable gap
            └─ add TB stimulus (recommend / apply)
                 └─ re-compile + re-run + re-measure
                      └─ compare before/after → repeat
```

**STOP and hand back to the human when:**
- All gating metrics meet the target on **fresh** `sim_get_coverage` output — done.
- Remaining uncovered items are all classified **unreachable / out-of-scope**, and
  meeting the literal target would require deleting code or excluding reachable
  paths — present the exclusion list + costs; do not force the number green.
- Two consecutive iterations add stimulus but the gating metric does not move
  (thrash) — stop, present the residual gaps and options, ask for direction.
- A gap can only be closed by an RTL change (genuinely dead/unreachable logic
  that the user may want removed) — recommend it; do not silently edit RTL.
- The TB itself is failing/aborting — coverage is invalid; escalate the TB bug
  before any coverage work.

Never loop silently. Each iteration reports before→after numbers and what changed.

## Safety rails (do not violate)

- **No fake-pass.** Never raise the percentage by deleting RTL, narrowing scope
  to dodge a real path, lowering the agreed target, or excluding a *reachable*
  line/branch. Exclusions are only for provably-unreachable code, stated as an
  explicit assumption, and confirmed with the user when reachability is uncertain.
- **Pragmas don't work here — don't pretend they do.** xsim ignores
  `(* coverage_off *)` and `// xilinx coverage off` (verified, zero effect). Do
  not insert them to "handle" reserved bits; that is a silent fake-pass. Exclude
  in the CI list instead.
- **Evidence before claims.** "Coverage met" / "target reached" REQUIRES fresh
  `sim_get_coverage` output from the current TB+RTL on a **passing** run. Never
  infer, never reuse a stale number, never project.
- **Coverage ≠ correctness.** High code coverage does not mean the design is
  correct, timing-clean, or functionally verified. State this when reporting.
- **Smallest safe change first.** Close gaps by adding **testbench stimulus**
  before touching DUT RTL. Recommend RTL/architectural edits; do not apply them
  silently.
- **One change-class per iteration** so each delta is attributable.
- **Don't gate toggle.** Report it if asked; never let it block.
- **FSM / functional coverage are out of scope** — say so; do not substitute code
  coverage for them.
- **Real tools only.** Use exactly: `test_connection`, `get_license_status`,
  `get_project_info`, `open_project`, `list_simulation_files`,
  `set_simulation_top`, `sim_compile`, `sim_run`, `sim_run_async`,
  `sim_get_sim_status`, `sim_get_compile_log`, `sim_get_coverage`,
  `read_file_lines`, `update_file`/`replace_in_file` (TB edits). If a needed
  capability (e.g. FSM coverage) doesn't exist, say so — never invent a tool.

## Output

Report, in this shape:

1. **Scope & target** — gating metrics + thresholds; modules in/out of scope.
2. **Baseline (with evidence)** — `summary` percentages + per-metric `covered/total`
   from the first `sim_get_coverage`; note the run passed.
3. **Gap analysis** — table of in-scope `uncovered` entries: `file:line:type` →
   classification (reachable / config-only / unreachable / out-of-scope) → action.
4. **Iterations** — for each: what stimulus was added (one class), and the
   before→after delta on the gating metric (fresh tool output each time).
5. **Final state (with evidence)** — final `sim_get_coverage` `summary` +
   per-module `covered/total`; explicit PASS/FAIL vs each target. Link
   `report_path` (`dashboard.html`) for human review.
6. **Documented exclusions** — any unreachable items proposed for the CI
   exclusion list (`file:line:type` + one-line justification), flagged as
   assumptions for the user to ratify.
7. **Caveats** — restate: code coverage ≠ functional correctness; no FSM
   coverage; toggle not gated. Surface any residual gaps and the options/costs if
   the literal target wasn't honestly reachable.
