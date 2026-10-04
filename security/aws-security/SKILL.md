---
name: aws-security
description: Use when securing AWS.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [cloud, aws, aws-iam-best-practices]
---

# Aws Security

"Use when securing AWS."

## Trigger

Activate this skill when the user mentions:
- cloud,  aws,  aws-iam-best-practices workflows or issues
- Building, fixing, or optimizing aws security
- Questions about cloud best practices

## Core Concepts

- Threat modeling and risk assessment
- Attack surface analysis
- Defense in depth
- Zero-trust architecture
- Compliance and audit requirements

## Step-by-Step Workflow

1. **Scope** — Define assets, threats, attack surface
   - Expected: Documented scope with trust boundaries
2. **Assess** — Identify vulnerabilities, evaluate risk
   - Expected: Prioritized findings with CVSS scores
3. **Remediate** — Apply secure-by-design fixes
   - Expected: Vulnerabilities closed
4. **Verify** — Re-test and validate remediation
   - Expected: Independent verification complete
5. **Document** — Record findings and lessons learned
   - Expected: Audit-ready report

## Tools & Technologies

- Vulnerability scanners
- SAST/DAST tools
- SIEM platforms
- Pen-testing frameworks

## Best Practices

- Document decisions and rationale (ADRs, design docs, runbooks)
- Version everything - code, configs, data, and documentation
- Test incrementally; never claim passing without verification
- Respect domain-specific regulations and ethical standards
- Measure outcomes with meaningful metrics

## Common Pitfalls

- **Scope creep** → Unclear boundaries → Define scope explicitly
- **Tool reliance without analysis** → False positives → Manual validation required

## Tags

`cloud, aws, aws-iam-best-practices`

---

*LoopyLuci/Skills - 2026-09-24*
