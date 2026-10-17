---
name: qa-release
description: Manage QA release gates - go/no-go decisions, release sign-off reports, defect triage, and release readiness communication. Use this skill whenever a QA lead or manager needs to formally assess whether a build is ready to ship. Trigger on phrases like "release sign-off", "go or no-go", "is this ready to release", "defect triage", "release gate", "approve the release", "block the release", "release readiness", "quality gate", "sign off on this build", "triage these bugs", or any request to make or document a formal release decision. Also trigger when a release manager or PM asks "what's the QA status?" or "can we ship this?".
---

## Overview

Based on the **Google SRE Book** and **"Accelerate"** by Forsgren, Humble & Kim. Google SRE's error budget concept reframes the release gate: instead of "is it good enough to ship?", ask "how much of the error budget does this risk consuming?" Accelerate's research shows that high-performing teams ship more frequently AND have lower change failure rates - speed and quality are not a tradeoff, they're correlated.

# QA Release

Run release gates, triage defects, and produce formal sign-off decisions.

## When to Use

- Making a go/no-go decision before a release
- Running a defect triage session with engineering and PM
- Writing a formal release sign-off report
- Setting and enforcing quality gates for a CI/CD pipeline
- Communicating release quality status to stakeholders

## Inputs to Gather

1. **Release scope** - what features and fixes are in this release?
2. **Test results** - regression pass rate, outstanding defects
3. **Open defect list** - severity, owner, resolution status
4. **Quality gates** - what thresholds must be met to ship?
5. **Business context** - hard deadline, customer commitments, risk tolerance?

## Workflow

### Step 1: Assess Test Completion

Before triaging defects, confirm testing is done:

- [ ] Regression suite executed (what % complete?)
- [ ] Smoke test passed on release candidate build
- [ ] New feature testing complete
- [ ] Performance and security testing done (if in scope)
- [ ] All P1 defects from previous releases verified as fixed

If testing is incomplete, record the gap and quantify the risk it represents.

### Step 2: Defect Triage

Triage every open defect against the release:

For each defect, decide one of:
- **Fix before release** - required for go
- **Fix in hotfix** - ship with a commitment to patch within [timeframe]
- **Defer** - acceptable risk, tracked in backlog
- **Won't fix** - by design or out of scope

Triage criteria:
| Severity | Default Decision | Override Condition |
|----------|-----------------|-------------------|
| P1 | Fix before release | None - P1 blocks release |
| P2 | Fix before release | PM accepts risk in writing with mitigation |
| P3 | Defer acceptable | Core user journey affected - escalate |
| P4 | Defer | Always deferrable |

Document every override decision and who made it. Do not allow verbal agreements - get written approval on the ticket or in the release thread.

### Step 3: Quality Gate Check

Evaluate against pre-agreed thresholds. If no thresholds exist, use these defaults:

| Gate | Default Threshold | Status |
|------|-------------------|--------|
| Regression pass rate | ≥ 95% | PASS / FAIL |
| Open P1 defects | 0 | PASS / FAIL |
| Open P2 defects | ≤ 2, all with accepted risk | PASS / FAIL |
| Test coverage (new features) | 100% of P1 test cases executed | PASS / FAIL |
| Performance regression | ≤ 10% degradation vs baseline | PASS / FAIL |

All gates must pass for a GO decision unless an explicit exception is documented.

**SRE Error Budget framing (for teams with defined SLOs):**
If your team operates with SLOs and error budgets, frame the release decision as:
- What is the current error budget remaining this month?
- What is the estimated error budget cost if this release causes a typical incident?
- If estimated cost > remaining budget: NO-GO (or scope reduction required)

**Accelerate's change failure rate benchmark:**
- Elite: 0-15% of releases cause production incidents
- High: 16-30%
- Medium: 16-30% (same range, different velocity)
- Low: 46-60%

Track your team's rolling change failure rate. If it exceeds 30%, the release gate thresholds are too permissive or the root causes are systemic.

### Step 4: Go/No-Go Decision

State the decision clearly. Do not hedge.

**GO** - all quality gates pass, open defects triaged and accepted.
**NO-GO** - one or more quality gates fail, or a P1 defect is open.
**CONDITIONAL GO** - specific conditions must be met before shipping (e.g., one P2 fix required, then re-test and re-sign-off).

### Step 5: Sign-Off Report

```
Release Sign-Off Report
Release: [version / release name]
Date: [date]
Environment: [staging / pre-prod]
QA Lead: [name]

Test Summary:
  Regression pass rate: [x]%
  Cases executed: [n] / [total]
  Open defects: P1: [n] | P2: [n] | P3: [n] | P4: [n]

Quality Gate Results:
  [gate name]: PASS / FAIL
  [gate name]: PASS / FAIL

Defect Triage:
  Fix before release: [IDs or "none"]
  Hotfix: [IDs + commitment date or "none"]
  Deferred: [IDs or "none"]
  Exceptions approved by: [name, title]

Decision: GO / NO-GO / CONDITIONAL GO
Conditions (if applicable): [what must happen before shipping]

QA Sign-Off: [name]
Date/Time: [timestamp]
```

## Defect Triage Session Format

When running a triage meeting with engineering and PM:

**Agenda (30 minutes max):**
1. Review open defect list - 5 min (QA lead presents)
2. Defect by defect - 20 min (owner proposes, team agrees on fix/defer/accept)
3. Final decision - 5 min (QA lead states go/no-go)

**Rules:**
- Every defect gets a decision. Do not leave any as "under investigation" going into release.
- PM can accept risk on P2/P3 defects. Engineering lead confirms effort estimate for same-day fixes.
- QA lead has veto on P1 decisions - no P1 ships without QA sign-off.

## Anti-Patterns

**Pressure-based approval**
"We promised the customer" is not a quality gate. If a P1 defect is open, the release is not ready. Document the business pressure and escalate - do not absorb it silently and approve anyway.

**Verbal sign-off**
Release decisions must be written. A Slack message saying "looks good to me" is not sign-off. Use the template, document the decision, attach it to the release ticket.

**Moving goalposts on quality gates**
Quality gates set the week before release should not be renegotiated the day before release. If business conditions change, escalate through the proper channel and document the new threshold and who approved it.

**Shipping without testing incomplete areas**
If 20% of the regression suite could not be executed, that is not "95% pass rate on what we ran." Incomplete coverage is a risk that must be called out explicitly.

**No post-release tracking**
Defects deferred or accepted for release must be tracked to resolution. Create follow-up tickets at triage time - not after the next defect reaches customers.

## Quality Checklist

Before issuing any release sign-off:

- [ ] Regression suite ≥ 95% complete
- [ ] All P1 defects resolved and verified
- [ ] Every P2 defect has a documented triage decision
- [ ] Quality gates evaluated against pre-agreed thresholds
- [ ] All exceptions documented with approver name
- [ ] Sign-off report written and attached to release ticket
- [ ] Decision is explicit: GO / NO-GO / CONDITIONAL GO
- [ ] Deferred defects have follow-up tickets created
