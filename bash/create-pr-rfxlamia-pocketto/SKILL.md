---
name: create-pr
description: Opens a GitHub PR for the current branch linked to the Pocket issue (Pocket Enterprise). User-triggered recorder — commits traveling state, formats a structured PR body, discovers or creates the PR, and records it in .pocket-meta.json. Trigger on "create-pr", "open a PR", "create pull request", or when pocket-development offers it after a phase completes in enterprise mode.
---

# Create PR

Standalone Pocket Enterprise skill. Opens (or reuses) a GitHub pull request on the **current branch** for a completed development phase. Pocket does **not** manage git branches — no checkout, create, or switch.

**Core principle:** Recorder only. The PR is created or discovered; warnings (e.g. >20 files) are surfaced but never block. Enforcement stays with CI and the human supervisor.

**Use this when:** Pocket Enterprise is enabled, phase tasks are DONE on the current branch, and you need the structured PR gate (what / why / how-to-test, issue link via `refs` or `closes`).

**Do NOT use when:** Enterprise mode is off — run `pocketto-pi mode` first; this skill will explain and stop.

---

## Invocation

```text
/pocketto:create-pr <plan_dir> [<phase_file>]
```

Examples:

```text
/pocketto:create-pr docs/pocket/plans/2026-06-09-github-trace-loop/
/pocketto:create-pr docs/pocket/plans/2026-06-09-github-trace-loop/ execution-plan/phase-1.md
```

- `<plan_dir>` — directory containing `log.json` and execution plan file(s).
- `<phase_file>` — optional. When omitted, select the unique `log.phases[]` entry with `status == REVIEW`. Zero or multiple REVIEW phases → **STOP** and request an explicit phase file.

---

## Hard Constraints

<HARD-GATE>
1. **NO branch management** — never `git checkout`, `git switch`, `git branch`, or `git worktree` for PR creation. PR opens on whatever branch `git rev-parse --abbrev-ref HEAD` returns.
2. **Traveling state BEFORE `gh pr create`** — `git add -f` + commit `log.json`, plan docs, and spec docs first (no-op if nothing to commit).
3. **Always `--body-file`** — never inline multi-line `gh pr create --body "…"` (cross-shell quoting hazard).
4. **Recorder / non-blocking** — `fileWarning` (>20 files) is surfaced to the user; PR creation still proceeds.
</HARD-GATE>

---

## Preflight

Run ALL steps before any git add or `gh` call.

### Step 1: Enterprise mode

```bash
npx -y pocketto-pi mode --json --contract 2
```

Parse the JSON envelope:

- If `ok` is `false` → **STOP.** Explain the mode error and how to fix Pocket Enterprise config.
- If `data.enterprise` is not strictly `true` → **STOP.** Explain that `create-pr` requires Pocket Enterprise (`pocketto-pi mode init` or a `## Pocket Enterprise` heading in `AGENTS.md`). Do not call `gh`.

### Step 2: gh authentication (skill layer)

```bash
gh auth status
```

If not authenticated → **STOP** with an actionable `gh auth login` error. No partial meta write, no commit, no PR.

### Step 3: Resolve paths

Read `<plan_dir>/log.json` first. Canonical phase identity:

```text
phase_file = phase.file
phase_key  = phase-${phase.order}
```

| Input | Resolution |
|-------|------------|
| `plan_dir` | Absolute path to the plan directory |
| `phase_file` | Explicit arg → resolve to `log.phases[].file` (exact or basename) and require `status == REVIEW`. Omitted → the unique `log.phases[]` entry with `status == REVIEW`. Zero matches → **STOP** ("No phase in REVIEW"). Multiple matches → **STOP** and request an explicit phase file. Never infer from a root `execution-plan.md` or a legacy `execution-plan-phase-N.md` filename. |
| `spec_dir` | `docs/pocket/spec/<slug>/` where `<slug>` matches the plan directory basename (e.g. `2026-06-09-github-trace-loop`) |
| `phase_key` | `phase-${phase.order}` from the resolved `log.json` entry |

Confirm `log.json` exists under `plan_dir`. Use `log.phases[]` order to determine `finalPhase` (last phase in the array).

### Step 4: Linked issue

```bash
npx -y pocketto-pi meta get <spec_dir> github_issue.number --json --contract 2
```

