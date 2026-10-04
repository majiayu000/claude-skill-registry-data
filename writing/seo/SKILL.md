---
name: seo
description: Audit, plan, and implement SEO improvements across technical SEO, on-page optimization, structured data, Core Web Vitals, and content strategy. Use when the user wants better search visibility, SEO remediation, schema markup, sitemap/robots work, or keyword mapping. Do NOT use for writing the page copy itself (article-writing / brand-voice) or for general page-speed refactors unrelated to search (that is the optimize skill).
origin: ECC
---

# SEO

Improve search visibility through technical correctness, performance, and content relevance, not gimmicks.

## When to use

- auditing crawlability, indexability, canonicals, or redirects
- improving title tags, meta descriptions, and heading structure
- adding or validating structured data
- improving Core Web Vitals
- doing keyword research and mapping keywords to URLs
- planning internal linking or sitemap / robots changes

**When NOT to use:**

- the request is "write the blog post" — that is `article-writing`; SEO scopes the brief, not the prose
- the request is general runtime performance with no search stake — that is `optimize`
- you have not read the actual page yet. Recommendations issued without reading the live HTML are
  the #1 anti-pattern in this skill (see Failure modes)

## Inputs

Required before any recommendation — **absent input = stop, never proceed from assumption**:

1. **The real page HTML**, fetched this session. On skyyrose.co:
   `curl -s "https://skyyrose.co/<path>?cb=$(date +%s)"`.
   **NEVER `WebFetch`** — it strips `<script>`, so every JSON-LD block disappears and you will
   report "no structured data" on a page that has three. Cache-bust is mandatory: Batcache
   serves stale HTML.
2. **The template that emits it** — for the WP theme, `wordpress-theme/skyyrose-flagship/`
   (PHP 8.2, classic theme, WooCommerce). A fix lands in the template, not in the rendered HTML.
3. **Target keyword / intent per URL.** One primary theme per URL. Without it you cannot detect
   cannibalization and the audit is decoration.

## Procedure

1. Fetch the live HTML with a cache-busted `curl` (never WebFetch). Save it so the checks below
   have a stable target.
2. Fix technical blockers before content optimization:
   - **Crawlability** — `robots.txt` allows important pages, blocks low-value surfaces; no
     important page unintentionally `noindex`; shallow click depth; redirect chains ≤ 2 hops;
     canonicals self-consistent and non-looping.
   - **Indexability** — consistent preferred URL format; correct `hreflang` if multilingual;
     sitemaps reflect the intended public surface; no duplicate URLs competing without a canonical.
3. Check on-page structure: exactly one `H1`; `H2`/`H3` reflect real content hierarchy;
   title ~50–60 chars with the primary concept near the front; meta description ~120–160 chars,
   honest, topic stated naturally.
4. Validate structured data against what is actually on the page: `Organization`/business schema
   on the homepage · `Article`/`BlogPosting` on editorial · `Product` + `Offer` on PDPs ·
   `BreadcrumbList` on interior pages · `FAQPage` **only** when the Q&A content genuinely exists.
5. Budget Core Web Vitals: LCP < 2.5s · INP < 200ms · CLS < 0.1. Common fixes: preload hero
   assets, cut render-blocking work, reserve layout space, trim heavy JS.
6. Map keywords: define intent → gather realistic variants → prioritize by intent match, value,
   competition → one primary theme per URL → detect cannibalization.
7. Plan internal linking: strong pages link to pages you want ranked; descriptive anchors;
   backfill links from new pages to relevant existing ones.
8. Implement in the template, rebuild if theme assets changed (`cd wordpress-theme && npm run build`
   — production serves `.min`), bump the `SKYYROSE_VERSION` triple, then re-run Verification
   against the live URL.

## Reference shapes

Title formula, meta formula, minimal JSON-LD, and audit-finding shape:

```text
Primary Topic - Specific Modifier | Brand
Action + topic + value proposition + one supporting detail

[HIGH] Duplicate title tags on collection pages
Location: wordpress-theme/skyyrose-flagship/<template>.php
Issue:    Dynamic titles collapse to one default string — duplicate signals, weak relevance.
Fix:      Emit a unique title per collection from the collection name + primary category.
```

```json
{ "@context": "https://schema.org", "@type": "Article",
  "headline": "Page Title Here",
  "author": { "@type": "Person", "name": "Author Name" },
  "publisher": { "@type": "Organization", "name": "Brand Name" } }
```

# Verification

Fetch once, check many. A `curl` that returns a non-200 or an empty body is a **dead gate**, not
a pass (bug-230) — re-run before interpreting anything downstream of it.

1. **Page is reachable and not stale** — cache-bust every request:

```bash
curl -s "https://skyyrose.co/?cb=$(date +%s)" -o /tmp/seo-page.html -w 'HTTP %{http_code} %{size_download} bytes\n'
```

   **PASS:** `HTTP 200` and a body over ~50KB for a real theme page. `[live]`

2. **Structured data actually parses** — presence is not validity:

```bash
python3 - /tmp/seo-page.html <<'PY'
import json, re, sys
html = open(sys.argv[1]).read()
blocks = re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', html, re.S)
ok = 0
for i, b in enumerate(blocks):
    try:
        d = json.loads(b)
        t = d.get("@type") if isinstance(d, dict) else [x.get("@type") for x in d]
        print(f"block {i}: valid, @type={t}"); ok += 1
    except Exception as e:
        print(f"block {i}: INVALID: {e}")
print(f"{ok}/{len(blocks)} blocks parse")
sys.exit(0 if blocks and ok == len(blocks) else 1)
PY
```

   **PASS:** exit 0, and every block reports `valid`. Zero blocks also exits 1 — an absent gate
   input fails closed, it does not pass. `[live]`

3. **Exactly one H1, and a title in range**:

```bash
grep -o '<h1' /tmp/seo-page.html | wc -l
grep -o '<title>[^<]*</title>' /tmp/seo-page.html | head -1
```

   **PASS:** H1 count is `1`; title length 50–60 chars. Any other H1 count is a finding. `[live]`

Prove check 2 can fail before trusting it (rule 3): the first regex written for it used
`<script type="application/ld+json"` and returned `0/0 blocks parse`, exit 1 — because the live
markup is `<script data-jetpack-boost="ignore" type="application/ld+json">`. A "0 blocks" result
is a broken selector until proven otherwise.

**Attribution before claiming a finding is yours** (rule 4): run the same check against the
pristine tree — `git archive HEAD wordpress-theme/skyyrose-flagship | tar -x -C <scratch>` —
never `git stash`, the stash stack is shared across worktrees.

## Worked example

Real run against production, 2026-07-28:

```bash
$ curl -s "https://skyyrose.co/?cb=$(date +%s)" -o home.html -w 'HTTP %{http_code} %{size_download} bytes\n'
HTTP 200 136605 bytes

$ grep -o '<title>[^<]*</title>' home.html | head -1
<title>The Skyy Rose Collection</title>

$ grep -c 'application/ld+json' home.html
3

$ printf '%s' 'The Skyy Rose Collection' | wc -c
      24
```

Then the JSON-LD parse check (script above) `[live]`:

```text
block 0: valid, @type=Organization
block 1: valid, @type=WebSite
block 2: valid, @type=Organization
3/3 blocks parse
```

**Findings from this run:** the homepage title is 24 characters (measured, not eyeballed) — under the 50–60 target and
carrying no category or intent term, so it wins nothing beyond the brand name `[live]`. Two of
three JSON-LD blocks are `@type=Organization`, i.e. the organization entity is emitted twice
from two different sources; one should be removed so the entity is unambiguous `[live]`. Both
are audit findings, not deployed fixes — the fix belongs in the emitting template and is
unverified until re-fetched post-deploy.

## Failure modes

| Failure | What it looks like | Rule |
|---|---|---|
| `WebFetch` used on live HTML | "the page has no structured data" on a page with 3 blocks | `WebFetch` strips `<script>`. Always cache-busted `curl` |
| No cache-bust | fix deployed, audit still shows old markup | Batcache serves stale. `?cb=$(date +%s)` on every request |
| Repo → live scope jump | "production SEO bug" from reading a template only | bug-287. Severity requires `[live]`. State scope before severity |
| Zero-blocks read as "clean" | a broken selector reported as a passing check | bug-230 fail-open. Zero findings from an unproven selector is an artifact — verify the selector against known-present markup |
| Schema for absent content | `FAQPage` on a page with no Q&A | Match schema to reality; mismatched markup is a manual-action risk |
| CSS/JS fix not rebuilt | template edited, production unchanged | Production serves `.min`. `cd wordpress-theme && npm run build`, then bump the `SKYYROSE_VERSION` triple (`functions.php`, `style.css`, `readme.txt`) — it is the cache-bust param on ~52 enqueue calls |
| Keyword stuffing / thin duplicates | copy written for bots | Write for users; consolidate or differentiate near-duplicate pages |

## Related skills

`skyyrose-market:skyyrose-seo-commerce` (WooCommerce-specific schema + PHP; plugin-namespaced —
verified on disk at `~/.claude/plugins/cache/skyyrose-suite/skyyrose-market/1.0.0/skills/`,
**not** a bare `skyyrose-seo-commerce` in `.claude/skills/`) · `frontend-patterns` ·
`brand-voice` · `market-research`
