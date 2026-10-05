---
name: finops
description: Run CloudSweep LangGraph analysis, AI review, and report polish into one final AWS FinOps report.
user_invocable: true
---

# FinOps Orchestrator

## Authority Boundary

**Simple and GenAI domains** (lambda, s3, dynamodb, bedrock, sagemaker, ec2,
ebs, cloudwatch, cloudwatch-alarm, sqs, kinesis, nat, tgw, organizations):
LangGraph Python analyzers own detection, thresholds, savings arithmetic, and
Terraform remediation candidates. Claude is the reviewer only.

**Complex domains** (rds, elb, ecs, elasticache):
LangGraph owns evidence packaging: Terraform resource attributes, domain metric
summaries and derived series, cost slices, and resource records. Claude domain
skills own the complex-domain findings themselves. If quantity or unit price
cannot be resolved from the provided evidence, the Skill must use
`estimated_monthly_saving_usd=0.0`, `savings_status=unmeasured`, and
`confidence=LOW`. If quantity and price are available but safety guardrails are
incomplete, use `savings_status=reasonable_estimate` and keep it separate from
evidence-backed savings.

**Public-pricing modeling** (s3, lambda, rds, elb, ecs, elasticache): when
`cost_report.json` is absent or does not resolve a resource's price, LangGraph
may request a raw AWS public on-demand unit price via
`result/.machine/{domain}_pricing_request.json`. Claude supplies only a unit price per
SKU key in the **shared, cross-scenario cache** at
`pricing_cache/{domain}_pricing_model.json` (repo root -- schema:
`schemas/pricing-model.schema.json`) using `mcp__aws-pricing__get_pricing` --
never a savings figure. This file is shared because AWS public list pricing
for a given region+SKU is identical across every scenario; **merge new
sku_key entries into the existing cache file rather than overwriting it.**
LangGraph performs all quantity x price x waste-ratio arithmetic (simple
domains) or the complex-domain Skill performs its own arithmetic using the
resolved unit prices in its evidence bundle (complex domains), capping the
resulting confidence at MEDIUM. This does not change who owns detection,
thresholds, or savings arithmetic. Supplying the pricing model is optional
enrichment, not a gate: findings are already priced via cost_report, a static
per-unit rule price, or reported as unmeasured on every run regardless of
whether a pricing model exists yet.

## Inputs

Set `WORK_DIR` to the workload or scenario directory. CloudSweep inventories
supported evidence such as Terraform, metrics, parsed input, cost reports,
GenAI evidence, Cost Explorer responses, anomaly results, and CloudTrail events.

All generated artifacts belong under `<WORK_DIR>/result/`.

## Required Workflow

1. Inventory evidence under `WORK_DIR` and detect which domains are present.

   When evidence comes from MiniStack, collect it before domain analysis:

```text
python -m cloudsweep <WORK_DIR> --from-ministack --collect-only
```

2. Run LangGraph once. For each complex domain it writes
   `result/.machine/{domain}_skill_request.json` containing a structured evidence
   bundle.

2b. **For each pending `result/.machine/{domain}_pricing_request.json`** (written when
   `cost_report.json` is absent and no valid cached pricing model resolves
   every needed SKU), call `mcp__aws-pricing__get_pricing` for each listed
   `sku_key`. Read the existing `pricing_cache/{domain}_pricing_model.json`
   if present and **merge** the newly-resolved SKUs into its `unit_prices`
   list (do not drop existing entries); write the merged file back to
   `pricing_cache/{domain}_pricing_model.json` per
   `schemas/pricing-model.schema.json`. This is a shared, cross-scenario
   cache at the repo root, not scoped to this scenario's `result/` folder.
   This step is optional per run: if skipped, LangGraph still emits findings,
   priced from the domain's static fallback rule price (or reported as
   unmeasured) at LOW confidence.

3. **For each complex domain request** (rds, elb, ecs, elasticache), run the
   corresponding Claude skill so it writes authoritative findings:

   | Domain | Skill | Output file |
   |--------|-------|-------------|
   | rds | finops-rds | `result/.machine/rds_skill_analysis.json` |
   | elb | finops-elb | `result/.machine/elb_skill_analysis.json` |
   | ecs | finops-ecs | `result/.machine/ecs_skill_analysis.json` |
   | elasticache | finops-elasticache | `result/.machine/elasticache_skill_analysis.json` |

   Simple and GenAI domains do not need a pre-run step.

4. Rerun the LangGraph machine analysis:

```text
python -m cloudsweep <WORK_DIR>
```

   LangGraph loads any `result/.machine/{domain}_skill_analysis.json` files it finds and
   enriches them with `finding_id`, `savings_group`, and `evidence_facts`.
   If a complex-domain Skill output is missing, LangGraph emits no findings for
   that complex domain and writes `result/.machine/{domain}_skill_request.json`. Run the
   missing domain Skill and rerun LangGraph; never infer complex-domain savings
   from the request bundle alone.

5. Read `result/.machine/cloudsweep_graph_state.json`. Treat an `unsupported` status in
   `analyzer_coverage` as an error. Do not replace a missing analyzer with
   Claude arithmetic.

6. If LangGraph writes `result/.machine/ai_review_request.json`, perform the
   AI review described in that request and write
   `result/.machine/ai_review.json` using `schemas/ai-review.schema.json`.
   This review is advisory: it may identify missed candidates, overreach,
   weak evidence, and cross-domain hypotheses, but it may not mutate finding
   IDs, savings, pricing source, savings status, or Terraform patches.

7. Rerun LangGraph. If it writes
   `result/.machine/report_polish_request.json`, write concise executive
   prose to `result/.machine/report_polish.json` using
   `schemas/report-polish.schema.json`. Report polish must preserve
   evidence-backed savings and `reasonable_estimate` upside as separate
   numbers.

8. Rerun LangGraph one final time. The final output is the single report
   `result/finops_report.md` plus `result/main_optimized.tf` when
   `--standard-output` is used. AI review and report polish are folded into
   that one report; do not run a separate `claude_review`/`finalize` report
   path for this workflow.

## Review Rules

- Cite `fact_id` values for every observed cross-domain statement.
- Mark an unobserved relationship as `hypothesis`; exclude it from savings.
- Missing ownership, SLA, compliance, dependency, peak, or cross-account
  evidence should be called out as a caveat or follow-up unless it directly
  contradicts the candidate. Do not erase a priced or reasonable-estimate
  candidate solely because approval evidence is pending.
- Never apply Terraform. CloudSweep writes candidate output only.
- Preserve Terraform candidates only when their source hash still matches.
- Do not double count alternative findings or organization and workload savings.

## Outputs

Machine outputs:

```text
result/.machine/cloudsweep_graph_state.json
result/.machine/{domain}_pricing_request.json   (only when cost_report is absent and the shared cache doesn't resolve every SKU)
result/.machine/ai_review_request.json           (only when AI review is pending)
result/.machine/report_polish_request.json       (only when report polish is pending)
```

Claude/AI internal outputs:

```text
result/.machine/ai_review.json
result/.machine/report_polish.json
pricing_cache/{domain}_pricing_model.json   (shared cache at repo root, NOT under result/ -- optional, in response to a pricing_request; merge, don't overwrite)
```

Final outputs:

```text
result/finops_report.md
result/main_optimized.tf
```
