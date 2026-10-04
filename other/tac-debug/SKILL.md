---
name: tac-debug
description: "Use when encountering any bug, test failure, unexpected behavior, or build error in TAC Express. ALWAYS find root cause before attempting a fix. No guessing."
---

# TAC Express — Systematic Debugging

> **Iron Law:** NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.
> Symptom fixes are failure. Random fixes waste time and create new bugs.

---

## The Four Phases

You MUST complete each phase before proceeding to the next.

### Phase 1: Root Cause Investigation

**Before touching any code:**

1. **Read the error completely**
   - Full stack trace, not just the last line
   - Note file paths, line numbers, error codes
   - Check for nested errors (`cause:` property)

2. **Reproduce consistently**
   - Can you trigger it every time?
   - Is it browser-specific? Node version? OS?
   - What are the exact steps?

3. **Check recent changes**
   - `git log --oneline -20` — what changed?
   - `git diff HEAD~3..HEAD` — what's different?
   - New package install? Config change?

4. **For multi-package errors (common in this monorepo):**
   ```bash
   # Identify which package boundary fails:
   pnpm --filter @workspace/ui typecheck
   pnpm --filter @workspace/services typecheck
   pnpm --filter web typecheck
   pnpm --filter dashboard typecheck
   ```

5. **Trace data flow backward**
   - Where does the bad value originate?
   - UI → Service → Database — which layer breaks?
   - Add `console.error` at each boundary if unclear

### Phase 2: Pattern Analysis

1. Find working code that does something similar in this codebase
2. Compare working vs. broken — list every difference, however small
3. Check `DESIGN_SYSTEM.md` / `AGENTS.md` § 4 — is a rule being violated?
4. Check if a forbidden package was accidentally used

### Phase 3: Hypothesis & Test

1. State ONE specific hypothesis: _"I think X fails because Y"_
2. Make the SMALLEST change to test it
3. Verify result
4. If wrong: form NEW hypothesis — do NOT stack fixes

**Three strikes rule:** If 3+ different fixes have failed, STOP. The architecture may be wrong. Discuss before continuing.

### Phase 4: Implement the Fix

1. Write a failing test that captures the bug
2. Implement the minimal fix
3. Verify the test now passes
4. Verify no other tests broke
5. Commit with: `fix(scope): describe root cause and fix`

---

## TAC Express-Specific Debug Checklist

### Build Errors

```bash
# Run in order — each isolates a different layer:
pnpm typecheck                    # TypeScript errors
pnpm lint --max-warnings 0       # ESLint violations  
pnpm --filter @workspace/ui build # UI package builds?
pnpm build                        # Full monorepo build
```

### Common TAC Express Pitfalls

| Symptom | Likely Cause | Check |
|---------|-------------|-------|
| `Cannot find module '@workspace/ui'` | Build order issue | Run `pnpm build --filter @workspace/ui` first |
| CSS token not applying | Token not in `globals.css` | Check token name matches exactly |
| Supabase error in component | Direct DB call in component | Move to `packages/services` |
| `lucide-react` import error | Forbidden package | Replace with `@remixicon/react` |
| Hydration mismatch | `useEffect` missing deps | Check SSR/CSR boundary |
| Type error in service | Missing return type | Add explicit return type annotation |

### ESLint Violations Debug

```bash
# See all violations with context:
pnpm lint --max-warnings 0 2>&1 | head -100

# Fix auto-fixable:
pnpm lint --fix

# Check specific file:
pnpm dlx eslint packages/ui/src/components/MyComponent.tsx
```

### Turbopack / Next.js Issues

```bash
# Clear all caches:
Remove-Item -Recurse -Force apps/web/.next
Remove-Item -Recurse -Force apps/dashboard/.next
Remove-Item -Recurse -Force node_modules/.cache
pnpm dev
```

---

## Red Flags — STOP and Re-investigate

If you catch yourself:
- "Let me just try changing this and see..."
- Adding multiple fixes at once
- Skipping the test step
- "It's probably the same issue as before..."
- Proposing solutions before reading the error trace
- Attempting Fix #4 without discussing architecture

**All of these mean: STOP. Return to Phase 1.**

---

## Debug Notes Format

When documenting a resolved bug:

```markdown
## Bug: [short description]
Date: YYYY-MM-DD
Ticket: TAC-XXX

### Root Cause
[Exact explanation of what caused it]

### Evidence
[Stack trace, error message, or data that confirmed root cause]

### Fix
[What was changed and why it works]

### Prevention
[Test added, rule updated, or pattern to follow going forward]
```
