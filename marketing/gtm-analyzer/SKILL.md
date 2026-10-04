---
name: gtm-analyzer
description: >
  Evaluates current go-to-market positioning versus the market. Analyzes
  website, content, pricing, ICP alignment, and competitive landscape to
  identify gaps, opportunities, and produce a GTM health report.
tags: [gtm, strategy, positioning, market-analysis, planning]
---

# GTM Analyzer

Performs a comprehensive evaluation of your current go-to-market positioning against the competitive landscape and market trends. Audits your website, content strategy, pricing perception, ICP alignment, channel effectiveness, and competitive differentiation. Produces a GTM Health Report with scored dimensions, identified gaps, and prioritized opportunities.

## Prerequisites

- `agency.config.json` populated (services, ICP, pricing, brand voice, case studies)
- WebSearch tool available
- Agency website accessible
- Optional: traffic/analytics data
- Optional: previous GTM analyzer report for trend comparison

## Capabilities Used

1. `company-researcher` -- competitive landscape analysis
2. `cro-auditor` -- website conversion assessment
3. `content-seo-optimizer` -- content strategy evaluation
4. `icp-builder` -- ICP validation and refinement
5. `brand-voice` -- messaging consistency check
6. `tam-calculator` -- market sizing for opportunity assessment

## Phase 0: Intake

Read `agency.config.json`:
- `agency.name`, `agency.domain` -- identity
- `services[]` -- current service offerings
- `icp.segments[]` -- target customer profiles
- `pricing` -- pricing structure and positioning
- `case_studies[]` -- available proof points
- `brand_voice` -- messaging guidelines
- `competitors[]` -- known competitors (from `competitive-intel` if available)
- `channels[]` -- active marketing/sales channels

Accept parameters:
- `scope` -- `full` | `quick` | `specific_dimension`. Default: `full`
- `dimension` -- (required if scope = `specific_dimension`) one of: `website`, `content`, `pricing`, `icp`, `channels`, `competitive`, `messaging`
- `include_recommendations` -- boolean. Default: `true`
- `include_competitive` -- boolean, run competitive analysis. Default: `true`
- `previous_report` -- path to previous GTM report for comparison

## Phase 1: Website and Digital Presence Audit

Evaluate your own website as a GTM asset:

### First Impression (5-second test)
- WebSearch: `site:{{agency.domain}}`
- What does the homepage communicate in 5 seconds?
- Is the value proposition clear?
- Is the ICP obvious (who is this for)?
- Is the primary CTA visible and compelling?

### Messaging Audit
```
MESSAGING ASSESSMENT
---
Homepage headline: [what it says]
  Clarity: [1-5] -- Does it explain what you do?
  Specificity: [1-5] -- Is it generic or differentiated?
  ICP targeting: [1-5] -- Does it speak to the ideal client?

Value proposition: [extracted from site]
  Unique: [yes/no] -- Could a competitor say the same thing?
  Benefit-driven: [yes/no] -- Focused on client outcomes?
  Provable: [yes/no] -- Backed by data or case studies?

Service pages:
  Count: [N]
  Quality: [assessment]
  Missing services: [services in config not on website]
  Excess services: [services on website not in config -- scope creep?]
```

### Trust Elements
- Case studies visible: [count and quality]
- Client logos: [present/absent, count]
- Testimonials: [present/absent, count]
- Social proof metrics: [present/absent -- "100+ clients served"]
- Certifications/partnerships: [Shopify Partner badge, etc.]
- Team/about page: [present/absent, quality]
- Blog/content: [present/absent, freshness]

### Conversion Architecture
- CTA hierarchy: [primary CTA clear?]
- Lead capture forms: [present, number of fields]
- Calendar booking: [available?]
- Chat/contact options: [available?]
- Exit intent: [present?]
- Mobile experience: [assessment]

### Website Score
```
Website Dimension Score: [1-10]
  Messaging clarity: [1-5]
  Trust elements: [1-5]
  Conversion architecture: [1-5]
  Visual quality: [1-5]
  Mobile experience: [1-5]
```

## Phase 2: Content Strategy Evaluation

### Content Inventory
- WebSearch: `site:{{agency.domain}}/blog`
- Total published content pieces: [count]
- Content freshness: [last publish date]
- Publishing frequency: [posts per month]
- Content types: [blog, case study, video, guide, tool]

### Content-ICP Alignment
For each ICP segment, check:
- Content specifically targeting this segment: [count]
- Keywords covered relevant to this segment: [list]
- Gaps: topics this segment cares about with no content

### Content Quality Assessment
- Depth: [surface-level tips vs comprehensive guides]
- Originality: [unique data/insights vs generic advice]
- SEO optimization: [titles, meta descriptions, headings, internal links]
- CTA integration: [does content drive business outcomes?]
- Distribution: [is content shared/promoted beyond the blog?]

### Content Score
```
Content Dimension Score: [1-10]
  Volume: [1-5]
  Quality: [1-5]
  ICP alignment: [1-5]
  SEO effectiveness: [1-5]
  Distribution: [1-5]
```

