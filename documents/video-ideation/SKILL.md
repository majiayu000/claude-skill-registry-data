---
name: video-ideation
description: Use when the user wants video ideas for a YouTube channel, what to make next, or topics for the coming month. Requires the TubeLab MCP.
license: MIT
metadata:
  author: tubelab
  version: "5.2"
  requires: tubelab-mcp
---

# Video Ideation

## Overview

About ten ideas for one channel, drawn from three sources and ranked: the channel's own winning formats, outliers in its niche, and related niches. A fourth source, channels with the same audience, runs only on request. Every idea needs proof that the audience wants it (potential) and proof that this channel can deliver it (fit). An idea with demand but no fit belongs on someone else's channel. Adapt each winner with a twist; never copy it.

**Without TubeLab:** no outlier ratio, no outliers from similar channels, no filter for channels your size and no audience estimates. Ideas copy big channels' hits, with no proof of demand.

## Workflow

1. Clarify scope only if needed. Unless told otherwise, the goal is reach, or conversion if the channel sells something. Findings from `reverse-engineer-niche` or `reverse-engineer-channel` replace sources one and two: twist their patterns, blends and gaps, use their formulas, and skip searches they cover.
2. Source one, the channel's own formats. Read the channel and find the formats that win for it by ratio. Double down on each with a new twist. A new channel has no formats of its own: say so, and lean on the other sources.
3. Source two, outliers in its niche. Search them, once limited to channels no bigger than this one, and twist the best for this channel.
4. Source three, related niches. Find them with one search for the outliers of channels similar to this one, not by guessing neighbours. Twist the formats winning there.
5. Only if the user asks for ideas from channels with the same audience: run one channel search with gender, age band, income tier and region plus a subscriber floor, with no retry. Assume the profile from who the channel addresses, unless a channel-search hit gives it, and say so in the Source bullet. If fewer than two usable channels come back, say so.
6. Keep at most 2 winners per other channel; the channel's own formats have no limit. Fetch and view the thumbnail of every source video, and say so if one fails to load. Expect three to four searches.
7. For the twists you may use SCAMPER: substitute, combine, adapt, modify, put to another use, eliminate, or reverse. It is a tool, not a form.
8. Rank each idea on potential and fit.

## Output Format

```markdown
# 💡 Video Ideas: [{channel}]({url})

- **Best idea:** {title, and why in one sentence}

## 🏆 Ranking
Potential and fit are judgment calls: High, Medium or Low.

| # | Idea | Source | Potential | Fit |
|---|---|---|---|---|

## 💡 Ideas

### 1. {Title}

[![]({source video thumbnail})]({video url})

- **Source:** {own format, niche outlier, related niche, a reverse-engineer finding (pattern, blend or gap), or same audience (on request, noting an assumed profile)}
- **Proof:** [{channel}]({url}) · [{title}]({video url}) · {views, ratio, date}
- **Twist:** {the SCAMPER move and what it changes, in one sentence}
- **Why it fits:** {one sentence}
```

- Length: about 1,100 words. About ten ideas, with every source used represented, best first.
- Language: plain words and short, complete sentences. Nothing compressed.
- Bullets: one fact each, under 25 words, except quotes and verbatim titles. No extra sections or bullets.
- If it runs long, cut whole items, never proof.
- Links: link every video, channel, moment, brand and offer you cite, built from IDs, handles and links in the data. Never guess one.
- Own formats: the proof is the channel's own video, and its linked title is enough.
- Thumbnails: use the 320px `mqdefault.jpg` image, on its own line under the heading, linked to the video.

## Common Pitfalls

- Do not search without `publishedAtFrom` and `classificationQuality` at `"neutral"` or above, or the results fill with low-effort videos.
- Do not take proof from another audience or language, from sister channels, or from paid placements (huge views, almost no likes). Outlier hits carry no audience data, so judge it from the title and thumbnail; the language tag can call a Hindi or Urdu video English.
- Do not trust ratios from channels with a few hundred subscribers.
- Do not mix in Shorts, and do not pitch a video the channel already made.
- Do not write titles over 60 characters.
