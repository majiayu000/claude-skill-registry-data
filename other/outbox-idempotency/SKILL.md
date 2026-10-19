---
name: outbox-idempotency
description: "Transactional outbox pattern for reliable event delivery: idempotency keys, ordered replay, poison-message handling, and leak tests that catch duplicates or lost events. Use when adding event-driven integrations (webhooks, CDC, message bus), introducing an outbox table or idempotency_key column, or investigating 'event delivered twice' / 'event never arrived' incidents."
license: MIT-compat
compatibility: "PostgreSQL 15+ / any transactional store; framework-agnostic"
metadata: {}
allowed-tools: []
---

Standard: name/description/length rules — [agentskills.io standard](../references/agentskills-standard.md).
# Outbox Idempotency Skill — Quick Reference (body <500 lines; full procedure in references/outbox-procedure.md)

## When to use this skill (trigger)
Any of these fires it:
- Adding an event-driven integration (webhooks, CDC, message bus) that must not lose or duplicate events.
- A migration introduces an `outbox` table or an `idempotency_key` column.
- An incident report says "event delivered twice" or "event never arrived".
- Code review mentions `INSERT INTO outbox` without a unique key or replay logic.
- Designing retry semantics for a service that writes events and sends them.

## Disambiguation
- Fires: event-driven integrations that must not lose/duplicate events, an outbox/idempotency_key migration, 'event delivered twice/never arrived', retry semantics for an event writer.
- Does NOT fire for: a plain CRUD endpoint with no events, or tenant isolation (use pg-rls-multitenant).

## When NOT to use this skill (neighbour prompts — do not fire)
- Fire-and-forget logging or metrics where ordering does not matter and duplicates are
  harmless — there is no outbox to protect and no idempotency key is needed.
- A synchronous RPC that returns before any work is queued — the skill fires only when
  work outlives the request.
- "We already have retries" — retries are the reason the UNIQUE constraint exists; the
  skill fires when retries are mentioned alongside outbound writes.

## Decision table — idempotency strategy
| Pattern | When to pick | Pitfall |
|---------|-------------|---------|
| UUID v7 idempotency key on every outbox row | Default; sortable by time; collision-safe | Key must be generated BEFORE the business transaction commits |
| Natural key (entity_id + version) | Immutable entities with monotonically increasing versions | Version gaps look like missing events if not handled |
| Hash of payload + sequence number | High-throughput streams where UUID cost matters | Hash collisions possible; pair with sequence check |

## Near-miss triggers (act before the incident)
- A poller uses `LIMIT` without `ORDER BY` → out-of-order delivery for ordering-dependent consumers.
- `UPDATE sent_at` happens BEFORE the publish ACK → duplicate publish on crash.
- `DELETE` appears anywhere near `poison_outbox` → lost event with no audit trail.
- `max_attempts` is absent or 0 → poison messages block the queue forever.
- Outbox INSERT and business write are in separate transactions → lost events on connection drop.
- Replay reuses a fresh idempotency key → double-delivery even after the root cause is fixed.

## Numbered procedure (summary; full recipe in references/outbox-procedure.md)
1. **Create outbox table** — `id uuid PRIMARY KEY DEFAULT gen_random_uuid()`, `idempotency_key text NOT NULL UNIQUE`, `payload jsonb NOT NULL`, `created_at timestamptz NOT NULL DEFAULT now()`, `sent_at timestamptz`, `attempts int NOT NULL DEFAULT 0`, `last_error text`.
2. **Write in same TX** — INSERT outbox row + business data in ONE transaction; commit both or neither.
3. **Poller loop** — SELECT ... WHERE sent_at IS NULL ORDER BY created_at LIMIT N FOR UPDATE SKIP LOCKED; publish; UPDATE sent_at = now() on success; increment attempts on failure.
4. **Poison handling** — after max_attempts (default 5), move row to poison_outbox table with error snapshot; do NOT delete it.
5. **Replay** — SELECT from poison_outbox ORDER BY created_at; re-publish only after root cause is fixed; keep original idempotency_key so dedup still works.
6. **Leak test harness** — `scripts/check_outbox.py` validates schema presence, UNIQUE idempotency_key, poller ordering, poison threshold, and no lost events under concurrent publish. Run against Docker Postgres before merge; any FAIL blocks merge.

## Worked examples
Good (one-transaction write):
```sql
BEGIN;
INSERT INTO accounts (id, balance) VALUES ('a1', 100);
INSERT INTO outbox (idempotency_key, payload)
  VALUES ('acct-a1-debit-001', '{"event":"account.debitted","account":"a1"}');
COMMIT;
```
Bad (separate transactions — loses the event on connection drop):
```sql
INSERT INTO accounts (id, balance) VALUES ('a1', 100);
-- network drop here == event never sent, no row to recover
INSERT INTO outbox (idempotency_key, payload) VALUES (...);
```
Bad (poller without ordering — consumers that care about order break):
```sql
SELECT ... FROM outbox WHERE sent_at IS NULL LIMIT 50 FOR UPDATE SKIP LOCKED;
```

## Pitfalls from research (real incidents)
- Out-of-order delivery when poller uses LIMIT without ORDER BY + SKIP LOCKED.
- Duplicate publishes when poller crashes between publish and UPDATE sent_at.
- Poison messages block the queue when max_attempts is absent.
- Lost events when business TX commits but outbox INSERT fails due to connection drop.
- Replaying without idempotency_key causes double-delivery even after fix.

## Verification checklist (all must pass before merge)
- [ ] Outbox table has UNIQUE idempotency_key
- [ ] Business write + outbox INSERT are in ONE transaction
- [ ] Poller uses ORDER BY created_at + FOR UPDATE SKIP LOCKED
- [ ] Poison threshold moves rows after max_attempts
- [ ] Replay preserves original idempotency_key
- [ ] Leak test harness runs green against Docker Postgres
- [ ] No DELETE on poison_outbox rows

## Verification
- Run the offline gate: `python3 scripts/check_outbox.py <sql-file>` — must exit 0.
- Run the self-test: `python3 scripts/check_outbox_test.py` — must print ok.
- Run the standard validator: `python3 scripts/validate_skills.py` — must report OK.
- Full procedure, version table, worked examples, and pitfalls: `references/outbox-procedure.md`.
- Eval prompts with expected behaviour and failure signs: `references/EVALS.md`.
- Primary sources with URLs and retrieval dates: `references/SOURCES.md`.

## Related skills
- [acceptance-harness](../acceptance-harness/SKILL.md) — the outbox leak test is an acceptance scenario with PASS evidence.
- [honest-status](../honest-status/SKILL.md) — the outbox migration is a status item; mark it VERIFIED only when the leak test ran.
- [problem-json-contracts](../problem-json-contracts/SKILL.md) — outbound failures are emitted as problem details.
- [long-test-discipline](../long-test-discipline/SKILL.md) — the leak test is a long test; run it in the foreground with a recorded seed and a resource cap.
- [module-contract-first](../module-contract-first/SKILL.md) — the outbox schema and the idempotency contract are module contracts; snapshot them, block merge on drift.
- [shared-tree-git](../shared-tree-git/SKILL.md) — the outbox migration and the leak-test evidence are committed with a task-id prefix.
