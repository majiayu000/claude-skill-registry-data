---
name: deep-research
description: "Systematic multi-angle web research methodology."
allowed-tools:
  - web_search
  - browse_page
  - write_file
enabled: true
related-skills: [github-deep-research, consulting-analysis]
license: MIT
author: Adapted from deer-flow (Bytedance, MIT)
---

# Deep Research

## Overview

Systematic methodology for thorough web research. **Load this skill BEFORE
starting any content generation task** to ensure information from multiple
angles, depths, and sources.

## When to Use

**Always load when:**
- User asks "what is X", "explain X", "research X", "investigate X"
- User wants to understand a concept, technology, or topic in depth
- A single web search would be insufficient to answer properly
- Before creating presentations, reports, articles, or any content requiring
  real-world information

## Core Principle

**Never generate content based solely on general knowledge.** A single search
query is NEVER enough.

## Research Methodology

### Phase 1: Broad Exploration

Start with broad searches to understand the landscape:

1. **Initial Survey**: Search for the main topic to understand overall context
2. **Identify Dimensions**: From initial results, identify key subtopics,
   themes, angles needing deeper exploration
3. **Map the Territory**: Note different perspectives, stakeholders, viewpoints

### Phase 2: Deep Dive

For each important dimension identified, conduct targeted research:

1. **Specific Queries**: Search with precise keywords for each subtopic
2. **Multiple Phrasings**: Try different keyword combinations
3. **Fetch Full Content**: Use `browse_page` to read important sources in full,
   not just snippets
4. **Follow References**: When sources mention other resources, search for those

### Phase 3: Diversity & Validation

Ensure comprehensive coverage by seeking diverse information types:

| Information Type | Purpose | Example Searches |
|-----------------|---------|------------------|
| **Facts & Data** | Concrete evidence | "statistics", "data", "market size" |
| **Examples & Cases** | Real-world applications | "case study", "example", "implementation" |
| **Expert Opinions** | Authority perspectives | "expert analysis", "interview", "commentary" |
| **Trends & Predictions** | Future direction | "trends 2026", "forecast", "future of" |
| **Comparisons** | Context and alternatives | "vs", "comparison", "alternatives" |
| **Challenges & Criticisms** | Balanced view | "challenges", "limitations", "criticism" |

### Phase 4: Synthesis Check

Before proceeding to content generation, verify:

- [ ] Searched from at least 3-5 different angles?
- [ ] Fetched and read the most important sources in full?
- [ ] Have concrete data, examples, and expert perspectives?
- [ ] Explored both positive aspects and challenges/limitations?
- [ ] Information is current and from authoritative sources?

**If any answer is NO, continue researching before generating content.**

## Search Strategy Tips

### Effective Query Patterns

```
# Be specific with context
"enterprise AI adoption trends 2026"

# Include authoritative source hints
"[topic] research paper"
"[topic] McKinsey report"

# Search for specific content types
"[topic] case study"
"[topic] statistics"

# Use temporal qualifiers — use the ACTUAL current year
"[topic] 2026"
"[topic] latest"
```

### Temporal Awareness

Always check the current date before forming search queries:

| User intent | Temporal precision | Example query |
|---|---|---|
| "today / just released" | Month + Day | `"tech news February 28 2026"` |
| "this week" | Week range | `"technology releases week of Feb 24 2026"` |
| "recently / latest" | Month | `"AI breakthroughs February 2026"` |
| "this year / trends" | Year | `"software trends 2026"` |

### When to Use browse_page

Use `browse_page` to read full content when:
- A search result looks highly relevant and authoritative
- You need detailed information beyond the snippet
- The source contains data, case studies, or expert analysis

### Iterative Refinement

Research is iterative:
1. Review what you've learned
2. Identify gaps in your understanding
3. Formulate new, more targeted queries
4. Repeat until comprehensive coverage

## Quality Bar

Research is sufficient when you can confidently answer:
- What are the key facts and data points?
- What are 2-3 concrete real-world examples?
- What do experts say about this topic?
- What are the current trends and future directions?
- What are the challenges or limitations?
- What makes this topic relevant or important now?

## Common Mistakes

- ❌ Stopping after 1-2 searches
- ❌ Relying on search snippets without reading full sources
- ❌ Searching only one aspect of a multi-faceted topic
- ❌ Ignoring contradicting viewpoints or challenges
- ❌ Using outdated information when current data exists
- ❌ Starting content generation before research is complete

## Output

After completing research, you should have:
1. Comprehensive understanding from multiple angles
2. Specific facts, data points, and statistics
3. Real-world examples and case studies
4. Expert perspectives and authoritative sources
5. Current trends and relevant context

**Only then proceed to content generation.**
