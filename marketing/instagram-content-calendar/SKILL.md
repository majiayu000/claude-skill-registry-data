---
name: instagram-content-calendar
description: >-
  Instagram content calendar and weekly content planner: builds the week (or
  month) of Reels, carousels and stories from evidence - the user's own top
  reels, niche outliers and real events - with the format, hook formula, SEO
  keyword, posting slot and engagement list per day. Use when the user says
  "plan my week", "content calendar", "what should I post", "content plan",
  "posting schedule", "I have nothing to post", or wants a month of ideas. Uses
  the IShort MCP (list_my_scripts, search_my_scripts, get_bio_analytics) to
  plan from what already worked for them.
---

# Instagram content calendar

The control room. Other skills execute; this decides what gets executed. Run
it weekly, same day each week.

## Inputs (read what exists, ask for the rest in ONE batched question)

1. `~/.instagram-claude-skills/brand-voice.md`: who they talk to, what they sell.
2. `~/.instagram-claude-skills/swipe.md` (from `instagram-reels-research`):
   what is working in the niche now. Outranks every default below.
3. `~/.instagram-claude-skills/log.md`: what was posted, so themes don't repeat
   within two weeks. Create it if missing.
4. **Their own winners (IShort MCP):** `list_my_scripts` sorted by `views` for
   their handle; the top 3 by multiple are the themes to repeat in new shapes.
   `get_bio_analytics` shows which bio links get clicked: plan the week's
   Offer post around the link that already converts.
5. What actually happened this week: a result, a mistake, a question from a
   client or the comments. Posts come from here, not from "topics".

## The mix (4-5 posts/week, at least 3 Reels)

| type | per week | job | format |
| --- | --- | --- | --- |
| Proof | 1 | something that happened, with a number | Reel |
| Teach | 1-2 | one thing they can do today (the searchable post) | Reel or carousel |
| Opinion | 1 | a position some people disagree with | Reel |
| Story | every 2 weeks | a scene with a cost | Reel |
| Offer | every 2 weeks | what they sell, plainly | carousel or stories |

Never two of the same type back to back. Every Teach post gets an SEO keyword
(it is the post that keeps getting found in Instagram Search and Google).

## Each slot

```
TUE  REEL · Teach · hook #12 "The Number List"
     angle: <the specific angle from this week, not a topic>
     keyword: <primary search phrase>      length: 30-40s
     source: <outlier / their winner / this week's event>
     next: instagram-reel-script-generator
```

"AI" is not an angle. "The 3 prompts that cut our client onboarding from 2
days to 2 hours" is.

## When to post

Early evening local time for consumer audiences, early morning for business.
If the user has data, use it: IShort's analytics (best-time heatmap) or a
competitor report's `bestPostingDay`/`bestPostingHour`. Say plainly: the hour
matters far less than the first two seconds.

## Engagement list

10 accounts (from `instagram-reels-research`) to comment on daily, 20 minutes
a day, with real comments.

## Output

The week as a table, then each slot expanded, then append the plan to
`log.md`. Offer to write Monday's script now.
