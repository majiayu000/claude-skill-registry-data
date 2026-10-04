---
name: token-watch
description: Use when running the scheduled fleet token check, when asked how the quota is trending, when asked the status of the Claude accounts, or before deciding whether to rotate pools.
user-invocable: true
---

# Token Watch

**The cadence lives on the schedule of the `Token watch` row of the Team Lead board,
and nowhere else. Read it there; do not trust a time written in a file — including this
one.** The user re-armed it on 2026-09-19 and four files in this repo still carried the
superseded 08:07/13:07/18:07 afterwards.

**"Every 3h" is a paraphrase of that re-arm, not the rule.** The armed calendar is a list
of fixed times and its gaps are not uniform — measured 2026-09-21, the overnight gap was
6h against 3h for the other six. The board's own stall detector derived the interval the
same way and filed a false "has not succeeded in 4h" against a run that was on time.
**Root-caused 2026-09-22 and a fix is in flight** — the scheduler took a calendar rule's
interval as the gap between the next two occurrences plus 1h slack, so at 04:01 it measured
06:00→09:00 and called the on-time 00:05 run stale. Two tickets are building against it. So
treat a stale or stall signal on this row as *probably* spurious until that ships, and then
stop: once it does, a stale signal here means something, and a skill still saying otherwise
is the worse failure.

The contract is `docs/process/token-control.md`
— tiers, rotation policy, and the account-switch runbook live there and are not
repeated here. This skill is the procedure and the **output shape**.

## The output is a table, not an essay

The user, 2026-09-09: *"Your token watch is not decipherable."* The pass before that
had reported one pool live, quoted two from a ledger, and answered "how am I
trending" with a single-pool pace multiple across nine prose bullets.

**A pace multiple on the active pool is not a trend when the estate holds three
pools with staggered resets.** Report the estate, then the one call.

- **In-session: the ESTATE table, then at most three lines** — the measured
  points/h, the gap-or-handoff verdict, and anything that needs the user. Nothing
  else unless he asks.
- **Trend log: ONE line.** `date time PT · pool · all% (Fable%) · elapsed% ·
  verdict`. A finding that is genuinely new gets one sub-bullet. The long-form
  entries in that file are history, not the format to copy.
- **Say what to do, not what the number is.** "Rotate now or expect a hard stop
  Thursday midday" is answerable in one word; "the pool is at 38%" is not.

## Procedure

1. **Establish the account live** — `~/.claude.json` → `oauthAccount.emailAddress`,
   plus a `/usage` week bar with a distinct %/reset. Same reset = same pool.
   **Never trust a written pool figure, including one asserted in the cron prompt.**
2. **Read `/usage` off an idle peer's pane.** Sentinel-test first: send one
   character and read back whether it **replaced** or **appended**. Text on the
   `❯` line is usually a ghost over an empty editor. Inspect the palette before
   pressing Enter — `/` opens it and a stray Enter fires the highlighted entry.
3. **Record BOTH meters**, week bar and session line:
   ```
   python3 scripts/fleet_budget_watch.py --record-meter <email> \
     --all-models <%> --fable <%> --resets <ISO> \
     --session-resets <ISO> --session-pct <%>
   ```
   The session reset is the window's **phase** and exists nowhere else; without
   it the watcher trails from run time and can only report an upper bound.
4. **Run the instruments, capturing the drift exit code directly** —
   `cmd > f 2>&1; echo $?`. Piping to `tail` reports tail's status and reads as
   clean. `fleet_budget_watch.py` (the estate panel + the binding 5h window),
   `fleet_burn_report.py`, `fleet_context_report.py`, `plugin_drift_check.py`.
5. **Append the one-line trend entry.** Tier 0 always, Tier 1 automatically,
   Tier 2 asks the user.
6. **First run after a weekly reset:** also run the end-of-week retro from the
   contract.

## Reading the estate panel

`fleet_budget_watch.py` prints every pool, not just the active one:

