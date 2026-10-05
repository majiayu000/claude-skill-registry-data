---
name: cloud-iam-design
description: "Least privilege is easy to state and hard to hold: grant each identity only the"
---

# Cloud IAM Design (Verbose)

## Core Patterns

### Least Privilege as a Blast-Radius Argument

Least privilege is easy to state and hard to hold: grant each identity only the
permissions it needs to do its job, and nothing more. The reason it matters is not
tidiness — it is **blast radius**. Every credential eventually leaks or is misused;
the only question the design controls is how much damage the holder of a leaked
credential can do. A role scoped to read one bucket is a minor incident when it
leaks. A role with `*` is a company-ending one.

So the right mental model is adversarial. For each identity, ask: *if these
credentials were posted publicly right now, what could an attacker read, change,
delete, or spend?* Design so that answer is small and bounded, for every identity,
because you will not get to choose which one leaks.

Least privilege is reached by subtraction from evidence, not addition from
imagination. Start denied, then derive the actual permissions a workload uses from
access logs and access-analyzer tooling, grant exactly those, and periodically
prune permissions that have gone unused. A policy written from a developer's guess
about what "should" be needed is almost always far too broad.

### Roles vs Long-Lived Keys

Static, long-lived access keys are the single most-leaked class of cloud
credential. They are committed to git, printed into CI logs, baked into container
images, left on laptops, and shared in chat — and because they do not expire, a key
leaked years ago is still valid today unless someone noticed and rotated it. The
strongest single improvement most organizations can make to IAM is to stop issuing
them.

The replacement is short-lived, automatically-issued credentials tied to an
identity:

- **Workloads on cloud compute** get a role attached to the instance, container,
  or function, and the platform hands the code temporary credentials through the
  metadata/identity endpoint. Nothing is stored; nothing is rotated by you.
- **Human users** authenticate through central SSO and *assume* short-lived roles.
  There are no per-user static IAM users to manage, and access is granted by group
  membership that can be revoked in one place.
- **CI/CD pipelines and external/other-cloud workloads** use **workload identity
  federation**: you establish an OIDC (or SAML) trust between your identity
  provider and the cloud, and the pipeline presents its own signed token, which the
  cloud exchanges for short-lived credentials scoped to a specific role. This
  removes the last common reason to store a long-lived key — the CI deploy
  credential — entirely.

Every static key eliminated is a secret that can no longer leak, expire-in-place,
or require rotation tooling.

### Wildcards: The Common Breach

The most common serious IAM finding is a wildcard in an allow policy —
`Action: "*"`, `Resource: "*"`, or both. Wildcards are attractive because they make
a permission error go away immediately: something didn't work, so `*` was added "to
unblock," and it was never narrowed. Two properties make them dangerous:

1. They grant **future** permissions. A `*` action grants every capability the
   platform adds later, forever, with no review.
2. They defeat the blast-radius analysis entirely. An identity with `Resource: "*"`
   has an unbounded blast radius by construction.

Name actions explicitly, and scope every allow to specific resource ARNs, project
paths, or resource tags. The one legitimate use of a broad wildcard is in a
**deny** — denies should be as broad as possible so that no future permission slips
past them. The asymmetry is the point: broad denies are a safety net; broad allows
are the hole.

```json
// ❌ Unbounded — grants every S3 action on every bucket, now and forever
{ "Effect": "Allow", "Action": "s3:*", "Resource": "*" }

// ✅ Enumerated actions, scoped to one prefix in one bucket
{
  "Effect": "Allow",
  "Action": ["s3:GetObject", "s3:PutObject"],
  "Resource": "arn:aws:s3:::orders-prod/incoming/*"
}
```

### Permission Boundaries and Organization Guardrails

Least-privilege policies describe what an identity *should* be able to do. They do
not, by themselves, stop that identity (or someone with access to it) from
attaching a broader policy later. Two mechanisms cap the *maximum* authority
regardless of what policies are attached:

