---
name: seo-audit
description: When the user wants to audit, review, or diagnose SEO issues on their site. Also use when the user mentions "SEO audit," "technical SEO," "why am I not ranking," "SEO issues," "on-page SEO," "meta tags review," or "SEO health check." For building pages at scale to target keywords, see programmatic-seo. For adding structured data, see schema-markup.
metadata:
  version: 1.0.0
---

# SEO Audit

You are an expert in search engine optimization. Your goal is to identify SEO issues and provide actionable recommendations to improve organic search performance.

## Initial Assessment

**Check for product marketing context first:**
If `.claude/product-marketing-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Before auditing, understand:

1. **Site Context**
   - What type of site? (SaaS, e-commerce, blog, etc.)
   - What's the primary business goal for SEO?
   - What keywords/topics are priorities?

2. **Current State**
   - Any known issues or concerns?
   - Current organic traffic level?
   - Recent changes or migrations?

3. **Scope**
   - Full site audit or specific pages?
   - Technical + on-page, or one focus area?
   - Access to Search Console / analytics?

### ⚠️ GSC Access: Required for Complete Audit

**Always ask for Google Search Console access before starting.**

Without GSC you cannot audit:
- What queries actually drive impressions/clicks
- Which pages are indexed (vs. what you assume from sitemaps)
- Crawl errors and coverage issues
- Manual actions
- Core Web Vitals field data

**If GSC access is unavailable:** state this explicitly at the top of the report — *"This audit is based on frontend crawl analysis only. Without Google Search Console access, indexation status, crawl errors, and actual traffic data cannot be verified."* Do not present a partial audit as complete.

### ⚠️ No Speculation Rule

**Only report findings you can verify with actual data.**

- ❌ "Internal links are likely siloed" → not a finding
- ✅ "We crawled 97 blog posts — 64 have zero internal links to service pages" → finding
- ❌ "This may cause issues" → not actionable
- ✅ "Page X returns 404 — confirmed via direct fetch and navigation click" → finding

If you cannot verify something with data, either skip it or explicitly flag it as "unverified — requires Screaming Frog / GSC to confirm."

---

## Audit Framework

### ⚠️ Important: Schema Markup Detection Limitation

**`web_fetch` and `curl` cannot reliably detect structured data / schema markup.**

Many CMS plugins (AIOSEO, Yoast, RankMath) inject JSON-LD via client-side JavaScript — it won't appear in static HTML or `web_fetch` output (which strips `<script>` tags during conversion).

**To accurately check for schema markup, use one of these methods:**
1. **Browser tool** — render the page and run: `document.querySelectorAll('script[type="application/ld+json"]')`
2. **Google Rich Results Test** — https://search.google.com/test/rich-results
3. **Screaming Frog export** — if the client provides one, use it (SF renders JavaScript)

**Never report "no schema found" based solely on `web_fetch` or `curl`.** This has led to false audit findings in production.

### ⚠️ Schema Markup: Rules That Change Over Time

Always apply schema based on **current Google guidelines**, not outdated SEO playbooks.

**AggregateRating — critical rule:**
Google does NOT allow `AggregateRating` markup for self-collected testimonials hosted on your own site. Using it this way violates structured data guidelines and can trigger a rich result rejection or manual action. AggregateRating is only valid when pulling from a recognized third-party review platform (Google Reviews via Places API, Trustpilot, etc.). Before recommending it, confirm the site has a legitimate source.

**FAQPage schema — deprecated for most sites (as of September 2023):**
Google removed FAQ rich results for most websites. They now only show for official government and health websites. **Do not recommend FAQPage schema to local businesses, SaaS sites, or e-commerce** — it will produce no rich results. This is a common outdated recommendation that wastes developer time.

**HowTo schema — also restricted:**
HowTo rich results are similarly limited. Check current Google documentation before recommending.

**Always verify schema guidelines are current before recommending any schema type.** Google changes eligibility regularly.

### Priority Order
1. **Crawlability & Indexation** (can Google find and index it?)
2. **Technical Foundations** (is the site fast and functional?)
3. **On-Page Optimization** (is content optimized?)
4. **Content Quality** (does it deserve to rank?)
5. **Authority & Links** (does it have credibility?)

---

## Technical SEO Audit

### Crawlability

**Robots.txt**
- Check for unintentional blocks
- Verify important pages allowed
- Check sitemap reference

**XML Sitemap**
- Exists and accessible
- Submitted to Search Console
- Contains only canonical, indexable URLs
- Updated regularly
- Proper formatting

**Site Architecture**
- Important pages within 3 clicks of homepage
- Logical hierarchy
- Internal linking structure
- No orphan pages

**Crawl Budget Issues** (for large sites)
- Parameterized URLs under control
- Faceted navigation handled properly
- Infinite scroll with pagination fallback
- Session IDs not in URLs

### Indexation

**Index Status**
- site:domain.com check
- Search Console coverage report
- Compare indexed vs. expected

**Indexation Issues**
- Noindex tags on important pages
- Canonicals pointing wrong direction
- Redirect chains/loops
- Soft 404s
- Duplicate content without canonicals

**Canonicalization**
- All pages have canonical tags
- Self-referencing canonicals on unique pages
- HTTP → HTTPS canonicals
- www vs. non-www consistency
- Trailing slash consistency

### Site Speed & Core Web Vitals

**⚠️ You must fetch and report actual scores — never tell the client to "run PageSpeed themselves."**

Fetch PageSpeed Insights API for the homepage and at least one key landing page:
`https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://example.com&strategy=mobile`

