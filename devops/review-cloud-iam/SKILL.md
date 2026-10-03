---
name: review-cloud-iam
description: Review AWS, Azure, and Google Cloud identity and access management for effective privilege, escalation paths, external trust, workload identity, long-lived credentials, guardrails, and auditability. Use when asked to assess IAM policies, role assignments, service accounts, federated access, organization or tenant hierarchy, access exports, or an explicitly authorized cloud environment. Use provider evidence rather than generic least-privilege claims.
---

# Review Cloud IAM

Produce a provider-aware, evidence-backed view of who can do what, on which resource, under which conditions, and how that access can change.

Read [methodology](references/methodology.md) before normalizing provider data or claiming an escalation path.

## Establish the operating contract

1. Record the provider, organization or tenant, accounts, subscriptions or projects, environments, resource boundary, identities, evidence sources, observation window, exclusions, owner, and decision to support.
2. Prefer read-only exports, infrastructure-as-code, policy files, access-analysis results, and audit logs. Require explicit authorization before querying a live tenant.
3. Require separate explicit approval before changing policies, revoking sessions, rotating credentials, disabling identities, or assuming roles. Treat review authority as read-only.
4. If scope or live authority is unclear, analyze only the supplied artifacts and state which effective-access conclusions remain unavailable.

## Execute the review

1. Inventory human, workload, federated, guest, emergency, root or super-admin, service-linked, and automation identities. Record ownership and lifecycle state without exposing credentials.
2. Normalize organization hierarchy, groups, roles, policies, bindings, resource policies, trust policies, conditions, explicit denies, permission boundaries, and organization guardrails into principal-to-resource paths.
3. Calculate effective access with inheritance, deny precedence, conditions, session policy, resource policy, and cross-account or cross-tenant trust. Do not judge a policy statement in isolation.
4. Identify privilege-escalation and persistence paths through role assumption, pass-role or impersonation, policy or role-assignment mutation, group membership, credential creation, federation changes, deployment identities, and control-plane ownership.
5. Review privileged human access for federation, phishing-resistant MFA where supported, separate admin identities, just-in-time elevation, break-glass controls, recovery, and access review.
6. Review workload access for managed or workload identity, short-lived credentials, audience and subject restrictions, service-account impersonation, key inventory, rotation, and environment separation.
7. Review external principals, wildcard trust, tenant or organization boundaries, confused-deputy controls, resource sharing, and public or anonymous grants.
8. Compare granted access with observed use only when the audit window and log coverage are sufficient. Treat unused-access data as a removal candidate, not automatic proof that access is unnecessary.
9. Review who can alter IAM, disable logging, access audit evidence, modify guardrails, or create new credentials. Recommend reversible remediation sequencing and validation.

## Apply evidence rules

- Support each finding with the exact provider object, stable ID, scope, policy or binding excerpt, effective path, relevant conditions and denies, collection time, and source command or export. Redact tenant-sensitive values where appropriate.
- Label a path `confirmed` only when every edge is supported and its conditions are satisfiable. Label incomplete but credible paths `probable` and name the missing edge. Keep naming heuristics and tool-only alerts in `leads`.
- Distinguish `granted`, `effective`, `observed`, and `required` access. Never use these terms interchangeably.
- Demonstrate escalation as a complete sequence from current principal to new capability and target impact. Do not rate wildcard syntax, an admin-sounding role name, or a stale key alone as critical.
- State the audit-log retention, start and end time, services covered, and known blind spots before using last-used evidence.
- Never reproduce secrets, private keys, access tokens, recovery codes, or full sensitive policy conditions in the report.

## Enforce safety constraints

- Use read-only provider APIs and offline analysis by default. Do not assume a role or impersonate a principal merely to prove that a trust path works.
- Never modify IAM, attach policies, create keys, grant consent, trigger federation, revoke sessions, disable logging, or test a discovered credential without explicit change approval.
- Do not enumerate organizations, tenants, accounts, or projects outside the named boundary.
- Never upload tenant exports or policies to third-party analysis services without explicit approval.
- If exposed credentials appear, stop displaying them, preserve only a redacted reference, and invoke the owner's approved secret-response process. Do not test the credential.
- Present proposed removals with owner validation, dependency impact, rollback, and observation steps. Do not recommend blind deletion.

## Return the output contract

Return these sections in order:

1. `Decision summary` — material exposure, highest-value remediation, and confidence.
2. `Scope and evidence` — provider hierarchy, artifacts, live queries, observation window, and exclusions.
3. `Identity and trust map` — principal classes, privilege tiers, external trust, and control-plane owners.
4. `Effective-access paths` — source principal, intermediate edges, conditions, target capability, and evidence IDs.
5. `Findings` — ID, confidence, severity, affected scope, prerequisites, evidence, impact, provider-specific remediation, rollback, and verification.
6. `Access-reduction candidates` — unused or broad grants requiring owner validation, kept separate from vulnerabilities.
7. `Coverage and limitations` — services, policy types, log sources, identities, blind spots, and untested paths.
8. `Remediation sequence` — containment, short-term reduction, durable redesign, and validation order.

## Pass the quality gate

Before finalizing, verify that:

- Every escalation path is complete, provider-valid, and evidence-linked.
- Effective access accounts for hierarchy, inheritance, conditions, explicit denies, resource policies, and guardrails.
- Human and workload identities receive separate analysis.
- External trust and IAM control-plane mutation receive explicit coverage.
- Least-privilege recommendations name the required replacement access and avoid availability-breaking deletion.
- No secret appears in output and no state-changing action was performed without explicit approval.
