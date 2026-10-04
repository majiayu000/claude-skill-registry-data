---
name: autoresearch
description: "Bounded improvement loop: one artifact, fixed eval score, keep an edit only if strictly better. Use for AR_DESIGN/AR_FUNCTION/AR_ACCEPTANCE stages or standalone bounded iteration."
hooks:
  PreToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "bash ${CLAUDE_SKILL_DIR}/bin/check-harness-immutable.sh"
          statusMessage: "Checking harness immutability..."
    - matcher: "Edit"
      hooks:
        - type: command
          command: "bash ${CLAUDE_SKILL_DIR}/bin/check-harness-immutable.sh"
          statusMessage: "Checking harness immutability..."
---


<!-- desc:full -->
## Full description

Shared bounded-loop runner for the Karpathy autoresearch pattern applied to code:
ONE mutable artifact + a FIXED evaluation harness emitting ONE comparable composite score,
looped as snapshot -> one focused edit -> score -> keep-if-strictly-better-else-revert -> log,
bounded by per-pass max_iterations / max_consecutive_reverts and the cost brake.
Invoked by the pipeline-orchestrator for the AR_DESIGN / AR_FUNCTION / AR_ACCEPTANCE stages,
or runnable standalone. Validation only; NEVER auto-commits and NEVER runs destructive git.

# Autoresearch — bounded keep/revert runner

This skill is the **runner**. It does not define *what* to optimize or *how* to score —
those live in the three per-pass prompt files. The runner owns the **loop spine**:
setup, one-edit-at-a-time iteration, snapshot/keep/revert, the `results.tsv` log, and the
bounded stop conditions. It is adapted directly from the AMS PRD autoresearch
`program.md`, generalized from "edit one PRD to maximize a reflection score" to "edit the
production source touched by a task to maximize a per-pass composite score."

> Invariant (Karpathy autoresearch): **ONE mutable artifact + a FIXED harness emitting ONE
> comparable score**, then `loop { pick one idea -> edit -> score -> keep-if-better-else-revert
> -> log } -> stop on threshold / plateau / cap`. You read this file and follow it.

---

## How it is invoked

This runner has three **modes**, one per pipeline pass. The active mode selects exactly one
per-pass prompt file, which is the authoritative source for that pass's **mutable surface,
fixed harness, rubric/KPIs, composite formula, and hard constraints**:

| Mode | Pipeline stage | Per-pass prompt file (READ THIS for the active mode) |
|------|----------------|------------------------------------------------------|
| `design`     | AR_DESIGN (AR-1, pre-TDD)      | `program.ar-design.md` |
| `function`   | AR_FUNCTION (AR-2, post-TDD)   | `program.ar-function.md` |
| `acceptance` | AR_ACCEPTANCE (AR-3, post-QA)  | `program.ar-acceptance.md` |

**Two entry paths:**

1. **Pipeline-orchestrated (normal).** The `/pipeline` state machine invokes this runner at
   `AR_DESIGN` (after CODE_REVIEW), `AR_FUNCTION` (after TDD), and `AR_ACCEPTANCE` (after
   PHASE_GATE). The orchestrator passes the mode and fills all placeholders from
   `.aid/context.json` + `.aid/pipeline/config.json`. On stop the runner FIRST restores the
   editable set to the best-kept version, THEN logs final scores to `step_history` and writes
   `.aid/pipeline/state.json` **unconditionally as the FINAL action — after the last source
   mutation of ANY kind** (kept edit, revert/restore `cp`, or crash restore), so the Stop hook
   (`dev-pipeline-gate.sh`) freshness check still passes (newest source mtime <= state mtime).

2. **Standalone.** A human runs it directly on a single mode. Resolve placeholders yourself
   from `.aid/context.json` + `.aid/pipeline/config.json`; if a value is absent, use the
   defaults noted in the per-pass file and state the assumption in chat.

> **Order matters and is enforced upstream:** `function` mode requires a green test suite to
> exist (TDD produced it); `acceptance` mode requires QA to have run. Do not invent a harness
> a pass does not yet have — that is precisely why the passes are split.

---

## Placeholders (filled at runtime)

Resolved from `.aid/context.json` and `.aid/pipeline/config.json`. The per-pass file declares
which it uses; the runner only needs these for the loop spine:

