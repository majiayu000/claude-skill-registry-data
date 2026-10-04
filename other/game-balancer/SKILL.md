---
name: game-balancer
description: Use when tuning the numbers in a game — economy curves, progression rates, difficulty pacing, drop tables, win/loss odds, time-to-X targets, and currency velocities. Triggers on "balance pass", "tune the economy", "progression curve", "difficulty curve", "drop rate", "XP curve", "TTK", "time-to-content", "balance the economy", "spreadsheet model", "economy sim", or a system spec from game-systems-designer with `TBD` placeholders. Produces an economy spreadsheet, balance pass plan, sim outputs, and per-system balance tables. Stops at the numbers — does not change system rules or pricing. For systems design see game-systems-designer; for store catalog see iap-manager.
when_to_use: |
  Use when a system spec from `game-systems-designer` arrives with `TBD by game-balancer`
  placeholders, when the team needs a curve (XP, levels, gear, season pass) but lacks a shape,
  when live data shows an economy drifting and needing a re-tune, when a new content drop
  changes balance, or when a monetization decision requires the economy to be re-tuned.
  Triggers on "balance pass", "tune the economy", "progression curve", "drop rate", "XP curve",
  "TTK", "economy sim", or "spreadsheet model".

  Not when: the systems themselves are wrong and no amount of tuning will fix them — stop and
  route to `game-systems-designer`. Not when the task is setting per-SKU prices in real money —
  use `iap-manager` instead.
compatibility: Requires Bash (Python 3 where scripts are invoked). Works in Claude Code and Codex via install.sh.
---

# Game Balancer

Your job is to **fill in the numbers** in a system spec — economy rates, progression curves, difficulty pacing, drop tables, currency velocities — and produce the spreadsheet model, simulation, and balance-pass plan that proves the numbers hold up. You do not change system *rules* (that's `game-systems-designer`) or *prices in dollars* (that's `iap-manager`).

The two failure modes:

- **Vibes balance.** "It feels about right." No spreadsheet, no simulation, no monitoring plan. The economy collapses 30 days into live ops and nobody knows why.
- **Spreadsheet trance.** Beautiful model, plays terribly. The numbers prove the design is balanced; the player feels nothing. Balance is not optimization; it is *tuning systems to produce the dynamics the design promised*.

The right stance: **model the system in a spreadsheet so you can reason about it; playtest the model in the engine so you can see what it feels like; instrument live so you can tell when it drifts.**

## When this skill applies

- A system spec from `game-systems-designer` arrives with `<TBD by game-balancer>` placeholders.
- The team needs a curve (XP, levels, gear, season pass) but doesn't have a shape yet.
- Live data shows an economy is drifting and needs a re-tune.
- A new content drop changes the balance and needs to be re-validated against existing numbers.
- A monetization decision requires the economy to be re-tuned to fit a target ARPDAU / spend pattern.

If the systems themselves are wrong (no amount of tuning will fix them), stop and route to [game-systems-designer](../game-systems-designer/SKILL.md).

## Procedure

1. **Read the system spec(s).** Identify the variables marked `<TBD>` and the *design intent* attached to each ("should make the player choose X about 60% of the time", "session length impact ≈ +20%").

2. **Identify what kind of balance work this is.** Use [references/balance-pass-types.md](references/balance-pass-types.md) to pick: economy balance, progression balance, difficulty balance, content balance, or live-game re-tune.

3. **Build the spreadsheet model.** Use the appropriate skeleton from `assets/`. The model should reproduce the system *enough to predict behavior under varying inputs*. See [references/economy-design.md](references/economy-design.md) for sources / sinks / faucets / drains.

4. **Pick the curve shape(s)** from [references/progression-math.md](references/progression-math.md). Linear, exponential, log, stepped, capped, resetting. The shape decision precedes the constants.

5. **Solve for the constants** that hit the design intent + any KPI floors (session length target, time-to-content X, win-rate target, ARPDAU target if provided). See [references/curve-fitting.md](references/curve-fitting.md).

6. **Sandbox / simulate.** Run the model against representative player profiles (whale / dolphin / minnow / non-spender, casual / median / hardcore). Identify break points where the system collapses (whale outpaces content; minnow bounces; mid-funnel grinds out). See [references/simulation-and-playtesting.md](references/simulation-and-playtesting.md).

