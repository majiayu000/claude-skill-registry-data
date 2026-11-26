---
name: seme-development
description: "Use when working on the Seme memory system codebase."
license: MIT
metadata:
  author: project
  version: "1.3"
  category: software-development
  hermes:
    tags:
      - seme
      - memory-system
      - sqlite
      - typescript
    related_skills:
      - kernel-dev-database
      - kernel-dev-typescript
      - kernel-dev-api
      - kernel-dev-react
when:
  - working on the Seme codebase
  - implementing memory extraction, resolution, or retrieval features
  - adding API endpoints to the Seme server
  - building the TanStack Start dashboard
  - debugging extraction or entity resolution issues
---

## When to Use

- Working on the Seme codebase (apps/api, apps/web, docs)
- Implementing or debugging memory extraction, resolution, or retrieval
- Adding API endpoints or schema migrations
- Building or modifying the TanStack Start dashboard
- Entity extraction or knowledge graph issues

# Seme Development

## Architecture

- **Backend**: Hono + SQLite (better-sqlite3) + TypeScript. Runs on port 3000.
- **Frontend**: TanStack Start (React + Tailwind v4 + shadcn/ui). Runs on port 5173.
- **Storage**: `<storage-dir>/memory.db`, where `<storage-dir>` is `SEME_STORAGE_DIR` or the app's default under `$HOME`.
- **LLM**: OpenRouter, default model is `anthropic/claude-haiku-5.5` (7.5x cheaper than Gemini Flash, more reliable).
- **Monorepo**: `apps/api` (backend) + `apps/web` (frontend) + `docs/` (HTML pages + essays).
- **Essays**: `<soapbox-repo>/src/pages/essays/` (the separate soapbox site repo) — 9 Astro pages (7 long-form + 2 animated: Knowledge Graph, Hybrid Search). Converted from standalone HTML to proper Astro pages using BaseLayout. Topics: Knowledge Graph, Hybrid Search, Entity Extraction, Auto-Deprecation, Source Ingestion, KB Intelligence, Temporal Queries, Animated Knowledge Graph, Animated Hybrid Search.
- **Feature analysis**: `docs/feature-analysis.md` — lists all 24 features not on the original website.
- **Status**: all tracked issues resolved; 201/201 evals passing (7 suites).
- **Modules**: storage, extraction (memory + entity), resolver, profile, retrieval, ingest, validation, sleep, review, deletion, adaptation, graph, wiki, mcp, ingestion, search, kb, tasks, procedures, deprecation, import, integrations.

## Key Patterns

- **Schema Migrations**
- Migrations are versioned (v1-v9) in `src/schema/schema.ts`.
- Each migration has a `getSchemaSqlVx()` function.
- Storage runs migrations sequentially with checksum verification.
- When adding a new table, create a new migration version and update `getMigrations()` in `storage.ts`.
- Always update `SCHEMA_VERSION` constant.

### Extraction Pipeline

- Memory extraction and entity extraction are **separate LLM calls**.
- Memory extractor: extracts atomic claims (facts, preferences, decisions, etc.).
- Entity extractor: extracts named entities and relationships.
- Both run async after `endSession()`. The API returns immediately with `pipeline_job_id`.
- **Always wait 20-45s** before checking extraction results in tests.
- Entity extraction can fail independently — memories may exist without entities.

### Resolver (Cross-Slot Supersession Bug)

- `isSupersede()` MUST check `candidate.slot === incumbent.slot` before superseding.
- Without this check, memories with different single-valued slots (e.g., 'name' and 'home_city') will incorrectly supersede each other.
- Pattern: `if (candidate.slot !== incumbent.slot) return false;`

### FTS5 Query Sanitization

- FTS5 treats `?`, `*`, `"`, `()`, etc. as operators. Always sanitize user queries.
- Pattern: `userMessage.replace(/[?*"()]/g, ' ').trim()`
- Also strip punctuation from keyword match words: `userMessage.toLowerCase().replace(/[^a-z0-9\s]/g, '')`

