---
name: debug
description: Standard workflow for debugging tasks. Use when something is broken, an error occurs, or behavior is unexpected. Finds root cause before fixing — no random trial-and-error.
---

# Debug Workflow

This skill prevents "let's just try changing this" by enforcing the sequence: Identify Symptom → Find Root Cause → Present Diagnosis → Fix.

---

## Phase 1: Understand the Symptom

### What to Check

```
1. Full error message (do not summarize or skip lines)
2. Reproduction condition (when, which action, what input)
3. Expected behavior vs. actual behavior
4. When it started (relation to recent changes)
```

### Prohibited

```
// Prohibited: guessing without reading the error
"It's probably X." → immediate fix ← WRONG

// Correct
Read error message → trace stack → identify cause ← RIGHT
```

---

## Phase 2: Identify Root Cause

### Investigation Order

1. **Read the file where the error occurs**
   - Start from the top of the stack trace
   - Note the exact file name and line number from the error message

2. **Trace the call chain**
   - Where is this called from?
   - What data is being passed?

3. **Check recent changes**
   ```bash
   git log --oneline -10
   git diff HEAD~1
   ```
   - Did a recent commit touch a related file?

4. **Form a hypothesis based on evidence**
   ```
   // Prohibited: hypothesis without evidence
   "It's probably a cache issue." ← WRONG

   // Correct
   "In file X at line 42, value Y is null because
    function Z passes undefined from the caller." ← RIGHT
   ```

### Common Patterns (Baan project)

| Symptom | Where to look |
|---------|--------------|
| Build error | Full `npm run build` output, TypeScript error location |
| API returns 401 | `withAuth` present? Session cookie valid? |
| Settings not applied | `loadSettings()` key name, DB value, cache TTL |
| Test failing | `DATABASE_URL` pointing to `test.db`? Parallel execution? |
| Storage error | Provider config, credentials, bucket name |
| SSR hanging | Using `ssrFetch`? Direct `fetch` calls in Server Components are unsafe |

---

## Phase 3: Present the Diagnosis

**Always report the diagnosis before fixing.**

### Report Format

```
## Debug Result

### Root Cause
[file:line] — [what is happening and why]
Evidence: [relevant part of the error message or code]

### Fix
[what to change and how — 1-3 lines]

### Impact
- Files to change: [list]
- Side effects: [if any]

Shall I fix this?
```

### Stop Points

- Large impact (3+ files) → always get approval before fixing
- Small impact (1-2 files, clear fix) → ask "Shall I fix this?" and wait

---

## Phase 4: Fix

### Principles

- **Fix only the root cause** — no surrounding code improvements
- **Minimum change** — refactoring is a separate task
- Run `npm run build` after fixing

### Prohibited Patterns

```
// Prohibited: hiding the root cause
try {
  riskyOperation();
} catch (e) {
  // silently swallowing the error ← WRONG
}

// Prohibited: unrequested improvements
// "Fixed X, and also cleaned up Y while I was there." ← WRONG
```

---

## Phase 5: Report

```
## Fix Complete

Cause: [one line]
Fix: [file:line] — [what was changed]
npm run build: ✅

[One line for the user if there is anything to verify manually]
```
