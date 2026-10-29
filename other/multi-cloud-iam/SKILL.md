---
name: multi-cloud-iam
description: Use when reviewing identity across multiple cloud
  providers on an authorized engagement. Covers federated identity
  design, cross cloud role assumptions, consistent least privilege,
  and finding the weakest provider. Also use when one IdP fronts AWS,
  Azure, and GCP.
version: 1.0.0
domain: cloud
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [iam-privesc, cloud-security-basics, aws-enumeration]
tools:
  - name: Python
    version: "3.12"
---

Multi cloud identity usually means one IdP federating into three
different IAM models, and the seams are where privilege hides: a role
that is tight in AWS but admin in Azure. This skill covers authorized
review: mapping the identity fabric, testing cross cloud paths, and
finding the weakest provider. Test only accounts you are authorized
to assess.

## Quick Workflow

1. Map the identity fabric: IdP, federation trusts, and the roles in
   each cloud.
2. Inventory human and workload identities in each provider.
3. Test the federation: what does each IdP group get in each cloud.
4. Look for the weakest provider: where the same identity has the
   most privilege.
5. Trace cross cloud paths: compromise in one cloud reaching
   another.
6. Check workload identity: CI roles, pod identities, and function
   roles per cloud.
7. Review guest and external access in each provider.
8. Report the effective privilege per identity per cloud.

## 1. Federation mapping

```bash
# AWS: which IdP roles exist and who can assume them
aws iam list-roles --query 'Roles[?contains(RoleName, `saml`) || contains(RoleName, `oidc`)].RoleName' --output text
# Azure: enterprise apps and role assignments from the IdP
# GCP: workforce identity federation pools
echo "for each: IdP group -> cloud role -> permissions"
```

```python
#!/usr/bin/env python3
"""Effective privilege matrix (fill from enumeration)."""
matrix = {
    "dev-group": {"aws": "PowerUser", "azure": "Contributor", "gcp": "Editor"},
    "ci-role": {"aws": "deployer", "azure": "Reader", "gcp": "owner?"},
}
for ident, clouds in matrix.items():
    worst = max(clouds.items(), key=lambda kv: len(kv[1]))
    print(f"{ident}: widest in {worst[0]} ({worst[1]})")
print("the weakest provider sets the real privilege level")
```

## 2. Cross cloud path testing (authorized)

```bash
# Example path: CI role in AWS can read a secret that holds a GCP key
# 1. enumerate what the test role can read in cloud A
# 2. check whether any readable secret is a credential for cloud B
# 3. verify the credential works (authorized test only) and note scope
echo "document each hop; the finding is the unintended bridge"
```

## Edge cases

- Each cloud is managed by a different team. The review needs all
  three; a partial review misses the seams.
- The IdP groups are nested and messy. Resolve the nesting before
  rating privilege, or the matrix lies.
- Workload identities differ per cloud (IRSA vs workload identity
  federation vs managed identity). Learn each model.

## Escalation

- Effective admin found via the weak provider: demonstrate the
  path, then recommend normalizing to least privilege everywhere.
- Federation misconfiguration allows unintended groups in: fix the
  trust policy first, it is the front door.

## Detection and defender view

Defenders monitor multi cloud identity with centralized sign in
logs, alerts on cross cloud role assumptions, and regular access
reviews per provider. They defend with one IdP, short lived
credentials, and policy as code that enforces the same baseline in
each cloud. The durable goal is no standing privilege anywhere,
with just in time elevation that works the same in all clouds.

## Key references

- CWE-862 (Missing Authorization): cross cloud gaps.
- NIST SP 800-207: identity as the perimeter.
- Provider IAM federation documentation.