Or use WebFetch on: `https://pagespeed.web.dev/report?url=https://example.com`

**Report actual numbers:**

| Metric | Target | Actual (Mobile) | Actual (Desktop) |
|---|---|---|---|
| LCP | < 2.5s | ? | ? |
| INP | < 200ms | ? | ? |
| CLS | < 0.1 | ? | ? |
| TTFB | < 0.8s | ? | ? |
| Performance Score | > 70 | ? | ? |

**If you cannot fetch scores:** state this explicitly. Do not omit CWV or suggest the client checks it themselves.

**Speed Factors**
- Server response time (TTFB)
- Image optimization (especially hero/gallery images on visual-heavy sites)
- JavaScript execution
- CSS delivery
- Caching headers
- CDN usage
- Font loading

### Mobile-Friendliness

- Responsive design (not separate m. site)
- Tap target sizes
- Viewport configured
- No horizontal scroll
- Same content as desktop
- Mobile-first indexing readiness

### Security & HTTPS

- HTTPS across entire site
- Valid SSL certificate
- No mixed content
- HTTP → HTTPS redirects
- HSTS header (bonus)

### URL Structure

- Readable, descriptive URLs
- Keywords in URLs where natural
- Consistent structure
- No unnecessary parameters
- Lowercase and hyphen-separated

---

## On-Page SEO Audit

### Title Tags

**Check for:**
- Unique titles for each page
- Primary keyword near beginning
- 50-60 characters (visible in SERP)
- Compelling and click-worthy
- Brand name placement (end, usually)

**Common issues:**
- Duplicate titles
- Too long (truncated)
- Too short (wasted opportunity)
- Keyword stuffing
- Missing entirely

### Meta Descriptions

**Check for:**
- Unique descriptions per page
- 150-160 characters
- Includes primary keyword
- Clear value proposition
- Call to action

**Common issues:**
- Duplicate descriptions
- Auto-generated garbage
- Too long/short
- No compelling reason to click

### Heading Structure

**Check for:**
- One H1 per page
- H1 contains primary keyword
- Logical hierarchy (H1 → H2 → H3)
- Headings describe content
- Not just for styling

**Common issues:**
- Multiple H1s
- Skip levels (H1 → H3)
- Headings used for styling only
- No H1 on page

### Content Optimization

**Primary Page Content**
- Keyword in first 100 words
- Related keywords naturally used
- Sufficient depth/length for topic
- Answers search intent
- Better than competitors

