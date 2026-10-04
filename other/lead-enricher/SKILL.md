---
name: lead-enricher
description: >
  Enriches inbound leads with firmographic and technographic data.
  Takes minimal lead info and enriches via WebSearch, Apollo, or ZoomInfo
  to produce a complete lead record with company size, revenue, tech stack,
  social profiles, and decision-maker details.
tags: [leads, enrichment, firmographic, research]
---

# Lead Enricher

Takes raw inbound lead data (often just a name and email) and enriches it into a complete lead record. Uses WebSearch for public data, checks `tools.lead_enrichment` config for Apollo or ZoomInfo API paths, and outputs a fully populated lead record ready for qualification and routing.

## Prerequisites

- `agency.config.json` populated (ICP, tools config)
- WebSearch tool available
- Inbound lead data: at minimum, email address or company name
- Optional: Apollo.io API access (configured in `tools.lead_enrichment`)
- Optional: ZoomInfo access (configured in `tools.lead_enrichment`)

## Capabilities Used

1. `company-researcher` -- deep company data extraction
2. `person-researcher` -- contact-level enrichment
3. `linkedin-researcher` -- LinkedIn profile data
4. `email-validator` -- verify email deliverability
5. `crm-writer` -- write enriched record back to CRM

## Phase 0: Intake

Read `agency.config.json`:
- `icp.segments[]` -- for ICP fit tagging during enrichment
- `tools.lead_enrichment` -- check which enrichment tools are available:
  ```json
  {
    "tools": {
      "lead_enrichment": {
        "primary": "apollo",
        "apollo_api_key": "env:APOLLO_API_KEY",
        "zerobounce_api_key": "env:ZEROBOUNCE_API_KEY",
        "fallback": "websearch"
      }
    }
  }
  ```
- `crm.tabs` -- where to write enriched records
- `services[]` -- for service-need matching during enrichment

Accept parameters:
- `lead` -- (required) lead object with available fields
- `mode` -- `single` | `batch`. Default: `single`
- `leads` -- (required if mode = `batch`) array of lead objects
- `enrichment_depth` -- `basic` | `standard` | `deep`. Default: `standard`
- `validate_email` -- boolean, run email validation. Default: `true`
- `write_to_crm` -- boolean, write enriched record to CRM. Default: `true`

Minimum lead input:
```json
{
  "email": "priya@freshskin.co"
}
```
Or:
```json
{
  "contact_name": "Priya Mehta",
  "company_name": "FreshSkin Co"
}
```

## Phase 1: Email Domain Extraction

If only email provided:
- Extract domain: `freshskin.co`
- Derive company domain: check if `freshskin.co` resolves to a website
- Flag freemail domains (gmail.com, yahoo.com, outlook.com) -- lower quality lead signal

If company name provided but no domain:
- WebSearch: `"{{company_name}}" website`
- Extract the primary domain

## Phase 2: Contact Enrichment

### Apollo Path (if tools.lead_enrichment.primary = "apollo")
Use Apollo People Match or People Search:
- Input: email or name + company
- Extract: full name, title, phone, LinkedIn URL, company details
- Apollo returns: person match confidence, verified email, company firmographics

### WebSearch Path (if Apollo unavailable or as supplement)
Run `person-researcher` with available data:

**Name + Company search**:
- WebSearch: `"{{contact_name}}" "{{company_name}}"`
- WebSearch: `"{{contact_name}}" linkedin`
- WebSearch: `"{{contact_name}}" {{company_domain}}`

**Extract**:
- Full name (verify spelling)
- Current title and role
- LinkedIn profile URL
- Twitter/X handle
- Other social profiles
- Professional background summary
- Recent activity (posts, interviews, conference appearances)

### LinkedIn Enrichment
Run `linkedin-researcher` for:
- Profile headline and summary
- Current role details (start date, description)
- Previous roles (career trajectory)
- Education
- Skills and endorsements
- Connections count (proxy for network size)
- Recent posts (content they care about)
- Groups (interests and focus areas)

Compile:
```
CONTACT RECORD
---
Full name: [verified name]
Email: [email]
Email status: [valid/invalid/catch-all/unknown]
Title: [current title]
Phone: [if found]
LinkedIn: [URL]
Twitter: [handle]
Location: [city, country]
Seniority: [C-level/VP/Director/Manager/Individual]
Department: [Marketing/Ecommerce/Engineering/Operations/Executive]
```

## Phase 3: Company Enrichment

### Apollo Path (if available)
Use Apollo Organization Enrich:
- Input: domain
- Extract: company name, industry, employee count, revenue range, tech stack, social profiles

### WebSearch Path
Run `company-researcher` with the company domain:

**Firmographic data**:
- Company legal name
- Industry and sub-industry (SIC/NAICS if available)
- Employee count (exact or range)
- Revenue estimate (range)
- Founded year
- Headquarters location
- Funding status (bootstrapped, seed, Series A/B/C, public)
- Total funding raised

**Digital presence**:
- Website URL and platform (Shopify, WooCommerce, custom, etc.)
- Technology stack (via BuiltWith signals in search results)
- Social profiles: LinkedIn company page, Instagram, Twitter, Facebook, YouTube
- App store presence (if applicable)
- Review sites (G2, Capterra, Trustpilot, Google Reviews)

**Business signals**:
- Recent funding rounds
- Job postings (roles, departments expanding)
- Press mentions (last 6 months)
- Partnership announcements
- Product launches
- Awards or recognition
- Competitor landscape (who else is in their space)

