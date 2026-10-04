---
name: kelly-seo
description: SEO + GEO (AI-search) + brand-entity desk (Busabase App-in-Skill) — wired to Google Search Console for a dashboard over search analytics and an agent-prepared SEO opportunities review queue, plus an AI-visibility tracker (are we cited in ChatGPT / Perplexity / Gemini / Claude / Copilot answers), a GEO content-optimization queue gated by geo-qa, and an entity / knowledge-panel readiness checklist. Use when the user invokes $kelly-seo or /kelly-seo, mentions SEO, Google Search Console, GSC, search analytics, search performance, queries, keywords, rankings, positions, impressions, clicks, CTR, striking-distance queries, title/meta rewrites, content briefs, internal links, SEO opportunities review, GEO, generative engine optimization, AI search, AI visibility, being cited by AI answer engines, ChatGPT/Perplexity/Gemini/Claude/Copilot citations, brand entity, knowledge panel, Wikidata, schema.org, or entity readiness.
metadata:
  category: growth
  tags:
    - risk:local-write
    - surface:busabase
    - surface:gsc
  busabase:
    template: true
    folderSlug: kelly-seo
    resources:
      - sites
      - queries
      - pages
      - opportunities
      - geo-opportunities
      - ai-visibility
      - entity-signals
      - settings
    risk: local-write

---

# Kelly SEO

## Overview

Use this skill as Kelly's SEO + GEO desk. A Busabase-backed App-in-Skill
holds Google Search Console search analytics (clicks, impressions, CTR,
position for queries and pages across configured site properties) and an
agent-prepared SEO opportunities review queue: title/meta rewrites,
internal-link suggestions, new-content briefs, and page-issue fixes that the
user approves, edits, or blocks.

It also covers the AI-search side (GEO — Generative Engine Optimization): an
AI-visibility tracker showing whether AI answer engines (ChatGPT /
Perplexity / Gemini / Claude / Copilot) cite the brand for a set of tracked
prompts, a GEO content-optimization review queue (agent-drafted rewrites
that make a page more citable, each scored by the `geo-qa` quality gate),
and a brand-entity / knowledge-panel readiness checklist (Wikidata,
schema.org Organization/Person, consistent NAP, sameAs links). GEO
opportunities and entity signals flow through the same Busabase Bases and
the same five-state review model as SEO opportunities.

Pulling Search Console analytics is a genuine external operation a browser
cannot perform (it needs a Google service-account key or OAuth token):
`scripts/sync_gsc.mjs` is the only place analytics data enters the system.
The AirApp itself only reads Busabase and writes review decisions (approve /
request changes / block / revise) directly onto the opportunity, GEO
opportunity, or entity-signal record; `scripts/execute_decisions.mjs`
records the planned follow-up for approved SEO opportunities, and the agent
performs the actual site edit outside the app after explicit approval.

Default behavior is AirApp-first. Unless the user explicitly asks only for
explanation, sync what's due and give the user the clickable AirApp URL (or
the local preview URL when local preview is explicitly requested). Use
chat-only mode only when the user says "纯聊天", "chat only", "不要打开 UI",
or similar.

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Kelly SEO overview"></td>
    <td width="50%"><img src="assets/screenshots/queries.webp" alt="Kelly SEO queries"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Search Console KPI cards with daily clicks/impressions chart, top movers, and per-site freshness.</td>
    <td><strong>Queries</strong><br>Top queries with clicks, impressions, CTR, position, period deltas, and opportunity badges.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/pages.webp" alt="Kelly seo pages"></td>
    <td width="50%"><img src="assets/screenshots/opportunities.webp" alt="Kelly seo opportunities"></td>
  </tr>
  <tr>
    <td><strong>Pages</strong><br>Page-level click and impression table with top growth and decline movers for prioritizing content updates.</td>
    <td><strong>Opportunities</strong><br>Ranked SEO opportunity queue with impact, effort, evidence, and recommended next actions.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/geo.webp" alt="Kelly SEO AI visibility"></td>
    <td width="50%"><img src="assets/screenshots/optimize.webp" alt="Kelly SEO GEO optimizer"></td>
  </tr>
  <tr>
    <td><strong>AI visibility (GEO)</strong><br>An engines×prompts matrix of where the brand is cited across ChatGPT, Perplexity, Gemini, Claude, and Copilot, with an overall visibility score and trend.</td>
    <td><strong>GEO optimizer</strong><br>Agent-proposed rewrites that make pages more citable by AI engines, gated by geo-qa — one blocked for a fabricated stat.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/entity.webp" alt="Kelly seo entity readiness"></td>
  </tr>
  <tr>
    <td><strong>Entity readiness</strong><br>Entity readiness checklist showing schema coverage, citation signals, and blocked/ready status for AI answer engines.</td>
  </tr>
