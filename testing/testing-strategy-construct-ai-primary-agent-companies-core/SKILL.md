---
name: testing-strategy
description: >
  Use when planning how to test any deliverable or system. This skill provides a
  framework for selecting the right testing approach based on what is being delivered,
  ensuring comprehensive coverage without unnecessary overhead.
---

# Testing Strategy

## Overview
This skill guides agents in selecting and applying appropriate testing strategies for any deliverable. The right testing approach depends on what's being tested, its criticality, and the available time and resources.

## When to Use
- Before starting development to define testing approach upfront
- When planning how to verify a deliverable works correctly
- When deciding what types of tests to write and in what order
- When test coverage or quality is questioned
- When introducing a new feature, change, or fix
- **Don't use when:** Building throwaway prototypes or exploratory proofs of concept

## Core Procedures

### Step 1: Determine Testing Scope
Ask:
- What is the complexity of the deliverable? (simple/moderate/complex)
- What is the criticality? (low/medium/high/critical)
- Who will use it? (internal team/cross-company/end users)
- What are the failure consequences? (inconvene/degraded/blocked/harmful)

### Step 2: Select Testing Layers
Based on scope, select applicable testing layers:

| Deliverable Type | Required Testing | Optional |
|-----------------|-----------------|----------|
| Single function/method | Unit tests | Property-based tests |
| Module/component | Unit + integration tests | Performance tests |
| API/Service | Unit + integration + contract tests | Load/security tests |
| UI/Feature | Unit + E2E tests | Accessibility/usability tests |
| System/Platform | Integration + E2E + load tests | Security/chaos tests |
| Data/Analytics | Data validation tests | Accuracy/privacy tests |
| Prompt/AI output | Functional tests + evaluation tests | Bias/safety tests |
| Infrastructure | Integration + smoke tests | Chaos/disaster recovery tests |

### Step 3: Define Test Cases
For each testing layer, define cases covering:
1. **Happy Path:** Expected inputs produce expected outputs
2. **Edge Cases:** Boundary conditions, empty/null inputs, maximum values
3. **Error Cases:** Invalid inputs, missing dependencies, failure modes
4. **Regression Cases:** Previously discovered bugs, known issues

### Step 4: Prioritize Test Execution
Order:
1. Unit tests first (fast, cheap, isolate problems)
2. Integration tests second (verify component interaction)
3. E2E/system tests third (verify full workflow)
4. Performance/security tests as applicable
5. Manual/acceptance tests last

### Step 5: Set Coverage Targets
| Criticality | Minimum Coverage | Target Coverage |
|-------------|-----------------|-----------------|
| Low | 50% | 70% |
| Medium | 70% | 85% |
| High | 85% | 95% |
| Critical | 95% | 100% |

## Quality Checklist
- [ ] Testing scope appropriate for complexity and criticality
- [ ] All required testing layers included
- [ ] Happy path, edge cases, and error cases covered
- [ ] Tests are automated where possible
- [ ] Coverage targets defined and tracked
- [ ] Tests are maintainable (clear, independent, documented)

## Error Handling
- **Error:** Cannot automate a test case
  **Response:** Document manual test, explore automation alternatives, flag for future automation
- **Error:** Tests are too slow to run regularly
  **Response:** Separate into fast/slow suites, run fast suite on every change, slow suite on schedule
- **Error:** Tests are flaky (intermittent failures)
  **Response:** Fix or quarantine flaky tests immediately - they undermine confidence in test suite

## Cross-Team Integration
**Related Skills:** test-driven-development, testing-verification, output-validation-checklist, edge-case-analysis
**Used By:** ALL agents writing code or deliverables, especially testing agents (QA teams, Code Reviewers)