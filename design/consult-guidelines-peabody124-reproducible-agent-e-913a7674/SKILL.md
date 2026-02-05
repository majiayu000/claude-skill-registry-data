---
name: consult-guidelines
description: Review relevant guidelines before starting a task
---

## Overview

Read and internalize the coding guidelines relevant to the current task. This ensures consistent application of standards across all work.

## Parameters

- **task_type** (optional): "python", "git", "refactor", "debug", "review", or "all"

## Steps

### 1. Determine Relevant Guidelines

Based on task type, identify which guidelines to review.

**Mapping:**
- `python` → coding-standards.md, python-standards.md
- `git` → git-workflow.md
- `refactor` → coding-standards.md, anti-patterns.md
- `debug` → coding-standards.md (TDD section)
- `review` → anti-patterns.md, coding-standards.md
- `all` → all guidelines

**Constraints:**
- You MUST read `guidelines/coding-standards.md` for any code changes
- You MUST read `guidelines/python-standards.md` for Python work
- You MUST read `guidelines/git-workflow.md` before any commits
- You SHOULD read `guidelines/anti-patterns.md` before code review or refactoring

### 2. Summarize Key Points

Extract the 3-5 most relevant rules for the current task.

**Constraints:**
- You MUST highlight any MUST/MUST NOT constraints
- You SHOULD note any task-specific gotchas

### 3. Apply During Work

Keep these guidelines in mind while executing the task. Reference them when making decisions.

**Constraints:**
- You MUST cite the relevant guideline when it influences a decision
- You SHOULD flag if you discover a case not covered by guidelines

## Examples

**User:** "I'm about to refactor the auth module"
**Agent:** Reads coding-standards.md and anti-patterns.md, summarizes DRY principles and slop patterns to avoid, proceeds with refactor while citing guidelines.

**User:** "/consult-guidelines python"
**Agent:** Reviews coding-standards.md and python-standards.md, extracts key rules about ruff, type hints, and path management.
