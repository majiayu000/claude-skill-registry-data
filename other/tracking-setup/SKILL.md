---
name: tracking-setup
version: 1.1.0
description: "When the user wants to set up, improve, or audit analytics tracking and measurement. Also use when the user mentions 'set up tracking,' 'GA4,' 'Google Analytics,' 'conversion tracking,' 'event tracking,' 'UTM parameters,' 'tag manager,' 'GTM,' 'analytics implementation,' or 'tracking plan.' For A/B test measurement, see ab-test-setup."
---

# Analytics Tracking

You are an expert in analytics implementation and measurement. Your goal is to help set up tracking that provides actionable insights for marketing and product decisions.

## Initial Assessment

**Check for product marketing context first:**
Read `/brain/positioning-and-messaging.md` and `/brain/truth.md` before asking questions. Use that context and only ask for information not already covered or specific to this task.

**Check for existing GA4 state:**
Before proposing any tracking work, `grep` `brief/session-brief.md` and `marketing/plans/` for GA4 / analytics / tracking topics. For your project, `marketing/plans/ga4-tracking-plan.md` and `memory/project_ga4_setup_state.md` contain the authoritative current state. Don't redo discovery work that's already captured.

Before implementing tracking, understand:

1. **Business Context** - What decisions will this data inform? What are key conversions?
2. **Current State** - What tracking exists? What tools are in use?
3. **Technical Context** - What's the tech stack? Any privacy/compliance requirements?

---

## CRITICAL PRECHECKS — run these BEFORE configuring anything

Two failure modes bit us in production at the company and produced ~70% data loss in GA4. Run these prechecks on every GA4 project before writing any tracking plan or touching configuration.

### Precheck 1: Canonicalization (apex vs www)

If the site has a root domain like `example.com`, verify one of `example.com` and `www.example.com` permanently redirects to the other. Both should NOT return HTTP 200.

```bash
curl -sI https://example.com/ | head -3
curl -sI https://www.example.com/ | head -3
```

- **If exactly one returns 301/302 to the other:** good, canonicalized. Use only the canonical in GA4's domain list.
- **If both return 200:** broken. GA4 will split traffic across two `hostName` values, cookies fragment, link equity dilutes. Fix at the CDN/hosting layer (CloudFront Function, `next.config.js` redirects, Vercel rewrites) BEFORE marking GA4 setup complete. Do NOT "work around" it by listing both in cross-domain tracking — that hides the symptom but doesn't fix the fragmentation.

### Precheck 2: Subdomain GTM verification

If the tracking plan claims cross-domain coverage of subdomains (e.g. `docs.example.com`, `app.example.com`, `go.example.com`), verify each one actually fires the GTM container or GA4 tag:

```bash
curl -s https://subdomain.example.com/ | grep -o -E "GTM-[A-Z0-9]+|G-[A-Z0-9]+" | sort -u
```

Each subdomain should return the SAME container / measurement ID as the main site.

- **Nothing returned:** GTM is not installed on that subdomain. Traffic is invisible. For HubSpot subdomains (CMS Hub hosted), install GTM via Settings → Content → Pages → Domains → Site header HTML. For Docusaurus, add `@docusaurus/plugin-google-gtag`. For Mintlify, add `analytics` block in `mint.json`.
- **Different ID returned:** that subdomain is firing into a SEPARATE GA4 property you may not know about. Find it in the GA4 account picker (Admin → account dropdown top-left). Either retire it and install the main container, or accept the separation and grant reporting access to both properties.

Plan-vs-reality mismatch on cross-domain is the single most common Phase 6 bug. Always verify.

### Precheck 3: Consent Mode v2 geo-targeting

If the site uses Consent Mode v2 with a CMP (CookieYes, OneTrust, Cookiebot, etc.), check the consent defaults for **global denial without geo-targeting**.

```bash
curl -s https://example.com/ | grep -o -E "analytics_storage['\"]?\s*:\s*['\"]denied['\"]" -m 1
```

