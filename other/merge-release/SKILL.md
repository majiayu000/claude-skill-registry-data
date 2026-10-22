---
name: merge-release
category: release-management
model: claude-haiku-5-5
userInvocable: true
description: Merge an approved release PR into its target branch. Takes the release branch or the version it is for. Validates approval/checks/conflicts via gh, then merges. Step 3 of the release workflow.
argument-hint: "[release-branch | version]"
allowed-tools: "Bash(pwd:*), Bash(echo:*), Bash(git rev-parse:*), Bash(git branch:*), Bash(git fetch:*), Bash(bash:*), AskUserQuestion"
---

# Merge Release PR Command

> Workflow: `/create-release-branch` → `/create-release` → **`/merge-release`** → `/release`

## Usage

```bash
/merge-release                      # lists open release PRs to pick from
/merge-release release/v1.2.0       # by release branch
/merge-release v1.2.0               # by version — resolves to release/v1.2.0
```

Takes either form, or neither. With no argument it does **not** read the branch
you are on — it lists the open release PRs and asks you to choose.

## Context

Working directory: !`pwd`

Current branch: !`git branch --show-current 2>/dev/null || echo "(not in a git repository)"`

Available release branches: !`git branch -a --list 'release/*' 'origin/release/*' 2>/dev/null || echo "(no release branches)"`

Arguments provided: $ARGUMENTS

**Release terminology** — see `${CLAUDE_PLUGIN_ROOT}/shared/release-concepts.md`.

## Your Task

Thin dispatcher over `${CLAUDE_PLUGIN_ROOT}/shared/release/pr-merge.sh`. Do not re-derive validation logic in prose — call the script and surface its structured output. Pause only for the confirmations the steps below ask for.

### Step 0 — Pre-flight: verify git repo

```bash
git rev-parse --is-inside-work-tree 2>/dev/null
```

If non-zero, stop with the standard "not in a git repository" message instructing the user to `cd` into a service repo.

### Step 1 — Parse arguments

```bash
bash "${CLAUDE_PLUGIN_ROOT}/shared/release/parse-args.sh" \
  --skill=pr-merge --json -- $ARGUMENTS
```

Outcomes:
- **Exit 0** — `release_branch` populated; proceed.
- **Exit 10** — `missing` contains `release_branch`. Go to **Step 2** (interactive selection).
- **Exit 20** — show errors and stop.

### Step 2 — Interactive selection (no arg supplied)

List open release-labeled PRs:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/shared/release/pr-merge.sh" --list --json
```

If the array is empty, stop with: "No open release PRs found. Run /create-release first."

Otherwise use AskUserQuestion to present up to 4 PRs as options (label: `#<n> <headRefName> → <baseRefName>`, description: title) — the tool shows no more than 4; with more PRs, name the rest in the question text so the user can type one. The user picks one; remember its `headRefName` as `release_branch`.

### Step 3 — Plan: show PR state and gates

```bash
bash "${CLAUDE_PLUGIN_ROOT}/shared/release/pr-merge.sh" \
  --release-branch=<release_branch> --plan --json
```

The output JSON has:
- `pr` — number, title, url, state, mergeable, reviewDecision (raw `statusCheckRollup` is stripped — already aggregated below)
- `gates` — `approved`, `no_conflicts`, `checks_passing`, `checks_running`, `ready`
- `failing_checks[]` — slim `{name, conclusion}` per failed check, used to name what failed
- `running_checks_count` — count of checks still pending/in-progress (no per-check detail)
- `blocking_issues` — human-readable list of why it's not ready (empty when ready)

Render a short summary to the user (one section per gate, ✓ / ✗).

If `pr.state == "MERGED"`, congratulate the user and stop — there is nothing to do.

If `pr.state == "CLOSED"`, surface the URL and stop.

### Step 4 — Decide whether to merge

If `gates.ready == true`, use AskUserQuestion to confirm: **Merge PR #N now? [y/n]**. Also ask whether to delete the release branch after merge (pass `--delete-branch` on apply if yes).

If `gates.ready == false`, surface `blocking_issues` and AskUserQuestion to ask the user how to proceed. Valid options depend on which gate failed:

| Failed gate              | Allowed user choices                                                            |
|--------------------------|---------------------------------------------------------------------------------|
| `no_conflicts == false`  | Abort only — conflicts must be resolved on the branch first.                    |
| `checks_running`         | Abort, or wait and re-run `/merge-release`.                                     |
| `checks_passing == false`| Abort, view details (`gh pr checks <n>`), or merge anyway (override).           |
| `approved == false`      | Abort, or merge anyway (override; review-required is a soft gate).              |

When the user opts to override, pass the relevant flag(s) to apply: `--allow-unapproved`, `--allow-failing-checks`. **Conflicts cannot be overridden** — direct the user to resolve them and re-run.

### Step 5 — Apply

```bash
bash "${CLAUDE_PLUGIN_ROOT}/shared/release/pr-merge.sh" \
  --release-branch=<release_branch> --apply --json \
  [--allow-unapproved] [--allow-failing-checks] [--delete-branch]
```

The merge happens server-side (GitHub API) — no `git push` is issued, so the audit-gate hook does not apply.

If apply exits non-zero, surface stderr verbatim and stop.

### Step 6 — Report

On success:

```
✓ Release PR Merged
  PR:     #<n> <title>
  branch: <head> → <base>

Next:
  /release        # tag + GitHub release
```

## Important Notes

- **No extra round-trips** — run the steps straight through, pausing only for the confirmations they ask for; use parallel tool calls where independent.
- **No re-derived gh commands in prose** — every gh call goes through `pr-merge.sh`, including the Step 2 listing.
- **No audit recording needed** — the merge and optional branch deletion are server-side via the GitHub API.
