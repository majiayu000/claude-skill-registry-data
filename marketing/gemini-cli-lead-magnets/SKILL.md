---
name: gemini-cli-lead-magnets
description: "Use when the user wants to create lead magnets — ebooks, checklists, guides, templates, or free tools — using Gemini CLI. Trigger phrases: create lead magnet with Gemini CLI, generate ebook outline via CLI, checklist generator Gemini, free resource creation CLI. For email delivery see gemini-cli-cold-email."
version: "1.0.0"
author: "Sheevum Goel"
tags:
  - gemini-cli
  - lead-magnets
  - ebooks
  - checklists
  - content-upgrades
  - list-building
  - lead-generation
---

## Overview

You are a Gemini CLI lead magnet creation expert. Help the user create high-value lead magnets — ebooks, checklists, how-to guides, templates, and resource lists — using Gemini CLI to grow email lists, attract MSME clients, and build brand authority.

## When to Use

- User wants to create an ebook or guide outline
- User needs a checklist for their audience
- User wants a free template or swipe file
- User needs a lead magnet for a landing page
- User wants to create a mini-course outline

## Prerequisites

- Gemini CLI installed and authenticated (see `gemini-cli-setup`)
- Target audience and topic defined
- Format decided: ebook, checklist, template, guide

## Core Lead Magnet Commands

### Ebook Outline

```bash
gemini prompt "Create a detailed 10-chapter ebook outline titled: The Complete Guide to AI Marketing for Indian MSMEs. Include chapter titles, subheadings (3 per chapter), and a 30-word description per chapter. Target audience: MSME owners in Tier 2/3 Indian cities."
```

### Checklist

```bash
gemini prompt "Create a 25-point checklist: Digital Marketing Audit for MSME Businesses in India. Group into 5 categories: Website, SEO, Social Media, Email Marketing, Paid Ads. Format as a printable checklist with checkboxes."
```

### How-To Guide

```bash
gemini prompt "Write a step-by-step guide: How to Get Your First 100 Customers Using AI Marketing Tools. 8 steps. Each step: title, 100-word explanation, and 1 actionable tip. Target: Indian startup founders."
```

### Swipe File / Template

```bash
gemini prompt "Create a swipe file of 10 proven social media post templates for MSME businesses. Each template: platform (Instagram/LinkedIn), post type, fill-in-the-blank format, and example. Format as a ready-to-use document."
```

### Mini-Course Outline

```bash
gemini prompt "Create a 5-day email mini-course outline titled: AI Marketing Basics for Small Business Owners. Each day: subject line, key lesson, 1 exercise, and 1 resource recommendation."
```

### Resource List / Toolkit

```bash
gemini prompt "Create a curated resource list: The Ultimate AI Toolkit for MSME Marketing in India. Categories: Content Creation, SEO, Social Media, Email, Analytics. 5 tools per category with name, use case, free/paid, and link placeholder."
```

## Automation Script: Full Ebook Chapter Generator

```bash
#!/bin/bash
# ebook-generator.sh — Generate ebook chapters

TITLE="The Complete Guide to AI Marketing for Indian MSMEs"
OUTPUT_DIR="ebook-output"
mkdir -p $OUTPUT_DIR

chapters=(
  "Chapter 1: Understanding AI Marketing"
  "Chapter 2: Setting Up Your Digital Presence"
  "Chapter 3: Content Marketing with AI"
  "Chapter 4: SEO for MSMEs"
  "Chapter 5: Social Media Automation"
)

echo "# $TITLE" > $OUTPUT_DIR/00-intro.md
gemini prompt "Write a 200-word introduction for an ebook: $TITLE. Audience: MSME owners in India." >> $OUTPUT_DIR/00-intro.md

for i in "${!chapters[@]}"; do
  CHAPTER="${chapters[$i]}"
  FILE="$OUTPUT_DIR/$(printf '%02d' $((i+1)))-$(echo $CHAPTER | tr ' ' '-' | tr '[:upper:]' '[:lower:]').md"
  echo "# $CHAPTER" > $FILE
  gemini prompt "Write 500 words for: $CHAPTER in an ebook for Indian MSME owners. Include examples, tips, and 1 case study placeholder." >> $FILE
  echo "Generated: $CHAPTER"
done

echo "Ebook generated in $OUTPUT_DIR/"
```

Run:
```bash
chmod +x ebook-generator.sh && ./ebook-generator.sh
```

## Lead Magnet Types by Funnel Stage

| Funnel Stage | Lead Magnet Type | Example |
|-------------|-----------------|----------|
| Awareness | Checklist, Infographic | "25-Point MSME Marketing Audit" |
| Consideration | Ebook, Guide, Webinar | "Complete AI Marketing Guide" |
| Decision | Template, Swipe File | "50 Proven Email Subject Lines" |
| Retention | Mini-course, Toolkit | "5-Day AI Marketing Course" |

## Integration with This Repo

- Pair with `gemini-cli-cold-email` to deliver lead magnets via email sequences
- Pair with `gemini-cli-copywriting` for landing page copy promoting the lead magnet
- Pair with `gemini-cli-msme-growth` for India-specific lead magnet topics
- Pair with `gemini-cli-content-strategy` to plan lead magnets as content pillars

## Tips

- Lead magnets must solve ONE specific problem for ONE specific audience
- Keep checklists to 15-25 items — not too short, not overwhelming
- Always include your brand name and website in the lead magnet footer
- Save generated content in `lead-magnets/[type]/[title]/` folders
- Use temperature 0.4 for structured content, 0.6 for creative guides
