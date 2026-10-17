---
name: risk-based-testing
description: >
  Allocate testing effort based on risk and failure likelihood using Google's SET/SWE/TE model.
  Use when user says "risk-based testing", "where should I focus testing", "test coverage strategy",
  "prioritize what to test", "high risk areas", or needs to decide how to distribute QA effort
  across a codebase - even if they don't explicitly say "risk-based".
---

## Overview

Risk-based testing focuses effort where failures cause the most harm. Based on "How Google Tests
Software" by James Whittaker, Jason Arbon, and Jeff Carollo, this approach maps product risk to test
investment - instead of testing everything equally, you test the highest-risk components most deeply.

The core insight: not all code carries equal risk. A bug in a payment flow is not the same as a bug
in a tooltip. Risk-based testing makes that distinction explicit, then allocates testing hours
accordingly.

## Workflow

### Step 1: Map product into Attribute Component Capability (ACC) format

Break the product into three levels:
- **Attribute**: Quality characteristics users care about (reliable, secure, fast, correct)
- **Component**: Major subsystems or modules (auth, payments, search, notifications)
- **Capability**: Specific behaviors each component must support (login with OAuth, process refund, filter by date)

ACC gives you a structured map of what exists to test. Without it, coverage is guesswork.

### Step 2: Score each capability for risk

For every capability in your ACC map, assign two scores (1-3 scale):

| Dimension | 1 | 2 | 3 |
|-----------|---|---|---|
| **Likelihood of failure** | Low - stable, rarely changed | Medium - some recent changes | High - new, complex, frequently modified |
| **Impact of failure** | Low - cosmetic, no user harm | Medium - UX degraded, workaround exists | High - data loss, security, revenue, blocking |

**Risk score = Likelihood x Impact** (range: 1-9)

- Score 7-9: test deeply with all test types
- Score 4-6: standard coverage
- Score 1-3: smoke test only

### Step 3: Assign testing effort by risk tier

**High risk (7-9):**
- Unit tests for every branch
- Integration tests for all component interactions
- Exploratory testing sessions
- Security or performance testing where relevant

**Medium risk (4-6):**
- Unit tests for happy path and key edge cases
- Integration test for primary flow
- One exploratory session

**Low risk (1-3):**
- Smoke test: does it load, does the core path complete
- No deep coverage needed

### Step 4: Map risk to test roles (SET/SWE/TE split)

Google's three engineering roles cover different risk surfaces:

- **SET (Software Engineer in Test)**: Builds test infrastructure, writes unit and integration tests for
  high-risk components. Works closest to the code.
- **SWE (Software Engineer)**: Writes unit tests for their own code. Responsible for low-to-medium risk coverage.
- **TE (Test Engineer)**: Designs exploratory and system-level tests for high-risk capabilities. Thinks
  from the user perspective.

Map high-risk capabilities to TE-led sessions. Map medium-risk to SWE-owned tests. Low-risk stays in
automated smoke suites.

### Step 5: Build a risk register

Document findings in a table:

| Capability | Component | Likelihood | Impact | Risk Score | Test Type | Owner |
|-----------|-----------|-----------|--------|------------|-----------|-------|
| Process refund | Payments | 2 | 3 | 6 | Unit + integration | SET |
| Login with OAuth | Auth | 3 | 3 | 9 | Full suite + TE session | SET + TE |
| Update avatar | Profile | 1 | 1 | 1 | Smoke only | SWE |

Update this register at the start of each sprint as code changes shift the risk landscape.

### Step 6: Revisit after significant changes

Risk scores change. A stable module that gets refactored jumps to high likelihood. A new payment method
adds high impact. Review and re-score whenever:
- A component is significantly changed or refactored
- A production incident reveals a coverage gap
- New features are added to an existing module

## Anti-Patterns

**1. Equal coverage everywhere**
Bad: Spending the same testing effort on user avatar upload and the payment processor.
Good: Score risk, allocate proportionally. Low-risk code gets smoke tests. High-risk code gets deep coverage.

**2. Risk scoring without impact**
Bad: Scoring only likelihood - "this code is new so it's risky."
Good: Always multiply by impact. New code in a non-critical path is still low priority.

**3. Static risk register**
Bad: Score risk once at project kickoff and never revisit.
Good: Update scores at sprint start when code changes. Treat the register as a living document.

**4. Treating all bugs as equal**
Bad: Triaging all bugs with the same urgency regardless of location.
Good: A bug in a high-risk capability escalates immediately. A bug in a low-risk capability queues.

**5. No owner per capability**
Bad: Risk register exists but no one knows who tests what.
Good: Every high-risk capability has a named role owner (SET, TE, or SWE).

## Quality Checklist

- [ ] Product mapped into ACC format (Attribute, Component, Capability)
- [ ] Every capability has a likelihood score and an impact score (1-3 each)
- [ ] Risk tiers drive test type assignment (deep vs. standard vs. smoke)
- [ ] High-risk capabilities have named role owners
- [ ] Risk register is documented and shared with the team
- [ ] Plan exists to re-score after major code changes or incidents
- [ ] No personal names, project-specific paths, or internal tool references in output