```
POOL                  USED  LEFT  FABLE  RESETS            RUNWAY  TRUST
pool-a@example.com     80%   20%   100%  Thu 09-10 17:59      ~9h  idle since read — a FLOOR
pool-b@example.com     38%   62%    43%  Fri 09-11 04:00     ~29h  live  <- ACTIVE
```

- **A stale reading is a bound, not a figure. Say "80% or worse", never "80%"** —
  an unlabelled number reads as measured. Keep saying this; the reasoning under it
  changed on 2026-09-17 and the phrasing did not.
- **The old reason — "an idle pool's meter can only RISE" — is FALSE, and believing
  it cost two hours at a wall.** The primary pool was read live at 100% (Fable
  84%) on 09-15 and read **82% (Fable 66%) at 13:40 on 09-17 with the same reset and
  no reset in between**, so it shed ~18 points while idle. At the 08:37 wall that
  morning I reported "nothing to rotate to" on the strength of two 100% floors; one
  of them had headroom the whole time.
- **So a 100% row is a claim about a moment, never a property of the pool.**
  **Re-read an exhausted pool before concluding the estate is empty.** A stale
  reading bounds nothing in the direction you need when the question is whether to
  rotate — it can be wrong high as well as low, and the panel cannot tell you which.
  The only cure is a live read, which costs one pane drive.
- **A reading taken while a pool was still active is an under-read**, because the
  pool kept climbing after it. Check `account_since` before quoting one.
- **Runway is measured off the active pool's own meter** — points GAINED since
  the stint began ÷ hours — not from tokens, and never `used% ÷ hours`. That
  assumes the pool was empty when the fleet arrived; a pool re-entered at 59%
  read as 5.05 pts/h against a real 1.7 and produced a false Tier 2 on 09-10. Never project multiple days off the current
  5h window: on a quiet morning it read a third of the sustained rate and
  projected 99h of runway against a real 29h.
- **A stale active reading makes the RUNWAY column a span, like `~2-16h`.** The high end
  takes the reading at face value; the low end carries it forward at the measured rate. Neither
  is the answer, and the width is the point — a wide span means go read the meter. On 2026-09-19
  this panel and the morning digest each silently picked one end off the same ledger entry and
  published answers **14 hours apart**.
- **A rate averaged across an idle stretch is not the rate for a busy one, and the reverse is
  equally wrong.** The 2.51 points/h measured over 23.5h on 2026-09-19 was 0.6 points/h across
  the last five of those hours, and under 0.78 overnight. Quote the window the rate came from
  every time you quote the rate.
- **The 5h window is a statement about the last five hours, in BOTH directions.** The
  skill has long warned that a quiet window under-reads; a busy one over-reads the same
  way, and that is the half that keeps costing a pass. Three consecutive runs in
  September 2026 printed BREACH while the same panel's own last-hour figure projected
  the window to single-digit percent, because the burst that caused the breach had
  already finished. **Read the last-hour line before you report the verdict** — when the
  two disagree, the backward-looking number is describing work that is over.
- **The GAP line is the finding.** Whether the active pool outlasts the next
  pool's reset, or dies before it and leaves hours to bridge.
- **Check the meters separately.** Blended and Fable exhaust independently, and
  an estate can be comfortable on one while having a single pool's worth of the
  other.

## What not to do

- **Don't quote the trend log or any written "current pool" figure.** Pull live.
- **Don't call a trending-to-100% pool Tier 2.** That is expected under
  burn-freely rotation. The *rotation* is the Tier 2 call, because it severs the
  claude.ai connector set fleet-wide.
- **Don't report a mid-work session over 300k as a lever.** No agent can
  self-compact — surface it.
- **Don't re-explain a standing drift or a known blocker every pass.** Note it
  unchanged in one clause.
- **Don't stay silent on an open Tier 2 call.** Re-ping every run while inside
  24h of its projected date — in-session above 24h, PushNotification inside it.
