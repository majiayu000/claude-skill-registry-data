---
name: cx-volume-forecasting
description: Use to forecast support contact volume and calculate staffing requirements for voice, chat, or async channels. Trigger for "how many agents do we need", "forecast our ticket volume", "Erlang C", workforce management or WFM planning, service level and occupancy targets, shrinkage, headcount planning for support, or when a staffing model keeps missing its service level.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Forecasting volume and staffing to it

Two separate problems that get conflated, which is why staffing plans miss:

1. **Forecasting** — how many contacts will arrive, per interval.
2. **Staffing** — how many agents that requires at a given service level.

Getting the second right on a wrong forecast produces a confident wrong answer.
Getting the first right and then applying a queueing model whose assumptions your
channel violates produces the same. Do them in order, separately.

## Part 1: forecasting

### Forecast contacts per business unit, not contacts

Support volume is a function of business volume. Forecasting raw contacts means
re-learning your company's growth curve every quarter and being wrong at every
inflection.

Forecast the **ratio** — contacts per 1,000 active customers, per 1,000 orders,
per 1,000 shipments — then multiply by the business forecast someone else already
owns. Two benefits: the ratio is far more stable than the count, and when it
moves you have learned something real (a product regression, a policy change)
rather than just observing growth.

### Beat seasonal naive or don't ship

The baseline to beat is **seasonal naive**: this Tuesday 10:00 will look like last
Tuesday 10:00. It is free, it is surprisingly hard to beat, and a model that
cannot beat it is adding complexity and risk for nothing.

Measure error with **WAPE** (weighted absolute percentage error), not MAPE:

```
WAPE = Σ|actual − forecast| / Σ actual
```

MAPE divides by each actual, so a 30-minute interval with 2 contacts and a
forecast of 4 contributes a 100% error and dominates the average. Intraday
support forecasting is full of low-volume intervals, which is exactly where MAPE
becomes useless.

### The three seasonalities, and the fourth thing

- **Intraday** — the within-day curve. The most important and most stable.
- **Day of week** — Monday is not Saturday.
- **Annual / monthly** — paydays, month-end, billing cycles, holidays.
- **Events**, which are not seasonality: marketing sends, releases, outages,
  price changes, regulatory deadlines. These are the large errors, and no
  time-series model will find them. **They come from a calendar someone
  maintains**, not from history. If nobody maintains that calendar, that is the
  highest-value fix available to the forecast, ahead of any modelling work.

### Forecast the peak, staff the peak

A daily total tells you nothing about whether Tuesday 10:00 is survivable.
Forecast and staff at the interval you schedule to — usually 15 or 30 minutes.
Averaging a day and dividing by hours systematically understaffs the peak and
overstaffs the trough.

## Part 2: staffing

```bash
node scripts/staffing.mjs --mode voice --contacts 250 --aht 300
```

**Arguments**

- `--mode <voice|chat|async>` — the three cases are genuinely different models.
- `--contacts <n>` — contacts arriving in the interval.
- `--aht <seconds>` — average handling time **including after-contact work**.
- `--interval <minutes>` — default 30.
- `--target <seconds>` / `--service-level <p>` — e.g. 20 and 0.8 for 80/20.
- `--shrinkage <p>` — default 0.30.
- `--concurrency <n>` — chat mode: simultaneous conversations per agent.
- `--agents <n>` — evaluate a given headcount instead of solving for one.
- `--backlog-hours <h>` — async mode: the turnaround you are promising.

The tool prints a **marginal-agent table**, which is the actually
decision-useful output. Service level is steeply non-linear in headcount: near
the target, one agent can be worth 6 percentage points, and three agents further
on can be worth 2. That curve is where the staffing conversation should happen.

Method, formulas, and the derivation:
[references/queueing-models.md](references/queueing-models.md).

### The three numbers people get wrong

**Shrinkage is not optional, and it is bigger than you think.** It covers holiday,
sickness, breaks, training, meetings, coaching, 1:1s, and system downtime — every
paid hour not available to take contacts. Typical is **30–35%**. Erlang gives you
*productive* agents; rostered headcount is `productive / (1 − shrinkage)`. At 30%
shrinkage, 48 productive agents means **69 rostered**. Under-stating shrinkage is
the single most common cause of a plan that cannot be met.

