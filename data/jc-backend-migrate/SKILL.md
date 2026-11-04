---
name: jc-backend-migrate
description: Use when creating, modifying, or reviewing database migrations for the JapaConnect backend (PostgreSQL 18, golang-migrate). Covers up/down pairing, zero-downtime rules, the circular FK stub pattern, and post-migration sqlc regeneration.
---

# JapaConnect Backend — Migrations Skill

High-risk activity with its own defect history (BE-003: runner applied `.down.sql` forward). Follow exactly.

## Rules of the Road
1. **Always a pair**: `NNNN_name.up.sql` + `NNNN_name.down.sql`. The down must genuinely reverse the up — write it, don't stub it with a comment.
2. **Never edit an applied migration.** Fix-forward with a new pair. The only exception is a migration that has never left your machine.
3. **Numbering**: next contiguous number; check the directory before naming — collisions break the runner.
4. **Runner sanity** (BE-003 anchor): forward runs glob `.up.sql` only. If touching the runner, add/keep the test asserting `.down.sql` files are never applied forward.
5. **After every schema change**: update the affected `.sql` query files → `sqlc generate` → commit generated code in the same PR. Schema and sqlc structs must never drift.
6. **Catalog duty**: new tables/columns that introduce settings keys or Valkey patterns update those catalogs; table-count changes noted for JEOS stat accuracy.

## Zero-Downtime Rules (Prod Is Running While You Migrate)
- Add columns as NULLable or with DEFAULT → backfill in batches (separate migration or Asynq task for big tables) → then add NOT NULL/constraints in a later migration
- Never `ALTER TYPE` / rewrite a big table in one step — new column, dual-write window, swap
- Index creation on hot tables: `CREATE INDEX CONCURRENTLY` (must be outside a transaction — mark the migration `-- +migrate NoTransaction` per runner convention)
- Dropping columns: stop reading (deploy) → stop writing (deploy) → drop (migration) — three phases, never one

## Established Patterns (Locked)
- **Circular FK users ↔ spaces**: stub table migration first, `ALTER TABLE ... ADD CONSTRAINT` after both exist. Reuse this pattern for any future cycle.
- **Wallet ledger**: append-only — migrations must never add UPDATE-enabling constructs to the transactions table; balance remains derived.
- **Revenue splits (ADR-063, migration `000166`)**: same append-only constraint as the wallet ledger — `revenue_splits` must never have UPDATE-enabling constructs. It is an immutable audit record. The 3 new tables (`academy_instructor_profiles`, `revenue_splits`, `academy_instructor_payouts`) + 7 columns on `academy_tracks` + `payment_id` on `enrollments` are all additive (NULLable/DEFAULT) — zero downtime. Seed the 12 new RBAC nodes (`university.instructor.*`, `university.course.*`, `university.payout.*`) in the same migration (BE-005).
- **Geo preference (ADR-064, migration `000167`)**: single nullable column `user_profiles.content_country_preference` (ISO code) — additive, zero downtime. No new tables.
- **University space seeding (Section 39)**: seed migration inserts `space_type = 'university'` spaces from `db/seed/universities.json` + `university_fields` field values; enqueues `university:fetch_logo` per university. Idempotent (`ON CONFLICT DO NOTHING` on slug).
- **Seed migrations**: RBAC permission nodes seed completely (BE-005). New entity = its full node set in the same PR as its routes.
- **Honcho**: separate logical database on the same PG instance — its schema is Honcho's own; JC migrations never touch it.

## Review Checklist (When Reviewing a Migration PR)
- [ ] Pair present, down actually reverses up
- [ ] Idempotent-safe where sensible (`IF NOT EXISTS` on CREATE INDEX/TABLE in seeds)
- [ ] No data loss hidden in down (dropping a column in down is fine; dropping in UP needs the three-phase note)
- [ ] Foreign keys have ON DELETE behavior chosen deliberately (CASCADE vs RESTRICT vs SET NULL — justify in a comment)
- [ ] Big-table operations follow zero-downtime rules
- [ ] sqlc regenerated, build green

