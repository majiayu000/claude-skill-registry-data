---
name: pie-alert
description: PIE early warning system. Detects regressions, market events, source failures, and anomalies. Fires before users notice problems. Triggers self-healing or escalation. Law 5 (Self-Healing) enforcer.
---

# PIE Alert

The immune system. Detects problems before they become user-visible failures.
At scale (millions of users), a broken source or bad price that goes undetected
for 24 hours affects thousands of purchasing decisions. Unacceptable.

## Trigger Conditions

- Every 6 hours (Hermes cron)
- After any OpenClaw sync (post-sync validation)
- After `/pie-accuracy` finds regression
- After any source goes dark (scrape failure)
- User says "PIE alerts", "any problems?", "check for issues"

## Alert Categories

### 1. Source Failure (CRITICAL, Law 5)

A scraping source stopped producing data.

**Detection:**

```sql
-- Chains with no new prices in expected refresh window
SELECT c.name as chain, c.refresh_interval_hours,
  MAX(sp.last_seen_at) as last_price,
  EXTRACT(HOURS FROM now() - MAX(sp.last_seen_at)) as hours_dark
FROM openclaw.chains c
JOIN openclaw.stores s ON s.chain_id = c.id AND s.is_active = true
JOIN openclaw.store_products sp ON sp.store_id = s.id
WHERE c.is_active = true
GROUP BY c.id, c.name, c.refresh_interval_hours
HAVING EXTRACT(HOURS FROM now() - MAX(sp.last_seen_at)) > c.refresh_interval_hours * 2
```

**Auto-response:**

1. Mark affected prices as "degraded confidence"
2. Activate fallback chain (Law 10)
3. Log incident
4. If Pi-side scraper: SSH to Pi, check scraper logs
5. If 3+ chains fail simultaneously: likely Pi problem, escalate

### 2. Price Spike/Crash (HIGH, Law 5)

Individual ingredient price moved abnormally.

**Detection:**

```sql
-- Prices that moved > 50% in 7 days (likely data error, not market)
SELECT ci.name,
  old_price.avg_cents as prev_price,
  new_price.avg_cents as curr_price,
  ((new_price.avg_cents - old_price.avg_cents)::float / old_price.avg_cents * 100) as change_pct
FROM openclaw.canonical_ingredients ci
JOIN LATERAL (
  SELECT AVG(price_cents) as avg_cents
  FROM ingredient_price_history
  WHERE ingredient_id = ci.ingredient_id
    AND observed_at BETWEEN now() - interval '14 days' AND now() - interval '7 days'
) old_price ON true
JOIN LATERAL (
  SELECT AVG(price_cents) as avg_cents
  FROM ingredient_price_history
  WHERE ingredient_id = ci.ingredient_id
    AND observed_at > now() - interval '7 days'
) new_price ON true
WHERE ABS((new_price.avg_cents - old_price.avg_cents)::float / NULLIF(old_price.avg_cents, 0) * 100) > 50
```

**Auto-response:**

1. Quarantine suspicious prices
2. Check if it's real (multiple sources confirm) or data error (single source)
3. If real: update trend data, flag for chef alerts
4. If error: remove bad data, log source quality incident

### 3. Coverage Regression (HIGH)

Coverage % dropped compared to previous measurement.

**Detection:** Compare `/pie-measure` output to last logged value.
If `coverage_pct` dropped > 1% or `naked_count` increased: alert.

**Auto-response:**

1. Identify what was lost (which ingredients, which regions)
2. Usually caused by: source failure, bad sync, data corruption
3. Trigger `/pie-ratchet` focused on lost coverage
4. If caused by Census expansion without price follow-through: normal, not regression

### 4. Freshness Degradation (MEDIUM)

Stale prices accumulating faster than refresh cycle handles.

**Detection:**

```sql
SELECT
  COUNT(*) FILTER (WHERE last_seen_at < now() - interval '7 days'
    AND census_tier = 'core'
    AND freshness_category = 'volatile') as stale_volatile_core
FROM pricing_view
```

If `stale_volatile_core` > 500: alert. Core volatile items (fresh produce, proteins)
must be fresh. Stale core prices are user-visible failures.

**Auto-response:**

1. Identify which chains/regions are stale
2. Check if scraper is running (Pi cron)
3. If scraper running but prices stale: source may have changed format
4. Trigger targeted refresh or synthetic re-estimation

### 5. Market Event (MEDIUM, Law 11)

Real market disruption detected from price data patterns.

**Detection patterns:**

