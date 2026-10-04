---
name: draft-prep
description: This skill should be used before draft day, when the user asks to "build my draft board", "help me prep for my draft", "make tiers from these rankings", "tier my rankings", "rank players for my league", "adjust rankings for my scoring", or asks about positional scarcity or value-based drafting strategy. Builds a tiered, league-adjusted draft board from rankings the user supplies or that are read from their browser. Not for use during a live draft (draft-strategy live-draft-assistant) or for keeper decisions (draft-strategy keeper-evaluation).
---

# Draft Prep: Tiered Board Construction

Build a draft board that is tiered, value-adjusted, and specific to the user's league settings — not a reprint of generic rankings.

## Step 1: Load league context

Read `leagues.md` from the project root first — the fields that matter here are teams, scoring (including superflex and TE premium), starting slots, bench size, and keeper rules. If the file is missing or those fields are blank, ask for them directly and suggest running the `fantasy-league-setup:league-config` skill to persist the answers. If `leagues.md` defines more than one league, use the one marked `(default)` unless the user names another.

## Step 2: Get rankings data

Ask the user which they prefer, in this order:

1. **User-supplied rankings** (best) — a pasted CSV/list from any source they trust, ideally with projected points and ADP columns.
2. **Read from the browser** — if browser automation is available, read current consensus rankings and ADP off a rankings site or the platform's own draft board, and tell the user the source and the date it was read.
3. **No data available** — build the board structure and decision rules anyway and mark player slots as "fill from your rankings"; never invent projections and present them as real.

**Live platform source routing.** Honor a browser the user explicitly names. If `leagues.md` records a Preferred browser, use that when it has a signed-in session for the platform. Otherwise use any authenticated browser the current assistant already has. For Yahoo league data, prefer an authenticated browser over a connector. If a Yahoo connector returns `403`, `unauthorized`, or an equivalent authorization failure, do not retry it during the same task. For non-Yahoo platforms, use a purpose-built connector when it is available and returns complete current data; otherwise use the browser. Read league rosters, the free-agent pool, standings, transaction history, and any rankings site directly instead of making the user paste them. Timestamp live data and name the source. The session rules from `roster-ops` apply unchanged: the user's session is the auth; never ask for, read, store, or type credentials; use the visible UI rather than platform endpoints; and stop and hand back on any login, 2FA, captcha, consent, or unusual-activity screen. If no usable live source exists, state the access gap and do not fabricate league-specific analysis.

**This skill is read-only.** Reading a page needs no confirmation, but never click anything that changes a roster, files a claim, or sends an offer from here — that is what the `roster-ops` skills and their confirmation gates exist for.

Minimum viable columns: player and position. **Projected points are required for numeric value-over-replacement outputs; overall rank alone is enough to build tiers and scarcity notes, but not to claim point baselines or VOR totals.** ADP unlocks reach/value analysis; bye weeks unlock conflict warnings.

**Ask for two sources when possible, and blend them.** Sources routinely disagree by 15–25% on individual players, and the disagreement is itself signal: a player whose projections vary by more than a tier width has a genuinely uncertain role. Flag those explicitly — they are the players to avoid if the roster needs certainty, and to target if it needs upside.

## Step 3: Compute starter demand and replacement level

Value-based drafting prices every player against a defined positional baseline, not against zero. Do not use "last required starter" and "best freely available player" as if they were the same line.

**Do this in two passes.** First compute the **starter-demand baseline**: where the league runs out of weekly starters at each position. This is the draft-board/VBD line. Then estimate the **true waiver-replacement baseline**: the best player likely to remain freely available after teams fill starters and benches, using the actual platform pool when available or the league's bench depth and observed positional roster rates. Report that second line as a streamability and bench-value check; it is usually lower than the starter-demand line at RB/WR and can be higher in practice at highly streamable positions. If the input is rank-only, stop at demand/tier/scarcity structure and say numeric baselines are unavailable.

**Demand per position** = `teams × (dedicated starters + flex_slots × flex_share)`.

The `flex_slots` term matters and is often dropped: a 2-FLEX league has twice the flex demand of a 1-FLEX league.

**Derive the flex share — do not assume it.** Hardcoded splits are format-specific and wrong outside the format they came from. Instead: pool every flex-eligible player beyond their dedicated-starter baseline, sort by projection when available (or by rank if not), take the top `teams × flex_slots`, and count how many are RB vs. WR vs. TE. That count *is* the flex share, computed from the same board already in hand. It adapts automatically to PPR, standard, TE premium, superflex, and league size. As a sanity check on the result: full PPR skews the flex toward WR, standard skews it toward RB, and TE premium pulls TEs into it that base scoring never would.

**Then adjust the starter-demand baseline for streamability and league-specific replacement rules**, because "freely obtainable" differs sharply by position:

