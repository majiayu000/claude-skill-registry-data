---
name: nash-equilibrium-solver
description: "Models a strategic interaction as a normal-form (or extensive-form) game, identifies pure-strategy and mixed-strategy Nash equilibria, applies dominance and iterated elimination, checks subgame perfection, and translates the equilibrium back into a recommended action. Use when analyzing a pricing war; making capacity or market entry decisions; planning a bidding strategy; reading negotiation dynamics; or modeling any interaction of two or more parties where each player's best move depends on what others do."
---

# Nash Equilibrium Solver

> Turns a strategic situation into a game, solves it, and translates the equilibrium into a recommended move.

## What this skill is

A workflow that formalizes a real-world strategic interaction as a game - players, actions, payoffs - then solves for pure and mixed-strategy Nash equilibria, applies Iterated Elimination of Dominated Strategies (IEDS), checks Subgame-Perfect Equilibrium (SPE) in extensive form, and tests robustness to information assumptions. Produces a recommendation grounded in equilibrium analysis, not intuition.

## What it solves

- Strategic decisions made without modeling the other side's best response
- "What would I do?" reasoning that ignores the opponent's incentives
- One-shot intuition applied to repeated-game situations (or vice versa)
- Confusion between dominant-strategy equilibria and Nash equilibria
- Multiple-equilibrium situations where the recommendation must pick one credibly

## When to invoke

- Pricing decisions where competitor response is decisive
- Capacity or supply commitments in a concentrated industry
- Bidding strategy in auctions and tenders
- Market entry or exit decisions
- Negotiation preparation where multiple equilibria are credible
- Regulatory or policy interactions

## Phase 1: Define the game

Specify five elements:
- **Players** - every party whose decision matters (don't omit the regulator, the customer, the partner)
- **Actions** - discrete options per player; group continuous decisions into representative levels
- **Information** - complete or incomplete; perfect or imperfect; simultaneous or sequential
- **Timing** - one-shot or repeated; finite or infinite horizon
- **Payoffs** - quantified outcomes per action combination, in a common metric (profit, market share, utility)

Document every assumption. Bad payoff estimates make the equilibrium meaningless.

## Phase 2: Choose the representation

| Game type | Use | Tool |
|-----------|-----|------|
| Simultaneous, complete information | Normal form (payoff matrix) | n-dimensional matrix |
| Sequential, complete information | Extensive form (game tree) | Tree with payoffs at leaves |
| Incomplete information | Bayesian game | Type distributions |
| Repeated interaction | Stage game plus folk theorem | Discount factor δ |

Start with the simplest representation that captures the strategic essence.

## Phase 3: Apply dominance

For each player, eliminate **strictly dominated** strategies (always worse than another strategy regardless of others' actions). Then iterate.

Iterated Elimination of Dominated Strategies (IEDS) often solves the game without further machinery. If a unique strategy survives for each player, that profile is the equilibrium.

Note: **weakly dominated** strategies can survive in equilibrium - be careful eliminating them.

## Phase 4: Find pure-strategy Nash equilibria

A pure-strategy Nash equilibrium (NE) is a profile where no player can improve by unilaterally deviating.

Procedure for a normal-form game:
- For each cell, check whether the row player would deviate row-wise
- For each cell, check whether the column player would deviate column-wise
- A cell where neither would deviate is a pure NE

A game may have zero, one, or multiple pure NE. **Always report all of them**.

## Phase 5: Find mixed-strategy Nash equilibria

If a pure NE doesn't exist or is unsatisfactory, solve for the mixed-strategy equilibrium.

For a 2-by-2 game with players A (rows) and B (columns):
- Let p = probability A plays strategy 1
- Let q = probability B plays strategy 1
- Set A's expected payoffs equal so B is indifferent (solves for q)
- Set B's expected payoffs equal so A is indifferent (solves for p)

For larger games, use support enumeration or numerical solvers (Gambit, nashpy in Python).

Interpret the mixed strategy:
- In a one-shot game, the player literally randomizes
- In a repeated game, the mix represents the long-run frequency of pure-strategy choices
- In a populations game, the mix represents the share of the population playing each strategy

## Phase 6: Extensive form - subgame perfection

For sequential games, the standard NE concept is too weak (it allows non-credible threats). Use **Subgame-Perfect Equilibrium (SPE)** via backward induction:

1. Start at the terminal nodes
2. Pick the action giving the highest payoff to the player whose move it is
3. Replace the subgame with that payoff
4. Repeat until you reach the root

The path traced is the SPE. Any "threats" off the path are non-credible if they would require a player to act against their own interest.

## Phase 7: Equilibrium refinements and selection

When multiple equilibria exist, apply refinements:
- **Subgame perfection** - eliminates non-credible threats
- **Pareto dominance** - pick the equilibrium that everyone weakly prefers (when it exists)
- **Risk dominance** - pick the equilibrium that is the safer choice under uncertainty about others
- **Focal point (Thomas Schelling)** - convention, salience, history (e.g., split 50/50)
- **Forward induction** - actions reveal beliefs

State which refinement you applied and why.

## Phase 8: Robustness checks

Before recommending:
- Sensitivity: how does the equilibrium change with ±20% payoffs?
- Information asymmetry: what if the opponent has private information?
- Repeated interaction: does folk-theorem cooperation become available?
- Outside option: what's the Best Alternative to a Negotiated Agreement (BATNA) or disagreement payoff?
- Behavioral deviations: would loss-aversion, social preferences, or framing shift the equilibrium?

Equilibria that flip on small payoff changes are fragile - flag them.

## Output

- Game specification (players, actions, information, payoffs)
- Normal-form matrix or extensive-form tree
- Dominance elimination trace
- All pure-strategy Nash equilibria
- Mixed-strategy equilibria with derivation
- SPE for sequential games via backward induction
- Equilibrium selection reasoning if multiple exist
- Sensitivity and robustness commentary
- Recommended action with explicit caveats

## Operating rules

**Always**
- Specify all five game elements before solving
- Apply iterated dominance before searching for NE
- Report all equilibria, not just the convenient one
- Use subgame perfection for sequential games
- Run sensitivity on payoff assumptions

**Never**
- Recommend the row player's best cell without checking column player's deviation
- Treat the unique pure NE as the answer if mixed NE also exist
- Use non-credible threats in extensive-form recommendations
- Confuse Pareto-optimal with equilibrium
- Apply one-shot logic to a clearly repeated interaction
