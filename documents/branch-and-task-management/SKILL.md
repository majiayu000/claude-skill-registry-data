---
name: branch-and-task-management
description: "Create feature branches with naming conventions, load full issue context and impact analysis, and decompose acceptance criteria into atomic parallel tasks with dependencies. Use when starting work on a GitHub issue. This skill MUST be consulted because starting code without context causes misaligned implementations and wasted effort."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, TaskCreate, TaskList, TaskUpdate, TaskGet
context: fork
agent: general-purpose
---

# Branch and Task Management

## Contract

Iron law: no code before context — read the issue body and comments, load history, understand scope, then create the branch. Invoked by `/flow:start` (Phase 1 EXPLORE through Phase 2 PLAN) and by the `implementation-planner` agent for task decomposition. Returns: a feature branch named per `conventions.branchPatterns` checked out from the default branch, one TaskCreate task per acceptance criterion with dependencies set, and an initialized decision journal at `{JOURNAL_DIR}/issue-{N}.md`. Permitted skips: none — an issue without acceptance criteria is not decomposed; it goes back to the user (or `Skill(issue-crafting)`) first.

## Pre-Conditions

Before creating a branch, confirm: the issue exists and is OPEN; it has acceptance criteria (otherwise ask the user or create them); no existing branch already addresses it; you have read the full body AND comments.

## Branch Creation

```bash
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name' 2>/dev/null || printf '%s\n' "main")
git fetch origin "$DEFAULT_BRANCH"
git checkout -b "feature/issue-{N}-{desc}" "origin/$DEFAULT_BRANCH"
```

Patterns from `settings.json` → `conventions.branchPatterns`: `feature/issue-{N}-{desc}`, `fix/issue-{N}-{desc}`, `docs/issue-{N}-{desc}`. `{desc}` is 3-5 kebab-case words.

## Issue Context Loading

Fetch in parallel: `gh issue view $N --json title,body,labels,assignees,milestone` and `gh issue view $N --comments`. Extract: title; acceptance criteria (each `- [ ]` item becomes a task); labels (inform approach); related issues.

## Impact Analysis

Grep for issue keywords and check `git log --oneline -10 -- <related path>`. Map acceptance criteria to likely file changes. Flag when the issue touches multiple modules (coordination), shared utilities (side-effect risk), or test fixtures (cross-suite updates).

## Task Decomposition

For each acceptance criterion:

```
TaskCreate(
  subject: "Implement: {criterion summary}",
  description: "Acceptance criterion: {full text}\nLikely files: {paths}\nVerification: {how to check}"
)
```

Rules: at least one task per criterion; add infrastructure tasks (migrations, config) when needed; add a verification task at the end; set dependencies with addBlockedBy for sequential work.

## Parallel Task Detection

Different files with no shared imports, or different directories → parallelizable. Same file → sequential dependency. If agent teams are enabled and >5 criteria have independent file sets → suggest team dispatch.

## Decision Journal Init

Create `{JOURNAL_DIR}/issue-{N}.md` (default `.decisions/`):

```markdown
# Decision Journal: Issue #{N} — {title}
**Issue**: #{N} | **Branch**: {branch-name} | **Started**: {YYYY-MM-DD}
---
```

The autonomous-workflow skill governs ongoing entry format (Init/Log/Summarize).

## Verification

Branch setup is valid when: the branch name matches a convention pattern; issue details loaded; at least one task per acceptance criterion; no circular dependencies; journal initialized.
