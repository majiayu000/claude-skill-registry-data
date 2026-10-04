---
name: site-review
description: >
  Comprehensive website SEO and conversion audit with built-in fact-checking.
  Technical SEO, tactical SEO, intake/lead form assessment, and CRO analysis.
  Use when asked to "review a site", "SEO audit", "check a website", "conversion audit",
  "site review", "website analysis", or "intake assessment".
---

# Site Review — SEO & Conversion Audit with Fact-Checking

Run a comprehensive website review covering technical SEO, tactical SEO, intake/conversion assessment, and CRO opportunities. Every finding is internally verified before reporting.

## Critical Rule: Verify Everything

**NEVER report a finding without verifying it through at least two methods.** The #1 failure mode of site reviews is false findings. Common traps:

| False Finding | Reality | How to Verify |
|---------------|---------|---------------|
| "No chat widget" | Chat loads async via third-party script | Check all `<script>` sources for chat providers |
| "Phone number mismatch" | Dynamic number insertion (CallRail, etc.) | Check for call tracking scripts, inspect JS |
| "No structured data" | Schema in `<script type="application/ld+json">` | Search full HTML for `ld+json` |
| "Form only has X fields" | Fields render via JS or are below fold | Use `snapshot -i` to find ALL interactive elements |
| "No analytics" | Tag manager loads analytics async | Check for GTM, Segment, or other tag managers |
| "Missing meta tags" | Tags set dynamically via JS framework | Run `js "document.querySelector('meta[name=description]')?.content"` |

## Workflow

### Phase 0: Setup & Initial Scan

```bash
B=~/.claude/skills/gstack/browse/dist/browse

# Navigate and wait for full load
PATH="$HOME/.bun/bin:$PATH" $B goto <url>
PATH="$HOME/.bun/bin:$PATH" $B wait "body"

# Capture baseline data (run all)
PATH="$HOME/.bun/bin:$PATH" $B text                           # Full page text
PATH="$HOME/.bun/bin:$PATH" $B snapshot -i                    # All interactive elements
PATH="$HOME/.bun/bin:$PATH" $B links                          # All links
PATH="$HOME/.bun/bin:$PATH" $B perf                           # Performance timings
PATH="$HOME/.bun/bin:$PATH" $B screenshot /tmp/site-review.png # Visual capture
```

### Phase 1: Technical SEO Audit

Check each item. For every finding, note the verification method used.

#### 1A. Page Speed & Core Web Vitals
```bash
# Performance timing
PATH="$HOME/.bun/bin:$PATH" $B perf

# Check resource loading
PATH="$HOME/.bun/bin:$PATH" $B js "performance.getEntriesByType('resource').length"
PATH="$HOME/.bun/bin:$PATH" $B js "performance.getEntriesByType('resource').filter(r => r.duration > 500).map(r => r.name + ' (' + Math.round(r.duration) + 'ms)').join('\n')"

# Check image optimization
PATH="$HOME/.bun/bin:$PATH" $B js "document.querySelectorAll('img').length"
PATH="$HOME/.bun/bin:$PATH" $B js "[...document.querySelectorAll('img')].filter(i => !i.loading).map(i => i.src).join('\n')"
```

**Check:**
- [ ] Page load time (DOMContentLoaded, Load)
- [ ] Number of HTTP requests
- [ ] Large/slow resources (>500ms)
- [ ] Images without lazy loading
- [ ] Render-blocking resources

#### 1B. Meta Tags & SEO Essentials
```bash
# Meta tags (verify via JS, not just HTML source)
PATH="$HOME/.bun/bin:$PATH" $B js "document.title"
PATH="$HOME/.bun/bin:$PATH" $B js "document.querySelector('meta[name=\"description\"]')?.content || 'MISSING'"
PATH="$HOME/.bun/bin:$PATH" $B js "document.querySelector('link[rel=\"canonical\"]')?.href || 'MISSING'"
PATH="$HOME/.bun/bin:$PATH" $B js "document.querySelector('meta[name=\"robots\"]')?.content || 'NOT SET'"

# Open Graph
PATH="$HOME/.bun/bin:$PATH" $B js "document.querySelector('meta[property=\"og:title\"]')?.content || 'MISSING'"
PATH="$HOME/.bun/bin:$PATH" $B js "document.querySelector('meta[property=\"og:description\"]')?.content || 'MISSING'"
PATH="$HOME/.bun/bin:$PATH" $B js "document.querySelector('meta[property=\"og:image\"]')?.content || 'MISSING'"
```

**Check:**
- [ ] Title tag (present, <60 chars, includes primary keyword)
- [ ] Meta description (present, <160 chars, compelling)
- [ ] Canonical URL (present, correct)
- [ ] Robots meta (not accidentally blocking)
- [ ] Open Graph tags (title, description, image)
- [ ] Twitter Card tags

