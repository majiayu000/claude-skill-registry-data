---
name: architect
description: >
  Sketch types, signatures, and module structure before code, then stay in the loop
  while implementation fills in. The output is the shape of the code, not a task plan.
  Use on request ("architect this", "design this before coding") or as a step of a
  larger workflow, for non-trivial work where jumping to code would lock in the wrong
  shape. For a written plan of scope, phases and risks, use the `plan-change` skill.
license: MIT
metadata:
  upstream: cursor/plugins@d42aff08 pstack/skills/architect
---

# Architect

Before writing code, trace every system the change touches, then sketch two different shapes for it (types, signatures, module boundaries) and pick the one where each piece of state has one owner, each task has one way to do it, and callers need to know least. Redesign instead of patching if workarounds repeat.

When the shape in question is a module boundary, use the vocabulary in [deep-modules.md](references/deep-modules.md): a lot of behaviour behind a small interface, placed at a seam where something really varies.
