---
name: finops-rds
description: >
  FinOps RDS Analysis Skill. Detects RDS cost inefficiencies from instance
  over-sizing, unnecessary Multi-AZ, storage/IOPS over-provisioning, old engine
  support costs, and reserved instance coverage gaps using Terraform,
  CloudWatch metrics, and AWS cost reports.
user_invocable: false
---

# FinOps RDS Analysis Skill

## Scope

Reduce unnecessary database spend while preserving availability, durability,
performance, backup/restore, compliance, and maintenance requirements.

## Required Evidence

| File | Used For | If Missing |
|------|----------|------------|
| `main.tf` | `aws_db_instance`, storage, Multi-AZ, backups, replicas, monitoring, tags | Cannot analyze; ask for path |
| `metrics.json` | CPU avg/p95/max, connections, freeable memory, IOPS, throughput, latency, storage, queue depth | Mark metrics unavailable |
| `cost_report.json` | Monthly RDS cost, pricing notes, RI coverage, Extended Support, storage, IOPS, backup, transfer cost | Mark cost unavailable |

Missing facts: write `Not available in the provided data; verify in the real environment.`

## Detection Rules

| Rule | Condition | Severity | Action |
|------|-----------|----------|--------|
| R1 | Multi-AZ on non-production with no SLA/DR requirement | MEDIUM | REVIEW_SINGLE_AZ |
| R2 | Instance class underutilized across CPU, memory, connections, I/O with safe p95/max | HIGH | REVIEW_DOWNSIZE |
| R3 | Production baseline lacks Reserved DB coverage | LOW | REVIEW_RESERVED_INSTANCE |
| R4 | Old engine version incurs Extended Support cost | HIGH | UPGRADE_ENGINE |
| R5 | gp2 storage is a gp3 migration candidate | MEDIUM | REVIEW_GP3_MIGRATION |
| R6 | Read replica has very low connection usage | MEDIUM | REVIEW_REPLICA_DEPENDENCIES |

## Safety Guardrails

- Do not downsize or disable Multi-AZ from average CPU or environment tags
  alone. Check p95/max CPU, memory, connections, IOPS, storage, latency, queue
  depth, failover/SLA, backup/DR, RI coverage first.
- For R5 RI eligibility uncertainty (Aurora vs RDS, custom engines), note the
  uncertainty in the finding evidence rather than omitting the finding.
- R5 requires IOPS and throughput validation before accepting a migration.
- R6 requires DR, reporting, and read-routing dependency validation.

## Modeled Savings And Pricing Source

Do not set savings to `$0` only because `cost_report.json` is missing. Use this
pricing waterfall and include `pricing_source` on every finding:

1. Prefer RDS line items from `cost_report.json` when they clearly map to the
   resource and recommendation. Set `pricing_source` to `cost_report`.
2. If an AWS public pricing tool such as `mcp__aws-pricing__get_pricing` is
   available, use `evidence_bundle.pricing.pricing_model` for region, engine,
   instance class, deployment type, and on-demand hourly prices. Set
   `pricing_source` to `aws_public_pricing_model` and cap confidence at `MEDIUM`
   unless cost allocation also confirms the resource.
3. If public pricing is unavailable but the rule cost block has a matching
   static price, use it as a modeled estimate with `pricing_source` set to
   `static_fallback_estimate` and `pricing_confidence=LOW`.
4. If quantity and price are available but safety guardrails are incomplete,
   use `savings_status=reasonable_estimate`, keep confidence LOW, and state
   the missing guardrails in `savings_reason`.
5. Use `$0`, `pricing_source=unmeasured`, and `LOW` confidence only when the
   quantity or price cannot be determined from the evidence bundle and rules.

For R1 non-production Multi-AZ review, estimate the monthly compute savings for
moving to Single-AZ as:

`(multi_az_hourly_usd - single_az_hourly_usd) * hours_per_month`

Use `engine`, `instance_class`, `multi_az`, and `region` from Terraform evidence
plus `hours_per_month` from the rule cost block. Safety guardrails that are not
resolved should lower confidence and require validation in the recommendation;
they should not erase a calculable modeled estimate.

## Output Contract

Read `result/.machine/rds_skill_request.json` after the first LangGraph pass. Use the
structured evidence bundle (`terraform`, `metrics`, `cost`, `pricing`, and
`resource_records`) to produce authoritative findings for this domain. If
`evidence_bundle.pricing.unresolved_skus` is non-empty, prefer filling
`pricing_cache/rds_pricing_model.json` via AWS public pricing before final Skill
analysis; otherwise use static fallback only as tier 3. Write
`result/.machine/rds_skill_analysis.json` conforming to
`schemas/skill-analysis.schema.json`, then rerun LangGraph.

Do not write Terraform patches; LangGraph will only normalize, validate,
aggregate, and report the Skill findings.

```json
{
  "schema_version": "1.0",
  "domain": "rds",
  "skill_version": "2.0",
  "findings": [
    {
      "rule_id": "RDS_R1_NONPROD_MULTI_AZ",
      "resource": "<tf_resource_name>",
      "severity": "MEDIUM",
      "confidence": "LOW",
      "estimated_monthly_saving_usd": 365.0,
      "pricing_source": "static_fallback_estimate",
      "evidence": [
        "multi_az=true",
        "environment=dev",
        "instance_class=db.r5.xlarge",
        "engine=postgres",
        "pricing_source=static_fallback_estimate",
        "multi_az_hourly_usd=1.0",
        "single_az_hourly_usd=0.5",
        "hours_per_month=730",
        "sla_requirement=not_available"
      ],
      "recommendation": "Needs evidence: confirm SLA/DR/compliance requirements before changing Multi-AZ."
    }
  ]
}
```

Use `$0`, `pricing_source=unmeasured`, and `LOW` confidence only when price or
quantity cannot be determined. Unresolved safety guardrails should be visible in
the evidence and recommendation.
