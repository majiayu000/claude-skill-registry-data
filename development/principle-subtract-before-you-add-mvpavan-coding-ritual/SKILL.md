---
name: principle-subtract-before-you-add
description: Apply when sequencing an addition, refactor or rewrite.
disable-model-invocation: true
---

# Subtract before you add

Build on the simplest base the change allows.

- Before adding, remove the dead code, redundant validators and stubs the
  change touches; report other removals instead of making them.
- When refactoring, or tempted to add an abstraction, a layer or a threaded
  signal, prefer deleting code to adding it.
- Delete a reference that carries nothing of its own rather than leave a stub
  pointing elsewhere.
- Keep each meaning in one authoritative place, so changing it is a
  one-place edit.
- Reach the minimum version before investing in its quality.
