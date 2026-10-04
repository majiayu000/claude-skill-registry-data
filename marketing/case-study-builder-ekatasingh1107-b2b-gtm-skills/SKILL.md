---
name: case-study-builder
description: >
  Turns client wins into structured case studies in multiple formats.
  Gathers before/after metrics, structures as Problem-Solution-Results,
  and outputs landing page copy, one-pager, social snippets, and email insert.
tags: [content, case-study, social-proof, marketing]
---

# Case Study Builder

Transforms raw client results data into polished, structured case studies. Follows the Problem-Solution-Results framework, pulls real metrics, and generates multiple output formats: full landing page copy, one-pager for sales collateral, social media snippets, and email-embeddable summaries.

## Prerequisites

- `agency.config.json` populated (services, brand voice)
- Client results data (metrics, timeline, deliverables) -- from CRM, QBR, or user input
- Client name and permission to use as a case study
- Optional: `brand-voice` capability output for tone consistency

## Capabilities Used

1. `crm-writer` -- pull client engagement history, deliverables, and metrics
2. `company-researcher` -- refresh company context for the case study narrative
3. `email-copywriter` -- generate email-embeddable case study snippet
4. `carousel-creator` -- generate social media carousel content
5. `landing-page-copy` -- generate full landing page case study
6. `brand-voice` -- ensure tone consistency across formats

## Phase 0: Intake

Read `agency.config.json`:
- `services[]` -- map client work to service categories
- `case_studies[]` -- check if this client already has an entry (update vs create)
- `agency.name`, `agency.domain` -- for attribution
- `brand_voice` -- tone and style guidelines

Accept parameters:
- `client_name` -- (required) the client featured in the case study
- `project_type` -- which service(s) the case study covers
- `time_period` -- when the work was done (e.g., "Jan-Mar 2026")
- `data_source` -- `crm` | `qbr` | `manual`. Default: `manual`
- `formats` -- array of desired outputs. Default: `["landing_page", "one_pager", "social", "email"]`
- `anonymize` -- boolean, use "Industry Leader" instead of client name. Default: `false`
- `approval_required` -- boolean, flag for client approval before publishing. Default: `true`

## Phase 1: Data Gathering

### From CRM (if data_source = crm)
Pull from CRM tabs:
- Deliverables completed during `time_period`
- Metrics tracked (before and after)
- Meeting notes mentioning results or feedback
- Client testimonial quotes (if captured)

### From QBR (if data_source = qbr)
Reference most recent `qbr-builder` output:
- Wins section
- Key metrics with quarter-over-quarter changes
- Deliverables completed
- Client feedback captured during QBR

### Manual Input (if data_source = manual)
Prompt for structured input:
```
CLIENT RESULTS INPUT
---
1. Company name and industry:
2. Their situation BEFORE you started (pain points, metrics):
3. What you did (services, deliverables, timeline):
4. Results AFTER (metrics, improvements, outcomes):
5. Client quote (if available):
6. Any unexpected wins or learnings:
7. Timeline (start to results):
```

### Supplementary Research
Run `company-researcher` (quick) for:
- Company description and industry context
- Company size and market position
- Their website URL and social profiles (for linking)

## Phase 2: Narrative Structuring

Organize data into the Problem-Solution-Results (PSR) framework:

### The Problem
- **Situation**: What was the client's business context?
- **Pain**: What specific challenge were they facing?
- **Stakes**: What would happen if the problem wasn't solved?
- **Previous attempts**: Had they tried other solutions?

Write 2-3 paragraphs that make the reader think "that sounds like my problem."

### The Solution
- **Approach**: How did you diagnose and plan the solution?
- **What was done**: Specific deliverables, not vague descriptions
- **How it was done**: Methodology, tools, process (shows expertise)
- **Timeline**: How long from kickoff to results
- **Collaboration**: How did you work with the client's team?

Write 2-3 paragraphs focused on the "how" -- this builds trust and differentiates from generic claims.

### The Results
- **Primary metric**: The headline number (e.g., "+18% conversion rate")
- **Secondary metrics**: Supporting numbers (traffic, AOV, revenue, speed)
- **Qualitative outcomes**: Client satisfaction, team efficiency, confidence
- **Unexpected wins**: Bonus outcomes they didn't plan for
- **Ongoing impact**: Is the improvement sustained?

Present as:
```
RESULTS SNAPSHOT
---
Headline metric: [+X% improvement in Y]
Supporting metrics:
  - [Metric 1]: [before] -> [after] ([change])
  - [Metric 2]: [before] -> [after] ([change])
  - [Metric 3]: [before] -> [after] ([change])
Timeline: [X weeks/months from start to results]
```

### The Testimonial
If a client quote is available, place it prominently. If not, note it as a gap to fill:
- "TODO: Request testimonial quote from [contact name]"

## Phase 3: Format Generation

### Format 1: Landing Page Copy
Full-length case study for website (800-1200 words):

```
LANDING PAGE CASE STUDY
===

HEADLINE: How [Client/Industry] Achieved [Headline Result] with [Service]
SUBHEADLINE: [One sentence expanding on the result with timeline]

HERO SECTION:
- Client logo (placeholder)
- Headline metric in large text
- Industry tag, service tag

CLIENT SNAPSHOT:
| Industry | [vertical] |
| Company Size | [employees/revenue tier] |
| Platform | [Shopify, etc.] |
| Services Used | [list] |
| Timeline | [duration] |

THE CHALLENGE:
[2-3 paragraphs from Phase 2 Problem section]

THE APPROACH:
[2-3 paragraphs from Phase 2 Solution section]
[Include a visual process/timeline element]

THE RESULTS:
[Metrics grid with before/after comparison]
[Pull quote from client if available]

KEY TAKEAWAYS:
1. [Insight applicable to similar companies]
2. [Insight about the approach]
3. [Insight about the results]

CTA:
"Facing similar challenges? Let's talk about your [service area]."
[Calendar link / contact form reference]
```

