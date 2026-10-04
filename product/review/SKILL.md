---
name: review
description: Risk-tiered code review (Blocker / High / Medium / Low). Use when the user runs /review or wants the current branch or diff reviewed.
---

# /review — Risk-Tiered Code Review

Performs a structured code review with four risk tiers. Produces an AC Trace Matrix.

## Optional council deliberation

When the user includes `--council <profile-path>`, follow `.claude/commands/council.md` after collecting the diff, acceptance criteria, and context below. For a PR use the `pr` source; for a local branch supply the captured diff and context as text. Treat the council transcript as additional review evidence, preserve dissent and limitations, and still complete the AC Trace Matrix. Never silently substitute the key-free demo for a real review. Council findings do not authorize code changes or GitHub publication.

## Usage
```
/review                      # Review current branch vs main
/review feat/T-42-my-feature # Review specific branch
/review #17                  # Review PR by number
```

---

## Step 1 — Get the Diff

```bash
# For a branch
git diff main..<branch> --stat      # File overview
git diff main..<branch>             # Full diff

# For a PR
gh pr diff <number>
gh pr view <number> --json title,body,commits
```

Also fetch the task details (if a Beads ID is findable from branch name or PR body):
```bash
bd show <TASK-ID> 2>/dev/null || true
```

---

## Step 2 — Read the Context

Before reviewing, understand intent:
1. Read the PR/commit description
2. Read the Beads task and its AC (if available)
3. Read the knowledge file for the affected repo: `cat knowledge/repos/<repo>.yaml`
4. Spot-check 2-3 key files to understand the full context (not just the diff)

---

## Step 3 — Risk-Tiered Analysis

Evaluate the diff against all four tiers. Rate each finding.

For **UI-facing** changes, also apply `.claude/protocols/evaluation-rubric.md` (visual design / originality vs generic patterns) in addition to the tiers below — surface HIGH findings when polish or product depth misses stated intent, not only when code is broken.

### Blocker — Must fix. Blocks PASS.

| Category | What to look for |
|----------|-----------------|
| **Security** | Hardcoded secrets, SQL injection, path traversal, XSS, auth bypass, unsafe deserialization |
| **Data loss** | Destructive operations without confirmation, missing rollback, irreversible mutations |
| **Credentials** | API keys, passwords, tokens, private keys committed |
| **Critical bugs** | Off-by-one in auth/payment code, null deref crashes in critical paths |

### High — Must fix. Blocks PASS.

| Category | What to look for |
|----------|-----------------|
| **Error handling** | Uncaught exceptions in async code, silent failures, missing error boundaries |
| **Type safety** | `any` without justification, unsafe casts, missing null checks |
| **Test gaps** | New code paths with zero test coverage |
| **Breaking changes** | Changed public interfaces without migration path |
| **Performance** | N+1 queries, unbounded loops, blocking the main thread |

### Medium — Does not block. Create follow-up task.

| Category | What to look for |
|----------|-----------------|
| **Code quality** | Deeply nested logic, functions >50 lines, duplicated logic |
| **Edge cases** | Missing validation for empty arrays, zero, empty strings |
| **Observability** | Missing logs/metrics for significant operations |
| **Naming** | Misleading variable or function names |

### Low — Optional. Minor polish.

| Category | What to look for |
|----------|-----------------|
| **Style** | Minor formatting inconsistencies |
| **Docs** | Missing JSDoc for public APIs |
| **Naming nits** | Slightly unclear names (not misleading, just verbose) |

---

## Step 4 — AC Trace Matrix

Map each acceptance criterion to how it is verified:

```markdown
## AC Trace Matrix

| Criterion | Verified By | Status |
|-----------|-------------|--------|
| User can update display name | `useUserSettings.test.ts:42` | ✓ |
| Error shows if API fails | `UserSettingsPage.test.tsx:89` | ✓ |
| Settings persist after refresh | Manual: navigate away and back | ✓ |
| Cannot set empty display name | `useUserSettings.test.ts:67` | ✓ |
```

If a criterion has no test and no documented manual verification: flag as High finding.

---

## Step 5 — Rework (if needed)

If Blocker or High findings exist:

1. List all Blocker and High findings clearly
2. Ask the worker/author to address them
3. Maximum **2 rework iterations**

After each rework: re-run the review against the updated diff.
Log the result: `bd comments add <TASK-ID> "review: iteration <n> — <finding counts>"`

If issues remain after 2 iterations:
- Revert the implementation
- File a Beads bug with all findings
- Close the review with FAIL status

---

## Step 6 — Final Verdict

### PASS
- Zero Blockers
- Zero High findings (or all fixed)
- AC Trace Matrix complete

```
bd comments add <TASK-ID> "review: PASS — 0B/0H/2M/1L"
```

### FAIL
- Any unfixed Blockers or High findings

```
bd comments add <TASK-ID> "review: FAIL — 1B/2H/0M/0L — reverted"
```

---

## Output Format

```
## Code Review: feat/T-42-refresh-tokens

Files reviewed: 4 (+187 / -23 lines)
Task: T-42 — Add refresh token rotation

### Findings

🔴 BLOCKER (0)

🟠 HIGH (1)
  - src/api/auth.ts:87 — Missing error handling on token refresh failure.
    Async function with no try/catch; unhandled promise rejection in production.
    Fix: wrap in try/catch, return error state to caller.

🟡 MEDIUM (2)
  - src/hooks/useAuth.ts:34 — refreshToken function is 60+ lines. Consider splitting.
  - src/api/auth.ts — No logging on token rotation for audit trail.

⚪ LOW (0)

### AC Trace Matrix
| Criterion | Verified By | Status |
|-----------|-------------|--------|
| Token rotates on use | useAuth.test.ts:112 | ✓ |
| Old token rejected after rotation | useAuth.test.ts:134 | ✓ |
| Error state on network failure | ✗ NOT COVERED | — |

### Verdict: FAIL — 0B/1H/2M/0L
AC criterion "Error state on network failure" is untested.
Address HIGH finding and add error state test, then re-review.

Rework iteration: 1/2
```
