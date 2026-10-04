---
name: long-form-writer
description: >
  Generates full long-form content: whitepapers, eBooks, research reports,
  and pillar pages. Takes a content brief and produces 2000-5000 word drafts
  with sections, data points, and CTAs.
tags: [content, writing, long-form, whitepaper, ebook, pillar-page]
---

# Long-Form Writer

Generates publication-ready long-form content from a content brief. Produces structured, data-backed drafts for whitepapers, eBooks, research reports, and SEO pillar pages. Each piece is built around the agency's expertise, case studies, and industry knowledge.

## Prerequisites

- `agency.config.json` populated (agency info, services, case studies)
- Content brief (ideally output from `content-brief` skill)
- Optional: research data from `blog-researcher` or `company-researcher`

## Phase 0: Intake

Read `agency.config.json`:
- `agency.name`, `agency.founder`, `agency.tagline` -- for byline and brand references
- `services[]` -- for naturally weaving in service expertise
- `case_studies[]` -- for proof points and examples
- `outreach.tone` -- baseline voice (adapt for long-form: more authoritative, educational)

Accept parameters:
- `content_type` -- (required) one of: `whitepaper`, `ebook`, `research-report`, `pillar-page`, `guide`, `playbook`
- `brief` -- (required) content brief object or text with topic, target audience, key points
- `word_count_target` -- (optional) target word count. Default: by type (see below)
- `tone` -- (optional) override: `educational`, `authoritative`, `conversational`, `data-driven`. Default: `authoritative`
- `research` -- (optional) research data to incorporate
- `seo_keywords` -- (optional) array of keywords to target for pillar pages
- `include_cta` -- boolean. Default: `true`
- `gated` -- boolean, is this gated content (lead magnet)? Default: `false`

### Word Count Targets by Type
| Content Type | Word Range | Sections |
|-------------|-----------|----------|
| Whitepaper | 3000-5000 | 6-10 |
| eBook | 4000-8000 | 8-12 chapters |
| Research Report | 2000-4000 | 5-8 |
| Pillar Page | 3000-6000 | 8-15 |
| Guide | 2000-4000 | 5-8 |
| Playbook | 2000-3000 | 5-7 |

## Phase 1: Structure Planning

Based on the brief and content type, generate the document structure:

### Whitepaper Structure
```
1. Title Page
   - Title (under 12 words, benefit-driven)
   - Subtitle (context or scope)
   - Author: [agency.founder] | [agency.name]
   - Date

2. Executive Summary (150-250 words)
   - The problem
   - Key findings
   - Recommended approach

3. The Problem / Market Context (400-600 words)
   - Industry challenge with data
   - Why it matters now
   - Cost of inaction

4-7. Core Sections (500-800 words each)
   - One key argument per section
   - Data + example + insight pattern
   - Case study integration where relevant

8. Recommendations / Framework (400-600 words)
   - Actionable steps
   - Decision framework or checklist

9. Conclusion (200-300 words)
   - Summary of key points
   - Forward-looking statement

10. About [agency.name] (100-150 words)
    - Brief company description
    - CTA: consultation, audit, demo

11. Sources / References
```

### Pillar Page Structure
```
1. H1: Primary keyword in title
2. Introduction (200-300 words) -- what they'll learn, who it's for
3. Table of Contents (linked)
4. Section 1: [H2 with keyword variation]
   - 400-600 words
   - Internal links to cluster content
5-10. Additional H2 sections
   - Each targets a long-tail keyword
   - Each can standalone as a useful section
11. FAQ section (5-10 questions with schema markup suggestions)
12. Conclusion + CTA
13. Related Resources (internal links)
```

### eBook Structure
```
Cover page
Table of Contents
Introduction: Why this matters
Chapter 1-8: One core topic per chapter
   - Opening hook
   - Teaching content
   - Example/case study
   - Key takeaway callout box
Chapter 9: Action plan / implementation
Conclusion
About the author
CTA page
```

## Phase 2: Research Integration

For each section, identify:
- **Data points needed**: stats, percentages, trends (from brief or research input)
- **Case study fit**: which `case_studies[]` from config support this section
- **Expert quotes**: reference industry leaders, studies, reports
- **Competitive insight**: what others in the space are saying

Rules for data:
- Cite sources for all statistics
- Use recent data (within 2 years)
- If no hard data available, use qualitative observations from case studies
- Never fabricate statistics

## Phase 3: Draft Generation

Write each section following these rules:

