---
name: resolving-merge-conflicts
description: "Use when you need to resolve an in-progress git merge/rebase conflict."
---

1. **See the current state** of the merge/rebase. Check git history, and the conflicting files.

2. **Find the primary sources** for each conflict. Understand deeply why each change was made, and what the original intent was. Read the commit messages, check the PRs, check original issues/tickets.

3. **Resolve each hunk.** Preserve both intents where possible. Where incompatible, pick the one matching the merge's stated goal and note the trade-off. Do **not** invent new behaviour. Always resolve; never `--abort`.

4. Discover the project's **automated checks** and run them, typically typecheck, then tests, then format. Fix anything the merge broke.

5. **Finish the merge/rebase.** Stage everything and commit. If rebasing, continue the rebase process until all commits are rebased.

## Travel-Tool context

Vendored from mattpocock/skills (see `.claude/ECC.md`, section *Also vendored*).

- **Never hand-merge `package-lock.json`.** Take either side, then run `npm install` in that package (`backend/`, `web/` or `mobile/app/`) to regenerate it, and check that `npm ci` passes.
- **Never hand-merge `backend/src/utils/schema.sql`.** It is a `pg_dump` of the live DB. Resolve it by taking the newer dump, and if both sides added migrations, ask the user to rerun `backend/scripts/refresh-ci-schema.sh` on the VPS.
- Numbered migration files (`backend/src/utils/migrations/NNN_*.sql`) that collide on a number: renumber the one that has **not** been applied to production. Ask if unsure; applied files must not be renamed.
- Checks: `cd backend && npm run build && npm run lint && npm test`, plus `npm run lint` in `web/` or `mobile/app/` if they were touched.
- On a branch someone else owns, merge rather than rebase, and never force-push.
