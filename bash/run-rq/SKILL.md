---
name: run-rq
description: |
  Use this skill to drive a research question (RQ) end-to-end: validate the
  RQ README, generate a fill batch-plan, start the Docker batch in the
  background, monitor progress, run aggregation, and propose findings updates.
  Trigger when the user says "RQ-N voranbringen", "run-rq", "fill RQ-N",
  "run RQ-N", "Forschungsfrage N starten", or names a specific RQ-N directory
  in research/.
---

# Skill: run-rq

End-to-end orchestration for advancing a single research question (RQ) in this lab repo. **Pure orchestration** — every operation calls existing repo scripts; no new Python or Bash code is written.

## Argument

- `RQ-N` (e.g. `RQ-model-quality`) or a direct path to an RQ dir.
- If not given: infer from the last user turn, otherwise ask back ("Which RQ? e.g. RQ-model-quality").

## Repo conventions (from the top-level `README.md` and memory)

- RQ dirs live in four subtrees: `research/questions-claude/<chapter>-*/` (Claude-Code RQs), `research/questions-opencode/<chapter>-*/` (OpenCode RQs), `research/questions-cross/<chapter>-*/` (cross-harness RQs), and `research/workflow-dev/<chapter>-*/` (workflow evolution). The `<chapter>` prefix (e.g. `2.6`) is an **ordering label, not an id** — the stable identity is the frontmatter `id:` (e.g. `RQ-lean`). Each RQ dir holds `README.md`, `findings.md`, `runs.csv`, `summary.md`.
- **Resolving an `RQ-<slug>` id to a path** (the dir name carries a chapter number, not the id): grep all subtrees for the frontmatter `id:`. Anchor with `^id:` and a trailing boundary so the whole slug must match exactly (no slug is a prefix of another, so an exact-line match is unambiguous):
  ```bash
  RQ_DIR=$(grep -rlE "^id:[[:space:]]*RQ-model-quality[[:space:]]*$" \
             research/questions-claude/*/README.md \
             research/questions-opencode/*/README.md \
             research/questions-cross/*/README.md \
             research/workflow-dev/*/README.md \
           2>/dev/null | head -1 | xargs -r dirname)
  ```
  On no match → ask the user. On multiple → take the first and inform the user. Pass `"$RQ_DIR"` to all scripts below (they accept any path and write outputs to the dir).
- Mandatory frontmatter fields: `id, question, factors, controls, outcomes, min_replicates`. There is no `status` field — whether the RQ needs work is read off the data (`experiments/rq-status.py`, rules in `experiments/rq_facts.py`). Only an RQ that ends without full data gets `closed: "<reason>"`, and only on the user's decision.
- Methodology constraint: `baseline-oneshot-*` / `baseline-iterative-*` only with `prompt: prose`; every other arm with all three styles. If `factors.workflow_x_prompt` exists, no additional `factors.workflow` / `controls.workflow` is allowed.
- Active katas: `claim-office`, `game-of-life`, `sphinx-score`, `game-of-life-cli`, `claim-office-lite`, `mars-rover`. `controls.kata_base` must be from this set. Each has the three prompt variants (`-prose`, `-user-story`, `-example-mapping`); all but `mars-rover` also have a `<basename>-verification/` suite, so `verification_pct` is available there.
  - The list is not a ranking, but the pool is lopsided in practice: `claim-office` and `game-of-life` carry the bulk of the runs, `sphinx-score` is the established small quality kata, and `mars-rover` is near-unused. Prefer a kata that already has runs in neighbouring RQs — a fill on a fresh kata has no reference cells to compare against.
  - **Check the actual kata dir before rejecting an RQ on this list.** The list is hand-maintained and has lagged behind the repo before (`sphinx-score` was in use in three RQs while still missing here). `ls experiments/katas/` is the authority; this line is a convenience copy.
