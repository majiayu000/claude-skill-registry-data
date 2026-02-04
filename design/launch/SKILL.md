---
name: launch
description: Go-to-market engine for ID8Labs. Transforms built products into successful launches through positioning, pricing, channel strategy, and tactical execution.
version: 1.0.0
mcps: [Perplexity, Firecrawl]
subagents: []
skills: [landing-page-designer]
---

# ID8LAUNCH - Go-to-Market Engine

## Purpose

Get your built product to market effectively. A great product with bad marketing dies. A good product with great marketing thrives.

**Philosophy:** Small launches, fast learning. One channel done well beats five done poorly.

---

## When to Use

- Product is built and ready to ship
- User needs go-to-market strategy
- User asks "how do I launch this?"
- User needs positioning help
- User wants pricing guidance
- User planning a Product Hunt launch
- Project is in BUILDING or LAUNCHING state

---

## Commands

### `/launch <project-slug>`

Run full launch planning for a built project.

**Process:**
1. POSITIONING - Define how you're different
2. PRICING - Set the right price point
3. MESSAGING - Craft compelling copy
4. CHANNELS - Choose where to launch
5. SEQUENCE - Plan the launch timeline
6. ASSETS - Create launch materials
7. EXECUTE - Go live

### `/launch positioning <product-description>`

Get positioning and messaging guidance.

### `/launch pricing <product-type>`

Get pricing strategy recommendations.

### `/launch ph` (Product Hunt)

Get Product Hunt-specific launch playbook.

### `/launch copy <product>`

Generate launch copy and messaging.

---

## Launch Philosophy

### The Solo Builder Advantage

| Advantage | How to Leverage |
|-----------|-----------------|
| **Speed** | Launch before competition even knows you exist |
| **Authenticity** | Your personal story is compelling |
| **Flexibility** | Pivot messaging instantly based on feedback |
| **Direct access** | You can personally engage with every early user |
| **No bureaucracy** | Make decisions in minutes, not meetings |

### Launch Reality Check

**What works for solo builders:**
- Small, focused launches
- One channel mastered
- Personal outreach
- Community building
- Content marketing

**What doesn't work (at our scale):**
- Massive PR campaigns
- Multi-platform blitzes
- Paid advertising (usually)
- Enterprise sales motions

---

## Process Detail

### Phase 1: POSITIONING

**Answer these questions:**

1. **What category are you in?**
   - Existing category (compete on features/price)
   - New subcategory (own a niche)
   - New category (hardest, biggest upside)

2. **Who is your customer?**
   - Be specific: "freelance designers" not "designers"
   - Know their pain, language, hangouts

