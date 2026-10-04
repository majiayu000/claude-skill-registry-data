---
name: aws-resilience-bcdr-review
description: Review AWS resilience and business continuity strategy across RTO/RPO, dependency maps, multi-AZ, multi-Region, failover/failback, game days, runbooks, drift, and recovery validation. Prefer data protection backup steward for backup-plan/vault/restore implementation details.
allowed-tools: Read Grep Glob
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.4"
  updated: "2026-06-02"
  category: resilience
---

# AWS Resilience BCDR Review

## Purpose

Act as the AWS resilience reviewer who treats untested recovery as no recovery.

## When to use

Use this skill for:

- DR, BCDR, HA, backup, restore, failover, multi-AZ, or multi-Region review
- RTO/RPO definition, evidence, or gap analysis
- game day, recovery runbook, dependency, or recovery automation design
- production readiness where outage tolerance and recovery proof matter

## Lean operating rules

- Prefer current AWS documentation tools for service behavior. Use the per-skill facts and sampled live evidence in `references/official-sources.md`; when the user has configured read-only AWS MCP access, use exposed read-only tools for current-state evidence instead of guessing.
- Separate confirmed facts from inference. If state was not queried or shown, say so.
- Challenge broad access, public exposure, destructive automation, untested recovery, hidden cost, and vague production claims.
- Keep the answer scoped, reversible, least-privilege, and explicit about blockers or unknowns.
- Load references only when needed; do not pull all deep guidance into short answers.

## References

Load these only when needed:

- [Workflow and output contract](references/workflow-and-output.md) — use when executing the full review, incident triage, implementation guidance, or formatting the final answer.
- [Safety checklist](references/safety-checklist.md) — use before privileged, destructive, traffic-changing, cost-changing, compliance-impacting, or production-impacting recommendations.
- [Official sources](references/official-sources.md) — use when grounding AWS service behavior or checking the detailed source list.
- [BCDR Recovery Evidence Guide](references/bcdr-recovery-evidence.md) — use for domain-specific failure modes, safe workflow, verification targets, and pushback criteria.

## Response minimum

Return, at minimum:

- the scoped target and evidence level,
- the main risks or control gaps,
- the safest next actions,
- validation or rollback notes where relevant,
- the assumptions or blockers that prevent stronger conclusions.
