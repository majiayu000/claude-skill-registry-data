---
name: superpowers-requesting-code-review
description: >
  Use before merging, after completing a major feature, or when stuck — dispatch structured code
  review to catch issues before they compound. Two-pass review (Critical then Informational),
  Fix-First protocol, adversarial review that scales by diff size.
---

# Requesting Code Review

**Core principle:** Review early, review often. The best bug is the one caught before it ships.

---

## When to Request

**Mandatory:**
- After each task in subagent-driven development
- After completing a major feature
- Before merge to main
- After fixing a complex bug

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)

---

## Step 1: Detect Base Branch

```bash
BASE_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||')
echo "Base branch: ${BASE_BRANCH:-main}"
```

---

## Step 2: Scope Drift Check

Before reviewing, verify the diff matches the stated intent:

```bash
git fetch origin "$BASE_BRANCH" --quiet 2>/dev/null || true
BASE_SHA=$(git rev-parse "origin/$BASE_BRANCH" 2>/dev/null || echo "HEAD~10")
HEAD_SHA=$(git rev-parse HEAD)

echo "Diff: $BASE_SHA..$HEAD_SHA"
git diff --stat "$BASE_SHA..$HEAD_SHA"
```

1. Read the PR description or TODOs.md to understand the stated goal
2. Compare against what actually changed
3. Flag if: the diff does MORE than planned, LESS than planned, or DIFFERENT than planned
4. If scope drift detected, report it before proceeding

---

## Step 3: Two-Pass Review

### Pass 1 — CRITICAL (always run)

These are bugs that pass CI but break in production:

| Category | What to check |
|----------|--------------|
| **SQL safety** | SQL injection, parameterized queries, transaction boundaries, cascade deletes |
| **Race conditions** | Concurrent access to shared state, missing locks, TOCTOU |
| **LLM trust boundaries** | Untrusted input passed to LLM calls, output not sanitized, prompt injection vectors |
| **Enum completeness** | Switch/case without default, missing error codes, unhandled states |
| **Auth/authz gaps** | Missing permission checks, token validation, IDOR vulnerabilities |
| **Resource leaks** | Unclosed connections, missing cleanup, file handle exhaustion |
| **Data loss risk** | Missing null guards before write, destructive operations without confirmation |

**For each finding:**
- **AUTO-FIX:** If the fix is obvious and self-contained, apply it immediately
- **ASK:** If the fix requires judgment or affects multiple files, batch for user approval

### Pass 2 — INFORMATIONAL (always run)

These are quality issues worth addressing:

| Category | What to check |
|----------|--------------|
| **Side effects** | Functions with hidden dependencies, mutable globals |
| **Magic numbers** | Unnamed constants, hardcoded values with implied meaning |
| **Dead code** | Unused exports, commented-out logic, redundant checks |
| **Test gaps** | Missing coverage for edge cases, happy path only |
| **Error handling** | Silent catches, empty catch blocks, generic error messages |
| **Naming** | Misleading names, inconsistent conventions |
| **Coupling** | Tight coupling between unrelated modules |

---

## Step 4: Test Coverage Diagram

Trace every code path in the diff and map user flows:

1. **Codepath tracing** — For each changed function, trace the execution paths (happy, nil, error, empty)
2. **User flow mapping** — Map changed code to user-facing flows it affects
3. **Coverage gap identification** — Which paths have no test?
4. **Gap remediation:**
   - If gaps are critical → add tests to the plan
   - If gaps are minor → note as informational

---

## Step 5: Fix-First Protocol

For every finding:

- **AUTO-FIX items:** Apply immediately. One commit per fix. Do not batch.
- **ASK items:** List them in a table:

```
PENDING REVIEW FINDINGS
══════════════════════════════════════
#  Severity   Category          Finding                              Action
══════════════════════════════════════
1  Critical   SQL safety       Missing parameterized query on line 45  ASK
2  High       Auth gap          No permission check in handler        ASK
3  Medium     Error handling    Silent catch block at service.go:120  ASK
══════════════════════════════════════
```

Present each ASK item via AskUserQuestion with:
- Re-ground (what changed, why it matters)
- Simplify (plain English, concrete example)
- Recommend (Completeness X/10 per option)
- Options: Fix it now / defer / won't fix

---

## Step 6: Adversarial Review (scales by diff size)

| Diff size | Adversarial passes |
|-----------|-------------------|
| <50 lines | Skip |
| 50–199 lines | 1 pass (try Claude Opus subagent, fall back to self) |
| 200+ lines | 2 passes (Claude subagent + self review) |

**Adversarial question:** "If I were an attacker/bug-generator, how would I break this code?"

---

## Step 7: Documentation Check

- Check if README, ARCHITECTURE.md, or inline docs reference the changed code
- Flag if docs are now stale (behavior changed, API updated, file renamed)
- Check CHANGELOG for any missing entries

---

## Step 8: TODOs Cross-Reference

```bash
cat TODOS.md 2>/dev/null || echo "No TODOs.md found"
```

Check if all TODOs related to the diff are addressed. Flag any TODOs that:
- Have been implemented but not marked done
- Reference code that no longer exists

---

## Step 9: Commit Fixes

For AUTO-FIX items, commit each separately:

```bash
git add -p
git commit -m "fix(review): AUTO-FIX — brief description

Reviewed with: superpowers-requesting-code-review
Severity: critical"
```

---

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Critical issues
- Proceed with more than 5 unfixed ASK items without flagging

**If reviewer is wrong:** Push back with technical reasoning, show code/tests proving it works.

---

## Integration with Workflows

- **Subagent-Driven Development:** Review after EACH task; catch issues before they compound
- **Executing Plans:** Review after each batch (3 tasks); get feedback, apply, continue
- **Ad-Hoc Development:** Review before merge or when stuck

---

## AskUserQuestion Standard Format

1. **Re-ground** — Project, branch, current task
2. **Simplify** — Plain English, no jargon, concrete examples
3. **Recommend** — `RECOMMENDATION: Choose [X]` with `Completeness: X/10`
4. **Options** — Lettered, effort shown as `human: ~X / AI: ~Y`
5. **One decision per question**