**Thin Content Issues**
- Pages with little unique content
- Tag/category pages with no value
- Doorway pages
- Duplicate or near-duplicate content

### Image Optimization

**Check for:**
- Descriptive file names
- Alt text on all images
- Alt text describes image
- Compressed file sizes
- Modern formats (WebP)
- Lazy loading implemented
- Responsive images

### Internal Linking

**Check for:**
- Important pages well-linked
- Descriptive anchor text
- Logical link relationships
- No broken internal links
- Reasonable link count per page

**Common issues:**
- Orphan pages (no internal links)
- Over-optimized anchor text
- Important pages buried
- Excessive footer/sidebar links

### Keyword Targeting

**Per Page**
- Clear primary keyword target
- Title, H1, URL aligned
- Content satisfies search intent
- Not competing with other pages (cannibalization)

**Site-Wide**
- Keyword mapping document
- No major gaps in coverage
- No keyword cannibalization
- Logical topical clusters

---

## Content Quality Assessment

### E-E-A-T Signals

**⚠️ E-E-A-T scope matters — apply correctly based on site type:**

- **YMYL content** (health, finance, legal, safety) → E-E-A-T is a critical ranking factor. Author credentials, sourcing, and medical/legal review are essential.
- **Local service businesses** (contractors, plumbers, restaurants) → E-E-A-T matters at the business level (credentials, awards, years in business), NOT at the blog post author level. Google does not care about author bios on a renovation company's blog.
- **SaaS/content sites** → Author E-E-A-T matters for product reviews and advice content; less so for feature pages.

**Experience**
- First-hand experience demonstrated
- Original insights/data (proprietary research, real project examples)
- Real case studies with outcomes

**Expertise**
- Accurate, detailed information
- Industry certifications and credentials visible on site (not just mentioned once)
- For YMYL: author credentials with sourcing

**Authoritativeness**
- Recognized in the industry (awards, press, associations)
- Cited by others / media coverage
- Active on relevant platforms (for local: GBP, HomeStars, Houzz)

**Trustworthiness**
- Accurate information
- Transparent about business (team, address, history)
- Contact information available
- Privacy policy, terms
- Secure site (HTTPS)
- Third-party reviews (not just self-collected testimonials)

### Content Depth

- Comprehensive coverage of topic
- Answers follow-up questions
- Better than top-ranking competitors
- Updated and current

---

## Backlinks & Authority

### Quality Over Quantity — The Core Rule

**3-5 backlinks from DR70+ niche-relevant sites outperform 50 backlinks from DR20 generic sites.** This is consistently confirmed across case studies. When auditing a site's backlink profile, count quality links separately from total links — a site with 3 strong links may be in better shape than a site with 80 weak ones.

**What makes a link "quality":**
- Domain Rating 70+ with actual organic traffic (not just a high DR score)
- Site is topically relevant to the client's niche — a DR81 home improvement site is worth more for a plumber than a DR81 finance site
- The linking page has content related to the client's services
- Real business with real audience, not a link farm

**Niche relevance > raw Domain Rating.** Google increasingly evaluates topical authority. A DR60 link from a site that covers plumbing, HVAC, and home services is more valuable for a plumber than a DR80 link from a generic business directory. Always check what the linking domain actually covers.

### For Local Service Businesses

For the map pack, backlinks have limited direct impact (see: Domain Authority Is Irrelevant for Map Pack below). But for organic rankings below the pack, focus on:

- **Local citations first** — NAP consistency across HomeStars, Houzz, Yellow Pages, BBB, industry associations. These are not strong links but foundational for trust signals.
- **Local press and community links** — a mention in a local news article or neighborhood blog is worth more than 10 generic directory submissions
- **Industry association pages** — HVAC associations, contractor licensing boards, trade organizations often link to members
- **Supplier/manufacturer pages** — if a plumber is a certified installer for a brand, that brand's "find an installer" page is a relevant, authoritative backlink

### Red Flags in Backlink Profile

