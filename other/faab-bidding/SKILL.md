---
name: faab-bidding
description: This skill should be used when the user asks "how much should I bid", "what's a fair FAAB bid", "size my bid", "blind bid amount", "how much of my budget is he worth", "should I use my waiver priority on him", or wants to know what a waiver claim is worth. Sizes blind FAAB bids and advises when to spend rolling waiver priority. Not for choosing which players to target (waiver-wire waiver-scan), auction draft bidding (draft-strategy live-draft-assistant), or browser execution (roster-ops submit-waiver-claim).
---

# Waiver Bid Sizing

Produce a specific number, not a range and a shrug. Bids are a function of four things: what class of player this is, how contested the claim will be, how much budget remains against how many chances remain, and what this league actually pays.

## Step 1: Load context

Read `leagues.md` from the project root first — the fields that matter here are the waiver system (FAAB, continual rolling priority, weekly reverse-standings priority, or a hybrid with FCFS phases), league size, scoring (superflex especially), and playoff weeks. If the file is missing or blank, ask for them and suggest running `fantasy-league-setup:league-config`. If more than one league is defined, use the one marked `(default)`.

Then ask for: **remaining budget or current claim priority**, the target player, and — highest leverage — **recent winning bids or claim results in this league** (most platforms show a transaction/bid history page). Also ask whether $0 bids are allowed, whether the platform processes claims **conditionally** (only one of your claims can win) or **independently** (every winning claim processes, so three wins can drain the budget), and whether post-waiver players become FCFS free agents immediately or after a second lock.

For any injury- or demotion-driven role change, pin the advice to an **as-of** timestamp and cite the evidence used. Before recommending a major bid, all-in priority burn, or a cut needed to fund the move, confirm both:

- An **official status change**: team transaction, practice report, inactive list, coach quote, or platform status.
- A **second credible source** confirming the role impact: beat reporter, national news desk, or depth-chart/practice report follow-up.

If that verification is missing or conflicting, keep the recommendation **provisional**: lower the aggression, avoid destructive cuts tied only to the rumor, and say to wait for waivers to process or for the next official report.

**Live platform source routing.** Honor a browser the user explicitly names. If `leagues.md` records a Preferred browser, use that when it has a signed-in session for the platform. Otherwise use any authenticated browser the current assistant already has. For Yahoo league data, prefer an authenticated browser over a connector. If a Yahoo connector returns `403`, `unauthorized`, or an equivalent authorization failure, do not retry it during the same task. For non-Yahoo platforms, use a purpose-built connector when it is available and returns complete current data; otherwise use the browser. Read league rosters, the free-agent pool, standings, transaction history, and any rankings site directly instead of making the user paste them. Timestamp live data and name the source. The session rules from `roster-ops` apply unchanged: the user's session is the auth; never ask for, read, store, or type credentials; use the visible UI rather than platform endpoints; and stop and hand back on any login, 2FA, captcha, consent, or unusual-activity screen. If no usable live source exists, state the access gap and do not fabricate league-specific analysis.

**This skill is read-only.** Reading a page needs no confirmation, but never click anything that changes a roster, files a claim, or sends an offer from here — that is what the `roster-ops` skills and their confirmation gates exist for.

## Step 2: Classify the player

Denominate baselines as a share of **remaining** budget, not the season-starting budget. Remaining budget is what you actually have to allocate, and it keeps the advice correct late in the season when the starting figure has become meaningless.

| Class | Definition | Baseline (% of remaining) |
|---|---|---|
| League-winner | A season-altering role opened: IR/season-ending injury ahead of them, or a permanent depth-chart change. Every-down workload. | 55–85% |
| Season-long starter | Weekly startable role, not a workhorse (new WR2 role, committee lead) | 15–30% early; 25–45% from week 10 |
| Useful depth / insurance | Bench piece, bye coverage, speculative upside | 3–8% (a high-leverage handcuff inheriting a concentrated workload: 8–15%, regardless of who owns the starter) |
| Lottery stash | Role might materialize later | 1–3%, and only if bench space is genuinely free |
| Streamer | One-week DST/K/TE/QB matchup play | **$0 in $0-bid leagues; otherwise league minimum + $1, in absolute dollars** |

Two notes on the table:

- **Duration, not just quality, sets the class.** The classic FAAB error is paying league-winner money in week 1 of an injury for a backup whose starter returns in three weeks. "Multi-week" must mean season-altering to qualify for the top class.
- **Streamers and lottery tickets are absolute-dollar bids, not percentages.** In a $1,000 league, 3% of remaining is $30 for a one-week defense that will be free again in seven days. Only the top three classes scale with budget size.
- **Superflex changes everything at QB.** A startable quarterback hitting waivers in a superflex league is league-winner class, never a streamer.

## Step 3: Count credible rivals — this sets the number

FAAB is a **first-price sealed-bid auction**. You do not need to bid your valuation; you need to beat the highest opposing bid. So the question is not "how aggressive is my league" but "how many teams will credibly bid on *this* player."

For each rival ask: (a) do they have this roster hole, (b) do they have meaningful budget or a better claim position left, (c) have they bid or claimed aggressively before?

- **0–1 credible rivals** → bottom of the class range.
- **2–3** → middle.
- **4+** → top of the range or above it.

