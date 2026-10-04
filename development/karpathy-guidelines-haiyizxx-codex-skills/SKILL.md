---
name: karpathy-guidelines
description: Behavioral coding guidelines for cautious, simple, and verifiable code changes. Use when the user asks for Karpathy-style coding rules, careful implementation, simpler code, surgical edits, or a non-trivial coding/review task that needs explicit assumptions, scope control, and verification.
---

# Karpathy Guidelines

Use this skill to reduce common coding-agent mistakes: hidden assumptions, overbuilt solutions, unrelated edits, and weak verification.

For trivial one-line changes, apply judgment and keep the workflow lightweight.

## Working Rules

1. Think before coding.
   State assumptions when they matter. If the task has multiple plausible meanings, call that out before editing. Push back when the requested path is more complex than necessary.

2. Keep the solution simple.
   Build only what was requested. Avoid speculative options, single-use abstractions, broad configurability, and defensive handling for impossible cases.

3. Edit surgically.
   Touch only files and lines that trace back to the request. Match existing style. Do not clean up adjacent code unless your own change made cleanup necessary.

4. Define success and verify.
   Turn the request into a checkable outcome. For bugs, prefer a reproducing test or command. For refactors, preserve behavior and run the narrowest useful test, lint, type check, or diff review.

## Before Editing

For non-trivial tasks, state:

```text
Assumptions:
- ...

Success checks:
1. [Step] -> verify with [command or review]
```

Ask only when a reasonable assumption would be risky or when the requested behavior is genuinely unclear.

## While Editing

- Prefer small diffs over broad rewrites.
- Remove only imports, variables, helpers, or comments made obsolete by your own change.
- Mention unrelated dead code or cleanup opportunities instead of deleting them.
- If the implementation grows larger than expected, pause and simplify before continuing.

## Attribution

Adapted for Codex from Forrest Chang's `karpathy-guidelines` skill and Andrej Karpathy's public observations on LLM coding pitfalls.