</table>

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual quality, responsive layout, and the complete canonical `content/kelly-seo-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery, ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's artifact and product contracts, stop before the unavailable Busabase operation, and report the exact missing dependency. Do not invent a second data backend.

## Boundary

- Pulling Search Console data is a trusted-script-only operation:
  `scripts/sync_gsc.mjs` calls the read-only GSC API and writes normalized
  site/query/page records into Busabase. It never mutates Search Console
  properties, submits sitemaps, or requests indexing.
- The AirApp reads and writes Busabase records only. It never calls the GSC
  API, edits site content, or mutates any remote system.
- Site-content edits happen only through approved opportunities, executed by
  the agent OUTSIDE the app (editing the site's repo/CMS), after
  `scripts/execute_decisions.mjs` marks the opportunity `ready_for_agent`.
  GEO content changes follow the same rule: approved in `#/optimize`,
  published by the agent outside the app.
- AI-visibility data is observational: the agent gathers whether engines
  cite the brand and writes it into the `ai-visibility` Base directly (via
  `busabase-sdk`, following `references/seo-schema.md`'s field slugs). Never
  fabricate a citation, an answer position, or a stat — the `geo-qa` gate
  BLOCKs ungrounded claims for exactly this reason.
- No Google credentials live in this repo. The service-account key path or
  OAuth token is referenced by env var name only (`KELLY_SEO_GSC_SERVICE_ACCOUNT_FILE`,
  `KELLY_SEO_GSC_ACCESS_TOKEN`). Never commit `config.local.json`, env files,
  service-account keys, or access tokens.

## Busabase Resources

Eight Bases under one application Folder (`kelly-seo`), declared in
`content/kelly-seo-app/app/js/config.js` and the generated template sidecars under `content/`:

- `sites`: configured Search Console properties with 28d totals and a daily trend series, synced by `scripts/sync_gsc.mjs`.
- `queries`: top queries with deltas, opportunity badges, top pages, and a trend series (capped at 100 rows by clicks).
- `pages`: top pages with deltas, indexing/canonical issues, top queries, and a trend series (capped at 100 rows by clicks).
- `opportunities`: the SEO review queue — title/meta rewrite, internal links, content brief, or page-issue fix, with the human decision and execution marker on the same row.
- `geo-opportunities`: the GEO content-optimization review queue — citable rewrite, quotable stats, Q&A block, or schema markup, gated by `geo-qa` (recomputed live from the draft on every read).
- `ai-visibility`: tracked AI-answer-engine prompts with per-engine mentions and a visibility trend.
- `entity-signals`: the brand-entity / knowledge-panel readiness checklist.
- `settings`: one row (`record-id: "config"`) with the brand, GSC sync window/read-only config, last-sync range, warnings, and the AI-visibility score baseline.

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space; see `references/seo-schema.md` for exact
field shapes. Metrics, the AI-visibility score, and the entity-readiness
score are recomputed client-side from the stored rows on every read
(`content/kelly-seo-app/app/js/seo-model.js`'s `buildSnapshot`/`assembleSnapshot`), so the
desk is always fresh regardless of when a browser session loads it relative
to the last sync.

## First Run And Onboarding

On invocation, check the `sites` Base. If it is empty, guide setup before
syncing real data: ask which site properties to track (`property_url`, a
short `site_id`, verification type) and which auth method to use. Never ask
the user to paste keys or tokens into chat.

Private config priority (read only by the trusted `scripts/sync_gsc.mjs`,
never by the AirApp):

1. `KELLY_SEO_CONFIG=/absolute/path/to/config.json`
2. `skills/kelly-seo/config.local.json`
3. `~/.config/kelly-seo/config.json`

Env priority:

1. Existing environment variables
2. `KELLY_SEO_ENV_FILE=/absolute/path/to/.env`
3. Repository root `.env`
4. `skills/kelly-seo/.env.local`
5. `~/.config/kelly-seo/.env`

`config.local.json` shape: `{ "sites": [{ "site_id", "property_url", "verification_type" }], "auth": { "method", "service_account_file_env", "access_token_env" }, "sync": { "window_days", "row_limit" } }`.

Auth methods (choose one):

- Service account (recommended for recurring syncs): the user creates a Google Cloud service account, downloads its JSON key, and adds the service account's email address as a user on each Search Console property (Settings → Users and permissions → Add user, Full or Restricted read access). Point `KELLY_SEO_GSC_SERVICE_ACCOUNT_FILE` at the key file path in a local env file.
- Plain OAuth access token (for quick manual runs): put a short-lived token with scope `https://www.googleapis.com/auth/webmasters.readonly` in `KELLY_SEO_GSC_ACCESS_TOKEN`.

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL.
Start `pnpm --dir content/kelly-seo-app dev` only when local preview/debugging is explicitly
requested.

Required app views (hash routes):

- `#/overview`: SEO command desk. Per-site KPI cards (clicks, impressions, CTR, average position, 28d vs previous 28d deltas), a daily clicks/impressions trend, top movers (queries with the biggest click gains and losses), site freshness (last sync), and the human-attention panel for opportunities needing review.
- `#/queries`: top queries table with clicks, impressions, CTR, position, deltas vs the previous period, and opportunity badges such as "position 8-15" or "CTR below expected". Selecting a row opens `#/queries/<id>` with a per-query trend, top pages for the query, and agent notes.
- `#/pages`: top pages table with URL, clicks, impressions, CTR, position, deltas, and indexing/canonical warnings when present. Detail at `#/pages/<id>` shows the per-page trend and top queries for the page.
- `#/opportunities`: review queue with workflow states `needs_review`, `changes_requested`, `approved`, `done`, and `blocked`. Each agent-proposed action (title/meta rewrite with draft, internal-link suggestion, new-content brief, fix-page issue) carries a reason, expected impact, an editable draft, decision buttons (approve / request changes / block), a `Review note` textarea, and a stable reference such as `Opportunity #1`. Decisions write directly onto the opportunity record through `busabase-sdk`.
- `#/geo`: AI-visibility tracker. An engines × prompts matrix showing, for each tracked prompt, which AI answer engines (ChatGPT / Perplexity / Gemini / Claude / Copilot) cite the brand, at what answer position, with what sentiment and cited page, plus an overall AI-visibility score and a visibility-over-time trend.
- `#/optimize`: GEO content-optimization review queue with the same `needs_review / changes_requested / approved / done / blocked` states. Each agent-proposed change (citable rewrite, quotable stats, Q&A block, schema markup) carries a target prompt, reason, expected impact, an editable draft, kb-style grounding lines, and a live `geo-qa` gate verdict (SHIP / FIX / BLOCK). A change the gate BLOCKs (for example a fabricated stat) cannot be approved until the failing checks are resolved.
- `#/entity`: entity / knowledge-panel readiness checklist of brand-entity signals (Wikidata entity, Wikipedia/notability, schema.org Organization, sameAs links, consistent NAP, founder/person entity) with a present / partial / missing status, an agent-proposed fix for each gap, and an overall readiness score.
- `#/sites`: configured properties with property URL, verification type, last sync, and 28d totals per site. The site switcher filters overview/queries/pages.
- `#/settings`: sanitized config summary — brand, locale, sync window/row-limit/read-only, read live off the Settings Base.

Demo mode:

- `?demo=1` opens a deterministic mock SEO desk ("Featherlog" persona) for documentation and screenshots.
- `?demo=overview`, `?demo=queries`, `?demo=pages`, `?demo=opportunities`, `?demo=geo`, `?demo=optimize`, `?demo=entity`, and `?demo=detail` select named mock scenes.
- `lang=en` or `lang=zh` forces UI chrome language for screenshots.
- Demo mode never reads or writes Busabase. Decisions stay in the browser only.

UI language: support English and Chinese chrome with `Auto` default. Keep queries, page URLs, and imported search data in their original language.

## Sync Workflow

1. Detect mode. Default to AirApp.
2. Load private config. If `config.local.json` is missing, enter onboarding.
3. If the user asks to sync, confirm the scope: which properties and the date window (default last 28 days plus the previous 28 days for deltas).
4. Run `node skills/kelly-seo/scripts/sync_gsc.mjs`. The script pulls Search Analytics dimensioned by query, by page, and by date for both windows, normalizes and upserts `sites`/`queries`/`pages` into Busabase (capped at the top 100 queries/pages by clicks — `records.list`'s server-side limit), and merges the sync-owned fields (window/row-limit/range/warnings) onto the `settings` row. It never touches `opportunities`, `geo-opportunities`, `ai-visibility`, or `entity-signals`.
5. Give the user the AirApp URL.
6. GSC data lags about two days; the sync window ends two days before today. Surface API errors and missing-property warnings in `settings.warnings`, never as silent failures.

`scripts/sync_gsc.mjs` fails gracefully with setup guidance when neither `KELLY_SEO_GSC_SERVICE_ACCOUNT_FILE` nor `KELLY_SEO_GSC_ACCESS_TOKEN` is usable. It is never required for demo mode or app startup.

## Opportunities Workflow

1. After a sync, analyze the `queries`/`pages` Bases for striking-distance queries (position 8-15), CTR below the expected curve for the position, pages losing clicks, internal-link gaps, and page issues. Write proposed actions into the `opportunities` Base with stable ids, sequential `ref` numbers, a reason, an expected impact, and an editable draft (via `busabase-sdk`, following `references/seo-schema.md`).
2. Send the user to `#/opportunities` to review. The user approves, edits drafts, requests changes with a note, or blocks — each verdict writes `status`/`decision-action`/`decision-note`/`decision-draft`/`decided-at` directly onto the opportunity record.
3. On explicit user request to execute, run `node skills/kelly-seo/scripts/execute_decisions.mjs` (dry-run by default). It re-reads `status: "approved"` opportunities and, with `--apply`, writes `execution-status: "ready_for_agent"` plus the concrete operation (`rewrite_title`, `add_internal_links`, `create_content_brief`, `fix_page_issue`) and target — no external side effects either way.
4. The agent then performs the approved edits in the site's repo/CMS outside the app, and marks the executed opportunity `status: "done"` by writing the field directly (via `busabase-sdk`).

## GEO (AI-search) Workflow

1. GEO state lives in the `ai-visibility` (tracked prompts × engines with position + sentiment + trend), `geo-opportunities` (agent-proposed citable rewrites), and `entity-signals` (the readiness checklist) Bases. Route all reads/writes through `busabase-sdk` — never bypass it.
2. For each agent-proposed GEO change written to `geo-opportunities`, the `geo-qa` gate (`evaluateGeoGate()` in `content/kelly-seo-app/app/js/seo-model.js`) is recomputed live from `draft`/`claims`/`has-schema`/`has-qa-block` on every read — it returns SHIP / FIX / BLOCK with a GEO Quality Score and per-check notes. The primary failure is an ungrounded/fabricated stat — a number in the copy with no matching entry in `claims` carrying a `source`. A BLOCK is a hard gate: the app rejects an approve before any write until the change is fixed.
3. Send the user to `#/optimize` to review. Approvals write `status`/`decision-*` directly onto the GEO opportunity record. Execution semantics: `operation: publish_geo_change` — the agent publishes the approved citable content in the site's repo/CMS OUTSIDE the app, then marks the item `done` by writing the field directly.
4. Entity-readiness edits from `#/entity` write `status`/`detail` directly onto the `entity-signals` record. The agent then earns the real signal (create the Wikidata item, add the sameAs links, standardize the brand name) outside the app.
5. Never invent an AI-visibility number, a citation, or a stat. If a claim in a GEO draft is not grounded in a real source, the gate must BLOCK it — do not ship content that an AI engine would then quote verbatim.

## Safety Defaults

- Treat anything that changes live site content, metadata, redirects, canonical tags, or robots rules as approval-required via the opportunities queue.
- Prefer the read-only GSC scope; never store key file contents or tokens in Busabase, logs, UI state, or reports — expose only env readiness booleans.
- Keep stored data minimal: top queries/pages and aggregates, not raw exports beyond what the dashboard needs.
- Use stable ids and refs so repeated syncs and executions are idempotent.
- If GSC totals and per-dimension rows disagree (sampling/privacy filtering), do not invent corrections; add a `settings.warnings` entry explaining the gap.
