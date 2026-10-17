---
name: code-review-diff
description: Review code changes from the current branch, staged changes, a git ref, or a diff/patch file. Pure git-native — no platform/PR awareness. Trigger when user says "review this", "review diff", "/aiwork:code-review-diff", or provides a git ref or diff path. Read-only — never posts comments.
disable-model-invocation: true
---

# Code Review

Pure git-native review pipeline. Resolves a diff from git-native inputs, runs the review pipeline, and produces a markdown report.

**Does NOT** check out branches, talk to Azure DevOps / GitHub, or post comments. PR resolution is the caller's job (see Usage).

## Arguments

`$ARGUMENTS` is a space-separated string. Parse out optional flags first, then treat the remainder as the diff source.

| Flag             | Meaning                                      |
| ---------------- | -------------------------------------------- |
| `--rules <path>` | Project rules markdown file.                 |
| `--pr <number>`  | PR / MR id (label only — no platform fetch). |
| `--ticket <id>`  | Ticket / work-item id (label only).          |
| `--name <title>` | Override inferred report title.              |
| `--print`        | Print review to stdout; skip save prompt.    |

Wrappers may pre-pin any of `rules_file`, `pr`, `ticket`, `name` — user-passed flags WIN.

## Input Detection

After flags are stripped, the remainder selects the diff source:

| Form                            | Source                                |
| ------------------------------- | ------------------------------------- |
| empty                           | current branch vs base (master/main)  |
| `staged`                        | `git diff --staged`                   |
| path ending `.diff` or `.patch` | local diff file                       |
| anything else                   | treat as git ref (branch / sha / tag) |

Ambiguous → ask user. Do NOT guess. **Never** treat a bare numeric as a PR id — PR identity is set only via `--pr`.

## Workflow

### 1. Resolve input → diff file path + metadata

#### empty

```bash
base=$(git rev-parse --verify master 2>/dev/null && echo master || echo main)
cur=$(git branch --show-current)
[ "$cur" = "$base" ] && abort "On base branch ($base). Switch to a feature branch."
git diff "$base"...HEAD > "/tmp/code-review-diff-$(date +%s).diff"
files=$(git diff --name-only "$base"...HEAD)
title="$cur"
slug="$cur"
```

#### `staged`

```bash
git diff --staged > "/tmp/code-review-diff-staged-$(date +%s).diff"
files=$(git diff --staged --name-only)
title="staged changes"
slug="staged"
```

#### `.diff` / `.patch` path

Use file as-is. Parse changed files from diff headers (`+++ b/...`).
`slug="$(date +%s)"`.

#### git ref

```bash
git diff "<ref>"...HEAD > "/tmp/code-review-diff-ref-$(date +%s).diff"
files=$(git diff --name-only "<ref>"...HEAD)
title="HEAD vs <ref>"
slug="$(git branch --show-current)"
```

### 1.5. Resolve report metadata

`name` = `--name` ?? `title`. `branch` = `git branch --show-current` (empty for diff-file / detached HEAD). `pr` / `ticket` = flags, empty if unset. Phase 4 omits empty fields.

### 2. Diff size guard

```bash
n=$(wc -l < <(echo "$files"))
```

If `n > 50` → warn user, ask: proceed full / filter to paths / abort.

### 3. Run pipeline

Read `references/pipeline.md` and **execute every phase**. The phase sequence, the lens set chosen by Step 1.4 (kind routing), the scoring pass, and the final Critical/Concerns/Nits format are mandatory — no shortcut to a freeform review, regardless of how small the diff looks. Inline vs. Task-tool fan-out is a perf choice (threshold + kind routing defined in `pipeline.md`); the contract is the steps and the output.

Inputs to pass through:

- `DIFF_FILE`, `CHANGED_FILES` — from step 1
- `TITLE` — `name` from step 1.5
- `BRANCH`, `PR`, `TICKET` — from step 1.5 (may be empty)
- `RULES_FILE` — resolved rules path (may be unset)

### 4. Output

Hold the rendered markdown review in memory. Then choose destination:

- If `--print` is set: print the markdown to stdout. Done.
- Otherwise, ask the user:
  1. Print only (no save) — default
  2. Save to `/tmp/review-<slug>.md`
  3. Other path

Skill produces markdown and stops. Sending it to a PR, a chat, or anywhere else is a follow-up the user runs themselves — this skill never invokes other skills or posts to forges.

## Usage

### Recommended: shell wrapper + worktree (non-destructive)

Run from terminal. Resolve PR id → source branch via platform CLI, then launch Claude in a worktree pinned to that branch. Keeps the user's main working tree untouched.

```bash
#!/usr/bin/env bash
# bin/cr-pr <pr-id>
PR_ID=$1
BRANCH=$(az repos pr show --id "$PR_ID" --query sourceRefName -o tsv | sed 's|refs/heads/||')
claude --worktree "$BRANCH" "/aiwork:code-review-diff --rules .claude/code-review-rules.md"
```

Replace `az repos pr show` with `gh pr view --json headRefName` for GitHub.

### In-session: check out first

Land on the PR's source branch first, then invoke `/aiwork:code-review-diff`. The skill reviews the current branch vs base. For Azure DevOps, `/dev-azdo:pr checkout <id>` does the checkout if that plugin is installed — otherwise check out the source branch with plain `git` first.

### Warning

This skill never checks anything out. Whatever is in cwd is what gets reviewed. If you want PR context but are on the wrong branch, the diff will reflect the wrong starting point.

## Notes

- Read-only. Never posts PR comments. Posting is a separate concern — `dev-azdo:pr` (`comments` op) covers Azure DevOps if that plugin is installed.
- Pipeline detail lives in `references/pipeline.md` — load only when running review.
- No `az`, no `gh`, no PR-id resolution. PR resolution lives outside this skill — in `dev-azdo:pr` when installed, or in a shell wrapper. Absent that, the user checks out the branch themselves; this skill still works.
