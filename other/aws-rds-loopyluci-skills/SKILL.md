---
name: aws-rds
description: Use when implementing aws rds.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [aws, rds]
---

# Aws Rds

"Use when implementing aws rds."

## Trigger

Activate this skill when the user mentions:
- "aws",  "rds" workflows or issues
- Building, fixing, or optimizing aws rds
- Questions about "aws" best practices

## Core Concepts

- Infrastructure as Code (IaC)
- Well-Architected Framework
- Identity and access management
- Networking and security groups
- Cost optimization and tagging

## Step-by-Step Workflow

1. **Design** — Architecture review against WAF pillars
   - Expected: Approved architecture diagram
2. **Implement** — IaC templates with least-privilege IAM
   - Expected: Reviewable version-controlled infra
3. **Validate** — Security scan, cost estimate, plan review
   - Expected: Clean plan within budget
4. **Deploy** — Apply with change management
   - Expected: Deployed infrastructure matches plan
5. **Monitor** — Alarms, dashboards, cost alerts
   - Expected: Full observability and cost allocation

## Tools & Technologies

- Terraform/Pulumi
- Cloud-native IaC
- Security scanning
- Cost management

## Best Practices

- Document decisions and rationale (ADRs, design docs, runbooks)
- Version everything - code, configs, data, and documentation
- Test incrementally; never claim passing without verification
- Respect domain-specific regulations and ethical standards
- Measure outcomes with meaningful metrics

## Common Pitfalls

- **Manual console changes** → Configuration drift → All changes through IaC
- **Over-privileged IAM** → Blast radius risk → Least privilege by default

## Tags

`"aws", "rds"`

---

*LoopyLuci/Skills - 2026-09-24*
