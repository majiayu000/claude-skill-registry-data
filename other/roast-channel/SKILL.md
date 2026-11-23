---
name: roast-channel
description: "Use when the user wants a YouTube channel roasted or analyzed, their own or anyone's: what works, what holds it back, what only it has, and what to change first. Requires the TubeLab MCP."
license: MIT
metadata:
  author: tubelab
  version: "6.1"
  requires: tubelab-mcp
---

# Roast Channel

## Overview

A blunt read of any channel. Its median views against its last few uploads show whether it is healthy, growing or declining. A format that gets fewer views each time it returns is worn out: keep what makes it work, and change what the title promises. A hit the channel never followed up is its cheapest opportunity.

The best videos usually rest on an asset only this creator has: a job, a life story, insider trust, credentials, a subculture they belong to, or a hard skill. YouTube also groups videos by who watches them together, so every channel has neighbours. The names, brands, tools and known ideas in a title or thumbnail are anchors: they tell YouTube which viewer to send. A hit with the wrong anchor can bring viewers the rest of the channel does not serve.

**Without TubeLab:** no outliers for its audience, similar channels or audience estimate, so the channel is compared only with itself.

## Workflow

1. Clarify scope only if needed. Unless told otherwise, the goal is reach, or conversion if the channel sells something.
2. Compare the last 4 to 6 long-form uploads with the median. Leave out Shorts and uploads still gathering views.
3. View the thumbnail of every video you feature, and say if one fails.
4. Search two or three times for what works now with the same audience. Their channels are its neighbours, plus on-topic hits from one similar-channels search with at least a tenth of its subscribers. Views per subscriber below most of theirs means the channel is the problem, not the niche.
5. Find the asset in the About text, the descriptions and the openings of the two or three best videos. Then find recent videos that skip it, and compare views.
6. Read the anchors in the titles and thumbnails of the best and weakest videos.
7. Flag off-audience hits: top videos whose topic or anchor is unlike its other videos.
8. Put the channel's recent titles and thumbnails next to the neighbours', with no new search. Name any that could belong to a neighbour.

## Output Format

```markdown
# 🔥 Channel Roast: [{channel}]({url})

- **Diagnosis:** {one sentence, with numbers}
- **Positioning:** {who it serves, with its audience estimate if a channel search returned the channel, and what it promises}
- **Against neighbours:** {its views per subscriber} against {the neighbours' median}, from {n} neighbours
- **Assets:** {what only this channel has, and how many recent videos use it}

## ✅ What Works

### 1. {Finding}

[![]({thumbnail})]({video url})

- [{title}]({video url}) · {views, ratio, date}
- **Why:** {one sentence}

## ⚠️ What Holds It Back
1. **{Problem, one flat sentence}**
   - [{title}]({video url}) · {views, ratio, date}
   - **Fix:** {one sentence}

## 🧬 Assets And Packaging

### Assets not used

[![]({thumbnail of a video that skips it})]({video url})

- **The asset:** {what only this creator has, and where it shows}
- **Used in:** [{title}]({video url}) · {views, ratio, date}
- **Skipped in:** [{title}]({video url}) · {views, ratio, date}
- **What it does instead:** {one sentence}

### Anchors

- **{Anchor}:** {which viewer it pulls, and whether the channel serves that viewer}
  - [{title}]({video url}) · {views, ratio, date}

### Off-audience hits

- [{title}]({video url}) · {views, ratio, date}
  - **Unlike the rest:** {how its topic or anchor differs}

### Look-alike packaging

[![]({this channel's thumbnail})]({video url}) [![]({neighbour's thumbnail})]({neighbour video url})

- **This channel:** [{title}]({video url}) · {views, ratio, date}
- **Neighbour:** [{channel}]({url}) · [{title}]({video url}) · {views, ratio, date}
- **What they share:** {one sentence}

## 🧪 Next 3 Tests
1. **{Title to test}**
   - **Based on:** [{channel}]({url}) · [{title}]({video url})
   - **Pass if:** {views by day 30}
```

- Length: about 850 words. Three items per section. Up to three anchors and two off-audience hits.
- Tone: blunt. Each problem is one flat sentence with its proof. No insults and no softening.
- Language: plain words and short, complete sentences. Nothing compressed.
- Bullets: one fact each, under 25 words, except quotes and verbatim titles. No extra sections or bullets.
- If a check finds nothing, say so in one bullet. If it runs long, cut whole items, never proof.
- Links: link every video, channel, moment, brand and offer you cite, built from IDs, handles and links in the data. Never guess one.
- Thumbnails: use the 320px `mqdefault.jpg` image, on its own line under the heading, linked to the video.

## Common Pitfalls

- Do not search without `publishedAtFrom` and `classificationQuality` at `"neutral"` or above, or the results fill with low-effort videos.
- Do not assume the channel is the user's. Write about "the channel" unless the user says it is theirs.
- Do not call fewer views a problem by itself. A healthy channel is a valid result.
- Do not read a ratio of 1.0 as typical. Big hits pull the channel's mean up, so a median video sits below 1.0.
- Do not advise deleting an off-audience hit. The data does not show who watched it, and deleting cannot be undone.
- Do not state a cause as fact. Say what the evidence suggests.
