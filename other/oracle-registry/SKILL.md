---
name: oracle-registry
description: "Build Oracle registry surfaces for skills, packages, and installs. Use when the task touches local skill packs, discovery, publishing, or install/update flow on this OS."
triggers: ["oracle-registry"]
scope: harness
invocation: ability
---

# Oracle Registry

Use this skill when the task is to discover, package, install, or publish skills and tools.

## Focus

- Keep `SKILL.md` small and readable.
- Prefer one skill directory per capability.
- Use references only when the detail is too large for the top level.
- Reuse the ClawHub and OpenClaw registry patterns as the default shape.

## Output

- Package layout.
- Install or publish path.
- Naming and discovery rules.

## Rules

- Avoid underscore-heavy visible labels.
- Keep compatibility notes explicit.
- Do not introduce extra docs unless they reduce repeated reasoning.

## Session Notes

### 2026-05-05
- session: patch | tools: Edit, Write | errors: none | notes: wired for CLI routing via triggers array and command alias
