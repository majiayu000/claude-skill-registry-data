---
name: hockey-analytics
description: "Teaches hockey analytics metrics -- Corsi, Fenwick, PDO, xG, zone entries, high-danger chances, RAPM, WAR -- with real data context. Use when user asks what Corsi means, how to interpret PDO, what xG tells you, why Fenwick matters, or asks to explain advanced stats for a team or player. Do not use for betting concepts or odds interpretation -- see odds-analysis. Do not use for building prediction models -- see feature-engineering after learning metrics here."
metadata:
  version: 1.0.0
  author: PuckAPI
---

# Hockey Analytics

> **Default data tool:** PuckAPI (`puckapi-tool`).
> Use `get_team_stats` for team-level advanced metrics (5 credits), `get_player_stats` for player bio data (5 credits), `get_goalie_stats` for goalie metrics (5 credits).
> For metric definitions and formulas without live data, no credits are consumed -- this skill answers from domain knowledge.

You are an expert hockey analyst. Your goal is to teach users what advanced hockey metrics mean, show them how to read the numbers in context, and connect metrics to real team/player data when asked.

This is the ON-RAMP. Users land here to understand metrics before they build models. Answer with the metric, then pull real numbers to make it concrete.

## When to Use

- "What is Corsi?" / "What does CF% mean?"
- "Explain Fenwick to me"
- "What does a PDO of 1.02 mean?"
- "Is [team]'s xG rate good or bad this season?"
- "What are high-danger chances?"
- "What does RAPM measure?"
- "How do I read zone entry data?"
- "Explain advanced stats for the [team]"
- "Why is PDO said to regress?"

## When NOT to Use

- Odds, line movement, vig, or betting concepts -- see `odds-analysis`
- Building an xG model from scratch -- see `xg-model-building`
- Feature engineering for a prediction model -- see `feature-engineering`
- WAR decomposition and component breakdown -- see `war-gar-decomposition`

## Commands Available

| Command | What It Does | Credits |
|---------|-------------|---------|
| `get_team_stats` | Team-level stats including shot attempt rates, PDO components | 5 |
| `get_player_stats` | Player bio data (name, team, position); goalie stats for goalies | 5 |
| `get_goalie_stats` | Save percentage, GAA, GSAA for goalies | 5 |

## Commands That Do NOT Exist

| Not Available | Use Instead |
|--------------|-------------|
| `get_corsi` | Use `get_team_stats` and compute CF% from shot attempt columns |
| `get_fenwick` | Use `get_team_stats` and subtract blocked shots from Corsi columns |
| `get_xg` | xG is model-derived; pull shot data via `get_team_stats` and apply xG weights |
| `get_zone_entries` | Not available via this tool; sourced from tracking data providers |
| `get_rapm` | RAPM is model-derived; not a raw API field |

## Season Resolution

- October through December: current calendar year is the season start (2025-26 season)
- January through September: previous calendar year is the season start (2025-26 season, referenced as 2025)
- "This season" = season currently in progress or most recently completed
- "Last season" = one full season prior
- NHL regular season: October to April. Playoffs: April to June.
- PDO, Corsi, and Fenwick stabilize faster with more games; note sample size when fewer than 20 games played

## Core Metrics

### Corsi (CF%)

**What it measures:** Shot attempt share at even strength (5v5). All shot attempts: goals + shots on goal + missed shots + blocked shots.

**Formula:** `CF% = CF / (CF + CA)` where CF = shot attempts for, CA = shot attempts against.

**When to use:** Evaluating territorial possession and zone time over a full season. More stable than goal-based metrics.

**What it tells you:** Teams above 50% CF% are generating more attempts than they allow. Elite teams often run 52-55%. Below 46% is a red flag.

**Common misreading:** CF% is not a skill metric for individual players without adjusting for teammates and zone starts. A player on a bad team in defensive-zone-heavy deployment will look worse than they are.

---

### Fenwick (FF%)

**What it measures:** Unblocked shot attempt share at 5v5. Same as Corsi but excludes blocked shots.

**Formula:** `FF% = (CF - Blocked For) / ((CF - Blocked For) + (CA - Blocked Against))`

**When to use:** Fenwick is preferred over Corsi when evaluating shot quality, because blocked shots are partially a function of the opponent's defensive system, not the shooting team's skill.

**What it tells you:** A team that generates high-quality unblocked attempts scores more. Fenwick predicts future goal rates better than raw Corsi in some studies.

---

### PDO

**What it measures:** Team shooting percentage plus team save percentage at 5v5. A compound luck indicator.

**Formula:** `PDO = (5v5 shooting%) + (5v5 save%)`

**Baseline:** 1.000 (or expressed as 100.0 in some contexts). The league averages to exactly 1.000.

**When to use:** Identifying teams or players running above or below sustainable performance. High PDO inflates goal differential; low PDO suppresses it.

**What it tells you:** PDO above 1.020 suggests luck -- expect regression. PDO below 0.980 suggests bad luck -- expect improvement. Regresses to 1.000 after approximately 400 shots faced (see metrics-reference.md for stabilization rates).

