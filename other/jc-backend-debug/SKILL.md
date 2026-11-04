---
name: jc-backend-debug
description: Use when reviewing or debugging JapaConnect Go backend code (github.com/jedafe/japa). Diagnoses the BE-series defect classes, pgx/sqlc pitfalls, transaction misuse, Asynq wiring, Valkey key issues, and layered-architecture violations.
---

# JapaConnect Backend — Review & Debugging Skill

Conventions and gates: `jc-backend-develop`. Run checks in order.

## 0. Known Defect Classes First (BE-Series Regression Anchors)
These shipped once — check them before anything else when symptoms match:
| Anchor | Symptom | Check |
|---|---|---|
| BE-001 noopEnqueuer | Tasks silently never run (emails, search sync) | Prod wiring injects the REAL Asynq client, not the noop test double |
| BE-002 GlitchTip unwired | Errors vanish, no reports | sentry-go initialized at boot AND error paths actually capture |
| BE-003 migration runner | Schema corrupted after deploy | Runner globs `.up.sql` only; `.down.sql` never applied forward |
| BE-00x wallet race | Negative balances / double-spend | Spend path holds `pg_advisory_xact_lock(user_id)` inside the tx |
| BE-005 RBAC seed gap | 403 on routes that should work | Every permission node the middleware checks exists in seed |
| BE-00x config JSON | JSON-typed settings come back zero-valued | `config.NewSettings` decode path for JSON-encoded values |
| BE-00x revenue split double-credit | Instructor credited twice for one enrollment | `academy:process_enrollment` idempotent on `payment_id` — guard with `jc:uni:enrollment:processed:{payment_id}` SET NX |
| BE-00x payout double-send | Instructor paid twice for same period | `academy:send_instructor_payout` holds advisory lock on instructor_id; stamps splits with `payout_id` only after transfer succeeds |
| BE-00x VisitorContext stale | Geo personalization shows wrong country after preference change | `jc:visitor:ctx:{session_id}` invalidated when `content_country_preference` changes |
| BE-00x geo boost runaway | Local content dominates feed, viral global posts buried | Feed geo boost cap is bounded — verify multiplier doesn't crush engagement/velocity signals |

## 1. Layer Violations
Handler containing business logic or direct store calls · service importing `net/http` · store with hand-concatenated SQL (must be sqlc) · middleware order broken (RequestID → RealIP → Logger → Recoverer → Tenant → GeoIP → VisitorContext → Auth → RBAC → RateLimit → Handler). **GeoIP must run before VisitorContext** (VisitorContext reads GeoContext from ctx); **both must run before Auth** so guest requests get geo personalization.

## 2. pgx / sqlc Pitfalls
- Missing `rows.Close()` / not using sqlc iterators → pool exhaustion under load
- `pgx.ErrNoRows` not distinguished from real errors → 500 where 404 belongs
- Nullable columns scanned into non-pointer/non-`pgtype` fields → silent zero values
- Queries edited in generated `.go` files instead of `.sql` sources (lost on regen)
- `sqlc generate` not re-run after query/schema change → drift between SQL and structs
- Context not propagated (`context.Background()` inside request path kills cancellation)

## 3. Transaction Misuse
- Tx opened in handler instead of service · multiple stores mutated without a shared tx
- `defer tx.Rollback(ctx)` missing after Begin · commit-then-enqueue vs enqueue-then-commit: side-effect tasks enqueue AFTER commit (or use outbox), else tasks fire for rolled-back data
- Advisory locks taken outside the tx (`pg_advisory_lock` vs correct `pg_advisory_xact_lock`)

## 4. HTTP Contract
- Errors leaking internals (`err.Error()` straight to client) instead of `RenderError` code+message
- 500 for expected conditions (missing row, validation) · pagination meta absent on list routes
- Mutating routes missing RBAC middleware — check EVERY POST/PATCH/DELETE has a node check
- Input structs without validation · IDs from URL params unvalidated

## 5. Asynq
Task enqueued but type not registered in the mux (silent dead-letter) · wrong queue tier (payment task on `low`) · non-idempotent handler that retries with side effects · payload struct changed without version tolerance for in-flight tasks.

## 6. Valkey
Keys outside `jc:` namespace · cache set without TTL (unbounded growth) · cache invalidation missing on the write path (stale render cache) · `SET NX` idempotency key without expiry (permanently locked).

## 7. Tenancy & Security
Store queries missing tenant_id filter (cross-tenant leak) · uploads trusting file extension over sniffed MIME · secrets in logs · rate limiting absent on auth/expensive routes. **Japa Academy**: `payout_method` (jsonb) is encrypted at app layer — verify it's never logged or returned in API responses unmasked. `academy_instructor_profiles` tenant-scoped — verify cross-tenant isolation.

