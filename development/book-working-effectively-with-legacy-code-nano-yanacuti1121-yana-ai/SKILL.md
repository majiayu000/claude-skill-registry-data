---
name: book--working-effectively-with-legacy-code--nano
description: >-
  Working with Legacy Code (Michael Feathers) — Minimal rules — essential one-liners only. Use when asked to apply Working with Legacy Code principles or review code against Working with Legacy Code standards.
origin: "github.com/ciembor/agent-rules-books (MIT)"
license: MIT
version: "1.0.0"
compatibility: "yana-ai >= 0.14.0"
---

# OBEY Working Effectively with Legacy Code by Michael Feathers

## When to use

Use when changing poorly tested or poorly understood code under a tight context budget.

## Primary bias to correct

Legacy work starts with control, not cleanup, rewrite, or elegance.

## Decision rules

- Treat code without trustworthy tests as legacy code: state what changes and what must remain.
- Characterize uncertain current behavior before changing it, including ugly behavior consumers may rely on.
- Use the legacy loop: find the change point, find an observation point, create or exploit a seam, break the blocking dependency, test, change, then refactor locally.
- Prefer fast focused tests; use broader harnesses only as temporary first coverage when no narrow test point exists.
- Create the narrowest useful seam for sensing or separation, and break only dependencies that block feedback.
- Use sprout, wrap, parameterize, inject, extract, or override moves when direct edits would be unsafe.
- Keep behavior changes, structural refactorings, and cleanup separate and small.
- Do not leave test-only seams, hidden dependencies, wrappers, globals, subclass tricks, or link/preprocessor tricks without a cleanup plan.

## Trigger rules

- When behavior is unclear, characterize first.
- When constructors, globals, statics, frameworks, I/O, clocks, randomness, environment, or deep object graphs block testing, break one dependency at the narrowest point.
- When a large method or class defeats local reasoning, sketch effects and create a seam before semantic edits.
- When rewrite or broad cleanup feels tempting, choose the next smaller verified move.

## Final checklist

- Behavior characterized?
- Feedback fast enough?
- Dependency isolated?
- One kind of change?
- Safer and clearer now?