3. **What's your key differentiator?**
   - Only choose ONE (you can't be everything)
   - Must be defensible and believable

4. **What's your positioning statement?**

```
For [target customer]
Who [key pain point]
[Product name] is a [category]
That [key benefit]
Unlike [main alternative]
We [key differentiator]
```

### Phase 2: PRICING

Use `frameworks/pricing-strategy.md` for detailed guidance.

**Quick framework:**

| Pricing Model | Best For | Example |
|---------------|----------|---------|
| **Freemium** | Viral growth, network effects | Notion, Figma |
| **Free trial** | High consideration purchases | SaaS tools |
| **Paid only** | Serious buyers, premium positioning | Basecamp |
| **Usage-based** | Variable value delivery | AWS, OpenAI |
| **Lifetime deal** | Quick cash, launch momentum | AppSumo |

**Solo builder defaults:**
- Start with 2-3 tiers max
- Include free tier if product has viral potential
- Price based on value, not cost
- You can always adjust later

### Phase 3: MESSAGING

**Core messages to create:**

1. **One-liner:** What it is in 10 words
2. **Tagline:** The memorable phrase
3. **Problem statement:** The pain you solve
4. **Value proposition:** Why choose you
5. **Social proof:** Evidence it works
6. **Call to action:** What to do next

**Messaging formulas:**

```
# Pain-Agitate-Solution
Pain: [Problem they have]
Agitate: [Make it worse - what happens if unsolved]
Solution: [How you fix it]

# Before-After-Bridge
Before: [Their current state]
After: [Their desired state]
Bridge: [Your product connects them]

# Feature-Advantage-Benefit
Feature: [What it does]
Advantage: [Why that's better]
Benefit: [What they get]
```

### Phase 4: CHANNELS

**Channel selection matrix:**

| Channel | Effort | Time to Results | Best For |
|---------|--------|-----------------|----------|
| **Product Hunt** | Medium | Immediate | B2B SaaS, dev tools |
| **Hacker News** | Low | Immediate | Technical products |
| **Reddit** | Low-Medium | Days-weeks | Niche communities |
| **Twitter/X** | Medium | Weeks-months | Builder audience |
| **SEO/Content** | High | Months | Long-term growth |
| **Email/Newsletter** | Medium | Days-weeks | Existing audience |
| **Cold outreach** | High | Days-weeks | B2B, high ACV |

**Solo builder recommendation:**
1. Pick ONE primary channel
2. Master it before adding others
3. Go where your users already are

### Phase 5: SEQUENCE

Use `frameworks/launch-sequencing.md` for platform-specific playbooks.

**Generic launch timeline:**

| Timing | Activity |
|--------|----------|
| T-2 weeks | Finalize positioning, messaging |
| T-1 week | Create all launch assets |
| T-3 days | Seed community, notify supporters |
| T-1 day | Final prep, queue posts |
| Launch day | Execute, engage, monitor |
| T+1 day | Follow up, gather feedback |
| T+1 week | Analyze, iterate, sustain |

### Phase 6: ASSETS

**Minimum launch assets:**

- [ ] Landing page (with clear CTA)
- [ ] Product screenshots/demo
- [ ] One-liner + tagline
- [ ] Social post copy (2-3 variants)
- [ ] Email announcement (for existing list)

**Nice to have:**

- [ ] Demo video (60-90 seconds)
- [ ] Press kit
- [ ] Detailed product walkthrough
- [ ] Testimonials/social proof

### Phase 7: EXECUTE

**Launch day checklist:**

Morning:
- [ ] Final check of landing page
- [ ] Verify sign-up flow works
- [ ] Post to primary channel
- [ ] Share to personal networks

Throughout day:
- [ ] Respond to every comment/question
- [ ] Monitor for issues
- [ ] Track key metrics
- [ ] Share updates/momentum

End of day:
- [ ] Thank supporters
- [ ] Note learnings
- [ ] Plan follow-up

---

## Framework References

### Go-to-Market Strategy
`frameworks/gtm-strategy.md` - Overall launch strategy

### Positioning
`frameworks/positioning.md` - How to position against competition

### Launch Sequencing
`frameworks/launch-sequencing.md` - Platform-specific playbooks

### Pricing Strategy
`frameworks/pricing-strategy.md` - Pricing models and psychology

### PR & Outreach
`frameworks/pr-outreach.md` - Press and influencer approach

---

## Output Templates

### Launch Plan
`templates/launch-plan.md` - Comprehensive launch checklist

### Landing Page Copy
`templates/landing-page-copy.md` - Conversion-focused copy template

### Press Kit
`templates/press-kit.md` - Media kit for press outreach

---

## Tool Integration

### MCPs

**Perplexity:**
- Research competitor positioning
- Find industry benchmarks
- Discover audience hangouts

**Firecrawl:**
- Scrape competitor landing pages
- Extract pricing information
- Analyze messaging patterns

### Skills

**landing-page-designer:**
- Generate landing page structure
- Create conversion-focused copy
- Design call-to-action sections

---

## Handoff

After completing launch planning:

1. **Save outputs:**
   - Launch plan → `docs/LAUNCH_PLAN.md` in project
   - Copy → Landing page components
   - Press kit → `docs/PRESS_KIT.md`

2. **Log to tracker:**
   ```
   /tracker log {project-slug} "LAUNCH: Launch plan complete. Primary channel: {channel}. Launch date: {date}."
   ```

3. **Update state:**
   ```
   /tracker update {project-slug} LAUNCHING
   ```

4. **Next steps:**
   - Execute launch plan
   - After launch, transition to growth

---

## Anti-Patterns

| Anti-Pattern | Why Bad | Do Instead |
|--------------|---------|------------|
| Launch everywhere | Spread too thin | Focus on ONE channel |
| No positioning | Generic = forgettable | Define clear differentiator |
| Price too low | Undervalues product | Price for value delivered |
| Skip soft launch | Miss early feedback | Test with small group first |
| Perfect before launch | Never ship | Good enough → iterate |
| Ignore launch | Build and pray | Treat launch as a feature |

---

## Quality Checks

Before launching:

- [ ] Positioning is clear and differentiated
- [ ] Pricing matches value and audience
- [ ] Landing page converts (test with friends)
- [ ] Sign-up flow works perfectly
- [ ] Primary channel is researched
- [ ] Launch assets are ready
- [ ] Timeline is realistic
- [ ] You're ready to engage all day
