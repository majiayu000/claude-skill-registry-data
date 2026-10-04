---
name: issue-debugging
description: Systematic methodology for issue debugging including root cause analysis, impact mapping, tiered validation plans, and confidence assessment. Use when analyzing bugs, fixing issues, or validating fixes.
user-invocable: false
allowed-tools:
  - Read
  - Write
version: 1.0.0
author: "Ashay Kubal @ Qball Inc."
---

# Issue Debugging

Systematic methodology for debugging that prevents the "first error fix and declare done" anti-pattern. Ensures root cause analysis, impact assessment, and verified fixes.

---

## When to Use This Skill

**Load this skill when the user request matches ANY of these patterns:**

| Trigger Pattern | Example User Request |
|-----------------|---------------------|
| Bug investigation | "Why is X failing?", "Debug this error", "Investigate this issue" |
| Test failures | "Tests are failing", "Fix the broken tests", "Why did CI fail?" |
| Error analysis | "Getting this error...", "Exception in...", "Stack trace shows..." |
| Regression hunting | "This used to work", "Something broke after...", "Regression in..." |
| Fix validation | "Did the fix work?", "Verify this change", "Make sure it's fixed" |
| Root cause requests | "What's causing this?", "Find the root cause", "Why does this happen?" |

**DO NOT use for:**
- New feature implementation (no existing bug)
- Refactoring without reported issues
- General code questions

---

## Overview

### The Problem

AI (and developers) often fix the first visible error and declare victory without verifying end-user functionality works. This leads to:
- Symptom fixes instead of root cause fixes
- Regressions in seemingly unrelated areas
- False confidence in fix completeness

### The Solution

This skill provides:
1. **Root Cause Analysis** - Find the actual cause, not just symptoms
2. **Impact Analysis** - Map affected areas and dependencies
3. **Validation Planning** - Tiered test priorities (P1/P2/P3)
4. **Confidence Assessment** - Objective fix reliability rating
5. **Escalation Triggers** - When manual testing is required

---

## Root Cause Analysis

### The 5 Whys Method

Iteratively ask "Why?" to drill past symptoms to root cause:

```
Problem: Login fails with 500 error
├─ Why? → API returns null for user profile
├─ Why? → Database query found no records
├─ Why? → Migration didn't run on deploy
├─ Why? → Deployment script skipped migration step
└─ Why? → Environment variable missing

Root Cause: Missing environment variable (not the 500 error)
```

**Key Principle**: Focus on HOW and WHY the defect occurred, not just WHERE.

### Hypothesis-Driven Debugging

Apply scientific method:

| Step | Action |
|------|--------|
| **Observe** | Gather data: errors, logs, stack traces, reproduction steps |
| **Hypothesize** | Form a **falsifiable** hypothesis about the cause |
| **Experiment** | Design tests to prove/disprove hypothesis |
| **Conclude** | If confirmed, proceed. If rejected, form new hypothesis |
| **Document** | Write down hypotheses tested (prevents circular investigation) |

### Binary Search / Bisection

For isolating bugs in time or space:
1. Place checkpoint at midpoint
2. Determine if bug is before or after
3. Repeat on remaining half
4. Continue until exact location found

**Efficiency**: O(log n) - approximately 7 tests for 100 commits.

---

## Impact / Dependency Analysis

### Mapping Procedure

For each affected file, identify:

```
Affected Code: src/auth/login.ts

Upstream (What calls this?):
├─ src/api/auth-routes.ts → POST /login
├─ src/middleware/session.ts → validateSession()
└─ src/pages/login.tsx → handleSubmit()

Downstream (What does this affect?):
├─ User dashboard → fetches profile on load
├─ Settings page → assumes profile exists
└─ API responses → include user context
```

### Risk Scope Assessment

| Scope | Definition | Validation Approach |
|-------|------------|---------------------|
| **Isolated** | Self-contained, no affected areas | Unit tests only |
| **Medium** | 1-5 affected areas | Integration tests |
| **Broad** | >5 affected areas, cross-cutting | Integration + E2E + manual |

---

## Debug Report Format

### Location

Debug reports are written to: `logs/debug-reports/{issue-id}-{timestamp}.yaml`

This location is separate from standard agent logs to:
- Enable easy reference by downstream pipeline stages
- Keep debug context grouped by issue
- Allow FixValidator to read validation plans

### Schema Overview

```yaml
debug_report:
  metadata:
    issue_id: "{id}"
    timestamp: "{ISO-8601}"
    analyzer: "bulwark-issue-analyzer"
    complexity: low | medium | high

  analysis:
    symptom: "{user-visible problem}"
    root_cause: "{underlying reason}"
    fix_approach: "{recommended approach}"

  impact_analysis:
    affected_files: [...]
    upstream_dependencies: [...]
    downstream_effects: [...]
    risk_scope: isolated | medium | broad

  validation_plan:
    tests_to_execute:
      - path: "{test file}"
        reason: "{why this test}"
        priority: 1  # P1=must, P2=should, P3=nice-to-have
    functionalities_to_validate: [...]

  confidence_criteria:
    high: [...]
    medium: [...]
    low: [...]

  debug_journey:  # Required for medium/high complexity
    hypotheses_tested: [...]
```

**Full schema**: See `references/debug-report-schema.md`

---

## Validation Plan

### Tiered Test Priorities

| Priority | Definition | Action |
|----------|------------|--------|
| **P1 (Must)** | Direct tests of affected function | Always run |
| **P2 (Should)** | Integration tests for upstream/downstream | Run if time/tokens allow |
| **P3 (Nice-to-have)** | E2E tests, edge cases | Run if available |

