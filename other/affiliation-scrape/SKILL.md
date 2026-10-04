---
name: affiliation-scrape
description: Research organizations a leader is affiliated with AND fetch logos for them. Output is a JSON record optimized for rendering a logo strip / social-proof section on the platform site. NOT the same as substrate organizational affiliations — for the substrate's structured org list, use `movement-leader-substrate`.
disable-model-invocation: true
---

> **Scope guard.** This skill exists to populate **logo strips and social-proof sections on the platform site**. Its output (`content-library/affiliations/{slug}.json`) carries logo URLs, logo quality grades, strip groupings, and prominence scores — fields that the [`movement-leader-substrate`](../movement-leader-substrate/SKILL.md) intentionally omits. If you are working on the substrate document, do NOT invoke this skill — substrate's organizational affiliations come from `network/organizations.md` and use a simpler `| Organization | Role | Years | URL |` table without logo metadata.

Scrape and document affiliations for: $ARGUMENTS

$ARGUMENTS should include:
- The person's full name (required): e.g. `"Alan Hirsch"`
- Optionally: their primary domain or website: e.g. `--site alanhirsch.org`
- Optionally: a category filter: `--category publisher,speaking,media`
- Optionally: an output path: `--output content-library/affiliations/alan-hirsch.json`
- Empty — ask the user for the person's name

## Before Starting

1. Confirm you have browser tools available (mcp__chrome-devtools)
2. Check `content-library/affiliations/` for any existing affiliation file for this person
3. If an existing file is found, load it and run in **incremental mode** — add new orgs, don't overwrite confirmed data

## Research Pipeline

### Stage 1 — Seed Searches

Run 6–8 targeted web searches to discover affiliations. Use these query templates (replace `{name}`):

1. `"{name}" publisher site:amazon.com OR site:goodreads.com OR site:booksellers.com`
2. `"{name}" speaking bureau OR keynote speaker`
3. `"{name}" endorsed by OR "foreword by" OR "endorsed by"`
4. `"{name}" conference keynote OR "main stage" OR plenary`
5. `"{name}" podcast interview OR "appeared on" OR "featured in"`
6. `"{name}" denomination OR church OR network OR movement`
7. `"{name}" seminary OR theological school OR university OR faculty`
8. `"{name}" "ministry partner" OR "strategic partner" OR affiliate`
9. `"{name}" site:{their-domain}` — read the About / Speaking / Partners page directly
10. `"{name}" award OR recognition OR honorary`

For each search result, record:
- URL
- Organization name
- Relationship signal (e.g., "keynote speaker," "published by," "board member")
- Confidence level (HIGH / MEDIUM / LOW)

### Stage 2 — Direct Site Crawl

If a personal website is known (or discoverable), navigate to it and read:

1. `/about` or `/about-us` — bio, affiliations mentioned in prose
2. `/speaking` or `/speaking-bureau` — which bureaus are listed
3. `/books` or `/resources` — publishers, endorsers, co-authors
4. `/partners` or `/ministry` — partner organizations
5. `/press` or `/media` — outlets that have featured them
6. Footer — often contains partner logos or links

Use `WebFetch` or `mcp__chrome-devtools__navigate_page` to read each page.

Extract any logo images found (note URL, alt text, surrounding anchor link — this is logo strip gold).

### Stage 3 — Classify Each Organization

For every discovered organization, classify it using these categories:

| Category | Examples |
|----------|---------|
| `publisher` | Baker Books, Zondervan, IVP, Wiley, Fortress Press |
| `speaking-bureau` | Premier Speakers Bureau, Chartwell, Ambassador Speakers |
| `conference` | Exponential, Q Ideas, The Gospel Coalition, Catalyst, Lausanne |
| `denomination` | Assemblies of God, CBAANZ, Fresh Expressions |
| `network` | 5Q Collective, Forge International, Communitas |
| `media` | Christianity Today, Relevant Magazine, Leadership Journal |
| `academic` | Fuller Seminary, Wheaton College, Regent College |
| `endorser-org` | Organizations whose leaders have publicly endorsed the person |
| `ministry-partner` | Mission orgs, church planting networks they partner with |
| `award-recognition` | Evangelical Christian Publishers Association, etc. |

### Stage 4 — Logo Research

For each confirmed organization, attempt to find a usable logo:

**Priority order:**
1. SVG from their website (`/logo.svg`, `/images/logo.svg`, footer SVG, `<img>` with `logo` in src)
2. High-res PNG from their website (look for `@2x`, `2x`, `hires`, `print` variants)
3. Wikipedia/Wikimedia Commons SVG
4. Clearbit Logo API: `https://logo.clearbit.com/{domain}` (returns PNG)
5. Google Favicon as last resort (too small — flag as LOW quality)

For each logo found, record:
- `logo_url` — direct URL to the image
- `logo_type` — `svg` / `png` / `favicon` / `not-found`
- `logo_quality` — `HIGH` (SVG or hi-res PNG ≥ 200px) / `MEDIUM` (PNG 100–200px) / `LOW` (favicon or < 100px) / `MISSING`
- `logo_background` — `transparent` / `white` / `dark` / `unknown` (important for dark mode logo strips)