- Model IDs are **lab-variant IDs** (`opus-4-7`, `opus-4-7-no-thinking`, `opus-4-6-portkey`, `opus-4-6-portkey-no-thinking`, `sonnet-4-6`, `sonnet-4-6-no-thinking`, `sonnet-4-6-portkey`, `sonnet-4-6-portkey-no-thinking`, `haiku-4-5`, `haiku-4-5-no-thinking`, `haiku-4-5-portkey`, `haiku-4-5-portkey-no-thinking`). The `-portkey` suffix marks models routed via the Portkey gateway.
- Aggregation is query-based: ALL runs in `experiments/runs/` matching the selector query count — regardless of which batch produced them.
- Batch plan is idempotent: counts existing matches and only fills missing replicates up to `min_replicates`.

## Phases

Run sequentially. On errors in any phase, **stop and ask the user**, do not skip ahead.

---

### Phase 1 — Validate

1. Resolve the RQ path into `$RQ_DIR` via the id-grep in "Repo conventions" above. On no match, ask the user; on multiple, take the first and inform the user.
2. Read `$RQ_DIR/README.md`.
3. Parse the frontmatter block (between the first two `---` lines). Check mandatory fields: `id, question, factors, controls, outcomes, min_replicates`. Missing fields → abort phase, inform user.
4. Check methodology constraints:
   - If `factors.workflow_x_prompt` is set: no additional `factors.workflow` and no `controls.workflow` may be set.
   - In every `workflow_x_prompt` entry: if `workflow ∈ {baseline-oneshot-v1-cc, baseline-iterative-v1-cc}`, then `prompt == prose` is required.
   - `controls.kata_base` is one of the active katas listed under "Repo conventions" above. Verify against `ls experiments/katas/` rather than against the list alone — the list is a convenience copy and has lagged the repo before.
   - Model values (in `controls.model` and/or `factors.model`) must appear in the lab-variant table.
5. Read `findings.md` (needed in phase 6 as the existing baseline).
6. Target computation: from `factors` × `controls` derive the cell count (every factor multiplies; paired factors like `workflow_x_prompt` count as a single factor with `len(pairing)` values). Target runs = cells × `min_replicates`. Report this number to the user.
7. **Portkey routing detection**: scan model values (in `controls.model` plus every `factors.model` entry) for a `-portkey` suffix. If any match:
   - Check `~/.claude.portkey/` directory exists. If missing: STOP, instruct the user to follow `experiments/docker/claude-config-portkey.README.md`. Do **not** start the batch.
   - Note: `batch.sh` auto-detects Portkey models from the plan JSON and sets `CLAUDE_CONFIG_DIR` automatically. No manual env-var needed in phase 3.

Output to user (compact):
```
RQ-N validated: <id>, <#cells> cells × min_replicates=<n> = <target> target runs.
cells at min_replicates: <full>/<declared> · findings: <n> · runs newer than findings: <n>
[Portkey routing required — using ~/.claude.portkey/ profile]   ← only if portkey_required
```

---

### Phase 2 — Plan

1. Run dry-run:
   ```
   experiments/batch-plan-from-rq.py "$RQ_DIR" --dry-run
   ```
2. Output contains the count of missing runs. Inform user:
   ```
   Cells: X, missing runs: Y → would write experiments/batch-plans/rq-{n}-fill.json
   ```
3. If `Y == 0`: no new runs needed — jump straight to phase 5.
4. Otherwise: get user confirmation ("Write the plan with Y runs now?"). Only proceed after explicit "yes".
5. Write the plan without `--dry-run`:
   ```
   experiments/batch-plan-from-rq.py "$RQ_DIR"
   ```
6. Briefly inspect the generated plan (Read on `experiments/batch-plans/rq-{n}-fill.json`) and summarize the cell distribution (`{kata, workflow, model}` frequencies) to the user.

---

### Phase 3 — Run

1. **Pre-check**:
   - `docker ps --filter name=docker-batch-run --format '{{.Names}}'` — if a container is running: STOP and ask the user whether the existing batch should finish first.
   - If `experiments/docker/batch.log` from an earlier run exists and is >0 bytes: ask the user whether to back it up as `experiments/docker/batch.<plan>.log` (`mv`, no deletion).