If no issue number → **STOP.** Explain that issue creation must run first (pocket-grinding Story 1 handoff). No PR without a linked issue.

---

## Current Branch

```bash
git rev-parse --abbrev-ref HEAD
```

Record as `<branch>`. This is the **only** branch reference used for PR discovery and creation. Do not change branches.

---

## PR Discovery (idempotent — no duplicates)

**Step A — meta:**

```bash
npx -y pocketto-pi meta get <spec_dir> phases.<phase_key>.github_pr.number --json --contract 2
```

If `data.value` is a positive PR number → fetch URL via `meta get … phases.<phase_key>.github_pr.url` (or `gh pr view <N> --json url`) and report reuse. **Stop** — do not create a duplicate.

**Step B — GitHub by branch (recovery when meta write was lost):**

```bash
gh pr list --head <branch> --json number,url
```

If any PR is returned → reuse the first match, record via [Record PR](#record-pr) below, report reuse. **Stop** — do not create a duplicate.

---

## Commit Traveling State (before `gh pr create`)

Enterprise mode requires `log.json` and plan/spec docs on the PR so pocket-development's phase-level pass can compute per-task SHA scope.

```bash
git add -f <plan_dir>/log.json <plan_dir> <spec_dir>
git diff --cached --quiet || git commit -m "chore(pocket): traveling state for <phase_key>"
```

- Use `git add -f` so gitignored paths (e.g. `log.json` under `docs/`) are included.
- If the index is unchanged after `git add`, skip commit (no-op).
- Push is **not** required by this skill — the recorder commits locally; the user or CI may push. If `gh pr create` needs the branch on the remote, surface that as a prerequisite failure from `gh`, not by branching.

---

## Build PR Body

### Structured input

Write a temp JSON file (Node `fs` — no shell heredocs):

| Field | Source |
|-------|--------|
| `issue` | Issue number from meta (Step 4) |
| `finalPhase` | `true` if this is the **last** phase in `log.json` (or the only phase in a flat plan); `false` for non-final phases in a multi-phase plan |
| `fileCount` | Count of files changed for this phase: `git diff --name-only <phase_baseline>..HEAD` (use `log.json` phase `baseline_sha` or first task's range; dedupe paths) |
| `what` | What this phase delivers — from phase file / task summaries |
| `why` | Why this work — from spec or plan context |
| `howToTest` | Verification steps — from plan acceptance criteria / test commands |

`finalPhase` drives the issue link keyword: `closes #N` (final/sole phase) vs `refs #N` (non-final multi-phase).

### Format and create

```bash
npx -y pocketto-pi format pr --input <pr-input.json> --json --contract 2
```

Parse `data.bodyFile` and `data.fileWarning`.

If `data.fileWarning` is `true` → surface a one-line warning to the user (≤20-file-per-PR rule). **Continue** — non-blocking.

```bash
gh pr create --head <branch> --title "<phase title>" --body-file <data.bodyFile>
```

Derive `--title` from the phase file heading or plan slug. Parse `gh` output for PR number and URL.

---

## Record PR

Only after successful create or reconcile — never before:

```bash
npx -y pocketto-pi meta set <spec_dir> phases.<phase_key>.github_pr.number <N> --json --contract 2
npx -y pocketto-pi meta set <spec_dir> phases.<phase_key>.github_pr.url "<url>" --json --contract 2
```

---

## Completion Report

```
PR_READY: <phase_key>
Branch: <branch>
PR: #<N> <url>
Issue link: <refs|closes> #<issue>
fileWarning: <true|false>
```

If reused (meta or `gh pr list`): report `PR_REUSED` instead of `PR_READY`.

---

## Red Flags

| Thought | Counter |
|---------|---------|
| "I'll create a feature branch first" | **STOP.** This skill never manages branches. PR opens on the current branch. |
| "Skip the traveling-state commit" | **STOP.** Review needs `log.json` + docs on the PR. Commit before `gh pr create`. |
| "23 files — don't open the PR" | Recorder is non-blocking. Warn and create anyway. |
| "I'll inline the PR body" | Always `format pr` → `--body-file`. Deterministic and cross-OS safe. |
| "No issue yet — create PR anyway" | **STOP.** Issue-first is a hard gate. Run pocket-grinding issue creation first. |
