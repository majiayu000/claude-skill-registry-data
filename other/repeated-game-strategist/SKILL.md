---
name: repeated-game-strategist
description: "Analyzes repeated-game interactions - competitor dynamics, partner trust, supplier-buyer relationships - using the folk theorem, tit-for-tat (TFT), grim trigger, discount-factor analysis, and reputation effects to recommend a sustainable strategy. Use when designing a long-running competitive posture; structuring a multi-period partnership; deciding whether to retaliate against a defection; building a vendor relationship strategy; or planning repeated-bid procurement."
---

# Repeated Game Strategist

> One-shot logic destroys value in repeated interactions. This skill chooses the strategy that survives the long run.

## What this skill is

A workflow for analyzing repeated interactions (competitors, partners, suppliers, customers, internal teams) where the same parties meet again and again. Applies the folk theorem, computes the critical discount factor for cooperation to be sustainable, evaluates classic strategies - Tit-for-Tat (TFT), grim trigger, generous TFT, and win-stay-lose-shift (Pavlov) - and recommends a policy with explicit triggers for retaliation, forgiveness, and reset.

## What it solves

- Treating repeated competitive moves with prisoner's-dilemma defection logic
- Retaliating reflexively to noise (treating an accident as deliberate defection)
- Never retaliating to genuine defection (training the other side to keep defecting)
- Cooperation strategies that unravel in finite horizons without commitment
- Ignoring reputation effects when private information enters the game

## When to invoke

- Setting a multi-year competitive posture (cooperate or compete on which dimensions)
- Structuring an ongoing supplier or partner relationship
- Designing a retaliation policy when a competitor breaks an implicit norm
- Procurement strategy with repeat suppliers
- Internal team dynamics (cross-functional cooperation patterns)
- Customer retention strategies with renegotiation cycles

## Phase 1: Specify the repeated interaction

- **Players** - typically 2; multi-player is harder to coordinate
- **Stage game** - payoff matrix for one round
- **Time horizon** - finite (and known? unknown?) or infinite
- **Frequency** - how often does the game repeat?
- **Discount factor δ** - how much do future payoffs count?
  δ ≈ 1 / (1 + discount rate per period)
- **Observability** - can each player perfectly observe the other's action? With what lag?
- **Noise** - can actions or outcomes be misinterpreted?

If the stage game is not a true social dilemma (cooperation Pareto-dominates one-shot Nash equilibrium), repeated-game analysis adds little.

## Phase 2: Identify the cooperation gain

Compute payoffs in each state:
- (C, C) - both cooperate
- (D, D) - both defect (one-shot Nash equilibrium)
- (C, D) - you cooperate, they defect (sucker payoff)
- (D, C) - you defect, they cooperate (temptation payoff)

Standard Prisoner's Dilemma (PD) ranking: T > R > P > S, where R = mutual cooperation, T = temptation, P = mutual punishment, S = sucker.

The **cooperation gain** = R − P, sustained over many periods.

## Phase 3: Critical discount factor

For cooperation under grim trigger:

```
δ ≥ (T − R) / (T − P)
```

If your δ exceeds this threshold, cooperation is sustainable. If not, you need a different mechanism or to accept the one-shot equilibrium.

Levers to raise δ:
- Longer time horizon (extend the relationship)
- Higher frequency of interaction
- Lower volatility (more stable future)
- Higher value of the relationship to each party

Levers to lower δ (when you want to break a collusive equilibrium against you):
- Bring in a third player who plays one-shot
- Shorten the time horizon (signal exit)
- Reduce observability (harder to detect defection)

## Phase 4: Choose a strategy

| Strategy | Mechanism | Strength | Weakness |
|----------|-----------|----------|----------|
| **Always cooperate** | Unconditional C | Maximizes mutual gain if other reciprocates | Exploited by any defector |
| **Always defect** | Unconditional D | Robust to exploitation | Forfeits cooperation gain |
| **Tit-for-Tat (TFT)** | Cooperate first, then copy opponent | Nice, retaliatory, forgiving, clear | Locks into mutual defection on a single error |
| **Generous TFT** | TFT but occasionally forgives a defection | Recovers from noise | Slightly exploitable |
| **Grim trigger** | Cooperate until first defection, then defect forever | Maximum deterrence | Catastrophic on a single error or noise |
| **Win-stay, lose-shift (Pavlov)** | Repeat last action if it paid; switch otherwise | Strong in noisy environments | Cooperates with unconditional defectors |
| **Tit-for-two-tats** | Defect only after two consecutive defections | Robust to noise | Slow to deter sustained defection |

Decision guide:
- High observability plus low noise → TFT or grim trigger
- Noisy observation → generous TFT, tit-for-two-tats, or Pavlov
- Finite known horizon → reputation effects required to avoid unraveling

## Phase 5: Reputation effects (incomplete information)

In a finite-horizon game, cooperation unravels via backward induction - unless players have private information about their type.

The Kreps-Milgrom-Roberts-Wilson reputation effect: if there's a small probability you're a "crazy" TFT type, even a rational opponent will cooperate for most of the finite horizon.

Implication: invest in **reputation** - observable history of cooperation, slow forgiveness, transparent retaliation - to make the "crazy type" prior credible.

## Phase 6: Retaliation policy

Define when to retaliate, how hard, for how long, and when to reset:

| Element | Question | Recommendation |
|---------|----------|----------------|
| Trigger | What action constitutes defection? | Specific, observable, public |
| Detection threshold | How sure must we be? | Higher with noise |
| Severity | How proportionate? | Tit-for-tat scale |
| Duration | How long? | Just long enough to restore deterrence |
| Forgiveness | When do we return to cooperation? | After observable peace gesture |
| Public posture | Do we announce retaliation? | Yes - improves deterrence |
| Asymmetric cost | What's the cost to you of retaliating? | Don't escalate beyond your sustainable cost |

## Phase 7: Multi-player extensions

When more than two players interact:
- Cooperation harder to sustain (more chances for someone to defect)
- Need monitoring across many players
- Standards, norms, and industry conventions emerge as coordination devices
- Public statements can serve as commitment to multilateral enforcement
- Watch for legal and regulatory limits on tacit coordination among competitors

## Output

- Game specification: stage payoffs, horizon, frequency, δ, observability, noise
- Critical discount factor and whether cooperation is sustainable
- Recommended strategy from the strategy table with reasoning
- Retaliation policy: trigger, severity, duration, forgiveness, public posture
- Reputation investment plan
- Trigger conditions to revisit the strategy (e.g., observed pattern change)
- Watch-list: behaviors that would force a switch in strategy

## Operating rules

**Always**
- Compute the critical discount factor before recommending cooperation
- Match the strategy to the noise level
- Define a public, proportional retaliation policy
- Invest in reputation when horizon is finite
- Distinguish a single accident from a defection pattern

**Never**
- Apply one-shot logic to a clearly repeated game
- Choose grim trigger in a noisy environment
- Retaliate on insufficient observation
- Defect at the announced last round (it unravels backward)
- Confuse tacit coordination with legal collusion among competitors
