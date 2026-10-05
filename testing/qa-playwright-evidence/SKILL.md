---
name: qa-playwright-evidence
description: "Trigger: QA, Playwright, E2E, regression, test plan. Produce reliable evidence for NutrIA releases."
license: MIT
metadata:
  author: "NutrIA"
  version: "0.1.0"
---

# Activation Contract
Use for feature validation and regressions.

# Hard Rules
- Derive tests from approved acceptance criteria.
- Prefer role/label/test-id locators and deterministic fixtures.
- Separate a product defect from a test or environment defect.
- Do not auto-close issues.

# Execution Steps
1. Create a human-readable scenario plan.
2. Generate focused tests for desktop and relevant mobile states.
3. Execute and retain failures/traces as evidence.
4. Report pass/fail, coverage gap and recommended Linear status.

# Output Contract
Return test evidence linked to the issue and explicit untested risks.
