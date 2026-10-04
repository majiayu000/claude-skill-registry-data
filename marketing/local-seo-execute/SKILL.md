---
name: local-seo-execute
description: >
  Autonomously execute SEO work for a local business client following proven local SEO guidelines.
  Use when user says "zrob SEO dla [klient]", "zacznij z [klient]", "uruchom SEO", "zrob mi SEO",
  or provides client details and asks to start SEO work. Produces: on-page fixes, service pages,
  schema markup, and a prioritized human TODO list.
allowed-tools: Bash, Read, Write, Edit, WebSearch, WebFetch
---

### Goal
Do the maximum amount of SEO work autonomously. Return what's done + a prioritized TODO list for the human.

### Required inputs -- ask before starting if missing

**Minimum required:**
- Business name
- City / primary market
- Primary service category
- Website URL

**Important (ask if not provided):**
- Phone number (needed for all pages -- flag as MISSING if not given)
- 1-2 sentences about the business (how long operating, any specialties)
- CMS: WordPress / custom / no website

**Optional but valuable:**
- GSC access (flag as missing -- explain what we lose without it)
- Pricing for main services (needed for realistic service pages)
- Additional cities/neighborhoods served

If critical info is missing, add it to the human TODO list with explanation. Never silently skip it.

### Phase 1 -- Audit and Plan (~$0.10 DataForSEO)

1. Check current rankings: DataForSEO SERP for 5-10 main keywords
2. Fetch homepage: check title tag, H1, phone visibility, address in footer
3. Check top 3 map pack competitors (review count, velocity, category)
4. Build Core 30 list: one page per service + location combinations needed
5. Identify which pages exist vs which need to be created

### Phase 2 -- On-page fixes (do autonomously)

For each fix, note what was changed and why.

**2.1 Title tag**
Formula: `[GBP Primary Category] in [City]`
Keyword FIRST. Not brand name first. Not "Best" or "Top".
Example: "HVAC Repair in Dallas" not "Smith's Heating - HVAC Services Dallas TX"

**2.2 H1**
Must echo the title tag topic. Service + city.

**2.3 Phone above fold**
Phone number must be visible without scrolling. On mobile must be a tap-to-call link.
If phone number not provided: add to TODO [INFO NEEDED].

**2.4 Address in footer**
NAP (Name, Address, Phone) must be in the footer of every page.

**2.5 LocalBusiness schema on homepage**
Use specific @type (e.g. Plumber, HVACContractor, Roofer).
Do NOT add AggregateRating unless using verified third-party data.

**2.6 Service schema on each service page**
Add Service schema with name, description, areaServed.

**2.7 GBP link target**
ONLY applies when client has multiple GBPs: each GBP should link to its specific location page.
Single GBP = homepage link is fine.

### Phase 3 -- Service pages (do autonomously)

For each missing page from Core 30:

**Research process (do all three before writing):**
1. WebSearch "[service] [city]" -- find local pricing, local regulations, local facts
2. WebSearch "site:reddit.com [service] [city]" or "[service] questions" -- find real customer questions
3. Check top 2 competitors' pages for the same keyword -- what topics do they cover?

**Page structure:**
- H1: [Service] in [City]
- First 100 words: confirm service + city + phone number
- 800-1200 words total
- Include: local pricing range (research this), local-specific facts, process explanation
- FAQ section (minimum 4 questions) -- AI crawlers extract from these
- Embed Google Maps (note in page for human to add iframe)
- Address in footer
- Internal links to related service pages

**Content rules:**
- Real local data beats generic content
- Include specific pricing ranges based on research (not made up)
- No duplicate content -- each city page must have unique local information
- Do NOT use collapsed accordions for important content (Googlebot cannot click)

**Save each page to:** `seo-pages/[client-slug]/[page-slug].md`

### Phase 4 -- Save content

Save all written pages to `seo-pages/[client-name-slug]/` with frontmatter:
```
---
title: [H1]
keyword: [target keyword]
url-slug: [recommended URL]
status: ready-to-publish
---
```

Also save `seo-pages/[client-name-slug]/index.md` with summary of all pages created.

### Phase 5 -- Human TODO list

Format as prioritized list. Most important first. Be specific.

```
HUMAN TODO -- [Business Name]
(do in this order)

[GBP] Check/set primary category to: [recommended category]
[GBP] Respond to all existing reviews with keywords naturally embedded
[GBP] Link to: [specific page URL]
[REVIEWS] Target: X reviews/month (currently ~Y, top competitor has ~Z at ~W/month)
  - Review quality matters more than count: ask customers to mention the specific service + city
[CITATIONS] Add business to these directories:
  Priority 1: Google Business Profile (verify), Yelp, BBB
  Priority 2: HomeAdvisor, Angi, Houzz, Thumbtack
  Priority 3: Local chamber of commerce, local business directories for [city]
[GSC] Grant access to Google Search Console -- we need this to find keyword gaps
  URL: search.google.com/search-console
[INFO NEEDED] Phone number -- required for all pages, above fold placement
[INFO NEEDED] Pricing for [service] -- needed for service pages to be specific
[INFO NEEDED] What neighborhoods/cities do you serve besides [City]?
[CONTENT] Publish X service pages (saved to seo-pages/[client]/)
[CONTENT] Add Google Maps iframe to each location page
```

### Proactive flags

Always flag these proactively even if user didn't ask:
- Missing phone number: "Phone number is critical -- it's a conversion factor AND ranking signal"
- Missing GSC access: "Without GSC we can't find which keywords Google already ranks the site for"
- Review velocity below 3/month: "Current velocity will lose ground to competitors -- need active review strategy"
- Review gap larger than 50: "Will take significant time to close -- be realistic with client about timeline"
- Competitor has active SEO agency: "Market has professional competition -- results will take longer"

### Key principles (non-negotiable)

These come from analysis of 843 tweets from @theseoguy_ -- proven local SEO insights:
1. GBP is the #1 asset, not the website
2. Category > everything else on GBP
3. Review velocity > review count
4. Review quality > review velocity (10+ words, photos, keywords + city in text)
5. Title tag: keyword first, not brand name
6. One location page per city -- never one page for all cities
7. No duplicate city pages -- each needs unique local content
8. FAQ sections are critical for AI crawler indexing in 2026
9. Domain Authority is irrelevant for map pack
10. Goal completion (conversions) is itself a ranking signal
