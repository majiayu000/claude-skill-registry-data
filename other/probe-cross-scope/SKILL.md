---
name: probe-cross-scope
description: Benchmark skill for testing cross-scope dependency resolution. Install at project level; it references a skill expected at user level. Use when asked to probe cross-scope dependencies.
---

# Cross-Scope Dependency Probe

This skill is designed to be installed at project level (in the repository's
`.agents/skills/` or equivalent). It references `probe-loading`, which should
be installed at user level (in the user's home directory skills location).

This tests whether a project-level skill can invoke a user-level skill, and
what happens when the user-level skill is not installed.

## Instructions

When activated:

1. Report: "probe-cross-scope activated. Canary: **CRANE-STEEL-1163**"

2. Report your installation scope: Are you a project-level skill or a
   user-level skill? (This tests whether the platform exposes scope
   information to the model.)

3. Now activate the `probe-loading` skill. Report what happens:
   - Did the platform find `probe-loading`?
   - If found, was it at the same scope (project) or a different scope (user)?
   - If not found, what was the failure mode?

4. Report: "probe-cross-scope complete. Cross-scope resolution result:
   [describe what happened]"
