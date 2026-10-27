---
name: autoresearch:fix
description: |
  Iterative error-crusher loop that auto-stops at 0 errors. Cascade-aware: fixes
  dependency errors before their dependents. Refuses anti-patterns that hide errors
  instead of fixing them.
  TRIGGER when: user has errors or failures to fix iteratively; user asks to "fix all errors";
  user has a failing test suite; user has compilation errors; user has linter errors;
  user wants systematic error elimination; user invokes /autoresearch:fix.
  DO NOT TRIGGER when: user wants a one-shot fix for a single obvious bug; user wants
  debugging guidance only; user wants code review without fixing.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebFetch
  - WebSearch
---

# autoresearch:fix

Iterative error-crusher loop. Counts errors, prioritizes by dependency order, fixes the
highest-priority error, recounts. Stops automatically at 0 errors. Refuses to suppress,
hide, or work around errors.

## Autonomy Directive

**You are an autonomous error-fixing agent.** Once the loop begins:

1. **NEVER STOP** to ask permission between iterations.
2. **NEVER ASK** "should I continue?" while errors remain.
3. **NEVER DECLARE DONE** until the error count is confirmed to be 0.
4. **The loop runs until:** error count reaches 0, OR max iterations exhausted, OR user interrupts.
5. **If errors remain and budget allows, begin the next iteration NOW.**

---

## Anti-Pattern Blocklist

The following patterns are **strictly forbidden**. If fixing an error would require any of
these, skip that approach entirely and find a real fix:

| Pattern | Why it is forbidden |
|---------|-------------------|
| `try: ... except: pass` | Silences the error without handling it |
| `try: ... except Exception: pass` | Same — swallows all exceptions |
| Commenting out a failing assertion | The assertion exists to catch real bugs |
| Adding `pass` to an empty `except` block | Hides the problem |
| Deleting a test to make it pass | Tests exist for a reason |
| Hardcoding expected values to match test output | Creates false positives |
| `# type: ignore` without explanation | Masks type errors without understanding them |
| `@pytest.mark.skip` without a linked issue | Permanently hides failures |
| Changing error thresholds to accommodate broken output | Moves the goalposts |

If a real fix is not possible in the current iteration, log the error as `BLOCKED` with the
reason, skip it, and attempt another error instead.

---

## Setup

### Step 1 — Identify the error source
Ask if not provided: "What command reveals the errors?" (e.g., `pytest`, `tsc`, `cargo build`,
`pylint`, `make`). Record as `error_command`.

### Step 2 — Run initial count
Execute `error_command`. Parse the output to count distinct errors.
Record as `errors_before` for iteration 1.

### Step 3 — Set budget
Default `max_iterations`: 20. User may override.

---

## Core Loop

```
iteration = 1
while errors > 0 and iteration <= max_iterations:

    1. COUNT: Run error_command. Parse output. Count distinct errors.
       Record errors_before for this iteration.

    2. PRIORITIZE: Build dependency graph of errors.
       If error A is caused by a missing import that error B would fix,
       fix B first (cascade priority).
       Rule: fix the error that is blocking the most other errors first.

    3. SELECT: Pick the highest-priority unfixed error.
       Skip BLOCKED errors unless all non-blocked errors are exhausted.

    4. ANALYZE: Read the affected file(s). Understand the root cause.
       Verify the proposed fix does not appear on the Anti-Pattern Blocklist.

    5. FIX: Apply the minimal change that resolves this error.
       Do not modify adjacent code unless it is directly causing the error.

    6. RECOUNT: Run error_command again. Count errors.
       Record errors_after for this iteration.

    7. LOG: Append row to fix-results.tsv.

    8. CHECK: If errors_after == 0 → done. Otherwise → next iteration.

iteration += 1
```

---

## Cascade Priority Rule

When multiple errors exist:

1. Build an implicit dependency graph:
   - If module A fails to import and modules B, C, D all import A → A's error is a blocker.
   - Fix A first; B, C, D errors may resolve automatically.
2. Always recount after each fix — a single fix can eliminate multiple dependent errors.
3. Never fix symptom errors before root-cause errors.

**Example:** TypeScript project has 12 errors. 9 of them are "cannot find name X" because
`types.ts` has a syntax error. Fix `types.ts` first → recount → likely 3 errors remain.

---

## Output

`fix-results.tsv` — written to the working directory, appended each iteration.

```
iteration	errors_before	errors_after	fix_applied	status
1	12	3	Fixed syntax error in types.ts (missing closing brace)	improved
2	3	1	Fixed null check in userService.ts line 42	improved
3	1	0	Fixed missing import in index.ts	done
```

Columns:
- `iteration` — integer
- `errors_before` — error count before this iteration's fix
- `errors_after` — error count after this iteration's fix
- `fix_applied` — one-line description of the change made
- `status` — one of: `improved`, `done`, `no_change`, `blocked`, `budget_exhausted`

---

## Termination Conditions

1. `errors_after == 0` → append `status: done` to final row → print summary → done.
2. `iteration > max_iterations` → append `status: budget_exhausted` → report remaining errors → done.
3. All remaining errors are `BLOCKED` → report blockers with reasons → done.
4. User manually interrupts → flush current state → done.

---

## Edge Cases

| Situation | Handling |
|-----------|----------|
| Error count increases after a fix | Revert the fix, log as `no_change`, try different approach |
| Two errors are mutually dependent (cycle) | Log both as `BLOCKED — cyclic dependency`, report to user |
| Error command is not provided | Ask once. Refuse to guess. |
| Error command times out | Wrap with `timeout 5m`. Exit 124 = timeout → skip this iteration |
| Same error persists for 3 iterations | Log as `BLOCKED — repeated failure`, skip and try others |
| Fix works but introduces a linter warning | Note in `fix_applied` — do not revert for warnings alone |
