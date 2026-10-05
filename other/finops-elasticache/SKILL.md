---
name: finops-elasticache
description: >
  FinOps ElastiCache Analysis Skill. Detects cost waste in ElastiCache clusters
  from excess replicas, overprovisioned node types, missing reserved node
  coverage, and HA mismatches using Terraform, CloudWatch metrics, and AWS
  cost reports.
user_invocable: false
---

# FinOps ElastiCache Analysis Skill

## Scope

Reduce ElastiCache spend while preserving cache hit rates, read throughput,
eviction limits, replication lag, Multi-AZ availability, and failover
requirements.

## Required Evidence

| File | Used For | If Missing |
|------|----------|------------|
| `main.tf` | `aws_elasticache_replication_group`, node type, num_cache_clusters, Multi-AZ, parameter group, engine version | Cannot analyze; ask for path |
| `metrics.json` | CacheHitRate, Evictions, CPUUtilization, DatabaseMemoryUsagePercentage, ReplicationLag, NetworkBytesIn/Out | Mark metrics unavailable |
| `cost_report.json` | Monthly ElastiCache cost, reserved node coverage | Mark cost unavailable |

Missing facts: write `Not available in the provided data; verify in the real environment.`

## Detection Rules

| Rule | Condition | Severity | Action |
|------|-----------|----------|--------|
| EC1 | num_cache_clusters >2 AND read replica traffic is low (p95 connections <30% of primary) | HIGH | REVIEW_REDUCE_REPLICAS |
| EC2 | DatabaseMemoryUsagePercentage p95 <50% AND CPUUtilization avg <20% | HIGH | REVIEW_DOWNSIZE_NODE |
| EC3 | Steady baseline with no reserved node purchase AND monthly cost >$200 | LOW | MODEL_RESERVED_NODE |
| EC4 | Single node, no replica, no Multi-AZ, production workload | INFO | REVIEW_HA_POSTURE |
| EC5 | Engine version eligible for upgrade AND current version EOL or approaching EOL | MEDIUM | UPGRADE_ENGINE |

## Safety Guardrails

- Do not reduce replicas when eviction count is >0 in any observation window,
  or when replication lag exceeds 100ms at p95.
- Do not downsize node type when cache hit rate drops below 95% or when
  evictions are non-zero; these indicate memory pressure.
- EC1 and EC2 may co-occur; report both. Do not combine their savings.
- EC4 is informational; set `estimated_monthly_saving_usd` to 0.0.
- For EC3, model savings conservatively: 1-year reserved is typically 30% off
  on-demand. Only recommend if the cluster has been stable for at least 60 days.

## Modeled Savings And Pricing Source

Do not set savings to `$0` only because `cost_report.json` is missing. Use this
pricing waterfall and include `pricing_source` on every finding:

1. Prefer ElastiCache line items from `cost_report.json` when they clearly map
   to the cluster and recommendation. Set `pricing_source` to `cost_report`.
2. If AWS public pricing has been supplied, use
   `evidence_bundle.pricing.pricing_model` for node-hour unit prices. Set
   `pricing_source` to `aws_public_pricing_model` and cap confidence at
   `MEDIUM` unless cost allocation also confirms the resource.
3. If public pricing is unavailable but the rule cost block has matching node
   prices, use them as a modeled estimate with `pricing_source` set to
   `static_fallback_estimate` and `pricing_confidence=LOW`.
4. If quantity and price are available but safety guardrails are incomplete,
   use `savings_status=reasonable_estimate`, keep confidence LOW, and state
   the missing guardrails in `savings_reason`.
5. Use `$0`, `pricing_source=unmeasured`, and `LOW` confidence only when the
   quantity or price cannot be determined from the evidence bundle and rules.

For EC1 replica reduction, estimate savings as:

`removed_node_count * node_hourly_usd * hours_per_month`

For EC2 node downsizing, compare current node-hour cost against the target node
type cost for the same node count. Safety guardrails that are not resolved
should lower confidence and require validation; they should not erase a
calculable modeled estimate.

## Output Contract

Read `result/.machine/elasticache_skill_request.json` after the first LangGraph pass.
Use the structured evidence bundle (`terraform`, `metrics`, `cost`, `pricing`,
and `resource_records`) to produce authoritative findings for this domain. If
`evidence_bundle.pricing.unresolved_skus` is non-empty, prefer filling
`pricing_cache/elasticache_pricing_model.json` via AWS public pricing before final
Skill analysis; otherwise use static fallback only as tier 3. Write
`result/.machine/elasticache_skill_analysis.json` conforming to
`schemas/skill-analysis.schema.json`, then rerun LangGraph.

Do not write Terraform patches; LangGraph will only normalize, validate,
aggregate, and report the Skill findings.

```json
{
  "schema_version": "1.0",
  "domain": "elasticache",
  "skill_version": "2.0",
  "findings": [
    {
      "rule_id": "ELASTICACHE_EC1_REDUCE_REPLICAS",
      "resource": "<tf_resource_name>",
      "severity": "HIGH",
      "confidence": "LOW",
      "estimated_monthly_saving_usd": 280.32,
      "pricing_source": "static_fallback_estimate",
      "evidence": [
        "num_cache_clusters=4",
        "target_node_count=2",
        "node_type=cache.r6g.large",
        "pricing_source=static_fallback_estimate",
        "node_hourly_usd=0.192",
        "hours_per_month=730",
        "replica_connection_p95_pct=18",
        "evictions=0",
        "replication_lag_ms_p95=12"
      ],
      "recommendation": "Needs evidence: confirm read routing, failover posture, and cache pressure before reducing replicas."
    }
  ]
}
```

Use `$0`, `pricing_source=unmeasured`, and `LOW` confidence only when price or
quantity cannot be determined. Unresolved safety guardrails should be visible in
the evidence and recommendation.