| Placeholder | Source | Meaning |
|-------------|--------|---------|
| `{{WORKSPACE}}` | context.json | Repo root path |
| `{{TASK_ID}}` | context.json | Current task id; names the results dir |
| `{{CRITICALITY_PROFILE}}` | context.json / config.json | Risk profile gating ASK-before-edit behavior |
| `{{KPI_TARGET}}` | config.autoresearch.kpi_target (default 9.5) | Quality-score target (0–10) |
| `{{TEST_COMMAND}}` | config.test_commands.unit (+coverage) | Harness command (function mode) |
| `{{MIN_COVERAGE}}` | config.thresholds.min_coverage_percent | Coverage gate (function mode) |
| `{{SAFETY_CRITICAL_FLOWS}}` | context.json | Flows requiring ASK-before-edit |
| `{{RECORD_FILE}}` | derived | `.aid/pipeline/autoresearch/{{TASK_ID}}/results.tsv` |
| pass-specific | config.autoresearch.<pass> | `max_iterations`, `max_consecutive_reverts`, internal `rounds`, and (AR-3) `max_acceptance_rounds`, `pass_rate_target` |

Per-pass caps come from `config.autoresearch`:
`{ kpi_target, ar_design:{max_iterations,max_consecutive_reverts},
ar_function:{max_iterations,max_consecutive_reverts,internal_rounds},
ar_acceptance:{max_acceptance_rounds, pass_rate_target} }`.

> **`ar_design` has NO `internal_rounds`.** The bounded internal refine-rounds knob belongs to
> `ar_function` ONLY (AR-2 allows a few internal apply/refine rounds before official scoring);
> AR-1 design does a single apply per iteration. The `internal_rounds` key was therefore
> **removed from the `ar_design` block in `config.default.json`** — it is a dead key under
> `ar_design` and must not be reintroduced there.

### Placeholder → config bindings

The per-pass prompt files may keep their `{{...}}` placeholder names; this table is the
authoritative binding of each to its `config.autoresearch` key:

| Placeholder | Config key |
|-------------|-----------|
| `{{AR1_MAX_ITERS}}`     | `config.autoresearch.ar_design.max_iterations` |
| `{{AR1_MAX_REVERTS}}`   | `config.autoresearch.ar_design.max_consecutive_reverts` |
| `{{AR2_MAX_ITERS}}`     | `config.autoresearch.ar_function.max_iterations` |
| `{{AR2_MAX_REVERTS}}`   | `config.autoresearch.ar_function.max_consecutive_reverts` |
| `{{AR2_INTERNAL_ROUNDS}}` | `config.autoresearch.ar_function.internal_rounds` (NEW key, default 2) |

---

## The loop SKELETON (shared by all three modes)

The mode's per-pass file supplies the **harness** (how to produce the composite score), the
**rubric/dimensions**, the **composite formula**, and the **hard constraints**. Everything
below is identical across modes.

### Setup phase (run ONCE per pass, then never again)

1. **Read the active per-pass prompt file** for this mode (table above). It is authoritative
   for mutable surface, harness, rubric, composite, constraints, and stop conditions specific
   to the pass. The runner's stop conditions below are layered *on top* of those.
2. **Resolve the mutable surface.** The artifact under optimization is the **production source
   changed by this task**:
   ```bash
   git -C "{{WORKSPACE}}" diff --name-only HEAD          # tracked changes
   git -C "{{WORKSPACE}}" ls-files --others --exclude-standard   # untracked (new) files
   ```
   The union (filtered to source per the per-pass file) is your mutable surface. Everything
   else — the harness, tests (in `function`/`acceptance`), criteria YAMLs, `.aid/*.json`,
   config — is **read-only**. (`git` here is read-only inspection; no commits, no resets, no
   `checkout`/`restore` of tracked files. Rollback is done via snapshot copies, below.)
3. **Create the results directory and snapshots dir:**
   ```bash
   mkdir -p ".aid/pipeline/autoresearch/{{TASK_ID}}/snapshots"
   ```
4. **Init `results.tsv`** (`{{RECORD_FILE}}`) if absent or header-only, with this header line
   (tab-separated):
   ```
   iter	composite	delta	<one column per rubric dimension>	status	snapshot	utc
   ```
   The per-pass dimension columns sit **between `delta` and `status`** and are named by the
   active per-pass file using the EXACT criterion ids (e.g. AR-1:
   `structural_health loudness_of_failures naming_clarity docs_traceability`; AR-2:
   `quality pass_rate coverage`). Each per-pass program file prints its OWN exact header.
   Single-letter abbreviations (S/L/N/D) are NEVER allowed as TSV column names — only in the
   human one-line chat output. If `results.tsv` already has data rows, **do NOT re-baseline** —
   resume from the next iter.
