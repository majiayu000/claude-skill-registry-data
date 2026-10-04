---
name: minimal-code
description: Use this skill alongside the build skill to resist over-engineering. Enforces YAGNI (no speculative features), KISS (the simplest thing that could possibly work), and DRY-when-it-actually-repeats (not DRY-in-advance). Prefer standard library over new dependencies. Prefer editing existing code over creating new files. Prefer adding one function over adding one class. Prefer flat over nested. Trigger proactively whenever Claude is tempted to introduce an abstraction, a new dependency, a new module, a helper class, a framework, a pattern, or a layer of indirection during Build.
---

# Minimal Code

Resist the urge to write more than necessary.

## Principles

- **YAGNI.** You aren't gonna need it. No speculative parameters, no "for future extensibility" hooks, no configuration for cases that don't exist.
- **KISS.** The simplest thing that could possibly work. If there's a one-line solution and a three-class solution, the one-liner wins until there's a concrete reason it doesn't.
- **DRY when it actually repeats.** Three occurrences before you extract a helper. Two might be coincidence. One is always coincidence.
- **Flat over nested.** Shallow call graphs, few layers, fewer indirections. Each extra layer is a place a future reader has to stop and look up.
- **Delete more than you add, when you can.** Touching a function is a chance to remove dead code that the function actually owns. (But not code it doesn't own — see `surgical-edit`.)

## Heuristics

### Dependencies
- Can the standard library do this? Use it.
- Is a dependency already present that covers this? Use it.
- A new dependency needs: justification in the plan, license check, maintenance check, bundle/runtime impact.

### Abstractions
- New class? Only if there's state *and* behavior *and* multiple call sites.
- New interface/protocol? Only if there are or will soon be multiple implementations — not "might be someday."
- New module? Only if the code doesn't fit the theme of an existing one.

### Configuration
- Hardcode first, extract to config when a second value appears.
- Feature flags for actual rollouts, not for "maybe someday."

### Indirection
- Don't wrap a library call in a function that does nothing but call it.
- Don't add a factory when a constructor works.
- Don't add a service layer when the call site is the only caller.

## The "one-function rule"

Before adding a new class, ask: would a single function do? Before adding a new module, ask: would a single function in an existing module do? Before adding a new file, ask: would three lines in an existing file do?

## Lines-of-code signal

Track LOC delta per task (the `/ship` command reports it). A steady upward trend without feature growth is a signal of over-engineering. A feature that shrinks the codebase is a win.

## What this skill must NOT do

- Don't celebrate removing code that's actually load-bearing.
- Don't delete tests to hit a LOC target.
- Don't over-minimize to the point of one-letter variable names and uncommented dense logic.

## References

- `skills/surgical-edit/SKILL.md`
