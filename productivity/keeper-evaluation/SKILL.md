---
name: keeper-evaluation
description: This skill should be used when the user asks "who should I keep", "which keepers should I pick", "is he worth keeping at that price", "keeper value", "what does keeping him cost me", or needs to compare keeper candidates before a draft. Runs keeper cost versus market value math to rank keeper candidates by surplus. Not for building the draft board itself (draft-strategy draft-prep) or in-draft picks (draft-strategy live-draft-assistant).
---

# Keeper Evaluation

Rank keeper candidates by **surplus value**: what the player is worth minus what keeping them costs. A good keeper is one priced below market, not simply the best player on the roster.

## Step 1: Load context

Read `leagues.md` from the project root first — the fields that matter here are keeper rules (how many, cost mechanism, escalation), teams, scoring, and starting slots. If the file is missing or keeper rules aren't recorded, ask: How many keepers? What does keeping a player cost (a draft round, an auction dollar amount)? Does the cost escalate year over year? Then offer to save the answers back to `leagues.md`. If more than one league is defined, use the one marked `(default)` unless the user names another.

## Step 2: Gather candidates and price them

For each candidate: player, keeper cost (round or $), and current ADP or auction market value. For round-cost leagues, get the **exact pick the keep consumes**: draft slot, round, and the league's collision rule if multiple keepers map to the same round. If the league has eligibility restrictions (tenure limits, drafted-only, no first-rounders, tag deadlines, etc.), screen those out before doing surplus math. Ask the user to supply these, or — if browser automation is available and they're logged in — read current values off their platform or a rankings site, stating the source and date.

**Live platform source routing.** Honor a browser the user explicitly names. If `leagues.md` records a Preferred browser, use that when it has a signed-in session for the platform. Otherwise use any authenticated browser the current assistant already has. For Yahoo league data, prefer an authenticated browser over a connector. If a Yahoo connector returns `403`, `unauthorized`, or an equivalent authorization failure, do not retry it during the same task. For non-Yahoo platforms, use a purpose-built connector when it is available and returns complete current data; otherwise use the browser. Read league rosters, the free-agent pool, standings, transaction history, and any rankings site directly instead of making the user paste them. Timestamp live data and name the source. The session rules from `roster-ops` apply unchanged: the user's session is the auth; never ask for, read, store, or type credentials; use the visible UI rather than platform endpoints; and stop and hand back on any login, 2FA, captcha, consent, or unusual-activity screen. If no usable live source exists, state the access gap and do not fabricate league-specific analysis.

**This skill is read-only.** Reading a page needs no confirmation, but never click anything that changes a roster, files a claim, or sends an offer from here — that is what the `roster-ops` skills and their confirmation gates exist for.

### Measure surplus in points or dollars, never in rounds

A round is not a constant unit of value. The gap between consecutive picks is steep in rounds 1–3 and nearly flat after round 8, so a flat round-based threshold simultaneously rejects elite keepers and accepts worthless ones. Keeping the overall #1 player at pick 1.12 captures 11 picks — just under one round — of market value and is one of the largest edges available in any keeper league; keeping a round-10 ADP player at a round-12 cost spans more rounds but can be worth almost nothing.

**Surplus = the player's value over replacement − the value over replacement of the player typically available at the exact cost pick.** Reuse the board from `draft-strategy:draft-prep`, which already computes exactly this unit. Price round costs by the actual overall selection they burn, not a generic "round 6" bucket: pick 6.01 and pick 6.12 are meaningfully different assets. If two keepers collide onto the same round, apply the league's written collision rule first (earliest slot, one-round escalation, forfeit next open pick, etc.) and then price the resolved pick.

**Keep threshold ≈ one tier gap at that position**, roughly 15–25 points in a 12-team half-PPR. Below that, the keeper slot is better spent on optionality.

### Adjust for pool dilution

Keepers remove players from the draft pool, but they also consume the picks used to keep them. Those two effects mostly cancel, so the naive assumption that "N keepers shift everyone N picks earlier" badly overstates the effect — a keeper kept at his own market price is value-neutral.