5. **Score the baseline** using the per-pass harness on the current on-disk source. Record the
   composite as `best_score`. Snapshot the baseline of every mutable file:
   ```bash
   TS="$(date -u +%Y%m%dT%H%M%SZ)"
   # Directory form — AUTHORITATIVE (matches each per-pass program file; per line 111 the
   # per-pass file wins): ONE baseline directory with the mutable files copied in preserving
   # their relative paths, so verify-run.sh's per-file revert check can diff against it.
   # Do NOT use a flat 000-baseline-<safe-F> file — that splits the baseline across files and
   # makes verify-run.sh skip the revert check (WARN, not FAIL).
   DST=".aid/pipeline/autoresearch/{{TASK_ID}}/snapshots/000-baseline-$TS"; mkdir -p "$DST"
   # for each mutable file F: copy it into "$DST" preserving its relative path
   ```
6. **Append row 0** to `results.tsv` with `iter=0`, `composite=<best_score>`, `delta=0.00`,
   the baseline dimension scores, `status=baseline`, the baseline snapshot tag, and UTC.
7. **Record the rubric fingerprint (harness-tamper detection).** At PASS START — once, here in
   setup — compute a SHA-256 fingerprint over the EXACT bytes of the harness inputs that define
   the score: the active mode's **criteria YAML** plus the reflection-agent's
   `{{WORKSPACE}}/.claude/agents/reflection-agent.md` (concatenate the files in a
   fixed order, then hash). Record it in `state.json` under
   `state.autoresearch.<mode>.rubric_sha256` and note it in the stop summary. The whole point of
   the keep/revert loop is comparing scores across iterations against a FIXED harness — if the
   criteria YAML or the agent prompt change mid-pass, every score before and after the change is
   **incomparable** and the loop's keep decisions are meaningless. Therefore `verify-run.sh`
   recomputes the same hash from the on-disk inputs and **FAILS LOUDLY on any mismatch** with the
   recorded `rubric_sha256`, rather than silently trusting a tampered run. (Spec-level: this
   runner is prose-driven — the runner computes/records the hash in prose and `verify-run.sh`
   owns the recompute-and-compare gate.)

### Experimentation loop

Track an in-memory counter `N` (next iter from `results.tsv`) and `consecutive_reverts`.
For each iteration:

1. **Read state.** Re-read the on-disk mutable files. Read `results.tsv`; set
   `best_score = max(composite where status='kept')`, fallback baseline. Skim recent
   `reverted` ideas — **do not repeat them**.
2. **Pick ONE focused edit.** A single, small, reviewable, single-purpose change permitted by
   the active per-pass file's constraints. **One idea per iteration** — never "while I'm here,
   also fix X" (multi-variable edits give uninterpretable scores).
3. **Snapshot PRE-edit.** Before touching anything, copy every mutable file you are about to
   change to a snapshot, so it is a clean rollback target:
   ```bash
   SLUG="<short-kebab-of-the-idea>"; TS="$(date -u +%Y%m%dT%H%M%SZ)"
   cp "$F" ".aid/pipeline/autoresearch/{{TASK_ID}}/snapshots/$(printf '%03d' $N)-pre-$SLUG-<safe-F>-$TS"
   ```
4. **Apply the edit.** Edit only the mutable source. Some per-pass files allow a bounded set of
   internal refine rounds before official scoring — follow the file; default is one apply.
5. **Score via the pass's harness.** **First, re-verify the harness fingerprint** (mid-pass tamper guard): recompute the rubric SHA-256 (criteria YAML + reflection-agent `AGENT-PROMPT.md`, same recipe as setup step 7) and compare it to the recorded `state.autoresearch.<mode>.rubric_sha256`; on mismatch, HALT the pass loudly with status `rubric-tampered` — every score across the change is incomparable — instead of waiting for the out-of-band `verify-run.sh`. Then run the per-pass harness exactly as that file specifies
   (e.g. `design`: reflection-agent only; `function`: `{{TEST_COMMAND}}` + coverage as Tier-1
   gates × reflection quality; `acceptance`: validators + reflection). Compute the **composite**
   per the file's formula. This is the official iteration score.
   > **reflection-agent harness:** spawn the subagent named `reflection-agent` and load its
   > prompt from `{{WORKSPACE}}/.claude/agents/reflection-agent.md`. NEVER hardcode
   > a user-level path (e.g. `~/.claude/skills/reflection/...`) — it does not exist.