## Phase 3: ICP and Market Fit Analysis

### ICP Validation
Review defined ICP segments against actual client base and market reality:

```
ICP SEGMENT ANALYSIS
---
Segment: [name]
  Defined criteria: [from config]
  Actual client match: [% of current clients that fit]
  Market size estimate: [TAM if available]
  Competition density: [how many competitors target this segment]
  Win rate signal: [are you winning deals in this segment?]
  Alignment verdict: STRONG / NEEDS_REFINEMENT / MISALIGNED
```

### Market Positioning
Where do you sit in the market?
```
POSITIONING MAP:
  Price point: [premium / mid-market / budget]
  Specialization: [specialist / generalist]
  Geography: [local / national / international]
  Client stage: [startup / growth / enterprise]
  Service depth: [full-service / boutique / niche]
```

### ICP Score
```
ICP Dimension Score: [1-10]
  Segment clarity: [1-5]
  Market-segment fit: [1-5]
  Client-ICP alignment: [1-5]
  Segment addressability: [1-5]
```

## Phase 4: Pricing and Packaging Analysis

### Pricing Perception
- Is pricing visible on the website? [yes/no]
- Pricing model: [retainer, project, hourly, value-based]
- Entry point: [minimum engagement size]
- Packaging clarity: [are packages defined and understandable?]

### Competitive Pricing Context
- WebSearch: `"{{service_type}} agency pricing" {{geography}}`
- Where does your pricing sit vs competitors?
- Is the value justification clear at your price point?

### Pricing-Value Alignment
```
PRICING ASSESSMENT
---
Service: [name]
  Price point: [range]
  Market comparison: [above / at / below market]
  Value justification visible: [yes/no]
  Case study ROI proof: [available / missing]
  Packaging: [clear tiers / custom only / unclear]
```

### Pricing Score
```
Pricing Dimension Score: [1-10]
  Market alignment: [1-5]
  Value communication: [1-5]
  Packaging clarity: [1-5]
  Accessibility: [1-5]
```

## Phase 5: Channel Effectiveness

### Active Channels Audit
For each channel in use:

```
CHANNEL: [name]
---
Status: [active / dormant / not started]
Investment level: [high / medium / low]
Activity frequency: [daily / weekly / monthly / sporadic]
Content quality: [assessment]
Engagement level: [metrics if available]
Lead generation: [generating leads? / brand only?]
ROI assessment: [positive / neutral / negative / unknown]
```

Channels to evaluate:
- Website / SEO (organic inbound)
- LinkedIn (personal + company page)
- Email outreach (cold email)
- Content marketing (blog, video, podcast)
- Paid advertising (Google, Meta, LinkedIn Ads)
- Referral / partnership program
- Events / conferences
- Instagram
- Twitter/X
- YouTube
- Community (Discord, Slack, forums)

### Channel-ICP Match
```
ICP Segment: [name]
  Where they spend time: [channels]
  Where we're active: [channels]
  Gap channels: [where ICP is but we're not]
  Wasted channels: [where we're active but ICP isn't]
```

### Channel Score
```
Channel Dimension Score: [1-10]
  Coverage: [1-5]
  ICP-channel alignment: [1-5]
  Activity consistency: [1-5]
  Lead generation effectiveness: [1-5]
```

## Phase 6: Competitive Differentiation

If `include_competitive` = true:

### Differentiation Assessment
```
DIFFERENTIATION MATRIX
---
Dimension        | Us          | Comp 1      | Comp 2      | Comp 3
Core service     | [what]      | [what]      | [what]      | [what]
Unique angle     | [what]      | [what]      | [what]      | [what]
Proof points     | [count]     | [count]     | [count]     | [count]
Content volume   | [level]     | [level]     | [level]     | [level]
Price position   | [tier]      | [tier]      | [tier]      | [tier]
ICP overlap      | -           | [%]         | [%]         | [%]
```

### Competitive Advantages
- What do you do that no competitor does?
- What do you do better than all competitors?
- What social proof do you have that competitors lack?

### Competitive Vulnerabilities
- Where are competitors stronger?
- What do they offer that you don't?
- Where are they winning deals you should win?

### Competitive Score
```
Competitive Dimension Score: [1-10]
  Differentiation clarity: [1-5]
  Competitive awareness: [1-5]
  Unique advantages: [1-5]
  Vulnerability exposure: [1-5]
```

## Phase 7: GTM Health Report

Compile all dimensions into a single health report:

