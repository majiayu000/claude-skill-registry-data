---
name: skill-evals
description: Run benchmark evaluations for any skill. Reads evals/evals.json from the target skill, spawns parallel with-skill and without-skill agent runs, grades outputs against assertions, aggregates benchmark statistics, and launches the eval viewer. Use when you want to measure or compare skill performance without entering the full skill-creator create/improve flow. Trigger on phrases like "run evals", "run the evals", "benchmark this skill", "run the eval loop", "test this skill against baseline", or when a skill has an evals.json and the user wants to see how it performs.
license: MIT
metadata:
  version: "1.1.6"
---

<!-- Changed from Anthropic's skill-creator (Apache-2.0, https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator); this file is not the original. -->

# Run Evals

Runs the benchmarking eval loop for an existing skill. Extracted from `skill-creator` — use this when the skill already exists and you only need to measure it, not create or improve it.

This is one continuous sequence — do not stop partway through.

---

## Inputs

- **Skill path** — absolute path to the skill directory being evaluated (e.g. `${CLAUDE_PROJECT_DIR}/.claude/skills/writing-architecture-and-design`)
- **Iteration** — auto-detect from existing `evals/workspace/iteration-*/` dirs; use next number, default 1

---

## File Structure

All eval artefacts live inside the skill directory being evaluated:

```
<skill-dir>/
  SKILL.md
  evals/
    evals.json                         ← eval definitions (pre-existing; read by this skill)
    inputs/                            ← optional fixture tree (pre-existing; tracked)
    workspace/
      iteration-N/
        stage_manifest.json
        <eval-name>/                   ← one directory per eval case
          eval_metadata.json
          with_skill/
            inputs/                    ← this run's private fixture copy
            staged_manifest.json
            eval_metadata.json
            outputs/                   ← skill output files + transcript.md go here
              run_delta.json
              product/
              reference/
            grading.json
            timing.json
          without_skill/               ← same shape as with_skill/
        benchmark.json
        benchmark.md
        feedback.json                  ← downloaded from viewer
```

**What each artefact contains, and its exact location, is `references/schemas.md`** — one section per
file. This tree is a map, not a specification: the shapes have one home, and it is not here.

Supporting tools:
- Grader: `<CORE>/../skills/experimental/.claude/skills/skill-evals/agents/grader.md`
- Benchmark: `<CORE>/../skills/experimental/.claude/skills/skill-evals/scripts/aggregate_benchmark.py`
- Viewer: `<CORE>/../skills/experimental/.claude/skills/skill-evals/eval-viewer/generate_review.py`
- Fixture guard: `<CORE>/../skills/experimental/.claude/skills/skill-evals/scripts/fixture_guard.py`
- Fixture staging: `<CORE>/../skills/experimental/.claude/skills/skill-evals/scripts/stage_fixtures.py`
- Harvest: `<CORE>/../skills/experimental/.claude/skills/skill-evals/scripts/harvest_run.py`

---

## Step 1 — Read evals and prepare

1. Read `<skill-dir>/evals/evals.json`
2. **Validate tier field — mandatory.** For every assertion/expectation in every eval case, verify a `tier` field is present with value `"structural"` or `"nuanced"`. If any assertion is missing `tier`, **stop immediately** and surface an error:

   > "evals.json validation failed: assertion `<name or text>` in eval `<eval_name>` is missing a required `tier` field. Add `\"tier\": \"structural\"` or `\"tier\": \"nuanced\"` to every assertion before running evals."

   Do not proceed until every assertion has a valid tier.

3. Determine the iteration number: check existing `evals/workspace/iteration-*/` dirs; use the next number (1 if none exist) — for reporting only.

**Do not create `iteration-N/` yourself.** The workflow's setup step derives the iteration from the
**highest** existing number, so a pre-created empty directory becomes the new highest and the run lands
one past where you told the user it would. The workflow creates the directory.

It takes the highest rather than the count because the two diverge the moment the sequence has a gap, and
an iteration directory is never reused: a run archive is the only record of what a past run did, and
`workspace/` is gitignored, so an overwrite cannot be recovered.

---

## Step 1b — Open the fixture guard

Skills whose evals have an `evals/inputs/` fixture tree resolve a **relative, in-repo** `Product path:`,
so a producer skill that owns its own file locations resolves *into the tracked fixture*. Nothing in the
harness prevents that write. Snapshot before the run so any movement is provably this run's:

```bash
python3 "<CORE>/../skills/experimental/.claude/skills/skill-evals/scripts/fixture_guard.py" \
  snapshot --skill-dir <skill-dir>
```

