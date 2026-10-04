---
name: weekly-briefing
description: This skill should be used when the user asks "what should I do this week", "weekly briefing", "run my week", "what's on my plate this week", "walk me through this week", or "give me my weekly checklist". Conducts one in-season briefing by running start/sit, waiver, and cut analysis in order. Not for a standalone lineup call (lineup-strategy start-sit), a standalone waiver scan (waiver-wire waiver-scan), cut-only advice (waiver-wire drop-candidates), or applying any change on the platform (roster-ops).
---

# Weekly Briefing

Run the in-season loop once and deliver a single page: lineup call, wire targets, recommended cut, and an optional trade seed. **This skill is a conductor, not a fourth copy of the methodology.** Reuse the sibling skills' decision contracts; do not invent a parallel start/sit or FAAB system here.

**Live platform source routing.** Honor a browser the user explicitly names. If `leagues.md` records a Preferred browser, use that when it has a signed-in session for the platform. Otherwise use any authenticated browser the current assistant already has. For Yahoo league data, prefer an authenticated browser over a connector. If a Yahoo connector returns `403`, `unauthorized`, or an equivalent authorization failure, do not retry it during the same task. For non-Yahoo platforms, use a purpose-built connector when it is available and returns complete current data; otherwise use the browser. Read league rosters, the free-agent pool, standings, transaction history, and any rankings site directly instead of making the user paste them. Timestamp live data and name the source. The session rules from `roster-ops` apply unchanged: the user's session is the auth; never ask for, read, store, or type credentials; use the visible UI rather than platform endpoints; and stop and hand back on any login, 2FA, captcha, consent, or unusual-activity screen. If no usable live source exists, state the access gap and do not fabricate league-specific analysis.

**This skill is read-only.** Reading a page needs no confirmation, but never click anything that changes a roster, files a claim, or sends an offer from here — that is what the `roster-ops` skills and their confirmation gates exist for.

## Step 1: Load league context

Read `leagues.md` from the project root first — the fields that matter here are scoring, starting slots, waiver system, playoff weeks, and Preferred browser. If the file is missing or those fields are blank, ask for them directly and suggest running the `fantasy-league-setup:league-config` skill to persist the answers. If `leagues.md` defines more than one league, use the one marked `(default)` unless the user names another.

## Step 2: Snapshot this week

Collect, in this order, only what the later steps need:

- Current week, as-of timestamp, and whether any games have already locked.
- The user's roster with positions, byes, and injury designations.
- Standings or projected margin if available — start/sit uses favorite vs. underdog.
- The free-agent pool if a wire or cut decision is likely.

Prefer a live roster and player-pool read over a paste. If the live source is missing, ask for the roster and say which later sections will stay provisional.

## Step 3: Run the sibling methods in order

1. **Lineup** — run `lineup-strategy:start-sit` if it is installed. If it is not, reproduce its full decision contract inline: global assignment across eligible slots, lock/kickoff awareness, late-swap optionality, timestamp, and official status plus a second credible source for any injury-driven change.
2. **Wire** — run `waiver-wire:waiver-scan` if installed; otherwise reproduce its hole-first ranking inline. Do not size bids here; point at `waiver-wire:faab-bidding` when a claim needs a number.
3. **Cuts** — run `waiver-wire:drop-candidates` if a spot is needed or the bench is obviously bloated. If that plugin is missing, reproduce its cut-order and vetoes inline.
4. **Trade seed (optional)** — run `trade-analyzer:trade-finder` only when a starting-slot hole will still exist after the recommended adds. Skip this section when the wire already fixes the week.

Missing **analysis** can be done inline. Missing **transaction execution** must never be inlined: provide the clicks while preserving the transaction summary and explicit confirmation boundary.

## Step 4: Deliver one briefing

Lead with the as-of timestamp and league name. Then, in this order:

1. **Lineup** — the call in the first sentence, plus any lock/contingency that cannot wait.
2. **Wire** — at most three ranked targets, each tied to a named hole. Skip names if the pool was unavailable and describe the profile instead.
3. **Cut** — the recommended drop for the stated need, or "no safe cut."
4. **Trade** — one optional seed, or omit the section.
5. **Unverified** — anything still waiting on official status plus a second source.

Then offer the handoffs: `roster-ops:set-lineup` to apply the lineup, `roster-ops:submit-waiver-claim` to file a claim, `roster-ops:propose-trade` to send an offer. If those plugins are missing, give the clicks but do not file, set, or send anything from this skill.

## Worked example (fictional)

"Gridiron Gazette," 12-team half-PPR, week 9. **As of Tuesday 9:00 AM ET**, the live roster and free-agent pool are current. TE Oren Vasquez is on bye; RB room is Tobias Renner plus dart throws.

> **Week 9 briefing, as of Tuesday 9:00 AM ET.**
>
> **Lineup:** Start Harlan Pruitt at TE for the bye; keep Renner in RB1. No injury-driven swap is verified.
> **Wire:** 1) Silas Okafor — RB insurance, official IR ahead of him plus a beat-practice report. 2) Colby Trask — second-order add in the same backfield. 3) Pruitt only if he is still a free agent and not already rostered for the bye.
> **Cut:** Ironhogs DST if a spot is needed — second defense, matchup already passed.
> **Trade:** skip — the wire fills the week-9 TE hole and the RB insurance gap.
> **Unverified:** none on the recommended lineup. Okafor stays provisional if either role source disappears before claims lock.
>
> To apply the lineup, `roster-ops:set-lineup` can do it in your browser. To file Okafor, run `waiver-wire:faab-bidding` for the number, then `roster-ops:submit-waiver-claim`. This briefing does not click either one.
