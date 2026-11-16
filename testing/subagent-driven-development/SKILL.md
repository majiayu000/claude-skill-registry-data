---
name: subagent-driven-development
description: Split a substantial task among independent agents when the harness supports delegation. Use only when parallel work reduces elapsed work without creating conflicting edits.
---

# Subagent-Driven Development

Delegate bounded tasks, not vague ownership of the whole problem.

1. Decide whether work can truly run in parallel. Identify dependencies and shared files first.
2. Define interfaces, assumptions, ownership, expected artifacts, and completion checks for each workstream.
3. Give each worker only relevant context and a narrow assignment. Prefer read-only review delegation when write conflicts are likely.
4. Keep a single integration owner responsible for contracts, security, cross-workstream consistency, and final verification.
5. Avoid agents editing the same files or mutating the same branch concurrently.
6. Inspect all returned diffs and evidence; do not accept an agent's completion claim without checking.
7. Run integration tests after merging contributions and report which tasks were delegated.

If subagents are unavailable, continue sequentially. Do not pretend a task was delegated, and do not spawn agents merely to create activity. Keep human approval around external, destructive, or high-impact actions.
