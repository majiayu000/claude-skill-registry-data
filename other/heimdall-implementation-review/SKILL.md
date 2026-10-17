---
name: heimdall-implementation-review
description: Review delivered code, tests, queries, and dependencies for correctness, quality, and risk.
---

# Implementation Review

## Purpose

Validate concrete delivered artifacts — code, tests, database queries, and dependencies — for correctness, quality, and risk. This skill reviews work that has been completed or proposed for integration against requirements, performance standards, security standards, and prior analysis findings.

## When to Use

- When code changes need independent assessment of correctness and quality.
- When reviewing test suites for coverage adequacy and assertion quality.
- When validating that performance requirements are met in the implementation.
- When assessing implementations for security vulnerabilities and unsafe practices.
- When new dependencies are introduced or existing dependencies need health review.

## Workflow

1. **Identify which sub-domain(s) the brief invokes; apply only those subsections.**

### Code Correctness

Review code changes to ensure delivered work meets expectations.

- Trace every requirement to an implementation and verify it is present and correct.
- Check for edge cases that are or are not handled.
- Identify bugs, potential issues, and logic errors.
- Verify the code actually runs and behaves as expected.

### Tests

Evaluate test quality and effectiveness — not just whether they pass, but whether they actually validate correctness and cover edge cases.

- Identify which code paths are tested and which are not.
- Check for edge case coverage: boundary values, empty inputs, error paths, critical paths.
- Verify tests check behavior, not implementation details.
- Assess assertion quality — would this catch a regression?
- Flag over-mocking that makes tests tautological (tests verify mocks, not real behavior).
- Identify tests coupled to implementation details that break on harmless refactors.
- Identify critical-path coverage gaps by severity.

### Performance

Independently validate implementations against performance requirements and prior analysis findings. This is a validation skill: it reviews delivered work and changes against performance requirements — open-ended bottleneck investigation of a running system belongs to a prior performance analysis.

- Review database queries for missing indexes, N+1 patterns, or inefficient joins.
- Check for inefficient data structures, unnecessary allocations, or repeated work.
- Review locking, contention points, and connection pooling.
- Identify optimization opportunities with evidence and expected impact.
- Every performance concern must be backed by evidence (metrics, profiling, reasoning), not intuition.

### Security

Independently assess implementations for security vulnerabilities and unsafe practices. This is a validation skill: it reviews delivered work and changes against security standards — open-ended investigation of existing systems belongs to a prior security analysis.

- Identify trust boundaries and entry points systematically.
- Check for injection vulnerabilities (SQL, command, XSS, template).
- Verify input validation and output encoding.
- Check for hardcoded secrets, insecure defaults, or debug endpoints.
- Review encryption practices for data at rest and in transit.
- Review logging for sensitive data exposure.
- Systematically cover OWASP-class vulnerabilities.
- Secure against known threat models, never claim "secure."

### Dependencies

Review project dependencies to identify risks related to security, licensing, and maintenance status. This is a validation skill: it assesses dependency decisions and changes that have been delivered against quality standards — open-ended technology investigation and comparison of alternatives is out of scope for this review.

- Identify direct and transitive dependencies relevant to the review scope.
- Consult vulnerability databases (CVE, GitHub Advisory, OSV) for known issues in the specific versions in use.
- Evaluate severity and exploitability in the project's context.
- Check release frequency, maintainer count, and issue response times.
- Verify licenses are compatible with the project's usage model, including transitive dependencies.
- Assess breaking changes and migration risk.

## Quality Criteria

- Every requirement has been traced to an implementation and verified.
- All identified issues are documented with clear evidence or explanation.
- Feedback is actionable — the author knows exactly what to change.
- Findings are severity-categorized and evidence-backed, not intuition-based.
- Recommendations include expected impact, not just "this should be better."

## Anti-Patterns

- **Rubber-stamping**: Approving without thorough inspection.
- **Nitpicking only**: Focusing on trivial style issues while missing functional problems.
- **Assuming correctness**: Not verifying that the code actually runs or behaves as expected.
- **Coverage theater**: Measuring line coverage without assessing whether tests assert meaningful behavior.
- **Over-mocking**: Mocking so much that tests verify mocks, not real behavior.
- **Happy-path bias**: Testing only the expected flow, ignoring error and edge cases.
- **Implementation coupling**: Tests so tied to implementation details that they break on harmless refactors.
- **Micro-optimization focus**: Worrying about minor inefficiencies while ignoring systemic issues.
- **Ignoring the bottleneck principle**: Optimizing parts of the system that aren't the bottleneck.
- **Assuming external security**: Relying on firewalls, WAFs, or infrastructure instead of application-level security.
- **Version blindness**: Approving dependencies without checking the specific versions in use for known issues.
- **Ignoring transitive deps**: Reviewing only direct dependencies, leaving the transitive tree unexamined.
- **Silent approval**: Not raising concerns about outdated or unmaintained dependencies.
