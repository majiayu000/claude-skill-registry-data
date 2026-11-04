---
name: pr-summary
description: Generate a PR summary with reviewer suggestions based on file ownership. Fetches PR data, summarizes changes, highlights risks, and recommends reviewers from git history. Use when user says "pr summary", "summarize this PR", "who should review this", "generate PR description", when /morning finds a description that drifted from its diff, or wants a reviewer-ready summary of a pull request. For code review, use /review; for creating PRs, use /ship pr; for checking CI status, use /ship checks.
argument-hint: "/pr-summary | /pr-summary <number>"
allowed-tools: "Read, Grep, Glob, Bash, Write, AskUserQuestion"
---

## Overview

Generates a reviewer-friendly summary of a pull request and suggests reviewers based on file ownership history.

## When to Use

- A PR is open and needs reviewers picked from who actually knows the changed files.
- The PR description is empty, under 50 characters, or has drifted from the diff, including when `/morning` flags the drift.
- A reviewer wants the risk areas and the Merge Danger call before reading the diff.
- For a line-by-line review, use `/review`; for opening the PR, use `/ship pr`; for CI status, use `/ship checks`.

## Arguments

| Invocation | Action |
|-----------|--------|
| `/pr-summary` | Summarize the PR on the current branch |
| `/pr-summary <number>` | Summarize a specific PR by number |

## Process

### 1. Fetch PR Data

Determine the GitHub account from the git remote using [`standards/github-accounts.md`](../../standards/github-accounts.md).

```bash
GH_TOKEN=$(gh auth token --user <account>) gh pr view <number> --json title,body,files,additions,deletions,commits,labels,baseRefName,headRefName,author,reviewRequests
```

If no number is given, detect the current branch and find its PR:
```bash
GH_TOKEN=$(gh auth token --user <account>) gh pr view --json title,body,files,additions,deletions,commits,labels,baseRefName,headRefName,author,reviewRequests
```

### 2. Analyze Changes

1. **Categorize files.** Group changed files by type:

   | Category | File patterns |
   |----------|-------------|
   | Source code | `src/`, `lib/`, `app/` |
   | Tests | `test/`, `spec/`, `__tests__/`, `*.test.*`, `*.spec.*` |
   | Configuration | `*.config.*`, `.*rc`, `package.json`, `tsconfig.json` |
   | Documentation | `*.md`, [`docs/`](../../docs) |
   | Infrastructure | `Dockerfile`, `docker-compose.*`, [`.github/`](../../.github), `terraform/` |
   | Database | `migrations/`, `prisma/`, `*.sql` |

2. **Identify high-risk areas.** Flag files that need careful review:

   | Risk indicator | Why it matters |
   |---------------|---------------|
   | Auth or security files | Permission and access control changes |
   | Database migrations | Schema changes are hard to reverse |
   | API route definitions | Contract changes affect consumers |
   | Shared utilities or core modules | High blast radius |
   | Environment or config changes | Deployment impact |
   | Files with > 200 lines changed | Large diffs are harder to review |

3. **Summarize the diff.** Read the actual diff to understand:
   - What behavior changed.
   - What was added versus modified versus removed.
   - Whether tests cover the changes.

### 3. Suggest Reviewers

For each changed file, find the most frequent contributors:

```bash
git log --format='%an' --since='6 months ago' -- <file> | sort | uniq -c | sort -rn | head -3
```

1. **Aggregate across all files.** Count how many changed files each contributor has history with.

2. **Rank by coverage.** The best reviewer is the person with history across the most changed files.

3. **Exclude the PR author.** Never suggest the author as a reviewer.

4. **Present top 3 suggestions:**

   | Reviewer | Files with history | Coverage |
   |----------|--------------------|----------|
   | Alice | 8 of 12 | 67% |
   | Bob | 5 of 12 | 42% |
   | Carol | 3 of 12 | 25% |

### 4. Generate Summary

If the PR description is empty or under 50 characters, generate a reviewer-friendly description following the format in [`../../rules/git-workflow.md`](../../rules/git-workflow.md):