## 8. Japa Academy (ADR-063) & Geo-Aware (ADR-064)
- **Revenue splits immutability**: any UPDATE on `revenue_splits` is a defect — append-only, wallet-ledger philosophy. A "correct split amount" fix must be a compensating new row, never an edit.
- **Payout idempotency**: `academy:send_instructor_payout` must be idempotent — check advisory lock on `instructor_id` inside tx, and that splits are stamped with `payout_id` only AFTER the transfer succeeds (not before).
- **Pro stream accrual**: `source='pro_stream'` splits have no `payment_id` — verify they don't trip the payment-id idempotency guard (different guard key).
- **Marketplace publish gate**: catalog reads must filter `is_published_to_academy = true` separately from `is_published` — a course published to the platform but not approved for the marketplace must not appear in the university catalog.
- **VisitorContext cache**: `jc:visitor:ctx:{session_id}` (30-min TTL) — if geo personalization is wrong, check if the cache is stale after a preference change. Invalidation must fire on `content_country_preference` update.
- **Geo killswitch**: `geo_personalization.enabled = false` must make all surfaces fall back to global ranking — verify no code path reads `ContentCountry` without checking the killswitch.
- **University seeding**: `university:fetch_logo` task must store logo to SeaweedFS and set the `logo` field — if university pages show a broken image, check the task completed and the imgproxy URL is generated correctly.

## 9. V2 Community Features, Functional Tools & Mentorship (§§79–102, Phases 48–50)

### Geo-Aware Tool Pattern Bugs (§§79–101)
- **Missing `?dest=` filter**: list endpoints for v2 functional tools (visa routes, embassy alerts, arrival checklists, credential checker, CV formatter, housing guides, attestation guides, language tests, tax calculator, diaspora locator) must accept `?dest=` — if results are not filtered by destination country when the param is present, the store query is missing the `destination_country_id` WHERE clause.
- **Hardcoded nationality**: grep store queries and services for hardcoded country codes (e.g. `WHERE country = 'NG'` or `nationality = 'Nigerian'`) — the geo-aware pattern requires `destination_country_id` as the filter axis, never a hardcoded nationality. Hardcoded nationality in v2 tool code is a spec violation.
- **Missing `destination_country_id` in schema**: if a v2 functional tool table lacks the `destination_country_id` FK column, geo-filtering cannot work — the migration is incomplete. Check the table DDL.
- **Feature-flag returns 403 instead of 404**: when a v2 feature flag is disabled, the middleware must return **404 Not Found**, not 403 Forbidden (ADR-042). A 403 leaks the existence of the disabled feature. If you see 403s on disabled v2 routes, the feature-flag middleware path is wrong.

### ADR-088 AI Content Generation Bugs (§§79–101)
- **Missing HITL review gate**: if AI-generated content can be published without `hitl_reviewed_by` being set, the publish endpoint is missing the guard `ai_generated = true AND hitl_reviewed_by IS NULL → reject`. Test by attempting to publish an AI-drafted, unreviewed record.
- **Missing `ai_generated` columns**: if an admin-managed content table for §§79–101 (story_meta, wiki_pages, scam_reports, digest_editions, visa_routes, housing_guides, etc.) lacks `ai_generated`, `ai_model`, `hitl_reviewed_by`, or `ai_generated_at`, the migration is incomplete — ADR-088 requires all four columns on any table where content can be AI-drafted.
- **Direct LLM provider calls**: if a service or task for §§79–101 calls an LLM provider directly (not through the §20 Gateway abstraction), it bypasses the centralized AI Gateway — route all AI generation through the existing gateway.
- **Missing `is_japabot_indexed` gate**: if unindexed content (where `is_japabot_indexed = false`) is being embedded by `content:generate_embedding`, the task is not checking the flag — RAG retrieval will surface unreviewed AI content.