#### 1C. Structured Data
```bash
# Check ALL script tags for schema (MUST do this, not just check one spot)
PATH="$HOME/.bun/bin:$PATH" $B js "[...document.querySelectorAll('script[type=\"application/ld+json\"]')].map(s => JSON.parse(s.textContent)['@type'] || 'unknown').join(', ') || 'NO SCHEMA FOUND'"

# Get full schema content
PATH="$HOME/.bun/bin:$PATH" $B js "[...document.querySelectorAll('script[type=\"application/ld+json\"]')].map(s => s.textContent).join('\n---\n')"
```

**Check:**
- [ ] Organization schema
- [ ] LocalBusiness schema (if applicable)
- [ ] Service/Product schema
- [ ] FAQ schema (if FAQ exists on page)
- [ ] BreadcrumbList schema
- [ ] Review/Rating schema (if applicable)

#### 1D. Crawlability & Indexing
```bash
# Check robots.txt
PATH="$HOME/.bun/bin:$PATH" $B goto <base-url>/robots.txt
PATH="$HOME/.bun/bin:$PATH" $B text

# Check sitemap
PATH="$HOME/.bun/bin:$PATH" $B goto <base-url>/sitemap.xml
PATH="$HOME/.bun/bin:$PATH" $B text

# Return to main page
PATH="$HOME/.bun/bin:$PATH" $B goto <url>
```

**Check:**
- [ ] robots.txt exists and is valid
- [ ] sitemap.xml exists and is valid
- [ ] No critical pages blocked by robots.txt
- [ ] Sitemap includes all important pages

#### 1E. Mobile & Responsive
```bash
# Check viewport meta
PATH="$HOME/.bun/bin:$PATH" $B js "document.querySelector('meta[name=\"viewport\"]')?.content || 'MISSING'"

# Mobile screenshot
PATH="$HOME/.bun/bin:$PATH" $B viewport 375x812
PATH="$HOME/.bun/bin:$PATH" $B screenshot /tmp/site-review-mobile.png

# Check for horizontal scroll issues
PATH="$HOME/.bun/bin:$PATH" $B js "document.documentElement.scrollWidth > document.documentElement.clientWidth"

# Reset viewport
PATH="$HOME/.bun/bin:$PATH" $B viewport 1440x900
```

**Check:**
- [ ] Viewport meta tag present
- [ ] No horizontal scroll on mobile
- [ ] Text readable without zooming
- [ ] Touch targets adequate size (48x48px min)
- [ ] Images scale properly

#### 1F. Security & Performance
```bash
# Check HTTPS, cookies, headers
PATH="$HOME/.bun/bin:$PATH" $B js "location.protocol"
PATH="$HOME/.bun/bin:$PATH" $B js "document.cookie"

# Check for mixed content
PATH="$HOME/.bun/bin:$PATH" $B js "[...document.querySelectorAll('[src]')].filter(el => el.src.startsWith('http://')).map(el => el.tagName + ': ' + el.src).join('\n') || 'No mixed content'"
```

**Check:**
- [ ] HTTPS enabled
- [ ] No mixed content warnings
- [ ] HTTP → HTTPS redirect works

### Phase 2: Tactical SEO Audit

#### 2A. Heading Structure
```bash
PATH="$HOME/.bun/bin:$PATH" $B js "[...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(h => h.tagName + ': ' + h.textContent.trim().substring(0,80)).join('\n')"
```

**Check:**
- [ ] Single H1 tag
- [ ] H1 includes primary keyword
- [ ] Logical heading hierarchy (no skipped levels)
- [ ] Headings are descriptive, not generic

#### 2B. Content Quality
```bash
# Word count
PATH="$HOME/.bun/bin:$PATH" $B js "document.body.innerText.split(/\\s+/).length"

# Check for thin content areas
PATH="$HOME/.bun/bin:$PATH" $B text
```

**Check:**
- [ ] Sufficient word count for topic (500+ for service pages, 1000+ for articles)
- [ ] Primary keyword used naturally in body text
- [ ] No keyword stuffing
- [ ] Content addresses user intent
- [ ] E-E-A-T signals present (credentials, experience, expertise)

#### 2C. Internal Linking
```bash
# Get all internal links
PATH="$HOME/.bun/bin:$PATH" $B js "[...document.querySelectorAll('a[href]')].filter(a => a.href.includes(location.hostname)).map(a => a.textContent.trim().substring(0,40) + ' → ' + a.pathname).join('\n')"

# Check for broken anchor text
PATH="$HOME/.bun/bin:$PATH" $B js "[...document.querySelectorAll('a[href]')].filter(a => !a.textContent.trim() && !a.querySelector('img')).map(a => a.href).join('\n') || 'All links have text'"
```

