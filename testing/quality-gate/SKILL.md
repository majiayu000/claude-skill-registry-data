---
name: quality-gate
description: "Quality gate enforcement — TDD, lint, type-check, test, build checks before any commit or PR"
applyTo: "agents/*.agent.md"
---

# Quality Gate

Before any commit, push, or PR, ALL CI/CD checks MUST pass:

- `ruff check .` — zero errors
- `npx tsc --noEmit` — zero errors
- `pytest .` — 100% passing
- `npm run build:web` — no critical warnings

**Rules:**
- No commits with broken lint/type/test/build
- "Fix later" is not accepted
- If a test fails due to legitimate change, UPDATE the test, don't remove it
- The developer (not CI) is responsible for running checks BEFORE push