### Writing Rules (non-negotiable)
1. **No fluff**: Every sentence must inform, argue, or prove. Delete filler.
2. **Active voice**: "We increased conversion by 40%" not "Conversion was increased by 40%"
3. **Concrete over abstract**: Numbers, examples, specifics. No "many companies struggle with..."
4. **One idea per paragraph**: Short paragraphs (3-5 sentences max)
5. **Scannable**: Use headers, bullet points, bold key phrases, callout boxes
6. **No jargon without explanation**: First use of any technical term gets a brief definition
7. **Case study integration**: Weave in naturally ("When we worked with [client], we found...")
8. **Transition sentences**: Each section flows logically to the next
9. **No self-congratulation**: Show expertise through substance, not claims

### Formatting Elements
- **Callout boxes**: Key stats, definitions, pro tips (mark with `> CALLOUT:`)
- **Pull quotes**: One per major section (mark with `> QUOTE:`)
- **Bullet lists**: For actionable items, checklists, features
- **Numbered lists**: For sequential steps or rankings
- **Tables**: For comparisons, specs, frameworks
- **Bold**: Key terms, important numbers, section openers

### CTA Integration
If `include_cta` = true:
- **Soft CTA**: End of each major section ("Want help with this? [link]")
- **Medium CTA**: After case study sections ("See how we did this for [client]")
- **Hard CTA**: Final section ("Schedule a free consultation")
- For gated content: the CTA is the download itself (pre-gate landing page copy)

## Phase 4: SEO Optimization (Pillar Pages)

If content_type = `pillar-page`:
1. Primary keyword in H1, first paragraph, and at least 2 H2s
2. Secondary keywords distributed naturally across sections
3. Keyword density: 1-2% for primary, 0.5-1% for secondaries
4. Meta title: under 60 chars, keyword-forward
5. Meta description: under 155 chars, includes keyword and value prop
6. Schema markup suggestions (FAQ, HowTo, Article)
7. Internal linking opportunities: flag where cluster content can link
8. External link suggestions: 3-5 authoritative sources to reference

## Phase 5: Quality Check

Before returning:
1. **Word count**: Within target range for content type
2. **Section balance**: No section more than 2x the length of others
3. **Data backed**: At least one stat or example per major section
4. **Case study count**: At least 1-2 case studies referenced
5. **CTA count**: Appropriate density (not every paragraph, but present)
6. **Readability**: Flesch-Kincaid target 50-65 (professional but accessible)
7. **Banned phrases**: Check against `outreach.banned_phrases`
8. **No plagiarism patterns**: All content original, data properly attributed

## Phase 6: Output

Return structured JSON:

```json
{
  "content_type": "whitepaper",
  "title": "The D2C CRO Playbook: How Indian Brands Are Doubling Conversion Rates on Shopify",
  "subtitle": "A data-backed guide to product page optimization for growing D2C brands",
  "author": "Ekata Singh | Plasho",
  "word_count": 3847,
  "sections": [
    {
      "heading": "Executive Summary",
      "content": "Full section text...",
      "word_count": 210,
      "data_points": ["40% of D2C brands have sub-2% conversion rates"],
      "case_studies_referenced": []
    },
    {
      "heading": "The Hidden Cost of Poor Product Pages",
      "content": "Full section text...",
      "word_count": 520,
      "data_points": ["Baymard Institute: 69.8% cart abandonment rate"],
      "case_studies_referenced": ["Kibi Sports"]
    }
  ],
  "seo": {
    "meta_title": "D2C CRO Playbook: Double Your Shopify Conversion Rate",
    "meta_description": "Learn how Indian D2C brands are optimizing product pages to 2x conversion rates. Data-backed strategies from real Shopify case studies.",
    "primary_keyword": "D2C CRO",
    "secondary_keywords": ["shopify conversion rate", "product page optimization", "D2C ecommerce"],
    "keyword_density": {"D2C CRO": "1.4%"}
  },
  "ctas": [
    {"type": "soft", "text": "Want a free CRO audit?", "placement": "after section 3"},
    {"type": "hard", "text": "Schedule a consultation", "placement": "conclusion"}
  ],
  "sources": [
    {"name": "Baymard Institute", "data": "69.8% cart abandonment rate", "year": 2025}
  ],
  "generated_at": "2026-03-13T10:00:00Z"
}
```

## Example Usage

Trigger phrases:
- "Write a whitepaper about CRO for D2C brands"
- "Generate an eBook about Shopify store optimization"
- "Create a pillar page for 'Shopify development India'"
- "Write a research report on D2C ecommerce trends in India"
- "Draft a guide on email marketing for Shopify stores"
- "Create a gated playbook about product page optimization"
