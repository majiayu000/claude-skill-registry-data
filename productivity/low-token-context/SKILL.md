---
name: low-token-context
description: >
  Build compact Codex task context and avoid token blowups. Use when work spans
  large repos, repeated sessions, long logs, many files, expensive models, or
  the user mentions limits, context, tokens, compression, summaries, or keeping
  Codex fast.
---

# Low-Token Context

Goal: get enough evidence to act without loading the whole project.

## Workflow

1. Run a compact repo snapshot when the repo is unfamiliar:
   `scripts/repo_snapshot.sh <repo>`.
2. Estimate heavy files before reading broadly:
   `scripts/token_budget.sh <repo>`.
3. Search first with `rg`, `git diff`, package manifests, and exact symbols.
4. Read only the files needed to state:
   - edit surface
   - invariants
   - verification command
   - known risks
5. Write or update a small task brief if the work will continue across turns.

## Task Brief Contract

```md
# Task Brief
## Goal
## Relevant Files
## Current Behavior
## Required Change
## Constraints
## Verification
## Open Risks
```

## Stop Rules

- Stop exploring once new files are repeating facts.
- Summarize command output instead of pasting logs.
- Store durable project facts in markdown memory; do not repeat them in every prompt.
- For codebase graph tools, request exact symbols or files rather than broad "explain everything" queries.

Read `references/low-token-patterns.md` for budgets and anti-patterns.

## Validation

- Context includes the goal, edit surface, constraints, verification, and risks.
- Large logs or broad file reads are summarized instead of pasted.
- Durable facts are written to memory/wiki only when they will help future sessions.
