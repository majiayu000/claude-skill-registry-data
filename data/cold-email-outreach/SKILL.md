---
name: cold-email-outreach
description: Automated cold email outreach pipeline using Resend API. Builds prospect lists from government databases or web scraping, enriches with contact info, sends personalized cold emails with drip follow-ups, and tracks responses. Use when setting up cold email campaigns, building lead lists, automating email outreach, prospecting businesses, sending drip sequences, or managing email deliverability.
---

# Cold Email Outreach — Automated Prospecting & Drip Pipeline

Build lists, enrich contacts, send personalized cold emails, follow up automatically.

## Pipeline Overview

1. **Source** — Pull leads from government databases, web scraping, or CSV import
2. **Enrich** — Find emails via website scraping, Google search, or enrichment APIs
3. **Personalize** — Generate custom email copy per lead using templates + variables
4. **Send** — Deliver via Resend API with rate limiting and domain rotation
5. **Follow Up** — Automated drip sequences (Day 3, Day 7)
6. **Track** — Log opens, replies, bounces to Google Sheets or CSV

## Requirements

- **Resend API key** — `RESEND_API_KEY` (free tier: 100 emails/day)
- **Verified sending domain** — SPF + DKIM + DMARC configured
- **Google Sheets OAuth** (optional) — for lead tracking

## Quick Start

```bash
export RESEND_API_KEY=your_key

# Send from CSV list
node scripts/send-campaign.js --list leads.csv --template templates/intro.txt --from "hello@yourdomain.com"

# Dry run (no emails sent)
node scripts/send-campaign.js --list leads.csv --template templates/intro.txt --dry-run

# Send follow-ups
node scripts/send-followups.js --campaign campaign-2026-03-12
```

## Email Templates

Templates use `{variable}` placeholders:

```
Subject: {subject}

Hi {first_name},

{body}

Best,
{sender_name}
```

Available variables: `{first_name}`, `{business_name}`, `{city}`, `{industry}`, `{specific_issue}`, `{sender_name}`, `{subject}`

## Deliverability Rules

- Max 25 emails per domain per day (cold outreach)
- Warm up new domains: start at 5/day, increase by 5 every 3 days
- Always include physical address (CAN-SPAM)
- Include unsubscribe mechanism
- Rotate sending domains if scaling past 50/day
- Remove bounced emails immediately
- Honor unsubscribes within 24 hours

## Scripts

- `scripts/send-campaign.js` — Main campaign sender with rate limiting
- `scripts/send-followups.js` — Drip follow-up sender
- `scripts/enrich-list.js` — Email enrichment from websites

## References

- `references/templates.md` — Proven email templates with open rates
- `references/deliverability.md` — Domain setup and spam prevention guide