Rostered percentage is a useful proxy for how many managers have noticed a player at all, but league-specific behavior beats global popularity every time.

Layer the league's own history on top **non-parametrically**: start from the **75th percentile of this league's observed winning bids for comparably contested adds**, matching on how contested the claim was rather than on class label. Then beat the **top close comp that matters**, plus the binding round-number cluster, by $1-2. Do not apply a uniform multiplier to the whole table — real markets bid up the top disproportionately while streamer prices stay pinned at the floor.

## Step 4: Budget discipline

- **Do not decay bids as the season shortens.** Unspent FAAB is worth exactly zero in January, and prices in most leagues *rise* as a share of remaining budget in weeks 9–13 when managers dump budget before the playoffs. A contender should plan to finish the season at or near $0.
- **Opportunity cap**: default guardrail is `remaining budget / expected remaining opportunities`, estimating roughly one starter-class-or-better add per 3–4 remaining weeks. This is a planning tool, not a veto: a verified league-winner with a durable role can justify exceeding it, especially late.
- **Reserve**: while a minimum bid exists, keep $1 per remaining waiver week so a week-15 injury doesn't end the season with an unusable roster. Drop the reserve to $0 once the playoff roster is set.
- **Do not assume eliminated teams stop bidding.** Consolation prizes, last-place penalties, keeper value, weekly high-score awards, and ordinary competitive integrity can all justify continued claims. Model their stated incentives and league rules rather than assigning them a blanket $0 strategy. If the league allows FAAB trading, mention it only when a legal, self-interested trade exists — never as an automatic transfer to a contender.

## Step 5: Pick the number

- **Beat the maximum, not the average.** When observed comps span a range, bid above the *top* of it. Matching the middle of a two-point range is a coin flip.
- **Break round numbers.** Field bids cluster hard at 10/15/20/25 and at 25%/50%. Bid $1–2 above the *binding* cluster — the one your bid must clear — never a multiple of 5.
- **Ties go to waiver priority** in most leagues, which is the real mechanical reason this works. A team with poor priority (usually the league leader) must bid *above* a likely tie, not at it. Confirm the league's tiebreaker; it is worth $1.
- **$0-bid leagues**: file $0 claims freely on marginal players and use `minimum + $1` only when the player is enough of a streamer or stash that you actually care about winning him.
- **Consider waiting.** In most leagues an unclaimed player becomes a free agent 24 hours after waivers process. For low-rostered speculative adds, waiting costs $0.
- **Multiple targets**: with conditional claims, file all of them aggressively since only one can hit. With independent processing, cap the sum at what the budget survives.

**Regret is asymmetric — shade up, not down.** Standard auction theory says shade your bid below your valuation. FAAB inverts this: overpaying burns optionality you do **not** recover, but losing the player costs the player forever, possibly to the rival you're chasing. Losing a league-winner by $2 is often the expensive mistake; just be honest that the extra $10 is gone once you spend it.

## Priority and hybrid waiver systems

Identify the exact mechanic before advising:

- **Continual rolling priority (reset after use)**: no dollars involved; priority is a depleting asset that resets to last after a successful claim. Spend it only on a player who would start for you or who is a verified league-winner-class stash.
- **Weekly reverse standings / recomputed priority**: today's priority is less scarce because it resets from standings each cycle. Be more willing to use it on a real starter or short-term fix, especially if the user is near the bottom and likely to climb back up the order next week.
- **FAAB with post-waiver FCFS**: bid only on players worth beating the room for; leave low-signal streamers for the FCFS window when possible.
- **Hybrid systems**: some leagues run waivers first, then FCFS, or combine FAAB with rolling tiebreakers. State which phase the advice assumes before naming the number.

In all priority formats, if the claim is driven by unverified injury chatter, downgrade to a provisional recommendation and do not tell the user to burn the top claim until the official status plus second source are in hand.

## Worked example (fictional)

"Couch Commissioners," $200 season budget, **$124 remaining**, week 8 with 6 weeks left. **As of Tuesday 9:00 AM ET**, the fictional team's official transaction log places the starter on IR and an independent beat report confirms Okafor took the lead first-team work; the platform budget and bid history were refreshed at the same time. Target: RB Silas Okafor. If either role source were missing, the major bid below would remain provisional rather than executable advice.

- **Class**: the starter is on IR, so the role is season-altering — this is the top of *season-long starter* and arguably league-winner. Comps confirm it: the league's last two lead-back rentals cleared at $41 and $37. Starter band on $124 remaining = $19–56 (25–45%, week 10 window approaching).
- **Credible rivals**: four teams have an RB hole and more than $40 left. That's 4+ → top of the range or above.
- **League history**: comps span $37–41; the 75th percentile of comparably contested adds sits around $40, so the actionable floor is "beat $41 and the $40 cluster."
- **Opportunity cap**: 6 weeks ≈ 2 more starter-class adds → $124 / 2 = $62. Not binding, and a verified every-down role could justify pushing through it anyway.
- **Reserve**: 6 waiver weeks left → hold $6. Ceiling $118.
- **Cluster**: field will cluster at $35 and $40; the binding cluster is $40.

> **Bid $42.** It clears the $40 cluster and the $41 comp, sits inside the starter band, respects the $62 opportunity cap, and leaves $82. Four credible rivals is exactly the case for the top of the range — and if you lose at $42, don't chase him at a worse price next week.