### Stage 5 — Verify & Deduplicate

Before finalizing:
1. Remove duplicates (same org found via multiple searches)
2. Remove false positives (e.g., a conference where they attended but didn't speak)
3. Flag LOW confidence entries for user review
4. Check that every MEDIUM/HIGH confidence entry has a clear public record (URL as source)

## Affiliation Data Schema

For each organization, produce a record matching this shape:

```json
{
  "id": "baker-books",
  "name": "Baker Books",
  "short_name": "Baker",
  "category": "publisher",
  "website": "https://bakerpublishinggroup.com",
  "relationship_type": "author",
  "relationship_description": "Primary publisher for Alan Hirsch's books including The Forgotten Ways and 5Q. Baker is one of the leading evangelical academic publishers.",
  "relationship_start_year": 2006,
  "books_published": ["The Forgotten Ways", "The Permanent Revolution", "5Q"],
  "logo_url": "https://bakerpublishinggroup.com/images/baker-logo.svg",
  "logo_type": "svg",
  "logo_quality": "HIGH",
  "logo_background": "white",
  "source_urls": ["https://bakerpublishinggroup.com/authors/alan-hirsch"],
  "confidence": "HIGH",
  "include_in_strip": true,
  "strip_group": "publishers",
  "strip_label": "Published by",
  "prominence_score": 10,
  "notes": ""
}
```

**Field definitions:**
- `id` — kebab-case slug, unique
- `name` — full legal/official name
- `short_name` — abbreviated name for logo strip labels
- `category` — from the category table above
- `relationship_type` — `author`, `speaker`, `faculty`, `board`, `partner`, `alumni`, `endorsed-by`, `media-featured`
- `relationship_description` — 1–3 sentences: what is this relationship, why does it matter to the person's credibility
- `relationship_start_year` — approximate year the relationship began (omit if unknown)
- `logo_url` — direct URL to best available logo
- `logo_type` — `svg` / `png` / `favicon` / `not-found`
- `logo_quality` — `HIGH` / `MEDIUM` / `LOW` / `MISSING`
- `logo_background` — `transparent` / `white` / `dark` / `unknown`
- `source_urls` — array of URLs confirming the relationship
- `confidence` — `HIGH` (direct evidence) / `MEDIUM` (strongly implied) / `LOW` (inferred)
- `include_in_strip` — boolean, set to `true` for HIGH confidence orgs with usable logos
- `strip_group` — one of: `publishers`, `speaking`, `media`, `networks`, `endorsers`, `academic`
- `strip_label` — short label for the group header in the logo strip (e.g., "Published by", "As seen in")
- `prominence_score` — 1–10, how much credibility this relationship adds (10 = major publisher/conference)
- `notes` — any caveats, ambiguities, or things to verify

## Output Format

Save results to `content-library/affiliations/{person-slug}.json` (create directory if needed).

Then print a report:

```
## Affiliation Scrape Report: [Person Name]

### Summary
- Organizations found: N
- HIGH confidence: X
- MEDIUM confidence: Y
- LOW confidence: Z (review needed)
- Strip-ready (include_in_strip = true): N

### By Category
| Category | Count | Strip-ready | Logo quality |
|----------|-------|-------------|-------------|
| publisher | 3 | 3 | HIGH |
| speaking-bureau | 2 | 2 | HIGH |
| conference | 8 | 5 | MEDIUM |
| media | 6 | 4 | MEDIUM |
| network | 4 | 3 | HIGH |
| academic | 2 | 1 | LOW |
| ministry-partner | 5 | 2 | MEDIUM |

### Strip Groups (ordered by prominence)
**publishers** — "Published by" — 3 orgs
**networks** — "Part of" — 3 orgs
**speaking** — "Available to speak" — 2 orgs
**media** — "As featured in" — 4 orgs
**conference** — "Keynote speaker" — 5 orgs

### Needs Review (LOW confidence or MISSING logo)
| Org | Issue | Action needed |
|-----|-------|--------------|
| Example Conference | LOW confidence — only indirect mention found | Verify via speaker page or personal site |
| Example Network | MISSING logo — no SVG or PNG found | Manual logo download needed |

### Next Steps
1. Run `/affiliation-audit {person-slug}` to evaluate strip readiness and grouping
2. Resolve flagged LOW confidence entries manually
3. Download any MISSING logos to `public/images/orgs/`
4. Run `/logo-strip-author {person-slug}` to generate the final section
```

## Key Rules

- **Public record required** — Every HIGH/MEDIUM confidence entry must have a `source_urls` entry proving the relationship
- **No fabrication** — If you cannot verify an affiliation from public sources, set confidence to LOW and flag it
- **Logos from authoritative sources only** — Don't grab logos from third-party aggregators; prefer official org websites
- **Note permissions ambiguity** — Logo use for social proof is generally considered nominative fair use, but flag any org that may object
- **Idempotent** — If re-run, merge new findings with existing file; never overwrite confirmed HIGH confidence entries
- **Prominence scoring** — A major publisher (Baker, Zondervan) scores 10; a regional conference scores 3–5
