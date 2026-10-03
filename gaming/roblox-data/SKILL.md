---
name: roblox-data
description: "Design or review Roblox persistence, schemas, session ownership, retries, and cross-server state."
---

# Roblox data

Read [`../../references/roblox-engineering.md`](../../references/roblox-engineering.md). Inspect the existing data layer and every writer before choosing a storage pattern.

## Classify the state

- Durable player or game state belongs in DataStoreService.
- Frequent, ephemeral cross-server coordination belongs in MemoryStoreService with explicit expiration and recovery when an entry disappears.
- One-way cross-server notifications may use MessagingService, but the message should identify authoritative state that receivers can reread. Do not make delivery itself the durable record.
- Local caches need an owner, invalidation rule, maximum lifetime, and fallback when the backing service fails.

## Preserve correctness

- Keep service access server-side. Define the key format, serializable schema, schema version, defaults, validation, migration, and ownership of each mutation.
- Use atomic update patterns for concurrent or retry-sensitive writes. Keep update callbacks pure and non-yielding; derive the new value only from their arguments and immutable inputs.
- Make rewards, purchases, and other consequential mutations idempotent. Record the operation identifier with the durable outcome so a retry cannot grant twice.
- Use a session lease when multiple servers could write the same player record. Define acquisition, renewal, release, stale-owner recovery, and what gameplay can continue after ownership is lost.
- Wrap service calls, distinguish retryable failure from invalid data, and use bounded backoff with jitter. Never retry in a tight loop or treat failure as an empty profile.
- Treat shutdown saving as a final attempt, not the only persistence path. Bound shutdown work and make player departure, reconnect, teleport, and server failure explicit lifecycle cases.
- Never enable or exercise live DataStore access through an agent-run Studio test. The user performs Studio validation, preferably against a separate test version when durable data is involved.

## Deliverable

State the service choice, schema and key format, authority, operation lifecycle, concurrency behavior, failure policy, and migration path. Verify pure serializers, validators, migrations, and idempotency locally; give the user a short Studio checklist for runtime behavior.
