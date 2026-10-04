---
name: content-brief
description: Generate SEO-informed content briefs with competitive positioning
tags: [content, seo, brief, marketing]
---

# Content Brief

Generates comprehensive, SEO-informed content briefs by combining topic research, keyword analysis, and competitive gap analysis. Uses `signal-scanner` capabilities for topic research and `company-researcher` patterns for competitor content analysis. The output is a ready-to-write brief with outline, keywords, differentiation angles, and distribution plan.

## Prerequisites

- `agency.config.json` in the project root
- WebSearch tool available
- User-provided topic or target keyword

## Capabilities Used

1. `signal-scanner` -- for topic research and trending content discovery
2. `company-researcher` -- for competitor content analysis and positioning research

## Phase 0: Read Agency Context

1. Read `agency.config.json` from the project root.
2. Extract `services[].name` and `services[].keywords` -- these define the agency's expertise areas.
3. Extract `icp.segments[]` -- the audience this content should attract.
4. Extract `agency_name` and any existing content strategy settings.
5. Note the agency's primary markets and industries for relevance filtering.
6. Accept parameters:
   - `topic` -- (required) the topic or keyword to build a brief for
   - `content_type` -- `blog` | `guide` | `case-study` | `comparison` | `how-to` | `listicle`. Default: `blog`
   - `target_audience` -- which ICP segment this content targets. Default: primary segment
   - `word_count_target` -- optional override. Default: determined by competitive analysis

## Phase 1: Topic Research

Run WebSearch queries to understand the topic landscape:

**Top ranking content:**
- `"{{topic}}" best practices`
- `"{{topic}}" guide {{current_year}}`
- `"{{topic}}" for {{icp_industry}}`
- `how to {{topic}}`
- `"{{topic}}" tips {{current_year}}`

Visit top 10 results from search. For each, extract:
- URL and domain authority indicator (known brand vs niche blog)
- Title and H1
- Word count (estimate from content length)
- Headings structure (H2s and H3s)
- Key points covered
- Content format (listicle, how-to, narrative, data-driven)
- Publication date (is it fresh or outdated?)
- Unique angle or hook
- Internal/external links pattern
- Multimedia usage (images, videos, infographics, tools)

Compile:
```
TOP 10 RANKING CONTENT ANALYSIS:
---
Average word count: [range]
Most common format: [format]
Publication recency: [X of 10 published in last 12 months]
Content depth: [surface / moderate / deep]
Common H2 topics: [list the most repeated subtopics]
```

## Phase 2: Keyword Analysis

From the search results and topic research, build a keyword map:

**Primary keyword:**
- The main keyword the content should rank for
- Search intent classification: informational | commercial | transactional | navigational

**Secondary keywords:**
- 5-10 variations and related terms found across top results
- Long-tail variants

**Question keywords (People Also Ask patterns):**
- Search `"{{topic}}" questions` and `{{topic}} site:quora.com OR site:reddit.com`
- Extract the top 5-8 questions people ask about this topic
- These become H2 candidates or FAQ sections

**Semantic keywords:**
- Terms that consistently appear in top-ranking content
- Industry-specific jargon the audience would use
- Related concepts that signal topical authority

**Keyword difficulty estimate:**
- Based on who currently ranks: all major brands = high difficulty, mix of small sites = medium, mostly forums/low-authority = low
- Recommendation: pursue | skip | long-tail alternative

Compile:
```
KEYWORD MAP:
---
Primary: [keyword] -- Intent: [type] -- Difficulty: [high/medium/low]
Secondary: [keyword1], [keyword2], [keyword3], [keyword4], [keyword5]
Questions:
  1. [question] -- [search volume indicator: high/medium/low based on PAA presence]
  2. [question]
  3. [question]
  4. [question]
  5. [question]
Semantic: [term1], [term2], [term3], [term4], [term5]
```

## Phase 3: Competitive Gap Analysis

Analyze the top 3 ranking articles in depth:

**For each competitor article:**
- What they cover thoroughly
- What they mention but don't go deep on
- What they miss entirely
- Their unique angle/value-add
- Their CTA and monetization approach
- Quality of examples and data

**Gap identification:**
- Topics covered by 0 of 3 articles (blue ocean)
- Topics covered shallowly by all 3 (depth opportunity)
- Perspectives missing (practitioner POV, data-driven, case-study-backed)
- Recency gaps (outdated stats, old examples, pre-{{current_year}} advice)

**Agency differentiation:**
- Cross-reference gaps against `services[].keywords`
- Where can the agency's real expertise add value no competitor can?
- What case study results or data can be cited?
- What practitioner insight is unique to the agency?

Compile:
```
COMPETITIVE GAP ANALYSIS:
---
TOP 3 COMPETITORS:
1. [URL] -- Covers: [topics]. Misses: [gaps]. Angle: [their hook]
2. [URL] -- Covers: [topics]. Misses: [gaps]. Angle: [their hook]
3. [URL] -- Covers: [topics]. Misses: [gaps]. Angle: [their hook]

BLUE OCEAN TOPICS (nobody covers):
- [topic]
- [topic]

DEPTH OPPORTUNITIES (covered shallowly):
- [topic]
- [topic]

OUR UNIQUE ANGLE:
[What makes our take different, based on agency expertise and case study data]
```