- Sudden spike in referring domains (could signal spam attack or PBN)
- High % of exact-match anchor text (over-optimization risk)
- Links from unrelated foreign language sites
- Links from domains with no organic traffic of their own

---

## Common Issues by Site Type

### SaaS/Product Sites
- Product pages lack content depth
- Blog not integrated with product pages
- Missing comparison/alternative pages
- Feature pages thin on content
- No glossary/educational content

### E-commerce
- Thin category pages
- Duplicate product descriptions
- Missing product schema
- Faceted navigation creating duplicates
- Out-of-stock pages mishandled

### Content/Blog Sites
- Outdated content not refreshed
- Keyword cannibalization
- No topical clustering
- Poor internal linking
- Missing author pages

### Local Business

**For local businesses, Google Business Profile is the #1 ranking factor for local pack — audit it first.**

GBP Audit Checklist:
- Primary and secondary categories correct?
- Service area configured (vs. storefront)?
- All services listed with descriptions?
- Photos: quantity, quality, recency (Google favors active profiles)
- Review count + average rating vs. top 3 competitors
- Review velocity (last 30/90 days) — stagnant reviews hurt rankings
- Q&A section populated with common questions?
- Posts active (last 30 days)?
- NAP on GBP matches site exactly

Website Local SEO:
- Inconsistent NAP across pages (name, address, phone must be identical everywhere)
- Missing or incorrect LocalBusiness schema
- Missing location/service area pages
- No local content (neighborhood-specific projects, local permits, local testimonials)
- Citation consistency on HomeStars, Houzz, Yellow Pages, industry directories

---

### Local SEO: Advanced Frameworks

#### Core 30 — Mirror GBP in site structure

The most impactful local SEO move: build one dedicated page for every service and category listed on the GBP, structured to mirror it exactly. Homepage links to category pages; category pages link to individual service pages. This works because Google's local algorithm uses the website as a corroboration layer for the GBP entity — when the two structures match, Google has no ambiguity about what the business does and what it should rank for.

Example: a plumber with 4 GBP categories (Plumber, Drain Cleaning, Water Heater, Emergency) and 8 services under those categories = 12 targeted pages minimum. "Core 30" is the benchmark target; start there before any other content work.

#### Entity Test — free alternative to keyword research for local

To find which services need separate pages, compare map pack results for two similar queries (e.g. "plumber houston" vs. "water heater installation houston"). If different businesses appear, Google treats them as separate service entities requiring separate pages. If the same businesses appear, Google sees them as the same intent and one page can cover both. Free, takes 2 minutes per service pair, more practical than keyword tools for local.

#### Title Tag Formula for Local

Homepage title tag: `[GBP primary category] + [city]`

- Written for Google, not humans
- Not the brand name, not "Home", not "Best", not generic
- Matches the GBP primary category exactly
- Example: "General Contractor Toronto" not "Norseman Construction | Custom Homes"

Most local business homepages have just the brand name or "Home" in the title — this wastes the highest-signal on-page element available.

#### Rank Map First — before any content work

Before building pages, run a rank map (169-point grid search across the service area). Interpret results:

- **Most areas red** (not ranking) → needs topical relevance; build Core 30 pages first
- **Positions 4–6 in specific zones** → already has topical relevance; needs geographic relevance pages for those zones

Never start content without this map — it tells you which problem you're solving.

#### Geographic Relevance Pages

After Core 30 is established, look at the rank map and build `[service] + [neighborhood/landmark]` pages for zones sitting at positions 4–6. Moving from 4→3 is far easier than 19→3. Target specific landmarks (parks, shopping centres, intersections, nearby streets) with local references — permit processes, local building codes, driving routes technicians use, common issues in older vs. newer construction in that area.

#### GSC Modifier Mining

Export GSC queries-per-URL using "Search Analytics for Sheets" (free add-on). Find pages where Google serves queries containing terms not present on the page. Adding those terms to the page confirms the algorithm's correct inference — this is not keyword stuffing, it's corroboration. Example: Google serves your water heater page for "lead pipe replacement" → add "lead" to the page. Moves pages from positions 5–10 into top 3.

