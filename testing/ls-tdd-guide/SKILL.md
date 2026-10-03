---
name: ls-tdd-guide
description: Use when following a test-driven development workflow with test generation, coverage analysis, and multi-framework support.
metadata:
  version: "1.2"
compatibility: "Python 3.12+. Framework floors are authoritative in [framework-guide.md](references/framework-guide.md#compatibility-matrix). Scripts follow [TOOLING_POLICY.md](../../docs/TOOLING_POLICY.md) and [INPUT_HARDENING_STANDARD.md](../../docs/INPUT_HARDENING_STANDARD.md)."
---

# TDD Guide

Test-driven development skill for generating unit, integration, and E2E scaffolds; analyzing coverage; and guiding evidence-backed red-green-refactor workflows across Jest, Vitest, Pytest, JUnit, Mocha, and Jasmine adapters.

## Table of Contents

- [Capabilities](#capabilities)
- [Workflows](#workflows)
- [Tools](#tools)
- [Input Requirements](#input-requirements)
- [Compatibility](#compatibility)
- [Limitations](#limitations)

---

## Capabilities

| Capability | Description |
|------------|-------------|
| Test Generation | Convert requirements into distinct unit, integration, or E2E scenarios and templates |
| Coverage Analysis | Parse LCOV, Istanbul JSON, Cobertura XML, and JaCoCo XML; identify applicable gaps |
| TDD Workflow | Guide red-green-refactor cycles with phase-specific execution evidence |
| Framework Adapters | Generate imports, tests, assertions, suites, and setup for every CLI choice |
| Quality Scoring | Count tests without overlap and score assertions, isolation, naming, and smells on 100 points |
| Fixture Generation | Create realistic test data, mocks, and factories |

---

## Workflows

### Generate Tests from Code

1. Provide requirements as user stories, acceptance criteria, or API specifications.
2. Select `--test-type unit`, `integration`, or `e2e`; each choice changes scenarios, execution scope, and template guidance.
3. Select a compatible target framework and language.
4. Review and replace every generated placeholder assertion.
5. **Validation:** Compile and run the generated scaffold in the selected project.

### Analyze Coverage Gaps

1. Generate LCOV, Istanbul JSON, Cobertura XML, or JaCoCo XML from the project test runner.
2. Run `coverage_analyzer.py` with a threshold from 0 through 100.
3. Treat `null` branch coverage as not applicable for branchless files.
4. Review prioritized, file-specific uncovered lines and branches.
5. **Validation:** Confirm each applicable coverage dimension meets the target.

### TDD New Feature

1. Write the test first (RED) and run it.
2. Supply `status: failed`, `failure_kind: assertion` or `expectation`, and a non-empty `failure_message`.
3. Implement minimal code and supply a passing execution result (GREEN).
4. Refactor while keeping tests green; an unchanged optional refactor is valid.
5. **Validation:** Advance only when the current phase's structured evidence passes.

---

## Tools

Scripts are both importable Python modules and command-line tools. Run examples from the skill root (`ls/skills/ls-tdd-guide`) or adjust paths for your checkout.

| Tool | Purpose | Usage |
|------|---------|-------|
| `test_generator.py` | Generate test cases from requirements JSON | `python scripts/test_generator.py --input requirements.json --framework pytest --module auth` |
| `coverage_analyzer.py` | Parse and analyze coverage reports | `python scripts/coverage_analyzer.py --report lcov.info --threshold 80` |
| `tdd_workflow.py` | Guide red-green-refactor cycles | `python scripts/tdd_workflow.py --phase red --requirement "user can sign in"` |
| `framework_adapter.py` | Generate framework-specific snippets | `python scripts/framework_adapter.py --framework pytest --action imports` |
| `fixture_generator.py` | Generate test data and mocks | `python scripts/fixture_generator.py mock-data --schema-file schema.json --count 5` |
| `metrics_calculator.py` | Calculate test quality metrics | `python scripts/metrics_calculator.py --source app.py --tests test_app.py` |
| `format_detector.py` | Detect language and framework | `python scripts/format_detector.py --file source.ts` |
| `output_formatter.py` | Format JSON output for CLI/desktop/API | `python scripts/output_formatter.py --kind coverage --input summary.json` |

---

## Input Requirements

**For Test Generation:**
- Source code (file path or pasted content)
- Compatible framework/language pair (see the authoritative [compatibility matrix](references/framework-guide.md#compatibility-matrix))
- Test scope: `unit`, `integration`, or `e2e`

**For Coverage Analysis:**
- Coverage report file in LCOV, Istanbul JSON, Cobertura XML, or JaCoCo XML
- Optional source context
- Threshold from 0 through 100

**For TDD Workflow:**
- Feature requirements or user story
- Current phase (RED, GREEN, REFACTOR)
- Test code and implementation status

## Compatibility

Use the single authoritative [compatibility matrix and upstream sources](references/framework-guide.md#compatibility-matrix). Do not copy version floors into secondary references.

---

## Limitations

| Scope | Details |
|-------|---------|
| Generated scope | Unit, integration, and E2E outputs are scaffolds; replace placeholders and supply project-specific setup |
| Static analysis | Scripts do not execute tests; callers supply structured execution evidence |
| Language support | Best for TypeScript, JavaScript, Python, and Java |
| Report formats | Native support is LCOV, Istanbul JSON, Cobertura XML, and JaCoCo XML |
| Generated tests | Require human review for domain assertions and complex orchestration |

**When to use other tools:**
- E2E testing: Playwright, Cypress, Selenium
- Performance testing: k6, JMeter, Locust
- Security testing: OWASP ZAP, Burp Suite

## 2026-07 Refresh Note

Refresh classification: existing LocalSetup-native TDD coverage remains the target for TDD imports. Do not create a duplicate `ls-tdd-skill`; route TDD requests here and use `ls-test-runner` for framework-specific commands.
