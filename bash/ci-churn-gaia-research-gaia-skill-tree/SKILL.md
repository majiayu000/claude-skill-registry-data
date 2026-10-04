---
name: ci-churn
description: >-
  Measure CI churn cost for a pull request: how many commits and how many
  CI-compute seconds were burned on avoidable "fix the CI" push rounds.
  Use when you want to understand the efficiency cost of a PR's iteration
  cycle, get actionable pre-push check suggestions, or include a churn
  summary in a pipeline report. Triggers: "ci churn", "how much CI did we
  burn", "avoidable commits", "ci efficiency", "wasted CI time", "churn
  report", "/ci-churn". Called automatically by /fp-drift at pipeline close.
version: 1.0.0
---

# ci-churn — CI Efficiency Report

Measure how many commits and CI-compute seconds were spent on avoidable
"fix the CI" push rounds for a pull request, and surface the pre-push
checks that would have prevented them.

## When to use

- At the end of any feature pipeline run (`/fp-drift` calls this automatically)
- Standalone after any PR you want to audit for iteration efficiency
- As a retrospective tool: "we spent N minutes of CI compute on churn"

## How it works

### 1. Commit classification

Every commit in the PR is classified by its subject line:

| Label | Pattern examples | Meaning |
|---|---|---|
| `feature` | `feat(...)`, `add ...`, `refactor ...` | Intentional work |
| `review-fix` | `per review`, `address review findings` | Fixed after code review |
| `ci-fix` | `fix import`, `restore export`, `codeql`, `lazy-import`, `wheel smoke` | Fixed because CI caught something locally-detectable |

`feature` commits are the signal. `ci-fix` and `review-fix` are churn.

### 2. CI duration fetch

For each commit SHA, the GitHub Actions API is queried for every workflow
run triggered by that push. Duration is computed as
`updated_at − run_started_at` (no `run_duration_ms` field exists in the API).

### 3. Metrics computed

| Metric | Formula |
|---|---|
| **Churn ratio** | `avoidable_commits / total_commits` |
| **CI compute burned** | Sum of all run durations on avoidable commits |
| **Agent blocked-wait (min)** | Sum of *failed* run durations — the minimum time the agent was blocked waiting for bad results |
| **Agent blocked-wait (max)** | Same as CI compute burned — the agent also waited during the fix runs |
| **Session time** | Parsed from `--session-log` if provided (pi/claude-code JSONL) |

### 4. Root cause hints

Based on which `ci-fix` commit messages matched which patterns, the script
suggests concrete local pre-push checks that would have caught the same
failure before it hit CI.

## Run it

```bash
# Basic — auto-detects repo from git remote
python3 scripts/ci_churn.py <pr-number>

# With session log for agent time estimate (pi or claude-code JSONL)
python3 scripts/ci_churn.py <pr-number> --session-log ~/.pi/sessions/latest.jsonl

# Machine-readable JSON output
python3 scripts/ci_churn.py <pr-number> --json

# Explicit repo
python3 scripts/ci_churn.py <pr-number> --owner myorg --repo myrepo
```

## Reading the output

```
CI Churn Report — PR #1017  (gaia-research/gaia-skill-tree)
════════════════════════════════════════════════════════

Commits: 5 total  (1 feature · 1 review-fix · 3 ci-fix)
Churn ratio: 80.0%  (4 of 5 commits were avoidable)

CI compute burned on avoidable commits : 22m 49s
CI compute on failed runs (all commits): 4m 16s
Agent blocked-wait estimate (min / max): 4m 16s / 22m 49s

Commit breakdown
────────────────────────────────────────────────────────
      SHA  Label         CI (s)  Fails  Message
─────────  ────────────  ──────  ─────  ─────────────────────────────────
5f418b26b  feature            0      0  feat(intake): batch skill intake…
ff99b6165  △ review-fix     187      2  fix(intake): address review findings…
3f3f98776  ⚠ ci-fix         391      1  fix(prWriter): restore open_pr export…
e1b612175  ⚠ ci-fix         398      0  fix(pushFromFile): lazy-import yaml…
78e0028b5  ⚠ ci-fix         393      0  fix(pushFromFile): replace substring…

Suggested local pre-push checks
────────────────────────────────────────────────────────
  • python3 -c "from gaia_cli.main import main"   # import chain smoke test
  • python3 -m pytest tests/ -x -q --timeout=30   # fast local test gate
  • bandit -r src/ -ll                             # security lint (CodeQL class)
```

## Interpreting churn ratio

| Ratio | Signal |
|---|---|
| 0% | Perfect — every commit was intentional feature work |
| 1–20% | Healthy — minor CI surprises, typical for new code paths |
| 20–50% | Elevated — pre-push checks are missing or not being run |
| >50% | High churn — the local development loop is not catching what CI catches |

## Optional: session log integration

If you pass `--session-log PATH`, the script parses `durationMs` (pi) or
`duration_ms` (claude-code) fields from assistant turns in the JSONL log
and reports total agent session time alongside CI compute. This lets you
answer: "of the N minutes this agent spent on this PR, how many were
blocked waiting for CI results on avoidable failures?"

Session log paths:
- **pi:** `~/.pi/sessions/<project>/<session-id>.jsonl` (check `pi session ls`)
- **claude-code:** `~/.claude/projects/<project>/<session-id>.jsonl`

## Notes

- `run_started_at` → `updated_at` delta is used because the GitHub Actions
  API has no `run_duration_ms` field. This slightly over-counts (includes
  queue time), but is consistent across all runs.
- The first commit on a PR branch often has 0 runs because CI hadn't fired
  yet when the PR was opened — this is expected, not a bug.
- `gaia push --from-file`, `gaia dev add`, and pure tooling PRs will
  almost always show 0 feature commits and high churn ratios. That is
  accurate — the entire PR was iteration cost, not new capability.
