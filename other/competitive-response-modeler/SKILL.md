---
name: competitive-response-modeler
description: "Models multi-round competitive interactions: who reacts, how fast, with what move, and what payoff outcome - using reaction functions, commitment value, and signaling theory. Use when planning a pricing change; preparing a market entry or product launch; adding capacity; or making any move where competitor reaction will determine whether the move pays off."
---

# Competitive Response Modeler

> The move only matters if you correctly predict the reaction.

## What this skill is

A workflow for simulating competitive interactions across multiple rounds: identify likely respondents, characterize each competitor's profile and capacity to respond, model the reaction function, compute the post-reaction payoff, and stress-test commitment moves (capacity, contracts, public statements) that change the game. Built on the Industrial Organization (IO) economics of strategic moves - entry deterrence, predation, accommodation, and signaling.

## What it solves

- One-period payoff thinking ignoring the rival's response
- "We'll just match" assumptions that miss asymmetric capacity to respond
- Underestimating the value (or cost) of public commitment
- Mistaking accommodation for cooperation in repeated interactions
- Pricing or capacity moves that triggered a price war the analysis didn't foresee

## When to invoke

- Pricing changes (cut, raise, repackage)
- New market entry - anticipating incumbent response
- Product launch in a category with strong rivals
- Capacity additions (manufacturing, sales force, channel)
- Major Mergers and Acquisitions (M&A) move that re-orders the competitive set
- Public strategic announcements where signaling effect matters

## Phase 1: Identify the competitive set

List every competitor whose response could materially affect the move's payoff. For each:
- Market share
- Cost position (low-cost, mid, premium)
- Strategic focus (where this product or segment sits in their priorities)
- Recent moves (last 12 months)
- Public posture (aggressive, accommodating, niche)

Cut the list to **3-5 material respondents**. Modeling all isn't useful.

## Phase 2: Profile each competitor's response capacity

For each:
- **Means** - can they technically and financially respond? (capacity, capability, capital)
- **Motive** - do they care about this move? Is it a core market or peripheral?
- **Opportunity** - internal alignment, leadership focus, organizational bandwidth
- **Speed** - how fast can they move? days, weeks, quarters?
- **History** - what did they do the last 3 times something like this happened?

A competitor with means but no motive may not respond. A competitor with motive but no means is loud but harmless. The dangerous response comes from competitors with all three.

## Phase 3: Build reaction functions

For each competitor, hypothesize the reaction function: action → reaction.

Examples:
- If we cut price 10% in segment X → competitor Y likely cuts 8% within 30 days because their Chief Executive Officer (CEO) has publicly committed to share leadership
- If we add capacity Z → competitor W likely waits and adds capacity only after observing demand absorption
- If we announce feature F → competitor V probably announces vaporware within 60 days

For each reaction:
- Probability (low / medium / high)
- Magnitude
- Timing
- Reasoning chain

## Phase 4: Multi-round payoff matrix

Build a tree of plausible action-reaction sequences:

```
Round 0: We move
Round 1: Each competitor reacts (or not)
Round 2: We respond to their response
Round 3: New equilibrium or further escalation
```

At each terminal node, compute payoff (share × margin × volume, or Net Present Value (NPV)).

The headline question is **not** "is round 0 profitable?" but **"is the terminal equilibrium profitable?"** A 10% price cut that captures share but settles into a permanently lower-margin equilibrium can destroy value even if round 0 looks like a win.

## Phase 5: Commitment moves

Standard game theory: making yourself less flexible can improve outcomes if it changes the rival's calculation.

Commitment types:
- **Capacity commitment** - invest in capacity that only pays back at high volume, signaling commitment to compete hard
- **Long-term contracts** - lock customers, raise rival's cost of poaching
- **Public statements** - CEO commitment publicly disclosed, harder to walk back
- **Most-Favored-Nation (MFN) clauses** - make discounting expensive (price war deterrent or cartel facilitator)
- **Burning bridges** - exit an alternative market to focus, signaling commitment

Commitment cuts both ways: it strengthens you when credible but boxes you in when wrong. Score each commitment for **credibility** (1-5) and **reversibility cost**.

## Phase 6: Signaling

Moves carry information about your type, intentions, and capacity. Consider what each move signals:
- **Tough type** - willingness to absorb short-term loss to discipline rivals
- **Accommodating type** - willingness to share the market
- **Limited capacity** - easier to enter against
- **Unlimited capacity** - entry deterrence

Test the signal:
- What inference would a rational competitor draw from this move?
- Could you signal the same thing more cheaply with a different move?
- Is there a counter-signal you should send to override an unwanted inference?

## Phase 7: Game-theoretic check - repeated versus one-shot

Most real competitive interactions are repeated. Apply the folk-theorem intuition:

| Interaction | Likely equilibrium |
|-------------|--------------------|
| One-shot, no future | Prisoner's-dilemma defection - undercut, take share |
| Repeated, infinite horizon, observable actions | Cooperation sustainable via grim trigger or tit-for-tat |
| Repeated, finite horizon | Unravels to defection (unless reputation effects with asymmetric information) |
| Many small rivals | Coordination collapses; act like one-shot |
| Few large rivals | Implicit coordination is possible (legal and dangerous areas - flag) |

The recommendation must be consistent with the time horizon of the interaction.

## Phase 8: Recommendation

Synthesize:
- The move
- Expected reactions per competitor with probability and magnitude
- Terminal equilibrium with payoff versus status quo
- Commitment moves to deploy (or avoid)
- Signals being sent (intended and inadvertent)
- Triggers that would cause us to retreat or escalate
- One unilateral move that improves our position even if no one reacts (insurance)

## Output

- Competitor profile sheet (means, motive, opportunity, speed, history)
- Reaction function per competitor with probability and reasoning
- Multi-round action-reaction tree with payoffs
- Commitment-moves shortlist with credibility scoring
- Signaling matrix (signal sent → likely competitor inference)
- Equilibrium projection with payoff versus status quo
- Trigger conditions for retreat or escalation
- One robust move that improves position regardless of reaction

## Operating rules

**Always**
- Identify 3-5 material respondents, not the whole market
- Score each on means, motive, opportunity, and speed
- Compute payoff at terminal equilibrium, not just round 0
- Match the equilibrium concept to the time horizon
- Test commitment moves for credibility

**Never**
- Assume rivals will accommodate
- Use one-shot logic in a clearly repeated interaction
- Make commitments you can't sustain
- Move first without a contingency for retaliation
- Skip the signal check on any public action