## V2 Community Features, Functional Tools & Mentorship Migrations (§§79–102, Phases 48–50)

### RBAC Seed Migration Naming Convention
Each v2 feature domain gets its own dedicated RBAC seed migration following the pattern `000NNN_seed_{feature_domain}_rbac_nodes.sql`. Examples:
- `000180_seed_story_rbac_nodes.sql` — `story.*` nodes
- `000181_seed_wiki_rbac_nodes.sql` — `wiki.*` nodes
- `000182_seed_scam_alert_rbac_nodes.sql` — `scam_alert.*` nodes
- `000183_seed_planning_group_rbac_nodes.sql` — `planning_group.*` nodes
- `000184_seed_visa_timeline_rbac_nodes.sql` — `visa_timeline.*` nodes
- `000185_seed_mutual_aid_rbac_nodes.sql` — `mutual_aid.*` nodes
- `000186_seed_calendar_rbac_nodes.sql` — `calendar.*` nodes
- `000187_seed_achievement_rbac_nodes.sql` — `achievement.*` nodes
- `000188_seed_visa_routes_rbac_nodes.sql` — `visa_routes.manage` nodes
- `000189_seed_appointment_alert_rbac_nodes.sql` — `appointment_alert.*` nodes
- `000190_seed_embassy_monitor_rbac_nodes.sql` — `embassy_monitor.manage` nodes
- `000191_seed_arrival_checklist_rbac_nodes.sql` — `arrival_checklist.manage` nodes
- `000192_seed_credential_checker_rbac_nodes.sql` — `credential_checker.manage` nodes
- `000193_seed_cv_formatter_rbac_nodes.sql` — `cv_formatter.*` nodes
- `000194_seed_housing_guide_rbac_nodes.sql` — `housing_guide.manage` nodes
- `000195_seed_attestation_guide_rbac_nodes.sql` — `attestation_guide.manage` nodes
- `000196_seed_service_rbac_nodes.sql` — `service.*` nodes
- `000197_seed_language_test_hub_rbac_nodes.sql` — `language_test_hub.manage` nodes
- `000198_seed_tax_calculator_rbac_nodes.sql` — `tax_calculator.manage`, `tax_content.review` nodes
- `000199_seed_community_locator_rbac_nodes.sql` — `community_locator.*` nodes
- `000200_seed_mentorship_rbac_nodes.sql` — `mentorship.*` nodes
- `000201_seed_digest_rbac_nodes.sql` — `digest.manage` node
- `000202_seed_ama_rbac_nodes.sql` — `forum.ama.*` nodes
- `000203_seed_japa_stage_rbac_nodes.sql` — `profile.japa_stage.edit` node

**Never batch multiple feature domains into one seed migration.** Each domain's nodes must be seeded in their own migration file. Total: 48 v2 RBAC nodes across ~24 seed migrations. Seed completely (BE-005).

### New Tables for §§79–102 (~23 tables)
| Section | Table(s) | Notes |
|---|---|---|
| §79 Community Story Wall | `story_meta` | Extension table on `contents` (content_type='story') |
| §80 Destination Wiki | `wiki_pages`, `wiki_revisions` | Wiki page content + revision history |
| §81 Scam Alert Board | `scam_reports`, `scam_alert_subscriptions` | User-submitted scam reports + alert subscriptions |
| §82 Japa Planning Groups | `planning_groups` ×4 | Planning group tables (groups, members, check-ins, topics) |
| §83 Visa Timeline Tracker | `visa_timelines` ×2 + materialized view | Timeline entries + stats materialized view |
| §84 Community Digest Widget | `digest_editions` | Digest edition content |
| §85 Mutual Aid Board | `mutual_aid_posts` | Mutual aid request/offer posts |
| §86 Community Calendar | `calendar_entries` ×3 | Calendar entries, attendees, reminders |
| §88 Achievement Feed | `achievement_meta` | Extension table on `contents` (content_type='achievement') |
| §90 Visa Route Comparison | `visa_routes` | Visa route comparison data |
| §91 Embassy Appointment Alerter | `appointment_alerts` ×2 | Alert configs + alert dispatch log |
| §92 Arrival Checklist | `arrival_checklist_guides` ×2 | Checklist guides + items |
| §93 Professional Credential Checker | `credential_professions` ×3 | Professions, requirements, verification sources |
| §94 CV/Resume Formatter | `cv_standards` ×2 | CV format standards + sessions |
| §95 Housing Guide | `housing_guides` | Destination-specific housing guides |
| §96 Attestation Guide | `attestation_pathways` ×2 | Attestation pathways + steps |
| §98 Service Directory | `service_listing_meta` | Extension table on `contents` (content_type='service_listing') |
| §99 Language Test Hub | `language_tests` ×4 | Test types, providers, scores, equivalents |
| §100 Tax Calculator | `tax_treaty_pairs` ×2 | Tax treaty pairs + rate tables |
| §101 Diaspora Community Locator | `community_organisations` | Diaspora community organisations |
| §102 Mentorship Matching | `mentorship_connections` | Mentor-mentee connections with scoring |

