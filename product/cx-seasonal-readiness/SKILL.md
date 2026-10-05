---
name: cx-seasonal-readiness
description: Use to plan and run peak-season support — what to freeze, pre-stage and measure daily so volume spikes do not become quality and attrition crises. Trigger for "peak season readiness", "holiday staffing plan", "Black Friday prep", freeze policy or KB changes before peak, pre-hire and ramp for surge, daily war room metrics, peak post-mortem, or when last year's peak broke SLA and attrition.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Seasonal readiness

Peak season is not a bigger version of a normal week. It is a different operating mode
where small mistakes compound across every interval for six weeks.

**The common failure is staffing up while everything else stays live.** New macros ship
the week before Christmas, policy changes land during the surge, training stops because
everyone is on the phones, and the war room watches only volume while quality and
attrition detonate quietly. Readiness is three lists — freeze, pre-stage, measure — plus
an honest after-action so next year is not a replay.

## What to freeze (and for how long)

During peak, **change is a demand multiplier**. Every policy tweak, KB rewrite, macro
edit and routing experiment creates handle-time inflation and repeat contact that your
volume forecast did not include.

Freeze window: from **pre-peak staging complete** until **post-peak stabilisation** —
typically one to two weeks before the known start until volume returns to baseline band.
Adjust to your calendar; the principle is that freeze starts before customers feel the
surge, not on day one of it.

| Category | Freeze | Exception process |
| --- | --- | --- |
| Policy and refunds | No substantive changes | P1 legal/regulatory only; document expected volume impact |
| Knowledge base | No structural rewrites; typo fixes only | Single owner approves; measure deflection impact separately |
| Macros and templates | No new variants; bug fixes with before/after AHT check | Version control; rollback plan required |
| Routing and IVR | No experiments | Outage-driven changes only |
| QA rubrics | No criterion changes | Calibration holds; do not re-baseline scores mid-peak |
| Marketing and product comms | Coordinate sends with WFM | Pull forward or push back; never "surprise" the queue |

**Freeze is not stagnation.** Build the backlog of improvements in a queue for
post-peak. The discipline is sequencing, not stopping work forever.

## What to pre-stage

Staging happens **weeks before**, not the night before. Minimum set:

### Capacity

- **Hire and ramp on your own measured curve**, not "full productivity on day one." Count
  tenure mix in the staffing model; see onboarding ramp data if you have it.
- **Cross-skill the right direction** — train peak queues from stable ones before peak,
  not during it.
- **Confirm shrinkage by interval for the season** — holidays cluster; sickness patterns
  shift; planned leave must be in the schedule before the forecast is signed off.
- **Vendor and BPO surge clauses** — notice periods, skill mix, quality gates — executed
  in writing, not assumed.

### Content and tooling

- **Peak-specific KB articles and macros** drafted, reviewed and published before freeze.
  Tag them so they can be retired after.
- **Known-issue list** from product and engineering — what will generate contacts even if
  marketing is quiet.
- **Escalation paths and on-call roster** for peak — named backups, not "whoever is
  online."

### Event calendar

Maintain a **single calendar** product, marketing, billing and ops share: sends,
releases, price changes, billing runs, regulatory deadlines. Forecast errors at peak are
usually missing events, not bad time-series models.

## Daily war room: what to measure

A 15–30 minute stand-up during peak, same time every day, same deck. **Do not add
metrics because anxiety is high.** Six to eight numbers, owners attached.

| Metric | Why it is on the wall |
| --- | --- |
| Forecast vs actual volume by interval | Early miss detection; feeds intraday management |
| Forecast vs actual AHT | Catches macro/policy drift despite freeze |
| Service level or backlog age by channel | The customer-facing outcome |
| Occupancy by queue and skill | Separates understaffing from wrong mix |
| Adherence and shrinkage actuals | Catches schedule integrity before it compounds |
| Quality sample or critical-error rate | Peak is when shortcuts show up |
| Repeat contact or re-open rate | Leading indicator of tomorrow's volume |
| Attrition signals — OT hours, absence, schedule swaps | Peak burns people; watch the leading edge |

**Decisions the war room is allowed to make:** intraday flex, break moves, callback
blocks, defer non-peak work, escalate hiring or vendor surge. **Decisions it is not
allowed to make:** change targets, ship policy, rewrite KB, open routing experiments.

Log decisions with owner and expected effect. Post-peak review reads this log, not
memory.

## Running the peak week

- **Protect training and coaching minimums** even at highest occupancy — cutting them
  raises AHT for the rest of the season.
- **Single comms channel for floor** — one intraday update source; rumours cost adherence.
- **Explicit deferral list** for non-urgent work (projects, optional callbacks, low-severity
  tickets) with approval threshold.
- **Executive escalation path** when freeze exceptions are requested — default is no.

## After-action

Within two weeks of return to baseline, before teams scatter:

1. **Forecast accuracy** — WAPE by interval and by day; which events were missing from the
   calendar.
2. **Staffing model** — where requirement was wrong (volume, AHT, shrinkage, skill mix).
3. **Freeze discipline** — what changed despite freeze and what it cost.
4. **Quality and repeat contact** — lagged by one to two weeks; peak damage often shows
   after volume drops.
5. **Attrition and absence** — overtime hours, schedule change count, post-peak sick spike.
6. **Customer-visible incidents** — SLA breaches, social spikes, executive complaints.

Turn findings into **dated actions** for next season: hire date, freeze start, calendar
owner, vendor notice. "We should plan earlier" is not an action.

## Traps

- **Staffing to daily totals** when peak is interval-shaped — mornings drown while
  afternoon reports "fine."
- **BPO as infinite flex** without quality gates — bad peak handling becomes repeat
  contact on your in-house team.
- **Deflection projects mid-peak** — bot and IVR changes fail loudly when volume is
  highest.
- **Copying last year's headcount** without checking product, channel mix and tenure
  composition — the ratio moved.
- **Skipping after-action because everyone is tired** — that is when memory is freshest
  and the organisation will forget by Q2.

## Present results to the user

1. **Peak calendar** — start, end, freeze window, known events — with owners.
2. **Freeze register** — what is locked, what exceptions exist, who approves.
3. **Pre-stage checklist** — capacity, content, tooling, vendor — with status and gaps.
4. **War room metric set** — the six to eight daily numbers, thresholds and owners.
5. **Intraday authority matrix** — which levers ops can pull without executive sign-off.
6. **After-action template** — questions and data sources — scheduled before peak starts.
7. **Risks that could not be quantified** — and what to watch on day one.
