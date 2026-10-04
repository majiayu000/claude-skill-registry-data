---
name: implement
description: Standard workflow for implementation tasks. Use when adding new features, modifying existing ones, or refactoring. Triggered by requests to implement, add, create, or change something.
---

# Implementation Workflow

This skill prevents jumping straight to code by enforcing the sequence: Investigate → Plan → Approval → Implement.

---

## Phase 1: Investigate

Always do this before writing any code.

### 1-1. Clarify the Task

If the request is ambiguous, **ask first — do not implement**:

- "Which screen or feature should this be added to?"
- "What is the expected behavior?"
- "Should this integrate with existing X, or be standalone?"

### 1-2. Read Existing Code

```
Investigation priority order:
1. Files directly related to the task (files the user mentioned)
2. Check if a similar feature already exists (DRY principle)
3. Files that will be affected by the change
4. Related test files
```

Use the Explore agent when:
- Three or more files are likely involved
- It is unclear where the implementation should live
- A broad impact across the codebase is expected

### 1-3. Check Constraints

- Does it conflict with security rules (`.claude/rules/security.md`)?
- Does it follow existing architectural patterns?
- Will `npm run build` pass after the change?

---

## Phase 2: Present a Plan

After investigation, present the plan **before writing any code**.

### Plan Format

```
## Investigation Summary
- Related files: [list]
- Existing similar feature: [description, or "none"]
- Impact scope: [files that will change]

## Implementation Options

### Option A: [approach name]
- Overview: [1-2 lines]
- Pros:
- Cons:

### Option B: [approach name] (if applicable)
- Overview:
- Pros:
- Cons:

## Recommendation
Option A is recommended. Reason: [brief]

## Files to Change (Option A)
- `path/to/file.ts` — [what changes]
- `path/to/other.ts` — [what changes]

Shall I proceed?
```

### Stop Point

After presenting the plan, **always stop**. Wait for the user's approval.
Do not start implementing after asking "Shall I proceed?" without waiting for a response.

---

## Phase 3: Implement

Implement only after receiving explicit approval.

### Principles

- **Implement only what was approved** — no "while I'm at it" additions
- **No unrequested refactoring, comment additions, or type improvements**
- **Change one file at a time and build incrementally**

### Completion Check

```bash
npm run build   # required
```

After the build passes, explicitly state "Implementation complete."

---

## Phase 4: Report

```
## Implementation Complete

Changed files:
- `path/to/file.ts`: [one-line summary of what changed]

npm run build: ✅ passed
```

No extra explanation or summary needed. The user can read the diff.
