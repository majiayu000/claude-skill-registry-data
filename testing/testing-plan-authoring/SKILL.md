---
name: testing-plan-authoring
description: Testing Plan Authoring — Authors multi-layered QA strategies across unit, integration, contract, E2E/browser, accessibility, performance, and security testing, linking 100% of PRD acceptance criteria to executable test suites.
---

# SKILL: Testing Plan Authoring
## Domain: Quality Assurance, Verification Engineering, SDD Stations 11-13

**Activation triggers:** test plan, QA strategy, test matrix, E2E journey tests, acceptance criteria traceability, coverage targets, SDD Station 11.

---

## 1. Role & Engineering Law

The Testing Plan Authoring skill constructs the complete multi-layer verification strategy for the software product.  
It enforces the **Acceptance Criteria Verification Law**:
- Every single Acceptance Criterion (`[AC-FR-xxx-y]`) defined in the PRD MUST map directly to at least one automated test suite and specific test case.
- Any PRD acceptance criterion without an associated test case triggers a hard gate failure.
- Critical user journeys from the App Flow Document must be covered by end-to-end browser tests.

---

## 2. Document Structure & Required Sections

Every generated Testing Plan must follow `.factory/specifications/templates/09_testing_plan.template.md` and contain:
- **Header Metadata:** Document ID, Version, Status, Parent PRD ID, Parent App Flow ID, Target Specification, QA Lead, Date.
- **Section 1: Quality Assurance Strategy & Test Pyramid:** High-level testing philosophy and distribution.
- **Section 2: Test Strategy by Layer:**
  - Structured table defining Layer, Framework/Tooling, Target Scope, Coverage Threshold, and Execution Gate:
    - Unit Tests (pytest / Vitest) -> Gate G7 (>= 85% line)
    - Integration Tests (pytest-asyncio) -> Gate G8 (100% endpoints)
    - Contract Tests (Pydantic / Schemathesis) -> Gate G8
    - E2E / Browser QA (Playwright / BrowserOrchestrator) -> Gate G9
    - Accessibility (axe-core) -> Gate G9 (WCAG 2.2 AA)
    - Performance & Load (Locust / k6) -> Gate G11
    - Security SAST (ECC AgentShield / Bandit) -> Gate G10
- **Section 3: Critical User Journey Verification:**
  - Step-by-step E2E browser test specifications directly mapped from Journeys `J-01`, `J-02` in `03_app_flow.md`.
- **Section 4: Test Data & Fixture Isolation Strategy:**
  - DB isolation, mocking boundaries, seed data paths.
- **Section 5: Requirements Traceability Matrix (PRD Acceptance Criteria → Test Cases):**
  - Tabular mapping: `PRD Acceptance Criterion | Summary | Automated Test Suite / File | Specific Test Function / Case Name | Gate Link`.
- **Section 6: Signoff & Gate Linkage.**

---

## 3. Validation Checklist (Quality Gate G7-G13 & G0.5 Pre-Condition)

- [ ] Every `[AC-FR-xxx-y]` from the PRD appears in the Requirements Traceability Matrix.
- [ ] Every row links to an explicit test file and test function name.
- [ ] Critical user journeys from `03_app_flow.md` are accounted for in E2E specifications.
- [ ] All 7 test layers specify tools and thresholds.
- [ ] Document saved to `.factory/specifications/<project>/09_testing_plan.md`.
