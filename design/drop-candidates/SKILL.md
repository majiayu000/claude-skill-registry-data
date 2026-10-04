---
name: drop-candidates
description: This skill should be used when the user asks "who should I drop", "who's safe to cut", "make room on my roster", "who's droppable", "what's my cut list", or needs to free a roster spot for an add. Ranks the user's own roster from most to least cuttable with bye-week and playoff-schedule awareness. Not for picking the incoming player (waiver-wire waiver-scan), bid amounts (waiver-wire faab-bidding), benching decisions for this week's lineup (lineup-strategy start-sit), or a combined weekly checklist (lineup-strategy weekly-briefing).
---

# Drop Candidates: The Cut List

Rank the roster from most-cuttable to untouchable. The default failure mode is cutting the wrong kind of player for the right reasons — this skill exists to stop bye-week panic drops of players who decide week 16.

## Step 1: Load context

Read `leagues.md` from the project root first — the fields that matter here are roster size, starting slots, playoff weeks, IR slots, and any acquisition cap. If the file is missing or blank, ask and suggest running `fantasy-league-setup:league-config`. If more than one league is defined, use the one marked `(default)`.

Ask for the current roster (with byes and injury notes), the most relevant free-agent alternatives at the same positions, and *why* a spot is needed — a one-week streamer justifies a much shallower cut than a season-long add.

If the proposed cut is driven by an injury, demotion, or role-loss report, pin the analysis to an **as-of** timestamp and cite the evidence. Before recommending a destructive cut on that basis, confirm both:

- An **official status change**: transaction wire, inactive list, practice report, coach quote, or platform designation.
- A **second credible source** confirming that the role or timeline actually changed.

If that verification is missing or conflicting, mark the player **no-action for now** unless there is an immediate roster emergency and the user explicitly accepts the risk.

**Live platform source routing.** Honor a browser the user explicitly names. If `leagues.md` records a Preferred browser, use that when it has a signed-in session for the platform. Otherwise use any authenticated browser the current assistant already has. For Yahoo league data, prefer an authenticated browser over a connector. If a Yahoo connector returns `403`, `unauthorized`, or an equivalent authorization failure, do not retry it during the same task. For non-Yahoo platforms, use a purpose-built connector when it is available and returns complete current data; otherwise use the browser. Read league rosters, the free-agent pool, standings, transaction history, and any rankings site directly instead of making the user paste them. Timestamp live data and name the source. The session rules from `roster-ops` apply unchanged: the user's session is the auth; never ask for, read, store, or type credentials; use the visible UI rather than platform endpoints; and stop and hand back on any login, 2FA, captcha, consent, or unusual-activity screen. If no usable live source exists, state the access gap and do not fabricate league-specific analysis.

**This skill is read-only.** Reading a page needs no confirmation, but never click anything that changes a roster, files a claim, or sends an offer from here — that is what the `roster-ops` skills and their confirmation gates exist for.

## Step 2: Price the roster spot

A bench spot is not free storage. Its value equals the best player the user could acquire with it over the rest of the season, which in an active 12-team league is meaningfully positive. Two consequences most managers miss:

- **Stalled stashes should be cut faster than feels comfortable.** Three weeks of flat snap share is already generous.
- A third QB in a 1-QB league, or a second K or DST, is a straight points loss.

The exception: where the league caps weekly acquisitions, the spot is *cheaper* because it can't be churned anyway, so holding upside is more defensible.

## Step 3: Classify every bench player

Cut order, most cuttable first:

1. **Second K or DST** — never roster two outside the single week a swap is pre-staged.
2. **Expired streamers** — last week's matchup play whose matchup has passed.
3. **Redundant depth at a replenishing position.** Measure redundancy against *this league's* starting slots, then check the **actual free-agent pool** before calling a position replaceable. If the wire currently offers multiple startable WRs and no playable RBs, the sixth WR is more expendable than the fourth RB; if the pool shows the opposite, flip the conclusion. Use real pool evidence, not generic WR/RB assumptions.
4. **Stalled lottery tickets** — stashes whose path to a role hasn't moved in 3+ weeks (snap share flat or falling), and backups in true committee backfields where no single injury creates a workload.
5. **Injured starters and own-handcuffs** — use an IR slot if the league has one and the player qualifies; cutting is a last resort.

### Handcuffs are not a cut class — split them

A backup behind a genuine workhorse is **protected on a contender**, not cuttable. If that starter goes down, *whoever holds the backup* owns the replacement workload — the payout accrues to the roster holding the handcuff, not to the manager who owns the starter. Rostering the top backups behind concentrated-workload backfields is the most reliable way to acquire a league-winner without spending waiver budget.

What *is* cuttable is the committee backup, where an injury splits work three ways and no windfall exists. That case belongs in class 4 above. The distinction is workload concentration, not who owns the starter.

## Step 4: Apply the vetoes

- **The claim-back test**: would a rival plausibly claim this player within two weeks? If yes, don't cut for a marginal add — releasing a useful player to the league costs more than the add gains.
- **Bye-week trap**: a player on bye *this* week is temporarily worthless and may be a top-3 asset. Never cut a weekly starter for their bye; stream around it by cutting from classes 1–4 instead.
- **Playoff-schedule veto**: from about week 10, weight the league's configured playoff weeks. A mediocre bench piece with elite playoff matchups outranks a slightly better player facing top defenses then. Conversely — and say this out loud, because it is counterintuitive — "good so far" players with brutal playoff schedules move *up* the cut list. If the league grants the top seeds a first-round bye and the user is likely to earn one, weight the *later* playoff weeks accordingly rather than the first.
- **Source-verification veto**: if the cut depends on a rumored injury setback, surprise benching, or depth-chart shakeup that lacks official status plus a second credible source, do not recommend the cut yet. Give a provisional ranking and say what confirmation would unlock it.

## Step 5: Deliver

Rank the roster most-to-least cuttable with a one-line reason each, mark the recommended cut for the stated need, and flag any veto that applied. If nothing survives the vetoes, say the roster has no safe cut and the incoming add must beat the least-protected player outright.

## Worked example (fictional)

"Mud Dogs," week 9, 12-team league, needs one spot for a TE streamer. Bench: RB Colby Trask (backup to a rival's workhorse), WR Jalen Moss (bye this week, WR3 rest of season), RB Dewey Sandoval (stash, snaps flat 4 weeks), Ironhogs DST (second defense, added for a matchup that has passed).

> 1. **Cut: Ironhogs DST** — second DST, class 1. Its matchup already passed and you should never carry two. Done.
> 2. Next if another spot is needed: Dewey Sandoval — stalled stash, class 4, four weeks of flat snaps. Claim-back test passes; nobody claims him.
> 3. **Protect Colby Trask.** He backs up a workhorse with a concentrated touch share — if that starter misses time, *you* own the replacement, not the rival who drafted him. That's the cheapest league-winner path on this roster.
> 4. **Never: Jalen Moss.** Bye-week trap — he's a weekly starter next week and a rival claims him within minutes.
