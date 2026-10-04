---
name: growth-loops
description: Design growth loops (Reforge/Balfour framework). Identify acquisition, monetization, and engagement loops with quantified inputs and outputs.
model_tier: opus
---

# Growth Loops

## When you activate
Product is past PMF. User asks: "how do we grow X?", "design growth loops for Y", "channel strategy after PMF"

## What you produce
Saved to `products/<name>/launch/growth-loops.md`:

```
## Growth Loops — <product>

### Loop 1: <name> — Acquisition / Engagement / Monetization
**Type:** Viral | Content | Paid | Sales | UGC

**Steps:**
1. <action> → 2. <action> → 3. <action> → 4. <action that reinvests in step 1>

**Inputs needed:**
- <e.g. 100 new users/month from cold outreach>

**Outputs produced:**
- <e.g. 30 referrals/month from happy users>

**Loop multiplier:** <e.g. each user generates 0.3 new users = 0.3x compounding>

**Bottleneck:** <which step has the worst conversion or longest time>

**Investment to test:** <hours/dollars to validate the loop works>

### Loop 2: ...

### Loop interaction
How loops feed each other. E.g. Loop 1 (content SEO) produces signups → Loop 2 (referral) compounds those → Loop 3 (paid retargeting on warm visitors) catches stragglers.

### What we deliberately don't do
1. Paid ads before organic loops are proven
2. <other deferrals>

### Measurement
For each loop:
- Loop completion rate (% users who finish all steps)
- Loop cycle time (how long start → reinvest)
- Loop value (revenue or users generated per cycle)
```

## Protocol
1. Read the product's `metrics.md` and `prd.md`.
2. Identify which loop types fit the product. Not every loop type works for every product:
   - **Viral**: requires natural network involvement (collaboration tools, social products)
   - **Content (SEO)**: requires evergreen high-intent search demand
   - **Paid**: only when CAC < LTV is provable AND organic loops are saturated
   - **Sales**: B2B with deal size justifying high-touch
   - **UGC**: requires users producing artifacts worth indexing
3. Design 2–3 loops, max. More = unfocused.
4. Quantify inputs and outputs. Loops without numbers are aspirations.
5. Identify bottleneck per loop — that's the experiment queue.

## Sources
- `factory/playbooks/scale-stage/growth-loops-reforge.md`
- `factory/playbooks/scale-stage/100-to-1000-customers.md`

## What you don't do
- Don't design a viral loop for a product that isn't inherently social.
- Don't recommend paid before organic loops are proven — you'll burn cash.
- Don't paste "AARRR funnel" as a loop. Funnels are linear; loops compound. They're different mental models.
