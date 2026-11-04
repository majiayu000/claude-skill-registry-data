---
name: jc-backend-develop
description: Use when building new features, endpoints, services, or entities in the JapaConnect Go backend (github.com/jedafe/japa). Covers the layered architecture (Handlers→Services→Stores), the Spec-Readiness and Contract-Delivery Gates, full RBAC CRUD delivery per entity, sqlc/pgx patterns, and catalog maintenance.
---

# JapaConnect Backend — Development Skill

Go monolith serving all five frontend apps at `/api/v1`. Module: `github.com/jedafe/japa`.

## ⛔ GATE 1 — SPEC-READINESS (Run Before Any Implementation)
Before writing code for any feature:
1. Locate the governing JEOS section doc and/or ADR for the feature.
2. If no spec exists, or the spec conflicts with what's being asked: STOP and output:
```
⚠️ MISSING/CONFLICTING SPEC — implementation paused
Feature: [name]
Issue: [no JEOS section covers this | conflicts with ADR-0XX | conflicts with section XX]
Action needed: create/update the JEOS spec (and ADR if architectural) before backend work continues.
```
Architectural decisions made mid-implementation without an ADR are spec drift — the exact failure mode JEOS audits exist to catch.

## ⛔ GATE 2 — CONTRACT-DELIVERY (The Mirror of the Frontend Gates)
The frontend agents STOP when routes are missing. Your job is to make sure they never stop. **Every new entity ships with the complete contract or it doesn't ship:**

1. **Full RBAC CRUD route set** (non-negotiable — super-admin must be able to manage every entity):
   - `GET /api/v1/admin/[entity]` — list with `?page=&limit=&sort=&q=&filter=` (offset pagination + meta for admin tables)
   - `GET /api/v1/admin/[entity]/:id` · `POST` create · `PATCH /:id` update · `DELETE /:id`
   - **Both directions of every state transition**: `POST /:id/suspend` AND `/:id/unsuspend`, `/ban` AND `/unban`, `/approve` AND `/reject`, etc.
   - Bulk endpoints where the DataTable spec needs them: `POST /api/v1/admin/[entity]/bulk` with `{action, ids}`
   - Readonly/log entities still get `DELETE /:id` and `POST /clear` (all / older-than)
2. **RBAC permission nodes seeded** — one node per action (`[entity].list`, `.view`, `.create`, `.update`, `.delete`, `.suspend`, `.ban`, …) added to the seed migration AND registered in the RBAC middleware. *Regression anchor BE-005: 174 of 249 nodes were once missing from seed. Never partially seed.*
3. **Catalogs updated in the same PR** — `api-routes-catalog.md` (new routes), `valkey-keys.md` (new `jc:` keys), `system-settings.md` (new keys), `asynq-tasks.md` (new tasks). An uncatalogued route is invisible to the frontend gates and therefore doesn't exist.

If any part of the contract can't be delivered (e.g. spec ambiguity on a state transition): STOP + output:
```
⛔ INCOMPLETE CONTRACT — implementation paused
Entity: [entity]
Undeliverable: [e.g. unclear whether orgs support suspend; bulk action semantics undefined]
Action needed: [decision required]
```

## Architecture (Layered — Never Skip Layers)
```
Handler (Chi)  →  Service (business logic)  →  Store (sqlc-generated)  →  PostgreSQL 18
     ↓                    ↓
Middleware chain     Asynq enqueue (side effects)
```
- **Handlers**: parse/validate input, call ONE service method, render response. No business logic, no direct store calls.
- **Services**: business logic, transaction boundaries, orchestration across stores, enqueue Asynq tasks.
- **Stores**: sqlc-generated only. Hand-written SQL goes in `.sql` query files → `sqlc generate`. Never string-concatenate SQL.
- **Middleware order**: RequestID → RealIP → Logger → Recoverer → Tenant → GeoIP → VisitorContext → Auth → RBAC → RateLimit → Handler.
  - **GeoIP** (Section 37): MaxMind GeoLite2 in-process, attaches `GeoContext{CountryCode, City, ...}` to ctx.
  - **VisitorContext** (ADR-064): runs immediately after GeoIP; synthesizes `GeoContext` + `user_profiles.field_values` (`japa_status`, `destination_country`) + resolved language into `VisitorContext{OriginCountry, CurrentCountry, DestinationCountry, JapaStage, Archetype, ContentCountry, Confidence}`. Cached at `jc:visitor:ctx:{session_id}` (30-min TTL). Gated by `system_settings.geo_personalization.enabled`.

