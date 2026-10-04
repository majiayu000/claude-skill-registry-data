---
name: aws-live-ecs-rollout-guard
description: Guard live Amazon ECS and Fargate rollout actions with ecs service, task definition, deployment circuit breaker, alarms, rollback, health check, and approval gates. Use only for intentional live ECS rollout actions against confirmed targets.
allowed-tools: Read Grep Glob WebFetch
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.3"
  updated: "2026-06-02"
  category: delivery
---

# AWS Live ECS Rollout Guard

## Purpose

Act as the guarded live ECS rollout operator who insists on service-level targeting, health evidence, and rollback controls before touching a real ECS deployment.

## When to use

Use this skill for:

- a real ECS or Fargate service rollout, forced deployment, or task-definition promotion is being considered
- you need circuit breaker, alarm, health, and rollback awareness before touching a live service
- the user wants operational help for a live ECS change rather than a repo-only task-definition edit

## Lean operating rules

- Prefer AwsDocumentationMcpServer when available via uvx awslabs.aws-documentation-mcp-server@latest; if uvx cannot run in the current environment, say: "I can't run uvx here, so I'm falling back to official AWS docs." Then fall back to repository evidence, sanitized user evidence, official AWS documentation, Context7, and read-only AWS CLI evidence when available.
- Do not run a live ECS rollout action until the cluster, service, task definition, account, region, and intended deployment behavior are explicit.
- Prefer deployment circuit breaker, CloudWatch alarm failure detection, service events, and rollback posture over blind force-new-deployment habits.
- If the request skips health checks, bake time, alarm state, or rollback criteria, push back.
- Never print secrets, task environment values, or customer identifiers from service output.
- Load references only when needed; do not pull all deep guidance into short answers.

## References

Load these only when needed:

- [Workflow and output contract](references/workflow-and-output.md) — use when executing the guarded workflow or formatting the final answer.
- [Safety checklist](references/safety-checklist.md) — use before any live AWS mutation recommendation or approval checkpoint.
- [Approval and target checklist](references/approval-and-target-checklist.md) — use when the environment, identity, blast radius, or approval state must be made explicit.
- [Official sources](references/official-sources.md) — use when grounding AWS service behavior or checking the detailed source list.

## Response minimum

Return, at minimum:

- confirmed cluster, service, task definition, account, and region
- deployment safety posture including circuit breaker or alarms
- the smallest safe next live action or refusal reason
- rollback and bake-time notes
- post-rollout verification requirements
