---
description: Full product launch pipeline - from idea to go-to-market plan
argument-hint: "[product or feature to launch]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Agent
  - Glob
  - Grep
  - WebSearch
  - WebFetch
  - Bash(date:*)
---

Full launch pipeline. Takes a product or feature idea through competitive research, positioning, pricing analysis, and GTM planning.

## Steps

### Step 1: Capture the launch brief

If the user described what they're launching, use that. Otherwise ask for:
- What is the product/feature?
- Who is the target customer?
- What's the timeline?

Write a one-paragraph launch brief.

### Step 2: Competitive scan (parallel agents)

Spawn agents to research in parallel:

**Agent 1 — Competitor landscape:**
- Search for direct competitors (products solving the same problem)
- Extract pricing, features, positioning, strengths, weaknesses
- Identify gaps in the market

**Agent 2 — Market signals:**
- Search for recent trends in this space
- Look for demand signals (Reddit threads, HN discussions, Twitter conversations)
- Note any regulatory or platform changes that affect timing

### Step 3: Positioning

Based on competitive findings, define:
- **Category:** What market category does this belong to?
- **Differentiation:** What do you do that competitors don't?
- **Value prop:** One sentence that makes a customer say "I need this"
- **Positioning statement:** For [target], [product] is the [category] that [key benefit] unlike [alternative] because [reason]

### Step 4: Pricing analysis

Using competitor pricing data:
- Map competitor price points (free tier, entry, pro, enterprise)
- Identify the price range your market expects
- Recommend a pricing strategy with rationale
- Include pricing model (one-time, subscription, usage-based, freemium)

### Step 5: Landing page brief

Generate a structured landing page outline:
1. **Hero:** Headline, subheading, primary CTA
2. **Pain points:** 3-4 problems your target customer has
3. **Solution:** How your product solves them
4. **Features:** Top 5-6 features with benefits (not just descriptions)
5. **Social proof:** What type of proof would work (testimonials, stats, logos)
6. **Pricing:** Based on Step 4 analysis
7. **FAQ:** 5-6 questions your target customer would ask
8. **Final CTA:** Closing push

### Step 6: Go-to-market checklist

Generate a phased launch checklist:

**Pre-launch (2-4 weeks before):**
- [ ] Landing page live
- [ ] Email capture / waitlist set up
- [ ] Launch announcement drafted
- [ ] Distribution channels identified (communities, newsletters, social)
- [ ] Early access / beta users lined up

**Launch day:**
- [ ] Announce on primary channels
- [ ] Post on Product Hunt / HN / relevant communities
- [ ] Email waitlist
- [ ] Monitor for issues
- [ ] Respond to early feedback

**Post-launch (1-2 weeks after):**
- [ ] Collect and address feedback
- [ ] Publish case studies / results
- [ ] Optimise based on conversion data
- [ ] Follow up with early users

### Step 7: Write the launch plan

Save everything to `launch-plan-[product-name].md`:

```markdown
# Launch Plan — [Product Name]

## Brief
[one paragraph]

## Competitive Landscape
[table of competitors with pricing/features/positioning]

## Positioning
[positioning statement and differentiation]

## Pricing Strategy
[recommended pricing with rationale]

## Landing Page Brief
[structured outline from Step 5]

## Go-to-Market Checklist
[phased checklist from Step 6]

## Timeline
[key dates and milestones]

## Risks
[top 3 risks and mitigations]

---
Generated: [date]
```

Output a summary of the plan and ask the user what to execute first.