## Stack (Non-Negotiable)
Go (latest stable) · Chi router · sqlc + pgx/v5 (pool via `pgxpool`) · Asynq (Valkey-backed, three tiers: critical/default/low) · PostgreSQL 18 · Valkey (keys namespaced `jc:`) · Meilisearch 1.45 · SeaweedFS (S3 API) · imgproxy · Honcho (AI memory, separate logical DB, same PG instance) · GlitchTip via sentry-go · golang-migrate · `slog` structured logging · env vars `JC_` prefixed, typed config, missing-required exits at boot.

## Response Contract (What the Frontends Consume)
- Success: `RenderJSON(w, status, data)` · Lists: `RenderPaginated(w, data, meta{total,page,limit})` or cursor meta for feeds
- Errors: `RenderError(w, status, code, message)` — machine code + human message; the frontend surfaces `message`
- Validation errors: 422 with per-field map · AuthN 401 · AuthZ 403 · not found 404 — never 500 for expected conditions
- All timestamps RFC 3339 UTC · IDs as strings in JSON

## Mandatory Patterns
- **Wallet/credits**: append-only immutable ledger, balance = SUM; every spend inside a tx holding `pg_advisory_xact_lock(user_id)`. Never a mutable balance column. *(Regression anchor: double-spend defect.)*
- **Revenue splits (ADR-063)**: `revenue_splits` is an **immutable audit record** — append-only, never UPDATE. Each paid enrollment or Pro-stream accrual writes one row with the exact percentages/amounts applied at the time. `academy:process_enrollment` is **idempotent on payment_id** (guard against double-credit, cf. AUDIT-BE-005). Payout execution (`academy:send_instructor_payout`) mirrors the wallet double-spend guard: advisory lock on instructor_id inside the tx, stamp splits with `payout_id` only after transfer succeeds.
- **Render-time resolution (ADR-052)**: coupon embeds/affiliate links store entity IDs only; resolve codes/URLs/expiry at render time; fail closed on inactive.
- **Idempotency**: webhook handlers and payment callbacks guard with Valkey `SET NX` on an idempotency key.
- **Geo-aware personalization (ADR-064)**: `VisitorContext.ContentCountry` is the default for all `?geo=` surfaces (trending §53, search §13, feed §32, discovery). Explicit `?geo=` always wins; absent param → `ContentCountry`. Feed score gets a **bounded** geo-relevance multiplier (cap so it re-weights, never dominates). Search passes `ContentCountry` as a boost/optional-filter on the `relevant_countries` Meilisearch attribute. **Never hard-filter by geo** — re-weight only. User override: `user_profiles.content_country_preference` (nullable ISO code) wins over resolved. Killswitch: `system_settings.geo_personalization.enabled`.
- **University space type (Section 39)**: universities are `space_type = 'university'` spaces with the `university_fields` custom field group. Auto-seeded on first deploy from `db/seed/universities.json`; logo fetch via `university:fetch_logo` (low tier). Admin CRUD + CSV bulk import. Discovery routes at `/api/v1/universities` (public) and `/api/v1/admin/universities` (admin). The `logo` field doubles as the university page's profile image (Section 34 media + imgproxy).
- **Uploads**: MIME sniffed from content (not extension), size-capped, stored to SeaweedFS, served via imgproxy URLs.
- **Tenancy**: tenant middleware resolves host → tenant_id into context; stores filter by it.
- **GDPR/NDPR erasure**: user deletion cascades through owned data AND calls the Honcho deletion API — required, not best-effort. **Japa Academy**: `academy_instructor_profiles`, `revenue_splits`, and `academy_instructor_payouts` are user-owned — erasure must cascade through them. `revenue_splits` are financial audit records: anonymize the instructor reference, never delete the split row (regulatory retention).
- **Search**: writes that affect searchable entities enqueue a Meilisearch sync task (default queue) — never sync inline. Content documents gain a `relevant_countries` filterable attribute (array of ISO codes from geo spaces/tags) for ADR-064 search weighting.
- **Errors**: wrap with `fmt.Errorf("...: %w", err)`; unexpected errors captured to GlitchTip with request context. *(Regression anchor BE-002: GlitchTip must actually be wired.)*
- **TipTap content**: stored as JSON, rendered to HTML server-side, cached in Valkey.

## Testing Expectations
Table-driven tests for services · `httptest` for handlers (auth + RBAC denial cases included) · a failing-permission test per new permission node · store tests against a real PG (dockertest or test DB) for tx-sensitive logic (wallet, claims).

