---
name: source-driven-development
description: >
  Read and understand existing code before writing any modifications.
  Use when modifying any existing codebase. Follow established patterns,
  conventions, and architecture rather than introducing new ones.
version: 1.0.0
permissions:
  - fs.read
triggers:
  - context: "modifying existing code"
  - context: "adding to an existing codebase"
  - context: "working in an unfamiliar codebase"
  - command: "/build"
platforms:
  - claude-code
  - cursor
  - gemini-cli
  - copilot
  - codex
  - opencode
  - windsurf
  - kiro
model_variants:
  claude:
    enforcement_style: "human-partner collaborative"
  gemini:
    enforcement_style: "structured-checklist"
  gpt:
    enforcement_style: "directive-imperative"
author: codehands-core
signed: true
tier: 0
---

## Overview

The fastest way to introduce bugs is to modify code you haven't read. Source-driven development mandates reading before writing — understand the existing patterns, then follow them. Your code should look like it was written by the same author as the surrounding code.

## When to Use

- When modifying ANY existing codebase
- When adding features to an existing project
- When fixing bugs in unfamiliar code
- When joining a project for the first time
- NOT for greenfield projects with no existing code

## Process

### 1. Read Before Write

Before modifying any file, read:
- **The file you'll change** — all of it, not just the function
- **Files that import/call your target** — understand callers
- **Files that your target imports/calls** — understand dependencies
- **Related test files** — understand expected behavior

### 2. Identify Existing Patterns

Look for and follow:
- **Naming conventions** — How are variables, functions, files named?
- **Error handling patterns** — try/catch? Result types? Error callbacks?
- **Import organization** — Grouped? Sorted? Relative vs. absolute?
- **Testing style** — Describe blocks? Flat tests? Fixtures? Mocks?
- **Architecture patterns** — MVC? Hexagonal? Feature-based folders?

### 3. Follow, Don't Invent

```
GOOD: Follow the existing pattern even if you know a "better" one
BAD:  Introduce a new pattern because it's "modern" or "cleaner"
```

If the codebase uses callbacks, use callbacks. If it uses async/await, use async/await. Consistency is more valuable than local improvement.

### 4. Exception: Targeted Improvements

If existing code has problems that DIRECTLY affect your task (e.g., a file that's too large, unclear boundaries), include targeted improvements as part of your change. But:
- Only improve what's in the path of your change
- Don't propose unrelated refactoring
- Call out the improvement explicitly in your commit message

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I can figure out the code as I go" | You can't. You'll make assumptions that conflict with the actual design. Read first. |
| "The existing code is bad, I should use better patterns" | Consistency beats local quality. Mixing patterns makes the codebase harder to understand for everyone. Fix patterns in a dedicated refactoring task, not mid-feature. |
| "Reading the whole file is too slow" | Reading a file takes 30 seconds. Debugging a misunderstanding takes 30 minutes. Read the file. |
| "I've worked with similar codebases before" | Similar is not identical. Every codebase has unique conventions. Read this one. |

## Red Flags

- Modifying a file without reading it first
- Introducing a new pattern not used elsewhere in the codebase
- Code that looks stylistically different from surrounding code
- Not reading test files before modifying tested code

## Verification

- [ ] Target file and its direct dependencies read before modification
- [ ] Existing naming conventions identified and followed
- [ ] Existing patterns (error handling, testing, architecture) followed
- [ ] No new patterns introduced without explicit justification
- [ ] Related test files read and understood

## See Also

- `codehands:context-engineering` — How to manage context while reading
- `codehands:code-simplification` — When targeted improvements are warranted
- `codehands:code-review-and-quality` — Review for pattern consistency
