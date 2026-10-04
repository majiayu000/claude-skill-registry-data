---
name: ai-news-radar
description: Searches and summarizes the latest AI news in English from selected sources. Removes duplicates and categorizes the topics.
user-invocable: true
metadata:
  openclaw:
    emoji: "🤖"
    requires:
      bins: []
      env: []
---

# AI News Radar

## Objective

Searches and summarizes the main recent Artificial Intelligence news from curated sources.

The skill:

- searches recent news
- removes duplicates
- categorizes the topics
- translates/summarizes in English
- returns:
  - title
  - link
  - category
  - short summary

## Usage

Invoke with:

- `/ai-news-radar`
- “latest AI news”
- “AI summary”
- “what happened in AI today”
- “AI briefing”

Optionally, the user can specify the number of items:

- “show me 5 AI news items”
- “top 10 AI news stories”

## Preferred sources

Use these sources:

### Primary sources

- Anthropic News — Company announcements
- Claude Blog — Product updates and guides
- Google AI — Gemini/DeepMind

### Curation sources

- TLDR AI — Daily AI industry digest
- The Decoder — AI-focused site
- Last Week in AI — Weekly roundup

## Instructions

### Determine quantity

If the user specifies a quantity:

- use the requested quantity

Otherwise:

- use 10 news items by default

Maximum:

- 20 news items

## Selection criteria

Prioritize news items that are:

1. Recent, maximum 72 hours old
2. Relevant to generative AI, models, products, research, agents, tools, or the market
3. Published or highlighted in the preferred sources
4. Potentially impactful for professionals, creators, developers, or companies

## Duplicate removal

If the same news item appears in more than one source:

- keep only one entry
- choose the most original or most direct source as the main link
- mention additional sources in the “Also appeared in” field
- do not repeat the news item in the list

## Possible categories

Classify each news item into one of these categories:

- Launch — launch, release, announcement, GPT, Claude, Gemini, model
- Research — paper, benchmark, study, research
- Developer tool
- Product — feature, API, update, tool
- Market — funding, startup, acquisition
- AI safety — safety, alignment, red team
- Opinion — opinion, future, prediction
- Other

## Output format

Return the list in English using the following format:

# Latest AI News
```markdown
## 1. [News title](link)

**Category:** Product launch  
**Main source:** Source name  
**Also appeared in:** Source 2, Source 3  
**Date:** MM/DD/YYYY, if available

Short paragraph explaining what happened, why it matters, and the potential impact. Do not write more than 4 lines.

---

## 2. [News title](link)

**Category:** Research  
**Main source:** Source name  
**Also appeared in:** —  
**Date:** MM/DD/YYYY, if available

Short paragraph explaining what happened, why it matters, and the potential impact.
```
# Error handling

If any feed fails:

- continue normally
- ignore the unavailable feed

Never interrupt the full briefing because of a partial failure.

# Important rules

Always respond in English.  
Never copy the full text of an article.  
Always summarize.  
Always include the original link.  
Do not invent information.  
Do not repeat duplicate news items.  
Prioritize clarity.  
Prioritize original sources whenever possible.