## Japa Academy Entities (ADR-063 — Section 36 extension)
When building Japa Academy creator-economy features, the entity set is:
- **`academy_instructor_profiles`** — one per user per tenant. `status ∈ pending|approved|rejected|suspended` (gated application). `tier ∈ standard|verified|partner`. Optional `commission_pct_override`. `payout_method` (jsonb, encrypted at app layer). `kyc_status`. Full RBAC CRUD + both-direction state transitions (approve/reject, suspend/unsuspend).
- **`revenue_splits`** — immutable per-event record (`creator_pct`/`platform_pct`, amounts, `source ∈ purchase|pro_stream`). Links to `enrollment`/`payment` in and `payout` out. **Append-only — never UPDATE.**
- **`academy_instructor_payouts`** — one per instructor per period; gross/commission/net; `status ∈ pending|processing|paid|failed`. State transitions: `pending→processing→paid` or `→failed`.
- **`academy_tracks` columns**: `instructor_id` (null = platform course), `price_kobo` (null = free/Pro-only), `currency`, `is_published_to_academy` (marketplace visibility, distinct from `is_published`), `category`, `language`, `total_enrolled` (cached counter).
- **`enrollments` column**: `payment_id` (nullable FK → `payments`; null for free/Pro/pro_stream).
- **Course reviews**: reuse polymorphic `reviews` table (Section 29) with `entity_type = 'academy_track'`. No `course_reviews` table.
- **Migration**: `000166` (Japa Academy tables + columns), `000167` (`user_profiles.content_country_preference` for geo).
- **5 new Asynq tasks**: `academy:process_enrollment` (critical), `academy:calculate_period_payouts` (scheduled, low), `academy:send_instructor_payout` (critical), `academy:notify_instructor_approved` (default), `academy:notify_course_approved` (default). Plus `university:fetch_logo` (low) for university space seeding.
- **12 new RBAC nodes**: `university.instructor.*`, `university.course.*`, `university.payout.*` — seed completely (BE-005).
- **7 new settings**: `university.default_commission_pct`, `university.verified_tier_commission_pct`, `university.partner_tier_commission_pct`, `academy.pro_stream_rate_kobo`, `university.payout_min_threshold_kobo`, `university.payout_period_days`, `university.surface_domain`.
- **4 new Valkey keys**: `jc:visitor:ctx:{session_id}` (30-min TTL, shared with geo), `jc:uni:instructor:{user_id}` (instructor profile cache), `jc:uni:payout:period:{instructor_id}:{period}` (payout lock), `jc:uni:enrollment:processed:{payment_id}` (idempotency guard).

## Deliverables Per Task
1. Gate 1 + Gate 2 output · 2. migration pair if schema changes (invoke `jc-backend-migrate`) · 3. sqlc queries + `sqlc generate` · 4. store/service/handler code · 5. routes registered + RBAC nodes seeded · 6. Asynq tasks (invoke `jc-backend-worker`) · 7. all catalogs updated · 8. tests · 9. `go build ./... && go vet ./...` clean (run locally via Claude Code — no Go toolchain in chat sessions).
## V2 Mandatory Patterns (Phases 41–50)

### AI Personas (§68, ADR-068)
- Persona provisioning is **transactional**: create `users` (is_bot=true) + `professional_profiles` + `ai_personas` in one tx. Partial provision is a data integrity failure.
- `disclosure_mode` controls public rendering only. `is_bot=true` is permanent — never flip it, never expose it publicly.
- Every persona action writes `platform_events.is_synthetic = true`. This is non-negotiable and cannot be disabled by any setting.

### RAG Layer (§69, ADR-069)
- `content:generate_embedding` UPSERTS into `content_embeddings` (never raw INSERT — re-indexing a document must replace its chunks, not add duplicates).
- Text extracted from TipTap JSON before embedding — strip block structure to plain text first (utility function, not inline in task).
- Retrieval at `/ai/chat` is gated by `rag.enabled` system setting — fall back to non-RAG LLM call if false.
- Persona-authored content is indexed exactly like human-authored content (it passed HITL review).

### Content Studio (§75, ADR-076)
- `content.generate_draft` with `studio_job_id` must be idempotent on that ID — guard against re-running an already-generated job.
- AI-populated custom fields: if required fields are missing from model output, set `field_validation_warning = true` on the job. **Never block publish** — the human reviewer has final say.
- `studio.auto_publish_types` is checked at routing time. Guide categories `visa`, `banking`, `grants`, `health_insurance`, `admission` are hardcoded to always require review — this check must be in code, not configurable.

