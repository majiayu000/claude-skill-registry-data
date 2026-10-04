---
name: knowledge-graph
description: Configure and debug the Baan knowledge-graph pipeline — AI entity extraction, Wikidata linking, Schema.org mentions/about, entity hub pages, and the entity-bridge article generator. Use when asked to "extract entities", "tune entity extraction", "debug knowledge graph", "link to Wikidata", "configure FAQ schema", or when the Knowledge Graph page shows demo data.
---

# Knowledge Graph Workflow

Baan's knowledge graph is a pipeline: article body → AI entity extraction → Wikidata linking → frontmatter persistence → article_index DB cache → JSON-LD emission (Schema.org `about` / `mentions`) → entity hub pages + sitemap + public API.

## Required Reference

**Always read `docs/spec/knowledge-graph.md` first** — it is the authoritative reference. The steps below are an operational index.

Secondary references:
- `docs/knowledge-graph.md` — user-facing overview
- `docs/aeo-score.md` — how knowledge-graph coverage feeds the AEO score
- `docs/spec/faq-schema.md` — adjacent FAQ Schema pipeline
- `prompts/entityExtraction.system.md`, `prompts/entityExtraction.user.md` — the AI prompts

## When this skill applies

| Task | Steps |
|------|-------|
| Tune entity extraction quality | Prompt tuning (Step 1) |
| Diagnose missing / wrong entities | Pipeline trace (Step 2) |
| Knowledge-Graph page shows demo data | Data-load debug (Step 3) |
| Add / adjust Wikidata linking | Wikidata layer (Step 4) |
| Verify Schema.org JSON-LD output | JSON-LD verification (Step 5) |
| Implement / debug entity-bridge article ideas | Bridge feature (Step 6) |

## Step 1: Prompt tuning

The extractor lives at `lib/knowledge-graph/entity-extractor.ts`. The AI side is fully prompt-driven from:

- `prompts/entityExtraction.system.md` — defines entity types, output schema, extraction guidelines
- `prompts/entityExtraction.user.md` — injects article locale + content

Do not hardcode prompt text in TypeScript. Any change to extraction behavior is a prompt edit.

After editing, test with a representative article (Admin → Knowledge Graph → Extract). Compare output to expectation. Low quality typically means the system prompt needs tighter entity-type criteria, not code changes.

## Step 2: Pipeline trace

```
Article body
  → extractEntities() — lib/knowledge-graph/entity-extractor.ts
    → AI call (Gemini / ChatGPT / Claude — uses AI settings "Knowledge Graph" feature slot)
      → Entity[] { name, type, relevance, isMainSubject }
        → linkEntitiesToWikidata() — lib/knowledge-graph/wikidata.ts
          → Entity[] with wikidataId + description
            → POST /baan-admin/api/knowledge-graph/extract persists to frontmatter
              → upsertArticleIndexFromContent() updates DB cache
```

If entities are extracted but not persisted: check whether `saveToArticle: true` was passed to the API.
If persisted but not in the DB cache: check `article_index.entities` column — the cache should reflect frontmatter. Rebuild via `Admin → Settings → System → Rebuild article index` if drift is suspected.

## Step 3: Demo-data debug (common)

**Symptom**: Knowledge Graph page shows demo entities (Python, Google, Tokyo) despite real articles with entities.

Root causes, in order of likelihood:

1. **No article has `entities` in frontmatter yet** — verify by opening a post `.md` file
2. **Multi-locale mismatch** — per-article, every locale file is checked, and the first file with entities wins. If only one locale was extracted, ensure that locale's file is saved
3. **DB cache stale** — run `Admin → Settings → System → Rebuild article index`
4. **Build-cache stale** — delete `.next/standalone` and rebuild

The demo fallback triggers only when zero articles have entities, or `?demo=true` is set. Check the API response `isDemo` field to confirm which path was hit.

## Step 4: Wikidata layer

- `searchWikidata(query, locale)` — returns candidates
- `getWikidataEntity(id, locale)` — fetches label / description / URL for a known ID
- `linkEntitiesToWikidata(entities, locale)` — batched linker used by the extraction endpoint

Wikidata is rate-limited by fair-use. Keep per-test requests to 1 (see `.claude/rules/test-external-calls.md`). Failures are silent by design — an entity without `wikidataId` still renders, just without `sameAs`.

For language mapping (`ja` → `ja`, `pt-BR` → `pt`, unknown → `en`), see `getWikidataLanguage()`.

## Step 5: JSON-LD verification

Article pages emit Schema.org JSON-LD from `lib/schema.ts`. Partition by `isMainSubject`:

- `isMainSubject: true` → Schema.org `about`
- `isMainSubject: false` → Schema.org `mentions`

Entity `@id` is the internal hub URL (`/[locale]/entity/[type]/[name]`); `sameAs` is the Wikidata URL.

Verify by:
1. Open the article page
2. Inspect HTML → find `<script type="application/ld+json">`
3. Confirm `about` and `mentions` arrays contain expected entities with correct `@id` and `sameAs`

## Step 6: Entity-bridge feature

User flow: graph page → click two entities → AI proposes 5 bridging article ideas → click "Create article" → outline auto-generated → PostEditor prefilled.

Key files:
- `app/baan-admin/[secretPath]/(authenticated)/knowledge-graph/graph/page.tsx` — multi-select UI + bridge panel
- `prompts/ai-assistant/actions/bridge.md` — bridge-idea prompt
- `lib/prompt-loader.ts` — `ActionType: 'bridge'`
- `PostEditor.tsx` — reads `sessionStorage['newArticlePrefill']` via `useRef` (React 18 Strict Mode safe)

If bridge ideas fail to load: check `POST /baan-admin/api/ai-assistant` with `action: "bridge"` — the response must be valid JSON with an `ideas[]` array.

## Do not

- Do not add entity fields to frontmatter by hand — always use the extract endpoint so the DB cache stays in sync
- Do not call the extraction endpoint for every article in a loop during tests — the AI API rate limit and billing apply (see `.claude/rules/test-external-calls.md`)
- Do not modify `linkEntitiesToWikidata()` to fetch in parallel — Wikidata's fair-use requires serial calls
- Do not remove the `sameAs` field from emitted JSON-LD — downstream AEO tooling depends on it
