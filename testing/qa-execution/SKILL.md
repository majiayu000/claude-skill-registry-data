---
name: qa-execution
description: Run and document QA test execution cycles - smoke tests, regression suites, exploratory testing sessions, and release readiness checklists. Use this skill whenever a QA engineer needs to structure or report on active testing work. Trigger on phrases like "run smoke tests", "start a regression cycle", "exploratory testing session", "test this build", "release checklist", "is this build stable", "log test results", "what passed and what failed", "document my testing", "create a test run report", or any request to execute and record test outcomes. Also trigger when someone says "we need to test before release" or "can you help me track what I've tested".
---

## Overview

Based on **"Exploratory Software Testing"** by James Whittaker. Whittaker's Session-Based Test Management (SBTM) gives exploratory testing the rigor of scripted testing without losing the adaptability that makes it powerful. The charter is the unit of work. The time box is the constraint. The debrief is the accountability mechanism.

# QA Execution

Structure, run, and document test execution cycles from smoke checks to full regression.

## When to Use

- Running a smoke test on a new build
- Executing a regression suite before release
- Facilitating or documenting an exploratory testing session
- Producing a test run summary report
- Tracking what has and has not been tested in a sprint

## Inputs to Gather

1. **Test type** - smoke, regression, exploratory, or ad-hoc?
2. **Build/environment** - which environment, which version/build number?
3. **Scope** - which features or areas are in scope?
4. **Test cases or charter** - existing test cases, or freeform exploratory?
5. **Exit criteria** - what does "done" look like for this cycle?

## Execution Types

### Smoke Test

A fast sanity check - typically 10-20 minutes. Covers only critical paths.

**Goal:** Confirm the build is stable enough for deeper testing.

Run in this order:
1. Core authentication (login, logout, session handling)
2. Main user journey (the single most important flow for this product)
3. Critical integrations (payment, data sync, key API calls)
4. No P1 open defects blocking test execution

**Exit criteria:** All smoke cases pass. If any smoke case fails, reject the build and log a blocker.

**Output template:**

```
Smoke Test Result - [date] - [build/version]
Environment: [env name]
Tester: [your name or team]

| Test Area | Status | Notes |
|-----------|--------|-------|
| Auth | PASS/FAIL | |
| Main user journey | PASS/FAIL | |
| Critical integrations | PASS/FAIL | |

Result: PASS / FAIL
Blockers: [list or "none"]
Next step: [proceed to regression / reject build]
```

### Regression Test

Structured execution against a defined test suite. Verifies that existing functionality still works after changes.

**Pre-execution:**
- Confirm build version and environment
- Confirm test suite scope (full or targeted)
- Assign test cases if running as a team
- Note any known issues to exclude from blocking

**During execution:**
- Log pass/fail against each test case ID
- For each failure: capture screenshot, steps to reproduce, actual vs expected result
- Flag blockers immediately - do not complete the cycle with a P1 unresolved

**Post-execution:**
- Calculate pass rate: (passed / total) × 100
- List all failures with severity and assigned owner
- Make a go/no-go recommendation

**Output template:**

```
Regression Run - [date] - [build/version]
Environment: [env name]
Scope: [module or feature areas]

Summary:
  Total cases: [n]
  Passed: [n]
  Failed: [n]
  Blocked: [n]
  Pass rate: [x]%

Failures:
  [TC-ID] - [title] - [severity] - [owner]

Recommendation: GO / NO-GO
Rationale: [1-2 sentences]
```

### Exploratory Testing Session

Structured freeform testing guided by a charter. No predefined steps - the tester adapts based on what they find.

**Charter format:**

```
Mission: Explore [feature/area] to discover [type of risk]
Target: [specific screen, flow, or API]
Time box: [30 / 60 / 90 minutes]
Risks to probe:
  - [specific risk 1]
  - [specific risk 2]
Out of scope: [what not to test this session]
```

**Whittaker's HICCUPPS heuristic** - use to identify what to probe during a session:
- **H**istory - has this area broken before? Test it harder.
- **I**mage - does this match what the product claims to do?
- **C**omparable products - does it behave like similar products users expect?
- **C**laims - test every explicit claim in the spec, marketing, or docs
- **U**ser expectations - what would a reasonable user expect?
- **P**roduct - is it consistent with the rest of the product?
- **P**urpose - does it actually accomplish its intended job?
- **S**tatutes - does it comply with legal/regulatory requirements?

Run through HICCUPPS at the start of each charter to identify the sharpest angles of attack.

**During the session:**
- Note everything you tried, not just what failed
- Capture timestamps for major findings
- Log unexpected behavior even if it is not clearly a bug yet
- Stop at the time box - do not extend without a new charter

**Session notes template:**

```
Exploratory Session - [date]
Charter: [mission statement]
Tester: [name]
Duration: [actual time]

Areas covered:
  - [what you tested]

Findings:
  [ID] - [title] - [severity] - [reproduction steps summary]

Observations (not yet confirmed bugs):
  - [note]

Coverage gaps identified:
  - [what you did not get to]

Follow-up needed:
  - [next session charter or tickets to file]
```

## Defect Logging

Every defect logged during execution must include:

```
Title: [action] causes [unexpected result] on [component]
Environment: [env + build/version]
Severity: P1 / P2 / P3 / P4
Steps to reproduce:
  1. [step]
  2. [step]
Expected: [what should happen]
Actual: [what happens]
Evidence: [screenshot, video, logs - link or attach]
Reproducibility: Always / Intermittent / Once
```

Severity guide:
- **P1** - blocks core functionality, no workaround
- **P2** - impacts key flow, has workaround
- **P3** - minor functional issue
- **P4** - cosmetic or UX polish

## Anti-Patterns

**Rubber-stamp testing**
Going through test steps without thinking. If something looks odd, investigate it even if the test technically passed. The test case is a guide, not a script to mindlessly follow.

**No evidence capture**
A test that passes or fails with no screenshot or log is a test that cannot be verified, reproduced, or audited. Capture evidence even for passing tests in critical areas.

**Skipping blockers**
Never continue a regression cycle with a known P1 open. Document it, escalate it, and pause execution on affected areas. Completing a cycle while ignoring a blocker produces a meaningless pass rate.

**Testing only new features**
Regression means checking old things still work. New changes break existing behavior more often than they introduce new bugs. Weight regression coverage toward areas touched by the diff.

**No time box on exploratory sessions**
Exploratory testing without a time box drifts. A 2-hour session with no structure produces noise. Charter first, time box it, report at the end.

## Quality Checklist

Before closing any execution cycle:

- [ ] All executed test cases have a logged status (pass/fail/blocked)
- [ ] Every failure has a defect ticket with full reproduction steps and evidence
- [ ] Pass rate is calculated and recorded
- [ ] Blockers are escalated - not just logged
- [ ] Environment and build version are documented in the report
- [ ] Exploratory sessions have a written charter and closing notes
- [ ] Go/no-go recommendation is explicit, not implied
- [ ] Coverage gaps are documented for the next cycle
