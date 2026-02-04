---
name: test-strategy-planning
description: Create comprehensive test strategy documents following IEEE 829 structure. Plan test approach, scope, resources, and success criteria for software projects.
allowed-tools: Read, Write, Glob, Grep, Task, WebSearch, WebFetch
---

# Test Strategy Planning

## When to Use This Skill

Use this skill when:

- **Test Strategy Planning tasks** - Working on create comprehensive test strategy documents following ieee 829 structure. plan test approach, scope, resources, and success criteria for software projects
- **Planning or design** - Need guidance on Test Strategy Planning approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

A test strategy defines the overall approach to testing a software system. It establishes the scope, objectives, resources, schedule, and success criteria for testing activities before development begins.

## IEEE 829 Test Documentation Structure

| Document | Purpose |
|----------|---------|
| **Test Plan** | Master document defining test approach |
| **Test Design Specification** | Refinement of test approach for features |
| **Test Case Specification** | Individual test case details |
| **Test Procedure Specification** | Step-by-step execution procedures |
| **Test Item Transmittal Report** | Test deliverables handoff |
| **Test Log** | Chronological record of test execution |
| **Test Incident Report** | Documentation of anomalies |
| **Test Summary Report** | Overall test results and metrics |

## Test Strategy Template

```markdown
# Test Strategy: [Project Name]

## 1. Introduction

### 1.1 Purpose
[Why this test strategy exists and what it covers]

### 1.2 Scope
**In Scope:**
- [Feature/component 1]
- [Feature/component 2]

**Out of Scope:**
- [Feature/component X]
- [Third-party integrations (unless specified)]

### 1.3 References
- [Requirements document]
- [Architecture document]
- [Related standards]

## 2. Test Objectives

### 2.1 Business Objectives
- [Business goal 1 → Testing coverage]
- [Business goal 2 → Testing coverage]

### 2.2 Quality Objectives
| Quality Attribute | Target | Measurement |
|-------------------|--------|-------------|
| Functional Correctness | 100% critical paths | All acceptance tests pass |
| Performance | < 200ms p95 response | Load test results |
| Security | No critical vulnerabilities | Security scan results |
| Reliability | 99.9% uptime | Chaos testing results |

## 3. Test Approach

### 3.1 Test Levels

| Level | Scope | Responsibility | Tools |
|-------|-------|----------------|-------|
| Unit | Individual methods/classes | Developers | xUnit |
| Integration | Component interactions | Developers | xUnit + TestContainers |
| System | End-to-end workflows | QA | Playwright |
| Acceptance | Business requirements | QA + PO | SpecFlow |

### 3.2 Test Types

| Type | Coverage | Approach |
|------|----------|----------|
| Functional | All requirements | Requirement-based |
| Performance | Critical paths | Load/stress testing |
| Security | OWASP Top 10 | SAST + DAST + Pentest |
| Usability | Key user journeys | Heuristic evaluation |
| Accessibility | WCAG 2.2 AA | Automated + manual |

### 3.3 Risk-Based Prioritization

| Risk Area | Likelihood | Impact | Test Priority |
|-----------|------------|--------|---------------|
| [Payment processing] | Medium | High | P1 - Extensive |
| [User authentication] | Low | High | P1 - Extensive |
| [Reporting] | Low | Medium | P2 - Standard |
| [Admin settings] | Low | Low | P3 - Basic |

## 4. Test Environment

### 4.1 Environment Strategy

| Environment | Purpose | Data | Refresh Cycle |
|-------------|---------|------|---------------|
| Dev | Developer testing | Synthetic | On-demand |
| QA | Functional testing | Masked production | Weekly |
| Staging | Pre-prod validation | Production clone | Before release |
| Performance | Load testing | Scaled synthetic | Before release |

### 4.2 Infrastructure Requirements
- [Server specifications]
- [Network requirements]
- [Third-party service access]

## 5. Test Data

### 5.1 Data Strategy
- **Synthetic data**: Generated for unit/integration tests
- **Masked production data**: For realistic QA testing
- **Performance data**: Scaled to production volumes

### 5.2 Data Privacy
- [Anonymization requirements]
- [PII handling procedures]
- [Data retention policies]

## 6. Entry and Exit Criteria

### 6.1 Entry Criteria
- [ ] Requirements reviewed and approved
- [ ] Test environment available
- [ ] Test data prepared
- [ ] Test cases reviewed
- [ ] Build deployed to test environment

### 6.2 Exit Criteria
- [ ] All P1 test cases executed
- [ ] No critical defects open
- [ ] Code coverage ≥ 80%
- [ ] Performance targets met
- [ ] Security scan passed

## 7. Defect Management

### 7.1 Severity Levels

| Severity | Description | Resolution Time |
|----------|-------------|-----------------|
| Critical | System unusable | 4 hours |
| High | Major feature broken | 1 day |
| Medium | Feature degraded | 1 week |
| Low | Minor issue | Next release |

### 7.2 Defect Workflow
1. Tester logs defect with reproduction steps
2. Dev lead triages and assigns
3. Developer fixes and unit tests
4. Tester verifies fix
5. Defect closed or reopened

## 8. Test Deliverables

| Deliverable | Audience | Frequency |
|-------------|----------|-----------|
| Daily Test Status | Dev team | Daily |
| Test Summary Report | Management | Per sprint |
| Defect Metrics | All stakeholders | Weekly |
| Release Test Report | Release team | Per release |

## 9. Roles and Responsibilities

| Role | Responsibilities |
|------|------------------|
| Test Lead | Strategy, planning, reporting |
| QA Engineer | Test design, execution, defects |
| Developer | Unit tests, test support |
| Product Owner | Acceptance criteria, UAT |

## 10. Schedule

| Phase | Start | End | Milestone |
|-------|-------|-----|-----------|
| Test Planning | [Date] | [Date] | Strategy approved |
| Test Design | [Date] | [Date] | Test cases ready |
| Test Execution | [Date] | [Date] | All tests run |
| UAT | [Date] | [Date] | Sign-off |

## 11. Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Environment unavailable | Medium | High | Backup environment ready |
| Resource shortage | Low | Medium | Cross-training |
| Requirement changes | High | Medium | Change control process |
```