Compile:
```
COMPANY RECORD
---
Company name: [legal name]
Domain: [primary domain]
Industry: [vertical]
Sub-industry: [niche]
Employee count: [range]
Revenue estimate: [range]
Founded: [year]
HQ: [city, country]
Funding: [status + total raised]
Platform: [ecommerce platform]
Tech stack: [key technologies detected]

Social profiles:
  LinkedIn: [URL]
  Instagram: [handle]
  Twitter: [handle]
  Facebook: [URL]
  YouTube: [URL]

Recent signals:
  Hiring: [roles if any]
  Funding: [recent round if any]
  Press: [notable mentions]
  Product: [recent launches]
```

## Phase 4: Email Validation

If `validate_email` = true:

### ZeroBounce Path (if configured)
- Submit email to ZeroBounce API
- Get: status (valid/invalid/catch-all/spamtrap/abuse/unknown), sub-status, domain info

### Heuristic Path (if no API)
- Check MX records for domain
- Check if domain is active
- Flag disposable email domains
- Flag role-based emails (info@, hello@, support@)

Validation result:
```
Email validation:
  Address: [email]
  Status: [valid/invalid/risky/unknown]
  Type: [personal/role-based/freemail]
  Deliverability: [HIGH/MEDIUM/LOW]
  Risk flags: [catch-all, new domain, etc.]
```

## Phase 5: ICP Tagging

Match enriched data against `icp.segments[]`:

For each segment, check:
- Industry match
- Company size match (employee range)
- Revenue range match
- Geography match
- Platform match
- Stage match (post-PMF, mid-market, enterprise)

Tag the lead:
```
ICP Assessment:
  Best segment match: [segment name]
  Fit score: [1-5]
  Matching criteria: [list of matches]
  Non-matching criteria: [list of misses]
  Fit verdict: STRONG_FIT / MODERATE_FIT / WEAK_FIT / NO_FIT
```

## Phase 6: Service Need Detection

Based on enriched data, flag potential service needs:

- **Store development**: Outdated store, non-Shopify platform, poor mobile experience
- **CRO**: High traffic + low conversion signals, basic product pages
- **Catalog management**: Large SKU count, poor product imagery
- **Performance marketing**: Low traffic, no paid ads visible, competitor ads running
- **SEO**: Low organic visibility, thin content, no blog
- **Email marketing**: No email capture visible, no post-purchase flow

```
Detected needs:
  1. [Service] -- [signal that indicates this need] -- Confidence: [HIGH/MEDIUM/LOW]
  2. [Service] -- [signal] -- Confidence: [level]
```

## Phase 7: Output

Return structured JSON:

```json
{
  "enrichment_date": "2026-03-07",
  "enrichment_depth": "standard",
  "contact": {
    "full_name": "Priya Mehta",
    "email": "priya@freshskin.co",
    "email_valid": true,
    "email_type": "personal",
    "title": "Founder & CEO",
    "phone": "+91-98XXXXXXXX",
    "linkedin": "https://linkedin.com/in/priyamehta",
    "twitter": "@priyamehta",
    "location": "Mumbai, India",
    "seniority": "C-level",
    "department": "Executive"
  },
  "company": {
    "name": "FreshSkin Co",
    "domain": "freshskin.co",
    "industry": "Beauty & Skincare",
    "sub_industry": "D2C Skincare",
    "employee_count": "25-50",
    "revenue_estimate": "INR 5-10 Cr/year",
    "founded": 2022,
    "hq": "Mumbai, India",
    "funding": {"status": "Series A", "total_raised": "INR 8 Cr"},
    "platform": "Shopify",
    "tech_stack": ["Shopify", "Klaviyo", "Google Analytics"],
    "social": {
      "linkedin": "https://linkedin.com/company/freshskinco",
      "instagram": "@freshskinco",
      "twitter": "@freshskinco"
    },
    "recent_signals": {
      "hiring": ["Marketing Manager", "Content Creator"],
      "funding": "Series A closed Dec 2025",
      "product_launches": ["New serum line launched Jan 2026"]
    }
  },
  "icp_assessment": {
    "best_segment": "Post-PMF D2C India",
    "fit_score": 4,
    "fit_verdict": "STRONG_FIT",
    "matching": ["industry", "size", "geo", "platform", "stage"],
    "non_matching": []
  },
  "detected_needs": [
    {"service": "CRO", "signal": "Basic product pages, no trust elements", "confidence": "HIGH"},
    {"service": "Catalog Management", "signal": "50+ SKUs with inconsistent photography", "confidence": "MEDIUM"}
  ],
  "enrichment_sources": ["websearch", "linkedin", "zerobounce"],
  "data_completeness": "85%",
  "missing_fields": ["phone", "revenue_exact"],
  "generated_at": "2026-03-07T10:00:00Z"
}
```

## Phase 8: CRM Write and Handoff

If `write_to_crm` = true:
- Write enriched record to CRM via `crm-writer`
- Set `enrichment_status` = "complete"
- Set `enrichment_date` = today
- Set `icp_fit` = fit verdict

Handoff options:
- If `auto_qualify` flag set, trigger `lead-qualifier` with enriched data
- If `auto_route` flag set, trigger `lead-router` after qualification
- Otherwise, present enriched record for manual review

**APPROVAL GATE**: "Lead enriched. [Data completeness]% complete. Route to qualification?"

## Example Usage

Trigger phrases:
- "Enrich this lead: priya@freshskin.co"
- "I got a new inbound lead, enrich them: [name] at [company]"
- "Batch enrich this week's inbound leads"
- "Look up everything about [person] at [company]"
- "Fill in the missing data for [lead]"
- "Enrich and qualify [lead name]"
