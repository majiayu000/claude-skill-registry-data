---
name: competitive-intel
description: Weekly competitive landscape monitoring and analysis
tags: [competitive, intelligence, monitoring, strategy]
---

# Competitive Intel

Performs weekly competitive landscape monitoring across websites, social media, content, and client signals. Uses `company-researcher` patterns for deep competitor analysis. Produces a structured intelligence report with notable changes, content gaps, opportunities, and threats. Designed to run weekly as part of a strategic review cadence.

## Prerequisites

- `agency.config.json` in the project root
- WebSearch tool available
- List of 3-5 competitor agencies to monitor (stored in config or provided by user)
- Optional: previous competitive intel report for change detection

## Capabilities Used

1. `company-researcher` -- for competitor deep dives and structured data extraction

## Phase 0: Read Config and Competitor List

1. Read `agency.config.json` from the project root.
2. Check for `competitors[]` array in config. If present, use it:
   ```json
   {
     "competitors": [
       {
         "name": "Agency Alpha",
         "website": "https://agencyalpha.com",
         "linkedin": "https://linkedin.com/company/agencyalpha",
         "instagram": "@agencyalpha",
         "twitter": "@agencyalpha",
         "notes": "Premium positioning, strong in fashion D2C"
       }
     ]
   }
   ```
3. If no competitors in config, ask the user:
   ```
   Name 3-5 competitor agencies to monitor. For each, provide:
   - Agency name
   - Website URL
   - LinkedIn company page (if known)
   - Any other social handles
   ```
4. Extract `services[].name` to know what service areas to compare.
5. Extract `icp.segments[]` to understand which markets and industries overlap.
6. Check for previous report: look for the most recent `competitive-intel-YYYY-MM-DD.md` in the project directory.

## Phase 1: Website Monitoring

For each competitor, visit their website via WebSearch:

**Queries:**
- `site:{{competitor_website}}`
- `"{{competitor_name}}" new`
- `{{competitor_website}}/blog` or `{{competitor_website}}/case-studies`

**Extract and compare:**

Service offerings:
- List all services visible on their site
- Flag any NEW services not seen in previous report
- Flag any REMOVED services
- Note pricing if publicly visible (rare but valuable)

Case studies:
- List visible case studies / portfolio items
- Flag new case studies since last report
- Note industries and results highlighted
- Extract client names mentioned

Team changes:
- Check team/about page
- Flag new team members (especially leadership or sales hires)
- Flag departures if previously noted members are gone

Website changes:
- New pages or sections
- Design/branding updates
- New tools, calculators, or lead magnets
- Messaging changes (headline, value prop, CTA wording)

Compile per competitor:
```
[Competitor Name] -- WEBSITE CHANGES
---
New services: [list or "none"]
New case studies: [list or "none"]
Team changes: [list or "none"]
Website updates: [list or "none"]
Pricing visible: [yes/no, details if yes]
```

## Phase 2: Social Monitoring

For each competitor, check social presence:

**LinkedIn:**
- WebSearch: `"{{competitor_name}}" site:linkedin.com`
- WebSearch: `"{{competitor_name}}" linkedin post {{current_month}} {{current_year}}`
- Check for: new posts, client announcements, hiring posts, thought leadership content
- Note engagement levels (likes, comments) if visible in search snippets

**Twitter/X:**
- WebSearch: `"{{competitor_name}}" site:twitter.com OR site:x.com`
- WebSearch: `from:{{competitor_twitter}} {{current_month}}`
- Check for: announcements, client tags, industry commentary, product launches

**Instagram:**
- WebSearch: `"{{competitor_name}}" site:instagram.com`
- Check for: portfolio posts, client features, behind-the-scenes, engagement rates

**YouTube (if applicable):**
- WebSearch: `"{{competitor_name}}" site:youtube.com {{current_year}}`
- Check for: new video content, webinars, tutorials

Compile per competitor:
```
[Competitor Name] -- SOCIAL ACTIVITY
---
LinkedIn:
  Posts this week: [count estimate]
  Notable posts: [topic, engagement]
  Hiring posts: [roles, if any]
  Client mentions: [companies tagged]

Twitter:
  Activity level: [active/moderate/quiet]
  Notable tweets: [topic]

Instagram:
  Posts this week: [count estimate]
  Content type: [portfolio/behind-scenes/educational]
  Engagement: [high/medium/low relative to followers]
```

## Phase 3: Content Analysis

For each competitor, analyze their content strategy:

**Blog/content audit:**
- WebSearch: `site:{{competitor_website}}/blog {{current_year}}`
- List articles published in the last 30 days
- Categorize by topic: [SEO, CRO, design, development, marketing, case study, industry news]

**Keyword targeting:**
- What topics are they publishing about repeatedly?
- What keywords do their article titles target?
- Are they going after the same keywords as us?
- New keyword territories they're entering

**Content formats:**
- Blog posts (long-form, short-form)
- Video content (tutorials, webinars, client testimonials)
- Carousels/infographics (LinkedIn, Instagram)
- Podcasts or audio content
- Downloadable resources (guides, templates, tools)
- Email newsletters (check if sign-up page reveals frequency/topics)

**Content quality assessment:**
- Depth: surface-level vs comprehensive
- Originality: unique insights vs rehashed content
- Data usage: proprietary data, case study numbers, industry stats
- Production quality: design, visuals, formatting

Compile:
```
CONTENT LANDSCAPE
===
[Competitor 1]:
  Publishing frequency: [posts/month]
  Top topics: [topic1, topic2, topic3]
  Formats: [blog, video, carousel]
  Quality: [assessment]
  New topics this month: [topics not covered before]

[Competitor 2]:
  ...
```

