---
name: terraform-iac
description: Author and operate Terraform with safe plans, reviews, and drift control
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
Model infrastructure in Terraform with reusable modules, secure state, reviewable plans, and validation routines.

### Trigger Conditions
- **Positive:** New Terraform module or stack; Refactoring Terraform for safety/performance; Drift detection and remediation
- **Negative:** Kubernetes-only changes (route to kubernetes-specialist); Single-service containerization (route to docker-containerization); Cloud governance strategy (route to cloud-platforms)

### Guardrails
- Structure-first: keep SKILL.md aligned with examples/, tests/, and any resources/references so downstream agents always have scaffolding.
- Adversarial validation is mandatory: cover boundary cases, failure paths, and rollback drills before declaring the SOP complete.
- Prompt hygiene: separate hard vs. soft vs. inferred constraints and confirm inferred constraints before acting.
- Explicit confidence ceilings: format as 'Confidence: X.XX (ceiling: TYPE Y.YY)' and never exceed the ceiling for the claim type.
- MCP traceability: tag sessions WHO=operations-{name}-{session_id}, WHY=skill-execution, and capture evidence links in outputs.
- Avoid anti-patterns: undocumented changes, missing rollback paths, skipped tests, or unbounded automation without approvals.

### Required Artifacts
- SKILL.md (this SOP)
- metadata.json
- examples/ for plans
- tests/ or checks for validation

### Execution Phases
1. **Model desired state**
   - Capture infra intent, regions, and providers
   - Define module structure, inputs/outputs, and constraints
   - Plan remote state, locks, and secrets handling

2. **Plan and review**
   - Generate terraform plan with targeted scope
   - Review for destructive changes, dependencies, and policy violations
   - Capture approvals and apply windows

3. **Apply safely**
   - Use workspaces or per-env state with locks
   - Apply in staged environments with monitoring
   - Record outputs and share with dependent teams

4. **Validate and monitor**
   - Run compliance, security, and drift checks
   - Set up automated plan/apply pipelines where appropriate
   - Document rollback strategies and state backup cadence

### Output Format
- Module map and state management plan
- Reviewed terraform plan with risk notes
- Execution record with outputs and owners
- Validation report (policy, security, drift)
- Runbook with rollback and backup procedures

### Validation Checklist
- Remote state secured with locking/backups
- Plans peer-reviewed with destructive changes flagged
- Applies executed in safe order with monitoring
- Drift and compliance checks configured
- Confidence ceiling stated for promotion

Confidence: 0.70 (ceiling: inference 0.70) - Terraform SOP enforces reviewable plans and drift controls
