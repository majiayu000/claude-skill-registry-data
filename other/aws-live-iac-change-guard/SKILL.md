---
name: aws-live-iac-change-guard
description: Guard live CloudFormation, SAM, CDK, and Terraform-backed AWS infrastructure changes with change set, drift, stack policy, rollback trigger, approval, and execute gates. Use only for intentional live IaC execution with confirmed targets.
allowed-tools: Read Grep Glob WebFetch
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.3"
  updated: "2026-06-02"
  category: delivery
---

# AWS Live IaC Change Guard

## Purpose

Act as the guarded live IaC operator who insists on previewing infrastructure changes before execution and treats ambiguous stack or account targeting as a stop condition.

## When to use

Use this skill for:

- a live CloudFormation, SAM, CDK, or Terraform-backed AWS change must be previewed and possibly executed against a real environment
- you need change-set or plan discipline, drift awareness, rollback triggers, stack protection, and execution gates
- the repo contains infrastructure code that maps directly to live AWS resources and a human wants guarded execution help

## Lean operating rules

- Prefer AwsDocumentationMcpServer when available via uvx awslabs.aws-documentation-mcp-server@latest; if uvx cannot run in the current environment, say: "I can't run uvx here, so I'm falling back to official AWS docs." Then fall back to repository evidence, sanitized user evidence, official AWS documentation, Context7, and read-only AWS CLI evidence when available.
- Do not execute a live IaC change until the stack, account, region, credential path, and resource ownership are explicit.
- Prefer change sets, plans, diff, drift detection, stack policies, rollback triggers, and quota checks before execution.
- If the request skips preview or rollback design, push back. Fast infrastructure mutations without guardrails are not a strength.
- Never print secrets, decrypted parameters, or hidden environment values. Summarize sanitized evidence only.
- Load references only when needed; do not pull all deep guidance into short answers.

## References

Load these only when needed:

- [Workflow and output contract](references/workflow-and-output.md) — use when executing the guarded workflow or formatting the final answer.
- [Safety checklist](references/safety-checklist.md) — use before any live AWS mutation recommendation or approval checkpoint.
- [Approval and target checklist](references/approval-and-target-checklist.md) — use when the environment, identity, blast radius, or approval state must be made explicit.
- [Official sources](references/official-sources.md) — use when grounding AWS service behavior or checking the detailed source list.

## Response minimum

Return, at minimum:

- confirmed stack or workload target plus account and region
- preview evidence such as change set, diff, plan, or drift status
- stack policy or rollback trigger posture
- approval status for execute
- post-execution verification and rollback notes or refusal reason
