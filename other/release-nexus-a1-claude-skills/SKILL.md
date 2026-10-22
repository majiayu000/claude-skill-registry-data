---
name: release
category: release-management
model: claude-haiku-5-5
userInvocable: true
description: Create a GitHub release with a version tag and LLM-authored release notes. Takes an optional version and source branch; --pre-release marks it a pre-release, --fasttrack (-y / --yes) skips the confirmation prompt. Final step of the release workflow.
argument-hint: "[version] [branch] [--pre-release|--prerelease] [--fasttrack|-y|--yes]"
allowed-tools: "Bash(pwd:*), Bash(echo:*), Bash(grep:*), Bash(git rev-parse:*), Bash(git branch:*), Bash(git fetch:*), Bash(git tag:*), Bash(git log:*), Bash(bash:*), Bash(gh pr list:*), Bash(gh release view:*), AskUserQuestion, Skill, Write"
---

# Release Command

> Workflow: `/create-release-branch` → `/create-release` → `/merge-release` → **`/release`**

## Usage

```bash
/release                                  # interactive — suggests the version bump
/release v1.0.2                           # stable release from the default branch
/release v1.0.2 develop                   # stable release from another branch
/release v1.2.0-rc.1 --pre-release        # explicit pre-release
/release v1.2.0-rc.1 release/v1.2.0       # a release/* branch implies --pre-release
/release v1.0.2 -y                        # skip the confirmation prompt
```

`--prerelease` is accepted as an alias of `--pre-release`, and `--yes` /
`--fasttrack` as aliases of `-y`. Fasttrack still aborts rather than
auto-routing when the workflow case needs a decision — see Important Notes.

## Context

Working directory: !`pwd`

Current branch: !`git branch --show-current 2>/dev/null || echo "(not in a git repository)"`

Remote tags: !`bash "${CLAUDE_PLUGIN_ROOT}/shared/release/fetch-tags.sh" 2>/dev/null || echo "(fetch unavailable)"`

Latest release: !`bash "${CLAUDE_PLUGIN_ROOT}/shared/resolve-latest-release.sh" 2>/dev/null || echo "(resolver unavailable)"`

Available branches: !`git branch -a --list 'master' 'main' 'release/*' 'origin/master' 'origin/main' 'origin/release/*' 2>/dev/null || echo "(no branches)"`

Recent tags: !`git for-each-ref --count=10 --sort=-v:refname --format='%(refname:short)' refs/tags 2>/dev/null || echo "(no tags)"`

Arguments provided: $ARGUMENTS

**Release terminology** — see `${CLAUDE_PLUGIN_ROOT}/shared/release-concepts.md`.

## Your Task

Thin dispatcher over `${CLAUDE_PLUGIN_ROOT}/shared/release/`. Use parallel tool calls where steps are independent; pause only for the confirmations the steps below ask for. Do not re-derive parsing, version normalization, RC bumping, tag-existence checks, or workflow-case detection — call the scripts and surface their structured output.

The default release source is `origin/<repo default branch>` (resolved from `origin/HEAD` via `_default_branch()`, falling back to `master`). Users can override by passing a branch as the second argument (e.g. `/release v1.2.0-rc.1 release/v1.2.0` for an RC off a release branch). Note: passing a `release/*` branch as the target automatically implies `--pre-release`; stable releases must target the default branch. When no branch arg is given and the user appears to want something other than the default branch, hint that they can pass one explicitly.

### Step 0 — Pre-flight: verify git repo

```bash
git rev-parse --is-inside-work-tree 2>/dev/null
```

If non-zero, stop with the standard "not in a git repository" message instructing the user to `cd` into a service repo.

### Step 1 — Parse arguments

```bash
bash "${CLAUDE_PLUGIN_ROOT}/shared/release/parse-args.sh" \
  --skill=release-create --json -- $ARGUMENTS
```

Outcomes:
- **Exit 0** — `version` populated; `target` (branch) populated; `prerelease` may be `true`/`false`/`null`; `fasttrack` is bool.
- **Exit 10** — `missing` contains `version`. See **Resolving the version** below.
- **Exit 20** — surface errors and stop.

#### Resolving the version

When `version` is missing, suggest a concrete version. The Context block above fetches remote tags **first** (`Remote tags:`), then resolves `Latest release` (from `resolve-latest-release.sh`) and `Recent tags` (top 10) against that fresh tag set. **Use those values directly** — do not re-shell `resolve-latest-release.sh` or `git tag --sort=-version:refname | head -10`. If the `Remote tags:` line shows a `[stale-tags]` or `[no-remote]` marker, the fetch failed or was skipped — surface that to the user before presenting the recommendation, since `Latest release` may then be based on stale local tags.

Then propose a bump based on conventional-commit scope using `commits-data.sh` against the resolved branch:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/shared/release/commits-data.sh" \
  --base=<latest-tag> --head=<branch> --json
