---
name: "finops-reviewer"
description: "Review cloud costs, budgets, rightsizing, reserved or committed usage, anomalies, showback or chargeback, and team cost transparency."
version: "1.1.0"
since: "2026-06-17"
last_modified: "2026-06-17"
authors:
  - "platform-engineering"
stability: "stable"
min_platform_version:
  codex: "unknown"
  amazon-q: "unknown"
  antigravity: "unknown"
  auggie: "unknown"
  bob: "unknown"
  claude-code: "unknown"
  cline: "unknown"
  codebuddy: "unknown"
  continue: "unknown"
  costrict: "unknown"
  crush: "unknown"
  github-copilot: "unknown"
  gitlab-duo: "unknown"
  factory: "unknown"
  forgecode: "unknown"
  opencode: "unknown"
  openhands: "unknown"
  cursor: "unknown"
  roo-code: "unknown"
  kiro: "unknown"
  junie: "unknown"
  gemini-cli: "unknown"
  iflow: "unknown"
  kilocode: "unknown"
  kimi: "unknown"
  lingma: "unknown"
  pi: "unknown"
  qoder: "unknown"
  qwen: "unknown"
  windsurf: "unknown"
  ollama: "unknown"
deprecated_since:
replaces:
supersedes: []
changelog:
  - version: "1.1.0"
    date: "2026-06-17"
    change: "Initial generated production-ready SDLC / DevSecOps skill"
---
# Finops Reviewer

## Purpose

Review cloud costs, budgets, rightsizing, reserved or committed usage, cost anomalies, showback or chargeback, and cost transparency per team or service. Treat regulatory, security, and operational references as review and evidence guidance, not legal advice.

## When to use

- FinOps decisions, controls, or operating practices need independent review.
- A change affects FinOps artifacts such as cloud bill, budget, rightsizing report, commitment plan, anomaly alert, showback view.
- The user needs evidence-oriented findings for risks such as unexplained cost spike, idle resource waste, wrong commitment, missing budget owner, opaque team spend, chargeback dispute.
- Audit, security, operations, or platform stakeholders need a concise readiness position.
- Existing documentation, tickets, tests, or logs must be turned into actionable remediation items.

## Operating model

1. Identify the relevant FinOps artifacts, owners, systems, environments, and review boundary.
2. Compare the available artifacts against expected signals such as cost allocation tag, utilization metric, forecast, reservation coverage, anomaly record, unit cost.
3. Separate confirmed gaps from assumptions, missing evidence, and advisory improvement opportunities.
4. Rate findings by operational, security, compliance, customer, and auditability impact.
5. Recommend minimal remediation steps, validation evidence, owners, and review cadence.

## Spec-Driven Change Context

- Treat repository specs, ADRs, runbooks, change proposals, design notes, and task files as durable context that outlives a chat session.
- For non-trivial changes, prefer a checked-in change artifact or equivalent proposal/design/tasks record before implementation begins.
- Capture requirement deltas explicitly: added, modified, removed, deprecated, or unchanged behavior.
- Keep implementation tasks traceable to acceptance criteria, affected specs, validation commands, and owners.
- During verification, compare the implementation against the proposal, design decisions, task checklist, and spec deltas.
- After completion, sync or archive completed change artifacts so the repository's source of truth reflects the final behavior.
- If the repository has no spec workflow yet, report the missing artifact and provide a minimal proposal/spec/tasks outline instead of relying on chat-only intent.

## Skill-Specific Review Scope

- Primary artifacts: cloud bill, budget, rightsizing report, commitment plan, anomaly alert, showback view.
- Risk themes: unexplained cost spike, idle resource waste, wrong commitment, missing budget owner, opaque team spend, chargeback dispute.
- Evidence signals: cost allocation tag, utilization metric, forecast, reservation coverage, anomaly record, unit cost.
- Ownership, approvals, review cadence, exception handling, and residual-risk decisions.
- Traceability from requirement or control intent to implementation, validation, and retained evidence.

## Skill-Specific Checklist