## Test Approach Patterns

### Risk-Based Testing

Prioritize testing based on:

1. **Business criticality**: Revenue-impacting features first
2. **Technical complexity**: Complex components need more testing
3. **Change frequency**: Frequently changed areas need regression focus
4. **Defect history**: Bug-prone areas need more attention

### Shift-Left Testing

Move testing earlier in the SDLC:

- Requirements testing (review for testability)
- Design testing (architecture review, threat modeling)
- Static analysis (before code review)
- Unit testing (during development)

### Continuous Testing

Integrate testing into CI/CD:

- Pre-commit: Linting, unit tests
- PR: Integration tests, code coverage
- Merge: Full regression, security scan
- Deploy: Smoke tests, synthetic monitoring

## Quality Metrics

### Coverage Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Requirement coverage | 100% | Requirements traced to tests |
| Code coverage (line) | ≥80% | Coverage tool output |
| Code coverage (branch) | ≥70% | Coverage tool output |
| Risk coverage | 100% P1 risks | Risk-test mapping |

### Execution Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Test pass rate | ≥95% | Pass / Total |
| Defect detection rate | ≥90% | Pre-release / Total |
| Test automation rate | ≥70% | Automated / Total |
| Defect leakage | <5% | Production defects / Total |

## .NET Example: Test Strategy Configuration

```csharp
// Directory.Build.props - Shared test configuration
<Project>
  <PropertyGroup>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <CollectCoverage>true</CollectCoverage>
    <CoverletOutputFormat>cobertura</CoverletOutputFormat>
    <Threshold>80</Threshold>
  </PropertyGroup>
</Project>
```

## Integration Points

**Inputs from**:

- Requirements documents → Test scope
- Architecture documents → Test levels
- Risk assessments → Test prioritization

**Outputs to**:

- `test-pyramid-design` skill → Pyramid ratios
- `test-case-design` skill → Test techniques
- CI/CD pipeline → Automation scope
