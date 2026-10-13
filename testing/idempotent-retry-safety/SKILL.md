---
name: idempotent-retry-safety
description: >
  Use this when designing retry behaviour for an SDK method that causes a
  side effect — picking the IsRetryable predicate, requiring an idempotency
  envelope (Idempotency-Key header, MessageID, upsert key) before any retry
  is legal, and capping attempts with jittered exponential backoff.
  Triggers: retry, backoff, jitter, idempotent, at-least-once, exactly-once, IsRetryable, MaxAttempts, MessageID, dedup.
version: 1.1.0
last-evolved-in-run: v0.6.0-rc.0-sanitization
status: stable
tags: [retry, resilience, idempotency, sdk]
cross_language_ok: true
---

<!-- Cross-language: body is language-neutral; cross-references name language-pack siblings (`go-idempotent-retry-patterns`, `python-idempotent-retry-patterns`, `python-asyncio-leak-prevention`). The leakage scripts honor `cross_language_ok: true`. -->


# idempotent-retry-safety (v1.1.0)

## Scope

Defines the language-neutral rules for safe retries:

1. A predicate that only retries errors whose causes admit repetition.
2. An idempotency envelope so the receiver can dedupe.
3. Capped exponential backoff with jitter.

Language-specific code lives in `go-idempotent-retry-patterns` and `python-idempotent-retry-patterns`.

## Rationale

A retry that isn't proved idempotent is a correctness bug, not a resilience feature. Duplicated side effects (double-charge, double-publish, double-insert) are far worse than the transient failure the retry was meant to mask. Retry safety rests on three legs:

1. **Predicate.** Only retries errors whose causes admit repetition (transient network blip, server overload, pool timeout). Deterministic failures (invalid input, config error, permission denied, duplicate-already-detected) MUST NOT retry — same input → same failure.
2. **Idempotency envelope.** A caller-generated identifier (HTTP `Idempotency-Key` header, message ID, upsert key) that the receiver uses to dedupe. Without it, the caller cannot prove a retry didn't double-effect.
3. **Backoff with jitter.** Capped exponential backoff prevents accidental DoS of a recovering dependency. Jitter (±10% baseline) prevents thundering-herd lockstep retries.

## Activation signals

- A method causes a side effect (publish, write, mutation) and the TPRD requests retry behavior.
- An error taxonomy is being designed and you need to decide which classes are retriable.
- A publisher/client is getting `MaxAttempts`/`MaxRetries` configuration.
- Integration tests observe duplicate deliveries or double-processing.
- HTTP client work: deciding whether POST/PATCH can retry on 5xx.
- Reviewer cites "retries on non-idempotent op" or "no jitter → thundering herd".

## Decision criteria (language-neutral)

| Situation | Retry? | Notes |
|---|---|---|
| GET / idempotent query returned 5xx | YES | Safe — no side effect |
| PUT / upsert with deterministic key returned 5xx | YES | Key dedupes server-side |
| POST without idempotency key returned 502 | NO | Cannot prove request didn't commit |
| POST with `Idempotency-Key` header returned 502 | YES | Server-side dedup makes retry safe |
| Publish with dedup-message-id returned transient error | YES | Server dedup handles it |
| Duplicate-already-detected sentinel | NO | Already delivered; retry = bug |
| Invalid-config sentinel | NO | Deterministic failure; same result on retry |
| Caller cancellation | NO | Caller no longer wants the op |

**Tuning baseline**: `MaxAttempts=3`, `Initial=100ms`, `Multiplier=2.0`, `Max=5s`, `Jitter=0.1`. Raise `MaxAttempts` only for long-deadline batch ops; never raise `Max` above the caller's likely deadline.

## Universal anti-patterns (language-agnostic)

1. **Retrying a non-idempotent op with no envelope.** POST with no `Idempotency-Key`, retry on 502 — every retry may have committed.
2. **Backoff without jitter.** N clients all back off for exactly 1s, all retry simultaneously, dependency gets clobbered.
3. **Retry predicate that returns true on caller cancellation.** Wastes resources; can mask deadline-exceeded into ResourceExhausted.
4. **Blocking sleep that ignores cancellation.** Use the language's cancellation-aware sleep primitive, not the blocking variant.

## Language realizations

- `go-idempotent-retry-patterns` — Go realization (sentinel-based predicate, middleware composition, context-aware backoff via channel-select, server-side message-ID dedup envelope).
- `python-idempotent-retry-patterns` — Python realization (exception-class predicate with cause-chain walk, decorator-driven retries, async-cancellable backoff, idempotency-key headers on HTTP, idempotent-producer config).

## Cross-references

- `network-error-classification` — sentinel taxonomy that the predicate reads
- shared-core `tdd-patterns` — every retry path needs a RED test that exercises it
- `go-circuit-breaker-policy` / `python-circuit-breaker-policy` — breaker + retry are dual; same error taxonomy feeds both
- `go-context-deadline-patterns` / `python-asyncio-leak-prevention` — retry MUST respect the caller's deadline / cancellation
