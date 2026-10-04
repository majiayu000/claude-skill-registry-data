---
name: cc-title-hooks
version: 1.0.0
description: Generate high-CTR titles and opening hooks for a piece of content and score them against clarity and curiosity.
author: matrixx0070
tags: [content, titles, hooks, copywriting, ctr]
capabilities: []
---

## When to use

Use this when you have a topic and need a batch of title/hook options plus a scored recommendation — for a video, newsletter, or post. Works best after the content angle is decided.

**Not for:** thumbnail design (use cc-thumbnail-brief), writing the body, or SEO keyword research beyond the primary term.

## Method

1. Extract the core payoff and the target viewer. Every title must promise something specific to that person.
2. Draft across proven angles: number/list, how-to, curiosity gap, contrarian, outcome/result, and question. Produce at least 8 so you can compare.
3. Front-load the value word in the first 3-4 words — feeds and inboxes truncate.
4. Score each on three axes, 1-5: Clarity (is the payoff obvious?), Curiosity (does it open a gap?), Credibility (is it believable, not clickbait?). Decision point: if Clarity and Curiosity conflict, keep Clarity — confusion loses more clicks than a smaller gap.
5. Kill any title that over-promises what the content delivers; broken promises tank retention and trust.
6. Recommend the top 1-2 and note which is best for A/B against the runner-up.

## Example

Topic: budgeting app comparison. Options + scores (Clarity/Curiosity/Credibility):
- "I tested 7 budgeting apps so you don't have to" — 5/4/5 = 14
- "The budgeting app nobody recommends (but should)" — 3/5/4 = 12
- "How to pick a budgeting app in 5 minutes" — 5/3/5 = 13
- "This free app beat my $99/yr one" — 4/5/4 = 13
Recommendation: run option 1 vs option 4 (highest curiosity with intact credibility).

## Pitfalls

- Clickbait that the content cannot pay off — the click is worthless if retention dies.
- Burying the value word after "In this video I'm going to..." where truncation hides it.
- Generating one favorite and no alternatives, so there is nothing to A/B test.
- Scoring on gut feel with no axes, which hides why one title beats another.

## Output format

```
TOPIC: <...>  |  TARGET VIEWER: <...>  |  CORE PAYOFF: <...>

| # | Title | Clarity | Curiosity | Credibility | Total |
|---|-------|---------|-----------|-------------|-------|
| 1 | ...   | x/5     | x/5       | x/5         | xx    |
(8+ rows)

RECOMMENDATION: <#> — <why>
A/B: run <#> vs <#>
MATCHING HOOK (first spoken/written line): <...>
```
