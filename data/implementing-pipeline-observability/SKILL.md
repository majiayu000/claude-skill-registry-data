---
name: implementing-pipeline-observability
description: Instrument data pipelines with observability — freshness and volume SLAs, run success/latency metrics, data quality monitors, anomaly detection, lineage, and actionable alerting that avoids fatigue. Use when pipelines fail silently, incidents are found by stakeholders instead of alerts, setting up monitoring/SLAs for data, or reducing noisy alerts.
---

# Implementing Pipeline Observability

## When to use

- Failures or stale data are discovered by stakeholders, not by your alerts.
- Setting up monitoring, SLAs, or on-call for data pipelines.
- Alerts are too noisy (fatigue) or too quiet (silent failures).
- Do NOT use for one-off incident debugging (use `debugging-data-pipelines`).

## The four signals to monitor

1. **Freshness** — is data arriving within its SLA? (most incidents are lateness)
2. **Volume** — is row count within the expected range vs a trailing baseline?
3. **Quality** — do the data quality checks pass? (see
   `implementing-data-quality-checks`)
4. **Run health** — job success/failure, duration, and retry rate.

## Workflow

```
- [ ] Define SLAs per critical dataset (freshness + volume)
- [ ] Emit run metrics: status, duration, rows in/out per run
- [ ] Add freshness + volume monitors with baseline-relative thresholds
- [ ] Route alerts to an owner with context and a runbook link
- [ ] Tune thresholds to cut false positives; track MTTD/MTTR
```

1. **Set SLAs** for datasets that feed decisions ("orders fresh within 3h,
   ±20% daily volume"). Without an SLA there is nothing to alert against.
2. **Emit run metrics** (status, duration, input/output row counts) to a store you
   can query and chart, not just scattered logs.
3. **Monitor freshness and volume** against **trailing baselines**, not fixed
   numbers, so seasonality doesn't trigger noise.
4. **Make alerts actionable** — every alert names the dataset, the breached SLA,
   the likely blast radius, and links a runbook. Route to a clear owner.
5. **Tune** — suppress duplicates, group related alerts, and set severities so
   people trust the pager.

## Patterns

**Freshness monitor:**

```sql
-- Alert when the newest row is older than the SLA.
SELECT DATEDIFF('hour', MAX(ordered_at), CURRENT_TIMESTAMP()) AS hours_stale
FROM fct_orders
HAVING hours_stale > 3;
```

**Volume anomaly vs trailing baseline** — compare today's count to the mean of the
prior N days and alert on a large relative deviation, catching partial loads and
duplication that a fixed threshold misses.

**Run metrics** — record `{pipeline, run_id, status, started_at, duration_s,
rows_in, rows_out}` per run; chart duration and row counts to spot drift before it
becomes an incident. Tools: dbt artifacts, OpenLineage/Marquez, Elementary, Monte
Carlo, or a simple metrics table.

**Alert routing** — critical → page the owning team with a runbook; warning →
async channel. Deduplicate and group so one upstream failure isn't 50 pages.

## Common pitfalls

- **Alerting only on job failure** — data can be stale or wrong while every job
  "succeeds"; monitor freshness/volume/quality too.
- **Fixed thresholds on seasonal data** — false positives train people to ignore
  alerts; use trailing baselines.
- **Alerts with no owner or context** — nobody acts; include dataset, SLA, impact,
  and a runbook.
- **Over-alerting** — fatigue causes real incidents to be missed; tune severity
  and dedupe.
- **No metrics history** — you can't see gradual regressions (creeping duration,
  shrinking volume) without stored run metrics.
- **Monitoring everything equally** — focus SLAs on datasets that drive decisions.