2. **User confirmation** before start: "Start batch `rq-{n}-fill` with Y runs in the background? Expected wallclock ≈ Y × 6 min ≈ Z min." (6 min/run per memory, smart-subset experience.) For Portkey RQs (flag from phase 1.7), append: "via Portkey gateway (auto-detected)".
3. Start with `--detach` (backgrounds the batch and disowns the process so the terminal can be closed safely):
   ```bash
   cd experiments/docker && ./batch.sh rq-{n}-fill --detach
   ```
   Portkey routing is **auto-detected** by `batch.sh`: it scans the plan JSON for `-portkey` model names and sets `CLAUDE_CONFIG_DIR=~/.claude.portkey` automatically. No manual env-var override needed. Sharding is on by default (5 shards, round-robin); override with `--shards N` when a plan is small or should run in one container:
   ```bash
   cd experiments/docker && ./batch.sh rq-{n}-fill --shards 10 --detach   # large fill
   cd experiments/docker && ./batch.sh rq-{n}-fill --shards 1 --detach    # single container
   ```
4. After a few seconds, determine the container name via `docker ps --filter name=docker-batch-run --format '{{.Names}}'` and report it to the user.

---

### Phase 4 — Monitor

1. Polling loop with `experiments/docker/watch-batch.sh rq-{n}-fill`:
   - First 5 min: snapshot every 60 s.
   - After that: every 5 min.
   - On every poll, report the counter `[N/total]` and container status.
2. Termination conditions:
   - `Container STOPPED` AND counter = `[total/total]` → success, continue to phase 5.
   - `Container STOPPED` AND counter < total → resume (phase 4b).
   - User signals abort → `docker stop <container>` → resume (phase 4b).
3. **Important**: Take memory patterns seriously:
   - `\b429\b` with `claude_exit != 0` = real rate limit; backup-warning with `backup.<ms>.json` (which can incidentally contain `429`) is to be IGNORED.
   - "Claude configuration file not found at: …" at container start is harmless.
   - Do not panic-retry when `watch-batch.sh` is once slow to respond.
4. **Mid-execution cleanup after stop**: the youngest run dir in `experiments/runs/` that lacks `analysis-report.md` OR `transcript.jsonl` was interrupted mid-execution. Ask the user: "Delete interrupted run dir `<run-dir>` (no analysis-report.md)?" Only delete with `rm -rf` after explicit "yes".

5. **Reading partial results while the batch runs** — optional, but if you look at
   metrics mid-batch, these three rules are binding. All three failed in one session
   (2026-08-10) and produced three wrong statements to the user in a row.

   **a) Never quote a quality metric without `verification_pct` in the same query.**
   A run that failed external verification produces *excellent-looking* quality
   numbers — few functions, low complexity, no smells — because it barely implemented
   anything. The correctness-gating rule of phase 6 exists for exactly this, but it
   only helps if the correctness column is in front of you. Query it together, always:
   ```bash
   jq -r 'select(.run_status.exit_reason=="ok") |
     "vpct=\(.final_metrics.verification_pct) cog=\(.final_metrics.cognitive_max) …"' */metrics.json
   ```
   Real case: `cognitive_max` 1 and `cc_avg_loc_per_function` 4.67 were reported as
   "beats the best cell in the field" — the run had `verification_pct = 0`.

   **b) A run is only readable once it is finished.** `metrics.json` exists from the
   start and is filled at the end; a running run returns `null` for every metric and
   an absent `exit_reason`. Filter on `select(.run_status.exit_reason=="ok")` rather
   than on file existence, and never mix finished and running runs in one listing —
   `ls -dt | head -1` regularly hits a running one. (Same trap as the cursor-harness
   note in memory: judge runs only after `experiment-done.txt`.)

   **c) Do not interpret a cell at n=1.** Report partial values as an observation
   ("first run of cell X shows …"), never as a rank statement, a hypothesis
   confirmation, or a comparison against a reference cell that has full n. The
   variance across replicates in this lab routinely exceeds the between-cell
   differences being measured — `refactorings_applied` σ 17.4 at n=5 in
   RQ-architecture-axis-sol-pi F-1.4 is a documented example.

   Also watch the glob when spot-checking: `*hybrid-v6*opus-5*` matches pi and cursor runs
   from other RQs. Anchor workflow and model exactly — `*_exact-hybrid-v6-lab-split-cc_opus-5-no-thinking*`.

