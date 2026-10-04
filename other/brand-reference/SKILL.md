---
name: brand-reference
description: Find existing articles on the brand's own blog covering the target keyword or related topics. Extract reusable modules, internal-linking opportunities, and product use cases to anchor the new article in the brand's existing voice.
allowed-tools: Read, Write, Bash, WebFetch, WebSearch
---

# Brand Reference Skill

The new article should feel consistent with — and connected to — what the brand has already published. This skill finds the brand's existing coverage of the topic and extracts what's reusable.

## Scale tiers — pick the discovery mode that fits the corpus

How many published articles the brand has determines whether you load the full inventory or query Strapi per draft. The fetch script supports both modes; the choice belongs in this skill, not the script.

| Corpus size | Mode | Command | Why |
|---|---|---|---|
| < ~5,000 articles | **Full inventory** (default) | `doppler run -- python .claude/skills/brand-reference/scripts/fetch_strapi_inventory.py` | One JSON, scored locally. Cheap and easy to reason about. |
| ~5K – 50K | **Per-draft Strapi query** | `doppler run -- python .claude/skills/brand-reference/scripts/fetch_strapi_inventory.py --query "<keyword>,<related-term-1>,<related-term-2>" --limit 30` | Full cache becomes wasteful (10MB+ JSON every run). Ask Strapi to filter server-side using `$containsi` against `title`, `excerpt`, `content`. |
| 50K+ | **Strapi query + local re-rank** | Same `--query` call, then BM25 (SQLite FTS5) re-rank on the 30 candidates | Strapi search is good but coarse — at this scale a smarter local re-rank earns its keep. Embeddings only if BM25 keeps missing semantic matches. |

The full-inventory script prints a one-liner warning at the bottom of its output once `count >= 5_000` so you know to switch.

When using query mode, derive the term list from the research dossier: target keyword + 2-4 related terms from `content-pipeline/1-research/{slug}.md`. Don't query with one term alone — you'll miss synonyms.

## Discovery preference: Strapi API first, web crawl fallback

Many brand blogs (Pleasur.AI included) sit behind Cloudflare bot protection that returns 403 to `WebFetch` and `site:` searches. When that happens, the skill MUST first try the **Strapi API path** before falling back to web search:

1. Run `doppler run -- python .claude/skills/brand-reference/scripts/fetch_strapi_inventory.py` (add `--refresh` to bypass the 7-day cache)
2. Read the resulting `content-pipeline/brand-articles.json` — that's the canonical inventory
3. Only fall back to `WebSearch` / `WebFetch` (steps below) when:
   - The cache file is empty (Strapi returned zero published articles), OR
   - The script exits non-zero (env vars missing, network error) — in which case **state the failure mode in the output**, do not silently degrade

The `STRAPI_BASE_URL` / `STRAPI_API_TOKEN` env vars are the same ones `format_for_strapi.py` already uses for publishing. If they're not set, ask the user to wrap the command in `doppler run --` rather than skipping the API path.

## Input

A target keyword (the same one used by `research`). Reads:
- `brand-config.md` for the brand's blog domain
- `content-pipeline/brand-articles.json` (Strapi inventory cache, refreshed on demand)
- `content-pipeline/1-research/{slug}.md` if it exists (for context on the angle)

## Process

1. **Read brand-config.md** to get the brand's blog URL/domain.
2. **Refresh the Strapi inventory** (`fetch_strapi_inventory.py`) and load `content-pipeline/brand-articles.json`. Each entry has `{slug, url, title, excerpt, publishedAt, h2s}` — enough to score relevance without a per-article fetch.
3. **Score relevance against the target keyword.** Rank inventory entries by:
   - Title keyword overlap with the target keyword (highest weight)
   - H2 overlap with the keyword and its related terms (from `1-research/{slug}.md`)
   - Excerpt match (lowest weight, used as tiebreaker)
   Take the top 3–5.
4. **For each top-ranked article**: pull title + URL + excerpt + H2s from the cache. Only call `WebFetch` on an article when you need the full body to mine a specific module (definition, walkthrough, case study) and the excerpt isn't enough — most runs won't need this.
5. **Web-crawl fallback** — only when step 2 produced zero entries. Use `WebSearch` with a `site:[brand-domain]` operator and `WebFetch` the top 3–5 hits. Note the fallback in the output file so the editor knows the inventory was incomplete.
6. **Identify reusable modules.** Sections from existing articles that could be referenced, summarized, or directly linked from the new article. Examples:
   - "Existing definition we should reuse: [URL] — they define keyword cannibalization as..."
   - "Existing case study we can link to: [URL] — covers the X scenario"
   - "Existing tool walkthrough: [URL] — uses ProductA in step 4"
7. **Extract product-led examples.** When this brand explains the topic, how do they involve their own products? Catalog 3–5 examples — these inform the `product-mentions` step.
8. **Note internal-linking opportunities.** Per H2 of the planned article (use the research dossier's gap analysis as a guide), suggest which existing articles to link to.
9. **Write the reference file.** Save to `content-pipeline/2-reference/{slug}.md` with structure:

```
# Brand reference: {keyword}

## Existing articles on this topic
- [Title](URL) — published {date} — covers: ...
- [Title](URL) — covers: ...

## Reusable modules
### From [Title](URL)
- Definition we can reuse / link to: ...
- Case study: ...
- Statistic: ...

## Product-led examples in our existing coverage
- [URL]: uses ProductA to demonstrate ...
- [URL]: walks through ProductB workflow for ...

## Internal-linking opportunities (by planned section)
- For an H2 on "What is X" → link to [URL]
- For an H2 on "How to do Y" → link to [URL] and [URL]

## Voice / framing notes
- Distinctive way this brand talks about the topic: ...
- Common metaphors / examples: ...
```

## Output

`content-pipeline/2-reference/{slug}.md`

300–700 words. The `outline` and `draft` skills both read this.

## Quality checklist

- [ ] At least 3 existing brand articles identified (or noted as "no existing coverage" with confidence)
- [ ] Each identified article has URL + date + 1-line summary
- [ ] At least 3 product-led examples cataloged (if the brand has products)
- [ ] Internal-linking suggestions tied to actual planned sections
- [ ] If "no existing coverage" → state explicitly so `outline` knows to position this as net-new for the brand

## When this returns thin results

Be precise about *which* failure mode produced the thin result — they're not the same:

- **Strapi creds missing** (env vars unset, script exits with `error: STRAPI_BASE_URL...`) → STOP. Tell the user to wrap in `doppler run --` and re-run. Do NOT fall back to web crawl silently — pleasur.ai is Cloudflare-protected and the crawl will return 403 anyway.
- **Strapi reachable but empty** (script writes a cache with `count: 0`) → the blog has no published articles yet. Note this explicitly. The new article becomes a foundational piece. Suggest 2–3 product/feature pages from `brand-config.md` that could be linked anyway (not blog articles, but still internal). Plan for retro-linking once siblings ship.
- **Strapi reachable but the relevant articles are sparse** (cache has entries but none score well for this keyword) → list what IS in the inventory, even if loosely related — adjacent topics still earn link-equity. Don't pretend nothing exists.
- **Web-crawl fallback used** → flag this at the top of the output file so the editor knows the inventory might be incomplete vs. what's actually published.

In every case, the `product-mentions` skill will still find product fit from `brand-config.md`.