#### Domain Authority Is Irrelevant for Map Pack

For the local 3-pack, proximity + relevance + GBP trust signals dominate. A DA 25 local business regularly outranks a DA 80 national directory. Do not chase DA for map pack rankings. Backlinks matter for organic results below the pack, not for the pack itself.

#### Goal Completion as the Ranking Signal

Google's local ranking signal is not time on page or bounce rate — it's whether the user stopped searching after landing on the page. For local service businesses: did they call, get directions, or find what they needed without returning to Google? This means:

- Phone number above the fold, not buried
- Service + city in the first 100 words
- Social proof near the top, not just the bottom
- Company history and awards below the fold

Pages that achieve goal completion outrank better-designed pages that don't.

#### Collapsed Accordions — Hidden from Googlebot

Googlebot renders pages in mobile Chrome but cannot click to expand collapsed/accordion elements. Content inside dropdowns gets low crawl priority even if the page is otherwise well-optimised. Make all content visible on first load for pages you want to rank. Accordions are fine for UI that doesn't need to rank (support FAQs, legal copy), but not for service descriptions or local content.

---

## Output Format

### Audit Report Structure

**Executive Summary**
- Overall health assessment
- Top 3-5 priority issues
- Quick wins identified

**Technical SEO Findings**
For each issue:
- **Issue**: What's wrong
- **Impact**: SEO impact (High/Medium/Low)
- **Evidence**: How you found it
- **Fix**: Specific recommendation
- **Priority**: 1-5 or High/Medium/Low

**On-Page SEO Findings**
Same format as above

**Content Findings**
Same format as above

**Competitor Analysis** (mandatory — do not skip)
- Who ranks #1-3 for the client's primary keywords?
- Fetch and compare their: title tags, content depth, backlink count (if tools available), GBP presence
- What do competitors have that the client doesn't?
- This context is what transforms generic recommendations into actionable priorities

**Keyword Cannibalization Check**
- When the site has location pages + a blog + service pages, identify which URL Google should rank for each key query
- Flag conflicts: e.g., "/toronto-renovation-company/" vs. a blog post "/toronto-renovation-experts/" — which one is Google actually indexing for that term?
- Without this check, optimizing one page may undermine another

**Prioritized Action Plan**
1. Critical fixes (blocking indexation/ranking)
2. High-impact improvements
3. Quick wins (easy, immediate benefit)
4. Long-term recommendations

---

## References

- [AI Writing Detection](references/ai-writing-detection.md): Common AI writing patterns to avoid (em dashes, overused phrases, filler words)
- For AI search optimization (AEO, GEO, LLMO, AI Overviews), see the **ai-seo** skill

---

## Tools Referenced

**Free Tools**
- Google Search Console (essential)
- Google PageSpeed Insights
- Bing Webmaster Tools
- Rich Results Test (**use this for schema validation — it renders JavaScript**)
- Mobile-Friendly Test
- Schema Validator

> **Note on schema detection:** `web_fetch` strips `<script>` tags (including JSON-LD) and cannot detect JS-injected schema. Always use the browser tool, Rich Results Test, or Screaming Frog for schema checks. See the warning at the top of the Audit Framework section.

**Paid Tools** (if available)
- Screaming Frog
- Ahrefs / Semrush
- Sitebulb
- ContentKing

---

## Task-Specific Questions

1. What pages/keywords matter most?
2. Do you have Search Console access?
3. Any recent changes or migrations?
4. Who are your top organic competitors?
5. What's your current organic traffic baseline?

---

## Related Skills

- **ai-seo**: For optimizing content for AI search engines (AEO, GEO, LLMO)
- **programmatic-seo**: For building SEO pages at scale
- **schema-markup**: For implementing structured data
- **page-cro**: For optimizing pages for conversion (not just ranking)
- **analytics-tracking**: For measuring SEO performance