If `analytics_storage` is denied by default without a `region` parameter limiting the denial to regulated jurisdictions, GA4 is probably capturing 25–40% of reality. This is usually the biggest lever you can pull on a GA4 property. See `references/ga4-implementation.md` under "Consent Mode v2" for the correct pattern (geo-targeted denial to EU/EEA/UK/CH + Advanced Consent Mode flags).

**Red flag pattern (strict global denial):**
```javascript
gtag('consent', 'default', {
  'analytics_storage': 'denied',  // denies everywhere
  'wait_for_update': 500
});
```

**Correct pattern (geo-targeted denial + permissive default for rest of world):**
See `references/ga4-implementation.md` for the full snippet with the EU/EEA/UK/CH region list and Advanced Consent Mode (`url_passthrough`, `ads_data_redaction`).

**Also check the CMP's own geo-targeting.** If the cookie banner is configured to show globally, US visitors will see a banner even after fixing the gtag defaults. CookieYes: `app.cookieyes.com → site → Geo-Targeting` should be set to show only for regulated regions.

---

## Core Principles

### 1. Track for Decisions, Not Data
- Every event should inform a decision
- Avoid vanity metrics
- Quality > quantity of events

### 2. Start with the Questions
- What do you need to know?
- What actions will you take based on this data?
- Work backwards to what you need to track

### 3. Name Things Consistently
- Naming conventions matter
- Establish patterns before implementing
- Document everything

### 4. Maintain Data Quality
- Validate implementation
- Monitor for issues
- Clean data > more data

---

## Tracking Plan Framework

### Structure

```
Event Name | Category | Properties | Trigger | Notes
---------- | -------- | ---------- | ------- | -----
```

### Event Types

| Type | Examples |
|------|----------|
| Pageviews | Automatic, enhanced with metadata |
| User Actions | Button clicks, form submissions, feature usage |
| System Events | Signup completed, purchase, subscription changed |
| Custom Conversions | Goal completions, funnel stages |

**For comprehensive event lists**: See [references/event-library.md](references/event-library.md)

---

## Event Naming Conventions

### Recommended Format: Object-Action

```
signup_completed
button_clicked
form_submitted
article_read
checkout_payment_completed
```

### Best Practices
- Lowercase with underscores
- Be specific: `cta_hero_clicked` vs. `button_clicked`
- Include context in properties, not event name
- Avoid spaces and special characters
- Document decisions

---

## Essential Events

### Marketing Site

| Event | Properties |
|-------|------------|
| cta_clicked | button_text, location |
| form_submitted | form_type |
| signup_completed | method, source |
| demo_requested | - |

### Product/App

| Event | Properties |
|-------|------------|
| onboarding_step_completed | step_number, step_name |
| feature_used | feature_name |
| purchase_completed | plan, value |
| subscription_cancelled | reason |

**For full event library by business type**: See [references/event-library.md](references/event-library.md)

---

## Event Properties

### Standard Properties

| Category | Properties |
|----------|------------|
| Page | page_title, page_location, page_referrer |
| User | user_id, user_type, account_id, plan_type |
| Campaign | source, medium, campaign, content, term |
| Product | product_id, product_name, category, price |

### Best Practices
- Use consistent property names
- Include relevant context
- Don't duplicate automatic properties
- Avoid PII in properties

---

## GA4 Implementation

### Quick Setup

1. Create GA4 property and data stream
2. Install gtag.js or GTM
3. Enable enhanced measurement
4. Configure custom events
5. Mark conversions in Admin

### Custom Event Example

```javascript
gtag('event', 'signup_completed', {
  'method': 'email',
  'plan': 'free'
});
```

**For detailed GA4 implementation**: See [references/ga4-implementation.md](references/ga4-implementation.md)

---

## Google Tag Manager

### Container Structure

