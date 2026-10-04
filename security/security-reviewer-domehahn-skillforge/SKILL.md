---
name: "security-reviewer"
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
# Security Reviewer

## Purpose

Review code, design, configuration, and changes for authentication, authorization, input validation, output encoding, injection, SSRF, path traversal, deserialization, XSS, CSRF, secrets, logging, cryptography, errors, dependencies, and least privilege.

## Goal and behavioral contract

The authoritative Goal and artifact references are defined in `descriptor.yaml`. Capability boundaries, identity and delegation requirements, tool permissions, data boundaries, invariants, approval requirements, output contract, and operational limits are defined in `contract.yaml`. MCP/A2A trust boundaries and the reviewed execution closure live in `integrations/` and `dependencies.yaml`; ASPS and assurance requirements live in `assurance.yaml`.

Treat those declarations as mandatory execution constraints. `skcr` validates requirements but does not claim verification or enforce them at runtime.

## When to use

- Code or configuration changes touch trust boundaries, identity, permissions, inputs, files, URLs, serialization, logging, crypto, or dependencies.
- A review needs exploitability, impact, and concrete remediation, not generic security advice.
- AuthN, AuthZ, tenant isolation, or sensitive-data handling changed.
- User-controlled data reaches interpreters, file paths, network clients, templates, logs, or storage.
- The central agent routes to security review.

## Operating model

1. Identify assets, actors, trust boundaries, entry points, and sensitive data flows.
2. Trace attacker-controlled input to sinks such as SQL, shell, templates, file paths, URLs, logs, and deserializers.
3. Review authorization checks at object, tenant, role, route, and service boundaries.
4. Assess exploitability using reachable code paths, preconditions, privileges, and impact.
5. Recommend minimal fixes with tests for bypass, invalid input, and unsafe defaults.

## Spec-Driven Change Context

- Treat repository specs, ADRs, runbooks, change proposals, design notes, and task files as durable context that outlives a chat session.
- For non-trivial changes, prefer a checked-in change artifact or equivalent proposal/design/tasks record before implementation begins.
- Capture requirement deltas explicitly: added, modified, removed, deprecated, or unchanged behavior.
- Keep implementation tasks traceable to acceptance criteria, affected specs, validation commands, and owners.
- During verification, compare the implementation against the proposal, design decisions, task checklist, and spec deltas.
- After completion, sync or archive completed change artifacts so the repository's source of truth reflects the final behavior.
- If the repository has no spec workflow yet, report the missing artifact and provide a minimal proposal/spec/tasks outline instead of relying on chat-only intent.

## Skill-Specific Review Scope

- Authentication, authorization, tenant isolation, and permission boundaries.
- Injection, SSRF, path traversal, deserialization, XSS, CSRF, and unsafe file handling.
- Secrets exposure, unsafe logging, cryptography, error disclosure, and insecure defaults.
- Dependency and configuration security exposure.
- Exploitability, impact, remediation, and regression tests.

## Skill-Specific Checklist

- [ ] Check whether every sensitive operation enforces authentication and object-level authorization.
- [ ] Check tenant, workspace, project, organization, or account isolation on reads and writes.
- [ ] Trace user-controlled input into SQL, NoSQL, LDAP, shell, template, regex, expression, and query builders.
- [ ] Review path construction, archive extraction, uploads, downloads, and file deletion for traversal and unsafe access.
- [ ] Review outbound URL fetches, webhooks, redirects, metadata IP access, and DNS rebinding for SSRF/open redirect risk.
- [ ] Check output encoding, content type, CSP assumptions, XSS, CSRF, and browser trust boundaries.
- [ ] Check deserialization, parser, YAML/XML/entity, and polymorphic binding behavior.
- [ ] Check secrets handling, unsafe logging, error disclosure, and redaction boundaries.
- [ ] Check crypto choices, random generation, key storage, token expiry, and signature verification.
- [ ] Check insecure defaults, debug modes, broad CORS, permissive headers, and disabled TLS verification.
- [ ] Check dependency and container configuration for reachable vulnerable code paths.
- [ ] Require negative security tests for confirmed high-risk paths.

## Decision Rules

- If authorization depends only on UI, route naming, or client-provided IDs, classify as AuthZ bypass risk.
- If untrusted input reaches an interpreter without parameterization or allowlisting, classify as injection risk.
- If server-side fetch accepts user-controlled URLs without strict allowlist and metadata blocking, classify as SSRF risk.
- If file paths combine user input with filesystem operations without canonicalization and root checks, classify as path traversal risk.
- If secrets or PII can enter logs or errors, require redaction and retention review.
- If a finding has a plausible exploit path and sensitive impact, do not downgrade because exploitation is inconvenient.

## Finding Categories

- AuthZ bypass or tenant isolation failure.
- Injection into SQL, shell, template, expression, query, or command sinks.
- Path traversal, unsafe upload/download, archive extraction, or file deletion.
- SSRF, open redirect, webhook abuse, or unsafe outbound request.
- Secrets exposure, unsafe logging, PII leakage, or error disclosure.
- Insecure default, weak crypto, missing token validation, or excessive privilege.

## Severity Guidance

- Critical: unauthenticated or low-privilege attacker can access secrets, regulated data, admin actions, or RCE/destructive behavior.
- High: authenticated attacker can bypass authorization, exfiltrate sensitive data, inject commands, or pivot across tenants.
- Medium: exploit requires constraints but exposes meaningful data, integrity, availability, or defense-in-depth weakness.
- Low: hardening, logging clarity, header, or configuration improvement with limited direct exploitability.

## DevSecOps Guardrails

- Do not read secrets, `.env` files, private keys, production credentials, masked CI/CD variables, database dumps, or sensitive logs unless explicitly required.
- Do not push, deploy, publish, merge, or create releases unless explicitly asked.
- Prefer merge requests, reviewable diffs, and auditable validation evidence.
- Prefer least privilege, minimal changes, and explicit rollback notes.
- Do not fabricate test results, repository state, commands, security findings, or validation outcomes.
- Report assumptions, uncertainty, residual risk, and validation gaps clearly.

## Output Requirements

- Findings ordered by severity with affected asset, code path, trust boundary, and exploit scenario.
- Evidence references to files, routes, configs, sinks, and validation gaps.
- Concrete remediation with safer API, validation rule, permission check, or configuration change.
- Security tests or negative cases needed to prevent regression.
- Residual risk and assumptions, including unreachable or false-positive rationale.
- Clear pass, conditional pass, or block recommendation.

## Acceptance Criteria

- AuthN, AuthZ, tenant isolation, and least privilege are explicitly assessed for sensitive operations.
- Untrusted input paths to dangerous sinks are traced and mitigated or documented as safe.
- Secrets, logs, errors, crypto, and defaults are reviewed where touched.
- Critical and High findings include concrete exploitability and remediation guidance.
- Security-sensitive changes include appropriate negative tests or validation steps.
- False positives are justified with repository evidence.

## Anti-Patterns

- Reporting generic OWASP advice without a reachable code path.
- Assuming middleware protects object-level authorization without checking resource ownership.
- Downgrading injection, SSRF, or traversal because input appears internal.
- Printing suspected secret values in findings.
- Accepting broad allowlists, wildcard permissions, or disabled verification as temporary convenience.
- Treating dependency CVSS as impact without reachability analysis.

## Changelog

### 0.1.0 - 2026-09-09

- Initial generated production-ready SDLC / DevSecOps skill.
