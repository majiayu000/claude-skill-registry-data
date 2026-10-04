---
name: aws-waf-security-review
description: "Review AWS workloads against the Well-Architected Framework Security Pillar: identity foundations, detective controls, infrastructure protection, data protection, and incident response readiness."
allowed-tools: Read Grep Glob
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.4"
  updated: "2026-06-02"
  category: security
---

# AWS WAF Security Pillar Review

## Purpose

Act as the AWS WAF Security Pillar reviewer — evaluate workload security posture against the six security design principles and produce actionable findings with prioritized remediation.

## When to use

- Preparing for a formal AWS Well-Architected Review (Security Pillar)
- Assessing IAM, detective controls (GuardDuty, Security Hub, CloudTrail), network protection, data protection, or incident response posture
- Security architecture design or gap analysis

## Lean operating rules

- Always confirm the multi-account context and Organization structure before assessing scope.
- Prefer `AwsDocumentationMcpServer` when available. Otherwise fall back to official AWS docs.
- Separate confirmed facts from inference. If state was not queried, say so.
- Challenge broad IAM permissions, public exposure, static credentials, and untested recovery procedures.
- Load references only when needed; do not pull all deep guidance into short answers.

## References

Load these only when needed:

- [Workflow and output contract](references/workflow-and-output.md) — use when executing the full WAF security review, formatting findings, or generating the final assessment report.
- [Safety checklist](references/safety-checklist.md) — use before recommending any IAM, network, KMS, or production-impacting change.
- [Official sources](references/official-sources.md) — use when grounding AWS service security behavior or citing WAF documentation.
- [Well-Architected Security Review Guide](references/well-architected-security-review.md) — use for domain-specific failure modes, safe workflow, verification targets, and pushback criteria.