| Component | Purpose |
|-----------|---------|
| Tags | Code that executes (GA4, pixels) |
| Triggers | When tags fire (page view, click) |
| Variables | Dynamic values (click text, data layer) |

### Data Layer Pattern

```javascript
dataLayer.push({
  'event': 'form_submitted',
  'form_name': 'contact',
  'form_location': 'footer'
});
```

**For detailed GTM implementation**: See [references/gtm-implementation.md](references/gtm-implementation.md)

---

## UTM Parameter Strategy

### Standard Parameters

| Parameter | Purpose | Example |
|-----------|---------|---------|
| utm_source | Traffic source | google, newsletter |
| utm_medium | Marketing medium | cpc, email, social |
| utm_campaign | Campaign name | spring_sale |
| utm_content | Differentiate versions | hero_cta |
| utm_term | Paid search keywords | running+shoes |

### Naming Conventions
- Lowercase everything
- Use underscores or hyphens consistently
- Be specific but concise: `blog_footer_cta`, not `cta1`
- Document all UTMs in a spreadsheet

---

## Debugging and Validation

### Testing Tools

| Tool | Use For |
|------|---------|
| GA4 DebugView | Real-time event monitoring |
| GTM Preview Mode | Test triggers before publish |
| Browser Extensions | Tag Assistant, dataLayer Inspector |

### Validation Checklist

- [ ] Events firing on correct triggers
- [ ] Property values populating correctly
- [ ] No duplicate events
- [ ] Works across browsers and mobile
- [ ] Conversions recorded correctly
- [ ] No PII leaking

### Common Issues

| Issue | Check |
|-------|-------|
| Events not firing | Trigger config, GTM loaded |
| Wrong values | Variable path, data layer structure |
| Duplicate events | Multiple containers, trigger firing twice |

---

## Privacy and Compliance

### Considerations
- Cookie consent required in EU/UK/CA
- No PII in analytics properties
- Data retention settings
- User deletion capabilities

### Implementation
- Use consent mode (wait for consent)
- IP anonymization
- Only collect what you need
- Integrate with consent management platform

---

## Output Format

**Output location:** `marketing/tracking/[setup-slug]/` — confirm the project slug with the user before creating files.

### Tracking Plan Document

```markdown
# [Site/Product] Tracking Plan

## Overview
- Tools: GA4, GTM
- Last updated: [Date]

## Events

| Event Name | Description | Properties | Trigger |
|------------|-------------|------------|---------|
| signup_completed | User completes signup | method, plan | Success page |

## Custom Dimensions

| Name | Scope | Parameter |
|------|-------|-----------|
| user_type | User | user_type |

## Conversions

| Conversion | Event | Counting |
|------------|-------|----------|
| Signup | signup_completed | Once per session |
```

---

## Task-Specific Questions

1. What tools are you using (GA4, Mixpanel, etc.)?
2. What key actions do you want to track?
3. What decisions will this data inform?
4. Who implements - dev team or marketing?
5. Are there privacy/consent requirements?
6. What's already tracked?

---

## Tool Integrations

Key analytics tools:

| Tool | Best For | MCP |
|------|----------|:---:|
| **GA4** | Web analytics, Google ecosystem | ✓ |
| **Mixpanel** | Product analytics, event tracking | - |
| **Amplitude** | Product analytics, cohort analysis | - |
| **PostHog** | Open-source analytics, session replay | - |
| **Segment** | Customer data platform, routing | - |

---

## Related Skills

- **ab-test-setup**: For experiment tracking
- **seo-geo**: For organic traffic analysis
- **page-cro**: For conversion optimization (uses this data)

---

## Field-Tested Rules

- On a CMS with a native GA4 integration (HubSpot, WordPress, Shopify, etc.), enable either GTM or the native integration, never both. Running both double-counts every pageview and makes funnel conversion rates look about half of reality. GTM is usually the right choice since the GA4 tag lives in the container.

## Learnings

<!-- Updated by /reflect. Promote stable patterns to the main skill body. -->
