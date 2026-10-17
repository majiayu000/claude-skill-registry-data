---
name: uat-plan
description: >
  Generate a User Acceptance Testing plan with scenarios and sign-off criteria. Use when the user says
  "UAT plan", "acceptance testing", "user testing plan", "how do we test this with users",
  "test scenarios for business validation", "sign-off criteria", "go/no-go for release",
  "acceptance test cases", "validate with stakeholders" - even if they don't explicitly say "UAT".
---

## Overview

Based on **Writing Effective Use Cases** by Alistair Cockburn - where each use case's main success scenario plus extensions directly become test scenarios. Also draws on **Mastering the Requirements Process** by Robertson & Robertson where Fit Criteria are the testable conditions for acceptance, and **Requirements Engineering** by Hull, Jackson, and Dick for the V-Model that maps business requirements directly to acceptance tests. The key insight: UAT scenarios should not be invented by testers. They should be derived directly from use cases (Cockburn), fit criteria (Robertson), and business requirements (Hull's V-Model). If you wrote good requirements, the UAT plan writes itself.

## Workflow

### Step 1: Define the UAT scope and approach
```
PROJECT: [name]
RELEASE: [version or phase being tested]
UAT OBJECTIVE: [what business validation is needed before go-live]
TESTERS: [who will perform UAT - business users, not QA team]
ENVIRONMENT: [UAT environment details - must mirror production]
TIMELINE: [start date, end date, buffer for defect resolution]
```

### Step 2: Define entry and exit criteria
```
ENTRY CRITERIA (before UAT starts):
- [ ] All functional testing passed (QA sign-off)
- [ ] UAT environment provisioned and verified
- [ ] Test data prepared and loaded
- [ ] Testers trained on new functionality
- [ ] Known defects documented with workarounds

EXIT CRITERIA (before release approval):
- [ ] [X]% of test scenarios passed (typically 95-100% for Must scenarios)
- [ ] Zero critical or high-severity defects open
- [ ] All Must requirements verified
- [ ] Business sign-off obtained from [role]
```

### Step 3: Derive test scenarios from requirements
Use the V-Model mapping: business requirements map to acceptance tests.

For each use case (Cockburn method):
- **Main success scenario** = 1 happy-path test scenario
- **Each extension** = 1 additional test scenario (error, alternate, edge case)

For each requirement with a fit criterion (Robertson method):
- **Fit criterion** = test condition
- **Measurement method** = test procedure

```
| Scenario ID | Source | Description | Type | Priority |
|------------|--------|-------------|------|----------|
| UAT-001 | UC-01 Main Success | Customer places order successfully | Happy path | Must |
| UAT-002 | UC-01 Ext 3a | Order fails: item out of stock | Error path | Must |
| UAT-003 | UC-01 Ext 5a | Customer applies expired coupon | Edge case | Should |
| UAT-004 | FR-ORD-005 Fit | Order total calculated correctly with tax | Calculation | Must |
```

### Step 4: Write detailed test scenarios
For each scenario:
```
SCENARIO: UAT-[number]
TITLE: [descriptive name]
DERIVED FROM: [use case ID + step, or requirement ID + fit criterion]
PRECONDITIONS: [setup required before executing]
TEST DATA: [specific data needed]

STEPS:
1. [Actor action]
2. [Expected system response]
3. [Actor action]
4. [Expected system response]

EXPECTED RESULT: [what success looks like]
ACTUAL RESULT: [filled during execution]
STATUS: [Pass / Fail / Blocked / Not Run]
DEFECT: [defect ID if failed]
TESTER: [name]
DATE: [execution date]
```

### Step 5: Organize scenarios by business process
Group scenarios to match how users actually work, not by technical feature:
```
Business Process 1: Order Placement
  UAT-001: Place standard order (happy path)
  UAT-002: Place order with out-of-stock item
  UAT-003: Apply coupon to order
  UAT-004: Order total calculation

Business Process 2: Order Fulfillment
  UAT-010: Warehouse receives order notification
  UAT-011: Pick and pack confirmation
  ...
```

### Step 6: Define the defect management process
```
DEFECT SEVERITY:
- Critical: Blocks core business process, no workaround
- High: Major functionality broken, workaround exists
- Medium: Minor functionality issue, does not block
- Low: Cosmetic or enhancement

DEFECT WORKFLOW:
Tester logs -> BA triages -> Dev fixes -> QA verifies -> Tester retests

GO/NO-GO RULE:
- Zero open Critical or High defects
- All Must scenarios passed
- Medium/Low defects documented with workarounds or deferred to next release
```

### Step 7: Output the UAT plan
```
# UAT Plan: [Project / Release]

## 1. Scope and Approach
## 2. Entry and Exit Criteria
## 3. Test Scenarios (grouped by business process)
## 4. Detailed Test Cases
## 5. Defect Management Process
## 6. Schedule and Responsibilities
## 7. Sign-off Template
```

Include a sign-off template:
```
I confirm that UAT for [release] is complete and the system meets
the agreed acceptance criteria for go-live.

Name: ________________  Role: ________________  Date: ________________
Signature: ________________
```

## Anti-Patterns

**1. UAT scenarios invented from scratch**
Bad: Testers make up test cases based on what they think the system should do.
Good: Every UAT scenario traces to a use case, requirement, or fit criterion. No requirement = no test.

**2. QA team performs UAT**
Bad: The same team that did functional testing also performs UAT.
Good: UAT is performed by actual business users or their representatives - they validate business value, not technical correctness.

**3. No entry criteria - UAT starts on broken software**
Bad: UAT begins before QA has signed off, wasting business users' time on known bugs.
Good: Strict entry criteria - UAT only starts when QA confirms the build is stable.

**4. "Explore and find bugs" instead of structured scenarios**
Bad: Telling users to "play around and let us know what's wrong."
Good: Structured scenarios with steps, expected results, and pass/fail recording.

**5. No exit criteria - UAT never ends**
Bad: UAT drags on because there's no clear definition of "done."
Good: Exit criteria defined upfront - specific pass rates, defect thresholds, and sign-off authority.

## Quality Checklist

- [ ] UAT scope, testers, environment, and timeline defined
- [ ] Entry criteria documented and met before UAT starts
- [ ] Exit criteria documented with specific pass rates and defect thresholds
- [ ] Every Must requirement has at least one UAT scenario
- [ ] Scenarios derived from use cases (Cockburn) or fit criteria (Robertson)
- [ ] Each scenario covers: steps, expected result, and pass/fail recording
- [ ] Scenarios grouped by business process, not technical feature
- [ ] Defect management process defined (severity, workflow, go/no-go)
- [ ] Sign-off template included with named authority
