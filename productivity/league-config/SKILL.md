---
name: league-config
description: This skill should be used when the user asks to "set up my league", "configure my league", "add my league settings", "update my league config", "onboard my league", "change my scoring settings", or when any fantasy-football-skills skill finds no leagues.md file. Interviews the user once about scoring, roster slots, waiver system, league size, and platform, then writes the answers to a leagues.md file that all other fantasy football skills read.
---

# League Configuration

Interview the user about their fantasy league(s) and persist the answers to `leagues.md` in the project root. Every other fantasy-football-skills skill reads this file first, so a complete interview here means the user is never re-asked for scoring or roster context.

**Live platform source routing.** Honor a browser the user explicitly names. If `leagues.md` records a Preferred browser, use that when it has a signed-in session for the platform. Otherwise use any authenticated browser the current assistant already has. For Yahoo league data, prefer an authenticated browser over a connector. If a Yahoo connector returns `403`, `unauthorized`, or an equivalent authorization failure, do not retry it during the same task. For non-Yahoo platforms, use a purpose-built connector when it is available and returns complete current data; otherwise use the browser. Read league rosters, the free-agent pool, standings, transaction history, and any rankings site directly instead of making the user paste them. Timestamp live data and name the source. The session rules from `roster-ops` apply unchanged: the user's session is the auth; never ask for, read, store, or type credentials; use the visible UI rather than platform endpoints; and stop and hand back on any login, 2FA, captcha, consent, or unusual-activity screen. If no usable live source exists, state the access gap and do not fabricate league-specific analysis.

This skill may write `leagues.md`. It must never click anything that changes a roster, files a claim, or sends an offer.

## Workflow

