---
name: jc-backend-worker
description: Use when creating or modifying Asynq background tasks/workers in the JapaConnect backend. Covers task definition, queue tier selection, idempotency, retry/backoff, payload versioning, and enqueuer wiring.
---

# JapaConnect Backend — Asynq Workers Skill

Three-tier queues on Valkey: **critical** (payments, auth emails, webhooks out, university payouts, embassy polling/alerts) · **default** (search sync, notifications, media processing, general emails, university approval notifications, v2 community/functional tool tasks) · **low** (digests, cleanup, analytics rollups, backfills, payout calculation, university logo fetch, CV session purge, mentor embedding/search sync). 95 registered tasks (75 v1 + 20 v2) — keep `asynq-tasks.md` accurate.

## Japa Academy Tasks (ADR-063)
| Task | Queue | Idempotency | Notes |
|---|---|---|---|
| `academy:process_enrollment` | critical | SET NX on `jc:uni:enrollment:processed:{payment_id}` | Creates/updates enrollment + writes `revenue_splits` row. Guard against double-credit. |
| `academy:calculate_period_payouts` | low (scheduled) | Valkey lock per instructor+period | Aggregates open splits (`payout_id IS NULL`) into `academy_instructor_payouts` once threshold met. |
| `academy:send_instructor_payout` | critical | Advisory lock on instructor_id inside tx | Executes transfer via Section 17 provider; stamps splits with `payout_id` AFTER success. |
| `academy:notify_instructor_approved` | default | Send-state guard | Email notification on instructor approval. |
| `academy:notify_course_approved` | default | Send-state guard | Email notification on course marketplace approval. |
| `university:fetch_logo` | low | Natural key (university slug) | Downloads logo from seed URL → SeaweedFS → sets `logo` field. Used during university space seeding. |

**Revenue splits are immutable** — `academy:process_enrollment` writes one row per revenue event and never updates it. A split correction is a compensating new row, never an edit. **Pro-stream splits** (`source='pro_stream'`) have no `payment_id` — they use a different idempotency key (`jc:uni:pro_stream:{instructor_id}:{enrollment_id}`) to avoid tripping the payment-id guard.

## Geo-Aware Tasks (ADR-064)
| Task | Queue | Notes |
|---|---|---|
| `maintenance:update_geoip_db` | low (scheduled, weekly Sun 02:00 UTC) | Downloads MaxMind GeoLite2, atomically swaps reader pointer. No restart needed. |

## V2 Community & Functional Tool Tasks (§§79–102, Phases 48–50)
20 new Asynq tasks across community features, functional tools, and mentorship matching. All must pass the WIRING GATE below.

| Task | Queue | Schedule | Idempotency | Notes |
|---|---|---|---|---|
| `visa_timeline:refresh_stats` | default | nightly | Natural key (timeline_id) | Recomputes visa timeline aggregate stats from raw entries. |
| `visa_timeline:prompt_update` | default | weekly | Send-state guard per (user_id, timeline_id) | Prompts users with stale timelines to update their status. |
| `digest:generate` | default | weekly | Natural key (edition_id) | Generates community digest draft content via §20 AI Gateway. HITL review required before publish. |
| `digest:send_email` | default | on publish | Send-state guard per (edition_id, subscriber_id) | Sends published digest to subscribers. |
| `mutual_aid:expire` | default | nightly | Natural key (post_id) | Expires stale mutual aid posts past their deadline. |
| `calendar:staleness_check` | default | nightly | Natural key (entry_id) | Flags calendar entries not updated within configured threshold. |
| `calendar:send_reminders` | default | daily | Send-state guard per (entry_id, user_id) | Sends upcoming event reminders to attendees. |
| `planning_group:expire` | default | as needed | Natural key (group_id) | Expires inactive planning groups past their inactivity threshold. |
| `planning_group:checkin_reminder` | default | as needed | Send-state guard per (group_id, user_id) | Sends check-in reminders to planning group members. |
| `visa_routes:check_links` | default | weekly | Natural key (route_id, url) | Validates external links on visa route pages; marks broken links. |
| `embassy:poll_{slug}` | critical | per embassy (configurable per embassy) | Valkey lock `jc:embassy:poll:{slug}` | Polls a specific embassy's appointment availability page. Per-embassy schedule — each embassy has its own polling cadence. |
| `embassy:dispatch_alerts` | critical | as needed (triggered by poll) | Send-state guard per (alert_id, subscriber_id) | Sends appointment availability alerts to subscribers when `embassy:poll_{slug}` detects open slots. |
| `credentials:check_links` | default | weekly | Natural key (profession_id, url) | Validates external links on credential checker pages; marks broken links. |
| `cv_format:process` | default | on demand | Natural key (session_id) | Processes a CV formatting job — converts uploaded CV to destination-country format. Rate-limited via `jc:cv_quota`. |
| `cv_format_sessions:purge` | low | nightly | Natural key (session_id) | Purges expired CV format sessions and associated temporary files. |
| `mentor:generate_embedding` | low | on profile change | Natural key (profile_id) | Generates pgvector embedding from mentor/mentee profile text for match scoring. |
| `mentor:update_meilisearch` | low | on profile change | Natural key (profile_id) | Syncs mentor profiles to Meilisearch for mentorship search. |

