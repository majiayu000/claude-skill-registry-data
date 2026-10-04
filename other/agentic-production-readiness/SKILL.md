---
name: agentic-production-readiness
description: >
  Prepare an AI agent system for production operation. Cover SHIELD controls,
  sandbox/canary/production rollout, OpenTelemetry observability with GenAI
  semantic conventions, Agent Card drafting, governance, and post-deploy
  monitoring. Use for production readiness checks, go-live checklists, agent
  monitoring, agent cards, canary rollout, or deploying agent systems. Do NOT
  use for standard web-app deployment, local setup, feature work, or non-agent
  infrastructure tasks.
---

# Agentic Production Readiness

Use this skill when an agentic system is close to deployment or operational
handoff. Verify current protocol details instead of hardcoding unstable specs.

## Workflow

1. Identify deployment target, owner, data sensitivity, tool permissions, and
   rollback path.
2. Apply SHIELD:
   - Separation of duties.
   - Human approval for high-impact actions.
   - Input/output validation.
   - Enforced security models.
   - Least agency and least privilege.
   - Defensive controls such as sandboxing and SCA.
3. Plan staged rollout: sandbox, canary, then production. Define rollback
   triggers before release.
4. Configure observability: logs, traces, metrics, token/cost tracking, model
   versions, tool calls, latency, and policy versions.
5. Draft an Agent Card if external discovery or agent-to-agent use is required.
   Verify the current A2A location and schema before publishing.
6. Generate `DEPLOY_CHECKLIST.md` from
   `assets/templates/DEPLOY_CHECKLIST.md`.

## Governance Checks

- Named accountable owner.
- Credential source and rotation policy.
- Memory retention and review policy.
- Eval thresholds and release gates.
- Incident response and audit trail.
- Regulatory mapping only when the domain requires it.

## References

Read `../agentic-engineering-sdlc/references/day5_prototype_to_production.md`
for Agent Ops, durable execution, and deployment patterns.

## Done Criteria

- Rollout and rollback are explicit.
- Observability covers behavior, tools, cost, and safety.
- Agent Card details are marked draft until checked against the current spec.
- Governance and on-call ownership are assigned.