```
GTM HEALTH REPORT -- [Date]
Prepared for: [agency.name]
===

OVERALL GTM HEALTH SCORE: [X]/10

DIMENSION SCORES:
  Website & Digital Presence:  [X]/10  [bar chart]
  Content Strategy:            [X]/10  [bar chart]
  ICP & Market Fit:            [X]/10  [bar chart]
  Pricing & Packaging:         [X]/10  [bar chart]
  Channel Effectiveness:       [X]/10  [bar chart]
  Competitive Differentiation: [X]/10  [bar chart]

---

TOP STRENGTHS:
1. [Strength] -- [evidence]
2. [Strength] -- [evidence]
3. [Strength] -- [evidence]

CRITICAL GAPS:
1. [Gap] -- Impact: [HIGH/MEDIUM] -- [what it's costing you]
2. [Gap] -- Impact: [HIGH/MEDIUM] -- [what it's costing you]
3. [Gap] -- Impact: [HIGH/MEDIUM] -- [what it's costing you]

OPPORTUNITIES:
1. [Opportunity] -- Effort: [LOW/MEDIUM/HIGH] -- Expected impact: [description]
2. [Opportunity] -- Effort: [LOW/MEDIUM/HIGH] -- Expected impact: [description]
3. [Opportunity] -- Effort: [LOW/MEDIUM/HIGH] -- Expected impact: [description]

THREATS:
1. [Threat] -- Likelihood: [HIGH/MEDIUM/LOW] -- [mitigation]
2. [Threat] -- Likelihood: [HIGH/MEDIUM/LOW] -- [mitigation]
```

## Phase 8: Recommendations

Generate prioritized action plan:

```
GTM ACTION PLAN
===

QUICK WINS (do this week, low effort, high impact):
1. [Action] -- Dimension: [which dimension it improves]
   Expected impact: [specific]
2. [Action]
3. [Action]

SHORT-TERM (next 2-4 weeks):
1. [Action] -- Dimension: [which]
   Investment: [time/money estimate]
   Expected impact: [specific]
2. [Action]
3. [Action]

MEDIUM-TERM (next quarter):
1. [Action] -- Dimension: [which]
   Investment: [time/money estimate]
   Expected impact: [specific]
2. [Action]

STRATEGIC (next 6 months):
1. [Action] -- Dimension: [which]
   Investment: [time/money estimate]
   Expected impact: [specific]

DO NOT DO (traps to avoid):
- [Anti-pattern]: [why it's tempting but wrong]
- [Anti-pattern]: [why]
```

## Phase 9: Output

Return structured JSON:

```json
{
  "report_date": "2026-03-07",
  "agency": "{{agency.name}}",
  "overall_score": 6.8,
  "dimensions": {
    "website": {"score": 7.5, "strengths": ["Clear value prop", "Strong case studies"], "gaps": ["No blog", "Weak mobile CTA"]},
    "content": {"score": 4.2, "strengths": ["Quality case studies"], "gaps": ["No blog", "No SEO content", "No distribution"]},
    "icp": {"score": 8.0, "strengths": ["Well-defined segments", "Strong client-ICP match"], "gaps": ["International segment underserved"]},
    "pricing": {"score": 6.5, "strengths": ["Competitive for market"], "gaps": ["No pricing on website", "Packaging unclear"]},
    "channels": {"score": 5.8, "strengths": ["LinkedIn active", "Cold email running"], "gaps": ["No SEO", "Instagram dormant", "No referral program"]},
    "competitive": {"score": 7.0, "strengths": ["Unique CRO + catalog combo"], "gaps": ["Competitors have more case studies", "Pricing transparency"]}
  },
  "top_strengths": [
    "Strong ICP definition with proven client-market fit",
    "Unique service combination (CRO + catalog) that competitors don't offer",
    "Compelling case study with real metrics"
  ],
  "critical_gaps": [
    {"gap": "No content/SEO strategy", "impact": "HIGH", "cost": "Missing organic inbound leads entirely"},
    {"gap": "Single case study", "impact": "HIGH", "cost": "Limited social proof for different segments"},
    {"gap": "No referral program", "impact": "MEDIUM", "cost": "Not leveraging existing client relationships"}
  ],
  "recommendations": {
    "quick_wins": [
      {"action": "Add pricing page with 3 tiers", "dimension": "pricing", "effort": "LOW"},
      {"action": "Build second case study from existing client data", "dimension": "website", "effort": "LOW"}
    ],
    "short_term": [
      {"action": "Launch blog with 2 posts/month targeting ICP keywords", "dimension": "content", "effort": "MEDIUM"},
      {"action": "Set up referral incentive for existing clients", "dimension": "channels", "effort": "LOW"}
    ],
    "medium_term": [
      {"action": "Build SEO content cluster around core services", "dimension": "content", "effort": "HIGH"},
      {"action": "Launch LinkedIn thought leadership program", "dimension": "channels", "effort": "MEDIUM"}
    ]
  },
  "previous_comparison": null,
  "generated_at": "2026-03-07T10:00:00Z"
}
```

## Phase 10: Review

Present the GTM Health Report.

**APPROVAL GATE**: "GTM analysis complete. Overall score: [X]/10. Review the action plan?"

Save report as `gtm-analysis-{{date}}.md` for historical tracking.

Schedule next review: quarterly cadence recommended.

## Example Usage

Trigger phrases:
- "Run a GTM analysis"
- "How strong is our go-to-market?"
- "Evaluate our positioning"
- "GTM health check"
- "Where are the gaps in our marketing?"
- "Audit our GTM strategy"
- "Compare our positioning to competitors"
- "What should we focus on for growth?"
