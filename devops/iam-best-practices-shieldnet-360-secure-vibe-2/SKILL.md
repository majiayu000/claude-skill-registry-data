---
id: iam-best-practices
version: "2.0.0"
title: "Identity & Access Management Best Practices"
description: "Least-privilege cloud IAM: policy scope, privilege-escalation paths, permissions boundaries, workload identity over static keys, MFA enforced by policy, cross-account trust, and separating deploy from runtime. Use when generating IAM policies, roles, or trust documents, wiring CI/CD service accounts or workload identities, delegating role creation, or designing cross-account access."
category: prevention
severity: critical
applies_to:
  - "when generating IAM policies, roles, or trust documents"
  - "when wiring CI/CD service accounts or workload identities"
  - "when delegating role or policy creation to another team"
  - "when reviewing access-key creation, rotation, or revocation"
  - "when designing cross-account or cross-tenant access"
languages: ["hcl", "yaml", "json", "python", "go", "typescript"]
token_budget:
  minimal: 1300
  compact: 1800
  full: 2200
rules_path: "rules/"
related_skills: ["auth-security", "iac-security", "cicd-security", "secret-detection"]
last_updated: "2026-08-12"
sources:
  - "NIST SP 800-53 Rev. 5 (AC-2, AC-3, AC-6, AC-17, IA-2, IA-5)"
  - "CIS Controls v8 (Controls 5 and 6)"
  - "AWS IAM Best Practices"
  - "Google Cloud IAM recommender"
  - "CNCF Kubernetes RBAC Good Practices"
external_tools:
  - name: prowler
    purpose: "live cloud account IAM/security posture assessment (AWS/Azure/GCP)"
    command: "prowler aws"
---

# Identity & Access Management Best Practices

## Rules (for AI agents)

### ALWAYS
- Grant the minimum permissions the workload's stated job requires: deny by default,
  then add concrete actions against concrete resources. A wildcard action on a
  wildcard resource — in a custom policy, in `AdministratorAccess`, or in `iam:*`
  attached to something that runs continuously — is the same finding wearing three
  different names.
- Read a policy for the **privileges it can reach**, not only the ones it names. A
  principal that can write policy (`iam:PutRolePolicy`, `iam:AttachRolePolicy`,
  `iam:CreatePolicyVersion`) can grant itself anything, and a principal that can pass
  a role into a compute service it may also create (`iam:PassRole` with
  `lambda:CreateFunction`, `ec2:RunInstances`, `glue:CreateJob`) inherits that role's
  privileges. These read as narrow grants and are administrative ones.
  `references/escalation-paths.md` lists the combinations worth failing a review over.
- Bound delegated permissions with a **permissions boundary** or an organization-level
  policy (SCP, GCP org policy, Azure management-group policy) when teams may create
  their own roles. The boundary caps what any role they create can do, which is what
  makes self-service role creation safe rather than a privilege-escalation primitive.
- Prefer **workload identity** — IRSA on EKS, GKE Workload Identity, Azure Managed
  Identity, OIDC federation from CI — over a static key. The goal is that no
  long-lived credential exists to leak. Where one is genuinely unavoidable, give it a
  documented rotation cadence and automatic disablement on inactivity, and treat that
  as a temporary state rather than the steady state.
- Enforce MFA for human principals through a **policy condition**
  (`aws:MultiFactorAuthPresent`), not only a directory setting, so a credential that
  bypasses the directory still cannot act.
- Separate the **deploy** identity from the **runtime** identity. The pipeline gets
  permission to create and change infrastructure; the running service gets permission
  to do its job and nothing that mutates IAM. `cicd-security` owns hardening the
  pipeline that holds the deploy role.
- Scope cross-account trust to the actual counterparty. Inside your own organization
  that means a specific principal ARN or `aws:PrincipalOrgID`; for a **third party**
  acting on your behalf it additionally means an `ExternalId` — a per-consumer value
  the third party supplies, which defeats the confused-deputy case where another of
  their customers can name your account. Treat `ExternalId` as an identifier, not a
  secret: it is not one, and relying on its confidentiality is a false assurance.