**Check:**
- [ ] Internal links to key pages
- [ ] Descriptive anchor text (not "click here")
- [ ] No orphan pages (pages with no internal links pointing to them)
- [ ] Navigation is clear and complete

#### 2D. Local SEO (if applicable)
```bash
# Check for address/location info
PATH="$HOME/.bun/bin:$PATH" $B js "document.body.innerText.match(/\\d{5}(-\\d{4})?/g) || 'No zip codes found'"

# Check for phone numbers
PATH="$HOME/.bun/bin:$PATH" $B js "[...document.querySelectorAll('a[href^=\"tel:\"]')].map(a => a.href).join(', ') || 'No tel: links'"
```

**Check:**
- [ ] NAP consistency (Name, Address, Phone)
- [ ] LocalBusiness schema
- [ ] Google Business Profile link
- [ ] Service area pages (if multi-location)

### Phase 3: Third-Party Tools & Scripts Inventory

**This phase prevents false findings.** Before reporting on chat, analytics, call tracking, or any third-party tool, inventory everything that's loaded.

```bash
# Get ALL external scripts
PATH="$HOME/.bun/bin:$PATH" $B js "[...document.querySelectorAll('script[src]')].map(s => s.src).join('\n')"

# Get ALL iframes
PATH="$HOME/.bun/bin:$PATH" $B js "[...document.querySelectorAll('iframe')].map(f => f.src || f.id || 'anonymous iframe').join('\n')"

# Check for common tools by global variables
PATH="$HOME/.bun/bin:$PATH" $B js "({gtm: typeof google_tag_manager !== 'undefined', ga: typeof gtag !== 'undefined' || typeof ga !== 'undefined', fbq: typeof fbq !== 'undefined', hotjar: typeof hj !== 'undefined', hubspot: typeof _hsq !== 'undefined', intercom: typeof Intercom !== 'undefined', drift: typeof drift !== 'undefined', crisp: typeof $crisp !== 'undefined', zendesk: typeof zE !== 'undefined', callrail: !!document.querySelector('script[src*=\"callrail\"],script[src*=\"calltrk\"]'), leadtrap: !!document.querySelector('script[src*=\"leadtrap\"]'), vwo: typeof _vwo_code !== 'undefined'})"
```

**Identify and document:**
- [ ] Analytics (GA4, GTM, Segment, Mixpanel, etc.)
- [ ] Chat widgets (Intercom, Drift, Crisp, Zendesk, custom)
- [ ] Call tracking (CallRail, CallTrackingMetrics, etc.)
- [ ] A/B testing (VWO, Optimizely, Google Optimize)
- [ ] CRM integrations (HubSpot, Salesforce)
- [ ] Marketing pixels (Facebook, LinkedIn, Google Ads)
- [ ] Form tools (Typeform, Jotform, embedded forms)
- [ ] CMS platform (WordPress, Webflow, Squarespace, custom)

### Phase 4: Intake & Conversion Assessment

#### 4A. Lead Capture Forms
```bash
# Find ALL forms and their fields
PATH="$HOME/.bun/bin:$PATH" $B snapshot -i

# Detailed form field inventory
PATH="$HOME/.bun/bin:$PATH" $B js "[...document.querySelectorAll('form')].map((f,i) => 'Form ' + i + ':\\n' + [...f.querySelectorAll('input,select,textarea')].map(el => '  ' + (el.name||el.id||el.type) + ' (' + el.type + ')' + (el.required ? ' [required]' : '')).join('\\n')).join('\\n\\n') || 'No forms found'"
```

**Check:**
- [ ] Form exists above the fold
- [ ] Form fields are appropriate (not too many, not too few)
- [ ] Required fields marked
- [ ] Form has clear CTA button text (not just "Submit")
- [ ] Form has privacy/consent text
- [ ] Mobile form usability
- [ ] Form validation present
- [ ] Thank you page / confirmation exists

#### 4B. CTAs & Conversion Points
```bash
# Find all buttons and CTAs
PATH="$HOME/.bun/bin:$PATH" $B js "[...document.querySelectorAll('button, a.btn, a.button, [class*=\"cta\"], [class*=\"btn\"]')].map(el => el.textContent.trim().substring(0,50) + ' → ' + (el.href || 'button')).join('\\n')"

# Check phone links
PATH="$HOME/.bun/bin:$PATH" $B js "[...document.querySelectorAll('a[href^=\"tel:\"]')].map(a => a.textContent.trim() + ' → ' + a.href).join('\\n') || 'No phone links'"
```

**Check:**
- [ ] Primary CTA is clear and prominent
- [ ] CTA text is action-oriented (not "Submit" or "Click Here")
- [ ] Phone number is clickable (tel: link)
- [ ] Multiple conversion paths (form, phone, chat)
- [ ] CTAs visible on mobile without scrolling
- [ ] Sticky header/footer with CTA on mobile

