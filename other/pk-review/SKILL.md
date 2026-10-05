---
name: pk-review
description: "Review the current branch's changes against the project's code style and"
---

Review the current branch's changes against the project's code style and
conventions documented in AGENTS.md. Check for:

- Adherence to the project's commit conventions (Conventional Commits:
  `feat:`, `fix:`, `refactor:`, `docs:`, `chore:`).
- Code style violations (80-column wrap, .editorconfig rules).
- Security concerns (OWASP Top 10 relevant to the changed code).
- Test coverage gaps introduced by the changes.
- processkit compliance-contract adherence (entity writes via MCP tools,
  no hand-edits to `context/templates/`, `route_task` called before
  create/transition/link/record/open tools).

Summarise findings as a structured review with severity levels:
**blocker** / **warning** / **note**.
