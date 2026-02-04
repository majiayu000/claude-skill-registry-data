---
name: gmacko-qa-verify
description: Use when (1) verifying a feature is complete against acceptance criteria, (2) running QA checklist before release, (3) validating PR changes meet requirements. Performs systematic QA verification with documented results.
license: MIT
compatibility: opencode
metadata:
  phase: qa
  tier: workhorse
  permission: allow
---

# Gmacko QA Verification

Systematically verify feature completion against acceptance criteria and produce QA handoff document.

## When to Use

- Feature implementation is complete
- PR is ready for QA review
- Before promoting to staging/production
- User requests verification of specific functionality

## Prerequisites

- Feature plan exists: `docs/ai/handoffs/{feature}-plan.md`
- Dev handoff exists: `docs/ai/handoffs/{feature}-dev.md`
- Code changes are deployed to testable environment

## Workflow

```dot
digraph qa_verify {
    rankdir=TB;
    node [shape=box];
    
    start [label="Start QA" shape=ellipse];
    gather [label="1. Gather Context"];
    criteria [label="2. Load Acceptance Criteria"];
    functional [label="3. Functional Testing"];
    cross [label="4. Cross-Platform Testing"];
    edge [label="5. Edge Case Testing"];
    security [label="6. Security Spot Check"];
    regression [label="7. Regression Check"];
    document [label="8. Document Results"];
    decision [label="9. Go/No-Go Decision"];
    handoff [label="10. Write QA Handoff"];
    done [label="QA Complete" shape=ellipse];
    
    start -> gather -> criteria -> functional;
    functional -> cross -> edge -> security;
    security -> regression -> document -> decision -> handoff -> done;
}
```

## Execution Steps

### Step 1: Gather Context

Collect all relevant information:

```bash
# Find related artifacts
FEATURE_ID="[from user or issue number]"
PLAN_DOC="docs/ai/handoffs/${FEATURE_ID}-plan.md"
DEV_DOC="docs/ai/handoffs/${FEATURE_ID}-dev.md"

# Check artifacts exist
[ -f "$PLAN_DOC" ] && echo "Plan found" || echo "WARN: No plan doc"
[ -f "$DEV_DOC" ] && echo "Dev handoff found" || echo "WARN: No dev handoff"
```

