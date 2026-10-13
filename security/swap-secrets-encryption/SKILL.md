---
name: swap-secrets-encryption
description: Take the keys that encrypt secrets in the database from a KMS (self-hosted OpenBao Transit, or a cloud KMS) instead of ENCRYPTION_KEYS. Use when compliance requires KMS-held keys, or the user asks about envelope encryption. Not for debugging; when something fails, use the debug skill.
disable-model-invocation: true
---

# Swap the encryption key source

- **Interface:** `KeyProvider` (`active()`, `get(id)`) in `packages/nest-common/src/crypto.ts`.
- **Today:** `keysFromEnv(ENCRYPTION_KEYS)`: `id:base64key` entries, first active.
  `SecretBox` (AES-256-GCM, ciphertext `v2.<keyId>.<iv>.<data>`, with the row it
  belongs to as additional data; `v1` values, from before that, still decrypt) uses it.
- **Used in:** `apps/api/src/modules/webhooks/webhooks.service.ts` (writes endpoint
  signing secrets) and `apps/webhooks/src/outbound/delivery.service.ts` (reads them), both
  `new SecretBox(keysFromEnv(env.ENCRYPTION_KEYS))`.
- **Env:** `ENCRYPTION_KEYS` in `apps/api/src/env.ts` and `apps/webhooks/src/env.ts`.

## Swap

1. A `KeyProvider` whose data keys are wrapped by the KMS: store the wrapped keys (with
   their ids) in configuration, unwrap them once at boot, and serve them from memory.
   `active()` and `get()` are synchronous, so unwrap before the services start using
   them. Ciphertexts and `SecretBox` don't change, so existing rows keep decrypting as
   long as their key ids are still provided.
2. Build it in one place (a factory next to `keysFromEnv`) and use it in both services
   above; they must resolve the same key ids.
3. New variables (key ARN or name, the wrapped keys) in both services' `src/env.ts`,
   `.env.example` and `docs/environment.md`; cluster access to the KMS: OpenBao's Kubernetes
   auth in the cluster (the self-hosted default; check with the user before a cloud KMS,
   which also needs credentials in the services' SOPS Secrets).
4. Keep `keysFromEnv` for development and tests.

Rotating keys is the rotate-secrets skill.

## Tests

`packages/nest-common/src/crypto.test.ts` (round trip, rotation, unknown key) with a
fake KMS; `apps/webhooks/test/webhooks.integration.test.ts` signs deliveries with
secrets the API encrypted.

## Finish

1. The verify skill.
2. Ask the `reviewer` agent to review the change, and the `security-reviewer` agent: a
   new implementation brings its own credentials and sends data somewhere new. If you
   wrote a migration, the `migration-reviewer` agent too.
3. Update the seam's row in the README's "Scaling path" table if what's "Now" changed.