#### Phase 4b — Resume

1. Generate a resume plan:
   ```
   experiments/docker/resume-plan.sh rq-{n}-fill
   ```
   → writes `/tmp/rq-{n}-fill-resume.json`.
2. Show the size to the user (`jq '.runs | length' /tmp/rq-{n}-fill-resume.json`).
3. Get user confirmation: "Restart with `<m>` remaining runs?"
4. After "yes" — resume with `--detach` (Portkey auto-detected from plan content):
   ```bash
   cd experiments/docker && ./batch.sh /tmp/rq-{n}-fill-resume.json --detach
   ```
   Back to phase 4.

---

### Phase 5 — Aggregate

1. **Pipeline sanity check before aggregating** — pipeline bugs masquerade as research findings. Spot-check 2–3 of the matched runs (covering the workflow × model cells most central to the RQ) for divergence between `run.log` and `metrics.json`:
   - In `run.log` the agent typically reports a final test status (e.g. "All N tests pass", "experiment-done.txt written"). Compare this against `final_metrics.tests_passing` in `metrics.json`. If the agent reports green but `tests_passing` is `false`, that's a pipeline issue, not a workflow effect.
   - Grep `analysis-report.md` for known infrastructure failure patterns: `IGNORED_BUILDS`, `approve-builds`, `corepack`, `ENOENT`, `Cannot find module`, `tsc.*error`. These typically come from container/tooling drift (e.g. pnpm version bumps, missing deps), not from agent code.
   - For CLI-katas (`<basename>-verification/` exists): check `cli_built` in `metrics.json`. If `cli_built: false` for a run whose `src/cli.ts` exists and runs manually (`pnpm exec tsx src/cli.ts < scenario.input.json`), the verification stage misfired — re-run `analyze-run.sh <run_dir>` on the host (with absolute path).
   - If any of these checks fail: stop, report the suspected pipeline bug to the user, do NOT aggregate. Fixing buggy data after a finding has been drawn from it is much more expensive than spending two minutes on the spot-check.
2. **Post-processing before aggregation** — some metrics are not filled by `analyze-run.sh` and must be computed separately. Skipping a step here does not error; it silently produces a zero or a null that reads like a research result.
   - **`cost_usd` — always, for any RQ whose `outcomes` contain it.** pi/Requesty runs land with `cost_usd = 0` because Requesty reports no inline cost (`usage: null`); the value comes from token × list price. Run it before aggregating:
     ```
     experiments/compute-cost.py "$RQ_DIR"
     ```
     Idempotent — existing values are recomputed, so it is safe to run on an RQ whose older runs already carry costs.

     **Ordering caveat — this step reads `runs.csv`, which phase 5.3 writes.** On an RQ that was just filled (or that you reached with 0 missing runs), `runs.csv` still describes the *previous* run set, so the script costs a subset and reports success for it. The script now refuses a stale csv and tells you to aggregate first; if you hit that, run `aggregate-by-query.py` once, then this script, then `aggregate-by-query.py` again so the fresh costs reach `summary.md`. Two verifications afterwards, not one: no cell may show $0.00 at non-zero `total_tokens` (impossible combination), **and** every cell present in the coverage table must also appear in the `cost_usd` pivot. A cell missing from that pivot entirely is the more common failure and reads like "metric not applicable" rather than like an error.
   - **`mutation_score` — only when it appears in `outcomes:`.** Expensive (minutes per run), opt-in per RQ, and only computed for `tests_passing = true`:
     ```
     experiments/compute-mutation-score.py "$RQ_DIR"
     ```