Ask user:
> I'm starting QA verification for **[feature name]**.
>
> Please confirm:
> 1. Which environment should I test? (local/staging/production)
> 2. Is there a specific PR to review? (#number)
> 3. Any areas of particular concern?

### Step 2: Load Acceptance Criteria

Extract criteria from the feature plan:

```markdown
## Acceptance Criteria (from plan)

### Functional Requirements
- [ ] AC1: [Description]
- [ ] AC2: [Description]
- [ ] AC3: [Description]

### Non-Functional Requirements
- [ ] Performance: [Target]
- [ ] Accessibility: [Standard]
- [ ] Security: [Requirements]
```

If no plan exists, ask user for acceptance criteria.

### Step 3: Functional Testing

Test each acceptance criterion:

```markdown
## Functional Test Results

### AC1: [User can create a new project]
**Steps Taken:**
1. Navigated to /projects
2. Clicked "New Project" button
3. Filled form with test data
4. Submitted form

**Expected:** Project created, redirected to project page
**Actual:** [Describe what happened]
**Result:** PASS / FAIL
**Evidence:** [Screenshot URL or description]

### AC2: [Project appears in dashboard]
...
```

For each criterion:
- Document exact steps taken
- Record expected vs actual behavior
- Capture evidence (describe what you observed)
- Mark PASS/FAIL

### Step 4: Cross-Platform Testing

If feature affects multiple platforms:

```markdown
## Cross-Platform Results

| Platform | Tested | Result | Notes |
|----------|--------|--------|-------|
| Web - Chrome | Yes | PASS | |
| Web - Firefox | Yes | PASS | |
| Web - Safari | Yes | PASS | Minor style issue |
| Web - Mobile | Yes | PASS | |
| iOS Simulator | Yes | PASS | |
| Android Emulator | No | SKIP | Not applicable |
```

### Step 5: Edge Case Testing

Test boundary conditions:

```markdown
## Edge Cases

### Empty State
- [ ] No data displays appropriate message
- [ ] CTA to create first item visible

### Maximum Limits
- [ ] Form validates max length
- [ ] List handles 100+ items

### Error States
- [ ] Network error shows retry option
- [ ] Invalid input shows validation message
- [ ] Unauthorized access redirects to login

### Concurrent Access
- [ ] Multiple tabs don't conflict
- [ ] Real-time updates work correctly
```

### Step 6: Security Spot Check

Quick security verification:

```markdown
## Security Check

- [ ] Authentication required where expected
- [ ] User can only see their own data
- [ ] No sensitive data in console/network logs
- [ ] Form inputs properly validated
- [ ] No XSS vulnerabilities (test with `<script>alert(1)</script>`)
```

### Step 7: Regression Check

Verify related features still work:

```markdown
## Regression Check

### Related Features
- [ ] [Feature A] - Still working
- [ ] [Feature B] - Still working
- [ ] [Feature C] - Still working

### General Health
- [ ] Login/logout works
- [ ] Navigation works
- [ ] No new console errors
- [ ] No new Sentry errors (check dashboard)
```

### Step 8: Document Results

Compile test summary:

```markdown
## Test Summary

| Category | Passed | Failed | Skipped | Total |
|----------|--------|--------|---------|-------|
| Acceptance Criteria | 5 | 0 | 0 | 5 |
| Cross-Platform | 4 | 0 | 2 | 6 |
| Edge Cases | 8 | 1 | 0 | 9 |
| Security | 5 | 0 | 0 | 5 |
| Regression | 3 | 0 | 0 | 3 |
| **Total** | **25** | **1** | **2** | **28** |

### Issues Found

| ID | Description | Severity | Blocking? |
|----|-------------|----------|-----------|
| QA-1 | Empty state message missing | Medium | No |
```

### Step 9: Go/No-Go Decision

Based on results, make recommendation:

**APPROVED** - All criteria met, no blocking issues
```
Recommendation: APPROVED

All acceptance criteria verified. 1 minor issue found (non-blocking).
Feature is ready for release.
```

**APPROVED WITH NOTES** - Minor issues, can release
```
Recommendation: APPROVED WITH NOTES

Acceptance criteria met. Issues found:
- QA-1: Minor UX issue (create follow-up ticket)

Proceed with release, address issues in next sprint.
```

**NOT APPROVED** - Blocking issues found
```
Recommendation: NOT APPROVED

Blocking issues found:
- AC3 not met: Data not persisting correctly
- Security: Unauthorized access possible

Must fix before release. See issues section.
```

### Step 10: Write QA Handoff

Create `docs/ai/handoffs/{feature}-qa.md`:

```markdown
# QA Handoff: [Feature Name]

## Summary
- **Feature**: [Name]
- **Issue**: #[number]
- **PR**: #[number]
- **QA Date**: [YYYY-MM-DD]
- **Tester**: AI Assistant
- **Environment**: [staging/local]

## Recommendation
**[APPROVED / APPROVED WITH NOTES / NOT APPROVED]**

[Brief explanation]

## Acceptance Criteria Results

| Criterion | Result | Notes |
|-----------|--------|-------|
| AC1 | PASS | |
| AC2 | PASS | |
| AC3 | PASS | Minor delay observed |

## Test Coverage

| Category | Pass Rate |
|----------|-----------|
| Functional | 100% |
| Cross-Platform | 100% |
| Edge Cases | 89% |
| Security | 100% |
| Regression | 100% |

## Issues Found

### Blocking
None

### Non-Blocking
1. **QA-1**: Empty state message missing
   - Severity: Medium
   - Impact: UX only
   - Recommendation: Create follow-up issue

## Test Evidence

[Links to screenshots, recordings, or descriptions]

## Next Steps
- [ ] Address blocking issues (if any)
- [ ] Create follow-up issues for non-blocking items
- [ ] Proceed to release preparation

---

**Sign-off**: [Tester name]
**Date**: [YYYY-MM-DD]
```

## Automated Checks

Run these commands as part of verification:

```bash
# Code quality
pnpm typecheck
pnpm lint

# Build verification
pnpm build

# Check for console errors in browser
# Check Sentry for new errors
# Check PostHog for analytics events
```

## Red Flags

| Rationalization | Correction |
|-----------------|------------|
| "It works on my machine" | Test in the specified environment |
| "Edge cases can wait" | Edge cases reveal real bugs |
| "Security is someone else's job" | Basic security checks are everyone's job |
| "No plan doc, I'll guess the criteria" | ASK for criteria before testing |
| "Minor issues, I'll approve anyway" | Document ALL issues; let stakeholders decide |

## Integration

- **Input**: Feature ID, environment, PR number
- **References**: Feature plan, dev handoff, checklists
- **Output**: `docs/ai/handoffs/{feature}-qa.md`
- **Next**: `gmacko-release-prepare` (if approved)
