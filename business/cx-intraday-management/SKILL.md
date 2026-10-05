---
name: cx-intraday-management
description: Use to recover a day in real time when volume, handle time or availability diverge from plan — reforecasting decisions, break moves, overtime, callbacks and skill flex without burning tomorrow. Trigger for "intraday management", "real-time reforecast", "we are underwater at 11am", move breaks or lunches, call people back in, flex agents between queues, ride out the spike, or when the WFM plan is wrong before close of business.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Intraday management

The forecast and schedule were built yesterday. Today is different.

**The common failure is treating intraday management as a staffing calculator rerun every
hour.** Real-time reforecasting is useful; constant replanning is not. Most days are
recoverable with moves you already have — break placement, skill flex, a short callback
block — if you know when to act and when to absorb variance. This skill sits on top of
volume forecasting and shrinkage: it assumes you already know required versus scheduled by
interval, and asks what to do when that gap opens mid-day.

## The decision frame: reforecast, flex, or ride it out

Work in 15–30 minute intervals, not daily totals. At each checkpoint ask three
questions in order:

1. **Is the gap structural or noise?** A single hot interval after a known event (email
   send, outage) is different from a sustained miss across three consecutive intervals
   with no explanation.
2. **Is the constraint people, skill, or handle time?** Understaffing and skills mismatch
   look identical in aggregate occupancy. Handle-time inflation looks like understaffing
   but flexing agents will not fix it.
3. **Can you recover before the damage compounds?** Queue wait is non-linear. A 10-minute
   delay at peak costs more service level than the same delay at trough. Late recovery
   still leaves repeat contacts and abandonment you cannot undo.

| Signal | Likely cause | First lever |
| --- | --- | --- |
| Volume up, AHT stable, occupancy high in one queue | Understaffed interval or skill gap | Skill flex, break move, callback |
| Volume stable, AHT up, occupancy high everywhere | Process change, tooling, training gap | Do not flex — fix root cause or defer non-urgent work |
| Volume down, occupancy low, service still missed | Wrong skill mix or routing fragmentation | Flex by skill, not headcount |
| Spike then fast decay | Event-driven burst | Ride it out if queue clears within patience window |

**Ride it out** when: the miss is one or two intervals, abandonment is not accelerating,
and the scheduled cover returns before the next peak. Absorbing variance is cheaper than
over-correcting.

**Reforecast** when: actual volume or AHT has diverged enough that the remaining day's
requirement changes materially — typically after a sustained miss, a confirmed event, or
when you have lost a block of shrinkage (outage, mass absence). Update the *remaining*
day, not the whole week.

**Flex** when: people exist but are in the wrong place or state — the fastest recovery
lever and the one with the lowest tomorrow-cost if used surgically.

## Levers, in order of tomorrow-cost

Apply the cheapest lever that closes the gap. Escalate only when the prior lever failed
or the gap is too large.

### Break and lunch moves

Shift non-productive time out of saturated intervals into troughs. This is often the
first move and the least destructive.

Rules:

- **Never stack breaks into a deeper trough that already has cover risk.** Moving lunch
  from 12:00 to 13:00 helps only if 13:00 is genuinely lighter.
- **Supervisor and team-lead cover is not free capacity.** Pulling leads onto the phones
  trades intraday recovery for coaching and escalation capacity later the same day.
- **Communicate before moving.** Agents rearranging childcare or appointments will not
  flex again tomorrow if you move breaks without notice.

### Skill flex

Move agents qualified on a secondary skill into the queue that is bleeding. Effective
when routing fragmentation created a small-pool problem, not when total headcount is
short.

Watch for:

- **Flexing into a queue whose AHT you have not measured at flex volume.** Quality and
  handle time often rise when agents are on unfamiliar work.
- **Draining the donor queue.** Flex is a loan, not a gift. Monitor the queue you took
  from within one interval.

### Callback and voluntary overtime

Call back agents who are off-shift or offer voluntary overtime for defined blocks — usually
the trough before the next peak or the final push to close backlog.

Rules:

- **Time-box it.** "Two hours from 15:00" not "stay until we clear it." Open-ended
  overtime burns the next day's adherence and sickness.
- **Prefer callback of people already ramped on the skill.** Overtime on a novice queue
  raises AHT for hours after they leave.
- **Track cumulative weekly overtime by person.** Intraday heroics that repeat become
  structural understaffing with a burnout bill.

### What not to do mid-day

These feel decisive and usually make tomorrow worse:

- **Changing service-level or response-time targets** to green the dashboard. You have
  not improved service; you have stopped measuring the miss. Fix capacity or accept the
  miss explicitly.
- **Mass mandatory overtime** to save one day when the plan was wrong all week. You pay
  twice: today's premium and tomorrow's absence.
- **Raising chat concurrency or shrinking ACW** without a quality check. Both look like
  free capacity and show up as repeat contact within 48 hours.
- **Publishing a new forecast every hour** to the floor. Agents stop trusting the plan;
  supervisors stop executing the one they have.
- **Opening a hiring conversation intraday.** Hiring is seasonal and structural; it is
  not an intraday lever.

## The intraday rhythm

A workable cadence, adjusted to your operation:

| Time | Action |
| --- | --- |
| Opening + 30 min | Compare actual to forecast volume and AHT by interval; confirm shrinkage (who is actually available) |
| Pre-lunch | Gap profile for morning peak; decide break moves before the midday trough becomes a second peak |
| Mid-afternoon | Reforecast remaining day if sustained miss; activate callback only if gap persists past next interval |
| Pre-close | Decide deferrals explicitly (what carries to tomorrow) rather than letting backlog accrue silently |

Name an owner for each lever — WFM, ops lead, routing admin — before the day starts.
Intraday arguments about who can move breaks cost more than the breaks.

## Traps

- **Fixing volume when AHT moved.** Reforecasting contacts without checking handle time
  reproduces the same miss.
- **Chasing abandonment after the fact.** Abandonment-censored arrivals make the next
  interval look lighter than demand was. Do not cut staff because the queue emptied via
  hang-ups.
- **Flex without updating the schedule record.** Adherence reporting will show a miss
  that was intentional; if the schedule was not updated, you cannot learn from it.
- **Recovering service level while backlog grows** on async channels. Voice can look
  recovered while email waits spike — watch both clocks.

## Present results to the user

1. **Gap diagnosis by interval** — volume, AHT, occupancy and skill view — naming people
   versus skill versus handle time as the constraint.
2. **Recommendation: ride out, reforecast remaining day, or flex** — with the evidence
   threshold that triggered it.
3. **Specific lever plan** — break moves, flex pairs (from/to queue), callback block
   with time-box — in execution order.
4. **Explicit do-not-do list** for this scenario — especially target changes and
   open-ended overtime.
5. **Tomorrow cost** — what was borrowed (overtime hours, flexed queues, deferred backlog)
   and what must be repaid in the next schedule.
6. **Assumptions not verified** — e.g. flex AHT, event duration — and what to watch in
   the next interval to confirm.