- Keep sessions short and make the length a deliberate choice. Human and CI roles
  should use the shortest session the workflow tolerates. A longer window on a
  break-glass role is a defensible operational trade — an incident should not expire
  mid-response — but it has to be stated as a decision, paired with alerting, and not
  copied onto ordinary roles.
- For Kubernetes RBAC, scope `Role` and `RoleBinding` to one namespace and reserve
  `ClusterRole` for genuinely cluster-wide objects. Review every `cluster-admin`
  binding at pull-request time, and remember that permission to create workloads in a
  namespace is permission to use every service account in it.
- Log IAM-mutating calls to a tamper-evident sink and alert on them: policy changes,
  `iam:PassRole`, access-key creation, and role assumption from an unexpected
  principal. `logging-security` owns the shape of the record.
- Require out-of-band approval for break-glass use (root, organization owner,
  `cluster-admin`) and alert on every invocation, not on a sample.

### NEVER
- Use the root or organization-owner account for day-to-day work. It gets a hardware
  MFA device, offline storage, and only the tasks that genuinely require it.
- Embed a long-lived access key in source, a container image, a machine image, or a
  CI environment variable where a workload identity or OIDC federation is available.
- Grant `iam:PassRole` with `Resource: "*"`. Pin the exact role ARNs the caller may
  pass, and read that grant together with what the caller can launch.
- Share one principal between multiple humans or multiple services. One identity per
  actor is what makes the audit log mean anything.
- Disable MFA for a principal to resolve a login problem. Rotate the device; the
  requirement stays.
- Persist an OIDC or SAML assertion beyond its stated lifetime. Refresh by
  re-assertion rather than storing the original token.

### KNOWN FALSE POSITIVES
- `Resource: "*"` on APIs that accept no resource ARN — `sts:GetCallerIdentity`,
  `ec2:DescribeRegions` and their equivalents. The wildcard is the only expressible
  value, so the finding is the *action* being unnecessary, not the resource scope.
- Provider-managed service-linked roles carry broader permissions than a role you
  would write. That breadth is the provider's contract and is not yours to narrow.
- A bootstrap operator in a fresh account often needs elevated permissions before the
  guardrails it installs exist. Gate it by tag or organization policy and revoke on
  completion — a bootstrap role that survives bootstrap is a finding again.
- Local development emulators accept any credential. That is a property of the
  emulator, not a grant in your account.
- Enumerating explicit resource ARNs is correct for a bounded set. Attribute-based
  scoping (tags, organization paths) is the answer when the set grows, not a
  security upgrade over naming resources you can name.

## Context (for humans)

Cloud IAM has one property that makes reviewing it different from reviewing other
access control: **the effective permission set is not the stated one**. A role that
can attach a policy can attach `AdministratorAccess` to itself. A role that can pass
another role into a service it can also create runs as that role. Neither policy
contains a wildcard, and both are administrative. Reading a policy for what it says,
rather than for what it can reach, is the failure that produces most
over-permissioned estates.

The second property is that the scalable answer is rarely a better-written policy.
Permissions boundaries and organization policies are what let a platform team hand
role creation to product teams without handing over the account, and attribute-based
scoping is what keeps a policy correct as the resource set grows. Enumerating ARNs
more carefully does not scale past the point where someone starts pasting `*` to make
the deploy pass.

Capital One (2019) and Uber (2022) are the canonical illustrations of the two halves:
an over-permissioned role reached through a server-side request, and a static
credential found in a script after an MFA-fatigue login.

## References

- `references/verifying-findings.md` — confirm or refute a finding, then lock it
- `references/escalation-paths.md` — the permission combinations that are
  administrative without containing a wildcard, and how boundaries cap them
- `rules/iam_policy_invariants.json`
- `rules/key_rotation_policy.json`
- [AWS IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html).
- [Google Cloud IAM recommender](https://cloud.google.com/iam/docs/recommender-overview).
- [CNCF Kubernetes RBAC good practices](https://kubernetes.io/docs/concepts/security/rbac-good-practices/).
- [NIST SP 800-53 Rev. 5](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final).