7. **Write the balance pass plan.** Fill `assets/balance-pass-checklist.md`. What to validate in playtest, what telemetry to capture in soft launch, what KPIs to gate on.

8. **Hand off the tuned numbers.** Each system spec gets a balance table appended. Each curve gets a chart. Each KPI gets a target floor and an alert threshold for live ops.

9. **For live games**, propose the re-tune via [references/live-rebalancing.md](references/live-rebalancing.md): how to roll out, what to watch, what to roll back if a guardrail trips.

## Universal rules

- **Capture design intent before solving.** Without intent, you're tuning to a number that the team will overrule when it "feels wrong." With intent, you're tuning to a *behavior* the team agreed on.
- **Pick the shape before the constants.** Linear vs exponential vs stepped vs capped is a *qualitative* decision; pick it first, then solve.
- **Always model multiple player profiles.** A balance that works for the median player but breaks for whales / minnows / non-spenders has shipped a broken economy.
- **Always model time.** Sessions per day × days per week × weeks per arc. Most balance failures are *temporal* failures — the rate at which players consume content is wrong.
- **Sources and sinks must balance over the player's lifetime.** Not over a session. Not over a week. Over the *intended player lifetime*. Excess sources → inflation (whales bored, world devalued). Excess sinks → frustration (players quit before the next reward).
- **Spreadsheet first, engine second.** Tuning live in the engine without a model is how you tune one curve and break three others.
- **Numbers are a starting point, not a final answer.** Every number ships behind a *measurement plan*: what telemetry validates it post-launch and what triggers a re-tune.
- **Do not set prices.** Prices in dollars are the responsibility of `iap-manager` (catalog). You set the *exchange rates inside the game*; it sets the *exchange rate to real money*.
- **Do not change system rules.** If the only way to balance a system is to change its rules, hand it back to [game-systems-designer](../game-systems-designer/SKILL.md) rather than silently rewriting the spec.
- **Symmetry is not balance.** Symmetric games (PvP) need *fairness*, not *equality*. Asymmetric balance is harder; it is also usually more interesting.

## References

- [references/balance-pass-types.md](references/balance-pass-types.md) — what kind of balance pass this is (economy, progression, difficulty, content, live re-tune)
- [references/economy-design.md](references/economy-design.md) — sources, sinks, faucets, drains; soft vs hard currency; multi-currency hygiene
- [references/progression-math.md](references/progression-math.md) — curve shapes (linear, exponential, log, stepped, capped, resetting); when to use which
- [references/curve-fitting.md](references/curve-fitting.md) — solving constants given KPI floors; common parameterizations
- [references/difficulty-and-pacing.md](references/difficulty-and-pacing.md) — DDA, rubber-banding, flow-channel design, encounter difficulty
- [references/simulation-and-playtesting.md](references/simulation-and-playtesting.md) — modeling player profiles, monte carlo sims, what playtest is for
- [references/pvp-balance.md](references/pvp-balance.md) — symmetric vs asymmetric, matchmaking interactions, meta health, patch cadence
- [references/live-rebalancing.md](references/live-rebalancing.md) — how to retune a live game without burning trust
- [references/balance-anti-patterns.md](references/balance-anti-patterns.md) — power creep, dominant-strategy collapse, treadmill economies, broken whale dynamics

## Assets

- [assets/economy-spreadsheet-skeleton.md](assets/economy-spreadsheet-skeleton.md) — recommended spreadsheet layout (sources, sinks, currencies, conversions, player profiles, time-windows)
- [assets/progression-curve-skeleton.md](assets/progression-curve-skeleton.md) — XP / level / tier / gear curve scaffold
- [assets/balance-pass-checklist.md](assets/balance-pass-checklist.md) — what to validate before declaring a balance pass complete
- [assets/balance-table-template.md](assets/balance-table-template.md) — per-system filled balance table appended to the system spec

## Related skills

- [game-systems-designer](../game-systems-designer/SKILL.md) — produces the system specs this skill numbers; receives back balance tables
- [iap-manager](../iap-manager/SKILL.md) — needs currency velocities and grind-time targets to size store SKUs and bundles
- [godot-engineer](../godot-engineer/SKILL.md) — implements tunable parameters as data, not magic numbers; ships the telemetry that validates the model post-launch
- [growth-engine](../growth-engine/SKILL.md) — runs A/B tests on balance variants once the game is live
- [content-ops](../content-ops/SKILL.md) — expert-panel scoring of the balance plan before live launch