### Entity Type Handling (Scalable)

- Do NOT maintain a hardcoded dictionary of valid entity types. The LLM decides the type.
- `EntityCandidate.type` is `string` (not a union). Accept any type from the LLM.
- Normalize: lowercase + trim in validateOutput().
- Schema: `type TEXT NOT NULL` with NO CHECK constraint (migration v9 removed it).
- System prompt: list common types as guidance but say 'or any appropriate type for the entity'.
- The only validation: type must be a non-empty string. No hardcoded list.
- Previous bug: 'animal' type wasn't in validEntityTypes → entity extraction failed silently, memories existed without entities. The LLM returned 'animal' for pet names but validation rejected it.
- Pattern: never gate LLM output on a manually-maintained allowlist. The LLM may return types you haven't seen before ('animal', 'vehicle', 'food', etc.).
- Tested with 50 different entity mentions → 51 entities, 10 unique types. 'other' is used as fallback for things that don't fit standard categories (e.g., 'Tesla Model 3' → 'other').

### Memory Value Format

- `value_text` is an atomic claim sentence (e.g., 'The user's name is Charles.'), not a raw value.
- This is intentional: self-contained claims give the LLM full context during retrieval.
- Raw values ('Charles') are ambiguous without predicate context.

### Long Message Extraction

- Haiku extracts all facts from long rambling messages (400+ words, 30+ facts) with 100% coverage.
- No truncation or attention issues observed. Facts from all paragraphs are captured.
- Extraction takes ~45s for very long messages (async, runs after session end).

### Chunked Entity Extraction

- Entity extraction fails with >6-8 turns per LLM call (output too large, invalid JSON).
- Chunk turns into batches of 6: `for (let i = 0; i < turns.length; i += 6)`.
- Deduplicate entities across chunks by lowercase name.
- Merge relationship candidates from all chunks.
- Memory extraction does NOT need chunking (handles 50+ turns fine).
- Only entity extraction needs chunking due to larger per-entity output.

### Markdown Stripping in JSON Parsing

- LLMs sometimes wrap JSON in ```json fences even with response_format: json_object.
- Always strip before parsing: `content.trim().replace(/^```(?:json)?\n?/, '').replace(/\n?```$/, '').trim()`.
- Apply to both memory extractor and entity extractor.
- Pattern: strip fences, then JSON.parse, then validate.

### Async Extraction Timing

- Extraction runs asynchronously after `endSession()`.
- In tests, wait at least 20s (simple messages) or 45s (long messages) before checking results.
- Calling `seme.close()` too early causes 'database connection is not open' errors.
- Do not close the service until async operations complete.

### Knowledge Wiki

- Auto-generates Wikipedia-style pages per entity from accumulated memories.
- Maturity levels: draft → stable (≥3 memories, ≥0.9 conf) → canonical.
- Versioning: each update creates a version record with reason and created_by.
- Conflict detection: same slot, different values → flagged for review.
- API: GET/POST/PUT/DELETE /wiki, /wiki/:id, /wiki/entity/:entityId, /wiki/:id/versions, /wiki/search/:query, POST /wiki/compile/:entityId, POST /wiki/compile-all, GET /wiki/conflicts/:entityId.
- WikiCompiler.compileForEntity(entityId, entityName) generates content from linked memories.
- Wiki pages are markdown with sections grouped by memory kind.

### Source Ingestion

- Converts external content (URLs, PDFs, YouTube, text) into conversation turns for extraction.
- Chunking: paragraph-based, max 2000 chars per chunk. Falls back to character-based.
- Each chunk is prefixed with `[Source: Title (URL)]` for provenance.
- PDF: uses pdftotext -layout. YouTube: uses yt-dlp for VTT subtitles.
- API: POST /ingest/source (body: { url, pdf_path, text, title, session_id }), GET /sources.

### Hybrid Search

- Queries 4 layers: turns (FTS5), memories (FTS5), wiki (LIKE), graph (entity name match + 2-hop traversal).
- Returns unified LLM-ready context string with sections per layer.
- Temporal filtering: since/before/asOf parameters filter memories by observed_at.
- Abstention: abstain: true when no results across all layers.
- API: POST /search (body: { query, limit, include_turns, include_memories, include_wiki, include_graph, since, before, asOf }).

### KB Intelligence

- Challenge: keyword-overlap claim verification against existing memories.
- Emerge: pattern surfacing (by kind, by slot, by subject). Returns patterns with memory IDs.
- Connect: topic bridging via graph pathfinding + shared neighbors.
- Contradictions: same slot, different values. Severity based on confidence.
- Lint: low confidence, missing slots, duplicates, orphaned entities, deprecated pages. Health score = 1 - (issues * 0.1).
- API: POST /kb/challenge, /kb/emerge, /kb/connect, /kb/lint, GET /kb/contradictions.

### KB Tasks

- Task management: create, read, update, delete.
- Status: pending, in_progress, done, cancelled.
- Priority: low, medium, high, urgent.
- Link tasks to memories and entities via memory_ids and entity_ids arrays.
- API: POST /tasks, GET /tasks, GET /tasks/:id, PATCH /tasks/:id, DELETE /tasks/:id.

### Temporal Queries

- since/before/asOf parameters on retrieveContext and hybrid search.
- Filters memories by observed_at range at SQL level.
- asOf sets historical: true for snapshot queries.
- Normalized in service: since→from, before/asOf→to.

### Auto-Deprecation

- Detects stale facts: days since last_reinforced_at > threshold (per decay class).
- Thresholds: session=1d, fast=7d, medium=30d, slow=90d, exempt=365d.
- Marks as 'archived' (not deleted) with reason.
- API: POST /deprecation/run, GET /deprecation/thresholds.

### Procedures

- Saved SOPs, playbooks, prompts with trigger patterns.
- Types: sop, playbook, ui_walkthrough, prompt.
- Trigger matching: regex-based pattern matching.
- Guards and steps stored as JSON arrays.
- API: POST/GET/PATCH/DELETE /procedures, GET /procedures/match/:trigger.

### Per-Memory Feedback

- POST /memories/:id/feedback with signal_type.
- Adjusts confidence: compliment +0.1, correction -0.2, disengagement -0.05.
- Increments reinforcement_count and updates last_reinforced_at.
- Records feedback event with memory_id in detail_json.

### Data Import

- POST /import restores from export bundle.
- Strategies: skip (default), overwrite, merge.
- Imports episodes, turns, memories, entities, relationships, profile.
- Handles conflicts per strategy.

### Composio Integrations

- External service connection framework.
- Known services: Gmail, Slack, Notion, GitHub, Google Calendar, Linear.
- Status tracking: connected, disconnected, error, pending.
- API: GET /integrations, GET /integrations/known, POST /integrations/connect, PATCH /integrations/:id, DELETE /integrations/:id.

### Hybrid Search (FTS5 + Vector + Graph)

- Seme now uses **hybrid search**: FTS5 keyword matching + sqlite-vec vector similarity + graph traversal.
- Embeddings are generated via Ollama (`qwen3-embedding:0.6b`, 1024-dim, free, local) during extraction.
- Embeddings stored in `memories_vec` virtual table (sqlite-vec `vec0`).
- Retrieval queries 4 layers: FTS5 keyword, exact keyword, vector similarity (cosine distance < 0.5), graph entity matching.
- **Graceful degradation**: if Ollama is unavailable, embeddings are skipped (FTS5-only fallback). No crash.
- Default embedding dim changed from 4 → 1024. Override with `SEME_EMBEDDING_DIM`.
- Embedding provider: `src/embeddings/embedding-provider.ts` (Ollama primary, OpenRouter fallback, NoOp fallback).
- Factory function: `createEmbeddingProvider()` — returns OllamaEmbeddingProvider by default.
- `retrieveContext` is now **async** — all callers must `await` it.
- Vector search threshold: cosine distance < 0.5 (reasonably similar results only).
- SQLite cache_size = -64000 (64MB page cache).
- Entity extraction chunked at 6 turns/batch, processed in parallel (Promise.all).
- Markdown fence stripping in both extractors.
- Haiku only (7.5x cheaper than Gemini, more reliable).
- No hardcoded entity type dictionary (accept any string, normalize to lowercase).
- **Benchmark vs Mem0**: Seme hybrid search achieves ~50-90% retrieval accuracy on semantic queries (vs Mem0's 100% with vector-only search). Seme is 300x faster (0.003s vs 0.958s per query) and has richer data model (graph, temporal, auto-deprecation). Recommendation: hybrid search combines Seme's speed with Mem0's accuracy.

### Haiku Only (No Gemini)

- Haiku is 7.5x cheaper ($0.10/$0.50 vs Gemini's $0.75/$3.75 per M tokens).
- Haiku is more reliable (31/31 vs 29/31 on extraction eval).
- Haiku extracts more memories from long messages (33 vs 19).
- Default and only supported model is `anthropic/claude-haiku-5.5`.
- Gemini has been removed from evals and defaults. Do not re-add.
- Extraction eval runs only Haiku.

### Migration Checksum Mismatch

- When migration SQL is modified after the DB is created, the stored checksum won't match.
- Fix: compute the current checksum using `createHash('sha256').update(vXSql).digest('hex')` and update the DB: `UPDATE schema_migrations SET checksum = ? WHERE version = X`.
- Use tsx to compute: `import { getSchemaSqlVx } from '...'` then hash the SQL.
- This is a data migration, not a code change. The code is correct; the DB metadata is stale.

### Embedding Dimension Migration

- When changing `EMBEDDING_DIM`, existing DBs store the old dimension in `schema_meta`.
- The Storage constructor throws if `stored !== configured`.
- Fix: set `SEME_EMBEDDING_DIM` env var to match the stored dimension, OR update `schema_meta` value, OR delete and recreate the DB.
- For production migration: update `schema_meta` value and recreate the `memories_vec` table with the new dimension.
- The `memories_vec` virtual table uses `FLOAT[dim]` — changing dim requires recreating the table.

### KB Health Score Debugging

- Health score = 1.0 - (issues × 0.1). Starts at 100%, each issue costs 10%.
- 5 checks: low confidence (<0.5), missing slots (>5), duplicates, orphaned entities (no relationships), deprecated wiki pages.
- **Duplicates**: Use `POST /memory/forget` with `scope: "memory"` and `confirmed_irreversible: true`. Not `DELETE /memories/:id` (doesn't exist).
- **Orphaned entities**: Create relationships via `POST /relationships` with valid `source_turn_id` and `source_episode_id` (foreign key required). Get these from existing turns/episodes in the DB.
- **Missing slots**: Low severity. Observation-type memories often lack slots. Threshold is >5. Can be ignored or slots assigned.
- Sleep job dedup merges 0 duplicates if they have different IDs — use forget endpoint instead.
- KB lint issues don't affect functionality, only the diagnostic score.
- When frontend (port 5173) calls backend (port 3000), need CORS middleware.
- Restrict origins to known hosts: localhost:3000, 3001, 5173 (and 127.0.0.1 variants).
- Handle OPTIONS preflight with 204 response.
- Set Access-Control-Allow-Credentials: true for cookie support.

### TanStack Start + shadcn/ui

- Use `@tailwindcss/vite` plugin for Tailwind v4.
- CSS: `@import "tailwindcss"` + `@theme inline` with HSL CSS variables.
- shadcn components use `cn()` utility (clsx + tailwind-merge) from `src/lib/utils.ts`.
- Component imports use `../../lib/utils` (relative from `src/components/ui/`).
- Path aliases: `#/*` and `@/*` both map to `./src/*`.

### Bruno API Config

- All `.bru` files use `{{baseUrl}}` (port 3000).
- Environment file: `bruno/environments/local.bru` with `baseUrl: http://localhost:3000`.
- Create one `.bru` file per endpoint.

### HTML Docs (GitHub Design System)

- Use GitHub colors: #24292f text, #0969da blue, #d0d7de borders.
- System fonts: -apple-system, BlinkMacSystemFont, Segoe UI, etc.
- Flat 1px borders (not shadow-as-border like Vercel).
- Prism.js for JSON syntax highlighting.
- JSON code blocks use `<pre class="code-block"><code class="language-json">` with `json.dumps(indent=2)`.

## Auth Gate (Deployed)

- Production API spends the OpenRouter key, so gate it with a shared `SEME_API_KEY`.
- API middleware: when `SEME_API_KEY` is set (non-empty), require `Authorization: Bearer <key>` on every route except `GET /health`; compare in constant time (equal-length Buffer + `timingSafeEqual`). Register the auth middleware _after_ the CORS middleware so preflight (`OPTIONS`) is handled by CORS and never reaches auth.
- When `SEME_API_KEY` is unset, no auth (local dev and tests unchanged).
- `seed-rss.ts`: forward the `Authorization` header when `SEME_API_KEY` is present.
- Web: the SPA cannot carry the secret in its shell. Store the entered password in `sessionStorage` under `seme_api_key`; attach it to all API requests; on any 401 clear the key and re-show the gate. Verify the password against a protected endpoint (e.g. `/entities?limit=1`) before storing it.
- Secret handling: generate with `openssl rand -hex 24`, write to `~/.seme-gate-password` with chmod 600, never print/commit it. Set on the API app only via `flyctl secrets set`; redeploy the API to apply; keep the web's `VITE_SEME_API_URL` build arg.
- Verification: `/health` returns 200 without a header; a protected endpoint returns 401 without and 200 with `Authorization: Bearer $(cat ~/.seme-gate-password)` (read from file inside the command; do not echo).

## Pitfalls

- **Fly secrets staging**: `flyctl secrets set` may stage the secret without applying it; check `flyctl secrets list` and redeploy the app to apply staged secrets.
- **CORS before auth**: Register auth middleware after CORS handling; otherwise browser preflight (`OPTIONS`) is rejected and all web requests fail.
- **Web apiFetch headers**: Build headers with `new Headers(options?.headers)` before adding `Authorization`, so caller-supplied headers are preserved.
- **Web 401 handling**: On 401, clear the stored key and dispatch a `seme:unauthorized` event so the gate re-prompts instead of silently failing data loads.

- **Async extraction timing**: Always wait 20-45s before checking DB after `endSession()`. Calling `seme.close()` too early causes 'database connection is not open' errors.
- **KG eval noise**: `kg-eval.js` may print `Extraction failed ... The database connection is not open` from async extraction after `svc.close()`; these are expected noise and do not affect the pass count (21/21).
- **Async retrieveContext**: `retrieveContext` is now async (returns Promise). All callers must `await`. Forgetting `await` returns a Promise, causing `ctx.memories` to be undefined. Pattern: `const ctx = await service.retrieveContext(...)`.
- **Entity extraction is separate**: Memories can be extracted without entities. Entity extraction can fail independently. Always check both memories and entities after extraction.
- **Entity type allowlist**: Never gate LLM entity types on a hardcoded allowlist. The LLM may return types not in your list (e.g., 'animal' for pets). Validation must accept any non-empty string and normalize to lowercase. A mismatch causes silent invalid_output errors and zero entities created.
- **Cross-slot supersession**: Without `candidate.slot !== incumbent.slot` check, memories with different single-valued slots incorrectly supersede each other.
- **FTS5 special chars**: `?`, `*`, `"`, `()` in user queries cause syntax errors. Always sanitize.
- **Haiku vs Gemini**: Default model must be Haiku. Gemini was removed due to cost and reliability.
- **Port conflicts**: Seme API (3000), web app (5173/3001), docs (8888). Check for running processes before starting.
- **Background process env vars**: `export VAR=value && node ... &` does NOT pass env vars to the background process. Use a wrapper script: `cat > /tmp/start.sh << 'EOF' ... exec node ... EOF; bash /tmp/start.sh &`. Or set env vars inline: `VAR=value node dist/server.js &` (this works because the var is on the same command line).
- **Hono CORS**: Manual middleware works better than `hono/cors` in some setups. Use `app.use('*', async (c, next) => {...})`.
- **Monorepo**: API is CommonJS, web is ESM. Don't try to share code directly — use HTTP API calls.
- **Tailwind v4**: Uses `@import "tailwindcss"` and `@theme inline` — no `tailwind.config.js` needed.
- **shadcn components**: Use relative imports (`../../lib/utils`) from `src/components/ui/`.
- **Astro HTML-to-Astro conversion**: When converting standalone HTML essays to Astro pages, extract `<body>`, `<style>`, and `<script>` content separately. Use `set:html` for HTML content and `is:inline` for scripts. Escape backticks and `${}` in template literals. The `is:inline` directive prevents Astro from processing script content at build time.
- **rolldown binding issue**: Astro's build may fail with "Cannot find module './rolldown-binding.wasi.cjs'". Fix by reinstalling rolldown: `npm install rolldown`. This is an environment issue, not a code issue.

## Deploy / Release (Fly.io)

Seme ships as two independent Fly apps: `seme-web` (web) and `seme-api` (API). Deploys are manual and sequential; each app rebuilds on its own.

Procedure (run in order):

1. Merge the PR via GitHub: `gh pr merge <N> --merge` (regular merge commit; do not squash, do not delete the branch). Confirm with `gh pr view <N> --json mergeCommit,state` and record the merge commit sha.
2. Update local checkout: `git checkout main && git pull origin main`. Record new HEAD (`git rev-parse HEAD`).
3. Deploy web: from `apps/web`, `flyctl deploy --remote-only -a seme-web`. Record the release version from `flyctl releases -a seme-web`.
4. Deploy API: from `apps/api`, `flyctl deploy --remote-only -a seme-api`. Record the release version from `flyctl releases -a seme-api`. (This makes any document-mode extractor live for NEW ingests only — do not re-seed or rebuild data.)
5. Verify:
   - `curl -s -o /dev/null -w "%{http_code}" https://seme-web.fly.dev/` → 200
   - `curl -s -o /dev/null -w "%{http_code}" https://seme-api.fly.dev/health` → 200
   - `curl -s -o /dev/null -w "%{http_code}" https://seme-api.fly.dev/entities` (no auth) → 401 (gate intact)

Notes:

- `--remote-only` builds on Fly's depot builder; unchanged layers are cached, so a deploy with no source changes may reuse the prior image and still create a new release.
- Web and API deploy independently; deploy both only when both changed.
- Record merge commit sha, local HEAD, and both release versions in the deploy report.

Pitfalls:

- Fly secrets may stage without applying; check `flyctl secrets list` and redeploy to apply (see Auth Gate).
- Auth middleware must be registered after CORS so preflight never reaches auth.
- Do not re-seed or rebuild data as part of a deploy.

## Testing

- System eval: `node dist/evals/system-eval.js` (26/26)
- Memory-types eval: `node dist/evals/memory-types-eval.js` (71/71)
- KG eval: `node dist/evals/kg-eval.js` (21/21)
- KG quality eval: `node dist/evals/kg-quality-eval.js` (20/20)
- Extraction eval: `node dist/evals/extraction-eval.js` (31/31 with Haiku)
- Hard test: `node dist/evals/hard-test.js` (15/15)
- Super-hard test: `node dist/evals/super-hard-test.js` (17/17)
- Document-mode eval: `node dist/evals/document-mode-eval.js` (22/22 checks, 4/4 scenarios)
- MCP protocol test: `npm run test:mcp` (8/8 passed)