All new tables are additive — create with `IF NOT EXISTS` in seeds, NULLable/DEFAULT columns for zero downtime. Each table with `destination_country_id` includes the FK to `countries`.

### Mentorship Trigger Migration (§102, ADR-110)
- Create `trg_mentee_count` trigger in the same migration that creates `mentorship_connections`. The trigger function increments/decrements `active_mentee_count` on the mentor's profile when a connection's `status` transitions to/from `'active'`.
- Trigger fires on INSERT, UPDATE (status change), and DELETE of `mentorship_connections`.
- The `active_mentee_count` column on `user_profiles` (or mentor profiles) must be added in the same migration (NULLable, default 0).
- Down migration: `DROP TRIGGER IF EXISTS trg_mentee_count` + `DROP FUNCTION IF EXISTS` + drop the column.

### Column Additions to Existing Tables (§§79–102)
- **`user_profiles`**: add `japa_stage` (enum/text — the user's current japa stage for §87 Japa Stage Profiles) and mentorship-related columns (`active_mentee_count` integer default 0, `mentor_bio` text nullable, `mentor_expertise` text[] nullable, `mentee_goals` text[] nullable, `mentorship_embedding` vector nullable for pgvector).
- **`forum_threads`**: add `ama_config` (jsonb nullable — AMA-specific configuration: start_time, end_time, featured_expert_id, status). Used by §89 Ask-an-Expat AMA.
- **`contents`**: verify `content_type` column accepts new discriminator values (`story`, `achievement`, `service_listing`) — if `content_type` is an enum, ALTER TYPE to add values (safe, non-breaking). Add `is_japabot_indexed` boolean default false for ADR-088.
- **ADR-088 standard columns** (`ai_generated`, `ai_model`, `hitl_reviewed_by`, `ai_generated_at`) on any existing admin-managed content tables that will support AI drafting for §§79–101 features — additive, NULLable, zero downtime.

### Migration Review Checklist Additions (§§79–102)
- [ ] Each v2 feature domain has its own RBAC seed migration (`000NNN_seed_{feature_domain}_rbac_nodes.sql`)
- [ ] `destination_country_id` FK present on all v2 functional tool tables
- [ ] `trg_mentee_count` trigger created in the same migration as `mentorship_connections`
- [ ] `active_mentee_count` column added with default 0
- [ ] ADR-088 columns (`ai_generated`, `ai_model`, `hitl_reviewed_by`, `ai_generated_at`) added to admin-managed content tables
- [ ] `is_japabot_indexed` column added to RAG-retrievable content tables
- [ ] `content_type` enum extended (if applicable) with `story`, `achievement`, `service_listing`
- [ ] `japa_stage` and mentorship columns added to `user_profiles`
- [ ] `ama_config` jsonb column added to `forum_threads`
- [ ] All new tables use `IF NOT EXISTS` in seed data
- [ ] Down migrations reverse all additions (drop triggers, functions, columns, tables)
