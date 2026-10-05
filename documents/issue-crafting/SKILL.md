---
name: issue-crafting
description: "Craft well-structured GitHub issues with solution-agnostic outcomes, duplicate detection (open and closed), dynamically-discovered labels, and acceptance criteria describing observable behavior without implementation details. Use when creating new GitHub issues. Proactively suggest when an issue prescribes a method instead of describing an outcome."
allowed-tools: Bash, Read, AskUserQuestion
agent: Explore
---

# Issue Crafting

## Contract

Iron law: issues describe outcomes, never implementations — if the issue says "how," rewrite it. Invoked by `/flow:issue` (all phases), by `/flow:start` Phase 1 when the issue lacks acceptance criteria, and by `/flow:review` and `/flow:address` when a user-selected finding becomes a new issue. Returns a created and verified GitHub issue (`gh issue view <N> --json number,title,state,labels`) whose body follows the Context / Current State / Objective / Acceptance Criteria structure, with labels drawn from `gh label list`. Permitted skips: none — duplicate search (open and closed) always runs before creation, and any of the four requirement elements that is missing is gathered via the AskUserQuestion tool before composing.

## Solution-Agnostic Rules

- Describe outcomes: "Users can reset their password via email" — not "Add a reset_password method to UserController that sends a Postmark email."
- Acceptance criteria are verifiable without reading code: "Resetting a password with a valid token changes the stored password" — not "The `reset!` method updates the `password_digest` column."
- Never include file paths, function names, or class names in acceptance criteria.
- No vague criteria ("improve performance", "make it better"); no bundling unrelated changes into one issue.

## Requirements Gathering

Collect four elements; for each gap, use the AskUserQuestion tool with contextual options (e.g., "What's the current behavior?"):

1. **Context** — background and motivation
2. **Current State** — what happens now, what the problem is
3. **Objective** — the outcome to achieve
4. **Acceptance Criteria** — observable behaviors that prove completeness

## Duplicate Detection

```bash
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
gh issue list --state open --search "KEYWORDS" --limit 10
gh issue list --state closed --search "KEYWORDS" --limit 5
```

If matches are found, present them to the user before proceeding.

## Labels and Milestones

Never hardcode labels: `gh label list --json name,description --limit 50`, then select by content (bug reports → `bug`, features → `enhancement`, docs → `documentation`, security → `security`, when those labels exist). Check `gh api repos/$REPO/milestones --jq '.[] | "\(.number): \(.title)"'` and offer milestone assignment if any exist.

## Issue Body Structure

```markdown
## Context
{Background and motivation}

## Current State
{What's happening now — observable behavior}

## Objective
{What should be achieved — outcomes, not methods}

## Acceptance Criteria
- [ ] {Observable behavior 1}
- [ ] {Observable behavior 2}
```

## Verification

After creation run `gh issue view <N> --json number,title,state,labels` and confirm: clear, searchable title; no file paths or implementation details in the body; acceptance criteria describe what, not how; labels come from the repository's label set.