## Phase 4: Client Signals

Monitor competitor client movements:

**New client signals:**
- WebSearch: `"{{competitor_name}}" "client" OR "partner" OR "worked with" OR "case study" {{current_year}}`
- WebSearch: `"built by {{competitor_name}}" OR "designed by {{competitor_name}}"`
- Check for new logos on their website
- Check for client testimonials or reviews added

**Lost client signals:**
- Clients previously featured that are no longer on the site
- Companies that previously tagged the competitor but have stopped
- WebSearch: `"{{former_client}}" "new agency" OR "switched to" OR "partnered with"`

**Client overlap check:**
- Are any competitors targeting the same prospects as us?
- Are any competitors pitching to our existing clients?
- WebSearch: `"{{our_client_name}}" "{{competitor_name}}"`

Compile:
```
CLIENT SIGNALS
===
[Competitor 1]:
  New clients spotted: [list]
  Clients no longer featured: [list]
  Industries gaining: [industries of new clients]

[Competitor 2]:
  ...

OVERLAP ALERTS:
- [Competitor] appears to be targeting [industry/company] -- also in our pipeline
```

## Phase 5: Positioning Analysis

Synthesize all data into a competitive positioning map:

**Service overlap matrix:**
```
SERVICE           | Us | Comp1 | Comp2 | Comp3
---               | -- | ----- | ----- | -----
Store development |  Y |   Y   |   Y   |   N
CRO               |  Y |   N   |   Y   |   Y
Cataloging        |  Y |   N   |   N   |   N
Perf. marketing   |  Y |   Y   |   Y   |   Y
[service]         |  ? |   ?   |   ?   |   ?
```

**Price positioning:**
- Premium (higher than market), Mid-market, Budget (competing on price)
- Based on visible pricing, case study size, and client type

**Unique selling points comparison:**
```
USP COMPARISON:
---
Us: [our primary USP]
[Competitor 1]: [their USP -- what they emphasize most]
[Competitor 2]: [their USP]
[Competitor 3]: [their USP]

GAPS WE OWN (services/capabilities no competitor offers):
- [gap 1]
- [gap 2]

GAPS COMPETITORS OWN (things they offer that we don't):
- [Competitor]: [capability]
```

**Market positioning:**
- Which segments is each competitor strongest in?
- Where do we have the most differentiation?
- Where is the market most crowded?

## Phase 6: Weekly Intelligence Report

Compile everything into the final report:

```
COMPETITIVE INTELLIGENCE -- Week of [Date]
===

EXECUTIVE SUMMARY:
[3-4 sentences capturing the most important competitive developments this week]

---

NOTABLE CHANGES:
1. [Competitor] [specific change] -- Impact: [high/medium/low]
   Context: [why this matters to us]
2. [Competitor] [specific change] -- Impact: [high/medium/low]
   Context: [why this matters]
3. [Competitor] [specific change] -- Impact: [high/medium/low]
   Context: [why this matters]

---

CONTENT GAPS (topics competitors cover that we don't):
- [topic 1] -- covered by [competitor(s)], [estimated search interest]
- [topic 2] -- covered by [competitor(s)], [estimated search interest]
- [topic 3] -- covered by [competitor(s)], [estimated search interest]

CONTENT OPPORTUNITIES (topics nobody covers well):
- [topic 1] -- [why it's an opportunity]
- [topic 2] -- [why it's an opportunity]

---

CLIENT MOVEMENT:
- [Competitor] added [client] (industry: [x], size: [y])
- [Competitor] may have lost [client] (no longer featured)

---

OPPORTUNITIES:
- [specific opportunity based on competitor weakness or gap]
- [underserved segment or topic area]
- [timing-based opportunity -- competitor slow to react to trend]

THREATS:
- [competitive move that could affect our pipeline]
- [competitor entering our strongest segment]
- [pricing pressure from competitor]

---

POSITIONING SNAPSHOT:

             Premium
                |
    [Comp1] ---|--- [Us?]
                |
             ---|---
                |
    [Comp3] ---|--- [Comp2]
                |
              Budget
         Specialist --- Generalist

---

WEEK-OVER-WEEK CHANGES:
[What's different from last week's report -- new entries, resolved items, trend shifts]
If no previous report: "First report -- baseline established."
```

## Phase 7: Recommendations

Based on the intelligence gathered, provide specific recommendations:

```
RECOMMENDED ACTIONS
===

IMMEDIATE (this week):
1. [Action] -- because [competitor did X and we need to respond]
2. [Action] -- because [opportunity window is closing]

SHORT-TERM (next 2-4 weeks):
1. [Action] -- because [competitive gap to exploit]
2. [Action] -- because [content opportunity identified]

STRATEGIC (next quarter):
1. [Action] -- because [market positioning shift needed]
2. [Action] -- because [service gap to fill or differentiation to build]

MONITOR (watch but don't act yet):
- [Signal to keep tracking]
- [Competitor move that hasn't materialized yet]
```

Save the report as `competitive-intel-{{date}}.md` in the project root for historical comparison.

## Example Usage

Trigger phrases:
- "Run competitive intel"
- "Weekly competitor check"
- "What are our competitors doing?"
- "Monitor competitor agencies"
- "Competitive landscape update"

```
User: Run competitive intel
Assistant: [reads competitor list from config, searches websites/social/content/clients for each, compiles weekly report with changes, gaps, opportunities, threats]
```

```
User: What's Agency Alpha been up to lately?
Assistant: [deep dive on single competitor, full website + social + content + client analysis, positioning comparison]
```

```
User: Are any competitors going after Shopify CRO in India?
Assistant: [focused search on competitors' CRO offerings, Indian market presence, content targeting, client signals in that segment]
```
