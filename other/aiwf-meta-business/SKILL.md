---
name: aiwf-meta-business
description: Use for company work across Facebook, Instagram, WhatsApp Business, Meta Business Suite, Pages, Ads Manager, Business Portfolio, Pixel, Conversions API, lead forms, audiences, account quality, campaign planning, and Meta policy troubleshooting.
---

# AIWF Meta Business

## Core Rule

Confirm the business objective, account ownership, region, data source, consent basis, conversion event, and approval boundary before recommending Meta setup or campaigns. Draft and inspect by default.

## Workflow

1. Inventory the Business Portfolio, Pages, Instagram accounts, ad accounts, pixels/datasets, domains, apps, catalogs, people, partners, roles, and recovery owners.
2. Verify least-privilege access, two-factor authentication, payment ownership, account quality, domain control, and backup administrators.
3. Map campaign objective to funnel stage, audience, creative, landing page, conversion event, attribution window, budget cap, and stop rule.
4. For Pixel or Conversions API, document event names, deduplication IDs, data fields, consent, retention, diagnostics, and test evidence.
5. Check ad, landing-page, lead-form, targeting, special-category, and data-use requirements against current official policy.
6. Report delivery and conversion data with date range, attribution setting, spend, denominator, and known gaps.

Read `references/source-register.json` before current UI, API, policy, targeting, or eligibility claims.

## Hard Gates

- Explicit approval is required before publishing, spending, changing payment methods, accepting terms, adding people/partners, changing roles, connecting data, or mutating an account through an API.
- Never request passwords, session cookies, recovery codes, or raw access tokens in chat or files.
- Do not circumvent review, account restrictions, consent, special-ad rules, or audience protections.
- Do not fabricate engagement, testimonials, urgency, identity, results, or endorsements.
- Add `aiwf-data-privacy-protection` for customer/lead data and `aiwf-application-api-security` for app or webhook integrations.

## Output

Return account map, ownership gaps, campaign or integration plan, policy checks, measurement contract, approval gates, and rollback steps.
