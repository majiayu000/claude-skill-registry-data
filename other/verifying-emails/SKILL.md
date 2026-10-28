---
name: verifying-emails
description: Verify email addresses are real and deliverable before sending, to protect sender reputation. Use when the user has a lead list with emails and is about to start a campaign, or asks about bounce rates, email verification, or deliverability.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Verifying Emails

## Goal
Check addresses resolve before you send to them. Bounces damage domain reputation, and reputation is slow to rebuild.

## When to use
Before any first campaign from a new domain, and any time a list is older than about a month.

## Two ways

### During the scrape (easiest)
If the leads came from Google Maps, verification is a flag on the scrape itself:
```bash
python -X utf8 scripts/02_local_businesses/scrape_google_maps.py \
    --search "law firms in Mobile AL" --limit 50 \
    --contacts --leads 2 --verify-emails --out-csv output/verified.csv
```
Each decision-maker record comes back with an `emailVerification` object.

### On an existing list
```bash
python -X utf8 scripts/04_outreach/verify_emails_apify.py \
    --input output/leads.csv --output output/leads_verified.csv
```

## Reading the result

| Status | Do this |
|---|---|
| valid / deliverable | Send. |
| catch-all / accept-all | The server accepts everything, so this tells you nothing. Send, but keep these in a separate batch so a bad group doesn't poison the main one. |
| risky | Low volume only, or skip. |
| invalid / undeliverable | Remove. Do not send. |

## Rules of thumb
- Keep bounce rate under 2%. Above 5% and providers start filtering you.
- Verify in one batch before the campaign, not per-send.
- Never pattern-guess an address (`first@company.com`) and send to it unverified — that's how a domain gets burned.
- On a brand-new sending domain, warm up over 2–3 weeks before volume.

## Cost
Fractions of a cent per address.