### Participation Orchestration (§76, ADR-077)
- Orchestration actions are dispatched as the persona's backing account through **existing** action endpoints — no new action routes. The backing account must have the correct RBAC permission nodes to perform each action type.
- Daily action counters: Valkey keys `jc:persona:daily:{persona_id}:{date}:{action_type}` with TTL until midnight UTC. Counter overflow (exceeding budget) = skip the action entirely, do not error.
- Run-lock `jc:persona:lock:{persona_id}` (5-min TTL SET NX) prevents concurrent orchestration runs for the same persona.
- High-stakes gate is in task code: check parent content's guide_category or system tags BEFORE generating action content — don't waste AI gateway tokens on content that will route to review anyway.

### Remittance Tracker (§74, ADR-075)
- `api_config` JSONB on `remittance_providers` contains API credentials — encrypt at application layer (same pattern as payment provider secrets, §17). Never log or expose in responses.
- Rate history is append-only (new row per fetch). `remittance:prune_old_rates` is the cleanup mechanism — never delete rows inline in the fetch task.
- Provider adapter interface (`RateProvider`) must have a timeout and return an error on rate-fetch failure — the main task catches errors per-provider and logs to GlitchTip, never fails the whole batch.

### Newsletter (§62, ADR-080)
- Unsubscribe is token-based (`newsletter_unsubscribe_tokens`) — no auth required. Token must be single-use (delete after use) and short-circuit on invalid/expired token (404, not error).
- Bounce and complaint webhooks from the email provider MUST update `newsletter_subscribers.status` — undeliverable addresses that keep receiving email are a deliverability risk.

### V2 Community Features & Functional Tools (Phases 48–50, §§79–102)

#### Geo-Aware Tool Pattern (§§79–101, `.jeos/skills/geo-aware-tool-pattern.md`)
- **Destination country is the primary data axis** — every v2 functional tool (§§90–101) filters by destination country. No hardcoded nationality anywhere in query/store/service code.
- **`?dest=` filter** on all list endpoints for §§79–101 — public and admin. The filter accepts an ISO 3166-1 alpha-2 country code. Absent `?dest=` returns global/cross-destination results where sensible, but the filter must always be honored when present.
- **`destination_country_id` in schema** — every v2 functional tool table includes a `destination_country_id` FK to `countries`. This is the join axis for geo-filtering, not a nullable attribute.
- **Destination selector is the first UI input** — the frontend renders a destination country picker before any other filter on v2 tool surfaces. The backend must accept `destination_country_id` as the primary query parameter and return 400 if it's required but absent (tool-specific — some tools allow browsing without a destination, others require it).
- **Feature-flag middleware returns 404 (not 403) when disabled** (ADR-042): when a v2 feature flag is off, the middleware returns 404 Not Found, not 403 Forbidden. This prevents leaking the existence of disabled features to unauthorized users. Verify the feature-flag middleware path returns 404 for all §§79–102 routes.
- **RBAC seed migration naming**: `000NNN_seed_{feature_domain}_rbac_nodes.sql` — each v2 feature domain gets its own dedicated RBAC seed migration with this naming convention (e.g. `000180_seed_story_rbac_nodes.sql`, `000181_seed_wiki_rbac_nodes.sql`). Never batch multiple feature domains into one seed migration.
- **Admin list endpoints** for all v2 entities support `?filter=&sort=&paginate=` (filter + sort + paginate) — same DataTable contract as v1 admin endpoints. No v2 admin list endpoint ships without all three.

#### ADR-088 Universal AI Content Generation
- **Standard columns on all admin-managed content tables** for §§79–101: `ai_generated` (boolean, default false), `ai_model` (text, nullable — model identifier when AI-generated), `hitl_reviewed_by` (uuid, nullable FK → users — the admin who reviewed), `ai_generated_at` (timestamptz, nullable). These four columns are mandatory on any table where content can be AI-drafted.
- **AI generation via existing §20 Gateway** — no new AI client or provider wiring. All AI content generation (story drafts, wiki article drafts, scam alert summaries, digest text, etc.) goes through the existing AI Gateway abstraction. Never call an LLM provider directly from a service or task.
- **HITL review is mandatory before publish** — AI-generated content cannot be published without a human reviewer. The `hitl_reviewed_by` column must be non-null and `hitl_reviewed_at` set before `is_published = true`. The publish endpoint must reject if `ai_generated = true AND hitl_reviewed_by IS NULL`.
- **`is_japabot_indexed`** on RAG-retrievable content — content that should appear in Japabot search results (wiki pages, guides, stories) gets `is_japabot_indexed = true` after HITL approval. This flag gates the `content:generate_embedding` task — unindexed content is never embedded.

