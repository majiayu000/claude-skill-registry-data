---
name: marketing-ideas
model: reasoning
---

# Marketing Ideas

> **WHAT**: Library of 139 proven SaaS marketing tactics with implementation guidance  
> **WHEN**: User needs marketing ideas, growth strategies, or asks "how to market," "marketing tactics," "ways to promote," "ideas to grow"  
> **KEYWORDS**: marketing ideas, growth ideas, marketing strategies, marketing tactics, promotion, growth hacks, SaaS marketing

## Searchable Database

This skill includes **139 marketing ideas** organized by category in `references/ideas-by-category.md`.

**Quick category lookup:**

| Category | Ideas # | Examples |
|----------|---------|----------|
| Content & SEO | 1-10 | Programmatic SEO, Glossary marketing, Content repurposing |
| Competitor | 11-13 | Comparison pages, Marketing jiu-jitsu |
| Free Tools | 14-22 | Calculators, Chrome extensions, Importers |
| Paid Ads | 23-34 | LinkedIn, Google, Retargeting, Podcast ads |
| Social & Community | 35-44 | LinkedIn audience, Reddit, Short-form video |
| Email | 45-53 | Founder emails, Onboarding sequences, Win-back |
| Partnerships | 54-64 | Affiliate programs, Newsletter swaps |
| Events | 65-72 | Webinars, Conference speaking, Virtual summits |
| PR & Media | 73-76 | Press coverage, Documentaries |
| Launches | 77-86 | Product Hunt, Lifetime deals, Giveaways |
| Product-Led | 87-96 | Viral loops, Powered-by marketing, Free migrations |
| Content Formats | 97-109 | Podcasts, Courses, Annual reports |
| Unconventional | 110-122 | Awards, Challenges, Guerrilla marketing |
| Platforms | 123-130 | App marketplaces, Review sites, YouTube |
| International | 131-132 | Expansion, Price localization |
| Developer | 133-136 | DevRel, Certifications |
| Audience-Specific | 137-139 | Referrals, Podcast tours |


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install marketing-ideas
```


---

## Workflow

### 1. Gather Context

Check for `.claude/product-marketing-context.md` first. If it exists, use that context.

If not available, ask:
- What's your product and who's your target audience?
- What stage are you at? (pre-launch, early, growth, scale)
- What's your marketing budget and team size?
- What have you tried that worked or didn't?

### 2. Filter by Constraints

**By Stage:**
- Pre-launch → #77-86 (launches), #79 (waitlist referrals), #78 (Product Hunt)
- Early stage → #1-10 (content/SEO), #35 (community), #47 (founder-led)
- Growth → #23-34 (paid), #54-64 (partnerships), #65-72 (events)
- Scale → #131-132 (international), #73 (media acquisitions)

**By Budget:**
- Free → Content, SEO, community, social, comment marketing
- Low → Targeted ads, sponsorships, free tools
- Medium → Events, partnerships, PR
- High → Acquisitions, conferences, brand campaigns

**By Timeline:**
- Quick wins → Ads, email, social posts
- Medium-term → Content, SEO, community
- Long-term → Brand, thought leadership, platform effects

### 3. Recommend 3-5 Ideas

For each recommendation, provide:

```
### [Idea Name] (#number)

**What**: One-line description
**Why it fits**: Connection to their specific situation
**First steps**:
1. [Immediate action]
2. [Next step]
3. [Following step]

**Expected outcome**: What success looks like
**Resources**: Time, budget, skills required
```

### 4. Deep Dive on Selected Ideas

When user chooses an idea, reference `ideas-by-category.md` for full details and provide:
- Step-by-step implementation plan
- Tools and resources needed
- Common pitfalls to avoid
- Metrics to track

---

## Top Ideas by Use Case

### Need Leads Fast
- #31 Google Ads - High-intent search
- #28 LinkedIn Ads - B2B targeting
- #15 Engineering as Marketing - Free tool lead gen

### Building Authority
- #70 Conference Speaking
- #104 Book Marketing
- #107 Podcasts

### Low Budget Growth
- #1 Easy Keyword Ranking
- #38 Reddit Marketing
- #44 Comment Marketing

### Product-Led Growth
- #93 Viral Loops
- #87 Powered By Marketing
- #91 In-App Upsells

### Enterprise Sales
- #133 Investor Marketing
- #57 Expert Networks
- #72 Conference Sponsorship

---

## NEVER

- Recommend paid tactics to bootstrapped founders without alternatives
- Suggest tactics requiring skills the team doesn't have without acknowledging the gap
- Recommend 10+ ideas at once - overwhelm kills action
- Skip asking about what they've already tried
- Ignore budget constraints

---

## Related Skills

- `copywriting` - Write compelling marketing copy
- `page-cro` - Optimize landing pages for conversion
- `marketing-psychology` - Apply mental models to marketing