## Phase 4: Generate Brief

Assemble the complete content brief:

```
CONTENT BRIEF: [Topic]
===

TARGET KEYWORD: [primary keyword]
SECONDARY KEYWORDS: [comma-separated list]
SEARCH INTENT: [informational / commercial / transactional]
TARGET WORD COUNT: [range, based on competitive analysis]
CONTENT TYPE: [blog / guide / case-study / comparison / how-to / listicle]
TARGET AUDIENCE: [ICP segment name and description]

---

TITLE OPTIONS:
1. [title option -- SEO optimized, includes primary keyword]
2. [title option -- curiosity/click-driven]
3. [title option -- data or number-led]

META DESCRIPTION:
[155 characters max, includes primary keyword, compelling reason to click]

---

OUTLINE:

H1: [chosen title]

Introduction (150-200 words):
- Hook: [specific opening approach -- stat, question, pain point, contrarian take]
- Context: [why this matters now]
- Promise: [what the reader will learn/get]
- Credibility: [brief agency expertise signal]

H2: [Section 1 Title]
- Key points to cover:
  - [point 1]
  - [point 2]
  - [point 3]
- Unique angle: [what we add that competitors don't]
- Supporting evidence: [data, example, or case study to include]

H2: [Section 2 Title]
- Key points to cover:
  - [point 1]
  - [point 2]
  - [point 3]
- Unique angle: [differentiation]
- Supporting evidence: [data or example]

H2: [Section 3 Title]
- Key points to cover:
  - [point 1]
  - [point 2]
- Unique angle: [differentiation]

H2: [Section 4 Title -- if applicable]
- Key points to cover

H2: [FAQ / Common Questions -- if question keywords warrant it]
- Q: [question keyword 1]
  A: [brief answer direction, 50-100 words]
- Q: [question keyword 2]
  A: [brief answer direction]
- Q: [question keyword 3]
  A: [brief answer direction]

Conclusion (100-150 words):
- Summary of key takeaways
- CTA: [specific next action for the reader]

---

CONTENT REQUIREMENTS:

Must include:
- [specific data point or statistic]
- [real example or mini case study]
- [tool, framework, or template the reader can use]
- [at least 1 original visual -- chart, diagram, or screenshot]

Internal links (to agency pages):
- [page 1] -- link from [section]
- [page 2] -- link from [section]

External references (credible sources):
- [source 1] -- for [claim]
- [source 2] -- for [data point]

Keywords to naturally include:
- Primary: use in H1, first 100 words, 1 H2, conclusion
- Secondary: distribute across H2s and body text
- Semantic: weave naturally throughout

---

DIFFERENTIATION:

What competitors cover well:
- [summary of common ground]

What competitors miss:
- [gap 1 -- we address in Section X]
- [gap 2 -- we address in Section Y]

Our unique angle:
[2-3 sentences on what makes this piece different from everything else ranking]

Expert insight to leverage:
[Specific agency expertise, client results, or practitioner knowledge to weave in]

---

CTA STRATEGY:

Primary CTA: [what action the reader should take]
Placement: [where in the article -- after which section]
Secondary CTA: [softer ask -- newsletter, resource download, related content]
Placement: [end of article or sidebar]
```

## Phase 5: Distribution Plan

```
DISTRIBUTION PLAN:
===

Blog post:
- Publish on: [agency blog URL]
- Category: [blog category]
- Author: [suggested]
- Publish date: [recommended timing based on topic freshness]

LinkedIn:
- Article version: [yes/no -- for long-form LinkedIn publishing]
- Carousel: [5-7 slide breakdown of key points]
  - Slide 1: [hook/title]
  - Slide 2: [key insight 1]
  - Slide 3: [key insight 2]
  - Slide 4: [key insight 3]
  - Slide 5: [data point or case study]
  - Slide 6: [actionable takeaway]
  - Slide 7: [CTA]
- Text post: [2-3 sentence teaser with link]

Email newsletter:
- Subject line options:
  1. [option]
  2. [option]
- Excerpt: [150-word teaser for newsletter, ending with "Read the full guide ->"]

Social media posts (3-5):
1. [Platform]: [post text, max 280 chars for Twitter, longer for LinkedIn/IG]
2. [Platform]: [post text]
3. [Platform]: [post text]
4. [Platform]: [post text -- question format for engagement]
5. [Platform]: [post text -- stat or data-led]

Repurpose opportunities:
- [Thread version for Twitter/X]
- [Short-form video script for Instagram Reels / YouTube Shorts]
- [Infographic from key data points]
- [Email sequence if topic supports multi-part series]
```

## Example Usage

Trigger phrases:
- "Create a content brief for [topic]"
- "Write a brief about [keyword]"
- "SEO content plan for [topic]"
- "What should we write about [topic]?"
- "Content brief for our blog"

```
User: Create a content brief for "Shopify CRO for D2C brands"
Assistant: [searches top ranking content, analyzes keywords, finds competitive gaps, generates full brief with outline and distribution plan]
```

```
User: We want to write a comparison post: Shopify vs WooCommerce for Indian D2C brands
Assistant: [researches both platforms in Indian context, finds gaps in existing comparisons, builds brief with agency's Shopify expertise as differentiator]
```