1. **Check for an existing `leagues.md`** in the project root. If it exists, show the current config and ask whether to update a league, add a new one, or start over. Never silently overwrite.
2. **Read the settings page first** when a signed-in browser is available. Offer to open the league settings (and scoring/roster/waiver subpages) and extract every visible field below. Prefer the platform's exact wording for IDs, scoring magnitudes, and waiver rules. Ask only for what the page does not show.
3. **Interview** the user for remaining gaps, one short batch of questions at a time (not one giant wall). Fall back to a full interview when no browser is available or the user prefers to type. Collect the fields below for each league.
4. **Write `leagues.md`** using the structure in `leagues-template.md` (in this skill's directory). One `## League:` section per league. Strip the template's explanatory comments from the written file — keep it clean.
5. **Confirm** by echoing back a one-line summary per league (e.g., "Gridiron Gazette — 12-team half-PPR on Yahoo, $100 FAAB").

## Fields to collect

Required (advice quality degrades without these):

- **League name** — used as the section header so multiple leagues can coexist
- **Season** — record the fantasy season explicitly (for example `2026`) so dynasty, keeper, and draft contexts do not drift across years
- **Platform** — `yahoo`, `espn`, `sleeper`, or `other` (drives the roster-ops browser playbooks)
- **Platform league ID/key** — record the stable identifier exactly as the platform shows it (`league_id`, `league key`, Sleeper league ID, etc.). This is often in the league URL or settings page and survives league-name changes
- **Timezone** — record the league-local timezone that controls waiver runs, draft time, and deadline interpretation
- **Verified** — the date and source used to confirm the settings, e.g. `2026-08-04 via Yahoo league settings page` or `2026-08-04 via commissioner message`
- **Teams** — league size (drives replacement-level math)
- **Scoring** — `standard`, `half-ppr`, or `ppr`; plus modifiers with their **magnitudes**, not just flags: TE premium (+0.5 or +1.0 per reception is a materially different league), superflex/2QB, points per passing TD (4 vs 6), points per carry, return scoring, big-play or yardage bonuses, kicker scoring, DST scoring, IDP, and any fractional or negative scoring quirks
- **Scoring details** — ask these prompts explicitly and write the answers in plain language with exact values: passing TD points, TE premium, points per carry, return yards/TDs, 100/150/200-yard bonuses, long-play bonuses, kicker makes by distance plus misses, DST points allowed / sacks / turnovers / shutout bonuses, IDP lineup plus tackle/sack/turnover points, and whether any categories score fractionally or can go negative
- **Median scoring / all-play**, if used — it rewards consistency over ceiling and changes what "contender" means
- **Starting roster slots** — e.g., `1 QB, 2 RB, 2 WR, 1 TE, 1 FLEX (RB/WR/TE), 1 K, 1 DST`
- **Bench size** and IR slots
- **Draft setup** — snake, auction, salary-cap, linear, or other; plus the scheduled draft date/time and the pick clock or nomination timer
- **Waiver system** — classify it as `faab`, `rolling-priority`, `weekly-reverse-standings`, `fcfs`, or `hybrid`, then spell out the exact behavior: season budget and whether $0 bids are allowed, the processing day/time, whether waivers run weekly or continuously/daily, whether rolling priority resets to last after a successful claim, whether reverse-standings order recomputes each run or stays fixed for the week, when players become FCFS, and the tie-break rule for equal bids
- **Acquisition limits** — any cap on adds per week or per season. Common on Yahoo and ESPN, and it changes waiver and drop advice substantially, so ask explicitly rather than assuming none

Optional (ask, but accept "skip"):

- **Playoff weeks** — e.g., weeks 15–17 (drives drop-candidates, start/sit, and trade timing). Also ask how many teams make it, whether top seeds get a first-round bye, and what the seeding tiebreaker is — a points-for tiebreaker changes start/sit decisions in blowouts
- **Trade review** — none, commissioner review, or a league veto vote. Veto leagues need trades that *look* balanced, not just ones that are
- **FAAB tradeable?** — some platforms allow trading waiver budget, which unlocks real strategy for both contenders and eliminated teams
- **Keeper rules** — how many keepers, cost mechanism (round-based, auction dollar, escalating)
- **Trade deadline** week
- **The user's team name** — so skills can tell "my roster" apart in exports the user pastes
- **Preferred browser** — optional. Which authenticated browser skills should use when the user does not name one this turn: `ChatGPT built-in`, `Claude in Chrome`, or another named tool. Write `unknown` if they have no preference; routing then uses any signed-in session the current assistant already has. ChatGPT and Codex are the same app — do not record them as two different browsers. This is how a ChatGPT-app user keeps that browser as *their* default without hardcoding it for every other install.

## Rules

- Ask; never guess. If the user doesn't know a setting, mark it `unknown` in the file rather than inventing a default, and note that skills will ask when it matters.
- Preserve `leagues.md` as the contract. Keep the existing core bullets (`Platform`, `Teams`, `Scoring`, `Starters`, `Bench`, `Waivers`, and so on) and add detail with additional bullets rather than renaming or replacing the established ones.
- Multiple leagues get one section each in the same file. Ask which league is the "default" and mark it — other skills use the default when the user doesn't specify.
- `leagues.md` may contain the user's real league and team names. That is expected — it lives only in their project. Recommend adding `leagues.md` to `.gitignore` if the project is a public repo.
- Prefer the platform's exact wording for league IDs/keys and weird scoring or waiver rules. Freehand summaries are fine for explanation, but the file should preserve enough specificity that a later skill does not need to reinterpret it.
- Never ask for, store, or write passwords, session cookies, or platform credentials. League *settings* only.

## Worked example

User says: "Set up my league — it's a 10-team full PPR on Sleeper called Couch Commissioners, superflex, $200 FAAB."

A signed-in Sleeper tab is available, so read the league settings page first. Interview only the gaps the page does not show (which league is default, Preferred browser, team name if ambiguous), then write:

```markdown
# Fantasy League Configuration

## League: Couch Commissioners (default)

- Season: 2026
- Platform: sleeper
- Platform league ID/key: 987654321098765432
- Timezone: America/New_York
- Verified: 2026-08-04 via Sleeper league settings page
- Teams: 10
- Scoring: ppr (superflex)
- Scoring details: 4-point passing TDs; TE premium none; points per carry none; return yards/TDs none; yardage bonuses none; long-play bonuses none; K none; DST none; IDP none; fractional scoring yes where Sleeper applies; negative scoring only for turnovers
- Median scoring: no
- Starters: 1 QB, 2 RB, 2 WR, 1 TE, 1 FLEX (RB/WR/TE), 1 SUPERFLEX (QB/RB/WR/TE)
- Bench: 6, IR: 2
- Draft: snake, 2026-09-01 20:00 America/New_York, 90-second clock
- Waivers: faab, budget $200, $0 bids allowed, runs daily at 03:00 America/New_York, after-run FCFS until player lock, equal-bid ties break by waiver priority
- Acquisition limit: none
- Playoffs: weeks 15-17, 6 teams
- Trade review: none
- FAAB tradeable: no
- Keepers: none
- Trade deadline: week 12
- My team: The Replacements
- Preferred browser: unknown
```

Finish by telling the user the file is ready and that draft, waiver, and trade skills will now use it automatically.
