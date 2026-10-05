---
name: pocket-closing
description: Terminal pocket stage. User invokes after pocket-development's phase-level pass writes verdicts. Reconciles reviews against log.json, gates on REVIEW_FAIL/REVIEW_BLOCKED, advances REVIEW→DONE, runs `log close`, and emits a closeout summary. Trigger on "pocket-closing", "close the plan", "close out", "finalize plan", or when a plan is fully reviewed and all verdicts pass.
---

# Pocket Closing

The terminal stage of the Pocket pipeline. Invoked directly by the user after pocket-development's phase-level pass has written verdicts for a phase or flat plan. It reconciles those verdicts against the execution log, gates closure on review results, advances state, and produces the closeout artifact that ends the plan.

**Core principle:** Verdicts decide. pocket-closing never re-reviews and never improvises a close — it reads what pocket-development's phase-level pass wrote and translates it into an accept-and-close or a block. No clean verdict, no close.

## Position in Pocket Bundle

```text
pocket-grinding → pocket-planning → pocket-structuring → pocket-development → POCKET-CLOSING
                                                                                    ↑
                                                                  User invokes directly after
                                                                  pocket-development's phase-level pass
                                                                  reaches REVIEW on all tasks passing
```

pocket-closing is always invoked **directly** by the user (`/pocketto:pocket-closing <path>`) — pocket-development never auto-chains to it. When a phase passes with all `REVIEW_PASS`, the phase-level pass advances the phase to `REVIEW` and emits a `PHASE_COMPLETE` handoff naming pocket-closing as the next step; the user then runs it. pocket-closing owns the close from scratch: the phase-level pass deliberately does NOT update `log.json` ("leave to user or pocket-closing"), so this skill still runs its full preflight, verdict gate, freshness check, and `log close`. pocket-development names `log.json` as "pocket-closing's primary input." This skill is where the loop actually closes.

## Invocation

```text
/pocketto:pocket-closing <path-to-execution-plan-or-plan-dir>
```

Examples:
```text
/pocketto:pocket-closing docs/pocket/plans/2026-06-03-typing-dna/
/pocketto:pocket-closing docs/pocket/plans/2026-05-28-auth/execution-plan/phase-2.md
```

## Main Agent Role (HARDENED)

Main agent = **Reconciler + Closer only**. Does NOT review code.

