---
name: verify
description: >
  Run this after every code change in this Vue project, before committing,
  before opening a PR, or whenever the user says "verify", "check", "lint",
  "run tests", "build", "audit". Diff audit (router guards, store boundaries,
  UX, /ui consistency, error handling) → lint → tests + coverage gate →
  build. Coverage drops → add tests, never lower thresholds. Triggers on
  "is this ready to commit?", "any issues?", "tests passing?".
---

# Verify Skill

## Steps

1. **Diff audit** — review all changes (`git diff master...HEAD` or staged changes) using your knowledge of the stack:
   - Read `CLAUDE.md` and `ERRORS.md` for conventions, architecture, and known pitfalls
   - Read the `tasks` reference module structure for layer/naming conventions
   - Check `/ui` skill for design system and Vuetify conventions
   - Analyze the diff: architecture, security, UX, logic, consistency, error handling
   - No hardcoded checklist — reason from context. Examples of what to catch:
     - Router guards with permissive matching (startsWith vs exact)
     - Silent error swallowing (catch without user feedback)
     - Store mutations from outside the store
     - Cross-module store imports (only `useAuthStore`/`useCoreStore` allowed)
     - Missing form validation or confirmation dialogs on destructive actions
     - Inconsistent selectors in E2E tests (prefer getByRole/getByPlaceholder)
     - Broken or nonexistent route references
     - Store-contract tests that only assert a mock was called, not the resulting store state (interaction-only assertions let a dropped field slip through)
   - Fix all issues found before proceeding

2. **Lint** — `npm run lint`

3. **Tests + coverage** — check if Node API is reachable (`curl -sf http://localhost:3000/api/home`):
   - **Infra up** → `npm run test:coverage` (unit + coverage enforcement) then `npm run test:e2e` (Playwright E2E)
   - **Infra down** → `npm run test:coverage` (unit + coverage) + warn: "E2E skipped — run `docker compose -f docker-compose.test.yml up -d` for full coverage"
   - If coverage drops below thresholds (vitest.config.js) → fail. Add tests, never lower thresholds.

4. **Build** — `npm run build`

5. **Summary:** ✅ All passed → ready to commit | ❌ Failed → show failures, fix, re-run
