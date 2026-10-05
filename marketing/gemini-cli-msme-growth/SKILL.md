---
name: gemini-cli-msme-growth
description: "Use when the user wants India-specific MSME marketing automation using Gemini CLI — government scheme content, local business growth, Hindi/Hinglish copy, startup funding content, or B2G/B2B marketing for Indian markets. Trigger phrases: MSME marketing Gemini CLI, India startup content CLI, PMEGP MUDRA content Gemini, Hinglish marketing automation, UP Bihar MSME digital marketing. For general content see gemini-cli-copywriting."
version: "1.0.0"
author: "Sheevum Goel"
tags:
  - gemini-cli
  - msme
  - india
  - startup-india
  - pmegp
  - mudra
  - hinglish
  - lucknow
  - uttar-pradesh
  - b2b-india
---

## Overview

You are a Gemini CLI expert for India-specific MSME marketing. Help the user generate content tailored to Indian small businesses, government schemes, regional audiences, startup funding, and Hindi/Hinglish communication using Gemini CLI.

## When to Use

- User wants content about Indian government schemes (PMEGP, MUDRA, Startup India)
- User needs Hindi or Hinglish marketing content
- User wants local SEO content for cities like Lucknow, Jaipur, Surat, etc.
- User wants B2G (business-to-government) content for grant applications
- User needs MSME-specific growth playbooks

## Prerequisites

- Gemini CLI installed and authenticated (see `gemini-cli-setup`)
- Defined: target region, business type, language preference
- Gemini model: use `gemini-1.5-pro` for best Hindi language output

## Core MSME India Commands

### Government Scheme Summary (PMEGP)

```bash
gemini prompt "Write a simple, easy-to-understand 200-word summary of the PMEGP (Prime Minister's Employment Generation Programme) scheme for a kirana store owner in Uttar Pradesh. Include: eligibility, loan amount, subsidy, how to apply. Language: simple English."
```

### MUDRA Loan Content

```bash
gemini prompt "Create a WhatsApp message explaining MUDRA Loan Scheme (Shishu, Kishor, Tarun categories) to MSME owners in Lucknow. Keep it under 100 words. Use simple language. Include the official website."
```

### Hindi Marketing Copy

```bash
gemini prompt "Write an Instagram caption in Hindi for an AI marketing agency in Lucknow that helps small businesses grow online. Tone: friendly, motivating. Include 10 Hindi hashtags. Use Devanagari script."
```

### Hinglish Social Post

```bash
gemini prompt "Write a Hinglish (Hindi + English mix) Facebook post for a digital marketing agency targeting MSME owners in UP and Bihar. Topic: how social media can double their sales. Friendly tone. Max 100 words."
```

### Local SEO Content (City-Specific)

```bash
gemini prompt "Write a 150-word local SEO landing page description for a digital marketing agency in Lucknow, Uttar Pradesh. Target keyword: best digital marketing agency in Lucknow. Include USPs, service list, and a local CTA."
```

### Startup India Grant Application Brief

```bash
gemini prompt "Write a project brief for a Startup India recognition application for an AI-powered CRM startup serving MSMEs in India. Include: problem statement, solution, innovation, market size, team structure placeholder, and expected social impact."
```

### B2B Outreach for Indian SMEs

```bash
gemini prompt "Write a WhatsApp outreach message (under 80 words) from an AI marketing agency to a textile MSME owner in Surat. Goal: offer a free 30-min marketing audit call. Tone: respectful, direct."
```

## Automation Script: Regional Content Campaign

```bash
#!/bin/bash
# msme-campaign.sh — Generate city-specific MSME content

OUTPUT_FILE="msme-campaign.md"

cities=("Lucknow" "Kanpur" "Jaipur" "Surat" "Pune" "Coimbatore")

echo "# MSME Regional Content Campaign" > $OUTPUT_FILE
echo "Generated: $(date)" >> $OUTPUT_FILE

for CITY in "${cities[@]}"; do
  echo "" >> $OUTPUT_FILE
  echo "## $CITY" >> $OUTPUT_FILE
  echo "### Social Post" >> $OUTPUT_FILE
  gemini prompt "Write an Instagram post for an AI marketing agency targeting MSME owners in $CITY, India. Include local reference and 10 hashtags." >> $OUTPUT_FILE
  echo "### WhatsApp Outreach" >> $OUTPUT_FILE
  gemini prompt "Write a WhatsApp outreach message to a small business owner in $CITY about AI marketing tools. Under 80 words." >> $OUTPUT_FILE
done

echo "Done! Saved to $OUTPUT_FILE"
```

Run:
```bash
chmod +x msme-campaign.sh && ./msme-campaign.sh
```

## Key Indian Government Schemes Reference

| Scheme | Target | Benefit |
|--------|--------|---------|
| PMEGP | New entrepreneurs | Up to ₹25L loan, 15-35% subsidy |
| MUDRA Loan | MSMEs | Up to ₹10L (Shishu/Kishor/Tarun) |
| Startup India | Tech startups | Tax exemption, funding support |
| SIDBI | Small industries | Low-interest loans |
| GeM Portal | MSMEs | Govt procurement marketplace |
| ONDC | E-commerce MSMEs | Open digital commerce network |

## Language Content Templates

```bash
# Pure Hindi
gemini prompt "Hindi mein likho: [topic]. Devanagari script use karo."

# Hinglish
gemini prompt "Write in Hinglish (natural Hindi-English mix): [topic]. Like how young Indians actually speak."

# Regional English (Indian tone)
gemini prompt "Write in Indian English tone for [city] audience: [topic]. Warm, respectful, community-focused."
```

## Integration with This Repo

- Pair with `gemini-cli-seo` for local Indian city SEO content
- Pair with `gemini-cli-social` for regional platform-specific posts
- Pair with `gemini-cli-cold-email` for Hindi/Hinglish outreach campaigns
- Pair with `gemini-cli-lead-magnets` for govt scheme guide PDFs

## Tips

- Always specify the city/state for hyper-local content
- Use `gemini-1.5-pro` for best Hindi language output quality
- Test Hindi outputs with a native speaker before publishing
- Align content with local festivals: Diwali, Holi, Navratri, Eid
- Reference government schemes by their official Hindi names for authenticity
