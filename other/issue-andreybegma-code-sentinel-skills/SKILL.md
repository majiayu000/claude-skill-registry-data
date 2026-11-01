---
name: cs-issue
description: Create GitHub issues from analysis findings, bug descriptions, feature requests, or code inspection — with user confirmation, or autonomously with --auto. --ready queues them for cs-orchestrator
argument-hint: "[description | path] [--auto] [--ready] [--depends-on <n,...>]"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, AskUserQuestion
---

# GitHub Issue Creator

You create well-structured GitHub issues from analysis findings, bug descriptions or feature requests. **Without `--auto`, never create an issue without explicit user confirmation.**

## Inputs

`$ARGUMENTS` — one of:

- **Empty** — collect findings from the current conversation (previous `/cs-security`, `/cs-debug`, etc.)
- **Text description** — `"Login fails when email contains +"` or `"Add CSV export to reports"` — enrich with code context and create one issue
- **File path** — `src/api/handler.ts` — inspect the file, find problems, propose issues

Flags:

| Flag | Effect |
|---|---|
| `--auto` | **Autonomous.** Skip Step 3's confirmation: create every non-duplicate issue (CRITICAL + HIGH from findings; the one issue for a description), then report. Used by `cs-feature --auto` and `cs-orchestrator` |
| `--ready` | Also add the orchestrator's ready label (`.code-analyzer-config.json` → `orchestrator.readyLabel`, default `cs:ready`) so `cs-orchestrator` picks the issue up. Only with acceptance criteria (feature) or a reproduction (bug) — an issue without either gets no ready label and a note saying why |
| `--depends-on <n,...>` | Write `Depends on #n` lines into the body — the orchestrator dispatches only after those issues are closed by merged pull requests |

**Kind.** Every issue is a `bug` (something behaves wrongly or used to work) or a `feature` (something is missing). Findings from `/cs-security`, `/cs-debug` and `/cs-perf` are bugs; `/cs-dead-code` and `/cs-review` findings are features (cleanup work) unless they describe broken behaviour.

## Step 1: Gather Findings

### If no arguments (post-analysis mode):

1. Review the current conversation for findings from previous skills (`/cs-security`, `/cs-dead-code`, `/cs-debug`, `/cs-review`)
2. Collect all CRITICAL and HIGH findings
3. Include MEDIUM findings only if there are fewer than 5 total issues
4. If no previous analysis exists, tell the user to run an analysis first or provide a description

### If text description:

1. Search the codebase for related code (grep for keywords, function names, error messages)
2. Read relevant files to understand context
3. Formulate a single issue with code references

### If file path:

1. Read the file
2. Check `git log --oneline -10 -- $FILE` for recent changes
3. Propose issues for each finding

## Step 2: Check for Duplicates

Before proposing any issue, search existing issues:

```bash
gh issue list --state open --search "<key terms from the finding>" --limit 5
```

If a similar issue already exists:

- Show the existing issue number and title
- Mark the finding as **SKIP (duplicate of #N)**
- Do not include it in the confirmation list

## Step 3: Prepare Preview

Show the user a numbered list as **plain text**, then use `AskUserQuestion`:

```
Found N issues to create:

1. [CRITICAL] SQL injection in UserService.ts:45
   → Duplicate check: no existing issues found

2. [HIGH] Missing auth guard on /api/admin/users
   → SKIP: duplicate of #87

3. [HIGH] Hardcoded JWT secret in config.ts:12
   → Duplicate check: no existing issues found
```

Options:
| Option | Description |
|--------|-------------|
| **All (Recommended)** | Create all non-duplicate issues |
| **Critical only** | Create only CRITICAL severity issues |
| **High+** | Create CRITICAL + HIGH issues |
| **None** | Stop, create nothing |

User can type in "Other": numbers (`1 3`) = specific items, inverted (`!1`) = all except. These are **item numbers**, not option numbers.

**Wait for user response before proceeding.** Under `--auto`, skip this step: print the list and go straight to Step 4.

## Step 4: Create Issues

For each confirmed issue, run:

```bash
gh issue create --title "<title>" --body "<body>" --label "<labels>"
```

Show `✅ Created #N — <title> — <url>` after each.

### Issue Title Format

```
[SEVERITY] Short description — file:line
```

### Issue Body Format — feature request

A request (not a finding) gets this body, in this order and nothing else:

````markdown
## What is missing
[Plain words, no preamble]

## Why it matters
[What cannot be done, or what breaks, until this exists]

## Where
- `path/to/module/` — [what lives there and why it is affected]

## Acceptance criteria
- [ ] [Checkable by someone who did not write the code]
- [ ] [...]

## Out of scope
- [What this issue deliberately does not do]

Depends on #N        ← one line per dependency, only with --depends-on
Gate: [...]          ← only if a person must clear something before merge (a key, a sign-off, a release window)

## Found By

Code Sentinel `/cs-issue`
````

Title for a request: `feat: <short imperative>`; for a bug from a description: `fix: <short imperative>`.

### Issue Body Format — finding

````markdown
## Description

[Clear explanation of the problem]

## Location

- **File:** `path/to/file.ts:line`
- **Function:** `functionName()`

## Details

[Code snippet showing the problem — use ```lang fenced blocks]

## Suggested Fix

[Concrete fix recommendation from the analysis]

## Reproduction / Acceptance

- [ ] [How to see it fail, or what proves it fixed — a test, a command, steps]

## Found By

Code Sentinel `/cs-issue` — automated analysis
````

### Labels

Apply labels based on issue type. Create labels if they don't exist:

- Finding from `/cs-security` → `security`
- Finding from `/cs-dead-code` → `dead-code`
- Finding from `/cs-debug` → `bug`
- Finding from `/cs-review` → `code-quality`
- Finding from `/cs-perf` → `performance`
- Always add: `claude-generated`
- Kind: `bug` or `enhancement` (GitHub's defaults)
- With `--ready`: the ready label (`cs:ready` by default)

Severity labels:

- CRITICAL → `priority: critical`
- HIGH → `priority: high`
- MEDIUM → `priority: medium`

To create a missing label, run this command (ignore errors if label already exists):

```bash
gh label create "claude-generated" --description "Issue created by Code Sentinel" --color "c5def5" --force
```

The `--force` flag creates the label if it doesn't exist or updates it if it does.

## Step 5: Report

After all issues are created, show skipped items:

```
Skipped:
- [HIGH] Missing auth guard (duplicate of #87)
- [MEDIUM] N+1 query (user declined)
```

Omit if nothing was skipped.

## Important

- **Without `--auto`, never create issues without user confirmation** — this is the core rule
- Under `--auto`, the duplicate check is still mandatory, and nothing is ever labelled ready without acceptance criteria or a reproduction
- One change, one issue — never open a second issue for something that already has one
- No local filesystem paths in titles or bodies — repository-relative paths only
- Never paste user data, secrets or tokens into an issue
- If `gh` is not authenticated, tell the user to run `gh auth login` and stop
