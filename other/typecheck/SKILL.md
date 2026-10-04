---
name: typecheck
description: Run TypeScript type-check on both apps/web and apps/api in parallel and report errors. Use after any code change before saying work is "done", and as a precondition for /complete-session and /commit-and-track.
---

# typecheck

Fast type-check across the monorepo. Required before declaring any work complete.

## Steps

1. **Run both checks in parallel** with two `Bash` calls in the same message:
   ```bash
   cd apps/web && npx tsc --noEmit
   cd apps/api && npx tsc --noEmit
   ```
2. **Parse output** — count errors per file, highlight the most-recently-touched files first (those are usually the cause).
3. **Report** to the user as a clean summary:
   ```
   apps/web: ✅ 0 errors  (or)  ❌ 3 errors in 2 files
   apps/api: ✅ 0 errors
   ```
4. **If errors exist**, group them by file and propose fixes only for files you touched in this session. Don't try to fix preexisting drift unless the user asks.
5. **If both clean**, that's the entire response — no preamble.

## Verification

- [ ] Both apps checked
- [ ] Errors grouped clearly
- [ ] Preexisting errors flagged separately from new ones

## Notes

- This project uses `prisma generate` to create types — if errors mention missing Prisma types, run `cd data/schema && npx prisma generate` first
- A `cd ... && npx tsc` taking >60 seconds usually means a stale `.tsbuildinfo` — delete and retry