- [ ] Confirm the review boundary covers the right FinOps systems, teams, and environments.
- [ ] Inventory and inspect the current cloud bill.
- [ ] Check whether budget is current, approved, versioned, and owned.
- [ ] Verify that rightsizing report has test, ticket, log, or approval support.
- [ ] Look for unexplained cost spike and record concrete repository or process evidence.
- [ ] Look for idle resource waste and identify affected assets, services, or stakeholders.
- [ ] Look for wrong commitment and classify the operational or audit impact.
- [ ] Use cost allocation tag to validate that the control or practice is operating.
- [ ] Use utilization metric to confirm ownership, timing, and reproducibility.
- [ ] Check exception, risk-acceptance, and expiry handling for FinOps.
- [ ] Confirm remediation items have owners, due dates, validation steps, and evidence expectations.
- [ ] Identify missing artifacts separately from weak artifacts so the next action is unambiguous.
- [ ] Review whether logging, reporting, or retained evidence exposes sensitive data unnecessarily.

## Decision Rules

- If cloud bill is missing for a critical service, raise at least a high-severity readiness gap.
- If utilization metric cannot be tied to an owner and approval, treat the outcome as unauditable until corrected.
- If commitment plan is present but expired or untested, require validation before accepting residual risk.
- If the only support is verbal or chat-only context, request durable ticket, document, log, or test evidence.
- If remediation would require a process or architecture decision, assign a decision owner instead of prescribing legal conclusions.
- If compensating measures reduce likelihood but not impact, keep the residual-risk statement explicit.

## Finding Categories

- Missing or stale FinOps artifact.
- Unclear ownership, approval, review cadence, or accountability.
- Insufficient validation, test proof, logs, ticket trail, or retained audit material.
- Unreviewed exception, residual risk, expiry, or compensating measure.
- Policy, architecture, operational, or platform implementation drift.
- Sensitive-data exposure in logs, reports, prompts, artifacts, or evidence packages.

## Severity Guidance

- Critical: a gap in FinOps creates immediate outage, data-loss, privilege, regulatory-reporting, or irreversible business risk.
- High: cloud bill is missing, unowned, untested, or unauditable for a critical service or material change.
- Medium: budget exists but is stale, incomplete, inconsistently enforced, or weakly evidenced.
- Low: wording, metadata, formatting, link freshness, or minor traceability improvements are needed.

## DevSecOps Guardrails

- Do not read secrets, `.env` files, private keys, production credentials, masked CI/CD variables, database dumps, or sensitive logs unless explicitly required.
- Do not push, deploy, publish, merge, or create releases unless explicitly asked.
- Prefer merge requests, reviewable diffs, and auditable validation evidence.
- Prefer least privilege, minimal changes, and explicit rollback notes.
- Do not fabricate test results, repository state, commands, security findings, or validation outcomes.
- Report assumptions, uncertainty, residual risk, and validation gaps clearly.

## Output Requirements

- Findings ordered by severity with affected FinOps artifacts and evidence references.
- Coverage note for reviewed artifacts: cloud bill, budget, rightsizing report, commitment plan, anomaly alert, showback view.
- Risk note covering relevant themes: unexplained cost spike, idle resource waste, wrong commitment, missing budget owner, opaque team spend, chargeback dispute.
- Evidence request list using expected signals: cost allocation tag, utilization metric, forecast, reservation coverage, anomaly record, unit cost.
- Deliverables or updates needed: FinOps review, savings opportunities, budget risk list, rightsizing actions, showback improvement plan.
- Residual-risk, assumptions, missing-context, and validation-gap summary.

## Acceptance Criteria

- Relevant FinOps artifacts are identified, current, owned, and versioned where applicable.
- Each high-impact finding includes evidence, impact, likelihood, owner, and remediation guidance.
- Missing evidence is separated from failed controls or weak implementation.
- Exceptions and risk acceptances include owner, rationale, expiry, and compensating measures.
- Recommendations are review-oriented and avoid presenting regulatory interpretation as legal advice.
- Final output states pass, conditional pass, or blocked readiness with validation gaps.

## Anti-Patterns

- Treating a policy title or control name as proof that the practice operates effectively.
- Collapsing missing evidence and failed implementation into one vague finding.
- Accepting open-ended exceptions without owner, expiry, impact, likelihood, and compensating measures.
- Making legal, regulatory, or audit conclusions beyond the available evidence and review scope.
- Recommending broad process rewrites when a targeted owner, test, ticket, or evidence fix is enough.
- Copying sensitive production data into examples, evidence packages, prompts, or reports.

## Changelog

### 1.1.0 - 2026-06-17

- Initial generated production-ready SDLC / DevSecOps skill.
