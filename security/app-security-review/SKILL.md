---
name: app-security-review
description:
  Review repositories, features, or diffs for exploitable application security weaknesses, including injection,
  authentication and authorization failures, exposed APIs, and broken trust boundaries. Applies to web applications,
  APIs, CLIs, workers, and libraries. Produce findings and remediation recommendations. Route content abuse and
  moderation concerns to trust-and-safety-review when available.
---

# Application Security Review

Find credible attack paths in the current project and recommend concrete fixes at the boundary where trust should be
enforced. Emphasize web application security across frontend and backend code while adapting the method to APIs, CLIs,
workers, libraries, or other application surfaces.

This skill has no required language, framework, deployment environment, browser, running server, scanner, or connector.
Use the source, designs, configuration, contracts, and tools available for the requested review.

## Scope and routing

- Honor the requested repository, feature, diff, or surface. For a diff, inspect surrounding callers and controls to
  establish behavior without turning the review into an unrelated repository-wide audit.
- Cover technical exploits, exposed capabilities, unsafe defaults, and security-relevant business logic. A public API is
  not inherently unprotected; establish which actions and data should require authorization.
- Content-driven phishing, scams, harassment, and moderation policy belong to `trust-and-safety-review` when available.
  Neither skill requires the other to be installed. Explain overlapping issues once and flag adjacent concerns without
  silently expanding the review.
- Default to inspection and findings. Fix code only when the user's request authorizes fixes. Use existing permission
  for bounded local verification; a review alone does not authorize probing live services, accessing other users' data,
  load testing, or changing external state.

## Establish the project context

Read relevant project instructions, security documentation, manifests, configuration, and representative entry points.
Determine the actual stack and versions before relying on framework behavior. Identify:

- Entry points such as routes, server actions, RPC or GraphQL operations, WebSocket messages, webhooks, command
  arguments, file imports, and background jobs.
- Assets and actors: sensitive data, secrets, privileged operations, anonymous users, account roles, tenants, and
  service identities.
- Trust boundaries between clients, servers, storage, processes, external services, and any local operating-system
  privileges. Identify which actor can control each input or configuration value.
- Existing protections in middleware, gateways, service methods, database policies, libraries, and deployment
  configuration, including whether the reviewed path actually reaches them.

Review the surfaces that exist. For frontend-only code, inspect client-side sinks and data exposure, and mark
unavailable server enforcement as unverified. For backend or CLI code, trace API, input, file, process, and credential
boundaries without requiring a browser. A local command using its caller's existing permissions is not automatically a
privilege escalation.

If deployment configuration or another component is unavailable, record the dependency as an uncertainty. Do not invent
missing infrastructure or treat an unknown control as an established vulnerability.

## Trace and assess attack paths

Use the relevant sections of [references/attack-surfaces.md](references/attack-surfaces.md) after identifying the
project's surfaces. Treat them as coverage prompts, not findings or a requirement to check absent features.

For each candidate:

1. Identify the attacker's starting access and controlled input.
2. Follow the reachable path through parsing, validation, identity, authorization, transformation, and side effects.
3. Locate the sensitive operation or data exposure and the control that should enforce the intended boundary.
4. Inspect shared protections and plausible counterevidence before concluding that the path is exploitable.
5. Explain the concrete impact, deployment or state prerequisites, and the smallest suitable remediation.

Do not substitute a suspicious function name, missing local guard, or scanner warning for a complete path. Check
authorization for the action, object, tenant, and fields involved; authentication alone does not establish permission.
Client-side validation, hidden buttons, CORS, and unguessable identifiers do not replace server-side authorization.

Distinguish exploitable defects from defense-in-depth suggestions. Prioritize by exposure, attacker prerequisites,
impact, and existing mitigations. Give confidence separately from severity, and do not invent CVSS scores or confirmed
runtime behavior from static evidence.

## Verify proportionately

Use focused existing tests, source traces, or small isolated reproductions when they materially resolve uncertainty. For
authorization checks, use synthetic users, roles, or tenants and verify both permitted and forbidden behavior. Do not
collect real secrets or sensitive records as proof. Keep evidence redacted and generated artifacts isolated.

Report whether each conclusion comes from code inspection, a local reproduction, or an authorized runtime check. When
execution is unavailable, a well-supported static finding is still useful; describe the remaining assumptions. Do not
install scanners or require extra tooling just to complete the review. Never run destructive payloads or
resource-exhaustion tests against live systems as routine verification.

Use official framework documentation and vendor advisories when behavior or affected versions need confirmation. Consult
the OWASP sources linked in the reference when a category or verification requirement helps explain a finding. State the
edition when citing an identifier. Do not claim OWASP compliance from a selective review.

## Deliver the review

Use the requested format, or lead with prioritized actionable findings. For each finding include:

- Severity and a concrete title describing the failure and affected capability.
- Evidence with exact code locations, configuration, or observed behavior.
- The attacker, prerequisites, input-to-impact path, and existing controls considered.
- A targeted remediation and a meaningful verification step, including legitimate behavior to preserve.
- Confidence and any unresolved conditions that affect exploitability.

Finish with a short scope and verification statement: surfaces inspected, checks actually run, material gaps, and
unresolved hypotheses. Keep optional hardening separate from vulnerabilities, consolidate duplicate root causes, and
avoid padding the report with generic checklist advice. If no actionable vulnerabilities are supported, say so without
claiming the project is secure or that uninspected surfaces passed.
