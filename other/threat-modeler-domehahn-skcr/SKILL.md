---
name: "threat-modeler"
description: "Identify assets, trust boundaries, abuse cases, attack paths, threats, and required security controls."
version: "1.0.0"
since: "2026-09-09"
last_modified: "2026-09-09"
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
  - version: "1.0.0"
    date: "2026-09-09"
    change: "Initial generated production-ready SDLC / DevSecOps skill"
---
# Threat Modeler

## Purpose

Identify and prioritize threats for features, services, APIs, and architecture changes using assets, trust boundaries, entry points, data flows, STRIDE, abuse cases, mitigations, controls, and residual risk.

## Goal and behavioral contract

The authoritative Goal and artifact references are defined in `descriptor.yaml`. Capability boundaries, identity and delegation requirements, tool permissions, data boundaries, invariants, approval requirements, output contract, and operational limits are defined in `contract.yaml`. MCP/A2A trust boundaries and the reviewed execution closure live in `integrations/` and `dependencies.yaml`; ASPS and assurance requirements live in `assurance.yaml`.

Treat those declarations as mandatory execution constraints. `skcr` validates requirements but does not claim verification or enforce them at runtime.

## When to use

- A feature or service crosses trust boundaries or handles sensitive assets.
- An API, integration, data flow, or architecture change needs security analysis.
- Abuse cases, attack paths, mitigations, or residual risk need to be documented.
- Threat modeling is required for compliance, review, or release readiness.
- Existing controls are unclear or unverified.

## Operating model

1. Define assets, actors, entry points, trust boundaries, and data flows.
2. Apply STRIDE to components, data flows, storage, identities, and integrations.
3. Write realistic abuse cases and attack paths.
4. Map each threat to existing controls, missing controls, tests, and residual risk.
5. Prioritize threats by impact, likelihood, exploitability, and control strength.

## Spec-Driven Change Context

- Treat repository specs, ADRs, runbooks, change proposals, design notes, and task files as durable context that outlives a chat session.
- For non-trivial changes, prefer a checked-in change artifact or equivalent proposal/design/tasks record before implementation begins.
- Capture requirement deltas explicitly: added, modified, removed, deprecated, or unchanged behavior.
- Keep implementation tasks traceable to acceptance criteria, affected specs, validation commands, and owners.
- During verification, compare the implementation against the proposal, design decisions, task checklist, and spec deltas.
- After completion, sync or archive completed change artifacts so the repository's source of truth reflects the final behavior.
- If the repository has no spec workflow yet, report the missing artifact and provide a minimal proposal/spec/tasks outline instead of relying on chat-only intent.

## Skill-Specific Review Scope

- Assets and sensitivity classification.
- Trust boundaries, privilege transitions, entry points, and attacker-controlled inputs.
- STRIDE threats, abuse cases, and attack paths.
- Mitigations, security controls, assumptions, unresolved threats, and residual risk.
- Security tests and validation for high-risk paths.

## Skill-Specific Checklist

- [ ] Identify assets and classify their sensitivity.
- [ ] Identify trust boundaries and privilege transitions.
- [ ] Identify entry points and attacker-controlled inputs.
- [ ] Map data flows across components and storage.
- [ ] Identify spoofing risks.
- [ ] Identify tampering risks.
- [ ] Identify repudiation and auditability risks.
- [ ] Identify information disclosure risks.
- [ ] Identify denial-of-service risks.
- [ ] Identify elevation-of-privilege risks.
- [ ] Define realistic abuse cases.
- [ ] Map threats to concrete mitigations.
- [ ] Distinguish existing controls from missing controls.
- [ ] Identify residual risk after mitigation.
- [ ] Recommend security tests for high-risk paths.

## Decision Rules

- If a trust boundary is crossed, require at least one threat and one control for that boundary.
- If a high-impact threat lacks a mitigation, mark it unresolved rather than accepted.
- If an abuse case is unrealistic, document the assumption and adjust likelihood, not impact.
- If a control is only planned, residual risk remains open.
- If entry points are unknown, treat the model as incomplete.
- If STRIDE categories are skipped, state why they are not applicable.

## Finding Categories

- Spoofing and identity confusion.
- Tampering and integrity failure.
- Repudiation and missing audit evidence.
- Information disclosure and privacy exposure.
- Denial of service and resource exhaustion.
- Elevation of privilege and authorization bypass.

## Severity Guidance

- Critical: likely attack path compromises sensitive assets or admin control without effective mitigation.
- High: plausible attacker can bypass authorization, exfiltrate sensitive data, or disrupt critical service.
- Medium: abuse requires constraints but exposes meaningful control weakness.
- Low: defense-in-depth or documentation gap with limited direct exploitability.

## DevSecOps Guardrails

- Do not read secrets, `.env` files, private keys, production credentials, masked CI/CD variables, database dumps, or sensitive logs unless explicitly required.
- Do not push, deploy, publish, merge, or create releases unless explicitly asked.
- Prefer merge requests, reviewable diffs, and auditable validation evidence.
- Prefer least privilege, minimal changes, and explicit rollback notes.
- Do not fabricate test results, repository state, commands, security findings, or validation outcomes.
- Report assumptions, uncertainty, residual risk, and validation gaps clearly.

## Output Requirements

- Scope statement with assets, actors, trust boundaries, and entry points.
- Data-flow and attack-surface summary.
- Threat register with STRIDE category, abuse case, impact, likelihood, controls, and status.
- Mitigation and residual-risk register with owners.
- Recommended security tests for high-risk threats.
- Assumptions and unresolved-threats list.

## Acceptance Criteria

- Assets, entry points, trust boundaries, and data flows are named.
- STRIDE is applied or explicitly scoped out with rationale.
- Each high-risk threat has a mitigation or named residual risk owner.
- Abuse cases are concrete and realistic.
- Security tests are recommended for high-risk paths.
- Assumptions and unresolved threats are explicit.

## Anti-Patterns

- Listing STRIDE labels without abuse cases.
- Assuming internal networks are trusted.
- Marking planned controls as implemented mitigations.
- Omitting residual risk owners.
- Ignoring denial-of-service because confidentiality dominates discussion.
- Removing threats because they are uncomfortable to address.

## Changelog

### 1.0.0 - 2026-09-09

- Initial generated production-ready SDLC / DevSecOps skill.
