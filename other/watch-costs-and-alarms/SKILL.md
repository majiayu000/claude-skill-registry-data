---
name: watch-costs-and-alarms
description: Check AWS spend, run the cost report, or investigate CloudWatch alarms, budgets, and the dead-letter queue (cost review, billing check, why is spend up, alarm triage).
---
# Watch costs and alarms

Observability is CloudWatch plus deliberate cost guardrails: structured JSON
logs, seven alarms, a $60/month budget, a $150 billing tripwire, a cost anomaly
monitor, and `just cost-report` as the monthly cost-review (FinOps) ritual.

## Read first
- docs/OBSERVABILITY.md — the alarm table, cost guardrails, symptom-by-symptom triage checklists, and "The honest gaps".
- docs/PRD.md §16 — the FinOps invariants the guardrails implement.

## Commands
```bash
just cost-report    # Cost Explorer, last 30 days, grouped by stack tag + unit-economics KPIs
```
AWS credentials for account 458443189947. Alarms (search the CloudWatch console by construct name): `BillingAlarm` (WosCoreStack, > $150), `DltDepthAlarm` (WosBusStack, ≥ 1 message in SQS `wos-events-dlt`), four `OffsetLagAlarm`s (archiver/graph-writer/responder/live-publisher, > 1000 for 30 min), `Api5xxAlarm` (WosApiStack). Budget: `wandering-os-monthly`, $60, emails mbw@mbw.dev at 50/80/100%.

## Gotchas
- As of July 2026 nothing pages anyone: only `BillingAlarm` has an action, and its `CostAlerts` SNS topic has zero confirmed subscribers. Budget and anomaly alerts email mbw@mbw.dev directly, without SNS.
- Roughly half the spend bills outside AWS — Confluent, Neo4j Aura, Anthropic — so cost-report numbers are AWS-only; vendor consoles are manual paste-ins.
- All alarms treat missing data as not-breaching (the pipeline is idle between trips; silence must not page).
- Dead-letter records hold pointers (topic/partition/offset), not payloads, and expire after 14 days — the S3 archive is the durable copy.
- FinOps invariants are CI-enforced by infra synth tests (tags, budget, no NAT/MSK); any new always-on resource needs a PRD §16.1 cost-table entry in the same PR.
