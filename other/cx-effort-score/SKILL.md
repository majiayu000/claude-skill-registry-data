---
name: cx-effort-score
description: Use to measure customer effort from behavioural signals instead of CES surveys, and to audit whether a composite effort score is honest. Trigger for "customer effort score", "behavioural CES", effort without survey, repeat contacts and channel switches, transfers and reopens, or "our CES doesn't match operational data".
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Behavioural customer effort

CES asks customers how hard something felt. The answers arrive late, from a biased
sample, and conflate product pain with support pain. **Behavioural effort** uses what
they already did: repeats, switches, transfers, reopens, and time-to-resolution.

The trap on the other side is a **precision theatre composite** — five decimal places
on an index nobody can action. This skill builds a coarse, auditable effort signal,
not a fake science score.

## Signals that indicate effort

Each signal should be **observable in ticket/contact data** with stable definitions.

| Signal | Definition (typical) | What it captures |
| --- | --- | --- |
| **Repeat contacts** | Same customer + same driver within N days | Failure to resolve |
| **Channel switches** | Different channel, same issue window | Self-service or async failed |
| **Transfers** | Handoffs between teams/queues in one episode | Routing and specialisation friction |
| **Reopens** | Closed ticket reopened within N days | Premature closure or recurring defect |
| **Handle episodes** | Count of agent touches to resolution | Internal thrash |
| **Time to resolution** | First contact to final close | Delay; compare within driver |
| **Self-service failure** | KB view or bot session then contact | Documented in funnel |
| **Customer message volume** | Inbound messages per issue | Ping-pong async |

Normalise **time to resolution by driver**. Billing disputes should not be scored
against password resets on the same scale.

## CES survey traps (when you still have survey CES)

| Trap | Symptom | Behavioural cross-check |
| --- | --- | --- |
| Post-interaction timing | High CES, low outcome effort | Reopens within 7 days |
| Agent-triggered sends | CES improves, repeats rise | Compare solicited vs automatic sample |
| Scale change | Step change in trend | Driver-level repeats flat |
| Channel mix | Email CES vs chat CES | Switch rate into voice |
| "Easy" closed quickly | Good CES on rushed closes | Reopen rate |

If behavioural effort rises while CES falls, **trust the behaviour** until survey
solicitation, timing, and response bias are audited.

## Constructing a composite (without fake precision)

**Step 1 — Binary flags per episode.** For each resolved issue episode, mark whether
each signal exceeded a threshold (e.g. ≥2 transfers, reopen within 7 days, ≥2
channels). Thresholds should be set from **distribution elbows** on your own data,
not industry benchmarks.

**Step 2 — Weight by actionability, not optics.**

| Weight higher | Weight lower |
| --- | --- |
| Reopens, repeats on same driver | Absolute handle time alone |
| Channel switch after bot/KB | Single long wait on voice |
| Transfers across silos | One transfer to specialist |

**Step 3 — Bucket, do not over-index.** Report:

- **Low effort** — zero or one minor signal
- **Medium** — two signals or one severe (reopen, ≥3 transfers)
- **High** — repeat + switch, or reopen + long TTR

A single 0–100 score is optional for dashboards; **always publish bucket counts and
top drivers of high effort** alongside it.

**Step 4 — Segment honestly.** Effort varies by driver, channel, and customer type.
One global number hides product bugs as "support friction."

```
high_effort_rate = high_effort_episodes / all_episodes   (by driver, channel)
```

## Data requirements

| Field | Required |
| --- | --- |
| `customer_id` | Stable across channels |
| `issue_id` or linked episode key | Group touches into one effort story |
| `driver` / intent | Segment thresholds |
| `channel` per touch | Switch detection |
| `started_at`, `closed_at` | TTR |
| `transfer_count` or queue history | Transfer signal |
| `reopened_at` or status history | Reopen signal |

Without episode linking, **every ticket looks like low effort**.

## Traps

**Counting transfers as skill failure.** Some drivers require specialist routing;
measure **avoidable transfers** (return to previous queue, wrong team) via taxonomy.

**Penalising proactive outreach.** Exclude vendor-initiated contacts from repeats.

**Bot sessions as zero effort.** Include self-service failure in the episode.

**False precision.** Weighting tuned to 0.01 on 90 days of data will not replicate.
Prefer stable buckets and driver breakdowns.

## Present results to the user

1. **Effort bucket distribution** — low / medium / high with episode counts and
   definitions used.
2. **Top drivers of high effort** — ranked by volume × high-effort rate.
3. **Signal contribution** — which flags fire most often within high-effort episodes.
4. **Channel and segment cuts** — where switches and repeats concentrate.
5. **CES comparison** (if available) — where survey and behaviour disagree, with
   likely survey bias named.
6. **Recommended interventions** — mapped to signals (reopen → closure QA; switch →
   KB/bot; transfers → routing audit), not "improve effort score."
