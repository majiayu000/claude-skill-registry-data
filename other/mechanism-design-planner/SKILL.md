---
name: mechanism-design-planner
description: "Designs auctions, matching mechanisms, pricing schemes, and incentive structures using mechanism-design principles - Incentive Compatibility (IC), Individual Rationality (IR), revenue equivalence, and budget balance. Use when designing a marketplace pricing model or referral program; allocating internal resources; running a Request for Proposal (RFP) or procurement process; choosing an auction format; or setting any allocation rule where participants act strategically."
---

# Mechanism Design Planner

> Reverse-engineers the rules so that participants acting in their own interest produce the outcome you want.

## What this skill is

A workflow that frames an allocation problem as a mechanism-design problem, surfaces the design objectives (efficiency, revenue, fairness, simplicity), picks the right mechanism class (first-price, second-price, Vickrey-Clarke-Groves (VCG), posted-price, matching, scoring auction), checks the canonical properties (Incentive Compatibility (IC), Individual Rationality (IR), budget balance, no-deficit), and stress-tests against collusion and gaming.

## What it solves

- Mechanisms that are gamed because participants have private information and weak incentives to reveal it
- Auctions that maximize revenue in theory but kill participation in practice
- Pricing models that look optimal until customers stop adopting
- Allocation rules that produce inefficient outcomes (the wrong party wins)
- Programs (referrals, compensation plans, Requests for Proposal (RFPs)) that produce unintended behaviors

## When to invoke

- Designing a marketplace pricing model (commissions, dynamic pricing, surge)
- Procurement or RFP design where bidders are strategic
- Auction format decisions (English, sealed-bid, second-price, combinatorial)
- Internal resource allocation (compute quota, headcount, budget)
- Matching problems (school choice, dorm assignment, kidney exchange, marketplace pairing)
- Incentive compensation, referral programs, bug bounties

## Phase 1: State the problem formally

- **Participants** - buyers, sellers, candidates, applicants
- **Private information** - what does each participant know that others (and the designer) don't?
- **Allocation outcome** - what is being allocated and to whom?
- **Transfers** - what payments or rewards move between parties?
- **Designer's objective** - efficiency, revenue, fairness, participation, simplicity (pick 1-2 primary)
- **Constraints** - budget, legal, computational, fairness

Without explicit private information, mechanism design doesn't apply - it's just an allocation rule.

## Phase 2: Specify desired properties

Choose which properties the mechanism must satisfy:

| Property | Definition | When critical |
|----------|-----------|---------------|
| **Incentive Compatibility (IC)** | Truth-telling is a (dominant or Bayesian) best response | Always desirable; near-mandatory at scale |
| **Individual Rationality (IR)** | Participating beats opting out for each type | Required for voluntary participation |
| **Pareto efficiency** | No reallocation makes everyone weakly better off | Welfare-maximizing settings |
| **Budget balance** | Mechanism's payments sum to zero (or non-positive) | Self-sustaining without subsidy |
| **No-deficit** | Mechanism doesn't lose money | Weaker than budget balance |
| **Strategy-proofness** | Truth is a dominant strategy | When robust simplicity matters |
| **Pareto optimality of matching** | No coalition can improve via reassignment | Matching markets |

Standard tension: efficiency, IR, IC, and budget balance simultaneously is often impossible (the Myerson-Satterthwaite result for bilateral trade). State the trade-off explicitly.

## Phase 3: Pick a mechanism class

| Class | Use case | Notes |
|-------|----------|-------|
| **English (open ascending)** | Single-item, transparent, common | Familiar; reveals second-highest value |
| **Sealed-bid first-price** | Single-item, sealed, paid own bid | Shading optimal; complex strategy |
| **Sealed-bid second-price (Vickrey)** | Single-item, sealed, paid 2nd price | Truth-telling is a dominant strategy (IC) |
| **Vickrey-Clarke-Groves (VCG)** | Multi-item, combinatorial | IC plus efficient; revenue may be low; complex |
| **Posted-price** | Many small buyers, low-friction | Loses revenue from high-value buyers; simple |
| **Scoring auction** | Multi-attribute (price plus quality plus delivery) | Common in procurement |
| **Combinatorial** | Bundle allocations (spectrum, gates) | Computationally hard; needs careful design |
| **Deferred-acceptance (Gale-Shapley)** | Two-sided matching (schools, residencies) | Strategy-proof for proposing side |
| **Top trading cycles** | Pareto-efficient matching with priorities | Strategy-proof; efficient |

Pick the mechanism whose properties match your objectives.

## Phase 4: Revenue equivalence and expected outcomes

The Revenue Equivalence Theorem: under standard assumptions (risk-neutral bidders, Independent Private Values (IPV), symmetric, no reserve), all efficient single-item auctions yield the same expected revenue to the seller.

Implication: format choice is often **not** about expected revenue - it's about variance, transparency, complexity, IC, and resistance to collusion.

Compute under the chosen mechanism:
- Expected efficiency (probability the highest-value participant wins)
- Expected revenue (closed-form for standard auctions; simulation for non-standard)
- Expected participation (do all types prefer joining?)
- Worst-case loss or regret

## Phase 5: Reserve prices, fees, and quotas

- **Reserve price** - minimum price; trades efficiency for revenue (excludes low-value buyers)
  - The Myerson optimal reserve: where marginal revenue equals zero; depends on value distribution
- **Entry fee** - screens out low-value participants; can reduce participation
- **Quotas or caps** - limit allocation per participant; useful in matching to prevent monopolization
- **Subsidies** - encourage participation on the thin side of the market

Each lever has efficiency, revenue, and participation trade-offs. Quantify each.

## Phase 6: Collusion and gaming resistance

Stress-test the mechanism:
- **Bid rotation** - bidders take turns winning
- **Sham bidding** - phantom bidders inflating second-price auctions
- **Coordination via signaling** - early bids signaling intentions (open auctions susceptible)
- **Sniping** - last-second bids in soft-close auctions
- **Misreporting** - overstating need to get a larger allocation
- **Reverse-engineering scores** - gaming a scoring formula

Design defenses:
- Hard close versus soft close
- Anonymous bidders
- Sealed versus open
- Reserve plus proxy bids
- Audit plus penalty
- Periodic re-randomization

## Phase 7: Simulate before launch

For any non-trivial mechanism, simulate:
- 1,000+ trials with realistic participant value distributions
- Stress with strategic and non-strategic mix
- Compute mean and worst-case allocation efficiency
- Compute revenue distribution, not just expected revenue
- Test edge cases: thin participation, lopsided value distributions, single dominant bidder

## Output

- Problem statement: participants, private information, allocation, transfers, objective
- Property requirements with explicit trade-offs noted
- Recommended mechanism class with reasoning
- Parameter settings: reserve, fees, quotas
- Expected outcomes: efficiency, revenue, participation
- Collusion and gaming threat map with mitigations
- Simulation results across realistic scenarios
- Launch plan with monitoring metrics to detect manipulation

## Operating rules

**Always**
- State the private information explicitly
- Choose 1-2 primary objectives (efficiency, revenue, fairness, simplicity)
- Pick a mechanism whose properties match the objectives
- Stress-test against collusion and gaming
- Simulate before launch

**Never**
- Use first-price when truthful revelation matters
- Promise efficiency, IR, IC, and budget balance simultaneously for bilateral trade
- Skip reserve-price tuning
- Launch a complex mechanism without participant simulation
- Ignore behavioral deviations from rational play
