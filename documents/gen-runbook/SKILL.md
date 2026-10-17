---
name: gen-runbook
description: Generate an operational runbook from real system knowledge — alerts, playbooks, recovery steps
argument-hint: "[service-or-incident-type]"
related:
  - learn
  - create-report-in-dot-devin
  - deep-review-codebase
  - report-architecture-diagram
  - report
  - run-docs
---

## Goal

Generate an operational runbook from the real codebase and config — a document oncall/ops use when the system has problems: symptoms, diagnosis steps, mitigations, escalation

## Scope

- Covers: service overview, dependencies, common failure modes, diagnosis procedures, mitigation/rollback steps, escalation contacts
- Built from: architecture, deploy config, monitoring setup, past incidents (if any), code structure
- Output: a runbook doc in `.devin/` or `docs/` — does not modify code

## Execute

### 1. Map The System

> Goal: Understand the system being documented

1. Do `/learn` (codebase) or `/scan-codebase` — services, dependencies, data stores
2. Do `/report-architecture-diagram` if a visual overview is wanted
3. Identify deploy targets, environments, and external dependencies

### 2. Identify Failure Modes

> Goal: Collect how the system can break

1. From `/deep-review-codebase` findings — error handling, resilience gaps
2. External dependencies: DB down, API limits, queue backlog, cert expiry, DNS issues
3. App-level: memory leaks, deadlocks, bad deploys, config errors
4. Group into incident types: `outage`, `degraded`, `data-issue`, `security`

### 3. Write Runbook Structure

> Goal: Create a runbook that works during a panic

```markdown
# Runbook: <service>

## Quick Reference
- Dashboard: <url>, Logs: <where>, Deploy: <how>
- Escalation: <who/channel>

## Service Overview
- What it does, critical paths, SLA

## Dependencies
- <dep> — if down: <symptom + mitigation>

## Incident Playbooks

### <Incident Type>: <symptom>
**Detect**: <alert/signal>
**Diagnose**: <steps to find the cause — logs, metrics, queries>
**Mitigate**: <fix steps — restart, rollback, failover>
**Rollback**: <if the fix fails>
**Escalate**: <when and to whom>

## Common Operations
- Deploy, rollback, scale, secrets rotation

## Post-Incident
- Postmortem template, action items tracking
```

4. Fill in real copy-run commands — not floating "check the logs" advice

### 4. Validate Against Reality

> Goal: The runbook must be actually followable

1. Every command/path/query must be verified to exist in the repo/config
2. Clearly mark placeholders the user must fill (contacts, URLs not present in code)
3. Check that mitigation steps are not destructive without a warning

### 5. Report

> Goal: Deliver the runbook with its gaps

1. Save with `/create-report-in-dot-devin` or `docs/runbook-<service>.md`
2. Use `/report` to summarize: sections completed vs sections the user must fill
3. Suggest `/deep-review-codebase` if diagnosis steps lack required signals

## Rules

### 1. Runnable Steps

- Every diagnosis/mitigation step must be actually executable — verified commands
- Never write generic advice — a runbook is an executable doc

### 2. Evidence-Based

- Failure modes come from real code/config/findings — never guessed incident types
- Mark `[TODO: ...]` for data absent from the repo (contacts, external dashboards)

### 3. Safety First

- Destructive mitigation steps (rollback, restart, failover) must carry warnings and confirm points
- Escalation paths are explicit — a runbook does not mean handling everything alone
- Use /run-docs if needed

## Expected Outcome

- A runbook oncall can actually use during an incident
- Playbooks per failure mode with runnable steps
- Gaps to fill (contacts, dashboards) clearly marked
