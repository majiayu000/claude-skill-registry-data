---
name: rule-fedramp
description: MANDATORY when editing files matching ["api/src/**/*.py", "frontend/src/**/*.{ts,tsx}", "infra/**/*.tf", "**/Dockerfile*", ".github/workflows/**/*.yml"]. FedRAMP Moderate control alignment for code, infrastructure, and data flows
---

# FedRAMP Rules

simpler-grants-gov operates inside a FedRAMP Moderate authorization boundary. Every change must preserve that posture.

## Boundary Integrity

NEVER introduce a new outbound dependency (SaaS, CDN, analytics, LLM provider, email, SMS, error-tracking, data-warehouse) without an explicit entry in the System Security Plan (SSP) and an approved authorization package. ALWAYS route new integrations through adapters in `api/src/adapters/` so the boundary is auditable.

## Authentication and Access (AC, IA)

ALWAYS enforce least privilege on IAM roles and task policies. ALWAYS require MFA for human access paths. NEVER hardcode credentials or long-lived access keys. Session tokens MUST expire and rotate.

## Audit Logging (AU)

ALWAYS log security-relevant events (auth success/failure, privilege changes, data exports, admin actions) through the structured logger with stable event names. NEVER log PII or secrets (see `data-privacy.mdc`, `api-logging.mdc`). Audit logs MUST be tamper-evident and retained per the SSP.

## Encryption (SC)

ALWAYS encrypt data in transit with TLS 1.2+ and at rest via AWS KMS-managed keys. NEVER disable TLS verification in HTTP clients. NEVER write unencrypted PII to disk, S3, or backups.

## Configuration and Change (CM)

ALWAYS manage infrastructure via Terraform in `infra/`. NEVER apply changes out-of-band. Pin container base images and dependency versions (see `docker.mdc`).

## Vulnerability Management (RA, SI)

ALWAYS run SCA, SAST, and container scanning in CI. Block merges on high/critical findings unless explicitly waived. ALWAYS keep dependencies within supported versions.

## Incident Response (IR)

ALWAYS include correlation/trace IDs in logs so incidents can be reconstructed. NEVER delete audit trails.

## Grants.gov Coexistence

Integrations with legacy Grants.gov MUST stay inside the authorization boundary or use an ATO-covered interconnection. NEVER proxy PII to unauthorized systems.

---

## Related Rules

- **`security.mdc`** — code-level security controls
- **`data-privacy.mdc`** — PII classification and handling
- **`api-logging.mdc`** — structured audit-friendly logging
- **`docker.mdc`** — hardened container baselines
- **`infra.mdc`** — Terraform control implementations
- **`ci-cd.mdc`** — pipeline scanning gates

## Specialist Validation

**Simple (doc, lint):** None.
**Moderate (new adapter, new IAM policy):** Invoke `security-sentinel` and `codebase-conventions-reviewer`.
**Complex (new external integration, boundary change, new data flow):** Invoke `security-sentinel`, `architecture-strategist`, and `compliance-auditor` in parallel. A boundary change may also require an SSP update.
