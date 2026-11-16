---
name: blue-team-fix
description: >
  Defensive response to red team security findings — analyze each vulnerability,
  propose a targeted fix, and add a test that covers the fix. Use when the user
  has a security finding list (from red-team-check or a manual audit) and wants
  to fix the vulnerabilities. Produces: root cause analysis, code fix, and test.
  Does not auto-apply fixes — proposes and waits for user approval per fix.
origin: yamtam
version: 1.0.0
compatibility: >
  Expects input in red-team-check finding format. Works on local codebase.
  Does not auto-commit. Does not auto-apply — proposes per fix.
---

<!-- Concept inspired by Strix (Apache 2.0) — defensive security framing.
     All content written original for YAMTAM. No code ported. -->

## When to Use

- After running red-team-check and receiving a finding list
- When user shares a security audit report and wants fixes
- When a CVE or bug report references specific vulnerabilities in the codebase
- When a penetration test report needs to be remediated

Do NOT use:
- Without a finding list — always needs red-team-check output or equivalent as input
- To auto-apply fixes without user review — propose only, never apply unilaterally

## How It Works

### Step 1 — Triage Finding List

Read all findings from input. Prioritize by severity:
```
CRITICAL → fix first, block deploy if unresolved
HIGH     → fix before next release
MEDIUM   → fix in current sprint
LOW      → track in backlog, fix opportunistically
INFO     → no action required, document only
```

Output a triage table before starting any fixes:
```
| # | Severity | Category | Title | Fix Priority |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | A02 | Hardcoded DB password | P0 — fix now |
| 2 | HIGH     | A01 | IDOR on /api/users/:id | P1 — before release |
```

### Step 2 — Per Finding: Root Cause → Fix → Test

For each finding (start with CRITICAL, work down):

**Root Cause Analysis**
```
What pattern caused this?
  - Missing input validation
  - Hardcoded value that should be env var
  - Missing auth check
  - Unsafe library call
Why was it introduced?
  - Copy-paste from example code
  - Missing security requirement in spec
  - Insufficient code review
```

**Proposed Fix**
- Show the exact diff (before/after)
- Explain why the fix addresses the root cause
- Reference the secure pattern to use going forward
- Note any breaking changes

**Test to Cover the Fix**
- Write a test that would have caught this before it was introduced
- The test must FAIL on the unfixed code and PASS after the fix
- Test type: unit / integration depending on the vulnerability

**Present fix for approval before applying:**
```
Fix #N ready for review:
  File: path/to/file.ext
  Change: [diff shown]
  Test: [test code shown]

Apply this fix? (yes / skip / modify)
```

Do not apply the fix until the user confirms. If user says "yes to all" for a batch,
apply in order, stop and re-confirm if any fix has unexpected side effects.

### Step 3 — Verify Each Applied Fix

After user approves and fix is applied:
1. Show the actual diff in the file
2. Confirm the test file exists and references the correct assertion
3. Note if a full test run is needed (and prompt user to run it)

### Step 4 — Output Fix Summary

After all fixes are processed:
```
## Blue Team Fix Summary

| # | Severity | Title | Status | Test Added |
|---|----------|-------|--------|-----------|
| 1 | CRITICAL | Hardcoded DB password | FIXED | yes — test/security/test_secrets.py |
| 2 | HIGH     | IDOR on /api/users/:id | FIXED | yes — test/api/test_users_auth.py |
| 3 | MEDIUM   | Missing rate limit | SKIPPED by user | — |

Open items: 1 MEDIUM skipped — user to track in backlog.
Evidence: diffs shown above, test files created at paths listed.
```

## Gotchas

- Never apply a CRITICAL fix that touches auth or session handling without showing full diff first
- If a fix introduces a breaking API change, flag it explicitly — user must decide
- Fixes for A06 (vulnerable deps) require running package managers — ask before `npm install`
- Do not suggest "add a comment explaining why this is safe" as a fix — it is not a fix

## Anti-Fake-Pass Rules

Before claiming a finding is FIXED, you MUST show:
- [ ] The actual code diff (before and after)
- [ ] The test file path and key assertion
- [ ] User approval confirmation noted in output

MUST NOT say "fixed" if only proposed — use "proposed, awaiting approval".
MUST NOT say "all fixed" if any finding was skipped — use "N fixed, M skipped".
MUST NOT say "tests pass" without the user running them — use "test written, not yet run".
