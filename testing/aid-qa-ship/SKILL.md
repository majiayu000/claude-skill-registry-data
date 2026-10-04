---
name: aid-qa-ship
description: AID Phase 5 - QA and Release. Use for validating implementations, acceptance tests, preparing releases, deployment, operational readiness.
---

# QA & Ship (Phase 5)

Applies when: development complete, tests passing, code reviewed. Does not apply before Phase 5.
Purpose: validate implementation meets requirements, ensure production readiness, ship with confidence.
Exit: acceptance criteria verified, no blockers, deployed, stakeholders informed.

References: `references/acceptance-criteria-validation.md`, `references/qa-test-templates.md`, `references/release-checklist.md`.

## Deliverables

1. Test Results - All acceptance criteria covered
2. Release Certification - Checklist, stakeholder approvals
3. Release Notes - User-facing changelog
4. Deployment - Verified, monitoring active

## Cucumber Acceptance Verification

All acceptance criteria (Gherkin scenarios) must pass before release.

| Step | Command | Expected Result | If Fails |
|------|---------|-----------------|----------|
| 1 | `npm run cucumber:dry` | No undefined steps | Implement missing step definitions |
| 2 | `npm run cucumber` | All scenarios pass | Debug failing scenarios |
| 3 | `npm run test:critical` | @critical scenarios pass | BLOCKER - must fix |
| 4 | `npm run test:bdd` | HTML report generated | Review `reports/cucumber-report.html` |

Read the summary lines: `N scenarios (N passed)` / `N steps (N passed)` means pass; any `failed`, `skipped`, or `pending` count means fail.

### HTML Report Review

Check in `reports/cucumber-report.html`:
1. **Scenario Pass Rate** - Should be 100% for release
2. **Failed Scenarios** - Click to see step-by-step failure
3. **Pending Steps** - Yellow = not implemented (blocker)
4. **Duration** - Flag unusually slow scenarios
5. **Tags** - Verify no @wip or @skip in release

## QA Testing Checklist

### Cucumber Acceptance Tests ⭐ REQUIRED
- [ ] `npm run cucumber` passes with 0 failures
- [ ] `npm run test:critical` passes (release gate)
- [ ] `npm run cucumber:dry` shows no undefined steps
- [ ] HTML report (`reports/cucumber-report.html`) reviewed
- [ ] No @wip or @skip tags in scenarios for release
- [ ] No pending step definitions
- [ ] Scenario execution time reasonable (<30s average)

### Functional
- [ ] All user stories verified
- [ ] All acceptance criteria tested
- [ ] Edge cases covered
- [ ] Error handling tested
- [ ] Cross-browser/device (if applicable)

### Non-Functional
- [ ] Performance meets requirements
- [ ] Security scan passed
- [ ] Accessibility checked
- [ ] Load testing (if applicable)

### Integration
- [ ] All integrations verified
- [ ] API contracts honored
- [ ] Data flows end-to-end

### Test Code Quality (REQUIRED)
- [ ] Tests organized in correct directories (unit/integration/e2e)
- [ ] No hardcoded credentials in test code
- [ ] No secrets in README or documentation
- [ ] Tests run successfully in random order (`--randomize`)
- [ ] ALL existing tests still pass (no regressions)
- [ ] Assertions check specific values (not just existence)
- [ ] Tests verified to fail when code is broken

## Test Verification Steps

Before marking QA complete, MUST verify:

1. Run all tests. All must pass; no skipped tests without documented reason.
```bash
npm test
```
2. Run in random order. All must pass.
```bash
jest --randomize
# OR
vitest --sequence.shuffle
```
3. Check for credentials. Both must return no matches.
```bash
grep -rn "password.*=.*['\"]" tests/
grep -rn "sk_live\|pk_live\|AKIA" tests/
```
4. Verify assertions (mutation test): comment out a key line of code being tested, run the related test, test MUST fail, restore code and verify test passes.
5. Regression check: compare test count before vs after changes; same or more tests should pass.

## Release Process

Pre-Release: 1. Complete QA checklist 2. Stakeholder sign-off 3. Prepare release notes 4. Verify rollback procedure 5. Schedule deployment
Deployment: 1. Deploy to staging 2. Run smoke tests 3. Deploy to production 4. Verify production smoke 5. Enable monitoring
Post-Release: 1. Monitor errors & performance 2. Gather user feedback 3. Address critical issues 4. Document lessons learned 5. Close project artifacts

## Phase Gate Checklist

### Cucumber Acceptance Gates (MUST PASS) ⭐
- [ ] `npm run cucumber` exits with code 0
- [ ] `npm run test:critical` passes (all @critical scenarios)
- [ ] No undefined or pending step definitions
- [ ] HTML report generated and reviewed
- [ ] No @wip or @skip tags in release scenarios

### Test Quality Gates (MUST PASS)
- [ ] All tests pass (`npm test` returns 0 failures)
- [ ] Tests pass in random order (`--randomize` flag)
- [ ] No hardcoded credentials in test code
- [ ] ALL existing tests still pass (no regressions)
- [ ] Tests verified to catch bugs (mutation test)

### Acceptance & Quality
- [ ] All acceptance criteria verified (via Cucumber)
- [ ] No blocking bugs
- [ ] Performance validated
- [ ] Security review completed

### Release Readiness
- [ ] Rollback plan documented
- [ ] Monitoring configured
- [ ] Release notes prepared
- [ ] Stakeholder approval
- [ ] Deployment instructions verified

## Release Notes Template

```markdown
# Release Notes - [Feature]
**Date**: YYYY-MM-DD
**Version**: X.Y.Z

## What's New
- [Feature]: [Description]

## Improvements
- [Improvement]

## Bug Fixes
- [Fix]: [What was fixed]

## Known Issues
- [Issue]: [Workaround]
```

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Rushing to ship | Respect checklist |
| Testing in production | Use staging |
| Missing rollback | Always have way back |
| No monitoring | Set up first |
| Poor communication | Keep everyone informed |

## Role Guidance

| Role | Focus |
|------|-------|
| PM | Acceptance testing, UX, approve release |
| Dev | Fix bugs, support deploy, monitor |
| QA | Execute test plan, verify fixes, sign-off |
| Tech Lead | Operational readiness, approve deploy |

## Pipeline Integration

If `.aid/pipeline/state.json` exists with `pipeline_status: "running"`, Phase 5 test sequencing is driven by the **pipeline-orchestrator** skill.

| Without Pipeline | With Pipeline |
|-----------------|---------------|
| Manual test execution order | Pipeline enforces API_TESTS > E2E_TESTS > CERTIFICATION |
| Developer decides when to fix | Pipeline enforces fix-and-retry loops |
| Manual certification | Automated CERTIFICATION step with coverage verification |

Unchanged by the pipeline: Cucumber acceptance verification, QA testing checklist, release process, phase gate checklist.

Activation: the pipeline auto-transitions Phase 4 to Phase 5 when PHASE_GATE passes (if `auto_advance_phase: true` in config). Otherwise run `/pipeline` in Phase 5.

See `../pipeline-orchestrator/SKILL.md` for full pipeline documentation.
