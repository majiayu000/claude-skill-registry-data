---
name: dl-scaffold
description: Templates reutilisables pour scaffold rapide (crawler, route, schema, job). Copier+adapter > generer.
paths:
  - "src/adapters/crawlers/**"
  - "src/api/routes/**"
  - "src/core/entities/**"
---

# Scaffold rapide — Copier + Adapter

## Principe : NE PAS generer from scratch. Copier un template existant et l'adapter.

## Templates disponibles

### Nouveau crawler
1. Lire un crawler existant comme template : `src/adapters/crawlers/sirene.ts`
2. Copier la structure (AsyncGenerator + TokenBucket + withRetry)
3. Adapter : URL API, schema Zod de reponse, mapping vers DatalakeEntity
4. Patterns resilience dans `src/lib/` : token-bucket.ts, retry.ts, circuit-breaker.ts

### Nouvelle route API
1. Lire une route existante : `src/api/routes/entities.ts`
2. Copier la structure (Hono handler + Zod validation + cache headers)
3. Adapter : path, query params, service call
4. Validation schemas dans `src/api/validation.ts`

### Nouveau schema Zod
1. Lire les schemas existants : `src/core/entities/entity-cards.schema.ts`
2. Copier le pattern (export const XxxSchema = z.object({...}); export type Xxx = z.infer<typeof XxxSchema>)
3. Job types existants : `src/core/entities/job-types.ts` (25+ exemples)

### Nouveau data contract
1. Lire un contrat existant : `src/config/data-contracts/dl-entities-dqc.yml`
2. Copier la structure YAML (source, tier, SLA, dimensions qualite)
3. Source registry : `src/config/data-contracts/source-registry.yml`

### Nouveau job type
1. Lire job-types.ts : `src/core/entities/job-types.ts`
2. Ajouter le type au discriminated union
3. Ajouter le handler dans `src/worker/handlers/`

## Utilitaires reutilisables (src/lib/)
- `TokenBucket` — rate limiting
- `withRetry` — exponential backoff + jitter
- `CircuitBreaker` — fail-fast + auto-recovery
- `createLogger` — structured logging
- `isValidSiren/isValidSiret` — validation SIREN/SIRET
- `signPayload/verifySignature` — HMAC-SHA256
- `cleanMojibake` — nettoyage encodage UTF-8
