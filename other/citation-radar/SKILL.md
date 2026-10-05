---
name: citation-radar
description: 'Audits how likely AI answer engines (ChatGPT, Claude, Perplexity, Gemini, Google AI Overviews) are to cite your pages for the questions buyers ask, then ranks fixes by citation lift. Use when: ai search visibility, generative engine optimization, geo audit, aeo, llm citations, are we cited in ai answers, ai overviews, answer engine optimization.'
---

# Citation Radar (CLEAR Framework)

Buyers now ask an assistant before they open a search results page. Classic SEO audits measure rank; this skill measures whether a page is the kind of source an answer engine can lift a sentence from and credit. It works from the buyer's questions backward, not from keywords forward.

## Core Principle

**Answer engines cite claims, not pages.** A page earns citations when it contains short, specific, attributable statements that directly answer a question someone actually asks.

## The CLEAR Framework

| Letter | Dimension | What It Checks | Weight |
|---|---|---|---|
| **C** | Claim density | Specific, checkable statements per 100 words (numbers, named entities, dates) | 0.25 |
| **L** | Liftability | Answer sits in the first 40-60 words of the section; lists and tables for comparisons | 0.15 |
| **E** | Evidence | Named author, dated update, primary sources, schema markup | 0.20 |
| **A** | Answer match | Does an H2/H3 or first sentence answer the buyer question verbatim? | 0.25 |
| **R** | Rarity | Information not found on the top competing pages (original data, pricing, benchmarks) | 0.15 |

Score each dimension 0-10. **CLEAR score** = Σ(weight × score) × 10 → 0-100.

- **75+** Citable - protect and refresh quarterly
- **50-74** Fixable - one or two dimensions drag it down
- **<50** Invisible - rewrite around a specific question

## Process

1. **Question set** - collect 20-40 real buyer questions (sales calls, support tickets, community threads); tag each by funnel stage
2. **Map** - match each question to the page that should answer it; unmatched questions are content gaps
3. **Probe** - ask 2-3 assistants each question; record who is cited and which sentence they quote
4. **Score** - apply CLEAR to every mapped page
5. **Prioritize** - rank fixes by `question volume × (75 - current score)`, capped at 0 for pages already citable
6. **Rewrite brief** - for each top fix, name the question, the missing claim, and the proof to add

## Output

Save to `outputs/citation-radar-[domain]-[YYYY-MM-DD].md`

| Artifact | Description |
|---|---|
| **Question map** | Buyer question → target page → current citer |
| **CLEAR scorecard** | Five dimension scores and total per page |
| **Fix queue** | Top 10 rewrites ranked by expected citation lift |
| **Gap list** | Questions with no page, ready for `demand-engine` |

## Tips

1. **Probe, don't assume** - the page an assistant cites today is the real competitor
2. **Dates matter** - an undated page reads as stale to both people and models
3. **Tables win comparisons** - "X vs Y" questions get answered from tables

## Pairs With

- **context-anchor** - supplies Audience and Substantiation for rewrites
- **demand-engine** - turns the gap list into content
- **competitive-battlecard** - shows which competitor claims get cited instead of yours
