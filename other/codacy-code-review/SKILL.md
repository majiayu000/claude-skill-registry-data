---
name: codacy-code-review
description: Enriches pull request code reviews with Codacy data — quality issues, security findings, coverage, and duplication. Use whenever the user asks to review a PR, check what a pull request introduced, verify PR coverage, look at PR quality, or find new issues in a PR. Also use when another code-review skill is active (e.g. CodeRabbit) to layer Codacy data on top. Trigger this skill for any pull request review workflow, even if the user just says "review PR 42" or "what's wrong with this PR".
license: MIT
metadata:
  author: Codacy
  version: 1.4.0
---

# Codacy Code Review

> **Glossary:** See [glossary.md](../../references/glossary.md) for shared definitions of Codacy concepts (issues, findings, severity, coverage, tools, patterns, etc.).

This skill enriches code reviews with Codacy data. It works alongside any existing code review process (a code-review skill, CodeRabbit, manual review, etc.) — it adds Codacy-specific data on top.

## Prerequisites

- **Codacy Analysis CLI** (`codacy-analysis`) — for fast local analysis. See `codacy-analysis-cli` for setup.
- **Codacy Cloud CLI** (`codacy`) — for coverage data, quality gate status, and ignoring issues. See `codacy-cloud-cli` for setup.

Both CLIs share credentials at `~/.codacy/credentials`, so a single login covers both.

## Local vs Cloud analysis

This skill uses two complementary analysis sources:

| Source | What it provides | Speed |
|--------|-----------------|-------|
| **Analysis CLI** (local) | Issues and security findings on PR changes | Instant — no push or remote analysis needed |
| **Cloud CLI** (remote) | Coverage delta, quality gate, duplication, issue management (ignore/unignore) | Requires the PR to be pushed and analyzed by Codacy |

**Prefer local analysis** for issue detection — it runs immediately on the current working tree with `--pr` and doesn't require waiting for remote analysis. Use the Cloud CLI to supplement with coverage data and quality gate status, and to manage issues (ignore/unignore).

The Analysis CLI may not support every tool that Codacy Cloud runs. If the project uses tools not available locally (check with `codacy-analysis analyze --inspect --output-format json`), flag that some findings may only appear in the Cloud results.

## How Codacy PR data works

- **Cloud data reflects the HEAD commit of the PR** — the remote analysis shown is always for the latest push to the PR branch, not a specific commit.
- **Local analysis reflects the working tree** — `codacy-analysis analyze --pr` compares the current branch against the PR's target branch, catching issues even before pushing.
- **Ignoring issues** is a Cloud-only operation — it takes effect immediately on Codacy but any other configuration changes (patterns, tools) only apply after the next remote analysis.
- **Stale or missing remote analysis** — if the Cloud PR analysis appears outdated or incomplete, use `codacy pull-request <provider> <org> <repo> <prNumber> --reanalyze-and-wait` to trigger reanalysis and block until it completes (polls every 10 seconds, up to 20 minutes). For fire-and-forget, use `--reanalyze` instead and re-check manually.
- **Auto-detection** — when running inside the repo, the Cloud CLI auto-detects provider/org/repo from the git remote. Commands like `codacy pull-request <prNumber>` work without explicit parameters.

## Review workflow

When reviewing a pull request, follow these steps. Always complete all steps — do not skip.

```
Code Review Progress:
- [ ] Step 1: Gather PR context (title, description, linked ticket)
- [ ] Step 2: Run local analysis on PR changes
- [ ] Step 3: Fetch Cloud PR data (coverage, quality gate)
- [ ] Step 4: Check introduced issues
- [ ] Step 5: Check coverage
- [ ] Step 6: Verify alignment with ticket and PR description
- [ ] Step 7: Propose test plan and check coverage gaps
- [ ] Step 8: Summarize and suggest improvements
```

### Step 1: Gather PR context

Fetch the pull request metadata from the source provider (GitHub, GitLab, Bitbucket):
- PR title and description
- Linked ticket or issue (Jira, GitHub Issues, Linear, local spec, etc.) — look in the description, branch name, and commit messages

If there is a linked ticket, fetch its content as well.

### Step 2: Run local analysis on PR changes

