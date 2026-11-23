---
name: reverse-engineer-channel
description: Use when the user wants to reverse engineer a YouTube channel into what works for it, from formats, title and thumbnail formulas, hook formulas and script structure to how it earns, plus what does not work. Requires the TubeLab MCP.
license: MIT
metadata:
  author: tubelab
  version: "6.4"
  requires: tubelab-mcp
---

# Reverse Engineer Channel

## Overview

One channel taken apart into formulas the user can reuse. A formula is a pattern, not a quote: a title with its slots, a thumbnail as its parts. Reads are free; two searches add the rest. Not for what holds a channel back (`roast-channel`).

**Without TubeLab:** no audience estimates, AdSense status or detected revenue methods, and no similar-channel search to show whether a formula wins beyond this channel.

## Workflow

1. If the user names their own channel or market, aim learnings at it.
2. Read the channel's long-form list and its Shorts. The list holds the latest 120; read a video for its exact date. Look it up by handle in a channel search for audience, AdSense, RPM and revenue methods.
3. Find the outliers: videos with at least twice the list's average views, or the three highest. Split the list into up to ten blocks and compare median views. A turning point is a lasting jump or fall in the median after something changed.
4. View every thumbnail, on numbered contact sheets.
5. Group the videos into formats: ideas that can be remade with a twist, even if used once. Count how many of its videos beat their neighbours, the median of their own block, as older videos had longer to gain views. Rank videos the same way.
6. Run one similar-channel outlier search seeded with the channel: last year, ratio 2 or more, 50 hits. Per format, count channels whose outlier runs it, not recaps it: two or more means it travels.
7. Find what does not work: the formats, topics and habits of the weakest videos. Skip last month's uploads and channel updates.
8. Read the first 30 seconds of the five best videos and two weak ones. Name each opening's beats in general words, such as setup, stakes or twist. A hook formula is a beat order two strong openings share.
9. Read full transcripts of three best videos, one per format. Mark each beat and its time, and keep the layout they share.
10. Find how it earns, from the detected revenue methods, its description, the descriptions of its ten best and five newest videos, and sponsor reads.
11. Write five learnings, best first. Each names the skill that runs it, such as `title-formulas` or `script-breakdown`, and a prompt to paste. Tag every format, hook, script and learning "anyone can copy" or "needs their asset" (job, life, credentials, fame, budget, access or hard skill).

## Output Format

```markdown
# 🔬 Reverse Engineering: [{channel}]({url})

- **Why it works:** {one sentence, with numbers}
- **Sample:** the latest {n} long videos, from {month year} to {month year} · {n} thumbnails viewed · {n} openings and {n} full scripts read
- **Shorts:** {how they do next to the long videos, or "none posted"}
- **Start with:** {the one learning to act on this week}

## 📈 Outliers

{n} of {n} videos have at least twice the channel's average views.

[![]({thumbnail})]({video url}) [![]({thumbnail})]({video url}) [![]({thumbnail})]({video url})

1. [{title}]({video url}) · {views, ratio} · {its format}

- **Turning point, {month year} · {what changed}:** median views went from {views} to {views} · [{title}]({video url})

## 🧩 Formats That Work

A video beats its neighbours when it has more views than the median of the videos published around it.

### 1. {Format name} · {n} of {n} beat their neighbours

[![]({thumbnail})]({video url}) [![]({thumbnail})]({video url}) [![]({thumbnail})]({video url})

- **Topics:** {the topics it covers, best first}
- **Title formula:** "{the pattern with every slot in square brackets, such as "[Number] Days In [Place]"}" · [{title}]({video url}) · {views, ratio}
- **Thumbnail formula:** {the parts a viewer can point at, each a few words in square brackets, such as "[face, shocked, centre] + [object, oversized, left] + [price in white, top right]"}
- **Length:** {usual length}
- **Wins elsewhere:** {n} similar channels · [{title}]({video url}) · [{channel}]({url}) · {ratio}, or "only here"
- **Who can copy it:** {"anyone can copy" or "needs their [asset]"} · {why, in a few words}

## 🚫 What Doesn't Work

### 1. {Format, topic or habit} · {n} of {n} beat their neighbours

[![]({thumbnail})]({video url})

- **What it is:** "{title pattern, slots in square brackets}" · {thumbnail in a few words}
- **Proof:** [{title}]({video url}) · {views, ratio, date}
- **How it differs:** {what the formats that work have and this lacks}

## 🎣 Hook Formulas

### 1. {Formula name} · {n} of {n} strong openings

- **Structure:** {beat} → {beat} → {beat}
- **Runs:** the first {n} seconds
- **Weak videos:** {whether the weak openings read use it too}
- **Who can copy it:** {"anyone can copy" or "needs their [asset]"} · {why, in a few words}

<details>
<summary>Example: {title}</summary>

[{title}]({video url}) · {views, ratio}

- **{Beat}:** "{its words}"

</details>

## 🎬 Script Structure

- **Layout:** Hook 0:00 → {beat} {when} → ... → {ending} {when}
- **What repeats:** {the device every script reuses, and how often}
- **How it ends:** {one sentence}
- **Who can copy it:** {"anyone can copy" or "needs their [asset]"} · {why, in a few words}

<details>
<summary>Example: {title}</summary>

[{title}]({video url}) · {views, ratio, length}

| Time | Beat | What happens |
|---|---|---|
| [{m:ss}]({link to that moment}) | {type} | {a few words} |

</details>

## 💰 How It Earns

| Method | Offer | Where it shows |
|---|---|---|
| {product, merch, newsletter, course, membership, community, app, sponsor or affiliate: check each} | [{offer or brand}]({url}) | [{title}]({video or moment url}) · {in the description, or said in the video} |

- **Audience and ads (estimates):** {age, gender, income tier, region} · AdSense {on or off} · RPM {band}
- **Not found:** {the methods looked for and not seen}

## 🧠 Learnings

1. **{What to copy}**
   - **Proof:** [{title}]({video url}) · {views, ratio, date}
   - **Who can copy it:** {"anyone can copy" or "needs their [asset]"} · {why, in a few words}
   - **Run next:** `{skill}` · "{a prompt the user can paste, with [square brackets] for what they fill in}"

- ❌ **Needs their asset: {move}** · {the asset it needs and why it will not carry over, with proof}
```

- Length: about 1,700 words. Up to six outliers, three turning points, four good formats, three bad ones, three hook formulas, one script example and ten ways it earns.
- Language: plain words and short, complete sentences. Nothing compressed.
- Bullets: one fact each, under 25 words, except quotes, verbatim titles, formulas and prompts. No extra sections or bullets.
- If it runs long, cut whole items, never proof.
- Links: link every video, channel, moment, brand and offer you cite, built from IDs, handles and links in the data. Never guess one.
- Thumbnails: the 320px `mqdefault.jpg` image, linked to its video, on its own line.
- Quotes: only in the examples, word for word, with misspelt names fixed. Never paste a full transcript.

## Common Pitfalls

- One hit can be a format, but not a turning point.
- Do not study only the hits. A trait the worst videos share is not why the best ones won.
- Do not state a cause as fact. The data shows what changed, not why viewers came.
