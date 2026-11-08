---
name: seed-updates
description: >-
  Investor Updates. Writes the monthly investor update that keeps investors
  warm: a TL;DR, every metric with its month-over-month growth, highlights,
  lowlights, the asks, and the runway worked out from your cash and your
  average net burn. A short "prospects" version goes to warm investors who
  said "not now": the headline numbers, two highlights, the raise and an
  opt-out line, with no cash or runway. Reads seed/metrics.json (and
  seed/config.json for the founder and the raise), writes
  seed/updates/YYYY-MM.md. Never sends anything on its own. Use when the
  user says "write my investor update", "monthly update", "update my
  investors", "keep investors warm", "follow up with investors who said not
  now", "what's my runway", "MoM growth", or at the start of each month.
argument-hint: "[write --month YYYY-MM] [--to prospects]"
---

# seed-updates

Investor Updates is the habit that makes the next round easier. Once a month,
a short, honest email: what the numbers did, what went well, what did not,
what you need, and how long the money lasts. Investors who already backed you
can help when they know the asks; investors who said "not now" watch the line
go up and come back. This skill keeps the numbers in one file, works out the
growth and the runway exactly, and writes the update in the standard shape.
It writes. It does not send: the founder reads it and says yes first.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/update.py" init                                 # seed/metrics.json from the example
python3 "${CLAUDE_SKILL_DIR}/update.py" add --month 2026-12 --set revenue=7875 --set walks=2100 --cash 160000
python3 "${CLAUDE_SKILL_DIR}/update.py" add --month 2026-12 --highlight "..." --lowlight "..." --ask "..."
python3 "${CLAUDE_SKILL_DIR}/update.py" write --month 2026-11                # seed/updates/2026-11.md
python3 "${CLAUDE_SKILL_DIR}/update.py" write --month 2026-11 --to prospects # seed/updates/2026-11-prospects.md
python3 "${CLAUDE_SKILL_DIR}/update.py" write --stdout                       # the latest month, printed only
```

Other flags: `--dir PATH` (default `./seed`), `add --money-in N` (funding
that arrived that month, which is not burn), `add --net-burn N` (override),
`add --tldr TEXT` (your own TL;DR line), `init --force`.

## What it reads and writes

| file | what |
| --- | --- |
| `metrics.example.json` (this folder) | the Leashly pilot example `init` copies |
| `seed/metrics.json` | your metrics (key, label, unit: usd, count or pct), the `headline` three, and one entry a month: `values`, `cash` at month end, `money_in`, `highlights`, `lowlights`, `asks`, optional `tldr` |
| `seed/config.json` | from `/seed-plan`: the company name, the founder's name for the sign-off, the raise for the prospects version |
| `seed/updates/YYYY-MM.md` | `write`: the investor update |
| `seed/updates/YYYY-MM-prospects.md` | `write --to prospects`: the short version for "not now" investors |

## The method

- **Growth**: (this month minus last month) / last month, one decimal, for
  money and counts ("up 23.9% from $5,325"). Percent metrics change in
  points ("down 0.4 pts from 2.8%"). A metric with no last month says "new
  this month".
- **Net burn**: last month's cash + money that came in this month minus this
  month's cash. A raise landing is not negative burn: record it as
  `money_in`.
- **Runway**: this month's cash / the average net burn of the last 3 months
  (fewer if that is all there is), one decimal. "To around" = this month
  plus the runway, rounded up to a whole month. If the cash is not running
  down, it says so instead of a number.
- **TL;DR**: your own line if the month has `tldr`, otherwise the three
  headline metrics with their growth and the runway.
- **Honest by default**: a month with no lowlights, no highlights or no asks
  is flagged. Lowlights build trust; asks get you help.
- **Prospects**: the headline numbers and the top two highlights, the raise
  from config.json, "Hi {first_name}," for you to fill in per investor, and
  the opt-out line: "Not a fit any more? Reply 'no' and I won't send these
  again." Cash, burn, runway, lowlights and asks stay out on purpose.

## Steps

1. First time: `update.py init`, then replace the Leashly metrics with the
   five or six numbers this company tracks every month. Keep them the same
   month to month.
2. Each month, ask the founder for the month-end numbers, the cash in the
   bank, any money that came in, and three highlights, the lowlights and up
   to three asks. Record them with `update.py add`.
3. Run `update.py write --month YYYY-MM`. Read the TL;DR, the numbers and
   the runway back to the founder. Fix wrong numbers in seed/metrics.json and
   write again.
4. For investors who replied "not now" (in `/seed-closer`'s
   seed/pipeline.json, status passed with a "not now" reply), run `write
   --to prospects`. Never send it to anyone who said no, opted out or
   bounced.
5. Sending: show the founder the recipients and the full email, and wait for
   a clear yes for that batch. Then send it through the founder's own Gmail
   connector (or save Gmail drafts if they prefer). Fill in {first_name} for
   each prospect. Nothing goes out on its own.
6. Hand off: `/seed-closer` logs any reply and books a call; `/seed-model`
   updates the assumptions when real numbers drift from the plan.

## Example: the reel

Leashly (fictional) runs a one-city pilot before the seed. November 2026 in
seed/metrics.json: revenue $6,600, 1,760 walks, 210 active owners, $44,000
GMV, 31 walks saved by a backup walker, 2.4% walker cancellations, $177,800
cash at month end (October: $196,500; September: $214,000). `update.py write
--month 2026-11`:

```
Subject: Leashly investor update: November 2026

**TL;DR:** Revenue $6,600 (+23.9% MoM), walks completed 1,760 (+23.9%), active owners 210 (+22.8%). Runway 9.8 months.

- Revenue: $6,600, up 23.9% from $5,325
- Walker cancellations: 2.4%, down 0.4 pts from 2.8%
...
Cash at the end of November: $177,800. Net burn this month: $18,700. Average net burn over
the last 2 months: $18,100 a month, so the cash lasts about 9.8 months, to around Sep 2027.
```

The net burn is $196,500 - $177,800 = $18,700 in November and $214,000 -
$196,500 = $17,500 in October; the average is $18,100, and $177,800 /
$18,100 = 9.8 months. The prospects version opens "Hi {first_name}," and
ends: "We are raising a $1.5M seed (post-money SAFE). If the timing is
better now, would a 20-minute call be useful?"

## Rules

- Never send on the founder's behalf without a yes for that batch, and only
  through their own account. Respect every "no" and opt-out forever.
- Real numbers only. Never round a number up, drop a bad metric or skip a
  lowlight to make a month look better.
- Runway is arithmetic on the founder's own cash and burn, not a promise.
  Not investment advice.
- The prospects version never shares cash, burn or runway.
