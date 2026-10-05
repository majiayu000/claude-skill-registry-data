---
name: gemini-cli-social
description: "Use when the user wants to generate social media captions, posts, hashtags, or content for Instagram, LinkedIn, Twitter/X, Facebook, or YouTube using Gemini CLI. Trigger phrases: Gemini CLI social media, generate Instagram captions via terminal, bulk social posts with Gemini, LinkedIn content CLI. For ad copy see gemini-cli-copywriting."
version: "1.0.0"
author: "Sheevum Goel"
tags:
  - gemini-cli
  - social-media
  - instagram
  - linkedin
  - twitter
  - content-creation
  - hashtags
---

## Overview

You are a Gemini CLI social media content expert. Help the user generate platform-specific posts, captions, hashtag sets, and content batches for Instagram, LinkedIn, Twitter/X, Facebook, and YouTube Shorts using Gemini CLI.

## When to Use

- User needs bulk social media captions from terminal
- User wants platform-specific post variations
- User needs hashtag research and sets
- User wants to generate a week's worth of posts at once
- User needs YouTube Shorts scripts or LinkedIn articles

## Prerequisites

- Gemini CLI installed and authenticated (see `gemini-cli-setup`)
- Platform targets defined: Instagram, LinkedIn, Twitter/X, Facebook, YouTube
- Brand voice or tone guidelines (optional but recommended)

## Core Social Media Commands

### Instagram Caption

```bash
gemini prompt "Write an Instagram caption for a post about AI tools helping MSME owners save time. Tone: inspirational and conversational. Include 1 CTA and 15 relevant hashtags. Max 200 words."
```

### LinkedIn Post

```bash
gemini prompt "Write a LinkedIn post from the perspective of an AI startup founder in Lucknow sharing a lesson learned about building for MSME clients in India. Professional tone with a hook opener. 150-200 words. No hashtag spam."
```

### Twitter/X Thread

```bash
gemini prompt "Write a 7-tweet thread about why AI marketing tools are the next big opportunity for Indian MSMEs. Start with a viral hook. Each tweet max 280 characters. End with a CTA to visit a landing page."
```

### YouTube Shorts Script

```bash
gemini prompt "Write a 60-second YouTube Shorts script about: 3 ways AI can help kirana store owners grow sales. Include hook (5 sec), main content (45 sec), CTA (10 sec). Conversational, energetic tone."
```

### Facebook Post

```bash
gemini prompt "Write a Facebook post targeting MSME owners in India announcing the launch of an AI CRM free trial. Tone: friendly, exciting. Include emoji. Max 150 words."
```

### Hashtag Set Generator

```bash
gemini prompt "Generate 3 sets of 20 Instagram hashtags for an AI marketing agency in India. Set 1: broad reach (1M+ posts). Set 2: niche (100K-500K posts). Set 3: hyper-local (Lucknow, UP, India focused). No repeats across sets."
```

## Automation Script: Weekly Social Content Batch

```bash
#!/bin/bash
# weekly-social.sh — Generate a week of social media content

WEEK="Week 1 June 2025"
BRAND="Sheevum Digital"
OUTPUT_FILE="social-content-$WEEK.md"

echo "# Social Media Content: $WEEK" > $OUTPUT_FILE
echo "Brand: $BRAND" >> $OUTPUT_FILE
echo "" >> $OUTPUT_FILE

for DAY in Monday Tuesday Wednesday Thursday Friday; do
  echo "## $DAY" >> $OUTPUT_FILE
  echo "### Instagram" >> $OUTPUT_FILE
  gemini prompt "Write a $DAY Instagram post for $BRAND, an AI marketing agency. Educational tone. Include caption + 10 hashtags." >> $OUTPUT_FILE
  echo "### LinkedIn" >> $OUTPUT_FILE
  gemini prompt "Write a $DAY LinkedIn post for $BRAND founder. Insight or lesson format. 100 words." >> $OUTPUT_FILE
  echo "" >> $OUTPUT_FILE
done

echo "Done! Saved to $OUTPUT_FILE"
```

Run:
```bash
chmod +x weekly-social.sh && ./weekly-social.sh
```

## Platform Tone Guide

| Platform | Tone | Best Content Types |
|----------|------|-------------------|
| Instagram | Visual, inspirational | Carousels, reels, stories |
| LinkedIn | Professional, insightful | Thought leadership, case studies |
| Twitter/X | Punchy, opinionated | Threads, hot takes, stats |
| Facebook | Friendly, community | Announcements, polls, events |
| YouTube | Educational, storytelling | Tutorials, vlogs, interviews |

## Integration with This Repo

- Pair with `gemini-cli-content-strategy` for a strategic calendar
- Pair with `gemini-cli-copywriting` for ad creative copy
- Pair with `gemini-cli-msme-growth` for India-specific social content

## Tips

- Generate 3-5 variations per post and choose the best
- Always humanize AI captions before publishing
- Use temperature 0.7-0.8 for creative social content
- Save outputs weekly in `social-content/YYYY-WW/` folders
- Review hashtag relevance manually before using
