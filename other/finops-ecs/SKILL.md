---
name: finops-ecs
description: >
  FinOps ECS Analysis Skill. Detects cost waste in ECS/Fargate services from
  CPU/memory overprovisioning, missing autoscaling, and always-on workloads
  using Terraform, CloudWatch metrics, and AWS cost reports.
user_invocable: false
---

# FinOps ECS Analysis Skill

## Scope

Reduce Fargate and EC2-launch-type ECS spend while preserving deployment
surge capacity, sidecar headroom, latency SLAs, and batch burst requirements.

## Required Evidence

| File | Used For | If Missing |
|------|----------|------------|
| `main.tf` | `aws_ecs_service`, `aws_ecs_task_definition`, launch type, desired count, cpu/memory, autoscaling | Cannot analyze; ask for path |
| `metrics.json` | CPUUtilization, MemoryUtilization, p95/p99, RunningTaskCount, errors, throttles | Mark metrics unavailable |
| `cost_report.json` | Monthly Fargate/ECS cost per service | Mark cost unavailable |

Missing facts: write `Not available in the provided data; verify in the real environment.`

## Detection Rules

| Rule | Condition | Severity | Action |
|------|-----------|----------|--------|
| E1 | Fargate: CPU avg <20% AND p95 <50% AND no error/throttle spike | HIGH | REVIEW_RIGHTSIZE_CPU_MEMORY |
| E2 | EC2 launch type: CPU avg <15% AND no capacity provider strategy | MEDIUM | REVIEW_MIGRATE_TO_FARGATE_OR_RIGHTSIZE |
| E3 | Service with desired_count > 1 and no autoscaling target or policy | MEDIUM | ADD_TARGET_TRACKING_AUTOSCALING |
| E4 | Scheduled scaling absent for services with predictable traffic patterns | LOW | ADD_SCHEDULED_SCALING |

## Safety Guardrails

- For E1, always verify valid Fargate CPU/memory combinations (256/512, 512/1024,
  1024/2048, 2048/4096, 4096/8192, etc.) before proposing a target shape.
- Do not downsize when sidecar containers share the task CPU/memory budget.
  Check `container_definitions` for sidecar count and their reservations.
- Reject E1 when deployment surge (rolling update) would need the headroom
  (check `deployment_maximum_percent` > 100).
- Treat p99 latency SLA evidence as blocking for E1 when it is within 20% of SLA.
- E2 and E3 may co-occur on the same service; report both.

## Modeled Savings And Pricing Source

Do not set savings to `$0` only because `cost_report.json` is missing. Use this
pricing waterfall and include `pricing_source` on every finding:

1. Prefer ECS/Fargate line items from `cost_report.json` when they clearly map
   to the service and recommendation. Set `pricing_source` to `cost_report`.
2. If AWS public pricing has been supplied, use
   `evidence_bundle.pricing.pricing_model` for Fargate vCPU-hour and GB-hour
   unit prices. Set `pricing_source` to `aws_public_pricing_model` and cap
   confidence at `MEDIUM` unless cost allocation also confirms the resource.
3. If public pricing is unavailable but the rule cost block has matching
   Fargate unit prices, use them as a modeled estimate with `pricing_source`
   set to `static_fallback_estimate` and `pricing_confidence=LOW`.
4. If quantity and price are available but safety guardrails are incomplete,
   use `savings_status=reasonable_estimate`, keep confidence LOW, and state
   the missing guardrails in `savings_reason`.
5. Use `$0`, `pricing_source=unmeasured`, and `LOW` confidence only when the
   quantity or price cannot be determined from the evidence bundle and rules.

For E1 Fargate rightsizing, calculate current monthly compute cost as:

`desired_count * hours_per_month * (vcpu * vcpu_hour_usd + memory_gb * gb_hour_usd)`

Calculate the target cost from the proposed valid Fargate CPU/memory shape.
Safety guardrails that are not resolved should lower confidence and require
validation; they should not erase a calculable modeled estimate.

## Output Contract

Read `result/.machine/ecs_skill_request.json` after the first LangGraph pass. Use the
structured evidence bundle (`terraform`, `metrics`, `cost`, `pricing`, and
`resource_records`) to produce authoritative findings for this domain. If
`evidence_bundle.pricing.unresolved_skus` is non-empty, prefer filling
`pricing_cache/ecs_pricing_model.json` via AWS public pricing before final Skill
analysis; otherwise use static fallback only as tier 3. Write
`result/.machine/ecs_skill_analysis.json` conforming to
`schemas/skill-analysis.schema.json`, then rerun LangGraph.

Do not write Terraform patches; LangGraph will only normalize, validate,
aggregate, and report the Skill findings.

```json
{
  "schema_version": "1.0",
  "domain": "ecs",
  "skill_version": "2.0",
  "findings": [
    {
      "rule_id": "ECS_E1_FARGATE_RIGHTSIZE",
      "resource": "<tf_resource_name>",
      "severity": "HIGH",
      "confidence": "LOW",
      "estimated_monthly_saving_usd": 35.46,
      "pricing_source": "static_fallback_estimate",
      "evidence": [
        "cpu_avg_pct=12",
        "cpu_p95_pct=38",
        "errors=0",
        "desired_count=3",
        "current_cpu_units=1024",
        "target_cpu_units=512",
        "pricing_source=static_fallback_estimate"
      ],
      "recommendation": "Needs evidence: confirm sidecar reservations, deployment surge headroom, and latency SLA before downsizing."
    }
  ]
}
```

Use `$0`, `pricing_source=unmeasured`, and `LOW` confidence only when price or
quantity cannot be determined. Unresolved safety guardrails should be visible in
the evidence and recommendation.
