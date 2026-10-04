---
name: platform-adapter
description: Stable verb interface for code-host operations. Resolves the active platform from config and dispatches to the correct CLI (gh for GitHub, glab for GitLab). Exposes exactly 16 verbs — callers pass a verb name and arguments; the adapter handles platform selection and command execution.
user-invocable: false
model: haiku
allowed-tools: Bash, Read
---

# platform-adapter

Model-invocable skill for code-host operations across platforms.

## Purpose

Provide a single, stable verb interface over GitHub (`gh`) and GitLab (`glab`) CLI operations. Callers pass a verb name and a map of named arguments. The adapter resolves the active platform from project configuration, looks up the matching command in `reference/{platform}/verbs.md`, substitutes arguments, and executes. Callers receive raw CLI output (stdout) and exit code — the adapter does not transform field names across platforms.

This skill executes — it does not orchestrate.

## Input

Receive from caller (agent):

| Field | Required | Description |
|-------|----------|-------------|
| `verb` | Yes | One of the 16 supported verbs (see Verb Interface below) |
| `args` | Yes | Map of named arguments for the verb (see per-verb reference) |

## Verb Interface

The adapter exposes exactly 16 verbs:

| Verb | Purpose |
|------|---------|
| `view-pr` | Fetch PR/MR metadata (JSON) |
| `diff-pr` | Fetch PR/MR unified diff |
| `comment-pr` | Post a comment on a PR/MR |
| `request-changes` | Request changes on a PR/MR, blocking merge |
| `add-reviewer` | Add a reviewer to a PR/MR |
| `create-pr` | Create a pull/merge request |
| `merge-pr` | Merge a pull/merge request |
| `view-issue` | Read issue details |
| `create-issue` | Create a new issue |
| `list-issues` | List/search issues |
| `close-issue` | Close an issue |
| `comment-issue` | Post a comment on an issue |
| `add-label` | Add labels to an issue or PR |
| `attach-sub-issue` | Attach a child issue to a parent (GitHub only; GitLab falls back to related-link) |
| `view-user` | Get the current authenticated user's login |
| `update-comment` | Update an existing comment in place |

## Platform Resolution

### 1. Read Platform

```bash
platform=$(grep '^platform:' .garura/core/config.yaml | awk '{print $2}')
platform=${platform:-github}
```

The `platform:` key in `.garura/core/config.yaml` is the authoritative source. `git remote -v` is NOT used for platform detection.

### 2. Pre-flight Check (GitLab only)

When `platform=gitlab`, verify `glab` CLI is installed:

```bash
which glab
```

If `glab` is not found, halt immediately with:

```
glab CLI not found. Install via: brew install glab or https://gitlab.com/gitlab-org/cli
```

Do not fall back to `gh`. The caller receives a structured failure — not a raw shell error.

### 3. Load Verb Reference

Load the platform-specific command translation from:

```
reference/{platform}/verbs.md
```

Available references:
- `reference/github/verbs.md` — GitHub via `gh` CLI
- `reference/gitlab/verbs.md` — GitLab via `glab` CLI

If the reference file for the configured platform does not exist, halt with structured failure — do not fall back silently.

### 4. Execute Verb

Look up the section in `verbs.md` matching the requested verb. Substitute the provided `args` into the parameter tokens. Execute the resulting command.

## Process

### Step 1: Resolve Platform

Apply the platform resolution steps above. Halt on pre-flight failure before executing any verb.

### Step 2: Look Up Verb

Find the section in `reference/{platform}/verbs.md` whose heading matches the requested `verb`. If no matching section is found, halt with: `"Unknown verb: {verb}. Supported verbs: view-pr, diff-pr, comment-pr, request-changes, add-reviewer, create-pr, merge-pr, view-issue, create-issue, list-issues, close-issue, comment-issue, add-label, attach-sub-issue, view-user, update-comment."`

### Step 3: Substitute Arguments

Substitute the `args` map values into the command template's `{token}` placeholders. If a required argument is absent, halt with: `"Missing required argument '{arg}' for verb '{verb}'."`

### Step 4: Execute and Return

Execute the resolved command. Return raw stdout and exit code to the caller. The caller is responsible for parsing platform-specific field names — the adapter does not normalize output across platforms. Field-name mapping notes live in `reference/{platform}/verbs.md` for callers to consult.

## Output

Return to caller:

| Field | Description |
|-------|-------------|
| `stdout` | Raw CLI output |
| `exit_code` | Shell exit code (0 = success) |
| `verb` | The verb that was executed |
| `platform` | The platform that was used |

## Constraints

- NEVER infer platform from git remote — always read from `.garura/core/config.yaml`
- NEVER transform or normalize field names in the output — return raw CLI output
- NEVER fall back silently when a platform reference file is missing — halt with structured failure
- ALWAYS perform the `which glab` pre-flight check before any operation when platform=gitlab
- ALWAYS halt with the prescribed install hint text when `glab` is missing: `"glab CLI not found. Install via: brew install glab or https://gitlab.com/gitlab-org/cli"`
- NEVER add verbs beyond the 16 defined above without a schema change

## Version

| Field | Value |
|-------|-------|
| Version | 1.0.0 |
| Category | operations |