3. Invoke:
   ```
   experiments/aggregate-by-query.py "$RQ_DIR"
   ```
4. Expected outputs:
   - `$RQ_DIR/runs.csv` (one line per matched run)
   - `$RQ_DIR/summary.md` (per-cell pivots for each `outcome`)
5. Read `summary.md` in full and summarize to the user — show the per-cell pivot tables individually.
6. Sanity check: does every cell have ≥ `min_replicates`? If not: warn and offer to jump back to phase 2 (additional runs).
7. **Plausibility cross-check before phase 6** — if any cell value contradicts a previously-stable finding by a large margin (e.g. a workflow that was 100% green is suddenly 0%), do NOT treat that as a new finding without first running the spot-check from step 1 against that exact cell. A "the subagents arm is suddenly broken on game-of-life" type observation is more often a pipeline regression than a real shift.

---

### Phase 6 — Findings (write-first)

**Write directly to `findings.md`, then notify the user to review.** Markdown tables and trophy assignments are much easier to evaluate as rendered output than as a chat proposal; reverting is cheap (it's only markdown). After writing, send one line (in the user's language), e.g. "written — please review",.

Exception: **deletions** of existing findings still require explicit user confirmation before the `Edit` — losing a documented finding is more expensive than re-reading a fresh write.

`findings.md` shows **only the current state**. No status tags (`✅ stabil` / `⚠️ bedingt` / `🚫 offen` / `❌ widerlegt`), no comparisons with archive snapshots or older studies, no "previously X, corrected" hints in the prose. Header form: `## F-x.y — title` (no `· …` suffix).

**Overview table**: `findings.md` starts with a `## Overview` section containing a pivot table of the primary outcome across all factor levels (all models, all prompt styles, etc.) — before the individual `F-x.y` blocks. This table gives readers the full picture at a glance; individual findings then zoom in on specific effects. Update this table whenever findings are added or updated.

**Trophy convention (🏆) in overview tables**: append 🏆 to the best value per outcome row. Conventions:

- **Comparability first — a 🏆 needs an actual contest.** Before awarding anything, ask what varies across the columns of that row. Trophies are only meaningful when the cells differ in the factor under study and are otherwise alike. If a row spans cells that differ in *task size* rather than in the factor, drop the trophies for that table entirely and say so in the caveat block. The clearest case is an RQ with `kata_base` as a factor: `sphinx-score` (~183 Code Mass, ~12 cycles) against `claim-office` (~997, ~46) — the small kata always "wins" on cost, complexity and Code Mass (APP), which measures the kata, not the work. Same for any cross-kata cost or shape row. Options in order of preference: split the table so each row compares within one kata, restrict trophies to the rows that carry a real contrast, or omit them and label the table as context. This test comes **before** correctness-gating: gating narrows an existing field of competitors, it never creates one.
- **The test-list boundary is a comparability failure, not a close call.** Before
  awarding a trophy on `tdd_discipline`, `tdd_discipline_test_first`,
  `tdd_discipline_closure`, `test_first_rate`, `skip_events`, `cycles_total` or
  `chain_deviations`, check whether the row's cells differ in whether a test list
  is written up front. A `Skip` is compliance in a test-list workflow and a
  start-over condition in a strict-red one, so those columns then measure the
  architecture. Split the table by group and award within each, as
  RQ-tdd-workflow-comparison-opus55 does — never one trophy across the boundary.
  `aggregate-by-query.py` prints a warning naming both groups when an RQ is in
  this situation; treat it as binding. `red_batch_max` is the column that does
  compare everywhere, and on the measured field it orders the cells the opposite
  way from the score.
