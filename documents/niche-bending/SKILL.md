---
name: niche-bending
description: Use when the user wants to bend a proven YouTube format into a new market, starting from a channel they name or from channels that already earn. Requires the TubeLab MCP.
license: MIT
metadata:
  author: tubelab
  version: "5.1"
  requires: tubelab-mcp
---

# Niche Bending

## Overview

A niche is a market plus a format. The market is what the audience cares about, such as history or football. The format is a repeatable package: a title pattern, a thumbnail layout and a structure, such as "Every {thing} explained". Niche bending carries a format that blew up in one market into another market or language. The content is new, and the format is proven. Never invent a niche. Not for ten niche ideas from a wide search (`niche-finder`).

**Without TubeLab:** no search for channels that already earn, no revenue estimates, no outlier search to check a bend. Formats come from famous channels, and "open" stays unchecked.

## Workflow

1. Clarify scope only if needed. Start from the channel the user names, or else from channels that already earn. Bend into the user's market or language first, if they name one.
2. With a channel, read it, which is free. Find the one to three formats behind its best videos by ratio: the title pattern with the slots marked, the thumbnail layout and the length. A format needs three or more videos that beat the channel's average.
3. With no channel, run the preset below for one or two pages; page 2 is `from: 20`. Swap in the user's language if named, and change nothing else. Read the channels with the clearest repeatable format, and find their formats as in step 2. Note each one's revenue band and audience estimate from the hit.
4. View the thumbnail of every video you use, and say so if one fails to load.
5. Bend each format into markets where its promise still makes sense and the audience is large. A new market is a different audience or another language, not a neighbouring topic.
6. Check the best three bends with one outlier search each, in the bend's market and language, over the last year. Count the closely matching results, since the search total is capped, and set the status as the ranking legend says. Drop a crowded bend or bend it further. Say which bends went unchecked.
7. Rank four to six bends by the format's strength at its source, the market's size, how early the bend is, and fit with the user's market. A few strong bends beat six forced ones.

Cash cows, which are channels that already earn:

```json
{ "publishedAtFrom": "year", "classificationQuality": "neutral",
  "monetizationAdsense": true, "revenueMonthlyEstimationFrom": 800, "subscribersFrom": 1000,
  "language": ["en", "de", "fr"], "sortBy": "foundAt", "size": 20, "from": 0,
  "excludeNiche": ["music", "song", "lofi", "movies", "breastfeeding", "lingerie", "transparent", "transparency", "clean", "haul", "kids", "news", "politic", "india", "pakistan", "arabic", "manufacturing", "nature", "islamic"] }
```

## Output Format

```markdown
# 🔀 Niche Bending: {[channel](url), or "channels that already earn"}

- **Best bend:** {one sentence, with numbers}
- **Source:** {the channel, or how many channels you sampled and from how many pages}

## 🏆 Ranking
🟢 open: nobody found · 🟡 proven and early: one or two small channels with strong ratios, the best case · 🔴 crowded: several established channels · ⚪ not checked. Potential is a judgment call: High, Medium or Low.

| # | Bend | Format | New market | Status | Potential |
|---|---|---|---|---|---|
| 1 | {name} | "{title pattern}" | {market} | {🟢 open, 🟡 proven and early, 🔴 crowded, or ⚪ not checked} | {High, Medium or Low} |

## 🔀 Bends

### 1. {Bend name}

**Niche:** [{source channel}]({url}) · {market}

[![]({thumbnail})]({video url}) [![]({thumbnail})]({video url}) [![]({thumbnail})]({video url})

⬇️ **Bend:** {new market, and the language if it changes}

{Only when a channel already does it: up to three of its thumbnails, in one row like the one above.}

- **Format:** "{title pattern with slots}" · {thumbnail layout in a few words} · {usual length}
- **Proof at the source:** {n} videos use this format · best: [{title}]({video url}) · {views, ratio, date}
- **Source earns:** {monthly revenue band, as an estimate} · {its audience: age, gender, income tier, region}; only for a source found by search
- **Why this market:** {one sentence}
- **Already there:** {"nobody found", or [channel](url) · [title](video url) · views, ratio, date, or "crowded" with who}
- **First titles:** "{title}" · "{title}" · "{title}"
- **Thumbnail:** {what to keep from the layout, and what to swap}
```

- Length: about 1,000 words. Four to six bends, best first.
- Language: plain words and short, complete sentences. Nothing compressed.
- Bullets: one fact each, under 25 words, except quotes and verbatim titles. No extra sections or bullets.
- If it runs long, cut whole items, never proof.
- Links: link every video, channel, moment, brand and offer you cite, built from IDs, handles and links in the data. Never guess one.
- Thumbnails: the 320px `mqdefault.jpg` image, linked to its video, up to three on one line under their Niche or Bend line.

## Common Pitfalls

- Do not search without `publishedAtFrom` and `classificationQuality` at `"neutral"` or above, or the results fill with low-effort videos.
- Do not build on a hit the source never repeated. One lucky video proves a topic, not a format.
- Do not copy the source's titles, artwork, characters or name. Keep only the structure, or the channel reads as a copy.
- Do not bend into a market where the promise breaks. Ranking the worst deaths fits football legends, not kitchen gadgets.
- Do not call a bend open without saying what you searched. Empty results can mean the wrong search words.
