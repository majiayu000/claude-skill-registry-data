---
name: pr
description: >-
  Create, inspect, or merge GitHub pull requests. Use when the user asks to
  open a PR, check PR status, or merge a PR. Composes PR descriptions from
  existing review file metadata. Manual invocation only via /pr.
argument-hint: "[branch | status | number | merge | list]"
disable-model-invocation: true
context: fork
effort: medium
allowed-tools: Bash(*), Read, Grep, Glob
---

# GitHub Pull Request Workflow

You manage the GitHub PR lifecycle: create PRs with auto-composed descriptions,
inspect PR status, and merge with review verification. You start with an empty
context -- gather everything you need below.

Arguments: `$ARGUMENTS`

## Prompt Design Principles

- **Opt-in, not automatic.** PRs are a deliberate choice. Never create a PR unless
  explicitly asked. Direct-to-main is the default workflow for solo development.
- **Zero-overhead descriptions.** PR bodies are composed from existing review metadata
  (CODEREVIEW.md, SECURITY.md, TESTING.md, SPEC.md) and commit messages. No extra work from the user.
- **Idempotent operations.** Creating a PR when one already exists for the branch shows
  the existing PR. Merging a PR that is already merged reports the fact. Never duplicate.
- **Evidence grounding.** Review verdicts included in PR descriptions come from actual
  review file metadata, not from re-running reviews or guessing.

---

## Step 1: Parse Arguments and Determine Mode

Parse `$ARGUMENTS` to determine the operation:

| Input | Mode | Action |
|-------|------|--------|
| *(empty)* | **create** | Create a PR for the current branch |
| `<branch-name>` | **create** | Create a feature branch with that name, then create a PR |
| `status` | **status** | Show status of the current branch's PR |
| `<number>` or `<url>` | **inspect** | Show details of a specific PR |
| `merge` | **merge** | Merge the current branch's PR |
| `list` | **list** | List open PRs for this repo |

## Step 2: Verify Prerequisites

```bash
# Verify gh is authenticated
gh auth status

# Get repo and branch context
git remote get-url origin
git rev-parse --abbrev-ref HEAD
git rev-parse --show-toplevel
```

If `gh auth status` fails, report the error and stop.

If the repo has no GitHub remote, report that and stop.

## Step 3: Execute Mode

### Mode: create

**3a. Handle branch.**

```bash
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
```

If on `main` and a branch name was provided in `$ARGUMENTS`:
```bash
git checkout -b "$BRANCH_NAME"
```

If on `main` and no branch name was provided, derive one from the most recent commit
message (e.g., `feat/add-pr-skill`). Use lowercase, hyphens, no special characters.
Prefix with `feat/`, `fix/`, or `docs/` based on the commit content.

If already on a non-main branch, use it as-is.

**3b. Check for existing PR.**

```bash
gh pr list --head "$(git rev-parse --abbrev-ref HEAD)" --json number,url,state --jq '.[]'
```

If a PR already exists for this branch, display it and stop. Do not create a duplicate.

**3c. Gather context for PR description.**

Collect commit history since diverging from main:
```bash
git log --oneline main..HEAD
git diff --stat main...HEAD
```

Read review metadata from persistent files (if they exist). Extract only the
metadata footer line from each file:

```bash
grep 'REVIEW_META' CODEREVIEW.md 2>/dev/null
grep 'SECURITY_META' SECURITY.md 2>/dev/null
grep 'TESTING_META' TESTING.md 2>/dev/null
grep 'SPEC_META' SPEC.md 2>/dev/null
```

**3d. Compose PR title and body.**

- **Title:** Derive from the commit history. If there is one commit, use its message.
  If there are multiple, write a concise summary (under 70 characters).
- **Body:** Use this structure:

```markdown
## Summary

[2-5 bullet points summarizing the changes, derived from commit messages and diff stats]

## Spec

[If SPEC.md exists: spec title, criteria_met/criteria_total. If not: "No spec."]

## Review Status

| Review | Verdict | Date |
|--------|---------|------|
| Code Review | [PASS/BLOCKED/not run] | [date or n/a] |
| Security | [PASS/BLOCKED/not run] | [date or n/a] |
| Test Strategy | [assessed/not run] | [date or n/a] |

[If any BLOCK items exist, list them here]

## Commits

[git log --oneline main..HEAD output]
```

Populate the Review Status table from the REVIEW_META JSON. If a review file does
not exist or has no metadata, mark as "not run." PASS means zero BLOCK items.
BLOCKED means one or more BLOCK items remain.

**3e. Push and create the PR.**

```bash
# Push branch to remote (set upstream if needed)
git push -u origin "$(git rev-parse --abbrev-ref HEAD)"

# Create the PR
gh pr create --title "<title>" --body "<body>"
```

Report the PR URL.

### Mode: status

```bash
gh pr view --json number,title,state,reviews,statusCheckRollup,mergeable,url
```

Display: PR number, title, state, review status, CI check results, merge readiness.

If there are review comments, summarize them:
```bash
gh pr view --json comments --jq '.comments[].body'
```

### Mode: inspect

```bash
gh pr view <number_or_url> --json number,title,state,body,reviews,statusCheckRollup,comments,url
```

Display the PR details and summarize any review comments.

### Mode: merge

**Verify review gate.** Check that a passing codereview covers the current code by
reading REVIEW_META from CODEREVIEW.md:

```bash
REVIEW_BLOCKS=$(grep -oP '"block"\s*:\s*\K[0-9]+' CODEREVIEW.md 2>/dev/null)
REVIEWED_UP_TO=$(grep -oP '"reviewed_up_to"\s*:\s*"\K[a-f0-9]+' CODEREVIEW.md 2>/dev/null)
```

The review gate passes if ALL of these hold:
1. CODEREVIEW.md exists and has REVIEW_META
2. `REVIEW_BLOCKS` equals `0`
3. `REVIEWED_UP_TO` is non-empty and `git merge-base --is-ancestor "${REVIEWED_UP_TO}" HEAD`

If any condition fails, report that `/codereview` must be run first and stop.
Do not merge without a passing review.

**Verify GitHub merge readiness.** After the local gate passes, check the PR's remote state:

```bash
gh pr view --json mergeable,reviewDecision,statusCheckRollup --jq '{
  mergeable: .mergeable,
  reviewDecision: .reviewDecision,
  checks: [.statusCheckRollup[]? | {name: .name, status: .status, conclusion: .conclusion}]
}'
```

Block the merge and report the reason if any of these hold:
- `mergeable` is not `MERGEABLE` (conflicts, branch protection rules, etc.)
- `statusCheckRollup` contains any check with `conclusion` of `FAILURE` or
  `status` not `COMPLETED`
- `reviewDecision` is `CHANGES_REQUESTED` or `REVIEW_REQUIRED`

If no CI checks are configured, that is not a blocker (many repos have none).
If `reviewDecision` is empty or `APPROVED`, proceed.

If all checks pass:
```bash
gh pr merge --squash --delete-branch
git checkout main
git pull
```

Report that the PR was merged and the branch was cleaned up.

### Mode: list

```bash
gh pr list --json number,title,headRefName,state,updatedAt --template '{{range .}}#{{.number}} {{.title}} ({{.headRefName}}) {{.state}} {{timeago .updatedAt}}{{"\n"}}{{end}}'
```

Display the list. If no open PRs exist, say so.

## Step 4: Output

End with a one-line summary of what happened:
- **create:** "PR #N created: <url>"
- **status:** "PR #N: <state>, <merge readiness>"
- **inspect:** "PR #N: <title> (<state>)"
- **merge:** "PR #N merged to main. Branch <name> deleted."
- **list:** "N open PR(s)." or "No open PRs."