#### Community Features Reusing `contents` Table (§§79–89, §98)
- Community features (Community Story Wall §79, Achievement Feed §88, Service Directory §98) **reuse the existing `contents` table** with `content_type` discriminators (`story`, `achievement`, `service_listing`) — **do not create separate top-level tables** for these content types.
- Extension tables (`story_meta`, `achievement_meta`, `service_listing_meta`) hold type-specific columns and link back to `contents.id`. The discriminator column on `contents` drives which extension table to join.
- This pattern keeps the content pipeline (search indexing, embedding, geo-tagging, media) unified — no parallel infrastructure for community content.

#### Mentorship Matching (§102, ADR-110)
- **`active_mentee_count` is maintained by a PostgreSQL trigger** (`trg_mentee_count`), not computed at query time. The trigger fires on INSERT/UPDATE/DELETE of `mentorship_connections` where `status = 'active'` and adjusts the mentor's `active_mentee_count` accordingly. Never compute this count with a subquery or `COUNT(*)` in a read path — read the cached column.
- **Match scoring: 60% keyword overlap + 40% pgvector cosine similarity**. The matching algorithm combines keyword overlap (on mentor/mentee profile tags and bio tokens) with pgvector cosine similarity (on profile embeddings). The weights are 60/40 — verify the scoring function applies these exact weights, not configurable ones.
- **Asynq tasks**: `mentor:generate_embedding` (low queue — generates pgvector embedding from mentor/mentee profile text) and `mentor:update_meilisearch` (low queue — syncs mentor profiles to Meilisearch for search). Both must be registered and wired.
- **DM auto-open on accept** (§48 integration): when a mentorship connection transitions to `status = 'accepted'`, a DM conversation is auto-created and auto-opened for both parties. This is the §48 DM system — no new messaging infrastructure.

#### New Asynq Tasks for §§79–102
| Task | Queue | Schedule | Notes |
|---|---|---|---|
| `visa_timeline:refresh_stats` | default | nightly | Recomputes visa timeline aggregate stats |
| `visa_timeline:prompt_update` | default | weekly | Prompts users with stale timelines to update |
| `digest:generate` | default | weekly | Generates community digest draft content |
| `digest:send_email` | default | on publish | Sends published digest to subscribers |
| `mutual_aid:expire` | default | nightly | Expires stale mutual aid posts |
| `calendar:staleness_check` | default | nightly | Flags calendar entries not updated within threshold |
| `calendar:send_reminders` | default | daily | Sends upcoming event reminders |
| `planning_group:expire` | default | as needed | Expires inactive planning groups |
| `planning_group:checkin_reminder` | default | as needed | Sends check-in reminders to group members |
| `visa_routes:check_links` | default | weekly | Validates external links on visa route pages |
| `embassy:poll_{slug}` | critical | per embassy | Polls a specific embassy's appointment availability |
| `embassy:dispatch_alerts` | critical | as needed | Sends appointment availability alerts to subscribers |
| `credentials:check_links` | default | weekly | Validates external links on credential checker pages |
| `cv_format:process` | default | on demand | Processes a CV formatting job |
| `cv_format_sessions:purge` | low | nightly | Purges expired CV format sessions |
| `mentor:generate_embedding` | low | on profile change | Generates pgvector embedding from profile text |
| `mentor:update_meilisearch` | low | on profile change | Syncs mentor profiles to Meilisearch |

#### New Valkey Keys for §§79–102
| Key | TTL | Purpose |
|---|---|---|
| `jc:cv_quota` | rolling window | CV formatting quota per user (rate limit) |
| `jc:embassy_avail` | short (per poll cycle) | Cached embassy appointment availability |
| `jc:digest_draft` | draft lifecycle | Community digest draft-in-progress lock |
| `jc:wiki_edit_lock` | edit session timeout | Prevents concurrent edits on a wiki page |
| `jc:ama_active` | AMA session lifetime | Marks an AMA session as active/live |

#### New RBAC Nodes for §§79–102
48 v2 RBAC nodes total across the following domains: `story.*`, `wiki.*`, `scam_alert.*`, `planning_group.*`, `visa_timeline.*`, `digest.manage`, `mutual_aid.*`, `calendar.*`, `profile.japa_stage.edit`, `forum.ama.*`, `achievement.*`, `visa_routes.manage`, `appointment_alert.*`, `embassy_monitor.manage`, `arrival_checklist.manage`, `credential_checker.manage`, `cv_formatter.*`, `housing_guide.manage`, `attestation_guide.manage`, `service.*`, `language_test_hub.manage`, `tax_calculator.manage`, `tax_content.review`, `community_locator.*`, `mentorship.*`. Total RBAC node count: 297 (249 v1 + 48 v2). Seed completely per feature domain (BE-005).
