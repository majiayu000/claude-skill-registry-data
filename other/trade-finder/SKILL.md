---
name: trade-finder
description: This skill should be used when the user asks "find me a trade", "who should I target in a trade", "scan the league for trade partners", "who needs what in my league", "help me get a running back via trade", "is he a buy low", "should I sell high on him", or wants trade ideas without a specific offer on the table. Scans league rosters for complementary surpluses and mispriced players, then drafts a concrete opening proposal. Not for judging an existing offer (trade-analyzer trade-evaluation), handling the back-and-forth (trade-analyzer trade-negotiation), or sending the offer in the browser (roster-ops propose-trade).
---

# Trade Finder: Complementary Surplus Scan

Find the trades that *should* exist in this league: pairs of rosters where each team's surplus is the other's hole. Output is a shortlist of partners and one drafted opening proposal — not a vague "you could use a WR."

## Step 1: Load context

Read `leagues.md` from the project root first — the fields that matter here are scoring, starting slots, trade deadline, and playoff weeks. If the file is missing or those fields are blank, ask for them directly and suggest running the `fantasy-league-setup:league-config` skill to persist the answers. If `leagues.md` defines more than one league, use the one marked `(default)` unless the user names another. Gather every roster in the league plus standings. If browser automation is available and the user is logged in, read the league's rosters and standings pages directly — this skill needs every team, so reading beats pasting a dozen rosters by hand. A partial scan is fine; say which teams weren't scanned.
**Live platform source routing.** Honor a browser the user explicitly names. If `leagues.md` records a Preferred browser, use that when it has a signed-in session for the platform. Otherwise use any authenticated browser the current assistant already has. For Yahoo league data, prefer an authenticated browser over a connector. If a Yahoo connector returns `403`, `unauthorized`, or an equivalent authorization failure, do not retry it during the same task. For non-Yahoo platforms, use a purpose-built connector when it is available and returns complete current data; otherwise use the browser. Read league rosters, the free-agent pool, standings, transaction history, and any rankings site directly instead of making the user paste them. Timestamp live data and name the source. The session rules from `roster-ops` apply unchanged: the user's session is the auth; never ask for, read, store, or type credentials; use the visible UI rather than platform endpoints; and stop and hand back on any login, 2FA, captcha, consent, or unusual-activity screen. If no usable live source exists, state the access gap and do not fabricate league-specific analysis.

**This skill is read-only.** Reading a page needs no confirmation, but never click anything that changes a roster, files a claim, or sends an offer from here — that is what the `roster-ops` skills and their confirmation gates exist for.

For any in-season scan, make the timing explicit:

- State the shortlist **as of** a concrete date/time.
- Refresh rosters, standings, injuries, and usage news if the inputs are stale or partial.
- For any trade idea built around an injury discount or return timetable, require **both** the official team/game status and a second credible source before treating that injury angle as actionable.

## Step 2: Build the surplus/deficit matrix

