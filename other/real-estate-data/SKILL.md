---
name: real-estate-data
description: "Extract real estate listing data from online sources — handle anti-bot protection on major portals, use alternative aggregators and builder direct websites, and structure property data for analysis."
version: 1.2.0
author: Hermes Agent
license: BSD-3-Clause
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [market-lead, property-listings, home-search, data-extraction, zillow, new-construction]
    triggers: [market-lead, zillow, homes-for-sale, property-listings, home-search, new-construction, realtor, redfin, home-builder, mls]
    related_skills: [web-scraping-scrapling, gpt-researcher]
---

# Real Estate Data Extraction

A repeatable workflow for extracting real estate listing data from online sources. This skill covers finding homes for sale, new construction, and recently built properties when major portals have anti-bot protection.

## Anti-Bot Protection Status on Real Estate Sites

| Site | Protection | Accessible? | Notes |
|------|-----------|-------------|-------|
| **Zillow** | PerimeterX (px-captcha) | ❌ Blocked | Press-&-Hold human verification, all endpoints protected |
| **Realtor.com** | PerimeterX-like (KPSDK) | ❌ Blocked | Request cannot be processed error |
| **Redfin** | Moderate | ⚠️ Partial / ✅ Community pages | Builder filters limited but community detail pages (redfin.com/.../community/...) load reliably with address, phone, hours, builder bio, and nearby community recommendations. The "All New Homes" tab often triggers rate limiting. Extract what's visible on the community tab before navigating deeper. Note: CloudFront blocks may occur — retry in a fresh isolated context if 403'd. |
| **Homes.com** | Light | ✅ Works | Direct URL access for community pages |
| **NewHomeSource** | PerimeterX | ❌ Blocked | Same px-captcha as Zillow |
| **Adams Homes** (direct) | None | ✅ Works | Full listing data available |
| **Jome.com** | None | ✅ Works | Excellent new construction aggregator; builder filter requires UI interaction (click "Builders" button on page) — URL param filtering redirects to unfiltered results |
| **DR Horton** (direct) | AppDynamics + Cloudflare Turnstile | ❌ Blocked | All API endpoints (/api/search/*) return 404 for automated requests. Division pages redirect to main Florida page. Use aggregators (Jome, Redfin community carousels) to discover communities. Communities found: Avalon (Lehigh Acres, FL 33936, from $264,990). |
| **Lennar** (direct) | Cloudflare Turnstile | ❌ Blocked | Aggressive protection on all pages. Use aggregators instead. |
| **Builder websites** (no-bot) | None | ✅ Usually works | Best source for accurate pricing/availability. Check for Squarespace, custom WordPress, or static HTML sites. |

## Workflow: Extract Real Estate Listings

### Step 1: Discover Sources via DuckDuckGo (not Google)

When Zillow is blocked, search DuckDuckGo (lite mode works best) to find listing sources:

```
https://lite.duckduckgo.com/lite/?q="Builder Name" + "City" + "state" + price + beds + sqft
```

Alternatively use the Zillow community pages / new construction pages if accessible:
```
https://www.zillow.com/lehigh-acres-fl/new-construction/
https://www.zillow.com/community/<community-name>/<id>_plid/
```

### Step 2: Prioritize Direct Builder Websites

Builder websites are the most reliable source. Key data fields to extract:

- **Address** (street, city, state, ZIP)
- **Price** (current asking price, note any price cuts/incentives)
- **Square footage** (heated/cooled, total)
- **Beds / Baths** (full + half)
- **Floor plan name/number** (e.g., "1540", "2265")
- **Lot size** (acres or sq ft — often missing from listing pages)
- **Status** (Move-In Ready, Under Construction, To Be Built)
- **Community name** (important — builders often have multiple communities in one area)
- **Garage** (car count)
- **Stories** (1 or 2 story)
- **Incentives** (price cuts, flex cash, below-market interest rates)
- **MLS#** (for cross-referencing)
- **Features** (upgrades, appliances, flooring, lanai/patio)
- **School district / assigned schools**
- **Coordinates** (for Google Maps, from VIEW MAP links)

### Step 3: Use Aggregator Sites for Cross-Reference

| Source | Best For | Access |
|--------|----------|--------|
| **Jome.com** (jome.com) | New construction communities from all builders | ✅ Reliable |
| **Homes.com** (homes.com) | New home plans and communities | ✅ Usually works |
| **Lennar.com** (lennar.com) | Direct builder — new construction communities | ❌ Blocked by Cloudflare Turnstile | Same challenge as PerimeterX; use DuckDuckGo search to find aggregator pages (Jome, NewHomeSource, Redfin community pages) that mirror the data |
| **DR Horton** (drhorton.com) | Direct builder — all divisions | ❌ AppDynamics + Cloudflare Turnstile | API endpoints return 404; division pages redirect. Discover communities through Redfin "Recommended nearby communities" carousels or Jome.com. Common community patterns: Avalon |
| **NewHomeSource** (newhomesource.com) | Community-level data | ❌ Blocked |
| **Redfin** (redfin.com) | Filter by builder | ⚠️ Partial |

### Step 4: Extract Data Using Browser Snapshots

Use the Chrome DevTools MCP to navigate to listings and take snapshots:

1. **Listing overview page** — use `mcp_chrome_devtools_mcp_navigate_page` then `mcp_chrome_devtools_mcp_take_snapshot`
2. **Detail page** — navigate to each individual listing for full specs
3. **Look for these UI patterns:**
   - Card-based listings: price, beds, baths, sq ft, floorplan name, community
   - Detail pages: features, lot details, schools, incentives, mortgage calculator
   - Map links: often contain lat/lng coordinates

### Step 4a: Squarespace Builder Sites — Specialized Approach

Many home builders use Squarespace (identifiable by `squarespace.com` in static context, `squarespace-cdn.com` image URLs, and JSON payloads like `SQUARESPACE_CONTEXT`). These sites are heavily JS-rendered — curl alone can't extract listing data.

**Identification:**
- Page source contains `squarespace.com` references, `SQUARESPACE_CONTEXT` JSON in the `<script>` tags
- Images served from `images.squarespace-cdn.com`
- `<!-- This is Squarespace. -->` HTML comment at the top
- Pages are "collections" with IDs like `collection-6487447651321f457173a93c`

**Sitemap Discovery (critical first step):**
Squarespace sites publish a `sitemap.xml` that catalogs every listing page. Use it to find all listing URLs and glean preview data:

```bash
# Extract all listing URLs and their image captions (which often contain price & specs)
curl -sL "https://www.builder-site.com/sitemap.xml" | grep -oP "<loc>[^<]+</loc>" | grep "/listings/" | sed 's|<loc>||;s|</loc>||'
# Image captions in sitemap often contain: address, price, sq ft, beds, baths
grep -oP '(?:image:caption|image:title)[^<]*<[^>]*>[^<]+' sitemap_content
```

**Extracting Data from Rendered Pages:**
When `browser_navigate` fails (Chrome auto-launch issues), use the Chrome DevTools MCP directly:

1. Open the page: `mcp_chrome_devtools_mcp_new_page(url="<listing-url>")`  
2. Select the page: `mcp_chrome_devtools_mcp_select_page(pageId=N)`
3. Take a verbose snapshot of the accessibility tree: `mcp_chrome_devtools_mcp_take_snapshot(verbose=true)`
4. The accessibility tree contains all listing cards as structured elements with headings, paragraphs, and text — parse these for:
   - `heading` elements → street address
   - `paragraph` elements → specs line ("1426 SQ FT | 4 BED | 2 BATH") and price ("$303,990")
5. Individual listing cards are wrapped in `<article>` elements — one per home

**Data in the Accessibility Tree (snapshot output pattern):**
```
uid=138_135 heading "3005 8th St SW"                       ← address
uid=138_141 StaticText "1426 SQ FT | 4 BED | 2 BATH"       ← specs
uid=138_143 StaticText "$303,990"                           ← price
```

**Category Page URLs (faster than crawling each listing):**
If the site has listing categories, navigate directly:
```
https://www.builder-site.com/listings/category/Lehigh+Acres
https://www.builder-site.com/listings/category/Cape+Coral
```
Use `mcp_chrome_devtools_mcp_take_snapshot(verbose=true)` on the category page to get all listings at once.

**Pagination Handling:**
Squarespace listing pages use offset-based pagination. Look for "Older Posts" / "Newer Posts" nav links in the snapshot:
1. After taking the first-page snapshot, find the "Older Posts" link
2. Click it with `mcp_chrome_devtools_mcp_click(uid="<ref>")`
3. The page navigates to `?offset=<timestamp>&category=<name>`
4. Take another snapshot to get the next batch
5. Repeat until no more "Older Posts" links

### Step 4b: Uncover Hidden Listings with Pagination/Reveal Buttons

Many builder sites only show a subset of listings by default and hide the rest behind interaction:

1. **Look for "See More", "Load More", or "Show All" buttons** in the listing area — click them via `mcp_chrome_devtools_mcp_click` to expand the full set.
2. **Scroll down** using `mcp_chrome_devtools_mcp_press_key` with "End" or use `mcp_chrome_devtools_mcp_evaluate_script` with `window.scrollTo(0, document.body.scrollHeight)` to trigger lazy-load.
3. **Re-take the snapshot** after each expansion to capture newly loaded cards.
4. **Cross-reference the builder's master "Available Homes" page** (if it exists, usually at `/available-homes/` or `/homes/`) against the location-specific sub-page. Some builders show pricing and incentives on the master page that the location page omits, and vice versa.
5. **Check for filter/page tabs** — the page may have "Available Homes", "Floor Plans", "Quick Move-In" tabs that each show different subsets. Click each tab and snapshot separately.

### Step 5: Sort and Structure

For a clean deliverable, provide:
1. **Table sorted by price** (low to high)
2. **Table sorted by sq ft** (small to large, or large to small based on user preference)
3. **$/sq ft column** for value comparison
4. **Community groupings** if multiple communities exist
5. **Incentives column** — these are major decision factors

## Data Structure

```json
{
  "address": "2903 E 2ND St, Lehigh Acres, FL 33936",
  "price": 313100,
  "sq_ft": 1540,
  "beds": 3,
  "baths": 2,
  "floorplan": "1540",
  "community": "Lehigh Acres",
  "builder": "Adams Homes",
  "status": "Move-In Ready",
  "garage": 2,
  "stories": 1,
  "incentives": "$30K Price Cut! $20K Flex Cash or 4.99% Rate",
  "mls": "2026004089",
  "features": ["French Doors", "Tile Shower", "Granite Counters", "SS Appliances"],
  "schools": {
    "elementary": {"name": "Tortuga Preserve Elementary", "rating": "1/10"},
    "middle": {"name": "Varsity Lakes Middle School", "rating": "4/10"},
    "high": {"name": "Lehigh Senior High School", "rating": "3/10"}
  }
}
```

## Pitfalls & Troubleshooting

### Zillow always blocked
PerimeterX is a enterprise-grade bot protection. Do NOT retry repeatedly with different headers/user-agents — it won't help and wastes tokens. The protection is URL-level, not request-header level. Use alternative sources instead.

### AppDynamics-heavy builder sites (DR Horton, some large builders)
Large builders like DR Horton use enterprise APM tools (AppDynamics) combined with Cloudflare Turnstile. These sites are completely opaque to automated access — no curl arguments, header combinations, or browser contexts will bypass them. The API layer embeds the monitoring agent into every response. Do NOT waste tool calls trying to hit these API endpoints. Instead:

- Search Redfin or Zillow for builder-specific community pages ("By DR Horton" filter)
- Use Jome.com aggregator — it catches most major builder communities
- Check Redfin carousels on any reachable community page — "Recommended nearby communities" often includes builder communities even when the builder's direct site is blocked
- Try jome.com/community/fl/... URLs for community-specific detail pages

### No lot sizes on listing pages
Many builder websites don't show lot sizes on the main listing cards. Check detail pages, and if still missing, note it explicitly — users familiar with the area may already know typical lot sizes.

### Price/availability staleness
Builder websites are generally the most up-to-date, but always include a "Date sourced" timestamp. Third-party aggregators (Jome, NewHomeSpotter) may be days/weeks behind.

### Multiple communities in one city
Builders often have multiple communities in a single city, even on the same street. Make sure to group listings by community name, as pricing and features may differ.

### Incentives change frequently
Builder incentives (price cuts, rate buydowns, flex cash) change monthly or even weekly. Flag these as "current as of [date]".

### Redfin rate-limits on "All New Homes" tab
Redfin community detail pages load reliably for the initial community tab, but clicking the "All New Homes" tab or navigating to sub-pages may trigger a 403 (CloudFront block). Extract all visible data from the community overview tab first, including the "Recommended nearby communities" carousel which often surfaces related builder communities with prices.

### Builder sub-communities
Major builders like Lennar often sub-divide a single community into price-tiered collections (e.g., "Manor Homes" vs "Executive Homes" in the same master community). These may appear as separate entries on aggregator sites with different starting prices, floor plan ranges, and lot sizes. Always check for sub-community differentiation when multi-sourcing data.

## References

- See `references/adams-homes-lehigh-acres.md` for a worked example of Adams Homes in Lehigh Acres (direct builder site, jome.com cross-ref)
- See `references/coaston-homes-lehigh-acres.md` for a worked example of Coaston Homes in Lehigh Acres (Squarespace builder site, Chrome DevTools MCP extraction)
- See `references/christopher-alan-homes-lehigh-acres.md` for a worked example using a builder's direct website with a "See More" pattern, including cross-reference against the master available-homes page and full 17-listing dataset.
- See `references/lennar-lehigh-acres.md` for a worked example of Lennar Homes in Lehigh Acres (Cloudflare-protected builder site, using Redfin + Jome aggregators).
