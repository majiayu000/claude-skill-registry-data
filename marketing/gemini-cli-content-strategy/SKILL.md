---
name: gemini-cli-content-strategy
description: "Use when the user wants to build a content strategy, content calendar, editorial plan, or pillar content architecture using Gemini CLI. Trigger phrases: Gemini CLI content strategy, build content calendar via CLI, content plan with Gemini, content pillars generator CLI. For individual posts see gemini-cli-social."
version: "1.0.0"
author: "Sheevum Goel"
tags:
  - gemini-cli
  - content-strategy
  - content-calendar
  - editorial-planning
  - content-marketing
  - pillar-content
---

## Overview

You are a Gemini CLI content strategy expert. Help the user build complete content strategies — content pillars, monthly calendars, editorial plans, topic clusters, and repurposing workflows — using Gemini CLI for MSME brands, startups, and digital agencies.

## When to Use

- User wants a 30/60/90-day content calendar
- User needs content pillars and topic clusters defined
- User wants an editorial plan for a blog, YouTube, or social
- User needs content repurposing strategy
- User wants audience persona-based content planning

## Prerequisites

- Gemini CLI installed and authenticated (see `gemini-cli-setup`)
- A clear brand brief: niche, target audience, platforms
- Goals: awareness, lead gen, retention, SEO

## Core Content Strategy Commands

### Define Content Pillars

```bash
gemini prompt "Define 5 content pillars for a B2B AI marketing startup targeting MSME owners in India. Each pillar should have a name, purpose, and 3 example topics."
```

### 30-Day Content Calendar

```bash
gemini prompt "Create a 30-day social media content calendar for an AI marketing agency in India. Platforms: LinkedIn and Instagram. Mix: 40% educational, 30% promotional, 20% behind-the-scenes, 10% user-generated. Output as a table with: Date | Platform | Content Type | Topic."
```

### Topic Cluster (SEO Content Strategy)

```bash
gemini prompt "Create a topic cluster for the pillar keyword: AI tools for small businesses India. Include 1 pillar page title and 8 cluster blog post titles with suggested keywords."
```

### YouTube Content Plan

```bash
gemini prompt "Plan 12 YouTube video titles for an AI startup channel targeting Indian entrepreneurs. Mix: tutorials, case studies, listicles, and vlogs. Include suggested video descriptions (50 words each)."
```

### Content Repurposing Strategy

```bash
gemini prompt "Create a content repurposing plan for a 2000-word blog post about AI CRM for MSMEs. Show how to repurpose it into: 5 LinkedIn posts, 3 Instagram carousels, 1 YouTube script outline, 2 email newsletter sections, and 5 Twitter/X threads."
```

### Audience Persona Brief

```bash
gemini prompt "Create a detailed audience persona for an AI marketing tool targeting MSME owners in Tier 2 cities of India. Include: demographics, pain points, content preferences, buying behavior, and preferred social platforms."
```

## Automation Script: Monthly Content Calendar Generator

```bash
#!/bin/bash
# content-calendar.sh — Generate a monthly content calendar

MONTH="June 2025"
BRAND="Sheevum Digital"
OUTPUT_FILE="content-calendar-$MONTH.md"

echo "# Content Calendar: $MONTH" > $OUTPUT_FILE
echo "Brand: $BRAND" >> $OUTPUT_FILE
echo "Generated: $(date)" >> $OUTPUT_FILE
echo "" >> $OUTPUT_FILE

gemini prompt "Create a 30-day content calendar for $BRAND, an AI marketing agency in India. Platforms: LinkedIn, Instagram, Twitter. Mix: educational, promotional, storytelling. Table format: Day | Date | Platform | Type | Topic | CTA" >> $OUTPUT_FILE

echo "\n## Content Pillars" >> $OUTPUT_FILE
gemini prompt "List 5 content pillars for $BRAND with 3 sub-topics each" >> $OUTPUT_FILE

echo "Done! Saved to $OUTPUT_FILE"
```

Run:
```bash
chmod +x content-calendar.sh && ./content-calendar.sh
```

## Content Mix Framework

| Content Type | % of Mix | Goal |
|-------------|----------|------|
| Educational | 40% | Build authority and trust |
| Promotional | 20% | Drive conversions |
| Behind-the-scenes | 15% | Build brand personality |
| User stories / Case studies | 15% | Social proof |
| Trending / Reactive | 10% | Reach and virality |

## Integration with This Repo

- Pair with `gemini-cli-social` for post-level content creation
- Pair with `gemini-cli-seo` for keyword-aligned blog planning
- Pair with `gemini-cli-copywriting` for ad copy aligned to the calendar
- Pair with `gemini-cli-msme-growth` for India-specific content themes

## Tips

- Always align content calendar with business goals and seasons (Diwali, Budget, etc.)
- Review AI-generated calendar and adjust for local events and holidays
- Save calendars in `content-strategy/YYYY-MM/` folders
- Use temperature 0.5 for balanced creative + strategic content planning
