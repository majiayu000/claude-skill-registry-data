---
name: simulate-economy-monte-carlo
description: "Use when running economy balance simulations to detect hyperinflation, player bankruptcy, or resource scarcity in game economy designs."
---

# simulate-economy-monte-carlo - Skill Definition

## 1. Overview

Runs Monte Carlo simulations to detect economic imbalances in game economy designs. Models player behavior archetypes, simulates resource flow across playtime milestones, and identifies hyperinflation, bankruptcy risks, and resource scarcity. Output: data-driven `economy_simulation.md` with P5/P95 wealth percentiles and actionable balance recommendations.

## 2. When to Use

Use when:
- You have an economy design (income sources, sinks, drop rates) and want to detect imbalances before launch.
- Players are experiencing hyperinflation, bankruptcy, or resource scarcity in live or test environments.
- You need P5/P95 wealth percentiles and data-driven balance recommendations across playtime milestones.

Do not use when:
- Economy inputs are purely qualitative with no numbers — gather quantitative estimates first.
- The game has no persistent economy or player-held currency.

## 3. Triggers & Red Flags

* **Triggers**: `simulate-economy-monte-carlo`, `economy balance`, `inflation`, `player money flow`, `economy simulation`, `Monte Carlo`, `economic balance`, `resource sink`, `money printer`.
* **Red Flags**:
    * **Hyperinflation Detected**: Rapid growth of P95 wealth relative to content progression (the "Money Printer" effect).
    * **High Bankruptcy Rate**: A significant percentage of players hitting zero or negative resources during early milestones.
    * **Resource Hoarding/Stagnation**: High concentration of total currency held by a small group, leading to scarcity for the majority.

## 3. Core Pattern

1. **Variable Definition** — Gather income sources, expense sinks, drop rates, and starting resources.
2. **Persona Modeling** — Define distinct player archetypes (e.g., Min-Maxer, Casual Explorer, Whale) with behavioral weights.
3. **Simulation Execution** — Run high-iteration simulations across key playtime milestones (e.g., 1h, 10h, 50h).
4. **Statistical Analysis** — Calculate P5/P95 wealth percentiles, bankruptcy rates, and hoarding metrics.
5. **Reporting** — Export the finalized simulation report to `{TARGET_FOLDER}/docs/economy_simulation.md`.

## 4. Intercepts & Guards

* **[Vague Data Intercept]**: If economic inputs are qualitative (e.g., "players get a lot of gold"): *"To run a valid simulation, I need quantitative values. Could you provide estimated gold amounts for quest rewards or item costs?"*
* **[Extreme Imbalance Intercept]**: If initial data suggests immediate massive failure: *"The current input parameters suggest a >50% bankruptcy rate in the first hour. Should we adjust starting resources or increase income before running the full simulation?"*

## 5. Strategic Imperative

**Prioritize percentiles (P5/P95) over averages.** Averages hide the volatility that breaks games; always focus on capturing the worst-case player experiences to ensure economic robustness.
