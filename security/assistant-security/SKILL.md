---
name: assistant-security
description: "Analyze threats, vulnerabilities, dependencies, and attack surfaces. Use for explicit security work or changes to auth, input, or sensitive data."
---

# Security Tools

## Contracts

| Contract | File | Purpose |
|---|---|---|
| **Input** | `contracts/input.yaml` | Analysis type, scope, severity threshold |
| **Output** | `contracts/output.yaml` | Findings with severity, remediation, and risk level |
| **Phase Gates** | `contracts/phase-gates.yaml` | Scope → Analyze → Report pipeline gates |
| **Handoffs** | `contracts/handoffs.yaml` | Subagent dispatch contracts (currently none) |

**Rules:**
- Every finding must have severity, impact, and remediation — observations without fixes are not actionable
- Severity levels follow the 4-level scale consistently
- Findings must be evidence-based — cite specific code, config, or dependency

On-demand security analysis. Use when touching auth, inputs, dependencies, or preparing for review.

## Goal

Identify concrete security risks with evidence, severity, impact, and remediation that can be acted on before release or merge. Keep the analysis practical and company-safe: local-first, no secret exposure, no unapproved external scanners, and no generic security essays.

## Success Criteria

- Scope, analysis type, and severity threshold are explicit.
- Findings cite specific code, config, dependency, or threat paths.
- Each finding includes severity, impact, and smallest useful remediation.
- Residual risks and unassessed areas are called out separately from findings.

## Constraints

- Do not report generic security advice without evidence in the reviewed surface.
- Ask only when missing scope or access prevents a trustworthy security conclusion.
- Treat exploitable vulnerabilities and secret exposure as blockers, not nits.
- Do not paste, log, or repeat secrets. Redact values and cite only the file/location.
- Do not require external SaaS scanners, remote code upload, or unapproved dependency installs; use local/repo-native checks when available.

## Available Tools

| Tool | File | When to use |
|---|---|---|
| **Threat Model** | `threat-model.md` | New features, auth changes, external integrations. STRIDE analysis. |
| **Code Review** | `code-review.md` | Before merging PRs touching auth, input handling, data access. OWASP Top 10. |
| **Dependency Audit** | `dependency-audit.md` | Before releases, after adding packages, periodic CVE checks. |
| **Attack Surface** | `attack-surface.md` | Starting security work, after adding endpoints/integrations. |

## Usage

Read the relevant tool file when the situation calls for it.

**When to use which tool:**
- Starting a new feature with external input -> Attack Surface first, then Threat Model
- Adding/updating NuGet packages -> Dependency Audit
- PR touches auth, sessions, or data access -> Code Review (OWASP)
- New API endpoints or integrations -> Threat Model (STRIDE)

**Deep analysis:**
For thorough threat modeling, also load `prompts/threat-model.md` — it provides a detailed prompt pack for comprehensive STRIDE analysis.

## Practical Review Checklist

Always scan relevant surfaces for:
- **Secrets exposure**: committed tokens, private keys, credentials, `.env` leaks, sensitive logs.
- **Auth and authorization**: missing checks, confused roles, tenant isolation, IDOR, privilege escalation.
- **Input handling**: validation gaps, injection paths, unsafe parsing, untrusted file names.
- **Data access**: SQL/NoSQL injection, overbroad queries, missing row-level filters, unsafe migrations.
- **Shell/process execution**: command injection, unsanitized arguments, PATH/env trust, unsafe temp files.
- **Path and file operations**: path traversal, unsafe extraction, symlink races, broad delete/write.
- **Network and integrations**: SSRF, webhook verification, TLS assumptions, replay handling, timeout/retry abuse.
- **Serialization**: unsafe deserialization, object injection, prototype pollution, untrusted YAML/XML.
- **Dependency/config risk**: vulnerable packages, dangerous debug flags, permissive CORS, exposed admin endpoints.
- **Privacy/logging**: PII leakage, customer data in telemetry, excessive error detail.

Only report checklist items with evidence in the reviewed scope. If a category is relevant but unassessed, list it under residual risk rather than inventing a finding.

## Finding Template

```markdown
### [severity] Short title

- Category: injection | auth bypass | secret exposure | unsafe dependency | etc.
- File: file path or `project-level`
- Description: what the security issue is
- Evidence: file:line/config/dependency/threat path, with secrets redacted
- Attack path: how an attacker or misuse reaches the issue
- Impact: data, integrity, availability, compliance, or privilege impact
- Remediation: smallest useful fix
- Verification: command/test/manual check that would prove the fix
```

The contract-required fields are `severity`, `category`, `description`, `impact`, and `remediation`; include them exactly in every finding. Use lowercase severity values (`critical`, `high`, `medium`, `low`) when producing structured output.

## Severity Scale

All tools use a consistent 4-level scale:
- **CRITICAL**: Immediate exploitation risk, data breach potential
- **HIGH**: Significant vulnerability, needs fix before release
- **MEDIUM**: Should fix, but not immediately exploitable
- **LOW**: Minor concern, fix when convenient

## Output

Return:
- **Status** - completion state and confidence for the security analysis.
- **Risk summary** - overall result and scope assessed.
- **Findings** - actionable items with severity, impact, evidence, and remediation.
- **Evidence** - specific code, config, dependency, or threat path for each finding.
- **Residual risk** - accepted risks, assumptions, or areas not assessed.
- **Blockers** - missing access, missing context, or follow-up questions required for confidence.

## Stop Rules

- Stop and ask when required source, dependency, or deployment context is unavailable and affects severity.
- Stop and escalate immediately if a secret, credential, or active exploit path is found.
- Do not finalize a clean security result when important scope was inaccessible; report the residual risk.
