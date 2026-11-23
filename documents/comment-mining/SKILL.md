---
name: comment-mining
description: Use when the user wants to know what a YouTube audience asks, wants or complains about in the comments, in their own words. Requires the TubeLab MCP.
license: MIT
metadata:
  author: tubelab
  version: "5.2"
  requires: tubelab-mcp
---

# Comment Mining

## Overview

What the audience asks, objects to and wants next, in their own words. Likes are votes: a question with 900 likes is 900 people asking. Quotes stay word for word, and your reading of them goes on its own line.

**Without TubeLab:** comments can still be read, but the videos are picked blind. No outlier ratio and no similar-channel search, so you miss what viewers ask on competitors' breakout videos.

## Workflow

1. Clarify scope only if needed. Default to 10 to 15 videos, picked by ratio and never by raw views. Videos the user names are used as given. For a channel, take its five latest, its five best by ratio from the last three months of the free read, and five outliers of similar channels, from one search seeded with the channel. Skip outliers with fewer than 50 comments, and prefer the channel's own format and language. For a topic, take its top outliers from one search, at most two per channel.
2. Fetch comments one video at a time, because parallel fetches overwrite each other. Remove spam, repeated rows and the creator's own replies.
3. Group the rest into questions, objections and requests, weighted by likes. For a channel, mark each theme as raised on its own videos, on similar channels, or both. A theme raised only on similar channels is an ask the channel has not answered.

## Output Format

```markdown
# 🗣️ Voice of Audience: {channel, topic or videos}

- **Biggest ask:** {one sentence, with likes and number of videos}
- **Sample:** {n} videos, {n} comments · {how the videos were picked, with their ratios}

## 🧵 Themes
1. **{Theme}**
   - {n} videos · {total likes} likes · {raised on this channel, on similar channels, or both}
   - "{best quote}" · [{video}]({video url})
   - **What it means:** {one sentence}

| Comment (verbatim) | Type | Likes | Video (link) |
|---|---|---:|---|

## 💬 Their Words
- "{phrase}" · {n} times

## 💡 Video Ideas
1. **{Title}** · {the theme it answers}
```

- Length: about 700 words. Five themes, eight comments, three ideas.
- Language: plain words and short, complete sentences. Nothing compressed.
- Bullets: one fact each, under 25 words, except quotes and verbatim titles. No extra sections or bullets.
- If it runs long, cut whole items. Never cut quotes, and never squeeze sentences.
- Links: link every video, channel, moment, brand and offer you cite, built from IDs, handles and links in the data. Never guess one.

## Common Pitfalls

- Do not search without `publishedAtFrom` and `classificationQuality` at `"neutral"` or above, or the results fill with low-effort videos.
- Do not present a paraphrase as a quote.
- Do not call something a theme unless it appears under 3 or more videos. Under one video, it is a reaction to that video.
- Do not rank spam. Book promos and bots often collect many likes.
- Do not read a quiet comment section as a happy one. Top comments skew positive.
- Do not treat disabled comments as a finding. Say "no data".
