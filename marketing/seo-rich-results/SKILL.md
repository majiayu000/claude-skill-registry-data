---
name: seo-rich-results
description: >
  Per-type rich result eligibility checker. Given a URL or page type, determine
  WHICH Google rich results the page is eligible for, validate existing JSON-LD
  against Google's required/recommended properties per type, and produce a gap
  report. Use when user says "rich results", "rich snippets", "eligible rich
  results", "structured data types", or "schema eligibility".
allowed-tools:
  - Read
  - Bash
  - WebFetch
---

# Rich Result Eligibility Checker

<!-- Updated: 2026-06-10 -->

Deeper than the generic schema skill: this skill answers "which rich results CAN
this page earn, and what exactly is missing?" — per-type, against Google's own
required/recommended property lists. For markup **generation**, use `/seo-schema`.

## Inputs

- **URL** (preferred) — the page to check, or
- **Page type** — an archetype ("blog post", "product page", "event page") when
  no live URL exists yet, or
- **Local HTML file** — read with Read tool instead of WebFetch

Optional: existing JSON-LD pasted by the user for offline validation.

## Execution

1. **Fetch the page.** WebFetch the URL (or Read the local file). If WebFetch is
   blocked, fall back to `curl -sL <url>`.
2. **Detect existing structured data.** Extract every
   `<script type="application/ld+json">` block; also note Microdata
   (`itemscope`/`itemprop`) and RDFa (`typeof`/`property`). JSON-LD is Google's
   stated preference.
3. **Classify the page archetype** from content signals (title, H1, byline,
   price, dates, ingredients, salary, address, thread replies).
4. **Check eligibility** with the decision table below — map archetype → active
   rich result types. Reject any type on the deprecation list.
5. **Diff required properties.** For each eligible type, compare existing markup
   against the required and recommended property lists below.
6. **Output the gap report** (format under Output), with a Rich Results Test
   link for live verification.

## Eligibility Decision Table

| Page archetype | Eligible rich result types | Source of truth |
|---|---|---|
| Blog post / news / sports article | Article (`Article`, `NewsArticle`, `BlogPosting`) + BreadcrumbList | structured-data/article |
| Product page (ecommerce) | Product snippet, Merchant listing, Review snippet, BreadcrumbList | structured-data/product-snippet |
| Event / concert / webinar page | Event | structured-data/event |
| Recipe page | Recipe (+ ItemList for carousels, HowToStep for instructions) | structured-data/recipe |
| Job listing | JobPosting | structured-data/job-posting |
| Business location page | LocalBusiness | structured-data/local-business |
| Author / user / company profile | ProfilePage | structured-data/profile-page |
| Forum thread / UGC discussion | DiscussionForumPosting (or SocialMediaPosting) + Comment | structured-data/discussion-forum |
| Q&A page (one question, many answers) | QAPage (use instead of DiscussionForumPosting) | structured-data/discussion-forum |
| Page with reviews of OTHER things | Review snippet / AggregateRating | structured-data/review-snippet |
| Video page | VideoObject | structured-data/video |
| Any page with hierarchy | BreadcrumbList | structured-data/breadcrumb |
| Homepage / brand page | Organization (knowledge panel, not a rich result card) | structured-data/organization |

## Hard Rules — Deprecated & Restricted Types

Never report these as eligible (consistent with `/seo-schema`):

- **HowTo** — rich results removed September 2023 (HowToStep nested inside
  Recipe `recipeInstructions` is still fine).
- **FAQPage** — restricted August 2023: ONLY government and healthcare
  authority sites remain eligible. Everyone else: not eligible.
- **SpecialAnnouncement** — deprecated July 31, 2025.
- **CourseInfo, EstimatedSalary, LearningVideo** — retired June 2025.
- **ClaimReview** — retired from rich results June 2025.
- **VehicleListing** — retired from rich results June 2025.
- **Practice Problem** — retired from rich results late 2025.
- **Dataset** — retired from rich results late 2025.

Also flag self-serving abuse: `aggregateRating`/`review` on LocalBusiness or
Organization markup about **yourself** is not eligible for review snippets —
those properties are only for sites that capture reviews about *other* entities.

## Required vs Recommended Properties (Google-documented)

