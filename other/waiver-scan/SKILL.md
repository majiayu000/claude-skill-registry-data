---
name: waiver-scan
description: This skill should be used when the user asks to "work the wire", "who should I pick up", "scan the waiver wire", "best free agents for my team", "wire targets this week", "who's worth adding", "my guy got hurt, now what", "who replaces him", or "should I stream a defense". Ranks available players by fit with the user's actual roster holes rather than generic top-add lists. Not for bid amounts (waiver-wire faab-bidding), cut decisions (waiver-wire drop-candidates), weekly lineup calls (lineup-strategy start-sit), a combined weekly checklist (lineup-strategy weekly-briefing), or browser execution (roster-ops submit-waiver-claim).
---

# Waiver Scan: Fit Over Fame

Rank available players against **this roster's holes**, not a generic top-adds list. A backup RB one injury from a workload is worth more to a team with a thin RB room than the "consensus #1 add" WR is to a team already starting three good ones.

## Step 1: Load context

Read `leagues.md` from the project root first — the fields that matter here are scoring, starting slots, waiver system, playoff weeks, and any weekly acquisition cap. If the file is missing or those fields are blank, ask for them and suggest running `fantasy-league-setup:league-config`. If more than one league is defined, use the one marked `(default)`.

An acquisition cap changes everything downstream: where adds are limited, each claim must clear a much higher bar and churning streamers is off the table.

Pin time-sensitive recommendations to an **as-of** timestamp. When a player's value depends on an injury, benching, suspension, or activation, cite both the official status input and a second credible source before treating the role change as settled. If the evidence is incomplete, keep the ranking provisional and say the default action is to wait rather than force a move.

## Step 2: Get the two inputs

1. **The user's roster** — read from their platform if browser automation is available, otherwise pasted. Include the current week and any injury designations.
2. **The available player pool** — read the platform's free-agent list directly, or ask for a paste. Do not rely on one sort alone. Pull a broader sample: the best available players at each relevant position, plus views sorted by rostered%, recent usage or targets/snaps, projected points, and recent adds/drops if the platform shows them. A good fallback is 8-12 names per relevant position from multiple sorts, not just the global top 30 by rostered% or recent scoring. Without a pool, describe the *profile* to target ("your hole is RB depth — target any back whose starter just landed on IR") and ask for the list to name names.

**Live platform source routing.** Honor a browser the user explicitly names. If `leagues.md` records a Preferred browser, use that when it has a signed-in session for the platform. Otherwise use any authenticated browser the current assistant already has. For Yahoo league data, prefer an authenticated browser over a connector. If a Yahoo connector returns `403`, `unauthorized`, or an equivalent authorization failure, do not retry it during the same task. For non-Yahoo platforms, use a purpose-built connector when it is available and returns complete current data; otherwise use the browser. Read league rosters, the free-agent pool, standings, transaction history, and any rankings site directly instead of making the user paste them. Timestamp live data and name the source. The session rules from `roster-ops` apply unchanged: the user's session is the auth; never ask for, read, store, or type credentials; use the visible UI rather than platform endpoints; and stop and hand back on any login, 2FA, captcha, consent, or unusual-activity screen. If no usable live source exists, state the access gap and do not fabricate league-specific analysis.

**This skill is read-only.** Reading a page needs no confirmation, but never click anything that changes a roster, files a claim, or sends an offer from here — that is what the `roster-ops` skills and their confirmation gates exist for.

## Step 3: Diagnose roster holes

In severity order:

1. **Unfillable starting slot** — a bye, injury, or suspension leaves a required slot empty this week. Fix now.
2. **Weakest weekly starter** — the slot with the lowest expected points relative to positional average. This is the upgrade target.
3. **Missing insurance** — no viable backup behind a starter whose absence would zero a slot (usually RB).
4. **Bye-week wall** — a future week with 2+ starters out at one position. Fix 1–2 weeks ahead, not four.

## Step 4: Score each available player

**Opportunity outranks talent for in-season adds.** In order: depth-chart promotion (starter injured, traded, or benched), snap/route share trending up over 2+ weeks, red-zone and target share, and efficiency **last** — chasing one big game is how waiver budgets are wasted.