- **RB/WR**: use the computed demand line for draft scarcity, but estimate actual waiver replacement separately from bench depth and the likely post-draft pool. In deep leagues the freely available RB/WR can sit well below the last required starter.
- **QB in typical 1-QB leagues**: streaming the best weekly matchup aggregates to roughly QB8–QB10 season-equivalent output, so true replacement can be *better* than the league-size demand line (QB12 in a 12-team league). Use the streaming estimate. This is the mathematical reason late-round QB is usually correct. If the league materially changes QB scoring or access — 6-point pass TDs, heavy bonus scoring, deep lineups, start-2 QB, or superflex — recompute from that format instead of forcing the 1-QB prior.
- **TE**: streaming usually works poorly, because TE production is role-driven rather than matchup-driven. True replacement is often *worse* than the league-size TE demand line — roughly TE16–18 in an ordinary 12-team, 1-TE format — which means elite TEs are worth more than the naive line suggests. In 2-TE, TE premium, or unusually deep-bench formats, let the recomputed demand line set the premium rather than hardcoding a TE16–18 rule.
- **Superflex/2QB**: the superflex slot goes to a QB in essentially every lineup, so use a flex share of 1.0 for QB and compute demand as `teams × (dedicated QB slots + QB-assigned superflex slots)` — QB24 is the result for a 12-team 1QB+1SF league, not a universal constant. Do not describe this as a multiplier on QB value; let the recomputed baseline drive the board. What actually changes is that the entire position becomes draftable and the range around that computed demand line becomes the scarcity crisis: only about 32 NFL quarterbacks can start in a given week, while the league also needs backups. In most 12-team superflex rooms that means at least one QB is an early-round priority and the second rarely lasts deep into the draft; recompute that conclusion for other league sizes and slot counts.
- **K/DST and specialist positions**: in ordinary 1-K/1-DST formats with no return-yard or IDP distortion, replacement is the best free option every single week, so value over replacement is approximately zero. If the league pays heavily for return yards, starts multiple defenses, or turns IDP/specialists into scarce lineup slots, recompute those positions from the league settings instead of forcing them to zero.

**Draft VBD = projected points − starter-demand baseline points.** Use that consistently for the overall draft board rather than mixing baselines across positions. Also report **waiver VOR = projected points − likely waiver-replacement points** when the pool estimate is reliable; use it to explain streamability and bench value, not as an unlabeled substitute for draft VBD.

## Step 4: Build tiers

Tiers matter more than ranks — on the clock, the question is "is anyone left in the tier," not "who is ranked 43rd."

- Sort each position by projected points. **Break a tier where a gap between consecutive players is clearly larger than the gaps within the current group** — roughly one standard deviation of that position's gap distribution. A simpler working proxy: players within about 0.75–1.0 points *per game* of each other belong in the same tier.
- Draw tiers relative to projection *uncertainty*, not point level. Two players 8 points apart in a season projection whose sources disagree by 60 points are the same tier regardless of what any percentage rule says.
- **Stop tiering below replacement level.** Near the bottom of a position a 15-player tier is the correct answer — they genuinely are interchangeable, and forcing breaks there invents distinctions that do not exist.
- Label each tier with an action note, not just a number: "Tier 3 RB — last group you can trust weekly; if 2 remain at your pick, wait; if 1, take him."

## Step 5: Positional scarcity and structure notes

- Compare tier depth to league-wide demand from Step 3. The position where trustworthy players run out soonest is the scarcity priority.
- Flag the "cliff round": the round by which each position's last solid tier will be gone at current ADP.
- **In standard 1-K/1-DST formats, punt K and DST to the final two rounds.** Their value over replacement is approximately zero and free replacements are available all season, so every earlier pick spent on them throws away a bench asset. Only override this if the league settings themselves create real scarcity or outlier scoring for K, DST, return specialists, or IDP-style slots. A QB2 in a typical 1-QB league is nearly as wasteful.
- Name the structure the board implies — zero-RB, hero-RB, robust-RB, late-round QB, superflex double-QB — and say which draft slots can actually execute it. Structures are slot-dependent: advice to pair two players from an early tier is unreachable from most slots.
- Use weeks 15–17 (or the league's configured playoff weeks) strength of schedule as an **intra-tier tiebreaker only**. Full-season SOS at draft time is close to noise, since projections already embed it and preseason defensive rankings are unreliable. Where SOS is used at all, use positional splits, never team-level defensive rank.

## Step 6: Deliver the board

Output a markdown table per position. Include `(tier, player, projection, value over replacement, ADP, bye)` when projections exist; if the input is rank-only, switch to `(tier, player, rank, ADP, bye)` and state plainly that the board is structural rather than projection-priced. Then add the scarcity summary and 3–5 strategy bullets specific to their settings.

## Worked example (fictional)

"Gridiron Gazette," 12-team half-PPR, 1 QB / 2 RB / 2 WR / 1 TE / 1 flex. Derived flex share came out RB 0.45 / WR 0.5 / TE 0.05, so RB demand = 12 × (2 + 1 × 0.45) ≈ RB29; call the baseline 155 points.

| Tier | RB | Proj | Value (vs 155) | ADP |
|------|----|------|----------------|-----|
| 1 | Marcus Vellum | 285 | +130 | 1.02 |
| 1 | Dario Whitlock | 271 | +116 | 1.05 |
| 2 | Tobias Renner | 244 | +89 | 1.11 |
| 2 | Quincy Marsh | 238 | +83 | 2.03 |
| 3 | Errol Fontaine | 209 | +54 | 3.07 |

Board note produced: "Only five RBs clear +50, and your league demands about 29 RB-equivalent starts weekly. Those five go at ADPs 1.02, 1.05, 1.11, 2.03, and 3.07 — so only a manager near the turn (slots 10–12) can realistically pair two. From slots 1–9, plan on one of them plus a Tier 3 RB2, or commit to zero-RB deliberately rather than by accident."

Note what the example does: it reports what each draft slot can actually execute, rather than giving advice most of the league cannot follow.
