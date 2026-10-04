---
name: "ci-cd-reviewer"
description: "Describe what this skill helps an agent do."
version: "0.1.0"
since: "2026-09-09"
last_modified: "2026-09-09"
authors:
  - "platform-engineering"
stability: "experimental"
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
  - version: "0.1.0"
    date: "2026-09-09"
    change: "Initial generated production-ready SDLC / DevSecOps skill"
---
# Ci Cd Reviewer

## Purpose

Review CI/CD pipelines, workflow permissions, secrets handling, runner trust, cache safety, artifact integrity, deployment gates, environments, approvals, provenance, and release automation.

## Goal and behavioral contract

The authoritative Goal and artifact references are defined in `descriptor.yaml`. Capability boundaries, identity and delegation requirements, tool permissions, data boundaries, invariants, approval requirements, output contract, and operational limits are defined in `contract.yaml`. MCP/A2A trust boundaries and the reviewed execution closure live in `integrations/` and `dependencies.yaml`; ASPS and assurance requirements live in `assurance.yaml`.

Treat those declarations as mandatory execution constraints. `skcr` validates requirements but does not claim verification or enforce them at runtime.

## When to use

- Workflow, pipeline, deployment, release, or runner configuration changes.
- Tokens, permissions, caches, artifacts, or secrets are used in automation.
- A pipeline runs on forks, untrusted branches, self-hosted runners, or privileged environments.
- Deployment gates, approvals, or environment protections need review.
- The central agent routes to CI/CD review.

## Operating model

1. Map triggers, actors, permissions, runners, secrets, caches, artifacts, and deployment targets.
2. Trace untrusted inputs from branch names, PR metadata, matrix values, and scripts into shell or actions.
3. Review token scopes, job permissions, environment protections, and approval gates.
4. Assess artifact and cache integrity across job boundaries.
5. Recommend least-privilege pipeline changes with validation steps.

## Spec-Driven Change Context

- Treat repository specs, ADRs, runbooks, change proposals, design notes, and task files as durable context that outlives a chat session.
- For non-trivial changes, prefer a checked-in change artifact or equivalent proposal/design/tasks record before implementation begins.
- Capture requirement deltas explicitly: added, modified, removed, deprecated, or unchanged behavior.
- Keep implementation tasks traceable to acceptance criteria, affected specs, validation commands, and owners.
- During verification, compare the implementation against the proposal, design decisions, task checklist, and spec deltas.
- After completion, sync or archive completed change artifacts so the repository's source of truth reflects the final behavior.
- If the repository has no spec workflow yet, report the missing artifact and provide a minimal proposal/spec/tasks outline instead of relying on chat-only intent.

## Skill-Specific Review Scope

- Workflow triggers, branch/tag filters, and fork behavior.
- Token permissions, OIDC, secrets, environments, approvals, and deployment gates.
- Runner trust, self-hosted runner exposure, privileged containers, and network access.
- Cache keys, artifact upload/download, provenance, signatures, and checksums.
- Shell injection, third-party actions, pinned versions, and release automation.

## Skill-Specific Checklist

- [ ] Check workflow triggers for pull_request_target, forks, tags, schedules, and manual dispatch risk.
- [ ] Check job permissions and default token scopes for least privilege.
- [ ] Check secrets availability by branch, environment, fork, and job boundary.
- [ ] Check shell commands for untrusted PR, branch, tag, matrix, or commit data.
- [ ] Check third-party actions, includes, templates, and images are pinned or trusted.
- [ ] Check cache keys for poisoning, privilege boundary crossing, and restore-key abuse.
- [ ] Check artifacts are integrity-protected before downstream use or deployment.
- [ ] Check self-hosted runner labels, isolation, cleanup, and access to secrets.
- [ ] Check deployment environments require approvals, protected branches, and rollback gates.
- [ ] Check release publishing requires provenance, signing, changelog, and explicit version inputs.
- [ ] Check logs do not reveal secrets or tokens.
- [ ] Check failed-job reruns cannot escalate privileges unexpectedly.

## Decision Rules

- If untrusted code can access secrets or write tokens, classify as blocking risk.
- If deployment happens without environment approval or protected ref policy, require a gate.
- If artifacts cross trust boundaries without integrity verification, flag artifact tampering risk.
- If caches are shared between untrusted and trusted jobs, flag cache poisoning risk.
- If shell commands include untrusted context without quoting or allowlisting, flag injection risk.
- If third-party actions are unpinned, require pinning or risk acceptance.

## Finding Categories

- Excessive token permissions or missing least privilege.
- Secret exposure across fork, branch, job, log, or environment boundary.
- Script injection from untrusted CI context.
- Cache poisoning or artifact integrity failure.
- Untrusted or overprivileged runner execution.
- Missing deployment gate, environment approval, provenance, or rollback control.

## Severity Guidance

- Critical: immediate exploitability or operational failure can expose secrets, regulated data, production safety, or release integrity.
- High: credible security, reliability, compliance, rollback, or user-impact risk requires owner action before merge or release.
- Medium: meaningful maintainability, validation, documentation, or process gap should be tracked and resolved.
- Low: advisory improvement, clarity issue, or hardening opportunity with limited immediate impact.

## DevSecOps Guardrails

- Do not read secrets, `.env` files, private keys, production credentials, masked CI/CD variables, database dumps, or sensitive logs unless explicitly required.
- Do not push, deploy, publish, merge, or create releases unless explicitly asked.
- Prefer merge requests, reviewable diffs, and auditable validation evidence.
- Prefer least privilege, minimal changes, and explicit rollback notes.
- Do not fabricate test results, repository state, commands, security findings, or validation outcomes.
- Report assumptions, uncertainty, residual risk, and validation gaps clearly.

## Output Requirements

- Pipeline risk summary with trigger, actor, token, runner, secret, artifact, and deployment boundaries.
- Findings with workflow file, job, permission, evidence, impact, and remediation.
- Recommended permission, trigger, secret, cache, artifact, or environment changes.
- Validation commands or CI checks to prove the fix.
- Release/deployment readiness recommendation.
- Residual risks and required owner approvals.

## Acceptance Criteria

- Token permissions are least privilege per job.
- Secrets are unavailable to untrusted code paths.
- Artifacts and caches do not cross trust boundaries without integrity controls.
- Deployment jobs have protected refs, environment gates, and rollback path.
- Third-party actions/images are pinned or trusted.
- Injection risks from CI context are mitigated.

## Anti-Patterns

- Using repository-wide write tokens by default.
- Running untrusted fork code with secrets.
- Trusting artifacts from earlier jobs without checksums or provenance.
- Sharing cache keys between trusted and untrusted jobs.
- Deploying directly from a build job with no approval gate.
- Pinning by branch name instead of immutable version or digest.

## Changelog

### 0.1.0 - 2026-09-09

- Initial generated production-ready SDLC / DevSecOps skill.