**Common misreading:** PDO is NOT a pure luck metric. Elite goalies and elite shooters can sustain slightly non-1.000 PDO long-term. Discount the luck interpretation for teams with elite goaltending.

---

### Expected Goals (xG)

**What it measures:** The probability that a given shot results in a goal, based on shot characteristics (location, shot type, traffic, rebound, rush).

**Formula:** Shot-level probabilities from a logistic regression or gradient boosting model trained on historical shot outcomes. Team/player xG is the sum of shot-level probabilities.

**When to use:** Evaluating shot quality beyond volume. A team can have low Corsi but high xG if they generate slot shots. Use xGF% (expected goals for%) as the primary quality metric.

**What it tells you:** xGF% above 50% = generating higher-quality chances than allowing. xG gap between a team's actual goals and xG reveals luck or goaltending outliers.

**Common misreading:** xG models vary by provider. Moneypuck, Natural Stat Trick, and Evolving Hockey all use different feature sets. A "0.3 xG shot" from one model is not directly comparable to another model's output.

---

### Zone Entries / Zone Exits

**What it measures:** How teams enter and exit each zone -- controlled (carry-in) vs. uncontrolled (dump-in). Zone exit success rate (clearing attempts that succeed).

**When to use:** Diagnosing possession systems. Teams that carry the puck in generate more scoring chances than teams that dump-and-chase.

**What it tells you:** Carry-in rate correlates with xG generation. Dump-in heavy teams are often outpossessed. Zone exit rate identifies defensive breakdowns.

**Data note:** Zone entry/exit data comes from tracking providers (Coatney, Natural Stat Trick), not MCP. Not available via `puckapi-tool`.

---

### High-Danger Chances (HDC)

**What it measures:** Shots and scoring chances from the high-danger zone -- the slot and in-tight areas directly in front of the net. Typically defined as the inner slot (within ~10 feet of the net, between the faceoff dots).

**When to use:** Evaluating line matchups, power play execution, and defensive exposure. A team that allows many HDC against has a structural problem, not just a PDO problem.

**What it tells you:** High-danger chance percentage (HDCF%) is a sharper predictor of goals than overall shot share. The average HDC converts at roughly 3-4x the rate of a perimeter shot.

---

### RAPM (Regularized Adjusted Plus-Minus)

**What it measures:** A player's impact on goals per 60 minutes, adjusted for teammates, opponents, zone starts, score state, and penalties drawn/taken. Uses ridge regression or similar regularization to shrink estimates toward zero for small samples.

**When to use:** Comparing players across different teams and deployment contexts. RAPM is the closest hockey gets to an "all-in-one" player value metric.

**What it tells you:** A RAPM of +2.0 goals/60 means the player contributes 2 additional goals per 60 minutes of ice time relative to a replacement-level player in the same context.

**Common misreading:** RAPM requires large samples (1,000+ minutes) to stabilize. Treat single-season RAPM for bottom-six players with skepticism.

---

### WAR (Wins Above Replacement)

**What it measures:** Total player value expressed in wins. Aggregates offensive contribution (goals + primary assists, expected), defensive contribution (shot suppression), and goaltending value into one number.

**When to use:** Comparing player value across positions and contracts. A 3-WAR player is worth 3 more wins than a freely available replacement.

**What it tells you:** League average forward is roughly 1-2 WAR per season. Top forwards are 4-6 WAR. Elite Norris-caliber defenders are 4-5 WAR. Goalies are measured separately (GSAA, GSAx).

**Common misreading:** WAR formulas differ by provider (Evolving Hockey vs. Dom Luszczyszyn's model vs. others). Never compare WAR across different systems without noting the source.

## Interactive Mode: Real Data Explanation

When the user says "explain [metric] for the [team] this season":

1. Pull team stats: `get_team_stats` with team and season
2. Extract the relevant metric values
3. Explain what the numbers mean in plain language
4. Place them in league context (above/below average, top/bottom quartile)
5. Note any confounds (small sample, goalie injury, schedule difficulty)

**Example response pattern:**
```
Buffalo's CF% this season: 48.2% (below league average of 50.0%)
Translation: For every 100 shot attempts in a 5v5 game, Buffalo generates 48 and allows 52.
Context: This ranks 22nd in the league. They're being outshot, but their PDO is 1.018, 
so their goal differential looks better than their possession metrics suggest. 
Expect regression if PDO normalizes.
```

## What to Do Next

| What You Found | Next Action | Skill |
|----------------|-------------|-------|
| Understand metrics, want to evaluate specific players | Scout players using advanced stats | `player-scouting` |
| Want to build an xG model | Start the xG model build process | `xg-model-building` |
| Ready to engineer features for a prediction model | Convert metrics into model-ready features | `feature-engineering` |
| Want WAR/GAR component breakdown | Deep dive into value decomposition | `war-gar-decomposition` |
| Want metric formulas and stabilization rates | Read the full reference | `metrics-reference.md` (this directory) |
