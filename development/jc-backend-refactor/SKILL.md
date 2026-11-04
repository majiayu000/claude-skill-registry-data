---
name: jc-backend-refactor
description: Use when updating or refactoring existing JapaConnect Go backend code. Enforces layer extraction, sqlc consolidation, N+1 removal, transaction boundary correction, and error-wrapping hygiene — behavior-preserving only.
---

# JapaConnect Backend — Updating & Refactoring Skill

Conventions and gates: `jc-backend-develop`. Behavior-preserving; one-line comment per change. If the refactor reveals a missing route/node/catalog entry, run Gate 2 and flag it — refactoring is when contract gaps get caught.

## 1. Layer Extraction
Business logic found in handlers → extract to service methods · direct store calls in handlers → route through services · duplicated logic across services → shared internal package (not util-grab-bag; name by domain).

## 2. sqlc Consolidation
- Hand-written SQL strings → `.sql` query files + `sqlc generate`
- Per-row queries in loops (N+1) → single query with `= ANY($1)` / join, or sqlc `:copyfrom` for bulk inserts
- SELECT * in query files → explicit column lists (schema changes stop silently breaking scans)

## 3. Transaction Boundaries
Multi-store mutations without shared tx → service-level `pgx.BeginFunc` wrapping · side-effect enqueues moved AFTER commit · wallet/credit paths verified for `pg_advisory_xact_lock` (never weaken this while refactoring). **Japa Academy**: payout paths (`academy:send_instructor_payout`) must hold `pg_advisory_xact_lock(instructor_id)` inside the tx — never weaken this. `revenue_splits` append-only — a refactor that introduces an UPDATE on this table is a defect.

## 4. Error Hygiene
`errors.New(fmt.Sprintf(...))` → `fmt.Errorf("...: %w", err)` · sentinel comparisons → `errors.Is/As` · swallowed errors (`_ =`) → handled or explicitly justified · GlitchTip capture on unexpected paths.

## 5. Context & Config
`context.Background()` in request paths → propagated ctx with timeouts on external calls (Meilisearch, SeaweedFS, Honcho, imgproxy) · magic numbers → typed config from `JC_` env or system_settings. **Geo-aware (ADR-064)**: archetype market lists (origin vs destination countries) are heuristics — keep them in config (`system_settings` or a config struct), not hardcoded in Go source. `VisitorContext` resolution must read from ctx (not re-resolve from IP on every downstream call). Feed geo boost cap and search weight multipliers → `system_settings`, not constants.

## 6. Concurrency
Unbounded goroutines per request → Asynq tasks or bounded worker pools · shared maps without sync → restructure or `sync.Map` only where justified · goroutines without ctx cancellation → leak fixes.

## 7. Post-Refactor Verification
`sqlc generate` diff-clean · `go build ./... && go vet ./...` · existing tests pass untouched (behavior-preserving means tests don't change unless they encoded the defect) · catalogs still accurate if any route/task/key moved.

## 8. V2 Community Features, Functional Tools & Mentorship Refactoring (§§79–102, Phases 48–50)

### Geo-Aware Tool Pattern — Retroactive Application
- If existing v1 tools hardcode nationalities (e.g. `WHERE nationality = 'Nigerian'` or country codes in Go source), refactor them to use the geo-aware tool pattern: `destination_country_id` as the filter axis, `?dest=` query parameter, no hardcoded nationality. This is a behavior-preserving refactor only if the hardcoded value was the sole supported value — if multiple nationalities were hardcoded, the refactor expands the surface area and needs spec review.
- Move hardcoded country lists to config (`system_settings` or a config struct), not Go source — same principle as ADR-064 archetype market lists.

### ADR-088 Columns — Retroactive Addition
- If any admin-managed content table predating §§79–102 is missing the ADR-088 standard columns (`ai_generated`, `ai_model`, `hitl_reviewed_by`, `ai_generated_at`), add them via a new migration (additive, NULLable, zero downtime). This enables AI-assisted content drafting on existing tables without breaking behavior.
- When adding these columns, also add the HITL review gate to the publish endpoint: reject when `ai_generated = true AND hitl_reviewed_by IS NULL`. This is a behavior change only for AI-drafted content (which couldn't exist before the columns) — safe for existing human-authored content.

### Community Features — `content_type` Discriminator Pattern
- If existing community content was implemented as separate top-level tables (e.g. a `stories` table instead of `contents` with `content_type = 'story'` + `story_meta`), consider refactoring to the discriminator pattern. This unifies the content pipeline (search indexing, embedding, geo-tagging, media) and eliminates parallel infrastructure. **This is NOT behavior-preserving by default** — it requires a data migration and spec review. Flag it as a recommended refactor, not a silent change.
- When refactoring, move type-specific columns to the extension table (`story_meta`, `achievement_meta`, `service_listing_meta`) and keep only common content columns on `contents`.

### Mentorship Trigger Pattern — Denormalized Count Fields
- If any other entity uses a denormalized count field (e.g. `active_member_count`, `total_responses`) that is currently computed at query time with `COUNT(*)`, refactor to the trigger-maintained pattern used by `trg_mentee_count`: a PostgreSQL trigger fires on INSERT/UPDATE/DELETE of the child table and adjusts the parent's cached count. This eliminates N+1 count queries on read paths.
- The trigger must handle all three operations (INSERT, UPDATE, DELETE) and correctly handle status transitions (only count rows where the relevant status filter matches, e.g. `status = 'active'`).
- When refactoring, verify the cached count is read instead of computed — grep store code for `COUNT(*)` queries on the child table and replace with reads of the cached column.
