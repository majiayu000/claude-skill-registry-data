---
name: replay-verify
description: "Prove the simulation is deterministic by re-running a seeded scenario and diffing its order log and world-state hash against itself and against a stored golden baseline. Produces a PASS/FAIL reproducibility gate. Run before merging sim/controller changes and before a release gate. A FAIL means a replay diverged — the build is not reproducible."
argument-hint: "[scenario-name | all | --record | --bisect]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Write, AskUserQuestion, Task
model: sonnet
agent: determinism-engineer
---

# Replay Verify

This skill is the **reproducibility gate**. Project Aegis guarantees that a given
`(scenario, seed)` produces the identical order log and end-state on every run
(req 03, req 04, delegation spec §2.5). `/determinism-audit` finds *causes* of
non-determinism by static scan; this skill proves the *result* by actually
running the sim and comparing outputs.

The rule is simple: **a build whose replay diverges is not reproducible, and a
non-reproducible sim is broken — even if every unit test passes.**

**Output:** `production/determinism/replay-[date].md`

---

## Parse Arguments

- `scenario-name` — verify a single named scenario fixture
- `all` (default) — verify every scenario fixture found
- `--record` — record/refresh the golden baseline for the target scenario(s)
  instead of comparing (deliberate baseline regeneration — see Phase 6)
- `--bisect` — on a detected divergence, bisect the order log to the first
  diverging tick and attribute it (diagnostic mode)

Arguments combine: `/replay-verify convoy-intercept --bisect`.

---

## Phase 1: Detect the Sim and Replay Harness

1. **Solution check**: confirm `ProjectAegis.sln` exists. The sim runs via
   `dotnet`, not the Unity editor — the deterministic core is plain .NET.

2. **Replay fixtures**: glob for golden baselines, in priority order:
   - `tests/replay/**/*.golden.json` (or `.baseline`)
   - `tests/replay/fixtures/`
   - `src/**/*Tests/**/Replay*`

   If none exist:
   > "No replay baselines found under `tests/replay/`. Run
   > `/replay-verify [scenario] --record` to create the first golden baseline,
   > or scaffold the replay harness first." Then stop unless `--record` was passed.

3. **Replay runner**: locate the entry point that runs a seeded scenario headless
   and emits an order log + state hash. Candidates:
   - a test in `*.Tests` tagged `Replay`/`Determinism`
   - the demo (`src/ProjectAegis.Delegation.Demo`) run with a `--seed` / `--scenario` flag
   - a dedicated replay CLI

   If no runner exists:
   > "No replay runner found. The sim needs a headless entry point that takes
   > `(scenario, seed)` and emits a deterministic order log + end-state hash.
   > This is a prerequisite — see `determinism-engineer`. Recording the harness
   > is out of scope for this gate run." Then stop.

Report: "Sim: .NET via ProjectAegis.sln. Baselines: [N found / none]. Runner:
[path / not found]."

---

## Phase 2: Run the Replay (twice + against golden)

For each in-scope scenario, run the sim **three** ways to separate two failure
modes — *intra-run* non-determinism vs. *baseline drift*:

```bash
# Run A and Run B: same scenario+seed, two fresh processes
dotnet test ProjectAegis.sln --filter "Category=Replay&Scenario=[name]" 2>&1
# or, if a replay CLI exists:
# dotnet run --project src/ProjectAegis.Delegation.Demo -- --scenario [name] --seed [seed] --emit-log runA.log
# dotnet run --project src/ProjectAegis.Delegation.Demo -- --scenario [name] --seed [seed] --emit-log runB.log
```

Capture for each run: the **order log** (sequence of timestamped intents) and the
**world-state hash** at the final tick (and at periodic checkpoints if emitted).

**If the runner is unavailable in this environment** (no `dotnet` on PATH, runner
missing): record status as **NOT RUN** — do not treat as FAIL. Ask the developer
to confirm results from local/CI, mirroring the `/smoke-check` NOT-RUN handling.

---

## Phase 3: Compare

Three comparisons per scenario:

| Comparison | Question | Failure meaning |
|------------|----------|-----------------|
| **A vs B** | Did two fresh runs of the same seed match? | **Intra-run non-determinism** — the sim itself is unstable (worst case) |
| **A vs golden** | Did this run match the recorded baseline? | **Behavior drift** — sim changed since the baseline was recorded |
| **checkpoint hashes** | Do per-tick hashes match the golden? | Localises *where* divergence began |