- The direction is metric-dependent — note it in the column header or row label (`smell_total` etc. → "lower = better"; `refactorings_applied`, `predictions_correct_rate` → "higher = better"). Don't assume.
- **Check the trophy against its own row after writing.** The winner must be the best value *in that row* under the stated direction. Gating rules constrain which cells are eligible, but they never move the trophy onto a worse value: if the only eligible cell is not the row's best, that row gets no trophy. Two failure modes to look for — a 🏆 on a higher number in a "lower = better" row, and a 🏆 in a row where every cell is identical (no contest, so no winner).
- Use 🏆 only where there is a meaningful winner. If the spread is below 1 σ and the framing is "no effect", award 🏆 to all near-tied values (or to none if the table message is "indistinguishable") — don't fabricate a winner from rounding noise.
- Multiple 🏆 are fine for ties. Three 🏆 across a row signal "no effect", which is itself a useful reading aid.
- Always bold the winner value too — 🏆 is in addition to, not instead of, the bold.
- Trophies belong only in human-facing research documents (`findings.md`, archive snapshots). Workflow files (`experiments/workflows/**/*.md`) stay emoji-free per the RQ-emoji / CLAUDE.md convention.
- **Correctness-gating** for code-quality and efficiency metrics: when the RQ has a correctness outcome (typically `verification_pct`), trophies for quality/efficiency metrics (`smell_*`, `cognitive_*`, `mccabe_*`, `cc_*`, `duration_seconds`, `total_tokens`, `cost_usd`, also derived $/perfect-result ratios) go **only** to cells with mean `verification_pct ≥ 0.90` — cells, not just models: the same applies when the factor is a prompt style or a kata. A cell that scores low on complexity / cost / duration but failed the verification is showing a stub, an abort artifact, or an implementation of a smaller wrong rule set — not parsimony or speed. Awarding a 🏆 there is misleading.

  The threshold is 0.90 rather than a perfect 1.0 because several katas have a case that no model solves — on claim-office `14-family-steinheim` fails deterministically for every cell (RQ-1.19 F-1.19.4), which caps the achievable mean at 14/15 = 0.93. A literal 1.0 gate would disqualify every cell in such an RQ and leave the table without a single winner, which says nothing about the models and defeats the point of the overview. 0.90 admits cells that solve essentially the whole spec while still excluding stubs and aborts.

  **A cell above the threshold can still be disqualified for a specific metric** when its leading value comes from work it did not do. Judge the failure mode, not only the score: a cell that drops an entire class of scenarios has a lower Code Mass (APP) because of missing coverage, not parsimony. Mark such a leading value in parentheses and award the trophy to the best cell that did the full work — e.g. `(659.0)` with no 🏆, the trophy going to the next-lowest eligible cell. State the reason in the caveat block. State the rule explicitly in the table's caveat block when it applies. Pure correctness metrics (`verification_pct` mean / std) are not gated. RQs without a correctness outcome (pure code-quality studies on game-of-life) are also not gated. Gating is a filter on an existing contest, not a licence to award: if it leaves a single eligible cell in a row whose columns were never comparable, the answer is no trophy, not a trophy for the survivor.

1. Diff sources:
   - **Existing**: `findings.md` from phase 1.
   - **New**: `summary.md` from phase 5.
2. Three possible actions per effect:
   - **New finding**: cell/factor group with Δ ≥ 1σ over the other groups AND the effect is not yet covered in `findings.md` → new `F-{N}.{M+1}` block (M = highest existing finding number). Write directly.
   - **Update**: an existing finding covers the same effect, but cell values or interpretation have shifted → `Edit` the existing block directly. Rewrite table and rationale, **without** old/new diff, **without** "previously X", **without** reference to archive snapshots.
   - **Deletion**: data contradicts the finding → ask the user first ("Finding F-x.y is contradicted by new data — remove it?"), then remove the block including its `---` separator on confirmation. Do not mark it as "refuted".
