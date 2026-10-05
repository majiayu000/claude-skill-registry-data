---
name: finops-elb
description: >
  FinOps ELB Analysis Skill. Detects cost waste in idle or underutilized AWS
  load balancers (ALB/NLB/CLB) using Terraform, CloudWatch metrics, and AWS
  cost reports. Checks DNS, listener, target group, blue-green, and DR
  dependencies before flagging for deletion.
user_invocable: false
---

# FinOps ELB Analysis Skill

## Scope

Identify idle or overprovisioned load balancers while preserving active
traffic paths, blue-green deployments, DR standby capacity, and
certificate/WAF dependencies.

## Required Evidence

| File | Used For | If Missing |
|------|----------|------------|
| `main.tf` | `aws_lb`, `aws_alb`, `aws_elb`, listeners, target groups, certificates, WAF, DNS records | Cannot analyze; ask for path |
| `metrics.json` | RequestCount, ActiveConnectionCount, NewConnectionCount, ProcessedBytes, HealthyHostCount, UnHealthyHostCount | Mark metrics unavailable |
| `cost_report.json` | Monthly ELB/ALB cost per resource | Mark cost unavailable |

Missing facts: write `Not available in the provided data; verify in the real environment.`

## Detection Rules

| Rule | Condition | Severity | Action |
|------|-----------|----------|--------|
| LB1 | Zero requests AND zero active connections over observation period | HIGH | REVIEW_DELETE_IDLE_ALB |
| LB2 | Very low request rate (<100/day) with all healthy targets | MEDIUM | REVIEW_CONSOLIDATE |
| LB3 | NLB with no TLS offload or WAF requirement (ALB features unused) | LOW | REVIEW_DOWNGRADE_TO_NLB |
| LB4 | Classic Load Balancer (CLB) still in use | MEDIUM | MIGRATE_TO_ALB |
| LB5 | Listener exists but all target groups are empty | HIGH | REVIEW_DELETE_STALE_LISTENER |

## Safety Guardrails

- Do not flag for deletion when DNS records (Route 53 or external) point to
  the load balancer. Check `aws_route53_record` aliases in the Terraform slice.
- Do not flag when blue-green or canary deployment evidence is present (multiple
  target groups, weighted routing, or `deployment_group` references).
- Do not flag when the load balancer is a DR standby (tagged `Environment=dr`
  or `Purpose=standby`).
- Treat incomplete metrics (observation window <7 days) as confidence=LOW.
- NLB metrics differ from ALB: `ActiveFlowCount` replaces `ActiveConnectionCount`;
  adjust rule LB1 accordingly.

## Modeled Savings And Pricing Source

Do not set savings to `$0` only because `cost_report.json` is missing. Use this
pricing waterfall and include `pricing_source` on every finding:

1. Prefer ELB/ALB/NLB line items from `cost_report.json` when they clearly map
   to the resource and recommendation. Set `pricing_source` to `cost_report`.
2. If AWS public pricing has been supplied, use
   `evidence_bundle.pricing.pricing_model` for load balancer-hour and
   LCU/NLCU/GLCU-hour unit prices. Set `pricing_source` to
   `aws_public_pricing_model` and cap confidence at `MEDIUM` unless cost
   allocation also confirms the resource.
3. If public pricing is unavailable but the rule cost block has a matching
   static price, use it as a modeled estimate with `pricing_source` set to
   `static_fallback_estimate` and `pricing_confidence=LOW`.
4. If quantity and price are available but safety guardrails are incomplete,
   use `savings_status=reasonable_estimate`, keep confidence LOW, and state
   the missing guardrails in `savings_reason`.
5. Use `$0`, `pricing_source=unmeasured`, and `LOW` confidence only when the
   quantity or price cannot be determined from the evidence bundle and rules.

For idle load balancer deletion review, model fixed monthly savings as
`load_balancer_hourly_usd * hours_per_month`. Add observed LCU/NLCU/GLCU
savings only when usage quantity is present. Safety guardrails that are not
resolved should lower confidence and require validation; they should not erase
a calculable modeled estimate.

## Output Contract

Read `result/.machine/elb_skill_request.json` after the first LangGraph pass. Use the
structured evidence bundle (`terraform`, `metrics`, `cost`, `pricing`, and
`resource_records`) to produce authoritative findings for this domain. If
`evidence_bundle.pricing.unresolved_skus` is non-empty, prefer filling
`pricing_cache/elb_pricing_model.json` via AWS public pricing before final Skill
analysis; otherwise use static fallback only as tier 3. Write
`result/.machine/elb_skill_analysis.json` conforming to
`schemas/skill-analysis.schema.json`, then rerun LangGraph.

Do not write Terraform patches; LangGraph will only normalize, validate,
aggregate, and report the Skill findings.

```json
{
  "schema_version": "1.0",
  "domain": "elb",
  "skill_version": "2.0",
  "findings": [
    {
      "rule_id": "ELB_LB1_UNUSED",
      "resource": "<tf_resource_name>",
      "severity": "HIGH",
      "confidence": "LOW",
      "estimated_monthly_saving_usd": 16.43,
      "pricing_source": "static_fallback_estimate",
      "evidence": [
        "request_count_sum=0",
        "active_connection_count_max=0",
        "load_balancer_type=application",
        "pricing_source=static_fallback_estimate",
        "load_balancer_hourly_usd=0.0225",
        "hours_per_month=730",
        "no Route53 alias found"
      ],
      "recommendation": "Needs evidence: confirm DNS, certificate, WAF, and DR dependencies before deleting the load balancer."
    }
  ]
}
```

Use `$0`, `pricing_source=unmeasured`, and `LOW` confidence only when price or
quantity cannot be determined. Unresolved safety guardrails should be visible in
the evidence and recommendation.
