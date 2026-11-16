---
name: book--the-pragmatic-programmer--nano
description: >-
  The Pragmatic Programmer (Hunt & Thomas) — Minimal rules — essential one-liners only. Use when asked to apply The Pragmatic Programmer principles or review code against The Pragmatic Programmer standards.
origin: "github.com/ciembor/agent-rules-books (MIT)"
license: MIT
version: "1.0.0"
compatibility: "yana-ai >= 0.14.0"
---

# OBEY The Pragmatic Programmer by Andrew Hunt and David Thomas

## When to use

Use when you need a compact always-on engineering bias toward accountability, adaptability, and fast feedback.

## Primary bias to correct

Local code changes still have system-level consequences. Own the result beyond the edit.

## Decision rules

- Be pragmatic, not dogmatic: choose what improves real outcomes, not ceremony or shortcuts.
- Keep one authoritative source for each piece of system knowledge.
- Preserve orthogonality so unrelated concerns, business rules, views, and volatile details do not change together.
- Keep important choices reversible until evidence justifies commitment.
- Learn through thin working slices, prototypes, examples, tests, and fast feedback without fossilizing shortcuts.
- Automate repeatable work, keep it versioned, and favor inspectable text or scripts where longevity and recovery matter.
- Make assumptions, contracts, failure boundaries, diagnostics, resource ownership, cleanup, and ordering explicit.
- Treat shared mutable state, globals, ambient context, and async complexity as visible costs.
- Debug from reproduced facts and measured behavior, not coincidence or blame.
- Run relevant automatic tests before calling work done.
- Dig for real requirements behind stated solutions and current implementation details.
- Leave touched code, docs, tests, tooling, and process in a condition you can stand behind.

## Trigger rules

- When knowledge is copied, choose one owner and derive or trace the rest.
- When changes fan out widely, restore orthogonality.
- When a decision is uncertain or hard to reverse, seek feedback or make the step smaller.
- When manual steps repeat, automate and version them.
- When behavior is unexplained, generated, scaffolded, or tool-derived, inspect and prove it before relying on it.
- When errors, resources, state, locks, or ordering cross boundaries, make recovery and cleanup ownership explicit.
- When requirements sound like implementation details, restate the durable need before building.

## Final checklist

- One owner?
- Localized change?
- Reversible choice?
- Fast feedback?
- Explicit failures, state, and cleanup?
- Automated tests and rituals?
- Result worth standing behind?
