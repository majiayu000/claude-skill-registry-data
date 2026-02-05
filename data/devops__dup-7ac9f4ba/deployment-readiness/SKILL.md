---
name: deployment-readiness
description: Verify service readiness before deployment with explicit go/no-go gates
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TodoWrite
model: sonnet
x-version: 3.2.0
x-category: operations
x-vcl-compliance: v3.1.1
x-cognitive-frames:
  - HON
  - MOR
  - COM
  - CLS
  - EVD
  - ASP
  - SPC
---




## STANDARD OPERATING PROCEDURE

### Purpose
Assess whether a service is ready to ship by validating requirements, risks, rollback posture, and observability hooks.

### Trigger Conditions
- **Positive:** Pre-flight for production deployment; Go/no-go decision needed; Release checklist review
- **Negative:** Active incident recovery (route to cicd-intelligent-recovery); Marketing or launch orchestration (route to sop-product-launch); Post-release ops maturity audit (route to production-readiness)

### Guardrails
- Structure-first: keep SKILL.md aligned with examples/, tests/, and any resources/references so downstream agents always have scaffolding.
- Adversarial validation is mandatory: cover boundary cases, failure paths, and rollback drills before declaring the SOP complete.
- Prompt hygiene: separate hard vs. soft vs. inferred constraints and confirm inferred constraints before acting.
- Explicit confidence ceilings: format as 'Confidence: X.XX (ceiling: TYPE Y.YY)' and never exceed the ceiling for the claim type.
- MCP traceability: tag sessions WHO=operations-{name}-{session_id}, WHY=skill-execution, and capture evidence links in outputs.
- Avoid anti-patterns: undocumented changes, missing rollback paths, skipped tests, or unbounded automation without approvals.

### Required Artifacts
- SKILL.md (this SOP)
- metadata.json for registry
- Add examples/tests/resources if missing during execution

### Execution Phases
1. **Clarify deployment scope**
   - Identify change set, owners, and environments
   - List hard/soft/inferred constraints and confirm risky areas
   - Check dependencies and service level objectives

2. **Evaluate readiness signals**
   - Review test coverage, CI status, and security checks
   - Verify observability, feature flags, and config toggles
   - Ensure data/backfill/migration plans are reversible

3. **Risk and rollback planning**
   - Define rollback/roll-forward criteria and time limits
   - Pre-stage smoke tests and monitors
   - Assign decision owners and approval gates

4. **Decide and document**
   - Publish go/no-go decision with evidence
   - Capture gaps, mitigations, and follow-up tasks
   - Update runbooks and notify stakeholders

### Output Format
- Deployment readiness brief with scope and risks
- Go/no-go criteria with owners and time boxes
- Rollback/roll-forward plan and validation steps
- Evidence links for tests, security, and observability
- Follow-up actions and runbook updates

### Validation Checklist
- Constraints confirmed and ambiguous items resolved or flagged
- Rollback path validated or rehearsed
- Critical tests and monitors in place with evidence links
- Decision recorded with approvals and communications
- Confidence ceiling stated for readiness call

Confidence: 0.70 (ceiling: inference 0.70) - structured pre-flight checklist with explicit rollback planning