| Main agent MUST | Main agent MUST NOT |
|-----------------|---------------------|
| Read log.json and every reviews/*.json | Read implementation files or assess code |
| Reconcile each reviewable task to its verdict | Re-run, re-interpret, or override a review verdict |
| Gate close on REVIEW_FAIL / REVIEW_BLOCKED | Close a plan with any failing or missing verdict |
| Advance phases via `pocketto-pi log` CLI | Hand-edit log.json (CLI is the only writer) |
| Run `log close` and write closeout.md | Mark a task DONE or re-touch any `done_sha` |
| Emit a structured CLOSED / PHASE_ADVANCED / CLOSE_BLOCKED report | Silently block — every block names what, why, unblock |

## Preflight

Run ALL steps before changing any state. Failure in steps 1–3 → `CLOSE_BLOCKED` immediately.

### Step 1: Resolve plan_dir and the unique REVIEW target

Canonical phase identity (always from `log.json`, never from a legacy filename):

```text
phase_file = phase.file
phase_key  = phase-${phase.order}
```

Resolve the target phase:

```text
If invoked with a file path:
  if parent dir is 'execution-plan', plan_dir = grandparent dir; else plan_dir = parent dir
  Read log.json
  Resolve the file to the unique log.phases[] entry (exact phase.file, else basename)
  Require that phase.status == REVIEW
    else CLOSE_BLOCKED: "Phase <file> is <status>, not REVIEW."
  target = that phase
  Never target WAITING, BLOCKED, or already-DONE phases for advancement

If invoked with a dir path:
  if dir ends with 'execution-plan', plan_dir = parent dir; else plan_dir = dir
  Read log.json
  targets = phases where status == REVIEW
  0 matches  → CLOSE_BLOCKED: "No phase in REVIEW. Run pocket-development's phase-level pass first."
  >1 matches → CLOSE_BLOCKED: "Multiple phases in REVIEW: <files>. Re-run with an explicit phase file."
  1 match    → target = that phase
```

Directory input therefore advances only the current REVIEW phase. For a normal
multi-phase plan (Phase 1 `REVIEW`, Phase 2 `WAITING`), `/pocketto:pocket-closing <plan_dir>`
targets Phase 1, yields `PHASE_ADVANCED`, and leaves Phase 2 untouched.

Also derive `spec_dir` (used by the enterprise reads in E2 and E5), mirroring create-pr:

```text
spec_dir = docs/pocket/spec/<slug>/ where <slug> matches the plan directory basename
```

`.pocket-meta.json` lives under `<spec_dir>` (every writer — create-pr, pocket-grinding — writes it there), so the enterprise reads below resolve it from `spec_dir`, not `plan_dir`. `log.json`, `reviews/`, and `closeout.md` stay under `<plan_dir>`.

### Step 2: Read log.json

```text
<plan_dir>/log.json
```

Verify:
- File exists → else `CLOSE_BLOCKED: "log.json not found at <path>. Run pocket-development first."`
- `header` present with `status` and `phases[]` → else `CLOSE_BLOCKED: "log.json malformed: <field> missing"`
- Header `status` is `IN_PROGRESS` → if already `DONE`, report `ALREADY_CLOSED` and stop (idempotent, no re-close)

### Step 3: Load review verdicts and reconcile

```bash
ls <plan_dir>/reviews/
```

Read every `reviews/<task_id>-review.json`. For each reviewable task in each target phase (the same task set the phase-level pass computed — `status == DONE` with a non-null `done_sha`):

| Condition | Reconciliation |
|-----------|----------------|
| `DONE` + `done_sha` + review file **current for that `done_sha`** | Reviewable — record its `overall` verdict |
| `DONE` + `done_sha` + review file **stale** (predates the current `done_sha`) | `CLOSE_BLOCKED` — "T{id} verdict is stale: reviewed before the current done_sha. Re-run pocket-development's phase-level pass." |
| `DONE` + `done_sha` but NO review file | `CLOSE_BLOCKED` — "T{id} has no verdict. Run pocket-development's phase-level pass before closing." |
| Task is not `DONE` / missing `done_sha` | Not reviewable — was skipped by the phase-level pass; note and exclude from the gate |
| `reviews/` dir absent or empty | `CLOSE_BLOCKED` — "No reviews found. Run pocket-development's phase-level pass first." |

**Freshness check (mandatory).** A review proves a verdict only for the SHA it actually reviewed. If a task was corrected after review, the old verdict lingers — closing on it would accept code that was never reviewed at the current boundary. For each reviewable task `T`, compute:

```
latest_owned_sha(T) = max-by-commit-time of:
    { T.done_sha }
    ∪ { c.sha : c ∈ phase.corrections and T ∈ tasks(c) }

where tasks(c) = ({ c.for_task } if present) ∪ { owner[f] : f ∈ c.files and owner[f] is defined }
      owner[f]  = the task whose original done-range (prev..done_sha, in plan order) last touched f
```

This is **the identical attribution set the phase-level pass uses** (Task 4), so `reviewed_sha(T)` written by the phase-level pass equals `latest_owned_sha(T)` by construction. The set MUST include corrections where `c.for_task == T` even when no file `c` touches is owned by `T`; using owner-only attribution here would make a `for_task` correction invisible to closing and produce a permanent `CLOSE_BLOCKED` for that task.

The verdict is current iff `reviews/<T>-review.json`.`reviewed_sha == latest_owned_sha(T)` (exact SHA match). If any correction attributed to `T` is newer than its review — meaning `reviewed_sha` lags behind `latest_owned_sha(T)` — the verdict is stale → `CLOSE_BLOCKED: "T{id} verdict is stale: a correction changed its files after review. Re-run pocket-development's phase-level pass."`.

**Fallback (legacy reviews only).** If `reviewed_sha` is absent from the review file (older reviews predating this template change), fall back to the timestamp proxy: run `git show -s --format=%cI <latest_owned_sha(T)>` and require the review `timestamp` to be at or after that commit time. This path is a compatibility shim — any review produced after Task 4 lands will carry `reviewed_sha` and use the exact-match path above.

Reconciliation details, REVIEW_BLOCKED stub handling, and observation extraction: load `references/verdict-reconciliation.md`.

## Gate on Verdicts

A phase may advance ONLY when every reviewable task in it is `REVIEW_PASS`.

| Any task verdict | Action |
|------------------|--------|
| `REVIEW_FAIL` | `CLOSE_BLOCKED`. Print each failing task's `fix_instructions` verbatim. Fix → re-run pocket-development's phase-level pass → re-run pocket-closing. |
| `REVIEW_BLOCKED` with `blocked_category: "auditor-unavailable"` | `CLOSE_BLOCKED`. Infrastructure block — re-run pocket-development on the blocked task(s); do NOT print `ESCALATE:` instructions. |
| `REVIEW_BLOCKED` with `blocked_category: "audit-failed"` or `fix_instructions` starting with `ESCALATE:` | `CLOSE_BLOCKED`. Print the escalation `fix_instructions`. Resolve the escalation before closing. |
| `REVIEW_BLOCKED` with no `blocked_category` and no `ESCALATE:` prefix | `CLOSE_BLOCKED`. Stale/incomplete stub — re-run pocket-development's phase-level pass; do not close. |
| all `REVIEW_PASS` | Phase passes the gate — proceed to Advance State. |

The **current** per-task verdict decides the gate — an old `REVIEW_FAIL` superseded by a newer `REVIEW_PASS` (advanced `reviewed_sha`, `overall == REVIEW_PASS`) passes cleanly. The gate reads the current `reviews/<T>-review.json`, not any historical state.

Non-blocking observations (`stage_2` Minor issues, strengths, out-of-scope notes on PASSing tasks) do NOT block. Collect them — they go into the closeout summary as "carried forward."

## Enterprise Mode (opt-in): Approval Gate (E0)

Runs **after** the verdict gate passes and **before** any `log.json` mutation (Advance State / Close). This is the formal sign-off gate: with it on, a plan cannot close until a human approved the PR.

1. Detect mode:
   ```bash
   npx -y pocketto-pi mode --json --contract 2
   ```
   If `ok: false`, or `data.enterprise` is not `true`, or `data.require_approval` is not `true` → **skip this gate entirely** (proceed to Advance State). Non-enterprise runs and enterprise runs without `require_approval` are byte-identical to today.
2. Discover the target phase's PR — `phase_key = phase-${target.order}` from `log.json`, then
   ```bash
   npx -y pocketto-pi meta get <spec_dir> phases.<phase_key>.github_pr.number --json --contract 2
   ```
   falling back to `gh pr list --head "$(git rev-parse --abbrev-ref HEAD)" --json number --jq '.[0].number // empty'`.
   If no PR is found → **STOP** with state `APPROVAL_PENDING`: `require_approval` is explicitly configured, so a missing PR is a gate failure, not a skip (fail-closed). Tell the user to run `/pocketto:create-pr <plan_dir> <phase_file>` first.
3. Check the review decision:
   ```bash
   gh pr view <pr_number> --json reviewDecision
   ```
   - `reviewDecision == "APPROVED"` → gate passes; proceed to Advance State.
   - Anything else (`REVIEW_REQUIRED`, `CHANGES_REQUESTED`, empty) → **STOP** with state `APPROVAL_PENDING` and no `log.json` change:
     ```text
     APPROVAL_PENDING — PR #<N> is not APPROVED (<reviewDecision>).
     Ask a supervisor to review and approve the PR, then re-run:
     /pocketto:pocket-closing <plan_dir>
     ```

The gate reads GitHub; it never writes. Re-running pocket-closing after approval proceeds normally.

## Advance State

Advance the **target** phase `REVIEW → DONE` at the phase level only (`<phase_file>` = `target.file` from `log.json`):

```bash
npx -y pocketto-pi log update <plan_dir> <phase_file> DONE --json --contract 2
```

[CRITICAL] Phase-level update only. NEVER pass `--task` here — task `DONE` recomputes `done_sha` from current HEAD and would corrupt the review's SHA range. Tasks were already marked DONE by pocket-development; leave them untouched. Correction commits are recorded by pocket-development's phase-level pass (via `pocketto-pi log update --correction`), never by closing — this rule is unaffected by the correction cycle.

Parse the envelope, confirm `ok: true` and `data.newStatus == "DONE"` before continuing.

## Close

Attempt the close once the target phase is `DONE`:

```bash
npx -y pocketto-pi log close <plan_dir> --json --contract 2
```

`log close` verifies **every** phase in the plan is `DONE`. Read the envelope:

| Result | Meaning | pocket-closing output |
|--------|---------|----------------------|
| `ok: true`, `data.status == "DONE"` | All phases DONE → header set to `DONE` + `date_completed` | `CLOSED` — write closeout.md, emit final report |
| `ok: false`, code `PHASES_NOT_DONE` | Other phases still `WAITING`/`REVIEW` (multi-phase plan not finished) | `PHASE_ADVANCED` — the REVIEW target is DONE; name the next phase to run. Do NOT treat the non-zero exit as an error. |

`PHASE_ADVANCED` is the normal mid-pipeline state for phased plans: you advanced one phase, the plan continues. Point the user back to pocket-development for the next phase.

## Enterprise Mode (opt-in): Closeout

This section runs **only** when enterprise mode is active **and** the plan reached `CLOSED` (all verdicts clean, `log close` succeeded). Non-enterprise runs skip it entirely — the skill behaves exactly as today.

### Step E1: Detect enterprise mode

```bash
npx -y pocketto-pi mode --json --contract 2
```

Parse the envelope. If `ok: false` or `data.enterprise` is not `true` → **skip this entire section** (proceed directly to Closeout Summary). Fail-closed: no GitHub calls in non-enterprise mode, ever.

### Step E2: Read linked issue from `.pocket-meta.json`

```bash
npx -y pocketto-pi meta get <spec_dir> github_issue.number --json --contract 2
```

If `data.value` is `null` or missing → emit warning: `"Enterprise closeout skipped: no linked issue in .pocket-meta.json."` → proceed to Closeout Summary (no GitHub call).

### Step E3: Build closeout body via CLI

Write the closeout input to a temp JSON file:

```json
{ "slug": "<plan-slug>", "issue": <issue-number>, "phases": <phase-count> }
```

Then:

```bash
npx -y pocketto-pi format closeout --input <tmp.json> --json --contract 2
```

Parse `data.bodyFile` from the envelope.

### Step E4: Post closeout comment

```bash
gh issue comment <issue-number> --body-file <bodyFile>
```

**[CRITICAL] Do NOT call `gh issue close`.** The issue closes when the supervisor **merges** the final PR (`closes #<issue>` in the PR body). Merge is the human gate — Pocket never closes the issue directly.

### Step E4b: Refresh the task checklist comment

Bring the issue's task-checklist comment (written by pocket-development at PHASE_COMPLETE) up to final state so the issue shows every phase DONE:

```bash
npx -y pocketto-pi format tasklist <plan_dir> --json --contract 2
```

Parse `data.bodyFile` and `data.marker` (`<!-- pocket-tasklist -->`), then upsert exactly one marker-tagged comment on issue `<issue-number>` — list comments via `gh api repos/<owner>/<repo>/issues/<issue-number>/comments --paginate`, filter to bodies starting with the marker, create if none / PATCH the earliest if found (delete later duplicates). If this step fails (e.g. `gh` hiccup), emit a one-line warning and continue — the closeout itself already succeeded.

### Step E5: Discover linking PR number

Canonical identity from the target `log.json` phase: `phase_file = target.file`, `phase_key = phase-${target.order}`. The PR number is written by create-pr at the phase-nested path, so read it there:

```bash
npx -y pocketto-pi meta get <spec_dir> phases.<phase_key>.github_pr.number --json --contract 2
```

If `data.value` is non-null → use it as the PR number. Otherwise, fall back to branch discovery:

```bash
branch=$(git rev-parse --abbrev-ref HEAD)
gh pr list --head "$branch" --json number --jq '.[0].number // empty'
```

If no PR number is found by either method → emit warning: `"Enterprise closeout: could not determine linking PR number — skipping merge-state check."` → skip to Closeout Summary (the closeout comment was still posted).

### Step E6: Check linking PR merge state

```bash
gh pr view <pr-number> --json state,merged
```

If `merged` is `false` → the closeout comment has been posted, but emit this warning:

```text
⚠️  The linking PR (#<pr-number>) is not yet merged.
    The issue will close when the supervisor merges this PR.
```

## Closeout Summary

On `CLOSED` only, write `<plan_dir>/closeout.md` — the artifact that ends the plan. Load `references/closeout-summary-template.md` for the exact format. It records, per phase: each task, its `done_sha`, its verdict, and the observations carried forward; plus header dates and the final SHA range.

Then emit the terminal report:

```text
PLAN CLOSED — <plan_dir>
──────────────────────────────────────────
Phases : N — all DONE
Tasks  : M reviewed — all REVIEW_PASS
Closed : <date_completed>
Carried forward: K non-blocking observations (see closeout.md)
──────────────────────────────────────────
Closeout: <plan_dir>/closeout.md
```

## Output States

| State | Meaning |
|-------|---------|
| `CLOSED` | All phases DONE, header `DONE` + `date_completed`, closeout.md written |
| `PHASE_ADVANCED` | Reviewed phase advanced to DONE; other phases remain — plan continues |
| `CLOSE_BLOCKED` | Preflight failed, a verdict is missing, or a task is REVIEW_FAIL/REVIEW_BLOCKED |
| `APPROVAL_PENDING` | Enterprise `require_approval: true` and the phase PR is missing or not APPROVED — no `log.json` change; approve the PR and re-run |
| `ALREADY_CLOSED` | Header already `DONE` — idempotent no-op |

## Iron Laws

```text
1. NO CLOSE WITH A FAILING VERDICT
   Any REVIEW_FAIL or REVIEW_BLOCKED in a target phase → CLOSE_BLOCKED.
   WHY: Closing translates review results into an accept decision.
   Closing over a failure ships unreviewed-bad code as "done".

2. NO CLOSE WITHOUT A CURRENT VERDICT
   Every reviewable task (DONE + done_sha) must have a review file whose
   verdict was produced for that exact done_sha — not an earlier one.
   WHY: A DONE task with no verdict, or one whose code changed after the
   review, was never reviewed at the SHA being closed. Closing it asserts
   a review that did not happen.

3. NO CODE READING BY MAIN AGENT
   pocket-closing reconciles verdicts; it never re-reviews implementation.
   WHY: Re-reviewing duplicates pocket-development's phase-level pass and invites the main agent
   to override an independent verdict with its own judgment.

4. NO MANUAL log.json EDIT
   Only `pocketto-pi log` writes log.json. Never hand-edit it.
   WHY: The CLI keeps the schema, SHAs, and dates consistent and is the
   single source of state transitions across the bundle.

5. NO SILENT BLOCK
   Every CLOSE_BLOCKED states: what blocked, why, what would unblock.
   WHY: "Can't close" without a reason creates deadlock.
```

## Sample log.json — Before and After

**Before** (the canonical end state pocket-development's phase-level pass leaves — flat plan, all passed, still open):

```json
{
  "header": {
    "plan_dir": "docs/pocket/plans/2026-06-03-typing-dna",
    "plan_type": "flat",
    "status": "IN_PROGRESS",
    "date_started": "2026-06-03",
    "date_completed": null,
    "baseline_sha": "abc1234"
  },
  "phases": [
    {
      "order": 1,
      "file": "execution-plan/index.md",
      "status": "REVIEW",
      "tasks": [
        { "id": "T1", "name": "Capture keystroke timing", "status": "DONE", "done_sha": "bcd2345" },
        { "id": "T2", "name": "Derive dwell features",     "status": "DONE", "done_sha": "cde3456" }
      ]
    }
  ]
}
```

reviews/T1-review.json → `REVIEW_PASS`, reviews/T2-review.json → `REVIEW_PASS`.

**After** pocket-closing (gate passes → phase DONE → `log close`):

```json
{
  "header": {
    "plan_dir": "docs/pocket/plans/2026-06-03-typing-dna",
    "plan_type": "flat",
    "status": "DONE",
    "date_started": "2026-06-03",
    "date_completed": "2026-06-04",
    "baseline_sha": "abc1234"
  },
  "phases": [
    { "order": 1, "file": "execution-plan/index.md", "status": "DONE", "tasks": [ /* unchanged */ ] }
  ]
}
```

Plus `closeout.md` written to the plan dir. Output state: `CLOSED`.

## Reference Triggers

| Reference | When to Load |
|-----------|--------------|
| `references/verdict-reconciliation.md` | Mapping tasks↔verdicts, REVIEW_BLOCKED stubs, extracting carried-forward observations, edge cases |
| `references/closeout-summary-template.md` | Writing closeout.md — exact section structure and a filled example |
