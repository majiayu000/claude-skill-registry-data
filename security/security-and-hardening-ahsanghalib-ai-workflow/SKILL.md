---
name: security-and-hardening
description: Use when reviewing or changing code that handles untrusted input, authentication, authorization, sensitive data, external integrations, file or URL access, dependencies, or other security boundaries. Do not use as a substitute for a threat model on an unrelated cosmetic or framework-independent change.
license: MIT
---

# Security and Hardening

Treat external input as hostile, secrets as sacred, and authorization as a
server-side responsibility. Make the trust boundaries and residual risk
explicit before changing security-sensitive behavior.

## When to use

Use this skill for code or configuration involving:

- HTTP requests, forms, uploads, webhooks, queues, or model-generated output.
- Authentication, authorization, sessions, permissions, or tenant isolation.
- Databases, sensitive data, logging, serialization, URLs, paths, or commands.
- External services, new dependencies, package installation, or supply-chain
  exposure.
- A security review, hardening pass, vulnerability fix, or abuse-case analysis.

For an unexplained security failure, pair this with `systematic-debugging`.

For AI-specific threats involving prompts, retrieval, memory, model output,
agent permissions, or tool/MCP boundaries, pair this with
`ai-security-review`. For dependency, CI, artifact, SBOM, provenance, or
release-chain reviews, pair this with `supply-chain-security`.

## Threat model first

Before implementation or review, record:

1. Assets: credentials, personal data, tokens, money, availability, and
   integrity-sensitive state.
2. Actors: anonymous users, authenticated users, other tenants, compromised
   dependencies, operators, and automated clients.
3. Trust boundaries: every point where data crosses from a user, model,
   network, process, file system, database, or environment into the system.
4. Abuse cases: spoofing, tampering, repudiation, information disclosure,
   denial of service, and privilege escalation.
5. Required invariants: who may perform each action, what data may cross each
   boundary, and what must never be logged or persisted.

Separate observed facts, assumptions, and unresolved risks. Do not treat a
static search as proof that a runtime consumer or attack path does not exist.

## Baseline controls

Apply only the controls relevant to the boundary, but check each explicitly:

- Validate and size-limit input at every external boundary. Prefer an
  allowlist/schema and reject unexpected fields, types, encodings, and values.
- Parameterize database queries and use the repository's safe data-access
  abstraction. Never concatenate untrusted values into queries or commands.
- Encode output for its destination. Treat HTML, URLs, shell arguments, SQL,
  templates, logs, and structured data as different contexts.
- Enforce authentication and authorization on the server for every protected
  operation. Validate object ownership and tenant scope; do not trust client
  flags or hidden fields.
- Keep secrets out of source, logs, prompts, URLs, fixtures, and error output.
  Do not read or print `.env` files, credential stores, private keys, or tokens.
- Use least privilege, secure transport, safe session/cookie settings, and
  security headers where the repository's application boundary requires them.
- Return safe, stable errors to callers and keep stack traces and sensitive
  diagnostic detail out of user-facing responses.
- For files and URLs, constrain schemes, hosts, size, and destination; prevent
  traversal, unsafe redirects, SSRF, and writing outside an approved directory.
- Review lockfiles and dependency install behavior before release. Do not
  force dependency upgrades or automated audit fixes without checking
  compatibility and the repository's approval policy.

## Approval gates

Pause for explicit approval before making changes that alter:

- Authentication, authorization, session, permission, or identity behavior.
- Sensitive-data collection, retention, deletion, export, or logging.
- External integrations, CORS, webhooks, uploads, rate limits, or elevated
  process/file/database permissions.
- Production data, deployment behavior, or a destructive migration.

Prepare the proposed change, affected boundary, rollback, and validation plan
before requesting that approval.

## Never weaken the boundary

- Do not disable validation, headers, TLS checks, authorization, or audit
  logging to make a test or integration pass.
- Do not use `eval`, dynamic code execution, or unsafe HTML insertion with
  untrusted data.
- Do not place authentication state where untrusted client code can read it.
- Do not trust client-side validation as the only validation layer.
- Do not log credentials, full tokens, personal data, raw model output, or
  sensitive request bodies.
- Do not expose stack traces, SQL, filesystem paths, or provider responses to
  untrusted callers.

## Review and verification workflow

1. Establish a safe baseline and identify the affected boundary.
2. Trace input, validation, authorization, transformation, storage, output,
   and error paths.
3. Test one threat or invariant at a time with redacted fixtures and the
   narrowest safe test seam.
4. Apply the smallest hardening change without removing existing defenses.
5. Run relevant tests, type/lint/build checks, dependency checks, and static
   analysis available in the repository.
6. Review the final diff for secret exposure, bypasses, unsafe defaults,
   missing authorization, and unintended data or permission changes.

Report the threat model, controls checked, evidence, approval-gated actions,
untested paths, and residual risk. A clean local check is not proof of security
against an untested deployment, provider, or runtime configuration.

## Upstream basis

Adapted for this harness-agnostic repository from
[addyosmani/agent-skills security-and-hardening](https://github.com/addyosmani/agent-skills/tree/6ca0cd7db39b41b1c37e26d335c507ee92382c6d/skills/security-and-hardening),
licensed under MIT.