### Format 2: One-Pager (Sales Collateral)
Single-page PDF-ready format (300-400 words):

```
ONE-PAGER
===

[Agency Logo]                     [Client Logo]

CASE STUDY: [Client Name]
[Headline: How [Client] achieved [result]]

THE CHALLENGE:
[2-3 sentences]

WHAT WE DID:
- [Deliverable 1]
- [Deliverable 2]
- [Deliverable 3]

RESULTS:
+-------------------+-------------------+
| [Metric 1]        | [Metric 2]        |
| [BIG NUMBER]      | [BIG NUMBER]      |
| [context]         | [context]         |
+-------------------+-------------------+
| [Metric 3]        | [Metric 4]        |
| [BIG NUMBER]      | [BIG NUMBER]      |
| [context]         | [context]         |
+-------------------+-------------------+

"[Client quote]" -- [Name, Title]

Timeline: [duration] | Services: [list] | Industry: [vertical]

[Agency name] | [domain] | [CTA]
```

### Format 3: Social Snippets
LinkedIn post, Twitter/X thread, and Instagram caption:

**LinkedIn Post** (1200-1500 characters):
```
[Hook line with the headline metric]

[Client] came to us with [problem in 1 sentence].

Here's what we did:
1. [Step 1]
2. [Step 2]
3. [Step 3]

The results:
[Metric 1]: [before] -> [after]
[Metric 2]: [before] -> [after]
[Metric 3]: [before] -> [after]

[Key insight or lesson learned]

[CTA: link to full case study or "DM me if you're facing similar challenges"]

#[relevant] #[hashtags]
```

**Twitter/X Thread** (3-5 tweets):
```
Tweet 1: [Hook with headline metric]
Tweet 2: The problem: [2 sentences]
Tweet 3: What we did: [2-3 bullet points]
Tweet 4: Results: [metrics]
Tweet 5: [Key lesson + CTA]
```

**Instagram Caption** (for carousel post):
```
[Hook] + [Short narrative] + [Results] + [CTA]
Carousel slides: [slide-by-slide content for carousel-creator]
```

### Format 4: Email Insert
Short case study block for outreach emails (80-120 words):

```
EMAIL INSERT
===

Subject line reference: "How [Client] got [result] in [timeline]"

Body insert:
"Quick example: [Client], a [industry] brand, was struggling with [1-sentence problem]. We [1-sentence solution]. In [timeline], they saw [headline metric] and [secondary metric]. [Link to full case study]"
```

## Phase 4: Quality Check

Before output, verify:
- [ ] All metrics have "before" and "after" values
- [ ] Timeline is specific (not "a few months")
- [ ] Client name used correctly (or anonymized if `anonymize` = true)
- [ ] No confidential data exposed (revenue figures, unless approved)
- [ ] CTA links reference agency domain from config
- [ ] Tone matches `brand_voice` settings
- [ ] No superlatives without data backing ("best", "leading", "top")
- [ ] Each format stands alone (doesn't require reading another format)

## Phase 5: Output

Return structured JSON:

```json
{
  "client_name": "Kibi Sports",
  "anonymized": false,
  "project_type": "Conversion Rate Optimization",
  "time_period": "Jan-Mar 2026",
  "headline_metric": "+18% conversion rate",
  "results_summary": {
    "primary": {"metric": "Conversion Rate", "before": "2.4%", "after": "2.8%", "change": "+18%"},
    "secondary": [
      {"metric": "Page Load Speed", "before": "4.2s", "after": "2.1s", "change": "-50%"},
      {"metric": "Revenue", "before": "INR 25,40,000/mo", "after": "INR 31,00,000/mo", "change": "+22%"},
      {"metric": "Bounce Rate", "before": "50%", "after": "42%", "change": "-16%"}
    ],
    "timeline": "12 weeks"
  },
  "formats": {
    "landing_page": "[full markdown content]",
    "one_pager": "[formatted content]",
    "social": {
      "linkedin": "[post content]",
      "twitter_thread": ["tweet1", "tweet2", "tweet3", "tweet4"],
      "instagram": "[caption + carousel outline]"
    },
    "email_insert": "[short block]"
  },
  "testimonial": {
    "quote": "They transformed our product pages. The numbers speak for themselves.",
    "attribution": "Amit K., Founder",
    "status": "approved"
  },
  "approval_status": "pending_client_approval",
  "generated_at": "2026-03-07T10:00:00Z"
}
```

## Phase 6: Review and Distribution

Present all formats for review.

**APPROVAL GATE**: "Case study ready in [N] formats. Review each before publishing?"

Post-approval actions:
- Update `agency.config.json` `case_studies[]` array with the new entry
- Flag for website publishing (landing page format)
- Queue social posts (if `nurture-sequence` or social calendar exists)
- Make email insert available to `cold-email-drafter` and `outreach-draft-pipeline`

## Example Usage

Trigger phrases:
- "Build a case study from the Kibi Sports results"
- "Turn last quarter's results for [client] into a case study"
- "I need a case study for the website, use [client] data"
- "Create social proof content from [client] metrics"
- "Generate a one-pager case study for [client]"
- "Case study time -- here are the numbers: [paste metrics]"
