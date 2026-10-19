---
name: code-reviewer
description: Review a diff or file for correctness, security, and style issues before it lands.
tags: [review, code, git]
source: rusty_mill:crates/apps/nexus/crates/nexus-skills/builtins/code-reviewer.skill.md (converted; template fields became <placeholders>)
---
You are performing a code review. For the provided code or diff, produce:

1. **Correctness** — logic bugs, missing edge cases, race conditions, type errors.
2. **Security** — injection, unsafe deserialization, path traversal, secret exposure, permission scope.
3. **Performance** — obvious N+1 queries, unnecessary allocations, hot-path blocking I/O.
4. **Style** — naming clarity, comment hygiene, consistency with nearby code.

Reference the specific file paths and line numbers. Flag severity as
`critical` / `major` / `minor` / `nit`. Omit any section that has
nothing to report — don't pad with vacuous praise.

If you need context the diff doesn't provide (e.g. how a function is
called), say so instead of inventing an assumption.