6. **Keep or revert (STRICT improvement).**
   - If `composite > best_score` (strictly greater): `status = kept`; set `best_score = composite`;
     leave the edited files on disk; reset `consecutive_reverts = 0`.
   - Else: `status = reverted`; restore each touched file from its step-3 snapshot
     (`cp -p <snapshot> "$F"` — preserve mtime so a restored file never reads newer than
     `state.json`); `best_score` unchanged; `consecutive_reverts += 1`.
   - If scoring **crashed** / harness errored (e.g. could not run tests): `status = crash`;
     restore from snapshot (`cp -p`); `consecutive_reverts += 1`.
   - **Restore robustness (every restore `cp -p`):** check the exit status of EVERY restore
     `cp -p`. If ANY restore fails, do NOT advance on a mixed/partial tree: set the distinct
     loud status `restore-failed`, append the row, and **HALT the pass immediately** (then jump
     to the stop sequence so `state.json` is still written last).
   - **Function mode only:** a test going from green to red is an **automatic revert** regardless
     of the quality sub-score (the per-pass composite already zeroes out via the Tier-1 hard
     gate); log it as `status = reverted-redtest`, restore from snapshot, `consecutive_reverts += 1`.

   The `consecutive_reverts` counter increments on **`reverted`, `reverted-redtest`, and
   `crash`** alike (all three count toward the pass's `max_consecutive_reverts`); only a `kept`
   iteration resets it to 0.
7. **Append a `results.tsv` row:**
   ```
   <N>	<composite>	<composite - best_score_before_this_iter>	<dim scores...>	<kept|reverted|crash>	<snapshot>	<UTC-iso>
   ```
8. **Print ONE chat line** (see Output), increment `N`, check stop conditions, loop.

### results.tsv columns (authoritative)

**This SKILL.md is authoritative for the COMMON columns**, in this exact order:

```
iter	composite	delta	<one column per rubric dimension>	status	snapshot	utc
```

- `iter` — iteration index; AR-1/AR-2 use an integer, **AR-3 may use a string iter id** (e.g.
  `ar3-r<R>`).
- `composite` — the pass's composite score.
- `delta` — `composite - best_score_before_this_iter`.
- `<one column per rubric dimension>` — the **per-pass dimension columns**, inserted between
  `delta` and `status`. Each per-pass program file **defines its OWN dimension columns and MUST
  print its exact header**, using the EXACT criterion ids as column names:
  - **AR-1:** `structural_health` · `loudness_of_failures` · `naming_clarity` · `docs_traceability`
  - **AR-2:** `quality` · `pass_rate` · `coverage`
  - **AR-3:** per `program.ar-acceptance.md`.
  Single-letter abbreviations (S/L/N/D) are allowed ONLY in the human one-line chat output —
  NEVER as TSV headers.
- `status` — `kept` | `reverted` | `reverted-redtest` | `crash` | `restore-failed`.
- `snapshot` — the pre-edit snapshot filename for this iter; **AR-3 uses `-`**.
- `utc` — ISO-8601 UTC.

**Right-anchored positional parse rule (authoritative).** The renderer/parser **tolerates
per-pass dimension column sets** by reading the common columns positionally from BOTH ends:
the **FIRST column is always `iter`** and **the LAST three columns are always `status
snapshot utc`, in that order, for EVERY pass — AR-1, AR-2, AND AR-3 alike**. Everything between
`iter` and `status` is that pass's own columns: AR-1 and AR-2 lead with `composite delta` then
their rubric dimensions, while **AR-3 has no `composite`/`delta` — its in-between columns are
exactly its two dimensions `pass_rate why_alignment`**. A parser MUST key dimension columns off
the per-pass header row, NOT assume `composite`/`delta` at fixed positions 2–3. For this right-anchored rule to hold, **a row
must NOT carry any trailing free-text field after `utc`**: AR-3 in particular does NOT append an
inline one-line gap-summary field to its `results.tsv` row — every AR-3 pass ends, exactly like
AR-2, with `status` then `snapshot` (`-`) then `utc` as its final three columns. The human
one-line gap summary lives in chat/summary output ONLY, never in the TSV row. (`program.ar-acceptance.md`'s
row spec MUST agree with this: trailing `status`, `snapshot` = `-`, `utc`.)

---

## Stop conditions (bounded — the loop ALWAYS terminates)

Stop the loop when **ANY** fires. The first three caps come from `config.autoresearch.<pass>`;
all are enforced by the runner regardless of mode:

- **Target met:** the per-pass success condition holds (e.g. all KPI dimensions ≥ `{{KPI_TARGET}}`;
  for `function` the composite ≥ target with all Tier-1 gates green; for `acceptance` the
  per-pass DONE condition — pass_rate ≥ `pass_rate_target`, no blockers, why_alignment ≥ target).
- **Plateau:** `consecutive_reverts` reaches the pass's `max_consecutive_reverts`. This counter
  increments on `reverted`, `reverted-redtest`, and `crash` iterations; only a `kept` iteration
  resets it to 0.
- **Iteration cap:** `N` reaches the pass's `max_iterations`.
- **Cost brake:** the pipeline-wide `cost_limits.max_per_run_usd` is hit — stop immediately.
- **Human interrupt:** any new prompt / interrupt.
- **AR-3 outer loop:** `acceptance` mode additionally bounds its DEVELOP re-entry by
  `max_acceptance_rounds`; on the cap with open blockers it **ESCALATES to the user** rather
  than looping the pipeline. (Details in `program.ar-acceptance.md`.)

On stop, the runner MUST, in this order: (1) **restore the editable set to the best-kept
version** (the highest-scoring `kept` snapshot, or the baseline if nothing was kept) — restore
each file with `cp -p <snapshot> "$F"` (preserve mtime so a restored file never reads newer than
`state.json`), and **check the exit status of EVERY restore `cp -p`**; if ANY restore fails, set
the distinct loud status `restore-failed` and **HALT** (do not advance on a mixed tree) — but
STILL proceed to write `state.json` last (step 3). Before the baseline fallback, `test -r` the
target snapshot first and surface an explicit error if it is **absent or unreadable**, rather
than `cp`-ing a missing path. (2) summarize: starting composite, final `best_score`, count of
`kept` vs `reverted` vs `crash`, the top kept changes by delta, and which stop condition fired;
(3) in pipeline mode, write the final scores to `step_history` and write
`.aid/pipeline/state.json` **UNCONDITIONALLY as the FINAL action — after the last source mutation
of ANY kind** (kept edit, revert/restore `cp -p`, or crash restore), so the Stop hook does not
re-block. Because a plateau stop often fires right after a run of reverts (whose restore `cp -p`
sets the source mtime to the snapshot's preserved mtime), the state.json write MUST be the last
disk write of the pass — never conditioned on the last write being a kept edit. **Verify the
write symmetrically with the restore checks:** check the exit status of the `state.json` write
(prefer write-to-temp then atomic rename) and re-read it to confirm it parses and its mtime ≥ the
newest source mtime. If the write fails, set the distinct loud status `state-write-failed` and
surface it — do NOT rely on the downstream Stop gate, whose "re-run /pipeline" message would
otherwise mask a genuinely failed write.

---

## Safety brakes & hard constraints (non-negotiable — org + pipeline policy)

- **NEVER auto-commit. NEVER run destructive git** (no `commit`, `reset`, `checkout`/`restore`
  of tracked files, `clean`, force-push, branch deletion). `git diff`/`ls-files`/`status` for
  inspection only. Rollback is **always** via snapshot `cp`. The human commits after review;
  the runner only validates and leaves the existing "validated — your call" nudge.
- **Touch only the mutable surface** resolved in setup. Never edit the harness, tests
  (in `function`/`acceptance`), criteria YAMLs, `.aid/*.json`, `config.json`, `.mcp.json`, or
  any pipeline/skill file. Modifying the harness makes the score meaningless.
- **Snapshots only** under `.aid/pipeline/autoresearch/{{TASK_ID}}/snapshots/`, only via the
  `cp` commands above.
- **No new dependencies, no framework migration, no plaintext secrets.** If a fix seems to need
  a new dep or a secret, stop and surface it — do not add it.
- **No scope reduction to game the score** (don't delete behavior/criteria/tests to raise a number).
- **One idea per iteration. Strict-improvement keep.** Equal scores revert.
- **Respect `{{CRITICALITY_PROFILE}}`:** ASK before edits touching `{{SAFETY_CRITICAL_FLOWS}}`.
- **Bounded by construction:** per-pass `max_iterations` + `max_consecutive_reverts` + the cost
  brake (and AR-3's `max_acceptance_rounds`) guarantee termination.

---

## Output expectations (be quiet)

After each iteration, print exactly ONE line to chat:

```
iter <N> | <kept|reverted> | <composite> (Δ <delta>) | <one-line desc of the change>
```

Do not narrate reasoning or dump the reflection-agent's full breakdown. `results.tsv` is the
source of truth; the user can ask for detail. Emit the stop summary only when the loop ends.