### Selection Criteria

**P1 Tests** (always run):
- Tests in the same file/module as the fix
- Tests named after the affected function
- Tests that were failing before the fix

**P2 Tests** (run if possible):
- Tests for upstream callers
- Tests for downstream consumers
- Tests for related functionality

**P3 Tests** (run if available):
- E2E tests that include the affected flow
- Performance tests
- Edge case tests

### Functionality Validation

Beyond tests, list user-level verifications:
- "User can log in successfully"
- "Dashboard displays correct data after login"
- "Session persists across page refresh"

---

## Confidence Rubric

### Assessment Criteria

| Level | Criteria |
|-------|----------|
| **High** | All P1-P2 tests pass, no regression, at least one functionality verified |
| **Medium** | P1 tests pass, some P2-P3 skipped or not applicable |
| **Low** | Tests cannot reliably validate, broad risk scope with untested paths |

### Determining Complexity

| Complexity | Indicators |
|------------|------------|
| **Low** | Single file, isolated change, clear cause |
| **Medium** | 2-5 files, some dependencies, requires investigation |
| **High** | >5 files, cross-cutting, unclear cause, multiple hypotheses needed |

---

## Escalation Triggers

Manual testing is **required** when ANY of:
- Confidence level is `low`
- Risk scope is `broad` AND confidence is not `high`
- Any functionality cannot be validated via automated tests
- Security-related fix without security test coverage

### Escalation Message Format

When escalation is triggered, the Orchestrator must inform the user:

```
Manual testing required for:
- [functionality 1]
- [functionality 2]

Reason: [why automated validation insufficient]

Recommended manual test steps:
1. [step]
2. [step]
```

---

## Debug Journey Logging

### When Required

| Complexity | Debug Journey Required? |
|------------|------------------------|
| Low | Optional |
| Medium | **Required** |
| High | **Required** |

### Format

```yaml
debug_journey:
  started_at: "{timestamp}"
  completed_at: "{timestamp}"

  hypotheses_tested:
    - hypothesis: "Database connection timeout causing failure"
      tested_at: "{timestamp}"
      method: "Checked DB logs and connection pool stats"
      result: rejected
      evidence: "DB logs show successful queries, pool not exhausted"

    - hypothesis: "Null profile object when user has no data"
      tested_at: "{timestamp}"
      method: "Added logging at profile access point"
      result: confirmed
      evidence: "Stack trace shows NPE at profile.name access"

  investigation_path:
    - "Started with error log analysis"
    - "Ruled out infrastructure issues"
    - "Narrowed to application code"
    - "Identified profile access as failure point"
```

---

## Anti-Patterns

### What NOT to Do

| Anti-Pattern | Description | Correct Approach |
|--------------|-------------|------------------|
| **Shotgun Debugging** | Random changes hoping bug disappears | Hypothesis-driven approach |
| **Fix Without Verify** | Declaring "fixed" without running tests | Always verify at code + user level |
| **Symptom Fixing** | Adding workarounds instead of root cause fix | Use 5 Whys |
| **Blind AI Trust** | Accepting suggestions without verification | Test the failing scenario |
| **Full Regression** | Running 4000+ tests after every fix | Use tiered validation |
| **Circular Investigation** | Repeating tested hypotheses | Document debug journey |

**Full checklist**: See `references/anti-patterns.md`

---

## Quick Reference

### Before Fixing

- [ ] Symptom identified and documented
- [ ] Root cause analysis completed (not just symptom)
- [ ] Impact analysis completed (upstream/downstream)
- [ ] Risk scope assessed (isolated/medium/broad)
- [ ] Complexity determined (low/medium/high)

### After Fixing

- [ ] Fix implemented
- [ ] P1 tests pass
- [ ] P2 tests pass (or documented why skipped)
- [ ] Confidence level assessed
- [ ] Manual testing escalated if required
- [ ] Debug journey documented (if medium/high complexity)
- [ ] Debug report written to `logs/debug-reports/`

### Complexity → Actions

| Complexity | Debug Journey | Validation | Escalation |
|------------|---------------|------------|------------|
| Low | Optional | P1 tests | Only if low confidence |
| Medium | Required | P1 + P2 tests | If broad scope |
| High | Required | P1 + P2 + P3 | Almost always |

---

## Integration

### Pipeline Integration

This skill is used by the Fix Validation pipeline:

```fsharp
IssueAnalyzer (loads this skill, produces debug report)
|> FixWriter (reads debug report for context)
|> TestWriter (reads validation plan)
|> FixValidator (executes validation plan, assesses confidence)
|> CodeReviewer (reviews all, makes approval decision)
```

### Agent Integration

| Agent | Usage |
|-------|-------|
| `bulwark-issue-analyzer` (P1.2) | Loads via `skills: issue-debugging`, produces debug report |
| `bulwark-fix-validator` (P1.3) | Loads via `skills: issue-debugging`, executes validation plan |

### Artifact Flow

```
IssueAnalyzer
    └─> logs/debug-reports/{issue-id}.yaml
              │
              ├─> FixWriter (reads root cause, fix approach)
              ├─> TestWriter (reads validation plan)
              ├─> FixValidator (executes tests, assesses confidence)
              └─> CodeReviewer (reviews everything)
```

---

## Related Skills

- `subagent-prompting` (P0.1) - 4-part template for agent invocation
- `subagent-output-templating` (P0.2) - Output format for logs
- `pipeline-templates` (P0.3) - Fix Validation pipeline definition
