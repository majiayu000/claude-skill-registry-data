---
name: mk:help
description: Workflow navigation assistant. Scans project state (plans, reviews, tests, git) and recommends the next step in the 7-phase pipeline. Use when asked "what should I do next?", "where am I?", "help", or at session start. NOT for domain complexity routing (see mk:scale-routing); NOT for skill discovery (descriptions handle that automatically).
argument-hint: '[--verbose]'
source: local
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
keywords:
  - help
  - command-reference
  - skill-discovery
  - usage-guide
  - onboarding
  - catalog-listing
when_to_use: Use when the user asks for help understanding which skills or commands to use. Surfaces available commands and their purposes.
user-invocable: true
owner: research
criticality: medium
status: active
runtime: claude-code
---

# Navigation Help

Answers "What should I do next?" by scanning project state and mapping to the 7-phase pipeline.

## How It Works

`mk:help` is the FORWARD-looking navigator (what to do next). Backward-looking delivery
analysis stays with `/mk:status` (project-manager) — this skill never reproduces it.

Collect candidates from ALL scan sources below, then RANK them and emit the top 3 — do
NOT stop at the first hit. The rank-1 candidate equals what the old "stop at first
actionable hit" behavior would have returned (back-compat); ranks 2–3 are alternates with
one-line rationale. This skill is read-only: it reads state, never writes it.

### 1. Paused Step-File Workflows
Check `session-state/*-progress.json` for any in-progress step-file workflow.
- Found → "Resume [skill] at step [N]. Run `/mk:[skill]` to continue."

### 2. In-Progress Plans
Check `tasks/plans/` for plan files without matching review verdicts.
- Plan exists, no tests → "Plan approved. Next: run tester agent (Phase 2 — RED)"
- Plan exists, tests failing → "Tests failing. Next: run developer agent (Phase 3 — GREEN)"
- Plan exists, tests passing, no review → "Tests green. Next: run reviewer agent (Phase 4 — Review)"

### 3. Pending Reviews
Check `tasks/reviews/` for verdict files with WARN or action items.
- WARN verdict → "Review has warnings. Acknowledge and approve for Gate 2, or fix findings."
- FAIL verdict → "Review failed. Fix required changes, then re-run reviewer."

### 4. Uncommitted Changes
Check `git status` for staged/unstaged changes.
- Changes exist + review approved → "Ready to ship. Run `/mk:ship` (Phase 5)"
- Changes exist, no review → "Changes detected but no review. Run reviewer first."

### 5. Clean State
No plans, no reviews, no changes.
- "Everything clean. Options: start a new task with planner, run `/mk:retro`, or ask me anything."

## Additional Scan Sources (read after sources 1–5)

ALL four may be absent at rest (e.g. `session-state/checkpoints/` does not exist until
runtime). Absent file → skip silently; note the skip only under `--verbose`. Never error
on a missing source.

| # | Source | Fields to read | Absent-case |
|---|--------|----------------|-------------|
| 6 | `session-state/checkpoints/checkpoint-latest.json` | `state.model_tier`, `progress.plan_path`, `environment.{git_branch,working_dir_clean,uncommitted_changes}`, `budget.{estimated_spent_usd,turn_count}`, `created_at` | skip; no checkpoint context |
| 7 | `session-state/budget-state.json` | `estimated_cost_usd`, `turn_count`, `warnings_emitted` (advisory only) | skip; no budget caution |
| 8 | `session-state/detected-model.json` | `tier` (authoritative current-session tier) | skip; tier unknown |
| 9 | `tasks/reviews/<slug>-verdict.json` | `decision`, `dimensions[].verdict`, `created_at`; `.md` is prose fallback | use git/plan scan only |
| 10 | `docs/development-roadmap.md` (when present; Type-1 allowlisted) | current phase / milestone progress | skip; tag `(CF-C5)` if relied on |

**Model tier:** source the current tier from `session-state/detected-model.json` (written
fresh at SessionStart). Do NOT source `model_tier` from `budget-state.json` — it has no
`created_at`/session marker and may carry a prior session's tier. Treat budget figures as
advisory unless a current-session signal corroborates them.

**Staleness:** if `checkpoint-latest.json` `created_at` is older than 24h, demote its
evidence and note the staleness in the rationale.

## Ranking Heuristic (deterministic, evidence-cited — no vibes ranking)

Collect candidates from all sources, then rank:

1. **Blocked phase or BLOCKED verdict** → rank-1 unblock/fix action. A review verdict is
   blocked when `decision === "BLOCKED"` — the verdict enum is `PASS | PASS_WITH_RISK |
   BLOCKED`; there is NO top-level `"FAIL"` value. `FAIL` exists only per-dimension in
   `dimensions[].verdict`. Cite the failing dimension(s) in the rationale.
2. **In-progress phase** (plan phase `status: in-progress`, or GFM `- [ ]` checkboxes
   remaining) → continue action, rationale cites checkbox % (count `- [x]` vs `- [ ]`).
3. **Approved plan, nothing built** → cook action.
4. **Budget caution:** if `warnings_emitted > 0` OR spent ≥ $30, fold a budget caution into
   the rank-1 rationale (does not by itself create a rank).
5. **Clean state** → the existing fallback table (start a task / retro / ask).

Each candidate's rationale MUST cite the source file(s) it came from.

For skill suggestions based on task type, see `mk:agent-detector` (its `../agent-detector/references/lifecycle-routing.md` maps task patterns to skills).

## State-to-Recommendation Map

> Alias: `/mk:plan` routes to `mk:plan-creator` (slash-command wrapper at `.claude/commands/mk/plan.md`). Subcommands `red-team`, `validate`, `archive` are handled by the same skill.