**Embassy polling** (`embassy:poll_{slug}`) is the only v2 task on the **critical** queue — appointment slots are time-sensitive and users may miss windows if polling is delayed. Each embassy gets its own task instance with a configurable per-embassy schedule (some embassies release slots daily, others weekly). The `embassy:dispatch_alerts` task is enqueued by the poll task when open slots are detected.

**Mentorship tasks** (`mentor:generate_embedding`, `mentor:update_meilisearch`) are on **low** queue — they support the 60/40 keyword+pgvector matching algorithm but are not user-blocking. Profile changes enqueue both tasks; the embedding must complete before match scoring can use the new vector.

## ⛔ WIRING GATE (BE-001 Anchor)
A task that is defined but not wired is worse than no task — it fails silently. Every new task PR must show all four:
1. Task type constant + payload struct + `NewXxxTask` constructor
2. Handler registered in the worker mux
3. Enqueue call site(s) using the REAL enqueuer (never noopEnqueuer outside tests)
4. Entry in `asynq-tasks.md` (type, queue, retry policy, idempotency note)
Missing any → STOP + alert listing what's unwired.

## Task Design Rules
- **Idempotent by default**: retries WILL happen. Guard with natural keys (`WHERE NOT EXISTS`), Valkey `SET NX` with TTL, or upserts. A task that sends an email must record send-state before/atomically-with sending.
- **Payload = IDs, not objects**: pass `user_id`, re-fetch fresh state in the handler (render-time-resolution thinking — state may have changed since enqueue). Exception: immutable event data.
- **Payload versioning**: additive changes only to payload structs; in-flight tasks from the previous deploy must still decode. Removing a field = two-deploy dance.
- **Enqueue after commit**: services enqueue side-effect tasks after the owning tx commits. A task must never observe (or act on) rolled-back data.
- **Queue tier by blast radius**: user-facing money/auth → critical; user-visible soon → default; nobody notices an hour's delay → low.
- **Timeouts + retries**: explicit `asynq.Timeout`, `asynq.MaxRetry`; exponential backoff default; tasks calling external services (Meilisearch, SeaweedFS, Honcho, mail) get shorter timeouts + more retries than DB-only tasks.
- **Context**: handlers respect `ctx` cancellation for graceful shutdown; long batch tasks checkpoint so a restart resumes, not repeats.

## Scheduled/Periodic Tasks
Registered via the scheduler with cron specs from config (not hardcoded) · overlapping-run protection (Valkey lock) for jobs that must be singletons · every periodic task also in the catalog.

## Failure Handling
Dead-letter queue monitored (Control Panel job monitor consumes these stats — the API it reads must reflect real Asynq inspector data) · retryable vs terminal errors distinguished (`asynq.SkipRetry` for permanent failures like validation) · GlitchTip capture on terminal failure with task type + payload IDs.

## Testing
Handler unit tests with fake stores · idempotency test: run handler twice, assert single side effect · payload round-trip encode/decode test · enqueue-site test asserting correct queue + options.
