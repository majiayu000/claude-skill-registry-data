---
name: riflebird-cold-email
description: Transform SEO micro-audits into high-converting cold emails with zero jargon. Generates 2-3 email variations (customer perspective, competitor comparison, benefit-first) for e-commerce, local service, or B2B prospects. Translates technical SEO findings into business language, includes specific numbers and competitor comparisons, and positions Riflebird Agency as lean team of experts. Use when you have a completed SEO audit and need to create personalized cold outreach emails.
---

# Riflebird Cold Email Generator

Transform SEO micro-audits into high-converting cold emails with zero jargon.

## Purpose

Generate personalized cold outreach emails for Riflebird Agency that:
- Lead with business impact, not technical SEO terms
- Position agency as "lean team of experts"
- Include specific numbers and competitor comparisons
- Keep emails under 200 words
- Offer 2-3 variations to choose from

## How to Use This SKILL

```bash
# From project root
/skill riflebird-cold-email
```

## Workflow

When this SKILL is invoked, follow these steps:

### Step 1: Get Audit File Path

Ask the user for the path to the micro-audit markdown file (e.g., `leads/Riflebird/one-six-eight-london-micro-audit.md`).

Read the audit file and extract:
- Company name and domain
- Business type and industry
- Location (city, suburb, state)
- Issues found (technical problems)
- Positive findings (USPs, existing strengths)
- Competitive landscape info
- Recommended email approach section

### Step 2: Interactive Refinement

Ask the user these questions:

1. **Recipient name and role** (if known) - for personalization
2. **Include paid ads vs organic case study?**
   - Yes: Reference the Ahrefs screenshot (leads/Riflebird/result.jpg) showing paid traffic spikes vs sustainable organic growth
   - No: Focus purely on audit findings
3. **Primary goal for this email**:
   - Book discovery call
   - Offer free fix/value
   - Start conversation
4. **Tone preference**:
   - Friendly (warm, personal)
   - Professional (polished, corporate)
   - Bold (direct, provocative)

### Step 3: Extract and Translate Issues

From the audit, identify the **top 3 most compelling issues** based on:
- Business impact (revenue/traffic loss)
- Easy fix potential (low effort, high return)
- Competitor comparison opportunity
- Quantifiable metrics

For each issue, translate from SEO jargon to business language using the reference guide at `reference/jargon-translation.md`.

**Translation Examples**:
- "Title tag only 20 chars" → "Your Google listing is using 1/3 of the billboard space"
- "16 images missing alt text" → "70% of your products are invisible in Google image searches"
- "Meta description 30 chars" → "Your search result doesn't mention your 5-year warranty or price match"

### Step 4: Generate 3 Email Variations

Create three distinct emails using different approaches:

**Variation A: Customer Perspective**
- Opening: "I was searching [their keyword]..." hook
- Shows empathy and real-world search behavior
- Best for: E-commerce, local businesses

**Variation B: Competitor Comparison**
- Opening: "[Competitor] ranks #1 for [keyword] and here's why..."
- Creates competitive urgency
- Best for: Competitive markets, ambitious prospects

**Variation C: Benefit-First**
- Opening: "Quick question - did you know [shocking stat]?"
- Leads with curiosity and opportunity
- Best for: Prospects who may not know they have a problem

### Step 5: Email Structure (All Variations)

Each email must follow this structure:

