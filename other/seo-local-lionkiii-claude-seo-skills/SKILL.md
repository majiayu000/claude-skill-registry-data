---
name: seo-local
description: >
  Local SEO audit covering NAP consistency, local schema markup, Google Business
  Profile signals, local content, citations, review signals, and mobile optimization.
  No MCP required — fetches pages via WebFetch. Use when user says "local SEO",
  "Google Business Profile", "GBP", "NAP consistency", "local citations",
  "local schema", "local pack", "map pack".
allowed-tools:
  - Read
  - Bash
  - Glob
  - WebFetch
---

# Local SEO Audit

Performs a comprehensive local SEO audit from live URL fetching. No MCP required.

## Inputs

- `business`: Business name, URL, or location string.
  - If URL: fetch the homepage directly.
  - If business name + location (e.g., "Acme Plumbing Austin TX"): note that live lookup is not possible; analyze any URL the user provides separately.
  - Best input: homepage URL (e.g., `https://acme-plumbing.com`).

## Execution

**Step 1: Fetch and Extract Business Info**

Fetch homepage with WebFetch. Also fetch `/contact` and `/about` if linked from homepage.
Extract from HTML:
- Business name (from `<title>`, H1, or schema)
- Address (street, city, state, zip, country)
- Phone number(s)
- Email address(es)
- Schema markup (look for `<script type="application/ld+json">` blocks)

**Step 2: NAP Consistency Check**

NAP = Name, Address, Phone. Consistency across the site is a local ranking factor.
Check: homepage, footer, contact page, about page, schema markup.
For each location of NAP found, record exact text and flag discrepancies:
- Different phone formats (`(512) 555-1234` vs `512-555-1234`) — NOTE (not critical)
- Different address formats (abbreviated vs full state) — NOTE
- Completely different address or phone — CRITICAL flag

**Step 3: Local Schema Audit**

Check for these schema types in JSON-LD blocks:
- `LocalBusiness` (or subtype: `Plumber`, `Restaurant`, `MedicalBusiness`, etc.)
- Required properties: `name`, `address` (as `PostalAddress`), `telephone`
- Recommended: `geo` (as `GeoCoordinates`), `openingHours`, `url`, `image`, `priceRange`
- `PostalAddress` requires: `streetAddress`, `addressLocality`, `addressRegion`, `postalCode`

For any missing required/recommended properties, generate corrected JSON-LD at the end of output.
Detect business type from schema type or page content to select appropriate LocalBusiness subtype.

**Step 4: Google Business Profile Signals**

Check for presence of:
- Google Maps embed (`maps.google.com` or `google.com/maps` iframe)
- GBP link (`business.google.com/` or Google Maps URL with place ID)
- Reviews integration (review schema, review widget, or link to Google reviews)
- Service area mentions (city names, county, "serving [city]" in body text)
- Operating hours on website

**Step 5: Local Content Signals**

- City/region in `<title>` tag: check if geo-modifier present (e.g., "Plumber in Austin")
- City/region in H1: check if location keyword present
- Location pages (if multi-location): look for `/[city]/` URL pattern or location listing pages
- Local testimonials: customer names with locations, Google review embeds
- Proximity/location keywords in body: "near me", "in [city]", "serving [area]"

**Step 6: Citation Opportunities**

Based on detected business type, list relevant citation directories:

General (all business types):
- Google Business Profile, Yelp, BBB (Better Business Bureau), Yellow Pages, Apple Maps, Bing Places, Foursquare

Industry-specific (detect from schema type, title, or content):
- Restaurants: TripAdvisor, OpenTable, Zomato
- Healthcare: Healthgrades, ZocDoc, WebMD, Vitals
- Legal: Avvo, FindLaw, Justia, Lawyers.com
- Home Services: HomeAdvisor, Angi, Thumbtack, Houzz
- Real Estate: Zillow, Realtor.com, Trulia

Check if any citation platforms are already linked from the site.

**Step 7: Review Signals**

- Review schema (`@type: Review` or `AggregateRating` in JSON-LD)
- Review platform links (Google, Yelp, Trustpilot, industry-specific)
- Aggregate review score displayed on site
- Review request CTA (e.g., "Leave us a review" button/link)

**Step 8: Mobile Optimization**

Local searches are 60%+ mobile — check:
- `<meta name="viewport" content="width=device-width">` present
- Click-to-call links: `<a href="tel:+1...">` for phone numbers (not just plain text)
- Google Maps embed responsive (not fixed width)
- Tap targets for key CTAs (subjective — note if CTA buttons exist)

**Local SEO Score Calculation (0-100)**

| Factor | Max Points |
|--------|-----------|
| NAP consistent across all pages | 20 |
| LocalBusiness schema present and valid | 20 |
| GBP signals (Maps embed + GBP link) | 15 |
| Local content signals (title + H1 + body) | 15 |
| Citation platform presence (3+ found) | 10 |
| Review signals | 10 |
| Mobile: click-to-call + viewport | 10 |

## Output Format

```
## Local SEO Audit: [business name / URL]

**Local SEO Score: [N]/100**

### NAP Consistency Status

| Location | Name | Address | Phone | Match? |
|----------|------|---------|-------|--------|

### Local Schema

**Status:** [Present / Missing / Incomplete]
[If issues: show corrected JSON-LD block]

### GBP Integration Checklist

- [x] Google Maps embed
- [ ] GBP link
- [x] Operating hours
- [ ] Review integration
- [x] Service area mentions

### Local Content Assessment

| Signal | Status | Detail |
|--------|--------|--------|
| City in title | PASS/FAIL | [title content] |
| City in H1 | PASS/FAIL | [H1 content] |
| Location pages | N/A / Found | |

### Citation Opportunities

| Platform | Category | Status |
|----------|----------|--------|
| Google Business Profile | General | [Linked / Not detected] |
| Yelp | General | [Linked / Not detected] |

### Priority Actions

[Critical/High/Medium/Low action items]

## Data Sources

- Live fetch: [URL] via WebFetch
- Schema: extracted from page JSON-LD
```