The dilution at any pick P is the number of keepers whose market value is ahead of P but whose **cost pick is behind P** — the bargains. In a 12-team keep-2 league with typical surpluses that runs to roughly **5 to 6 picks, about half a round**, peaking in the middle rounds. Apply it where the value curve is steep and ignore it below round 8, where it changes nothing.

Because dilution is small, break-even sits near zero surplus, not comfortably above it. The genuine reason to require a *positive* threshold is **option value**: declaring keepers before camp locks the decision in ahead of injury news and ADP movement. Say that as the reason, rather than inflating the threshold.

## Step 3: Auction leagues

Surplus = market value − keeper price, in dollars — but two corrections come first.

**Compute inflation.** Keeping players below market leaves more money chasing less value:

`inflation = (total league budget − total keeper prices) / (market value of the remaining player pool)`

If a 12-team $200 league keeps $600 of value at $300 of price, then $2,100 chases $1,800 of value — 17% inflation on every subsequent bid. A user who doesn't know this underbids the entire auction. Multiply remaining players' market values by the inflation factor before comparing anything.

**Use a ratio, not an absolute threshold.** A $20 surplus on a $5 keeper is a 5× return and an obvious keep; the same $20 surplus on a $60 keeper is positive but commits nearly a third of the budget and constrains the whole roster. Keep when `market value / keeper price ≥ 1.5` for players priced above ~5% of budget, and keep essentially any positive-surplus player priced below 5%.

## Step 4: Tiebreakers

Apply these only to separate candidates of similar surplus — never as adjustments to the surplus itself, which would double-count what market value already prices in:

- **Escalation**: prefer the keeper with the longer cheap runway. Escalation affects *next* year's price, not this year's value, so it breaks ties rather than reducing surplus.
- **Age, in multi-year keeper formats**: RB production tends to fall off around 27, WR around 30, TE later, QB holding into the mid-30s. Irrelevant in single-season keeper leagues.
- **Role certainty**: prefer the player whose projection sources agree. Wide disagreement means an unresolved role.

Do **not** apply a positional adjustment. Market value already embeds positional scarcity — that is why QB1s go in round 5 rather than round 1 in a 1-QB league. Subtracting again for "QB replacement is free" penalizes the same fact twice. In **superflex**, the opposite holds and no adjustment is needed either: recomputed QB baselines make quarterbacks the most valuable keeper class outright, and the points-based surplus shows it automatically.

## Step 5: Rank and recommend

Output candidates sorted by surplus, mark keep/pass at the league's keeper count, and note the draft-board consequence of each keep ("keeping him burns your 6th — plan for zero-RB through round 5"). Explicitly flag any ineligible player or unresolved cost collision rather than silently pricing through it. Suggest running `draft-strategy:draft-prep` next so the board reflects the keeper-adjusted pool.

## Worked example (fictional)

"Basement Brawlers," 12-team half-PPR, keep 2, cost = round drafted last year − 1. The user drafts from slot 10, so the resolved snake cost picks are shown below; no candidates collide. If two keepers do collide, this league moves the later-declared keeper one round earlier before pricing it. Values come from the draft-prep board; replacement baselines RB 155, WR 150, QB 250, TE 110.

| Candidate | Resolved cost pick | Value at cost pick | Player value | Surplus | Verdict |
|-----------|--------------------|--------------------|--------------|---------|---------|
| WR Cassius Bell | 11.10 (overall 130) | +12 | +88 | **+76** | **KEEP** — largest edge available |
| RB Quincy Marsh | 3.10 (overall 34) | +61 | +83 | **+22** | **KEEP** — clears the ~20-point tier gap |
| TE Oren Vasquez | 5.10 (overall 58) | +30 | +41 | **+11** | Pass, narrowly — real but under a tier gap |
| QB Tug Ridley | 8.03 (overall 87) | +18 | +26 | **+8** | Pass |

Recommendation: keep Bell and Marsh. Note what changed by pricing in points rather than rounds — Ridley is not penalized for being a quarterback (his market price already reflects that), and Vasquez is a *narrow* pass at +11 rather than a confident one, so if either Bell or Marsh becomes ineligible, Vasquez is the next man up rather than an afterthought.
