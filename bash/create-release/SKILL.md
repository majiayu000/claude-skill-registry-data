---
name: create-release
category: release-management
model: claude-haiku-5-5
userInvocable: true
description: Push a release branch and open a PR to the target branch. Takes an optional target branch and version. Step 2 of the release workflow — runs after branching, before merging.
argument-hint: "[target-branch] [version]"
allowed-tools: "Bash(pwd:*), Bash(echo:*), Bash(git rev-parse:*), Bash(git branch:*), Bash(git fetch:*), Bash(git log:*), Bash(git remote:*), Bash(bash:*), Bash(gh pr list:*), Bash(gh pr view:*), AskUserQuestion, Write"
---

# Create Release PR Command

> Workflow: `/create-release-branch` → **`/create-release`** → `/merge-release` → `/release`

## Usage

```bash
/create-release                     # prompts for the version
/create-release master              # explicit target branch
/create-release master v1.2.0       # explicit target and version
```

Both arguments are optional. The target defaults to the repo's default branch.
The version is **not** inferred from the branch you are on — with none supplied
the parser reports it missing, `version-suggest.sh` proposes one from the repo's
release tags/branches and the commits since, and you pick.

## Context

Working directory: !`pwd`

Current branch: !`git branch --show-current 2>/dev/null || echo "(not in a git repository)"`

Available branches: !`git branch -a --list 'master' 'main' 'develop' 'release/*' 'origin/master' 'origin/main' 'origin/release/*' 2>/dev/null || echo "(no branches)"`

Arguments provided: $ARGUMENTS

**Release terminology** — see `${CLAUDE_PLUGIN_ROOT}/shared/release-concepts.md`.

## Your Task

Thin dispatcher over `${CLAUDE_PLUGIN_ROOT}/shared/release/`. Use parallel tool calls where steps are independent; pause only for the confirmations the steps below ask for. Do not re-derive parsing, ref resolution, ticket extraction, or gh-CLI mechanics — call the scripts and surface their structured output.

### Step 0 — Pre-flight: verify git repo

```bash
git rev-parse --is-inside-work-tree 2>/dev/null
```

If non-zero, stop with the standard "not in a git repository" message instructing the user to `cd` into a service repo.

### Step 1 — Parse arguments

```bash
bash "${CLAUDE_PLUGIN_ROOT}/shared/release/parse-args.sh" \
  --skill=pr-create --json -- $ARGUMENTS
```

Outcomes:
- **Exit 0** — `target` and `version`/`release_branch` populated; proceed.
- **Exit 10** — `missing` contains `version`. Run `bash "${CLAUDE_PLUGIN_ROOT}/shared/release/version-suggest.sh" --json` and use AskUserQuestion to pick. Re-run parser with the chosen version. `version-suggest.sh` fetches remote tags first so the suggestion reflects the authoritative tag set; **watch its stderr** — if it emits a `[stale-tags]` or `[no-remote]` marker, surface that to the user before presenting the recommendation (the version may be based on stale local tags). Do not block on the marker; continue.
- **Exit 20** — surface errors and stop.

### Step 2 — Gather commit data

`commits-data.sh` self-fetches both refs from origin and prefers `origin/<ref>` during resolution, so a stale local release branch will not mask real upstream commits. No manual `git fetch` needed.

```bash
bash "${CLAUDE_PLUGIN_ROOT}/shared/release/commits-data.sh" \
  --base=<target> --head=<release_branch> --json
```

The output JSON has:
- `commit_count` — true count across the full range
- `commits_returned`, `truncated` — how many entries `commits[]` actually holds; `true` when the range exceeds `--limit` (default 500). Aggregates are full-range; only `commits[]` is sliced (oldest dropped). When `truncated`, disclose "showing N of M commits" in the PR body.
- `file_count`
- `tickets[]` — uppercased, deduped ticket IDs (e.g. `JIRA-123`)
- `breakdown` — counts by conventional-commit type (`feat`, `fix`, `chore`, …)
- `has_breaking_change`
- `commits[]` — per-commit `{short, subject, type, scope, tickets, breaking}` (full sha is intentionally omitted; `short` is what release notes render and GitHub auto-links)

If `commit_count == 0`, stop with: "No commits to release — release branch matches the target."

### Step 3 — Author PR title and body

The shell library does **not** generate the PR body. That is your job.

**Title**: defaults to `Release <version>` (the script will use this if you pass `--title=""` or omit it). Override only if the user asked for something custom.

**Body**: write a concise, well-organized markdown PR body using the JSON from Step 2. A good shape:

```markdown
## Release v1.2.0

<one-paragraph summary derived from breakdown — e.g. "12 commits: 4 feat, 6 fix, 1 chore. No breaking changes.">

## Tickets

- JIRA-123, JIRA-456 …

## Highlights

- **feat(api)**: <subject from a feat commit>
- **fix(ui)**: <subject from a fix commit>
- (group by type, surface the most user-visible items)

## Commits

- abcd123 feat(api): subject — JIRA-123
- (full list, oldest-first or newest-first; pick whichever reads better)

## Testing checklist

- [ ] Manual smoke test
- [ ] Release notes reviewed
- [ ] Breaking changes documented (if any)
```

If `has_breaking_change` is true, surface it prominently at the top.

Write the body to a tempfile under `.claude/session-state/` (or `/tmp/` if the workspace path isn't available):

```bash
# Use the Write tool to create the file at e.g.
#   .claude/session-state/release-pr-body-<version>.md
```

### Step 4 — Plan: validate via pr-create.sh

```bash
bash "${CLAUDE_PLUGIN_ROOT}/shared/release/pr-create.sh" \
  --target=<target> --release-branch=<release_branch> \
  --plan --json
```

The output reports:
- `existing_pr` — non-null if an open PR exists for this head branch
- `will_push_branch` (bool) — apply will run `git push -u origin <release_branch>` first
- `will_update_existing` (bool) — apply will edit the existing PR rather than create a new one (requires `--update-existing`)
- `will_refuse_existing` (bool) — apply would refuse because a PR is already open and `--update-existing` was not passed

Show the plan summary to the user. If `existing_pr.state == "OPEN"`, surface the URL and use AskUserQuestion to ask whether to **update** that PR (re-run apply with `--update-existing`) or abort.

### Step 5 — Confirm and apply

Use AskUserQuestion to confirm: **Open release PR now?**.

If the user confirms, record the audit gate (this script issues `git push`):

```bash
bash "${CLAUDE_PLUGIN_ROOT}/hooks/record-audit.sh"
```

Immediately followed by apply:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/shared/release/pr-create.sh" \
  --target=<target> --release-branch=<release_branch> \
  --body-file=<tempfile> [--title="<custom>"] \
  --apply [--update-existing] --json
```

If apply exits non-zero, surface stderr verbatim and stop.

### Step 6 — Report

On success:

```
✓ Release PR <created|updated>
  PR:     #<n>
  url:    <url>
  branch: <release_branch> → <target>

Next:
  /merge-release   # merge once approved
```

## Important Notes

- **No extra round-trips** — run the steps straight through, pausing only for the confirmations they ask for.
- **No re-derived gh/git logic in prose** — every gh/git operation goes through the shared scripts.
- **Audit gate** — `record-audit.sh` must run *immediately before* `pr-create.sh --apply`, since the script issues `git push`. Do not run anything between them that could change HEAD or branch.
- **Body authoring is your job** — the shell scripts deliberately don't template prose; the JSON from `commits-data.sh` is what you have to work with. Keep it factual and grouped, no marketing voice.