Diff the order logs line-by-line and the state hashes. Record:
- First diverging tick (if any)
- Number of diverging order-log lines
- Whether divergence is A-vs-B (CRITICAL) or only A-vs-golden (drift — may be
  intentional)

**If `--bisect`:** walk the order log to the first tick where hashes diverge and
report the controller/target that emitted the first differing intent. This is the
hand-off artifact for `determinism-engineer` to root-cause.

---

## Phase 4: Classify the Result

| Verdict | Condition |
|---------|-----------|
| **PASS** | For all scenarios: A == B **and** A == golden (byte-identical order log + state hash) |
| **PASS (BASELINE DRIFT)** | A == B for all scenarios, but A != golden — the sim is *internally* deterministic but behavior changed vs. the baseline. Requires a human decision: intentional change (→ re-record) or regression (→ FAIL). |
| **FAIL** | Any scenario has A != B — the sim is non-deterministic. Release-blocking. |
| **NOT RUN** | Runner unavailable; developer must confirm from local/CI. Not a FAIL by itself. |

---

## Phase 5: Generate Report

````markdown
## Replay Verify Report
**Date**: [date]
**Scope**: [scenario-name | all]
**Mode**: [verify | --record | --bisect]
**Sim runner**: [path / NOT RUN reason]

---

### Results

| Scenario | Seed | A vs B | A vs Golden | First Divergent Tick | Verdict |
|----------|------|--------|-------------|----------------------|---------|
| [name] | [seed] | MATCH | MATCH | — | PASS |
| [name] | [seed] | MATCH | DIFFER | tick 1423 | DRIFT |
| [name] | [seed] | DIFFER | — | tick 087 | FAIL |

---

### Divergence Detail *(if any)*

**[scenario] — first divergence at tick [N]:**
- Order-log lines differing: [count]
- Run A: `[first differing intent]`
- Run B / Golden: `[first differing intent]`
- Attributed to: [controller / target id]  *(only with --bisect)*

---

### Verdict: [PASS | PASS (BASELINE DRIFT) | FAIL | NOT RUN]
````

---

## Phase 6: Write, Gate, and Handle Drift

Present the results table and any divergence detail in conversation.

Ask: "May I write this replay verification report to `production/determinism/replay-[date].md`?"

Write only after approval.

Then deliver the gate verdict:

**If FAIL (A != B):**
> "⛔ The sim is non-deterministic — two runs of the same seed diverged at tick
> [N]. This is release-blocking. Run `/replay-verify [scenario] --bisect` to
> localise the cause, then `/determinism-audit` on the implicated namespace, and
> hand the bisected tick to `determinism-engineer`."

**If PASS (BASELINE DRIFT) — A == B but A != golden:**
Use `AskUserQuestion` to resolve:
```
question: "[scenario] is internally deterministic but differs from its golden baseline. Was the behavior change intentional?"
options:
  - "Intentional — re-record the baseline" (→ re-run with --record after confirming the change is correct)
  - "Unintended regression — treat as FAIL" (→ stop; the change must be reverted or fixed)
  - "Unsure — needs review" (→ leave verdict as DRIFT, do not advance the gate)
```
Only regenerate a golden baseline with explicit user confirmation, and note the
reason in the commit message.

**If PASS:**
> "✅ Sim is reproducible — all scenarios produced byte-identical order logs and
> state hashes across runs and against golden baselines. Safe to merge / advance
> the gate. Pair with `/determinism-audit` for full coverage."

**If NOT RUN:**
> "Replay could not be executed (runner unavailable). Confirm reproducibility
> from local or CI before merging. NOT RUN is not a PASS."

---

## Phase 7: Gate Integration

`/replay-verify` + `/determinism-audit` together form the **sim merge gate** and
are required artifacts for the **Polish → Release gate**:
- `/determinism-audit` proves no known non-deterministic *patterns* exist (static).
- `/replay-verify` proves the sim actually *reproduces* (dynamic).

Neither alone is sufficient. The release gate requires a PASS (or explicitly
re-recorded baseline) here, with no open CRITICAL items in the latest audit.

---

## Collaborative Protocol

- **Never treat NOT RUN as PASS or FAIL** — record it and require manual
  confirmation, mirroring `/smoke-check`.
- **Never re-record a golden baseline without explicit approval** — silent
  re-recording hides regressions. Drift always goes to the user.
- **A != B is the worst case** — internal non-determinism is release-blocking and
  takes priority over baseline drift.
- **Determinism extends to all platforms** — note that a PASS in this environment
  does not guarantee cross-platform reproduction; flag platform-sensitive math
  (float/transcendental) for a target-hardware check.
