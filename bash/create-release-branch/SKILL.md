---
name: create-release-branch
category: release-management
model: claude-haiku-5-5
userInvocable: true
description: Create a release/vX.Y.Z branch from the repo's default branch (default), any branch, or a specific tag using tag@vX.Y.Z syntax. Takes a version and an optional source. Step 1 of the release workflow.
argument-hint: "<version> [source]"
allowed-tools: "Bash(pwd:*), Bash(echo:*), Bash(git rev-parse:*), Bash(git branch:*), Bash(git fetch:*), Bash(bash:*), AskUserQuestion"
---

# Create Release Branch Command

> Workflow: **`/create-release-branch`** → `/create-release` → `/merge-release` → `/release`

## Usage

```bash
/create-release-branch v1.2.0              # from the repo's default branch
/create-release-branch v1.2.0 develop      # from another branch
/create-release-branch v1.2.0 tag@v1.1.0   # from a specific tag
```

The version is required — omit it and you are prompted rather than guessed at:
`version-suggest.sh` proposes one from the repo's release tags/branches and the
commits since, and you pick. `source` defaults to the repo's default branch.

## Context

Working directory: !`pwd`

Repository: !`git rev-parse --show-toplevel 2>/dev/null || echo "(not in a git repository)"`

Current branch: !`git branch --show-current 2>/dev/null || echo "(not in a git repository)"`

Arguments provided: $ARGUMENTS

Latest release (deterministic — `<kind> <ref> <version>`): !`bash "${CLAUDE_PLUGIN_ROOT}/shared/resolve-latest-release.sh" 2>/dev/null || echo "(resolver unavailable)"`

**Release terminology** — use the definitions in `${CLAUDE_PLUGIN_ROOT}/shared/release-concepts.md`. "Latest release" is the value printed above.

## Your Task

This skill is a thin dispatcher over the deterministic shell library at `${CLAUDE_PLUGIN_ROOT}/shared/release/`. Do not re-derive parsing or version logic in prose — call the scripts and surface their structured output.

### Step 0 — Pre-flight: verify git repo

```bash
git rev-parse --is-inside-work-tree 2>/dev/null
```

If this returns non-zero, stop with the standard "not in a git repository" message that tells the user to `cd` into a service repo first (see `Working directory:` in Context above).

### Step 1 — Parse arguments

Run the parser:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/shared/release/parse-args.sh" \
  --skill=branch-create --json -- $ARGUMENTS
```

Possible outcomes:

- **Exit 0** — fully parsed. The output JSON has `version`, `source`, `source_kind` populated.
- **Exit 10** — ambiguous; the `missing` array names the field(s) the user didn't supply (typically `["version"]`).
- **Exit 20** — bad input. Show the `errors` array and stop.

### Step 2 — Resolve missing fields interactively

If the parser returned exit 10 with `missing` containing `version`:

1. Run `bash "${CLAUDE_PLUGIN_ROOT}/shared/release/version-suggest.sh" --json` to get a recommended next version grounded in the **current repo's** tag/branch state. This script fetches remote tags first so the suggestion is based on the authoritative tag set. **Watch its stderr**: if it emits a `[stale-tags]` or `[no-remote]` marker, the tag fetch failed or was skipped — surface that marker to the user before presenting the recommendation, since the suggested version may be based on stale local tags. Do not block on it; continue to the recommendation.
2. Use AskUserQuestion to present:
   - The `recommended` value with its `reason` as the (Recommended) option.
   - Each entry from `alternatives` as additional options.

   **Critical**: the suggestion must come from `version-suggest.sh` run in the *current working tree* — never carry over a version seen earlier in the conversation from a different repo.

3. Re-run `parse-args.sh` with the chosen version included in `$ARGUMENTS`.

If `source` was not supplied, default to `origin/<repo default branch>` (parse-args already does this via `_default_branch()`, resolved from `origin/HEAD`). The user may override via the second positional argument or the `tag@vX.Y.Z` syntax.

### Step 3 — Show plan and confirm

Run the action script in plan mode:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/shared/release/branch-create.sh" \
  --version=<v> --source=<s> --source-kind=<k> --plan --json
```

Print the human-readable plan (re-run without `--json` for display, or render the JSON yourself). Use AskUserQuestion to confirm before applying.

### Step 4 — Record audit, then apply

Pushing to `release/*` is gated by `git-mutation-guard.sh` and requires a security-auditor confirmation. Record one immediately before invoking the action script:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/hooks/record-audit.sh"
```

Then run apply:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/shared/release/branch-create.sh" \
  --version=<v> --source=<s> --source-kind=<k> --apply --json
```

If `--apply` exits non-zero, surface stderr to the user verbatim and stop.

### Step 5 — Report and suggest next steps

On success, show:

```
✓ Release Branch Created
  branch: release/<v>
  source: <ref>

Next:
  /create-release          # open PR to the default branch
  /merge-release           # merge once approved
  /release                 # tag + GitHub release
```

## Important Notes

- **No extra round-trips** — run the steps straight through, pausing only for the confirmations they ask for; use parallel tool calls where independent.
- **No per-step git invocations in prose** — every git/branch/version operation goes through the shell library. The library is the source of truth.
- **Version normalization happens in the parser** — pass `$ARGUMENTS` to it raw; do not strip or add the `v` prefix yourself.
- **Audit gate** — `record-audit.sh` must run *immediately before* the action script; do not run anything between them that could change HEAD or branch.