Exit non-zero → **stop. Do not run the workflow.** Surface the reason:
- exit 2 `already dirty` — the fixture tree was dirty before the run. Inspect it; it is very likely
  damage from an earlier run. Commit it or restore it, or re-snapshot with `--allow-dirty-inputs`
  (which makes the user's uncommitted bytes the restore target, never HEAD).
- exit 2 `still open` — a previous run's guard was never closed. Run `verify` (then `repair`) first.

A skill with no `evals/inputs/` is a clean no-op.

---

## Step 2 — Run the eval workflow

Invoke the `run-skill-evals` workflow, passing both the skill directory under test and skill-evals's own
directory as `args` (`<CORE>/../skills/experimental/.claude/skills/skill-evals`, which under a pin is the
pinned copy the run started on — the same spelling every other host path on this page uses, and one
both providers resolve, where `${CLAUDE_SKILL_DIR}` is Claude's alone; the workflow does not derive one
skill's directory from the other's, it takes both as input):

```
Workflow({ name: 'run-skill-evals', args: { skillDir: '<skill-dir>', skillEvalsDir: '<CORE>/../skills/interactive/.claude/skills/skill-evals' } })
```

The workflow handles everything in background — metadata setup, parallel executor runs (with_skill and without_skill), and grading for each run as it completes. Wait for it to return before proceeding.

The workflow returns `{ workspace, skill_name, iteration }`.

---

## Step 2b — Close the fixture guard

Run this **immediately after the workflow returns, before aggregating.** The workflow's own Stage phase
now gives every (case × configuration) its own private, writable fixture copy (`stage_fixtures.py`), so
the two arms no longer share one tree and cannot feed each other's output. This verifies the **tracked**
`evals/inputs/` tree itself stayed byte-identical. A write that reaches it despite staging is worse than
ordinary damage — it means an executor escaped its private copy, or staging itself broke — so the
grading may be *invalid*, not merely the tracked tree dirty. Find that out before you compute a
benchmark from it.

```bash
python3 "<CORE>/../skills/experimental/.claude/skills/skill-evals/scripts/fixture_guard.py" \
  verify --workspace <workflow.workspace>
```

- **exit 0** — the fixture tree is byte-identical and the lock is cleared. Continue to Step 3.
- **exit 3** — damage. Show `<workspace>/fixture_guard_report.md`, then restore and re-verify:

  ```bash
  python3 "<CORE>/../skills/experimental/.claude/skills/skill-evals/scripts/fixture_guard.py" \
    repair --apply --workspace <workflow.workspace>
  ```

  Carry the violation into the Step 5 summary as a **finding** — including any `transient-write`
  entry, which repair cannot undo (a file was created inside the fixture and deleted again; the bytes
  are correct but a write reached the fixture). If the report names suspect cases, say plainly that
  those cases' grading is not trustworthy this iteration.

The lock only clears on a clean close, so a skipped verify makes the *next* run refuse to start.
`fixture_guard.json` missing from the workspace means the guard never ran — that is itself the defect.

---

## Step 2c — Collect timing

The workflow cannot time itself — the Workflow runtime has no filesystem access — so the per-run
`timing.json` is written here, from the agent transcripts. Pass the **transcript dir the Workflow tool
reported when you launched it**:

```bash
python3 "<CORE>/../skills/experimental/.claude/skills/skill-evals/scripts/collect_timing.py" \
  --transcript-dir <the "Transcript dir" from the Workflow launch result> \
  --workspace <workflow.workspace>
```

Without this the Time and Tokens rows of `benchmark.md` are structurally `0.0` — `aggregate_benchmark.py`
and `agents/grader.md` both read `timing.json`, and until this step existed nothing wrote it. Exit 3
means no transcript named a run under this workspace, which usually means the transcript dir belongs to a
different run — check it before ignoring it.

---

## Step 3 — Aggregate benchmark

Use the `workspace` and `skill_name` values returned by the workflow. Run from the `skill-evals` directory:

```bash
cd "<CORE>/../skills/experimental/.claude/skills/skill-evals"
python -m scripts.aggregate_benchmark \
  <workflow.workspace> \
  --skill-name <workflow.skill_name>
```

This writes `benchmark.json` and `benchmark.md` to `<workflow.workspace>/`. Show the summary output to the user.

---

## Step 4 — Launch viewer

Use `workflow.workspace`, `workflow.skill_name`, and `workflow.iteration`:

```bash
nohup python "<CORE>/../skills/experimental/.claude/skills/skill-evals/eval-viewer/generate_review.py" \
  <workflow.workspace> \
  --skill-name "<workflow.skill_name>" \
  --benchmark <workflow.workspace>/benchmark.json \
  > /dev/null 2>&1 &
VIEWER_PID=$!
```

For iteration 2+, also pass:
```
--previous-workspace <parent of workflow.workspace>/iteration-<workflow.iteration - 1>
```

Tell the user the viewer is open and ask them to return when done reviewing.

---

## Step 5 — Read feedback

When the user returns, read `<skill-dir>/evals/workspace/iteration-N/feedback.json`:

```json
{
  "reviews": [
    {"run_id": "bloom-filter-with_skill", "feedback": "...", "timestamp": "..."}
  ],
  "status": "complete"
}
```

Empty feedback means the output was fine. Surface patterns and suggest next steps.

Kill the viewer:
```bash
kill $VIEWER_PID 2>/dev/null
```

---

## Notes

- `aggregate_benchmark.py` reads `<eval-name>/with_skill/grading.json` directly — a missing or unparseable grading is a named `ERROR`, recorded in the benchmark's `notes`, and fails the aggregation with exit 2
- The workflow (`run-skill-evals`) owns execution and grading; the skill owns validation (Step 1), aggregation (Step 3), and the viewer (Steps 4–5)
