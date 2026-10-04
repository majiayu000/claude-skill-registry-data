---
name: moat-builder
description: Identify and deepen moats — workflow lock-in, data network effects, domain depth, integration depth. Audit current moats + propose investments.
---

# Moat Builder

## When you activate
- Quarterly strategic review
- When user asks: "what's our moat?", "how do we defend X?", "what makes us hard to replicate?"
- After a competitor releases something similar

## What you produce
Saved to `products/<name>/scale/moat-YYYY-QN.md`:

```
## Moat Assessment — <product> — <quarter>

### Moat inventory (current state)
| Moat type | Strength (1-5) | Evidence | Threat |
|---|---|---|---|
| Workflow lock-in | <n> | <e.g. avg user has 7 integrations> | <e.g. competitor offers easy import> |
| Data network effects | <n> | <e.g. 18 months of behavioral data> | <e.g. competitor has 10x our users> |
| Domain depth | <n> | <e.g. handle 340B drug program correctly> | <e.g. competitor hires our former PM> |
| Integration depth | <n> | <e.g. native to 12 tools> | <e.g. competitor is acquired by a tool we're not native to> |
| Brand / community | <n> | <e.g. 8K active forum, 100 user-generated tutorials> | <e.g. competitor sponsors our biggest YouTube channel> |
| Switching cost | <n> | <e.g. retraining takes 4 weeks> | <e.g. competitor pays for migration> |

### The 30-day-copy test
If a well-funded competitor copied our product 1:1 today, in 30 days they would have:
- Feature parity: yes/no
- Performance parity: yes/no
- Distribution parity: yes/no
- What we still have: <list — this IS our moat>
- What we don't have: <list — this is where we're exposed>

### Top 3 moat investments for next quarter
1. <investment> — moat type — expected impact — cost
2. ...
3. ...

### Workflow lock-in audit (per-customer)
For top 10 customers, document:
- Integrations they use (count)
- Workflows built on top (count + estimated switching cost)
- Custom data they've created in the product (volume)
- Score: deep / medium / surface

Most customers should be migrating from "surface" → "deep" over their lifetime. If 6+ months in and still surface = activation/onboarding problem.

### Data flywheel narrative
The story for product marketing:
> "<one-paragraph: how data → improvement → more users → more data, with a specific time horizon a competitor can't shortcut>"
```

## Protocol
1. Read the product's `metrics.md`, recent retention analysis, customer interview synthesis.
2. Walk each moat type. Be ruthlessly honest about strength. Most early products are 1-2 across the board.
3. Run the 30-day-copy test. This is the realest test of moat.
4. For the customer-by-customer workflow audit: pull from Stripe + PostHog data.
5. Propose 3 investments. Each should have a quantified impact estimate.
6. Draft the data flywheel narrative — useful for fundraising, partnerships, and PR.

## Sources
- `knowledge-base/scale-stage/moat-building.md`
- `knowledge-base/ai-native-2026/founders-playbook-distilled.md` (re: workflow lock-in, data network effects, domain depth)

## What you don't do
- Don't call "better UX" a moat. It isn't.
- Don't overestimate brand strength early. Brand becomes a moat over years.
- Don't underestimate workflow lock-in — it's the most underrated moat for B2B SaaS.
