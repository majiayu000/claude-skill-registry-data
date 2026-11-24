---
name: "tech-hiring-qa-test-engineering"
description: "QA and test engineers ensure software is reliable, correct, and meets quality standards before it reaches users. The role has evolved significantly from manual testing toward automation-first engineering. The highest-value profile in 2025 i"
---

# QA & Test Engineering — Hiring Guide

## How to Use This Guide

- **Sourcing:** Use the title synonyms and Boolean strings in each section
- **Screening:** Skill tiers: T1 = must-have, T2 = differentiator, T3 = rare upside
- **Interviewing:** Use the assessment approach to design your interview loop
- **Benchmarking:** Comp ranges are US market, growth-stage (Series B–D). Adjust for location, company stage, and current market

---

## Universal Seniority Framework

Applies across all disciplines. Use as a baseline — teams vary on exact year ranges.

| Level | Typical YoE | What they own | Mentorship | Scope |
|---|---|---|---|---|
| **Junior (L3 / IC1)** | 0–2 years | Defined tasks, bug fixes, small features | Needs daily guidance | Self |
| **Mid (L4 / IC2)** | 2–5 years | Features end-to-end, moderate ambiguity | Occasional junior support | Feature / component |
| **Senior (L5 / IC3)** | 5–8 years | Projects, technical decisions, cross-team coordination | Active mentorship | Team / project |
| **Staff (L6 / IC4)** | 8–12 years | Technical strategy, cross-team systems, org-wide standards | Multiplies teams | Org |
| **Principal / Distinguished** | 12+ years | Company-wide technical direction, external influence | Defines engineering culture | Company |

**Promotion-readiness signal:** Consistently operating at the *next* level before the title, not just meeting current-level expectations.

---

## QA & Test Engineering

### What This Role Does
QA and test engineers ensure software is reliable, correct, and meets quality standards before it reaches users. The role has evolved significantly from manual testing toward automation-first engineering. The highest-value profile in 2025 is the SDET (Software Development Engineer in Test) — someone who writes production-quality automation code. Manual-only QA is declining but still relevant for complex UX and accessibility testing.

### Titles & Synonyms

| Level | Common titles |
|---|---|
| Junior | QA Engineer, QA Analyst, Test Engineer, Junior SDET |
| Mid | QA Engineer, SDET, Automation Engineer, Test Automation Engineer |
| Senior | Senior QA Engineer, Senior SDET, Lead QA Engineer |
| Staff+ | Staff SDET, QA Architect, Head of Quality, Director of Engineering (QA) |
| Specialist | Performance Test Engineer, Accessibility QA, Mobile QA Engineer |

### Skill Tiers

**Tier 1 — Must-have (SDET):**
- Test automation: Playwright, Cypress, or Selenium for E2E; pytest, JUnit, or similar for unit/integration
- Programming proficiency: Python, JavaScript/TypeScript, or Java — they are engineers who test, not testers who code
- Understanding of test pyramid: unit → integration → E2E ratio and when each applies
- Bug reporting discipline: reproducible steps, environment context, severity classification

**Tier 1 — Must-have (QA Engineer):**
- Test case design: equivalence partitioning, boundary values, exploratory testing
- Regression testing strategy and maintenance
- Defect lifecycle management in tools (Jira, Linear, etc.)
- Basic scripting ability even for manual QA roles

**Tier 2 — Differentiator:**
- CI/CD integration: tests running in pipelines, flaky test management, parallelisation
- Performance testing: k6, Locust, JMeter, Gatling
- API testing: Postman, REST-assured, contract testing (Pact)
- Mobile testing: Appium, XCUITest, Espresso
- Accessibility testing: axe, Lighthouse, screen reader testing (NVDA, VoiceOver)
- Visual regression: Percy, Chromatic, Applitools

**Tier 3 — Bonus:**
- Chaos/resilience testing
- Security testing basics (OWASP, DAST)
- Shifting quality left — embedding QA in early design and spec review
- Open source contributions to test frameworks

### Sourcing Strings

```bash
# LinkedIn X-Ray — SDET focus
site:linkedin.com/in/ ("SDET" OR "software development engineer in test" OR "test automation engineer" OR "QA engineer") (Playwright OR Cypress OR Selenium OR pytest OR "test automation") -recruiter -talent

# Performance testing
site:linkedin.com/in/ ("performance test engineer" OR "load test" OR "QA engineer") (k6 OR JMeter OR Locust OR Gatling) -recruiter

# GitHub
site:github.com "joined on" (Playwright OR Cypress OR pytest OR "test automation") "QA" OR "SDET" OR "testing"
language:python topic:testing followers:>15 pushed:>2025-01-01
```

### Seniority Signals

- **Junior → Mid:** Moves from writing tests they were told to write to designing test coverage strategy for a feature
- **Mid → Senior:** Owns quality culture on the team; drives shift-left testing; reduces regression cycle time; partners with engineers on testability
- **Senior → Staff:** Defines organisation-wide quality strategy; builds shared testing infrastructure; influences engineering practices through tooling and process

### Red Flags
- "I do manual testing only" for a role requiring automation — unless you're hiring specifically for exploratory/accessibility QA
- Automation tests that are brittle, hardcoded, and nobody maintains
- No understanding of test pyramid — 100% E2E tests with no unit tests is a red flag
- "The developers should write tests, I just check the product" — insufficient ownership for an SDET
- No experience with CI/CD integration for test suites

### Compensation (2025, US, Growth-Stage)

| Level | Base salary range |
|---|---|
| Junior | $75k – $110k |
| Mid | $110k – $150k |
| Senior | $140k – $195k |
| Staff / QA Architect | $185k – $255k |

*QA typically earns 10–20% less than equivalent-level software engineers. SDETs close the gap — strong SDETs command SWE-equivalent compensation.*
