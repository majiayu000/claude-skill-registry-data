---
name: start-sit
description: This skill should be used when the user asks "who should I start", "start or sit", "should I start X or Y", "who do I bench", "is he a must-start", "A or B at flex", "start X over Y?", or wants a start/sit recommendation from a roster they describe or paste. Gives the recommendation itself — no browser session required. Not for a combined weekly checklist (lineup-strategy weekly-briefing), applying the change on the platform (roster-ops set-lineup), picking up a replacement off waivers (waiver-wire waiver-scan), or deciding who to cut (waiver-wire drop-candidates).
---

# Start/Sit: The Weekly Call

Answer the most common question in fantasy football — who to start — from a roster the user pastes or describes. **This skill never requires a browser session**, which matters because start/sit questions usually arrive as a quick text with two names in it. If browser automation happens to be available and the user is logged in, reading their roster page saves them the typing — but never make a browser session a precondition for an opinion.

**Live platform source routing.** Honor a browser the user explicitly names. If `leagues.md` records a Preferred browser, use that when it has a signed-in session for the platform. Otherwise use any authenticated browser the current assistant already has. For Yahoo league data, prefer an authenticated browser over a connector. If a Yahoo connector returns `403`, `unauthorized`, or an equivalent authorization failure, do not retry it during the same task. For non-Yahoo platforms, use a purpose-built connector when it is available and returns complete current data; otherwise use the browser. Read league rosters, the free-agent pool, standings, transaction history, and any rankings site directly instead of making the user paste them. Timestamp live data and name the source. The session rules from `roster-ops` apply unchanged: the user's session is the auth; never ask for, read, store, or type credentials; use the visible UI rather than platform endpoints; and stop and hand back on any login, 2FA, captcha, consent, or unusual-activity screen. If no usable live source exists, state the access gap and do not fabricate league-specific analysis.

**This skill is read-only.** Reading a page needs no confirmation, but never click anything that changes a roster, files a claim, or sends an offer from here — that is what the `roster-ops` skills and their confirmation gates exist for.

If the user also wants the lineup actually applied on their platform, hand off at the end.

## Step 1: Load league context

Read `leagues.md` from the project root first — the fields that matter here are scoring, starting slots (especially what the FLEX accepts), and playoff weeks. If the file is missing or those fields are blank, ask for them directly and suggest running the `fantasy-league-setup:league-config` skill to persist the answers. If `leagues.md` defines more than one league, use the one marked `(default)` unless the user names another.

## Step 2: Get the roster and the question

Two shapes of question, and they need different amounts of input:

- **Head-to-head** ("start Vellum or Marsh?"): only needs the two players, the slot, and the scoring type. Answer directly — do not demand a full roster.
- **Whole lineup** ("who should I start this week?"): needs the full roster with positions, plus current week. Byes and injury designations if the user has them.

Ask only for what the question actually requires. A user asking about two players does not want an intake interview.

For any time-sensitive call, require freshness explicitly:

- State the recommendation **as of** a concrete date/time.
- On game day, require current injury designations, kickoff times, and any expected inactives news to be fresh. If the inputs are stale, undated, or "from earlier today," refresh them before giving a consequential answer.
- If browser automation is available and the user is logged in, prefer reading the live roster page and status tags directly over relying on memory or an old screenshot.
- For any injury-driven recommendation that materially changes the call, require **both** the official team/game status and a second credible source (practice report, beat reporter, or national reporter). One unsupported rumor is not enough to bench or start someone decisively.

## Step 3: Optimize the lineup globally, then adjust

For a whole lineup, solve the lineup as a full assignment problem across all eligible slots — **not** by greedily dropping the top projection into the next open spot. The right question is "which legal arrangement produces the best lineup overall?" not "who scores most at this row?" In practice:

- Respect each slot's eligibility from `leagues.md`, especially FLEX and SUPERFLEX.
- Treat already-locked players and slots as fixed once kickoff has passed.
- Prefer putting the latest-starting interchangeable RB/WR/TE into FLEX when the projection difference is small, because it preserves late-swap optionality.
- When two near-equal players have different kickoff times and one carries injury risk, keep the cleaner contingency tree alive rather than spending FLEX early.

