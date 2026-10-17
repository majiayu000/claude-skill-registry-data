---
name: aiwf-google-ads-business
description: Use for Google Ads, Business Profile, GA4, Google Tag Manager, Search Console, conversion tracking, Merchant Center coordination, campaign structure, keywords, audiences, budgets, attribution, Ads API work, and Google account hygiene for companies.
---

# AIWF Google Ads Business

## Core Rule

Separate account access, measurement, campaign design, and spend decisions. Verify ownership and conversion accuracy before optimizing bids or judging performance.

## Workflow

1. Inventory account IDs, owners, managers, billing, linked products, domains, properties, containers, data streams, conversions, and recovery access.
2. Define the business outcome and conversion contract: event, value, source, consent, deduplication, attribution, and validation method.
3. Map campaign type, location, language, audience, keyword or inventory intent, negatives/exclusions, creative, landing page, budget, and stop rule.
4. Validate tags and server events without sending unnecessary personal data or marking unverified events primary.
5. Review search terms, placements, change history, policy status, spend, conversions, value, and lag using explicit date windows.
6. For API work, use OAuth, developer-token and account permissions, quotas, test accounts, idempotent changes, and change receipts.

Read `references/source-register.json` before current API, UI, policy, consent, campaign, or monetization claims.

## Hard Gates

- Explicit approval is required for spend, publishing, bid/budget changes, billing, account links, user access, conversion mutations, or API writes.
- Never request passwords, cookies, recovery codes, or raw tokens; use the platform's supported authentication flow.
- Do not evade policy review, misrepresent products, use deceptive landing pages, or hide material terms.
- Add `aiwf-web-seo` for organic technical discovery and `aiwf-data-privacy-protection` for analytics/advertising data handling.

## Output

Return account map, measurement findings, prioritized campaign changes, budget and stop rules, policy gates, and a reversible execution plan.