- **Supply shock:** 10+ proteins spike > 20% same week (e.g., bird flu)
- **Regional disruption:** all prices in one state spike (e.g., hurricane)
- **Seasonal shift:** produce category moves > 15% collectively
- **Commodity swing:** staples (eggs, milk, bread) move > 10% nationally

**Auto-response:**

1. Classify event type
2. Flag affected ingredients with event context
3. If affects chef menu costs significantly: queue alert for affected chefs
4. Update seasonal models if seasonal (Law 7: Compound Learning)

### 6. Sync Failure (CRITICAL)

Pi-to-PG sync didn't complete.

**Detection:** Check `.last-sync-time` in `scripts/openclaw-pull/`.
If older than 48 hours: alert.

**Auto-response:**

1. SSH to Pi, check disk space and process status
2. Check PG connectivity
3. Attempt manual sync trigger
4. If Pi unreachable: note in morning briefing, degrade confidence on all prices

### 7. Confidence Drift (LOW)

Confidence scores no longer match actual accuracy (detected by `/pie-accuracy`).

**Detection:** Last accuracy run showed confidence tier missing its target.

**Auto-response:**

1. Log which tier drifted
2. Queue confidence recalibration in next session
3. Do NOT change confidence scores without full accuracy run to validate

## Alert Severity and Response Time

| Severity | Response time   | Who handles                      | Example                             |
| -------- | --------------- | -------------------------------- | ----------------------------------- |
| CRITICAL | < 1 hour        | Auto-heal, then notify developer | Source failure, sync failure        |
| HIGH     | < 6 hours       | Auto-heal attempt, log           | Price spike, coverage regression    |
| MEDIUM   | < 24 hours      | Queue for next ratchet run       | Freshness degradation, market event |
| LOW      | Next weekly run | Log for trend tracking           | Confidence drift                    |

## Self-Healing Protocol (Law 5)

For CRITICAL and HIGH alerts:

```
1. DETECT    -> alert fires
2. ISOLATE   -> quarantine bad data if applicable
3. FALLBACK  -> activate next source in chain (Law 10)
4. DIAGNOSE  -> identify root cause
5. REPAIR    -> fix if automated fix exists
6. VERIFY    -> confirm fix worked
7. LOG       -> full incident record
8. LEARN     -> update detection thresholds if false positive/negative
```

The entire sequence should complete without human intervention for known
failure modes. Unknown failures escalate to developer morning briefing.

## Alert Log

Append all alerts to `docs/pie-alert-log.md`:

```markdown
## [ISO timestamp] - [SEVERITY] [category]

**Detected:** [what was found]
**Impact:** [N ingredients, N regions, N users affected]
**Auto-response:** [what was done]
**Resolved:** yes/no
**Root cause:** [if known]
**Duration:** [time from detection to resolution]
```

## Existing Code to Leverage

- `lib/pricing/anomaly-detector.ts` - already detects price anomalies
- `lib/pricing/source-health-worker.ts` - monitors source freshness
- `lib/pricing/freshness-enforcer.ts` - enforces freshness rules
- `lib/openclaw/health-sources.ts` - source health tracking
- `lib/openclaw/health-contract.ts` - health check contracts
- `scripts/openclaw-pull/.last-sync-time` - sync recency check
- `lib/openclaw/pi-stats.ts` - Pi connectivity

**IMPORTANT:** Much of this detection logic may already exist in the anomaly
detector and source health worker. Wire existing code into the alert framework
rather than rebuilding detection from scratch.

## Constraints

- **Auto-heal first, escalate second.** Never alert without attempting a fix.
- **No false positive fatigue.** Tune thresholds so alerts are real. A noisy alert system gets ignored.
- **Never suppress CRITICAL.** Source failures and sync failures always surface.
- **Log everything.** Alert history enables trend analysis and threshold tuning.
- **Ratchet principle applies.** Once a failure mode is detected and fixed, it should never recur undetected. Add the detection to permanent monitoring.

## Key Files

- Anomaly detector: `lib/pricing/anomaly-detector.ts`
- Source health: `lib/pricing/source-health-worker.ts`
- Freshness enforcer: `lib/pricing/freshness-enforcer.ts`
- Health sources: `lib/openclaw/health-sources.ts`
- Pi stats: `lib/openclaw/pi-stats.ts`
- Sync time: `scripts/openclaw-pull/.last-sync-time`
- Alert log: `docs/pie-alert-log.md`
- PIE Laws: `docs/specs/pie-laws.md` (Laws 5, 10, 11)
