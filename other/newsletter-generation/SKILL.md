---
name: newsletter-generation
description: "Research and write professional newsletters."
allowed-tools:
  - web_search
  - browse_page
  - write_file
  - present_files
enabled: true
related-skills: [deep-research]
license: MIT
author: Adapted from deer-flow (Bytedance, MIT)
---

# Newsletter Generation

## Overview

Generates professional, well-researched newsletters combining curated content
from multiple sources with original analysis and commentary. Follows modern
newsletter best practices (Morning Brew, The Hustle, TLDR, Benedict Evans).

Output is a complete, ready-to-publish newsletter in Markdown.

## When to Use

- User asks to generate a newsletter, email digest, or content roundup
- User requests a curated summary of news or developments on a topic
- User wants to create a recurring newsletter format
- User asks to compile recent developments into a briefing
- User asks for a "weekly roundup", "monthly digest", or "morning briefing"

## Newsletter Workflow

### Phase 1: Planning

Identify:
- **Topic(s)**: main subject(s) of the newsletter
- **Format**: daily digest, weekly roundup, deep-dive, industry briefing
- **Audience**: technical, executive, general
- **Tone**: informative, casual, analytical
- **Length**: target word count or item count

### Phase 2: Research & Curation

Use `web_search` + `browse_page` to gather content:

1. **Search broadly** for recent developments on the topic
2. **Fetch full articles** with `browse_page` on promising results
3. **Curate 5-10 items** worth featuring — prioritize:
   - Breaking news / announcements
   - Original analysis / thought leadership
   - Data releases / reports
   - Interesting perspectives
4. **Extract key facts** from each source: headline, key point, why it matters
5. **Verify** claims with a second source where possible

### Phase 3: Writing

Structure the newsletter:

```markdown
# [Newsletter Name] — [Date]

## This Week's Headline
[1-2 sentence hook for the top story]

---

## Top Stories

### 1. [Headline]
[2-3 sentence summary of the story]
**Why it matters**: [1 sentence on significance]
[Source](URL)

### 2. [Headline]
[...]

### 3. [Headline]
[...]

---

## Quick Hits
- [Brief item with link](URL)
- [Brief item with link](URL)
- [Brief item with link](URL)

---

## Deep Dive: [Topic]
[Longer analysis section on one key topic — 200-400 words.
Original commentary, not just summary. Add your perspective on
what this means for the audience.]

---

## Quote of the Week
> "[Notable quote]" — [Attribution](URL)

---

## Coming Up Next Week
[1-2 sentence preview of expected developments]

---

*Curated by [Agent Name]. [Subscribe](link) | [Archive](link)*
```

### Writing Principles

- **Lead with value**: each item should answer "why does this matter to me?"
- **Scannable**: headlines + bold key points + short paragraphs
- **Original commentary**: don't just summarize — add perspective
- **Attribution**: link to every source
- **Consistent voice**: match the chosen tone throughout
- **Forward-looking**: end with what to watch for

### Phase 4: Review & Format

- Check all links work
- Verify facts against sources
- Ensure consistent formatting (headlines, bullets, spacing)
- Preview in Markdown renderer if possible

### Phase 5: Save & Present

Save to `.poirot/outputs/newsletter-{topic}-{YYYYMMDD}.md` via `write_file`.
Present via `present_files`.

## Newsletter Formats

| Format | Items | Length | Cadence |
|--------|-------|--------|---------|
| **Daily Digest** | 3-5 | 300-500 words | Daily |
| **Weekly Roundup** | 5-10 | 800-1500 words | Weekly |
| **Deep-Dive** | 1-3 | 1500-3000 words | Irregular |
| **Industry Briefing** | 5-8 | 600-1200 words | Weekly/Biweekly |

## Pitfalls

- **Too many items**: 5-10 is the sweet spot. More dilutes value.
- **No original commentary**: a link dump isn't a newsletter. Add perspective.
- **Stale news**: verify items are recent (within the newsletter's cadence
  window).
- **No "why it matters"**: readers skim. Each item needs a significance hook.
- **Inconsistent tone**: match the audience. Executive briefing ≠ casual blog.
- **Missing attribution**: every claim links to its source.