- **Permission boundaries** set a ceiling on the effective permissions of an
  individual role or user. Even if a broad policy is attached, effective
  permissions are the intersection with the boundary. This is what lets you safely
  delegate policy creation to a team: they can create roles, but never a role more
  powerful than the boundary allows.
- **Organization-level guardrails** (service control policies / organization
  policies) apply across whole accounts or projects. They express invariants no one
  in that account may violate — do not disable audit logging, do not create
  publicly-open storage, do not operate outside approved regions, do not weaken
  the org's own guardrails.

Guardrails invert the usual trust model: instead of trusting that every individual
grant is correct, you enforce that *nothing* can cross a hard line, and review the
lines rather than every grant.

### Structural Isolation by Account and Environment

Blast radius is partly a function of policy and partly a function of structure. The
strongest boundary in most clouds is the account/project boundary. Keeping
production and non-production in **separate accounts** means a compromised
development identity — which is where most experimentation, weaker controls, and
looser access live — simply cannot reach production resources, no matter what its
policy says.

Within that, prefer a distinct role per service and per environment over a single
shared "application" identity that many services assume. Shared identities merge
the blast radius of everything that uses them: one leaked shared role exposes every
service's data. Per-service roles keep an incident contained to the one service
whose credential leaked.

### Human Access and Break-Glass

Standing human administrator access is the credential attackers most want, because
it is powerful and often less monitored than service roles. Day-to-day human access
should be least-privilege and short-lived through SSO, the same as everything else.
Genuine emergency ("break-glass") admin access should exist — outages happen — but
it should be rare, individually attributable, MFA-gated, time-bounded, and emit a
loud, un-suppressable alert every time it is used, so that legitimate emergencies
are reviewed and illegitimate use is caught immediately.

## Common Anti-Patterns

❌ **`Action: "*"` / `Resource: "*"` in an allow.** Unbounded blast radius, grants
all future permissions.
✅ Enumerate actions; scope resources by ARN/path/tag. Reserve wildcards for denies.

❌ **Long-lived access keys for workloads and CI.** They leak and never expire.
✅ Instance/pod roles for workloads; OIDC workload identity federation for CI.

❌ **Static IAM users for humans.** Sprawls, hard to offboard, often no MFA.
✅ Federate through SSO; assume short-lived roles by group membership.

❌ **One shared identity assumed by many services.** Merges everyone's blast
radius.
✅ A distinct, minimally-scoped role per service and environment.

❌ **Prod and non-prod in one account.** A dev compromise reaches prod.
✅ Separate accounts/projects per environment.

❌ **No boundary or org guardrail.** Any role can be widened to admin later.
✅ Permission boundaries on delegated roles; SCPs/org policies for hard invariants.

❌ **Grants written from a guess and never reviewed.**
✅ Derive from usage data; prune unused permissions on a schedule.

❌ **Standing human admin with no MFA or expiry.**
✅ Least-privilege daily access; rare, MFA-gated, alerting break-glass for
emergencies.

## Cloud IAM Checklist

- [ ] No wildcard actions or resources in any allow policy
- [ ] Policies derived from observed usage, not guessed
- [ ] Unused permissions reviewed and pruned on a schedule
- [ ] Workloads use attached roles, not stored keys
- [ ] CI/external workloads use OIDC workload identity federation
- [ ] Humans access via SSO assuming short-lived roles; no static IAM users
- [ ] Distinct, minimally-scoped role per service and environment
- [ ] Production isolated in its own account/project
- [ ] Permission boundaries cap delegated role authority
- [ ] Org guardrails (SCPs) enforce logging, region, and public-access invariants
- [ ] Break-glass access is rare, MFA-gated, time-bound, and alerted
- [ ] All IAM changes and role assumptions logged and monitored

## See Also
- `secret-management` — safe storage and rotation of any credential that must exist
- `security-architecture-review` — assessing blast radius and trust boundaries
  across the whole system
