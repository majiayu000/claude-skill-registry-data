---
name: cto-audit
description: Perform deep, expert-level codebase and architecture audits to identify technical strengths, weaknesses, risks, and opportunities. Use when a user asks for an assessment of a codebase's structure, quality, or readiness for scale. Deliver detailed, actionable, and prioritized recommendations grounded in engineering best practices.
---

# CTO Audit

## Overview

Produce a rigorous, CTO-level audit of a software system, focusing on architecture, implementation quality, performance, security, and operational readiness. Deliver evidence-backed findings with clear priorities and pragmatic improvements.

## Audit Workflow

1. Clarify scope and constraints
   - Identify repositories, services, environments, and time constraints.
   - Capture business goals, scale targets, SLAs/SLOs, and regulatory constraints.
   - Ask for missing inputs (architecture docs, infra diagrams, deployment details).

2. Map the system
   - Inventory components: services, data stores, queues, third-party dependencies.
   - Trace critical flows: request path, data lifecycle, and failure modes.
   - Identify system boundaries and ownership.

3. Inspect architecture and design
   - Evaluate modularity, separation of concerns, and dependency direction.
   - Identify overengineering, premature abstraction, or tight coupling.

4. Assess implementation quality
   - Verify correctness in critical paths; check error handling and edge cases.
   - Identify incomplete features, TODOs, stubs, or silent failure points.
   - Note code smells that degrade maintainability.

5. Evaluate performance and efficiency
   - Identify hot paths, heavy I/O, N+1 patterns, and memory pressure.
   - Assess scalability limits (CPU, database, cache, network).
   - Recommend targeted optimizations with expected impact.

6. Review security and reliability
   - Check input validation, authn/authz, secrets handling, and data exposure.
   - Evaluate resiliency: retries, timeouts, backoff, circuit breaking, idempotency.
   - Note incident response readiness and observability coverage.

7. Review tooling, testing, and ops
   - Inspect test coverage and critical gap areas.
   - Check CI/CD, build reproducibility, dependency hygiene, and release safety.
   - Assess runtime monitoring, alerting, and runbooks.

8. Synthesize and prioritize
   - Group findings by severity and theme.
   - Highlight what works well and why.
   - Produce a prioritized roadmap of fixes and upgrades.

## Evaluation Dimensions

- Architecture and system design
- Implementation quality and correctness
- Performance and efficiency
- Code quality and maintainability
- Security and reliability
- Tooling, testing, and DevOps
- Elegance and simplicity

## Evidence Standards

- Cite concrete evidence: file paths, line numbers, configs, or logs.
- Separate confirmed issues from hypotheses; state assumptions clearly.
- Avoid ungrounded claims; request missing data when needed.

## Output Format

Summary:
- State purpose and scope.
- Summarize the system overview (1-2 sentences).
- List key strengths (2-4 bullets).
- List top risks (2-4 bullets).

Findings (ordered by severity):
- Use severity buckets: Critical, High, Medium, Low.

For each finding, include impact, evidence, and a crisp fix direction.

Recommendations (prioritized):
1. List immediate fixes (safety and correctness).
2. List near-term improvements (quality, performance, maintainability).
3. List strategic investments (architecture, platform, scale).

Overall Assessment:
- State readiness for scale and operational risk.
- Provide a short rationale and confidence level.