For each team, at each position, compare **startable-quality players rostered vs. starting slots required** (this league's slots — a 3rd good RB is surplus in a 2-RB league and par in a 2RB+flex league):

- Surplus: more week-in, week-out startable players than slots (+1 or more).
- Deficit: a starting slot filled by waiver-tier production.
- **Weight surplus by replenishment.** A third startable WR is worth less than a third startable RB, because the wire refills WR and does not refill RB. Position-blind surplus counting overvalues exactly the pieces that are easiest to replace.
- Note bye/playoff-schedule pressure: a team about to hit a triple-bye week has a *temporary* deficit worth exploiting gently.

## Step 2b: Scan for mispriced players — where the repeatable money is

Structural surplus finds trades that *should* exist. Mispricing finds trades that are *profitable*. Run both.

The principle is the same one that governs waiver adds: opportunity is sticky, efficiency is not.

- **Sell** a player whose touchdown rate is running well above his career or expected rate over a 4+ week sample, whose yards per touch far exceed his norms, or whose fantasy rank sits well above his target/carry share. His price will never be higher and the production is not repeatable.
- **Buy** a player whose target or carry share is top-15 at his position while his points rank sits outside the top 30. The volume is real; the results will follow.

Name these candidates explicitly on both rosters — they are the pieces to build the offer around.

## Step 3: Rank partner fit

Score each rival as a partner:

1. **Complementarity** (required): their surplus covers the user's deficit AND the user's surplus covers one of theirs. One-directional need means the user must overpay — deprioritize.
2. **Motivation**: bubble teams (records near .500) trade most; first-place teams trade least. Eliminated redraft managers usually stop trading out of **disengagement, not incentive** — so a clear, low-effort offer can still land. In keeper or dynasty formats the reverse holds: eliminated teams are a contender's best partners, since future value is worth more to them than this season's points.
3. **History**, if the user knows it: managers who've already made trades this season will trade again.
4. **Avoid arming your competition**: deprioritize the team directly chasing your playoff seed, and the team you play next week.

## Step 4: Draft the opening proposal

For the top partner, construct a specific offer:

- Trade **from surplus into deficit on both sides** — the offer should improve both starting lineups (verify with the lineup-delta test: value that doesn't reach a lineup isn't real to either side).
- **Gate the opener on their lineup improving, but treat that as necessary rather than sufficient.** The offer must visibly help their starters, remain defensible within the uncertainty of the value inputs, and respect league norms and the manager's stated preferences. A lineup upgrade does not make an extreme asset imbalance non-insulting, and a value-chart tie does not rescue an offer that leaves their lineup unchanged.
- Given that gate, **the opener may start at a meaningfully favorable raw-value anchor** so long as it is still credibly defensible from their lineup's perspective. That anchor is not the same as the final executable price: expect the accepted version to land materially closer to even, and say so.
- In multi-player constructions, include the **forced-cut and waiver-replacement cost** for whichever side has to clear a roster spot. A 2-for-1 that improves starters but forces them to cut their only bye-week RB is not actually clean.
- Check asset legality before proposing it: FAAB/pick trading allowed or not, keeper rights if relevant, recently added players, IR designations, and any platform restrictions visible on the page.
- Include the pitch: two sentences the user can send explaining why it helps *the other team*, referencing their situation ("you've got three startable RBs and a WR2 hole and the deadline's in two weeks").
- Offer 1–2 backup constructions (a smaller version, and a version with a different sweetener) for the negotiation to come.

## Step 5: Hand off

Suggest `trade-analyzer:trade-evaluation` to pressure-test the construction, `trade-analyzer:trade-negotiation` when the reply comes back, and `roster-ops:propose-trade` to send it. If an analysis plugin is missing, do that analysis inline. If the execution plugin is missing, provide the clicks but do not blur this read-only skill into an ungated browser transaction.

## Worked example (fictional)

"Basement Brawlers," 12-team, week 8. **As of Thursday 7:00 PM ET**, rosters, standings, and usage inputs are current, and no proposed angle depends on unresolved injury news. User (5-3): RB surplus (4 startable for 2+flex), TE deficit (streaming). Scan finds:

| Team | Record | Surplus | Deficit | Fit |
|---|---|---|---|---|
| Turf Burns | 4-4 | TE (elite Oren Vasquez + startable backup) | RB (RB2 slot is waiver-tier) | **Both-ways — top partner** |
| Blitz Krieg | 6-2 | WR | RB | One-way (user has no WR hole) — skip |
| Fumble Bees | 2-6 | QB | everything | Motivated but nothing user needs — skip |

> **Opening offer to Turf Burns**: send RB Errol Fontaine (user's RB4, their instant RB2 upgrade), receive TE Oren Vasquez. **Lineup gate passes** — Fontaine steps straight into their waiver-tier RB2 slot, so this visibly improves their starters and is not an insulting opener regardless of the value split. The user starts from a clearly favorable anchor because that is what openers are for, while expecting any executable deal to settle materially closer to even after counters. Pitch: "You're one RB from a playoff push and I'm streaming TE — Fontaine starts for you Sunday." Fallbacks: add RB Dewey Sandoval if they balk; smaller version targets their backup TE instead.