After the best legal assignment is identified, apply these adjustments in order:

1. **Volume over talent.** Projected touches, targets, and routes run predict weekly scoring far better than name value or last week's box score. A back with 18 touches on a bad offense usually beats a committee back on a good one.
2. **Scoring-format correction.** Slots are not format-neutral: full PPR promotes high-target pass-catching backs and slot receivers; standard scoring promotes goal-line backs; TE premium can push an elite TE ahead of a WR2 for the flex.
3. **Matchup, but only where it moves the needle.** Positional defensive splits matter (a defense stout against the run and porous against the pass), team-level defensive rank does not. Matchup is a tiebreaker between close players, never a reason to bench a clear starter — the range of outcomes for any individual player is far wider than the matchup effect.
4. **Game script and Vegas lines.** A heavy underdog throws more (helps pass-catchers, hurts early-down backs); a heavy favorite runs to close out games. The implied team total is the single best one-number matchup input available.
5. **Weather** only in the extremes — sustained wind above roughly 20 mph is the one condition that reliably suppresses passing and kicking. Cold and light rain are largely noise.

## Step 4: Floor vs. ceiling — the step most advice skips

The favorite/floor and underdog/ceiling rule is a **contextual heuristic**, not a law. Use it when the players are in the same tier and the matchup context actually makes variance matter; do not let it override a clearly stronger median projection just because the user is favored or behind.

The right answer depends on whether the user is favored, how many players remain on each side, and whether correlation helps:

- **Heavy favorite**: lean toward the higher **floor** when the choice is close and uncoupled. Reducing variance protects a lead.
- **Heavy underdog**: lean toward the higher **ceiling** when the choice is close and an outlier helps. Correlated bets are more defensible here.
- **Close matchup or unknown**: start the higher median and move on.

Ask for the projected margin if the user hasn't said, or accept "I don't know" and default to median. Two related cases worth flagging: if the league's playoff tiebreaker is **points-for**, a locked-in team should still maximize points rather than coast; and a team already eliminated from playoff contention should ignore this section entirely.

## Step 5: Add lock and contingency awareness

- Check kickoff order before finalizing. Once an early-game player locks, every downstream swap path changes.
- If a questionable player is in the recommended lineup, give the user the **primary plan and the contingency branch**: who starts if the player is active, and the exact late-swap fallback if he is inactive.
- If the only fallback plays earlier than the questionable starter, say that out loud — the user may need to choose certainty over median projection.
- If the best lineup requires leaving a slightly higher raw projection on the bench in order to preserve a better late window, explain that tradeoff explicitly.

## Step 6: Deliver

Give the call in the first sentence, then the reasoning. Say plainly when it is close — "these two are within a point of each other, start either and don't look back" is a legitimate and useful answer, and pretending to precision that isn't there teaches users to over-manage.

Flag anything genuinely urgent: an empty starting slot, a player on bye in the lineup, or a player already ruled out. Then offer the handoff: "to apply this on your platform, the `roster-ops:set-lineup` skill can do it in your browser — if you don't have that plugin installed, here are the clicks."

## Worked example (fictional)

"Gridiron Gazette," 12-team half-PPR, week 9. User asks at 11:35 AM Sunday: "Flex — Deion Marsette or Silas Okafor?" User is a 3.5-point favorite. Okafor plays in the late window and is officially questionable; Marsette plays at 1 PM.

> **As of Sunday 11:35 AM, the decision deadline is 12:55 PM — before Marsette locks. Start Okafor only if his current official game status plus a second credible report already support his normal workload by then; otherwise start Marsette before the 1 PM lock.** Okafor's 17 projected touches with goal-line work is the steadier profile, and as a slight favorite the floor lean matters because the players are close. Do not pretend Marsette remains a fallback after his game begins. Waiting for the late inactive list is viable only if the roster has another named, eligible late-window fallback; if it does, put that player in FLEX and state the exact contingency.

Note what did the work: the advice is timestamped, injury-sensitive, and built around the actual lock sequence. Volume wins only if availability is corroborated before the fallback disappears.