```

The JSON gives `breakdown.feat / fix / chore / …` and `has_breaking_change`. Map to a bump:

| Signal | Bump | Example |
|---|---|---|
| `has_breaking_change == true` | major | v1.2.3 → v2.0.0 |
| `breakdown.feat > 0` (no breaking) | minor | v1.2.3 → v1.3.0 |
| only `fix` / `chore` / `docs` / `refactor` | patch | v1.2.3 → v1.2.4 |

Use **AskUserQuestion** to confirm the bump (skip if `fasttrack` and the bump is unambiguous; abort fasttrack if `has_breaking_change` is true and the user did not pass an explicit version). Then re-run the parser with the chosen version.

For RC bumps (`prerelease == true`): scan the **Recent tags** Context value above for `vX.Y.Z-rc.*` matches and propose `-rc.<N+1>`. If the ladder doesn't go deep enough (rare — would need >10 RCs of the same X.Y.Z), only then re-run `git tag --sort=-version:refname | grep "^v<X.Y.Z>-rc"` for that specific stem.

### Step 2 — Plan: validate + detect workflow case

```bash
bash "${CLAUDE_PLUGIN_ROOT}/shared/release/release-create.sh" \
  --version=<version> --branch=<branch> [--prerelease] \
  --plan --json
```

The output reports:
- `workflow_case` — one of: `none-no-release-branch`, `prerelease`, `merged`, `no-pr`, `open-pr`, `closed-not-merged`
- `release_branch` — `{name, exists}`
- `existing_pr` — non-null when a PR for `release/<version>` exists
- `apply_blocked` — non-null if apply would refuse
- `suggested_skill` — `create-release` or `merge-release` when routing is required

Show a concise summary to the user. Then route based on `workflow_case`:

| `workflow_case` | What to do |
|---|---|
| `none-no-release-branch` | OK — proceed to Step 3 |
| `prerelease` | OK — proceed to Step 3 |
| `merged` | OK — proceed to Step 3 |
| `no-pr` | Use **AskUserQuestion**: "Run /create-release now?" → if yes, invoke `Skill(skill: "create-release")` then exit; otherwise stop. **Fasttrack: abort.** |
| `open-pr` | Use **AskUserQuestion**: "Run /merge-release now?" → if yes, invoke `Skill(skill: "merge-release", args: "release/<version>")` then exit; otherwise stop. **Fasttrack: abort.** |
| `closed-not-merged` | Use **AskUserQuestion** to confirm proceeding; if yes, re-plan with `--allow-unmerged-pr` for Step 4. **Fasttrack: abort.** |

### Step 3 — Author release notes

The shell library does **not** generate release-note prose. That is your job.

Gather commit data from the previous tag → release branch:

```bash
# Find the previous stable tag (or the previous RC if --prerelease).
prev_tag="$(git tag --sort=-version:refname \
            | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$' | head -1)"
bash "${CLAUDE_PLUGIN_ROOT}/shared/release/commits-data.sh" \
  --base="$prev_tag" --head=<branch> --json
```

Author a markdown release-notes file. A good shape:

```markdown
## What's Changed

<one-paragraph summary derived from breakdown — e.g. "12 commits: 4 feat, 6 fix, 1 chore. No breaking changes.">

### Features

- **api**: <subject from a feat commit> — JIRA-123
- ...

### Bug Fixes

- **ui**: <subject from a fix commit> — JIRA-456
- ...

### Other Changes

- <docs / chore / refactor commits>

**Full Changelog**: https://github.com/OWNER/REPO/compare/<prev-tag>...<version>
```

If `has_breaking_change == true`, surface a **⚠️ Breaking Changes** section at the top.

Write the notes to a tempfile under `.claude/session-state/` (or `/tmp/` if the workspace path isn't available):

```bash
# Use the Write tool to create the file at e.g.
#   .claude/session-state/release-notes-<version>.md
```

### Step 4 — Confirm and apply

Use **AskUserQuestion** to confirm: **Create release `<version>` from `<branch>` now?**

Skip the prompt if `fasttrack == true`; print a one-line auto-confirm marker instead.

Then record the audit gate. `gh release create` is not covered by `git-mutation-guard.sh` (the hook only matches `git push`), but this skill mutates remote state — recording the audit keeps the trail consistent with the other release skills:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/hooks/record-audit.sh"
```

Immediately followed by apply:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/shared/release/release-create.sh" \
  --version=<version> --branch=<branch> [--prerelease] \
  --notes-file=<tempfile> [--allow-unmerged-pr] \
  --apply --json
```

If apply exits non-zero, surface stderr verbatim and stop.

### Step 5 — Report

On success:

```
✓ Release <created>
  version: <version>
  branch:  <branch>
  url:     <url>

<For pre-releases:>
⚠️  This is a pre-release and is marked as such on GitHub.
```

## Important Notes

- **No extra round-trips** — run the steps straight through, pausing only for the confirmations they ask for.
- **No re-derived gh/git logic in prose** — every gh/git operation goes through the shared scripts.
- **Default source is `origin/<repo default branch>`** — if the user appears to want a different source (e.g. an RC off a release branch), ask them to pass it as the second argument: `/release <version> <branch>`.
- **Workflow gate** — when `release/<version>` exists, the action script enforces "no-pr → /create-release", "open-pr → /merge-release", "closed-not-merged → confirm with --allow-unmerged-pr". Do not bypass.
- **Fasttrack** (`--fasttrack | -y | --yes`) — auto-confirm the recommended version/branch/prerelease and skip the final confirmation. **Abort** (do not auto-route) if the workflow case is `no-pr`, `open-pr`, or `closed-not-merged`, or if `has_breaking_change` is true and no explicit version was supplied.
- **Notes authoring is your job** — the shell scripts deliberately don't template prose; the JSON from `commits-data.sh` is what you have to work with. Keep it factual and grouped, no marketing voice.
- **Title format** — the GitHub release title MUST be the bare version (e.g. `v1.4.0`). The script handles this; do not pass `--title` unless the user explicitly asked for a custom title.
