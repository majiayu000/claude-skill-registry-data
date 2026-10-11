---
name: testing-qa
description: Author and execute unit, integration, invariant, and end-to-end verification suites with 100% pass targets.
---

# Testing & Quality Assurance

## Strategy
- **Layered Pyramid:**
  1. Fast unit tests for pure functions, algorithmic calculators, and feature extractors.
  2. Integration tests for API endpoints, database transactions, and model clients.
  3. System invariant tests verifying critical security boundaries and safety gates.
  4. End-to-end user journey tests.
- **Verification Discipline:**
  - Execute automated tests after every functional change.
  - Zero tolerance for flaky, commented-out, or ignored tests.
  - Assert empirical outputs and side effects, not trivial mock assertions.
