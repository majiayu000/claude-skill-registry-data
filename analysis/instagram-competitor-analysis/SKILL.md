---
name: instagram-competitor-analysis
description: >-
  Instagram competitor analysis for Reels: breaks down any public account's
  posting pace, median and average views, outlier reels, best day and hour,
  winning duration, audio and hashtags, then compares it against the user's
  own account and turns the gaps into a 2-week action list. Use when the user
  says "analyze this competitor", "spy on @account", "what is @handle doing
  differently", "competitor report", "compare me with", or "why does their
  content get more views". Reads IShort competitor reports via the MCP
  (list_my_competitor_reports, get_competitor_report) or an IShort CSV export.
---

# Instagram competitor analysis

Not "they post more". The specific, copyable differences between an account
that wins in the niche and the user's, with numbers.

## Step 1. Get the data

| Have | Do |
| --- | --- |
| IShort extension | the user opens the competitor's Reels tab with the IShort Chrome extension, lets it load, and exports CSV. Run `../instagram-reels-research/scripts/outliers.py export.csv --json` for the median, multiples and outliers. This is the main path. |
| IShort MCP | `list_my_competitor_reports`, then `get_competitor_report(handle=...)` if a saved report exists (older extension versions saved these). Its `stats.medianViews`, best/worst reels and posting heatmap slot straight into the table below. Add `transcribe_reel` for their top reels. |
| Nothing | the user pastes 15-30 recent reels (views, date, duration, first line). Fewer than 15 = say the read is thin. |

Get the **user's own** account the same way. The comparison is the product.

A report gives: `stats` (totalReels, avgViews, medianViews, avgEngagement,
postingFrequency per week), `insights` (bestPostingDay, bestPostingHour,
optimalDuration, topHashtags, audioBreakdown original vs licensed, bestReels,
worstReels, contentTypeBreakdown, postingHeatmap, takeaways).

## Step 2. The breakdown

```
@competitor vs @user                      them        you
  reels analysed                           48          31
  median views                             42K         3.1K
  posts / week                             4.5         1.8
  outliers (3x+ median)                    7           1
  best duration bucket                     30-60s      under 30s
  original audio share / its avg views     ...
  best day / hour (by avg views)           Tue 19:00   ...
```

Use the median, not the average: one viral reel inflates the average and lies
about the account's normal day.

Then the three to five differences that matter, each with evidence:
- **Format**: what their top 5 reels share that their bottom 5 don't.
- **Hooks**: transcribe their top 3 (`transcribe_reel`, check `get_my_usage`)
  and name the formulas (`../instagram-reel-script-generator/references/hooks.json`).
- **Cadence**: their posting pace vs yours, and whether their views hold at it.
- **Packaging**: duration, audio, cover/on-screen text, caption length.
- **Topics**: what they repeat that works (series beat one-offs).

Timing claims need care: best day/hour from 30 reels is a hint, not a law.
Say "in this sample".

## Step 3. The 2-week action list

Five actions max, each one copyable, each tied to a number above:

```
1. Shoot 2 reels in their #3 format (<what>) - their 3 breakouts use it.
2. Move to 30-60s - their median in that bucket is 2.3x their <30s.
...
```

Hand script work to `instagram-reel-script-extractor` (their top reel) and
`instagram-content-calendar` (the two weeks).

## Rules

- Public data only. No logging in as anyone, no scraping beyond what the user
  loads in their own browser.
- Copy structure, not content.
- Never name a pattern from one reel.
