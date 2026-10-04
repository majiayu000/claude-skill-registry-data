---
name: seo-ai-optimization
description: >
  Audit a site or page against Google's OFFICIAL AI optimization guidance —
  readiness for AI Overviews and AI Mode, grounded in Google's published
  ai-optimization-guide and ai-features docs (not third-party GEO theory).
  Use when user says "AI optimization", "AI Overviews", "AI mode",
  "AI search readiness", "optimize for AI", or "GEO audit".
allowed-tools:
  - Read
  - Bash
  - WebFetch
---

# Google AI Search Readiness Audit (AI Overviews + AI Mode)

<!-- Updated: 2026-06-10 -->

This skill audits strictly against Google's own guidance:
https://developers.google.com/search/docs/fundamentals/ai-optimization-guide and
https://developers.google.com/search/docs/appearance/ai-features.
For multi-engine GEO (ChatGPT, Perplexity, Bing Copilot), use `/seo-geo`; for
llms.txt generation, use `/seo-llms-txt` — but note Google's position below.

## Core Facts (from Google's docs — anchor every finding here)

- **No special markup is needed.** "There are no additional requirements to
  appear in AI Overviews or AI Mode, nor other special optimizations necessary."
- **Eligibility = indexed + snippet-eligible.** A page must be indexed and
  eligible to be shown in Google Search with a snippet (Search technical
  requirements). Nothing more — and inclusion is never guaranteed.
- **How the features work:** RAG (grounding on the Search index) + query
  fan-out (concurrent related queries). Core ranking and quality systems decide
  what gets retrieved and cited — SEO is still the lever.
- **"AEO"/"GEO" = SEO**, per Google. Optimizing for generative AI search is
  optimizing for the search experience.
- **Snippet controls govern AI features:** `nosnippet`, `data-nosnippet`,
  `max-snippet`, and `noindex` limit what appears in AI Overviews/AI Mode.
- **Google-Extended controls Gemini training and grounding in OTHER Google
  systems — it does NOT control appearance in AI Overviews or AI Mode.**
  Googlebot in robots.txt is the Search-access control.
- **Measurement:** AI Overviews/AI Mode clicks are inside the Search Console
  Performance report under the "Web" search type (no separate report).

## Inputs

- **URL** (page-level audit) or **domain** (site-level audit)
- Optional: a local content draft (Read tool) for content-quality checks only

## Execution

### 1. Indexability & snippet eligibility (eligibility gate)

```bash
curl -sL <url> -o /tmp/ai-audit-page.html -w "%{http_code}\n"
curl -sL <origin>/robots.txt -o /tmp/ai-audit-robots.txt
```

Check, in order:
- HTTP 200 and not blocked for Googlebot in robots.txt (also CDN/WAF blocks)
- No `noindex` (meta robots or `X-Robots-Tag`)
- Snippet/preview controls: `nosnippet`, `max-snippet:[n]` (a low value
  restricts AI feature usage), `data-nosnippet` spans wrapping main content
- `Google-Extended` in robots.txt — report it, but state explicitly: this
  affects Gemini training/grounding elsewhere, NOT AI Overviews appearance
- Canonical sanity (page not canonicalized away)

Any failure here = NOT ELIGIBLE for AI features; stop and report the fix.

### 2. Content value checks (the biggest lever per Google)

Heuristics on the fetched main content:
- **Unique point of view / non-commodity test:** first-hand evidence, original
  data, named experience ("we tested", photos, case numbers) vs. commodity
  listicle patterns ("7 Tips for...") that restate common knowledge
- **People-first organization:** clear paragraphs, sections, descriptive
  headings that aid navigation
- **Multimodal support:** relevant high-quality images/video supporting the
  text (AI features can surface them)
- **Important content available as text** (not locked in images/canvas/video
  only)
- **Fan-out coverage WITHOUT page proliferation:** flag many near-duplicate
  pages targeting query variations — Google warns this violates the scaled
  content abuse spam policy and doesn't work
- If AI-assisted content: must meet Search Essentials + spam policies
  (see `/seo-helpful-content`)

### 3. Technical structure

- Internal links make the content findable
- Page experience basics: renders on mobile, main content distinguishable,
  reasonable latency
- JavaScript: critical content present in served HTML or properly rendered
- Duplicate content reduced
- Semantic HTML where easy — human readability over perfect code

### 4. Business data consistency (where applicable)

- Structured data **matches the visible text** (consistency, not extra schema —
  Google: "no special schema.org markup you need to add")
- Ecommerce: Merchant Center feed current; Local: Business Profile current

### 5. Mythbusting pass

Flag (as wasted effort, per Google's own mythbusting list) if the site is:
- Relying on **llms.txt** or "AI text files" for Google visibility (no special
  treatment — note this when cross-referencing `/seo-llms-txt`)
- "Chunking" content into fragments for AI
- Rewriting copy "for AI" / stuffing long-tail variants (AI systems understand
  synonyms and meaning)
- Buying/seeking inauthentic mentions
- Over-investing in structured data purely for AI features

## Output

```
## Google AI Search Readiness — <URL or domain>

### Eligibility Gate
| Check | Status | Evidence |
|---|---|---|
| Indexed / indexable | PASS/FAIL | ... |
| Googlebot allowed (robots.txt + CDN) | PASS/FAIL | ... |
| No noindex | PASS/FAIL | ... |
| Snippet controls (nosnippet/max-snippet/data-nosnippet) | PASS/WARN | ... |
| Google-Extended present? | INFO | affects Gemini training, NOT AI Overviews |

### AI-Readiness Scorecard (0-100)
| Pillar | Weight | Score | Notes |
|---|---|---|---|
| Indexability & snippet eligibility | 30 | XX | hard gate |
| Unique, non-commodity content | 35 | XX | biggest long-run lever per Google |
| Technical structure & page experience | 20 | XX | ... |
| Multimodal + business data consistency | 15 | XX | ... |

### Wasted-Effort Flags (Google mythbusting)
- ...

### Top 3 Actions
1. ...
```

Close with: track AI feature traffic in Search Console Performance report
("Web" search type); clicks from AI Overviews tend to be higher quality
(longer time on site), per Google.

## Cross-references

- `/seo-geo` — broader multi-engine GEO (ChatGPT/Perplexity); this skill is
  specifically Google's official guidance and will sometimes disagree with
  generic GEO advice — when it does, say so explicitly
- `/seo-llms-txt` — llms.txt generation (useful for other AI crawlers; Google
  states it is not needed for Google AI features)
- `/seo-helpful-content` — people-first content gate referenced throughout
  Google's AI guidance
- Controls reference: https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag
  and https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers
- Technical requirements: https://developers.google.com/search/docs/essentials/technical