3. Data gap: if an effect is suspected but coverage is too small for `n ≥ min_replicates` → note in `todos_and_ideas/1-IN.md` as a bullet with a concrete re-check target. **Do not** create as a finding in `findings.md`.
4. Format per block: statement / data-base table / rationale. Header `## F-x.y — title` with no suffix. The namespace before the last dot may carry dots itself (`F-4.4.1`, `F-1.12.5` — chapter-numbered ids are in use and valid). The em-dash `—` is load-bearing: `generate-snapshot-skeleton.py` parses headers on it and silently skips any it cannot match, which then reads as "no findings documented" in the snapshot for an RQ that has a full findings.md.
   **Glossary discipline**: terms like `code_mass`, `cc_loc`, `cc_longest_function`, `smell_total`, `verification_pct` are to be used only in the form from the glossary in the top-level `README.md` ("Code Mass (APP)", "Production LoC", "Smell Total", "Correctness (external)") or directly via the metric ID in backticks. Synonyms like "Code-Volumen", "Code-Gesamtvolumen", "LoC-Größe" are forbidden — they are ambiguous or collide with established definitions (APP). The three complexity metrics carry **no** prose name at all: write `cc_longest_function`, `cognitive_max`, `cognitive_avg` or `mccabe_max` in backticks. "Complexity Peak", "Spitzen-Komplexität", "Cognitive Complexity peak" and "McCabe peak" are forbidden; the first had been used for three different metrics at once. Before writing, read the glossary once and check every term used in the block against the table.
5. **Number formatting in `findings.md`:** large counts (typically `total_tokens`, `subagent_token_total`, cache stats) get the `M`-suffix (millions) or `k`-suffix (thousands), not scientific notation. `summary.md` keeps the pandas-default `e+07` form — only `findings.md` gets reformatted. Examples: `44.4 M` (good), `4.44e+07` (bad in findings, fine in summary), `1023 ms` or `1.0 s` (good for duration). σ-Werte werden im selben Format dargestellt wie der Mean (`σ ≈ 5 M`, nicht `σ ≈ 5e+06`). Rationale: M/k ist auf einen Blick lesbar, e+07 zwingt zum Kopfrechnen.
6. **Verify every number you just wrote** before reporting. Do not skip this — a wrong
   number in a findings table looks authoritative and gets quoted onward. Pull the written
   rows back out and diff them against `summary.md`:
   ```bash
   grep -n "<cell-name>" "$RQ_DIR/findings.md" | grep "|"
   ```
   Check each value against the same metric in `summary.md` for **this** RQ.

   The failure mode this catches: when several RQs are edited in sequence, values from a
   different kata sit in context and get written from memory instead of looked up. Cell
   names and metric names are identical across RQs — only the ranges differ, and a foreign
   value is often plausible enough to survive proofreading. (Real case, 2026-08-04:
   `cc_longest_function = 15.0` from the game-of-life RQ landed in the claim-office RQ,
   where 21.4 was correct — wrong trophy, plus an interpretation sentence built on the
   wrong figure.)

   Two habits prevent it upstream: query metrics **completely** per RQ rather than
   selectively (the gap appears when a table column is missing from the fresh extract),
   and treat magnitude as a sanity anchor — claim-office is the large kata
   (`code_mass` ~666, `cycle_count` ~47), game-of-life the small one (~144, ~15).

7. After verifying, send one short line to the user (in their language), e.g. "written — please review". The user reviews the rendered markdown directly.

---

## Out of scope (deliberately NOT in the skill)

- The actual batch execution inside the container (`run-batch.sh` runs in the container).
- ESLint / smell detection (runs per run inside `analyze-run.sh`).
- Cross-RQ aggregation or creation of new RQs.
- Auto-commit/push of `runs.csv` / `summary.md` / `findings.md` — stays a user decision.
- Merging into `main`.

## Behavior on errors

- **Phase 1 fails**: do not continue; give a clear constraint hint (e.g. "baseline-oneshot-v1-cc with prompt=example-mapping violates the methodology constraint in the top-level README, section 'Methodology constraints'").
- **Phase 2/3 scripts with non-zero exit**: show output to the user; do NOT blindly retry.
- **Phase 4 loses the container**: show `docker ps -a`, then offer resume.
- **Phase 5 produces an empty `runs.csv`**: check whether `experiments/runs/` actually contains matching runs (selector too narrow?). Inform the user.
