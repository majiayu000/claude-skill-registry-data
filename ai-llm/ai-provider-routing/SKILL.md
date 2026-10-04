---
name: ai-provider-routing
description: Use whenever a product calls Gemini, DeepSeek, or other LLM APIs; design a Gemini-free-first, project-aware, secure provider router with health tracking, bounded retries, circuit breakers, cache-friendly requests, observability, and capability-safe fallback.
---
# AI Provider Routing

Read `docs/GEMINI_FREE_FIRST.md` and `.ai/AI_PROVIDER_POLICY.json`.

1. Put provider calls behind a server-side adapter/router. Never expose raw keys to the browser.
2. Prefer Gemini free tier only when privacy policy and required capability allow it.
3. Group Gemini credentials by **project quota scope**. Multiple keys in the same project share rate limits and must not be treated as independent capacity.
4. Select the least-loaded healthy quota group/model, not naive key round-robin.
5. Classify failures:
   - 401 → bad credential, quarantine;
   - 403 → permission/policy, quarantine and investigate;
   - 404 → model/resource drift, refresh capabilities;
   - 429 short rate limit → project/model cooldown;
   - 429 daily quota → mark quota group exhausted until reset;
   - 5xx/timeout → bounded backoff, circuit breaker, compatible fallback.
6. Respect `Retry-After`, add jitter, cap total attempts, and avoid duplicate SDK+gateway retry layers.
7. Discover/configure current model capabilities rather than freezing stale names.
8. Fallback only when modality/tools/schema contract can be preserved. DeepSeek is a useful low-cost text/code/reasoning fallback when configured; it is not a substitute for unsupported image/audio/video requirements.
9. Prefer stable common prompt prefixes and track cache-hit telemetry where providers expose it.
10. Log provider/model/quota-group/latency/status/usage, not raw keys/prompts by default.
11. Never rotate projects/keys to evade provider quotas or terms.
12. Pair this Skill with `ai-integration-verification`.
