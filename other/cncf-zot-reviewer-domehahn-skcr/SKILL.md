---
name: "cncf-zot-reviewer"
description: "Review zot using its official documentation and repository in the Provisioning / Container Registry category. Zot is an OCI-native container registry for distributing container images and OCI artifacts."
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
# Cncf Zot Reviewer

## Purpose

Review and operate zot using current official documentation, repository evidence, and its CNCF Landscape classification without treating Landscape inclusion as endorsement.

## Goal and behavioral contract

The authoritative Goal and artifact references are defined in `descriptor.yaml`. Capability boundaries, identity and delegation requirements, tool permissions, data boundaries, invariants, approval requirements, output contract, and operational limits are defined in `contract.yaml`. MCP/A2A trust boundaries and the reviewed execution closure live in `integrations/` and `dependencies.yaml`; ASPS and assurance requirements live in `assurance.yaml`.

Treat those declarations as mandatory execution constraints. `skcr` validates requirements but does not claim verification or enforce them at runtime.

## When to use

- zot code, configuration, APIs, deployment, integrations, dependencies, upgrades, or operations are in scope.
- A technology choice or migration involving zot requires evidence-backed assessment.

## Operating model

1. Detect the installed or proposed version and deployment model before giving version-sensitive guidance.
2. Use current official documentation and repository evidence; use the CNCF Landscape only for classification metadata.
3. Inspect boundaries with identity, secrets, network, storage, dependencies, observability, upgrades, rollback, and disaster recovery.

## Spec-Driven Change Context

- Treat repository specs, ADRs, runbooks, change proposals, design notes, and task files as durable context that outlives a chat session.
- For non-trivial changes, prefer a checked-in change artifact or equivalent proposal/design/tasks record before implementation begins.
- Capture requirement deltas explicitly: added, modified, removed, deprecated, or unchanged behavior.
- Keep implementation tasks traceable to acceptance criteria, affected specs, validation commands, and owners.
- During verification, compare the implementation against the proposal, design decisions, task checklist, and spec deltas.
- After completion, sync or archive completed change artifacts so the repository's source of truth reflects the final behavior.
- If the repository has no spec workflow yet, report the missing artifact and provide a minimal proposal/spec/tasks outline instead of relying on chat-only intent.

## Skill-Specific Review Scope

- CNCF classification: Provisioning / Container Registry
- CNCF project maturity field: sandbox
- First-party source: https://github.com/project-zot/zot
- configuration, APIs, architecture, security, reliability, performance, lifecycle, deployment, upgrade, rollback, and operations

## Skill-Specific Checklist

- [ ] Confirm product identity, version, edition, license, repository, deployment model, and supported dependencies.
- [ ] Check secure defaults, authentication, authorization, secret handling, network exposure, tenant isolation, data protection, and supply-chain provenance.
- [ ] Check resource limits, scaling, availability, state consistency, backup and restore, failure handling, observability, upgrades, compatibility, and rollback.
- [ ] Check official tests, project-specific validation, negative paths, operational runbooks, and deprecation or migration notices.
- [ ] Trace zot inputs, outputs, identities, trust boundaries, external dependencies, and persistent state.
- [ ] Check zot defaults, configuration precedence, environment separation, and drift from reviewed source.
- [ ] Check zot least privilege, credential rotation, audit events, policy enforcement, and break-glass behavior.
- [ ] Check zot resource ownership, cleanup, quotas, rate limits, timeouts, retries, and backpressure.
- [ ] Check zot release notes, supported upgrade paths, schema or API compatibility, and rollback constraints.
- [ ] Check zot dashboards, alerts, health signals, incident procedures, backup evidence, and recovery exercises.

## Decision Rules

- Do not infer CNCF project maturity, security, compatibility, or endorsement when the Landscape project field is absent.
- Do not invent commands, configuration, APIs, defaults, or compatibility; verify version-sensitive behavior in first-party sources.
- Do not deploy, mutate clusters or cloud resources, migrate data, or change production state without exact-scope authorization and rollback evidence.
- If zot identity, version, edition, or deployment model cannot be established, report the uncertainty before recommending a change.
- If a zot change can affect availability, security boundaries, persistent data, or external consumers, require staged validation and explicit rollback criteria.

## Finding Categories

- Version, identity, API, configuration, or lifecycle mismatch.
- Security, identity, secret, network, isolation, data, or supply-chain weakness.
- Reliability, scaling, state, backup, upgrade, rollback, observability, or operational gap.
- Landscape classification, maturity, licensing, maintenance, adoption, or migration assumption.
- zot documentation, ownership, maintenance, licensing, provenance, or evidence gap.

## Severity Guidance

- Critical: enables broad compromise, secret disclosure, destructive production action, cluster or tenant escape, or material data loss.
- High: causes exploitable access, sustained outage, corrupt state, unsafe upgrade, or loss of recovery capability.
- Medium: creates a bounded correctness, reliability, compatibility, observability, maintenance, or performance risk.
- Low: improves documentation, classification, idiomatic configuration, or validation evidence.

## DevSecOps Guardrails

- Do not read secrets, `.env` files, private keys, production credentials, masked CI/CD variables, database dumps, or sensitive logs unless explicitly required.
- Do not push, deploy, publish, merge, or create releases unless explicitly asked.
- Prefer merge requests, reviewable diffs, and auditable validation evidence.
- Prefer least privilege, minimal changes, and explicit rollback notes.
- Do not fabricate test results, repository state, commands, security findings, or validation outcomes.
- Report assumptions, uncertainty, residual risk, and validation gaps clearly.

## Output Requirements

- State detected versions, deployment model, Landscape classification, project field, and first-party sources checked.
- Return prioritized findings with affected artifacts, evidence, impact, remediation, validation, upgrade, and rollback guidance.
- Distinguish verified facts, source-derived inferences, and unresolved assumptions.
- Include a zot architecture and dependency summary with trust boundaries and persistent state.
- Include zot validation commands or tests that are safe for the stated environment.

## Acceptance Criteria

- Recommendations match the detected version and deployment model.
- Landscape inclusion is not presented as endorsement, certification, or security assurance.
- Material security, reliability, data, upgrade, rollback, and operational risks have evidence-backed disposition.
- zot identity, version, configuration, dependencies, and deployment assumptions are explicit.
- zot failure, upgrade, rollback, observability, and recovery paths have proportionate evidence.

## Anti-Patterns

- Generating generic product advice without checking the installed version or repository artifacts.
- Copying marketing claims into architecture or security conclusions.
- Running production commands or destructive examples merely to validate a recommendation.
- Assuming Landscape inclusion or popularity proves that zot is secure, supported, compatible, or suitable.
- Using an unpinned latest version of zot as the basis for migration or production guidance.

## Changelog

### 1.0.0 - 2026-09-09

- Initial generated production-ready SDLC / DevSecOps skill.