### Article (`Article` / `NewsArticle` / `BlogPosting`)
- **Required: none.** Google documents only recommended properties.
- Recommended: `author` (+ `author.name`, `author.url`), `headline`,
  `image` (multiple ratios 16x9/4x3/1x1, ≥50K pixels), `datePublished`,
  `dateModified` (ISO 8601 with timezone).

### Product (product snippet)
- Required: `name`, AND at least one of `review` | `aggregateRating` | `offers`.
- Recommended: the other two of `review`/`aggregateRating`/`offers`;
  within `Offer`: `price` (or `priceSpecification.price`), `priceCurrency`,
  `availability`; `positiveNotes`/`negativeNotes` for editorial pros/cons.
- Note: `offers` without `review`/`aggregateRating` triggers a Rich Results
  Test warning. Per Google's Dec 2025 JS guidance, ship Product/Offer JSON-LD
  in server-rendered HTML, not JS-injected.

### Event
- Required: `name` (event title, not venue), `startDate` (ISO 8601 date+time),
  `location` (`Place` with `location.address`).
- Recommended: `endDate`, `description`, `image`, `eventStatus`,
  `location.name`, `offers` (+ `offers.price`, `offers.priceCurrency`,
  `offers.availability`, `offers.url`, `offers.validFrom`), `organizer`,
  `performer`, `previousStartDate` (only with `EventRescheduled`).

### Recipe
- Required: `name`, `image`.
- Recommended: `recipeIngredient`, `recipeInstructions` (prefer `HowToStep`),
  `prepTime` + `cookTime` (always paired) or `totalTime`, `recipeYield`
  (required if `nutrition.calories` present), `nutrition.calories`, `author`,
  `datePublished`, `description`, `keywords`, `recipeCategory`,
  `recipeCuisine`, `aggregateRating`, `video`.

### JobPosting
- Required: `title` (job title, not posting title), `description` (full HTML),
  `datePosted`, `hiringOrganization`, `jobLocation` (must include
  `addressCountry`).
- Recommended: `baseSalary` (employer-provided only), `employmentType`,
  `validThrough` (required if posting expires), `identifier`, `directApply`;
  for 100% remote jobs `jobLocationType: TELECOMMUTE` is required, plus
  `applicantLocationRequirements` if location-restricted.

### LocalBusiness
- Required: `name`, `address` (`PostalAddress`).
- Recommended: `url`, `telephone`, `geo` (`latitude`/`longitude`, ≥5 decimal
  places), `openingHoursSpecification` (`opens`/`closes`/`dayOfWeek`),
  `priceRange` (<100 chars), `menu` + `servesCuisine` (food businesses),
  `department`. (`review`/`aggregateRating` only for third-party review sites.)

### ProfilePage
- Required: `mainEntity` (`Person` or `Organization`) with `name`.
- Recommended: `dateCreated`, `dateModified`, `alternateName` (handle),
  `description`, `identifier`, `image`, `sameAs`, `interactionStatistic`,
  `agentInteractionStatistic`.

### DiscussionForumPosting
- Required: `author` (+ `author.name`), `datePublished`, AND one of
  `text` | `image` | `video` (content not required when representing a post on
  another page via external `url`).
- Recommended: `headline`, `url`, `author.url`, `interactionStatistic`,
  `sharedContent`, nested `comment` (each `Comment` requires `author` +
  `datePublished`).

## Output

```
## Rich Result Eligibility Report — <URL>

Detected page archetype: <archetype>
Existing structured data: <types found, format>

### Eligibility
| Rich result type | Eligible? | Markup present? | Verdict |
|---|---|---|---|
| Product snippet | Yes | Partial | Fix gaps |
| FAQ | No (restricted to gov/health, Aug 2023) | Yes | REMOVE |

### Gap Table (per eligible type)
| Property | Status | Required? | Fix |
|---|---|---|---|
| offers.priceCurrency | MISSING | Recommended | Add ISO 4217 code |

### Next Steps
1. <highest-impact fixes, required props first>
2. Validate live: https://search.google.com/test/rich-results
   (syntax-only check: https://validator.schema.org/)
3. For generating the missing JSON-LD, use /seo-schema
```

Always include the Rich Results Test link. Remind the user that valid markup
makes a page *eligible* — Google does not guarantee a rich result will show.

## Cross-references

- `/seo-schema` — markup generation, templates, full deprecation list
- `/seo-page` — broader single-page SEO review
- Full type gallery: https://developers.google.com/search/docs/appearance/structured-data/search-gallery