Run the Analysis CLI to get immediate results on the changed files — no need to wait for remote analysis:

```bash
# If the PR already exists (compares against the PR's target branch)
codacy-analysis analyze --pr --output-format json

# If the PR hasn't been created yet (compares against the merge base of the current branch)
codacy-analysis analyze --diff --output-format json
```

Use `--pr` when the pull request exists, `--diff` when you're reviewing changes on a branch before the PR is opened. Both run all locally available tools on the changed files only.

If the project hasn't been initialized for local analysis yet:

```bash
codacy-analysis init
codacy-analysis analyze --pr --install-dependencies --output-format json
```

Parse the local results for issues — these are available immediately and cover the bulk of the review. Note any tools listed in `capability.unavailable` that might provide additional findings only through Codacy Cloud.

### Step 3: Fetch Cloud PR data (coverage, quality gate)

Coverage, quality gate status, and duplication metrics are only available from Codacy Cloud:

```bash
codacy pull-request <provider> <org> <repo> <prNumber>
```

This returns: up-to-standards status, coverage delta, complexity delta, duplication delta, and changed files.

For the annotated diff with inline coverage annotations:
```bash
codacy pull-request <provider> <org> <repo> <prNumber> --diff
```

If the remote analysis is stale or missing, trigger a reanalysis and wait for completion:
```bash
codacy pull-request <provider> <org> <repo> <prNumber> --reanalyze-and-wait
```

This blocks until reanalysis finishes (up to 20 minutes) and reports the delta. While waiting, continue the review using local results from Step 2. For fire-and-forget reanalysis, use `--reanalyze` instead.

### Step 4: Check introduced issues

Combine findings from both local analysis (Step 2) and Cloud data (Step 3):

- **Local issues** are typically available first — use these to start the review immediately
- **Cloud issues** may include findings from tools not available locally — cross-reference once remote analysis completes
- Note the severity, category, and file location for each issue
- Flag Critical and High severity issues as blockers

If issues look like false positives, suggest ignoring them via the Cloud CLI:
```bash
# Ignore a specific issue in this PR
codacy pull-request <provider> <org> <repo> <prNumber> --ignore-issue <issueId> --ignore-reason FalsePositive

# Ignore all issues Codacy identified as potential false positives in one go
codacy pull-request <provider> <org> <repo> <prNumber> --ignore-all-false-positives

# Unignore if needed
codacy pull-request <provider> <org> <repo> <prNumber> --unignore-issue <issueId>
```

If the same false positive pattern keeps appearing across PRs, suggest disabling the pattern via `configure-codacy` instead.

### Step 5: Check coverage

Coverage data comes from the Cloud CLI (Step 3). Review:
- Overall coverage delta (did it go up or down?)
- Files with uncovered lines introduced by the PR
- Use `--diff` output to see which specific lines lack coverage (✘ markers)

Flag files with new uncovered lines as needing tests.

### Step 6: Verify alignment

**With the ticket/issue:** Check that the code changes address the stated requirements. Note any functionality described in the ticket that is not present in the changes. Note any changes that go beyond the scope of the ticket.

**With the PR description:** Verify the description accurately reflects what was changed. Note discrepancies.

If the ticket or PR description is missing, incomplete, or inaccurate, note specific improvements to suggest.

### Step 7: Propose test plan

Based on the changed code and coverage data:
1. List the scenarios that should be tested (happy path, edge cases, error cases)
2. For each scenario, check whether a test already exists in the PR diff
3. Flag scenarios with no corresponding test and no coverage in Codacy

### Step 8: Summary

Present a structured review summary:

```
## Codacy Review Summary

### Quality gate
[Pass / Fail — from Codacy PR analysis]

### Issues introduced
[List issues by severity, or "None"]

### Coverage
[Delta, uncovered lines in new code]

### Alignment
- Ticket: [aligned / gaps noted]
- PR description: [accurate / suggestions]

### Test plan
[Proposed scenarios and whether tests exist]

### Suggested improvements
- PR description: [if applicable]
- Ticket/issue: [if applicable]
```

## When another code review skill is active

If a code review skill (e.g. `code-review` skill, CodeRabbit) has already performed a review, add a **Codacy data section** to that review rather than replacing it. Follow steps 2–7 above and append the Codacy findings.
