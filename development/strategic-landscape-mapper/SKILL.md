---
name: strategic-landscape-mapper
description: "Builds a Strategic Landscape Map: a user-need value chain plotted against component maturity stages (novel → custom-built → productized → commoditized), with environmental forces, operating principles, and strategic plays identified. Use when designing platform strategy; deciding what to build, buy, or outsource; anticipating commoditization waves; planning multi-year technology investment; or aligning a leadership team on landscape and direction."
---

# Strategic Landscape Mapper

> Landscape mapping that shows where the terrain is moving, not just what it looks like today.

## What this skill is

A workflow that produces a Strategic Landscape Map: a user-need value chain from end customer down to commodity components, plotted on a maturity axis (novel → custom-built → productized → commoditized / utility). It applies environmental forces (the inevitable shifts you must account for), operating principles (universally applicable best practices), and strategic plays (deliberate moves) to recommend where to invest, what to outsource, and what to anticipate next.

## What it solves

- Strategy decks that have no map - only frameworks and slides
- Decisions to build in-house what is becoming commoditized (or vice versa)
- Missing the predictable transition from custom-built to productized to utility
- Confusing operational efficiency with strategic positioning
- Inability to communicate landscape to a leadership team in a single picture

## When to invoke

- Platform versus product strategy decisions
- Build, buy, or outsource trade-offs at scale
- Multi-year capital expenditure or technology investment planning
- Anticipating commoditization waves and the firms they will hurt
- Aligning a leadership team on the competitive landscape

## Phase 1: Anchor on the user and their need

Every map starts with the user (top of the map) and their **need** (one level below). Examples:
- Banking user → needs to send money
- Streaming viewer → needs to be entertained
- Developer → needs to ship code reliably

Without an anchored user need, the map is just a wishlist.

## Phase 2: Build the value chain

Below the user need, decompose the components required to satisfy it. Each component is either:
- Visible to the user, or
- Required to deliver a higher component (inferred from technical architecture)

Layers typically follow:
- User need (e.g., send money)
- Capability (e.g., transfer service)
- Sub-capability (e.g., authentication, ledger, settlement, fraud detection)
- Practice (e.g., Know Your Customer (KYC) processes)
- Data (e.g., transaction history)
- Infrastructure (e.g., compute, storage, network)

Connect each child to its parent with a dependency edge. The chain typically has 3-6 layers.

## Phase 3: Plot on the maturity axis

Place each component on the horizontal axis based on its maturity stage:

| Stage | Characteristics | Example (in 2025) |
|-------|-----------------|--------------------|
| **Novel** | New, rare, uncertain, high variation | Quantum-resistant cryptography |
| **Custom-built** | Bespoke per organization, expensive | Custom Large Language Model (LLM) fine-tuning workflows |
| **Productized** | Multiple vendors, comparable offerings | Vector databases |
| **Commoditized / utility** | Standardized, undifferentiated, metered | Compute, storage, bandwidth |

Plot each component as a node at the right horizontal position. Components shift right over time - never left.

## Phase 4: Apply environmental forces

Environmental forces are inevitable structural shifts - like weather. You don't control them; you account for them.

Key forces to check:
- **Everything matures** - assume rightward drift; ask "what will commoditize in 3-5 years?"
- **Commoditization of one component enables novel uses above it** - cloud commoditization unlocked the Software as a Service (SaaS) explosion
- **Past success breeds inertia** - incumbents resist commoditization of their core
- **Practice co-evolves with activity** - DevOps emerged with cloud, not separately
- **Long stability, then rapid transition** - identify which components are near a tipping point

## Phase 5: Apply operating principles

Operating principles are universally good practices, independent of context:
- Focus on user needs
- Know your users
- Use a common language (the map itself)
- Be transparent
- Challenge assumptions
- Use the right methods at each maturity stage (novel → experimental, commoditized → industrial efficiency)
- Manage inertia (it is both emotional and structural)
- Optimize flow, not silos
- Bias toward the new (or be eaten by it)

Score the organization on each. Principle gaps are easier to fix than strategy mistakes.

## Phase 6: Identify strategic plays

Strategic plays are deliberate moves available on the map:
- **Accelerate maturity** - invest to push a component right (commoditize a competitor's differentiation)
- **Slow maturity** - patent, regulate, raise fear-uncertainty-doubt (defensible only short-term)
- **Open source** - commoditize complements; a classic move used by International Business Machines (IBM), Red Hat, and Google
- **Build a market** - create demand for a component (Stripe did this for "online payments")
- **Sensible** trade-off between methods at each stage:
  - Novel → in-house lean / agile
  - Custom-built → in-house or contractor
  - Productized → buy off-the-shelf
  - Commoditized → use a utility provider
- **Pioneer / Settler / Town Planner** - explicit team structure matched to maturity stage

## Phase 7: Strategic recommendations

For each component on the map, recommend an action:

| Component | Current stage | 3-year stage | Action | Rationale |
|-----------|--------------|--------------|--------|-----------|
| [name] | Custom-built | Productized | Stop building; buy | Pioneering effort no longer differentiates |
| [name] | Productized | Commoditized | Switch to utility provider; redeploy capital | Cost savings; redirect to novel bets |
| [name] | Novel | Custom-built | In-house team; accept high failure | Optionality; differentiation if it works |

Cross-check against:
- Competitor maps (where are they investing?)
- Substitute industries (where could lateral entrants come from?)
- Regulatory trajectory

## Output

- One-page Strategic Landscape Map with user need, value chain, and maturity plot
- Environmental-forces commentary
- Operating-principles scorecard
- Strategic-play recommendations per component
- Three-year forward-looking map showing predicted maturity shift
- Top 3 strategic plays with first 90-day moves
- Inertia map: which incumbents (internal or external) will resist

## Operating rules

**Always**
- Start with the user and their need
- Plot on maturity stage, not just dependency
- Apply environmental forces first (the inevitable), then operating principles, then strategic plays
- Re-map every 6-12 months
- Identify inertia explicitly

**Never**
- Build a map without an anchored user need
- Treat the map as a static deliverable
- Confuse the dependency axis with the maturity axis
- Skip the "what will be commoditized in 3 years" question
- Use a single method (e.g., agile) across all maturity stages