### Mentorship Bugs (§102, ADR-110)
- **`trg_mentee_count` trigger missing**: if the `active_mentee_count` column on mentor profiles is stale or zero, check whether the PostgreSQL trigger `trg_mentee_count` exists on `mentorship_connections`. The trigger must fire on INSERT/UPDATE/DELETE where `status = 'active'` and adjust the count.
- **`active_mentee_count` computed at query time**: if a read path computes the mentee count with `COUNT(*)` or a subquery instead of reading the cached `active_mentee_count` column, it's a performance defect — the trigger-maintained column exists precisely to avoid this. Grep store code for count queries on `mentorship_connections`.
- **Scoring algorithm wrong**: if mentorship match scores don't match expected results, verify the scoring function applies **60% keyword overlap + 40% pgvector cosine similarity** — not configurable weights, not 50/50, not 70/30. Check the scoring function implementation.
- **`mentor:generate_embedding` not wired**: if match scoring uses pgvector but mentor/mentee profiles have no embeddings, the `mentor:generate_embedding` task may not be enqueued on profile change — check the profile update handler enqueues the task.
- **`mentor:update_meilisearch` not wired**: if mentorship search returns stale results, the `mentor:update_meilisearch` task may not be enqueued on profile change — check the profile update handler enqueues the task.
- **DM auto-open not firing on accept**: if a mentorship connection transitions to `accepted` but no DM conversation is created, the transition handler is missing the §48 DM auto-open integration — verify the handler enqueues DM creation on accept.

### Community Feature `content_type` Discriminator Bugs (§§79–89, §98)
- **Wrong `content_type` value**: if community content (stories, achievements, service listings) doesn't appear in the right views, check the `contents.content_type` discriminator — it must be `story`, `achievement`, or `service_listing` respectively. A typo or NULL value breaks the join to the extension table.
- **Extension table join missing**: if type-specific metadata (story_meta, achievement_meta, service_listing_meta) is absent from API responses, the store query is missing the JOIN on `contents.id` → extension table. The discriminator drives which extension table to join.
- **Separate table created instead of reusing `contents`**: if a new top-level table was created for community content instead of using the `contents` table with a discriminator, it's an architecture violation — community features must reuse `contents` to keep the content pipeline unified.

### New Asynq Task Debugging (§§79–102)
- **`visa_timeline:refresh_stats` / `visa_timeline:prompt_update`**: if visa timeline stats are stale or users aren't prompted to update, check the nightly/weekly scheduler is registered and the task handler isn't erroring silently.
- **`digest:generate` / `digest:send_email`**: if community digests aren't generated or sent, check the weekly scheduler for `digest:generate` and the publish-triggered enqueue for `digest:send_email`. The `jc:digest_draft` key may be stuck if a previous generation crashed — check for stale locks.
- **`mutual_aid:expire`**: if expired mutual aid posts still appear as active, the nightly `mutual_aid:expire` task may not be running or may be erroring on specific posts.
- **`calendar:staleness_check` / `calendar:send_reminders`**: if calendar entries show as fresh when they're stale, or reminders aren't sent, check the nightly `staleness_check` and daily `send_reminders` schedulers.
- **`planning_group:expire` / `planning_group:checkin_reminder`**: if inactive planning groups don't expire or check-in reminders aren't sent, verify the task handlers and enqueue sites.
- **`embassy:poll_{slug}`**: if embassy appointment alerts are delayed or missing, check the per-embassy polling schedule — each embassy has its own cadence. The `jc:embassy:poll:{slug}` Valkey lock may be stuck if a previous poll crashed. The `embassy:dispatch_alerts` task should be enqueued by the poll task when open slots are detected.
- **`cv_format:process` / `cv_format_sessions:purge`**: if CV formatting jobs hang or sessions aren't purged, check the `jc:cv_quota` rate limit key (may be blocking the user) and the nightly purge scheduler.
- **`mentor:generate_embedding` / `mentor:update_meilisearch`**: see Mentorship Bugs above.

### New Valkey Key Issues (§§79–102)
- **`jc:cv_quota`**: if CV formatting requests are rejected unexpectedly, the rolling-window quota key may be too restrictive or not resetting properly. Check the TTL and increment logic.
- **`jc:embassy_avail`**: if embassy availability data is stale, the short-TTL cache may not be refreshing — check the `embassy:poll_{slug}` task is writing to this key after each poll.
- **`jc:digest_draft`**: if digest generation is blocked ("already in progress"), the draft lock key may be stuck from a crashed previous run — manually clear it or add a max-TTL safety.
- **`jc:wiki_edit_lock`**: if wiki page edits are blocked ("another user is editing"), the edit lock may not be releasing on session timeout — check the TTL is set and the lock is cleared on explicit save/cancel.
- **`jc:ama_active`**: if AMA sessions show as active when they've ended, the key TTL may be too long or the session-end handler isn't deleting the key.

## Output Protocol
1. **Root cause** — one sentence · 2. **Broken code** · 3. **Fixed code** (surgical, minimal) · 4. **Secondary findings** · If the root cause matches a BE-series class, say so explicitly — it feeds the regression list.
