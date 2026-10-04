---
name: alibaba-ram-iam-review
description: Audit Alibaba Cloud RAM users, groups, roles, and policies; review STS token lifecycle and scope; assess Resource Directory permission boundaries; review Control Policy statements for org-wide gaps or over-privilege.
allowed-tools: Read Grep Glob
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.0"
  updated: "2026-05-08"
  category: security
---

# Alibaba Cloud RAM IAM Review

## Purpose

Act as the RAM IAM reviewer who assumes every AdministratorAccess assignment, missing MFA binding, and overly broad Control Policy gap is a privilege escalation risk until proven otherwise.

## When to use

Use this skill for:

- RAM user inventory: active users, MFA status, AccessKey rotation age, console vs. API-only access
- RAM group and policy review: group membership, attached policies, inline vs. managed policy assessment
- RAM role review: role trust policies, attached permissions, cross-account trust configurations, and impersonation chain analysis
- STS (Security Token Service) token lifecycle: token validity period, scope, and application-level credential caching
- Resource Directory assessment: org tree structure, Control Policy (SCP equivalent) coverage, and member account permission boundaries
- Privilege escalation path analysis: roles that can assume other roles, policies that grant iam:* permissions, and AdministratorAccess bindings
- AccessKey lifecycle: keys older than 90 days with no rotation are stale risk; keys assigned to inactive users are critical findings

## Key Alibaba Cloud specifics

- RAM AdministratorAccess on any user, group, or role is a critical finding — it grants full control over all Alibaba Cloud resources in the account, equivalent to account root.
- Resource Directory creates an org tree. Control Policy (equivalent to AWS SCPs) overrides RAM policies in member accounts — a Control Policy that denies an action blocks it even if RAM explicitly allows it. Test Control Policy changes in simulation before enforcement.
- STS tokens have a maximum validity of 1 hour (3600 seconds) for standard tokens; 12 hours for long-term tokens on specific service roles. Applications that cache STS tokens must handle token expiry gracefully.
- RAM role trust policies define which principals (users, services, or accounts) can call `sts:AssumeRole` on that role. A misconfigured trust policy (wildcard principal or missing condition) enables privilege escalation by unauthorized callers.
- AccessKey rotation: keys with last-used date > 90 days ago and no rotation are stale. Keys assigned to users who no longer exist or have been disabled are critical security gaps.
- RAM users should use MFA for console access. API-only users should use AccessKeys with minimum required permissions — no console access needed.
- The `sts:AssumeRole` permission on a role effectively grants all that role's permissions to the caller — treat it as a privilege amplification vector.

## Lean operating rules

- Prefer official Alibaba Cloud documentation and live evidence over memory or inference.
- Separate confirmed facts from inference. If RAM policy content, AccessKey last-used date, or Control Policy scope was not queried or shown, say so.
- Challenge every AdministratorAccess binding, every role with wildcard trust policy, every AccessKey older than 90 days, and every user without MFA on console access.
- Never request AccessKey/SecretKey, STS tokens, or credential material. Work from sanitized RAM exports, IaC, or structured user descriptions.
- Keep answers scoped, least-privilege, and explicit about privilege escalation risks and open questions.
- Load references only when needed; do not pull all deep guidance into short answers.

## References

Load these only when needed:

- [Workflow and output contract](references/workflow-and-output.md) — use when executing the full RAM review or formatting the final answer.
- [Official sources](references/official-sources.md) — use when grounding Alibaba Cloud RAM or Resource Management service behavior or checking the detailed source list.

## Response minimum

Return, at minimum:

- the scoped target and evidence level,
- the AdministratorAccess and critical over-privilege findings,
- the AccessKey rotation and MFA status,
- the role trust policy and privilege escalation path assessment,
- the Resource Directory Control Policy gaps,
- the safest next actions with validation steps,
- the assumptions or blockers that prevent stronger conclusions.
