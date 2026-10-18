---
name: x-audit
description: >-
  Post-mortem on what the user has already published on X - which posts
  actually worked, why, and what to stop doing - from their own analytics
  export. Use when the user shares their X analytics CSV or past posts and
  asks "what's working", "why did this flop", "read my analytics", "audit my
  account", "what should I double down on", or wants to know whether links,
  threads or a posting time actually matter for them.
---

# x-audit

The only honest source of what works for an account is that account. Every
rule in every X guide, including the ones in this pack, is a prior. The
user's own last 30 posts are the evidence.

One tool lives in this folder and it runs:

```bash
python3 audit.py account_analytics_content.csv
```

## Input

In order of preference:

1. **The analytics export.** On desktop: x.com/i/account_analytics, then
   Export. It is a Premium feature. One row per post: impressions plus the
   engagement counts (likes, replies, reposts, bookmarks, shares, new
   follows, profile visits). X does not document the column names and they
   have changed before, so `audit.py` matches them loosely; the older
   analytics.twitter.com export parses too.
2. **A sheet by hand** with post text, impressions, and whatever counts the
   user can see. Twenty rows is enough for a first pass.
3. **Screenshots** of the posts with their numbers. Transcribe into a CSV.

Also read `~/.claude/x/log.md` if it exists: it records which hook formula
each post used.

## What it measures, and why not impressions

Impressions are mostly a function of how many people already follow the user.
`audit.py` ranks on things that are not:

| metric | what it tells you |
| --- | --- |
| **Engagement rate** | whether the post earned the reach it got |
| **Replies per 1k impressions** | whether it started a conversation. X's ranker weighs replies far above likes |
| **Shares per 1k** (reposts + shares) | whether it travelled. Shares by DM or copied link are among the highest-weighted actions X publishes |
| **Bookmarks per 1k** | whether someone plans to use it |
| **Follows per 1k** | whether it made anyone want more of the user |

Posts under a noise floor of impressions are left out of the ranking, and the
user's replies on other people's posts (rows starting with @) are counted and
set aside so a good week of replying does not drown the posts.

## Then find the pattern

`audit.py` groups the posts by hook formula (classified with
`../x-post/hooks.json`), by length, and by format (text only vs with a link
or media), and reports every group whose engagement rate is 1.4x above or
below everything else, with its n and a confidence word. It checks day of
week **last**, and only mentions it when nothing else separates. It is almost
never the cause, and it is where people want it to be.

Add what the script cannot see, reading the top 5 and bottom 5 side by side:

- Topic. Which of the user's themes are in the top five?
- Whether the user replied in the first hour.
- Whether the post was the user looking good or the user looking bad.

**The link question, answered with their own data.** X says it stopped
down-ranking link posts over a year ago. An independent analysis in January
2026 still measured fewer views on them. If the format finding shows link
posts well below the rest with n of 5 or more, that is the answer for this
account, whatever anyone says. If it shows nothing, links are fine here.

State every finding as a claim with the evidence attached, and say how
confident it is. With 30 posts a pattern can show. With 8, say that instead
of inventing one.

## Output

```
AUDIT  ·  38 posts  ·  Jul 01 - Aug 28  ·  15 replies set aside

TOP BY ENGAGEMENT RATE
    5.8%    8.6 rep/1k    8.6 shr/1k     5,705 imp  "$4,000 is what one bad hire cost me."
    ...

WHAT THE DATA SAYS
  1. format = text only: 2.7% vs 0.8% for everything else (3.3x, above). n=26, solid.
  2. hook formula = Cost Confession: 3.9% vs 1.9% (2.0x, above). n=4, weak.
  Day of week shows nothing. Stop optimising it.

STOP:     link-first posts. Put the link in a reply for the next ten and re-run.
DO MORE:  the posts where you paid a cost, with the number in line 1.
```

Then hand the conclusions to `/x-plan`, so next week is built on the user's
own evidence instead of on defaults.