**Occupancy is a constraint, not an output to maximise.** Sustained occupancy above
about 85% drives burnout and attrition, and attrition raises AHT (new agents are
slower) and volume (worse resolutions cause repeat contacts). A staffing level
that hits the service level at 92% occupancy is not efficient, it is a plan to
lose staff. The tool warns above 85%; treat that as infeasible rather than tight.

**AHT must include after-contact work.** Wrap-up, notes, follow-up tasks. Excluding
it understates load by 10–20% and the error compounds through every interval.

## The assumptions, and when they break

Erlang C is the industry standard and it is **wrong in specific, knowable ways**.
The script reports these on every run rather than presenting a clean number.

| Assumption | Reality | Consequence |
| --- | --- | --- |
| No abandonment — everyone waits forever | Customers hang up | **Over-states** staff needed, often 5–15% at long waits |
| Poisson arrivals | Marketing sends and outages create correlated bursts | Under-states peak requirement |
| Single skill, one pool | Skills-based routing fragments the pool | Under-states requirement; small pools are much less efficient |
| One contact per agent | Chat has concurrency | Erlang C does not apply unmodified |
| Infinite queue, no balking | Queues are capped; callers get busy signals | Distorts both directions |
| Stationary within the interval | Volume ramps inside a 30-minute block | Understates the within-interval peak |

**Skills-based routing deserves emphasis.** Erlang is superlinear in pool size:
one pool of 40 needs fewer agents than four pools of 10 at the same service
level. Every skill split costs efficiency. If a plan keeps missing despite
correct arithmetic, over-fragmented routing is a leading suspect.

## Channel-specific guidance

**Voice** — Erlang C works, with the caveats above. If you have abandonment data,
Erlang A is a better fit and will usually tell you that you need fewer agents.

**Chat and messaging** — concurrency breaks Erlang C. The script divides required
capacity by concurrency as an approximation, and says so. The real problem: **AHT
per conversation rises with concurrency, non-linearly**. An agent handling three
chats does not handle each as fast as one. Measure your own AHT at each
concurrency level from your own data; assuming it is constant is where chat
staffing models go wrong. For high concurrency, simulation beats any closed form.

**Async (email, tickets)** — not a queue-wait problem at all. There is no
"answered within 20 seconds"; there is a backlog and a turnaround promise. Use
Little's Law: `L = λW`. The two things that matter are whether throughput exceeds
arrivals (if not, the backlog grows without bound and no service level is
achievable) and how much extra capacity clearing an existing backlog needs on top
of steady state. The script's async mode covers steady state and says explicitly
that it does not cover backlog recovery.

## Present results to the user

1. **Rostered headcount, not productive headcount.** The productive number is an
   intermediate result; quoting it as the answer under-staffs by ~40%. State the
   shrinkage assumption alongside it.
2. **The marginal-agent table.** Where the service-level curve flattens is the
   real decision, and it is usually more informative than the single solved
   number.
3. **Occupancy, with a verdict.** If it is above 85%, say the plan is not
   sustainable rather than reporting it neutrally.
4. **Which assumptions this scenario violates.** Pass through the script's
   caveats. A staffing number without them invites false confidence — especially
   the abandonment caveat, which usually means the true requirement is lower.
5. **Forecast error separately from staffing.** If the forecast has 15% WAPE, the
   staffing precision is theatre. Report the forecast error next to the headcount
   so nobody treats a ±1 agent difference as meaningful.
6. **What would change the answer most.** Usually AHT, shrinkage, or routing
   fragmentation — not the queueing model. Say which lever is worth pulling.

## Troubleshooting

**We staff to plan and still miss service level** — check, in order: shrinkage
understated, AHT excluding after-contact work, skills-based routing fragmenting
the pool, and intraday peaks inside the scheduling interval.

**The model says we need fewer agents than we have and service is fine** —
plausible; Erlang C over-states when abandonment is material. Validate against
actuals before cutting.

**Volume forecast is good, daily total is right, service level swings wildly** —
you are forecasting at the wrong granularity. Forecast per interval.

**Occupancy is always above 90%** — you are structurally understaffed, and the
attrition it causes will make it worse. This is a headcount problem, not a
scheduling problem.