| State | Pipeline Phase | Recommendation |
|-------|---------------|----------------|
| No plan | Phase 0 → 1 | "Start with `/mk:plan` or describe your task" |
| Existing plan — stress-test | Standalone subcommand | "`/mk:plan red-team {path}` — adversarial review of existing plan" |
| Existing plan — interview | Standalone subcommand | "`/mk:plan validate {path}` — critical question interview on existing plan" |
| Completed/cancelled plans | Housekeeping | "`/mk:plan archive` — archive completed or cancelled plans" |
| Plan approved, no tests | Phase 2 (TDD mode only) | "In TDD mode (`--tdd` / `MEOWKIT_TDD=1`): run tester agent — write failing tests (RED phase). In default mode: skip Phase 2; run developer directly" |
| Tests written, failing | Phase 3 | "Run developer agent — implement to pass tests (GREEN)" |
| Tests passing, no review | Phase 4 | "Run `/mk:review` — adversarial code review" |
| Review PASS/WARN | Phase 5 | "Run `/mk:ship` — commit, PR, deploy" |
| Shipped | Phase 6 | "Run documenter — update docs, then `/mk:retro`" |
| Paused workflow | Resume | "Resume [skill] at step [N]" |
| Mixed state | Clarify | "Multiple items in progress. Which to focus on?" |

## Specialist Skills (surface when domain matches)

| Situation | Skill | When to suggest |
|-----------|-------|----------------|
| Operations, triage, case management, escalation protocols, billing workflows | `/mk:decision-framework` | User asks "how should we handle X cases" or is designing any case-routing system |
| "Is everything green?", pre-review check, post-implementation validation | `/mk:verify` | After implementation completes, before review, or when user wants a quick health check |
| API contract design or review — interface shape, error semantics, compatibility, pagination | `/mk:api-design-principles` | User is authoring or reviewing what an API promises, not how it runs |
| Backend change end to end — handler, service, integration, webhook, job | `/mk:backend-development` | User is changing backend behavior and needs contract, data, and auth owners coordinated |
| Schema, migration, query, index, or ORM data-access boundary | `/mk:database` | User is modelling, evolving, or querying data |
| Infrastructure, containers, CI/CD, deployment safety, rollback | `/mk:devops` | User is changing how the system is built, configured, or delivered |

## Fast Paths (surface these prominently)

Not every task needs the full 7-phase pipeline. Mention these when relevant:

| Situation | Fast Path | What it bypasses |
|-----------|-----------|-----------------|
| Simple bug fix, typo, rename, config tweak | `/mk:fix` | Gate 1 (plan approval) — scope is the plan |
| Task flagged as `one-shot` by scale-routing | Auto Gate 1 bypass | Gate 1 — zero blast radius confirmed |
| Rapid iteration / spike work | `MEOWKIT_HOOK_PROFILE=fast` | post-write scan, pre-ship, pre-task-check, TDD check |

**Quick fix?** Use `/mk:fix` — bypasses Gate 1 for simple changes.

**Small config change?** Scale-routing may auto-bypass Gate 1 when blast radius is zero.

**Hook profiles:** Set `MEOWKIT_HOOK_PROFILE=fast` for rapid iteration (skips non-critical hooks).
Set `MEOWKIT_HOOK_PROFILE=strict` to enable ALL hooks including post-session capture.

## Gotchas

- Multiple in-progress plans create ambiguity — ask user which to focus on, don't guess
- `session-state/` files from previous sessions may be stale — check timestamps, warn if >24h old
- Git status can be noisy (untracked IDE files) — focus on files in `src/`, `lib/`, `app/`, `tests/`
- Don't recommend skipping phases — even if the user seems impatient, show the full path
- Fast paths are not loopholes — Gate 2 (review) is NEVER bypassed; security hooks are NEVER skipped
- `session-state/checkpoints/` does not exist until runtime — its absence is normal, not an error; skip silently
- `budget-state.json` is missing at session start — treat budget figures as advisory; never source model tier from it (use `detected-model.json`)
- Prefer the machine-readable `*-verdict.json` over the `.md` prose verdict; a verdict is blocked when `decision === "BLOCKED"` (never a top-level `"FAIL"`)
- This is the forward-looking navigator — backward-looking delivery status stays with `/mk:status`; do not duplicate it here

## Output Format

The ranked next-steps are a JSON-compatible shape (documented here for downstream tooling),
rendered as a concise human summary. This skill does NOT emit machine JSON itself — there is
no scanner script; the shape documents what the ranking reasons about.

```json
{
  "next_steps": [
    {
      "rank": 1,
      "action": "/mk:cook tasks/plans/260610-x/plan.md",
      "priority": "high",
      "rationale": "Plan approved (Gate 1), phase-02 in-progress at 3/7 checkboxes; budget $4.20 of $30",
      "source": ["tasks/plans/260610-x/phase-02-*.md", "session-state/budget-state.json"]
    }
  ],
  "progress": { "plan": "260610-x", "phases_done": 1, "phases_total": 6, "checkbox_pct": 43 }
}
```

Human rendering (same headings as before — rank-1 is "Recommended Next Step"):

```
## Status

**Current phase:** [Phase N — Name]
**State:** [brief description]

### Recommended Next Step
[rank-1 action] — [rationale]

### Other Options
- [rank-2 action] — [one-line rationale]
- [rank-3 action] — [one-line rationale]
```

If `--verbose` flag: also show full state scan results (plan files, review files, test
status, git status) AND which additional sources (6–10) were present vs skipped.
