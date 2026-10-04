---
name: ai-integration-verification
description: Use to verify AI-backed product behavior, provider routing, fallback, tool calls, streaming, structured output, quotas, or model changes; require live contract evidence when possible plus deterministic simulated failure tests.
---
# AI Integration Verification

Read `docs/AI_INTEGRATION_TESTING.md` for the full matrix.

1. Define the product contract independently of provider wording: required modality, schema, tool behavior, latency/error UX, and safety/privacy constraints.
2. Test router logic deterministically with fake provider adapters for 401/403/404/429/500/503/504/timeout/stream interruption.
3. Verify retry budget, circuit breaker recovery, same-project quota grouping, and fallback order. Record this deterministic suite as `ai-failure-matrix` evidence.
4. Verify a fallback cannot silently drop image/audio/video/tool/schema requirements.
5. Make tool/side-effect execution idempotent; retrying a model turn must not duplicate writes/charges/messages.
6. Test secret redaction and confirm keys are absent from client bundles/logs.
7. When authorized credentials are available, run a minimal live contract call through the **same application integration path** and record it as `ai-contract` evidence.
8. If live access is unavailable, leave `ai-contract` blocked/external-pending; mocks cannot prove current upstream compatibility.
9. Do not load-test free upstream APIs to discover limits; use provider documentation plus local simulators.