Before elevating an injury replacement to the top tier, verify the role change with an official status input plus a second credible source. If that is still pending, explicitly label the player a provisional target and avoid presenting him as a must-add over stable alternatives.

Concrete thresholds, since "trending up" is not actionable on its own:

- **WR**: route participation above ~70%, or a target share above ~20%.
- **RB**: snap share above ~60%, or clear goal-line work regardless of snaps.
- **TE**: route participation above ~65% — TE production is role-driven, so snaps matter more than matchup.

A player crossing these lines is startable regardless of name recognition; a famous player below them is not.

**Then weigh:**

- **Role match** — does this address hole #1 or #2, or add a redundant fifth WR? A candidate filling an unfillable slot beats a "better" player who would ride the bench.
- **The second-order add.** When a starter goes down, the whole league bids on the direct backup. The profitable claim is often the *complement* — the pass-catching back in a committee, or the WR3 absorbing vacated targets. Same information, a fraction of the cost. Always name this alternative when a headline injury happens.
- **Returning players.** One of the highest-value plays of the season is stashing a player the week *before* he's activated off IR, while the market still ignores him. Watch for practice-window openings and designated-to-return news.
- **Schedule** — for playoff-bound teams, weight the league's configured playoff weeks; for teams fighting for a spot, weight the next three weeks only.

## Step 5: Streaming (DST, K, and sometimes QB/TE)

Rank streamers by matchup, using inputs that actually predict:

- **The opposing offense's Vegas implied team total** is the single best one-number input for a defense. Low implied total, good stream.
- Then: opposing turnover-prone QB or a backup starting, opposing offensive-line injuries, home/away, and pass-rush matchup.
- For kickers: the kicker's own team implied total, plus dome or fair weather. Wind above roughly 20 mph is the one weather condition that reliably matters.

**Stream as a plan, not a reaction.** Look 3–4 weeks ahead and claim the defense with the best upcoming stretch *before* the market prices it, rather than paying up every week. Pair this with never rostering two defenses except for a pre-staged swap.

Tie the stream plan to the league's waiver mechanics: in FAAB or rolling-priority leagues, reserve claims for players whose edge survives the lock; in FCFS or hybrid leagues, many one-week streamers are better treated as post-waiver pickups than as primary claims.

## Step 6: Deliver ranked claims

Output a priority-ordered list: player, the hole he fills, the signal justifying him, and a priority note. Then hand off — for bid amounts run `waiver-wire:faab-bidding`, for who to cut run `waiver-wire:drop-candidates`, and to file the claim in the browser run `roster-ops:submit-waiver-claim`. If an analysis plugin is missing, do that analysis inline. If the execution plugin is missing, provide the clicks but preserve the transaction summary and explicit confirmation boundary; this read-only skill never files the move itself.

## Worked example (fictional)

"Mud Dogs," 12-team half-PPR. **As of Tuesday 9:00 AM ET in week 8**, the platform roster and free-agent pool are current. RBs are Tobias Renner plus two dart throws; WR room is strong; TE Oren Vasquez is on bye week 9.

Pool includes WR Deion Marsette (consensus top add, 22% rostered) and RB Silas Okafor (8% rostered). Okafor's promotion is verified by the fictional team's official IR transaction plus an independent beat-practice report that he took the lead first-team work; his 65% relief snap share is from the platform game log. Without both role sources, rank him provisionally rather than decisively first.

> 1. **RB Silas Okafor** — fills hole #3 (no RB insurance) and likely hole #2. Signal: 65% snap share in relief plus goal-line work, both above threshold, and the starter is on IR so the role is durable. Priority: high — lead-back roles don't reach next week's wire.
> 2. **RB Colby Trask** — the second-order add. He's the pass-catching complement in that same backfield, rostered in 2% of leagues, and will absorb third-down work Okafor doesn't. A fraction of Okafor's price for a real share of the vacated touches.
> 3. **TE Harlan Pruitt** — one-week stream for Vasquez's week-9 bye (hole #1 next week). Minimum bid; can wait if the pool is stable.
> 4. *Skip* WR Deion Marsette despite the consensus rank — he'd be your WR5 and never crack the lineup. Fit beats fame; let a WR-needy rival spend on him.