```
Subject: [6-10 words, specific and curiosity-driving]

Hi [Name],

[OPENING HOOK - 1-2 sentences]
- Choose from templates/opening-hooks.md
- Personalize with their specific business/location

[CONTEXT - 1 sentence]
- Why you're reaching out
- Keep it human and relatable

[MAIN ISSUE - 2-3 sentences]
- Present the #1 most impactful issue
- Use business language (zero jargon)
- Include specific numbers

[SUPPORTING ISSUES - 2-4 bullets]
- Issue #2 and #3 as concise bullets
- Each bullet = impact statement
- Use → or • for formatting

[IMPACT/OPPORTUNITY - 1-2 sentences]
- What they're missing out on
- Reference competitors or market position
- Create urgency without being pushy

[CASE STUDY - OPTIONAL - 1-2 sentences]
- If user selected "yes" to paid ads case study
- Reference the screenshot showing paid traffic (green spikes) vs sustainable organic growth (orange line)
- "We helped a client reduce their Google Ads dependency - the green spikes show their paid traffic attempts to compensate for poor organic rankings. After fixing their SEO, the orange line shows sustainable organic growth without the ad spend."
- Offer to share the Ahrefs screenshot

[SOLUTION PREVIEW - 1 sentence]
- Hint at fix without giving it all away
- Mention time required (e.g., "2-3 hours to fix")

[CTA - 1 sentence]
- Low-friction next step
- Choose from templates/closing-ctas.md

[SIGNATURE]
Ali Fathieh
Digital Marketing Specialist
Riflebird Agency
Melbourne
[Phone - leave placeholder]

P.S. [Objection handler or bonus value]
- Choose from templates/ps-lines.md
- Personalize with specific observation about their business
```

### Step 6: Quality Checklist

Before outputting emails, verify each one includes:

**Required Elements**:
- [ ] Mention their city/suburb/location
- [ ] Name at least 1 specific competitor
- [ ] Include 2-3 hard numbers from audit
- [ ] Reference a specific search term/keyword
- [ ] State time/effort required
- [ ] Personal touch about their business
- [ ] "Lean team" positioning in signature or body

**Constraints**:
- [ ] Body text under 200 words
- [ ] Subject line 6-10 words
- [ ] Maximum 3 issues mentioned
- [ ] Paragraphs 2-3 sentences max
- [ ] Zero SEO jargon (use business language)
- [ ] Scannable (bullets, short lines)

**Tone Check**:
- [ ] Conversational, not robotic
- [ ] Helpful, not salesy
- [ ] Specific, not generic
- [ ] Confident, not arrogant

### Step 7: Output Format

Present the three email variations clearly:

```markdown
# Cold Email Variations for [Company Name]

**Audit Source**: [file path]
**Industry**: [e-commerce/local service/B2B]
**Top Issues**: [3 issues in business language]

---

## Variation A: Customer Perspective

**Subject**: [subject line]

[full email]

**Why This Works**: [1-2 sentence explanation]

---

## Variation B: Competitor Comparison

**Subject**: [subject line]

[full email]

**Why This Works**: [1-2 sentence explanation]

---

## Variation C: Benefit-First

**Subject**: [subject line]

[full email]

**Why This Works**: [1-2 sentence explanation]

---

## Recommendations

**Best Choice**: [Which variation and why]
**A/B Test**: [Suggest testing two variations]
**Follow-Up**: [When to send if no response]
```

## Key Principles

### Zero Jargon Rule
Never use these terms without translation:
- Title tag, meta description, H1, H2
- Alt text, image optimization
- Schema markup, structured data
- SERP, organic ranking, backlinks
- Domain authority, page authority
- Canonical, redirect, crawl

Always translate to business impact:
- "Your Google listing"
- "Your search result"
- "Image search visibility"
- "Where you show up on Google"

### The "Lean Team of Experts" Positioning

Include this positioning in signature or body:
- "I'm Ali from Riflebird Agency - a lean Melbourne team specializing in [industry] SEO"
- "We're a lean team of experts focusing on increasing traffic and bringing more business"
- Emphasizes efficiency, specialization, and local presence

### Paid Ads vs Organic SEO Case Study (Optional)

When user selects to include the case study, reference the Ahrefs performance screenshot (`leads/Riflebird/result.jpg`):

**What the screenshot shows**:
- **Green line**: Paid traffic - temporary spikes when ads are running, drops when ads stop
- **Orange line**: Organic traffic - sustainable growth after SEO fixes
- **Key insight**: Client was "renting" traffic through ads instead of "owning" it through organic rankings

**How to reference it in emails**:

**Version 1 - Direct comparison**:
"I can share a case study screenshot that tells the story perfectly: the green spikes show a client's paid ad traffic trying to compensate for poor organic rankings. After we fixed their SEO, the orange line shows sustainable organic growth - no more ad dependency."

**Version 2 - Cost focus**:
"We helped a client cut their Google Ads spend by 60% while growing overall traffic. I have an Ahrefs chart showing the before/after - the difference between renting traffic (green spikes) and owning it (orange growth line) is dramatic. Happy to share it."

**Version 3 - Sustainability angle**:
"One of our clients was spending $2K+/month on ads just to maintain traffic (you can see the green spikes in our case study chart). We fixed their SEO and now they get that traffic organically - permanent results vs temporary fixes."

**When to use it**:
- Prospect appears to be running paid ads heavily
- E-commerce businesses with tight margins
- Local businesses with limited marketing budgets
- Any prospect concerned about ongoing costs
- Follow-up email if no response to first email

### Personalization Depth

Go beyond name/company. Include:
- Specific product they sell ("Your ELSA wall clocks")
- Local suburb ("Cheltenham shoppers")
- Unique selling point ("5-year warranty")
- Recent observation ("Just opened your Melbourne showroom")
- Competitor in their niche ("Temple & Webster")

### The P.S. Strategy

P.S. lines serve three purposes:
1. **Objection Handling**: "Not trying to sell you a huge retainer - these are simple fixes you could do in-house"
2. **Value Add**: "I'll send you the exact title tag to use - no strings attached"
3. **Personal Touch**: "Your ELSA clocks are gorgeous - criminal they don't show up in Google Images"

Choose based on prospect type and tone.

## Common Patterns

### E-Commerce Businesses
- Focus on product visibility in image search
- Reference shopping keywords ("designer wall clocks")
- Emphasize competitor comparison
- Mention seasonal opportunities
- Highlight missing product schema
- **Paid ads angle**: Cost per acquisition vs organic traffic value

### Local Service Businesses
- Lead with local search terms ("plumber Cheltenham")
- Reference Google Business Profile issues
- Mention Google Maps visibility
- Compare to nearby competitors
- Emphasize "near me" searches
- **Paid ads angle**: Local Services Ads cost vs organic local pack rankings

### B2B/SaaS Companies
- Focus on thought leadership keywords
- Reference comparison pages ("X vs Y")
- Mention buyer intent keywords
- Compare to industry leaders
- Emphasize trust signals and credentials
- **Paid ads angle**: High CPC for industry keywords vs organic authority

### Professional Services
- Lead with credential/expertise keywords
- Reference "best [service] in [city]" searches
- Mention trust elements (reviews, awards)
- Compare to established competitors
- Emphasize E-A-T factors (without jargon)
- **Paid ads angle**: Building long-term reputation vs paying for each lead

## Examples

See the `examples/` directory for complete cold email examples:
- `ecommerce-example.md` - Based on One Six Eight London audit
- `local-service-example.md` - For service-based businesses
- `b2b-example.md` - For B2B/SaaS companies

## Templates Library

Reference these template files during generation:
- `templates/opening-hooks.md` - 10 proven opening hook patterns
- `templates/body-frameworks.md` - Issue presentation structures
- `templates/closing-ctas.md` - Call-to-action variations
- `templates/ps-lines.md` - P.S. objection handlers and value-adds

## Jargon Translation Reference

Use `reference/jargon-translation.md` to convert technical SEO findings into business language that prospects understand and care about.

## Success Metrics

A successful cold email should:
- Get opened (compelling subject line)
- Get read (scannable, short, personalized)
- Get replied to (low-friction CTA, value-first)
- Position expertise (specific findings, numbers, tools)
- Build trust (transparent, helpful, not pushy)

Emails that follow this SKILL framework should achieve:
- 40-60% open rates (personalized subject lines)
- 15-25% reply rates (value-first approach)
- 5-10% conversion to calls (strong audit foundation)