#### 4C. Trust Signals
```bash
PATH="$HOME/.bun/bin:$PATH" $B js "document.body.innerText"
```

Look for in page text:
- [ ] Credentials/certifications
- [ ] Insurance accepted list
- [ ] Testimonials/reviews
- [ ] Awards/recognition
- [ ] Years of experience
- [ ] Team/provider bios
- [ ] HIPAA compliance mention
- [ ] Accreditation badges

#### 4D. Chat & Real-Time Support
```bash
# Already identified in Phase 3 — cross-reference here
# Verify the chat widget actually loads and is functional
PATH="$HOME/.bun/bin:$PATH" $B js "document.querySelectorAll('[class*=\"chat\"], [id*=\"chat\"], [class*=\"widget\"], [data-chat]').length"
PATH="$HOME/.bun/bin:$PATH" $B screenshot /tmp/site-review-chat.png
```

**Check:**
- [ ] Chat widget present and visible
- [ ] Chat is accessible on mobile
- [ ] Chat doesn't block important content

### Phase 5: Healthcare-Specific Checks (if applicable)

- [ ] HIPAA compliance mentioned
- [ ] Insurance/payer information clear
- [ ] Service area clearly defined
- [ ] Intake process explained
- [ ] Emergency/crisis resources provided (if behavioral health)
- [ ] Provider credentials displayed
- [ ] Telehealth vs in-person options clear
- [ ] Appointment scheduling available

### Phase 6: Internal Fact-Check & Validation

**This is the most important phase. Run it BEFORE delivering the report.**

For every finding from Phases 1-5, apply this validation:

#### Validation Matrix

| Finding Type | Verification Method 1 | Verification Method 2 |
|-------------|----------------------|----------------------|
| "Missing element" | `snapshot -i` interactive scan | `js` DOM query |
| "No third-party tool" | Script source inventory | Global variable check |
| "Broken/missing link" | `goto` the URL directly | Check response status |
| "No schema/markup" | `js` query for ld+json | HTML source search |
| "Phone mismatch" | Check for call tracking scripts | Compare with footer |
| "Form issue" | `snapshot -i` for all fields | `js` form field query |
| "Missing analytics" | Check for tag managers | Check global variables |
| "Content issue" | Re-read full text | Check multiple pages |

#### Fact-Check Process

For each finding in your draft report:

1. **State the finding** clearly
2. **Method 1**: How you initially found it
3. **Method 2**: How you verified it (must be different from Method 1)
4. **Confidence**: HIGH (verified 2+ ways) / MEDIUM (verified 1 way, plausible) / LOW (single signal, could be wrong)
5. **If confidence is LOW**: Run additional checks or mark as "Needs manual verification"

**Rules:**
- NEVER report LOW confidence findings as definitive problems
- ALWAYS note when something loads asynchronously (chat, forms, tracking)
- ALWAYS check for tag managers before claiming "no analytics"
- ALWAYS check for call tracking before flagging phone number mismatches
- ALWAYS use `snapshot -i` before claiming forms are missing fields
- If uncertain, say "Could not confirm" rather than making a false claim

### Phase 7: Deliver the Report

```
============================================
  SITE REVIEW — [URL]
  [Date]
============================================

TOOLS & PLATFORM DETECTED
---------------------------
CMS: [platform]
Analytics: [tools]
Chat: [tool or None]
Call Tracking: [tool or None]
A/B Testing: [tool or None]
CRM: [tool or None]
Other: [list]

TECHNICAL SEO
--------------
Score: X/10

[Findings with confidence level for each]

TACTICAL SEO
--------------
Score: X/10

[Findings with confidence level for each]

INTAKE & CONVERSION
---------------------
Score: X/10

[Findings with confidence level for each]

TRUST & CREDIBILITY
---------------------
Score: X/10

[Findings with confidence level for each]

TOP PRIORITIES (ranked by impact)
===================================
1. [Highest impact fix] — effort: [S/M/L]
2. [Second priority] — effort: [S/M/L]
3. [Third priority] — effort: [S/M/L]
...

ITEMS NEEDING MANUAL VERIFICATION
------------------------------------
[Any findings that could not be fully verified automatically]
```

## Error Handling

- If browse tool fails: note which checks couldn't be performed
- If a page requires authentication: note and skip those checks
- If JavaScript is disabled or fails: fall back to HTML source analysis
- Never skip the fact-check phase, even if browse has issues
- If the site blocks automated access: note it and provide recommendations based on what was accessible

## Tone

- Objective and data-driven
- No speculation presented as fact
- Confidence levels on every finding
- Actionable recommendations with effort estimates
- Honest about limitations of automated review
