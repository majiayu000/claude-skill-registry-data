---
name: triage-issue
description: Use when user reports a bug, wants to file an issue, mentions "triage", when investigating a production problem before fixing it, when planning a fix that needs a TDD-shaped GitHub issue, or when a bug needs root-cause analysis before assignment.
---

# Triage Issue

## Overview

Investigate a reported problem, find its root cause, and create a GitHub issue with a TDD fix plan. Exploration-first — no guessing. The issue is written in terms of behaviors and contracts, not file paths or line numbers, so it stays useful after refactors.

## When to Use

- User reports a bug or unexpected behavior
- User wants to file a GitHub issue before implementing a fix
- User says "triage", "investigate", or "what's causing this"
- Bug needs a structured fix plan before work begins

## When NOT to Use

- Root cause is already known — go straight to `debugging-and-recovery`
- No GitHub repo exists — you can't create the issue
- The problem is a missing feature, not broken behavior — use `spec-driven-development`

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "I know what's wrong, I'll skip investigation" | You know the symptom. Cause is found by tracing, not guessing |
| "The fix is obvious — no need for a plan" | Obvious fixes skip TDD cycles and reintroduce the bug |
| "I'll reference the file and line in the issue" | File paths rot — write behaviors and contracts, not pointers |
| "I'll ask the user for more details before investigating" | Codebase exploration answers more than follow-up questions |

## Red Flags

- Issue body names specific file paths or line numbers (stale after any refactor)
- Root cause described as "it just wasn't working" — that's a symptom, not a cause
- TDD fix plan has more than 6 RED/GREEN cycles (not a vertical slice — decompose)
- Fix plan describes internal state changes, not observable behavior changes

## Core Process

### 1. Capture the problem

Get a brief description from the user. If none provided, ask ONE question: "What's the problem you're seeing?" Do NOT ask follow-up questions — start investigating immediately.

### 2. Explore and diagnose

Use the Agent tool with subagent_type=Explore to find:

- **Where** the bug manifests (entry points, UI, API responses)
- **What** code path is involved (trace the flow)
- **Why** it fails (root cause, not symptom)
- **What** related code exists (similar patterns, tests, adjacent modules)

Look at: related source files, existing tests, recent changes (`git log` on relevant files), error handling in the code path, similar patterns that work correctly.

### 3. Identify the fix approach

Based on investigation, determine:
- The minimal change to fix the root cause
- Which modules/interfaces are affected
- What behaviors need to be verified via tests
- Whether this is a regression, missing feature, or design flaw

### 4. Design TDD fix plan

Ordered list of RED-GREEN cycles. Each is one vertical slice:

- **RED**: A specific test that captures the broken/missing behavior
- **GREEN**: The minimal code change to make that test pass

Rules: tests verify behavior through public interfaces, not implementation details. One test at a time. Each test must survive internal refactors.

### 5. Create the GitHub issue

Use `gh issue create`. Do NOT ask the user to review before creating — create it and share the URL.

<issue-template>

## Problem

[What happens (actual) vs what should happen (expected). How to reproduce.]

## Root Cause Analysis

[Code path, why it fails, contributing factors — no file paths or line numbers]

## TDD Fix Plan

1. **RED**: Write a test that [describes expected behavior]
   **GREEN**: [Minimal change to make it pass]

2. ...

**REFACTOR**: [Any cleanup needed after all tests pass]

## Acceptance Criteria

- [ ] Criterion 1
- [ ] All new tests pass
- [ ] Existing tests still pass

</issue-template>

After creating: print the issue URL and a one-line root cause summary.

## Verification

- [ ] Codebase explored before drawing conclusions
- [ ] Root cause identified (cause, not symptom)
- [ ] TDD fix plan uses observable behaviors, not implementation details
- [ ] Issue body contains no file paths or line numbers
- [ ] Each RED/GREEN cycle is a vertical slice
- [ ] GitHub issue created and URL returned to user