- **What:** one paragraph explaining what changed and why.
- **How:** key implementation decisions and trade-offs.
- **Evidence:** a before and an after: the exact test that failed and now passes, or the output that changed. "Tests are green" alone is a claim. A visible change carries high-resolution screenshots labeled `Before:` and `After:`; when none exist, capture them per [`standards/frontend-render-gate.md`](../../standards/frontend-render-gate.md) before the body is published.
- **Merge Danger:** the **Door**, one-way or two-way, and the **Blast Radius**, what breaks if the change is wrong. Always one-way: a migration that drops or rewrites data, an outbound send to users or partners, a deletion, and a public API removal.
- **Breaking changes:** if any, with migration steps.

The generated body follows [`../../rules/no-ai-process-leak.md`](../../rules/no-ai-process-leak.md), is never hard-wrapped, and carries no open questions; those go to the chat.

### 5. Output

Present the full summary:

1. **PR title and metadata.** Title, author, base branch, head branch, labels.

2. **Change summary.** Categorized file list with line counts.

3. **Risk areas.** Flagged files with explanations, plus the Merge Danger call: Door and Blast Radius, with the one-way trigger named when one applies.

4. **Test coverage.** Whether tests were added or modified for the changes.

5. **Suggested reviewers.** Top 3 with coverage percentages.

6. **Generated description.** If the existing description was thin, provide the generated one and offer to update the PR. Bots such as CodeRabbit append their own blocks to the body, delimited by HTML comment markers, and `--body-file` replaces the whole body, so fetch the live body right before the edit and carry every bot block over unchanged:
   ```bash
   GH_TOKEN=$(gh auth token --user <account>) gh pr view <number> --json body --jq .body > "$live_body"
   GH_TOKEN=$(gh auth token --user <account>) gh pr edit <number> --body-file "$new_body"
   ```
   `$new_body` holds the generated text followed by every bot-appended block copied from `$live_body`. Both are files from `mktemp`, deleted after the edit.

## Rules

- Account token prefixing is mandatory for all `gh` commands per [`standards/github-accounts.md`](../../standards/github-accounts.md).
- Never auto-update the PR description without asking. Always present the generated text and let the user decide.
- Reviewer suggestions are based on git history, not organizational hierarchy. State this in the output.
- When the PR has fewer than 3 potential reviewers from git history, show however many are available. Do not pad with guesses.
- All timestamps in GMT.
- Read the actual diff, not just the file list. A file list without context produces shallow summaries.

## Common Rationalizations

- "The file list and line counts say enough": a file list produces a shallow summary. Read the diff before writing What and How.
- "`Tests are green` covers Evidence": Evidence is a before and an after, such as the exact test that failed and now passes.
- "The description is plainly thin, so updating it saves a round trip": present the generated body and run `gh pr edit` only after the user says yes.
- "Git history yields two reviewers, the team lead makes a natural third": suggestions come from history alone. Show the two.
- "This migration is easy to reverse, call it two-way": a migration that drops or rewrites data, an outbound send, a deletion, and a public API removal are always one-way.

## Red Flags

- Stop and resolve the account from the remote when a `gh` command lacks the `GH_TOKEN` prefix.
- Stop and remove the author when they appear in the reviewer suggestions.
- Stop and ask the user when `gh pr edit` is about to run without their approval.
- Stop and move the question to the chat when the generated body contains an open question.
- Stop and capture high-resolution `Before:` and `After:` screenshots when a visible change has none to show.

## Verification

- Every `gh` call carried the `GH_TOKEN=$(gh auth token --user <account>)` prefix.
- The summary cites behavior read from the diff, beyond the file list.
- The reviewer table excludes the author, lists at most three people, and states that it comes from git history.
- The Merge Danger call names the Door and the Blast Radius, plus the one-way trigger when one applies.
- A generated body carries What, How, Evidence, Merge Danger, and Breaking changes, with one line per paragraph.
- The PR description on GitHub is unchanged unless the user approved the edit, and after an edit every bot-appended block from the live body is still present.

## Related Skills

- `/review` -- Detailed code review of the PR's changes.
- `/ship pr` -- Create or update a pull request.
- `/ship checks` -- Monitor CI status for the PR.
