---
name: meeting-prep
description: Research a prospect company and generate a sales meeting brief in minutes. Extracts business context, likely pain points, decision-maker signals, and specific questions to ask. No API keys required.
---

# Meeting Prep

Research any company before a sales call and generate a structured brief with everything needed to walk in prepared.

## What this does

Three phases:

1. **Company Research** - Extract business context, size signals, tech stack, marketing activity, hiring signals
2. **Pain Point Detection** - Identify likely pain points based on what is missing or underperforming
3. **Meeting Brief** - Generate questions, talking points, and service fit analysis

## How to use

Pass a URL, company name, or LinkedIn URL:

```
/meeting-prep https://empresa.com
```

Or with context:
```
/meeting-prep https://empresa.com - llamada de 30 minutos, contacto es el CMO
```

## Phase 1 - Company Research

Use ddgs and web scraping to collect:

- **Business type** - B2B / B2C, local / national / international
- **Size signals** - team size (from website, LinkedIn), years in business
- **Services / products** - what exactly do they sell
- **Target customers** - who do they serve (inferred from copy + case studies)
- **Current marketing** - are they running ads? SEO visible? Social active?
- **Tech stack** - CMS, analytics, chat, email tool, CRM signals
- **Hiring signals** - job postings can reveal priorities (hiring a "SEO specialist" = SEO is a priority or a pain)
- **Recent news** - press, blog, funding, partnerships

```python
from scripts.web_inspector import inspect_website, detect_tech_stack

data = inspect_website(url)
tech = data["tech_stack"]
```

Use ddgs to search:
- "[company name] news"
- "[company name] jobs" or site:linkedin.com/jobs [company]
- "[company name] review" or "[company name] testimonials"

## Phase 2 - Pain Point Detection

Based on Phase 1 findings, identify likely pain points.

**Pain point signals by absence:**

| Missing | Likely pain |
|---------|------------|
| No analytics / GTM | "We don't know what's working" |
| No Meta Pixel | Cannot do retargeting, no audience data |
| No conversion tracking | Cannot justify ad spend, blind on ROI |
| No case studies | Struggling to close deals, lack social proof |
| No blog / thin content | Invisible in search, losing to SEO competitors |
| Wix / Squarespace on a growing B2B | Platform limitations becoming painful |
| Outdated design (5+ years old) | Not converting new visitors, embarrassed to send link |
| No chat tool | Missing async conversations from website |
| No email capture | Losing leads they paid to get |
| Social profiles inactive | Know they should be doing social, not doing it |

**Pain point signals by context:**

| Context | Likely pain |
|---------|------------|
| Service business, no testimonials | Trust and closing rate |
| eCommerce, no pixel | Cannot scale paid acquisition |
| B2B, no case studies | Long sales cycle, no proof |
| Hiring for marketing roles | Current marketing not performing |
| Many competitors with better SEO | Losing organic traffic |
| Recent rebrand or website launch | Want to make the investment pay off |

Output 3-5 specific, evidence-based pain points. Not generic.

## Phase 3 - Meeting Brief

Generate a structured brief the agency rep can read in 5 minutes before the call.

### Brief format

```
## Meeting Brief: [Company Name]

Date: [date]
Contact: [name + role if known]
Meeting type: [discovery / follow-up / proposal]

---

### Company Snapshot

[3-4 sentences: what they do, who they serve, current state of their marketing]

### What They Likely Care About

1. [Pain 1] - Evidence: [what you found]
2. [Pain 2] - Evidence: [what you found]
3. [Pain 3] - Evidence: [what you found]

### Their Situation vs Competitors

[1-2 sentences: are they ahead or behind competitors in their market?]

### Questions to Ask

Opening (to confirm your research):
- "I noticed you're on [platform] - are you happy with it or is that something you've been wanting to change?"
- "I saw you're [doing X / not doing Y] - how's that been working for you?"

Problem discovery:
- [specific question tied to Pain 1]
- [specific question tied to Pain 2]
- "What does your current reporting look like? How do you know what's working?"

Budget and process:
- "Do you have a marketing budget you're working with, or is that still to be defined?"
- "Who else is involved in decisions like this?"

### Services That Fit

Based on findings:
1. [Service] - addresses [specific pain] - entry point
2. [Service] - addresses [specific pain] - monthly retainer potential

### Red Flags to Watch For

- [signal that means this is a bad fit - e.g. "if they mention they just signed with another agency"]
- [signal that means budget is likely low - e.g. "Wix free tier, no ads running, single person team"]

### One Thing to Remember

[Single most important thing from the research. The one insight that will make them feel you did your homework.]
```

## References

- `references/research-checklist.md` - what to check per company type
- `references/question-banks.md` - question library by pain type

## Output principles

1. Brief must be readable in under 5 minutes
2. Every pain point needs specific evidence from the research
3. Questions must be specific to THIS company, not generic sales questions
4. Do not include services that do not match what the agency offers (if provided)
5. The "One Thing to Remember" is mandatory - it is the line that builds rapport
