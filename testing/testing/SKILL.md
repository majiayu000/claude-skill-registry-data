---
skill_id: testing
name: Testing & Quality Assurance
description: "Test and assure quality — test plan, QA, coverage, unit test, integration test, end-to-end, performance, benchmark, regression. Applies TDD and FIRST principles for the CTO office's tester."
version: 1.0.0
category: testing
office: CTO
lead_agent: tester
triggers:
  - test
  - QA
  - coverage
  - unit test
  - integration test
  - e2e
  - performance
  - benchmark
  - test plan
  - regression
  - load test
  - API testing
collaborates_with:
  - api-tester
  - implementer
  - release-manager
  - security-analyst
  - compliance
  - experiment-tracker
---

# Testing & Quality Assurance -- Domain Dispatcher

> Office: CTO | Lead: tester
> Sub-skills: 5 | Frameworks: Test Pyramid, TDD, BDD, Given/When/Then

## Purpose

The CTO's quality assurance domain -- the `tester` orchestrator uses this skill for all cross-cutting QA workflows. This skill covers API testing, performance benchmarking, test results analysis, tool evaluation, and workflow optimization. Maxim applies behavioral science to quality culture, ensures test coverage gates are enforced before releases, and proactively loops compliance when test data involves PII.

## Sub-Skill Routing

| Task Signal | Routes To | SKILL.md Path |
|---|---|---|
| API testing, endpoint validation, contract testing | api-tester | api-tester/SKILL.md |
| load testing, stress testing, capacity planning, latency profiling | performance-benchmarker | performance-benchmarker/SKILL.md |
| test results analysis, test report, coverage report, regression analysis | test-results-analyzer | test-results-analyzer/SKILL.md |
| QA tool assessment, testing platform selection, automation framework eval | tool-evaluator | tool-evaluator/SKILL.md |
| workflow optimization, process improvement, bottleneck removal | workflow-optimizer | workflow-optimizer/SKILL.md |

## Activation

This domain activates when:
- User invokes `/mxm-test`
- Task contains keywords: test, QA, coverage, unit test, integration test, e2e, performance, benchmark, load test, stress test, regression, API testing, test plan, test data, test results
- Executive router detects quality assurance, testing, or validation signals
- Other Maxim skills proactively loop here: engineering (test scaffolding), security (security testing), compliance (PII in test data)

## Behavioral Layer

- Confidence: 🟢 HIGH (Maxim skill + external knowledge merged)
- Compliance: reads project-manifest.json before decisions
- Handoff: writes .mxm-skills/agents-handoff.md on completion
- Ethics gate: none -- standard Maxim behavioral output quality applies. Exception: when test data involves real PII or production data, compliance skill auto-looped immediately (CSO auto-loop rule). `test-data-generator` must use synthetic/masked data by default.
- Frameworks: Test Pyramid (unit > integration > e2e), TDD (Red-Green-Refactor), BDD (Given/When/Then), Contract Testing, Chaos Engineering, Performance Testing Patterns

## External Sources

- Primary: community-packs/claude-skills-library/ra-qm-team/ (QA frameworks, test plan templates, quality management standards)
- Secondary: community-packs/claude-skills-library/engineering-team/ (engineering test patterns, unit/integration test conventions)
- Conflict resolution: Maxim ALWAYS WINS

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
