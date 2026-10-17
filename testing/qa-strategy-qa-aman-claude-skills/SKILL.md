---
name: qa-strategy
description: Create QA test strategy documents, coverage matrices, and risk-based test prioritization plans. Use this skill whenever a QA lead or manager needs to plan what to test, why, and at what depth. Trigger on phrases like "write a test strategy", "test strategy document", "what should we test", "prioritize testing", "risk-based testing", "test coverage plan", "QA approach for this project", "coverage matrix", "test scope", "how should we approach testing this quarter", "where are our coverage gaps", or any request to define the strategic plan for testing - not the execution of it. Also trigger at project kickoff when a QA lead asks "how do we approach quality on this?"
---

## Overview

Based on **"How Google Tests Software"** by Whittaker, Arbon & Carollo, and **"Agile Testing"** by Lisa Crispin & Janet Gregory. Google's core insight: quality is not QA's job - it's the whole team's job. QA's role is to accelerate quality by enabling developers to test better, not by testing everything themselves. Crispin & Gregory: the QA strategy starts at requirements, not at the end of the sprint.

# QA Strategy

Define what to test, why, at what depth, and in what order.

## When to Use

- Writing a test strategy for a new product, project, or major feature
- Prioritizing test coverage when time or resources are constrained
- Identifying coverage gaps in an existing test suite
- Creating a coverage matrix to communicate quality scope to stakeholders
- Planning QA work for a quarterly roadmap or sprint cycle

## Inputs to Gather

1. **Product scope** - what is being built? What already exists?
2. **Team size and skills** - how many QA engineers, automation capability?
3. **Timeline** - sprint, quarter, or project duration?
4. **Risk profile** - what failure modes would be most damaging? (data loss, revenue impact, compliance breach, reputational)
5. **Existing coverage** - what is already tested? Where are the gaps?
6. **Tech stack** - frontend, backend, mobile, APIs, integrations?

## Workflow

### Step 1: Define Scope

Write a clear scope statement:

```
In scope:
  - [feature / system / user flow]
  - [specific integrations or APIs]

Out of scope:
  - [what QA will not cover and why]
  - [what is covered by other teams: security, performance, accessibility]

Assumptions:
  - [dependencies that must be true for this strategy to hold]
```

### Step 2: Risk-Based Prioritization

Identify the top risks to quality. For each risk:

| Risk | Likelihood (H/M/L) | Impact (H/M/L) | Priority |
|------|-------------------|----------------|----------|
| [risk] | H/M/L | H/M/L | P1/P2/P3 |

Priority = Likelihood × Impact:
- H × H = P1 (test first, test deeply)
- H × M or M × H = P2 (test thoroughly)
- L × H = P2 (test because impact is severe even if rare)
- M × M or lower = P3 (test proportionally to capacity)

Common risk categories to consider:
- Data integrity (writes, deletes, migrations)
- Authentication and authorization (who can access what)
- Payment and financial flows
- Third-party integration failures
- Performance under load
- Cross-browser / cross-device compatibility
- Accessibility compliance
- Regulatory/compliance requirements

### Step 3: Coverage Matrix

Map test coverage to risk and feature area:

| Feature Area | Unit Tests | Integration Tests | E2E Tests | Manual Exploratory | Priority |
|-------------|-----------|------------------|-----------|-------------------|---------|
| [feature] | YES/NO/PARTIAL | YES/NO/PARTIAL | YES/NO/PARTIAL | YES/NO | P1 |
| [feature] | YES/NO/PARTIAL | YES/NO/PARTIAL | YES/NO/PARTIAL | YES/NO | P2 |

Coverage depth guide:
- **P1 areas** - unit + integration + E2E + exploratory. Full depth.
- **P2 areas** - integration + E2E. Spot exploratory.
- **P3 areas** - integration or E2E only. No dedicated exploratory time.

**Google's test distribution target (70/20/10 rule):**
- **70% unit tests** - fast, cheap, developer-owned, run on every commit
- **20% integration tests** - verify component interactions, shared ownership
- **10% E2E tests** - cover critical user journeys only, expensive to maintain

If your distribution is inverted (heavy E2E, light unit), the suite will be slow, brittle, and expensive to maintain. Shift left.

**Crispin & Gregory - whole team quality:** QA participates in story refinement, not just sprint testing. Flag untestable stories before sprint start, not after code is written.

### Step 4: Test Types and Ownership

Define who owns each test type:

| Test Type | Owner | Tooling | When Run |
|-----------|-------|---------|----------|
| Unit | Developer | [Jest/pytest/etc] | Every commit |
| Integration | Developer + QA | [testing framework] | Every PR |
| E2E / Regression | QA | [Cypress/Playwright/etc] | Pre-release |
| Exploratory | QA | Manual | Sprint end |
| Performance | QA / Platform | [k6/JMeter/etc] | Pre-release |
| Security | Security team | [tooling] | Quarterly |
| Accessibility | QA + Frontend | [axe/Lighthouse] | Per feature |

### Step 5: Write the Strategy Document

```
QA Test Strategy - [Project/Quarter]
Version: 1.0
Author: [name]
Date: [date]
Stakeholders: [PM, Eng Lead, QA team]

1. Objective
   [1-2 sentences: what quality outcomes does this strategy target?]

2. Scope
   [in scope / out of scope / assumptions]

3. Risk Assessment
   [risk table from Step 2]

4. Coverage Matrix
   [coverage table from Step 3]

5. Test Approach by Type
   [table from Step 4]

6. Entry and Exit Criteria
   Entry: [what must be true before QA begins testing a feature]
   Exit: [what must be true before QA signs off]

7. Defect Management
   [how defects are logged, triaged, prioritized, and tracked]

8. Tooling
   [list of tools and their purpose]

9. Risks to the Strategy
   [what could invalidate this plan: team capacity, late specs, env instability]

10. Open Questions
    [items that need resolution before this strategy is fully executable]
```

## Anti-Patterns

**Copy-paste strategy**
A test strategy that is 90% identical to the last project's strategy is not a strategy. It is a template. Strategies must be calibrated to the specific risk profile of this product, this team, and this timeline.

**No risk weighting**
Testing everything equally is the same as testing nothing strategically. Prioritize by impact and likelihood. A P1 risk with 20% coverage is more dangerous than a P3 risk with 100% coverage.

**Treating coverage as binary**
"We have tests for this" is not the same as "this is well tested." Track depth: are there unit tests only? Integration tests? E2E? Exploratory? Partial coverage should be called out, not hidden.

**Strategy without ownership**
Every test type must have a named owner. "QA will handle this" without naming who is a strategy that will not be executed. Assign by person or team, not by role abstraction.

**Writing strategy after testing starts**
A strategy written after execution begins is documentation, not planning. Write the strategy during sprint 0 or project kickoff - before any test cases are written.

## Quality Checklist

Before finalizing any QA strategy:

- [ ] Scope is explicit - in scope and out of scope both defined
- [ ] Risk assessment covers data, auth, payments, integrations, and compliance (at minimum)
- [ ] Coverage matrix maps each feature area to a coverage depth level
- [ ] Every test type has an owner and a trigger condition
- [ ] Entry and exit criteria are measurable, not subjective
- [ ] Strategy has been reviewed by PM and Eng Lead
- [ ] Open questions are tracked and assigned
- [ ] Strategy is versioned and stored where the team can find it
