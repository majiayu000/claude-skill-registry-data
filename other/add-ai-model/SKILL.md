---
name: add-ai-model
description: Add, update, or retire an AI provider model option for the BYOK theme generator (OpenAI, Anthropic, Google) and verify the provider requests native structured output for it. Use when model lists go stale or a new provider/model is requested.
argument-hint: "<provider> <model-id> [label]"
---

# Add or update an AI model: $ARGUMENTS

1. **Verify the model ID** against the provider's current documentation. Model IDs change and retire; don't guess. The server passes the string straight to the provider, so a bad ID only fails at request time.
2. **Model list**: edit `AI_MODELS` in `app/types/ai.ts` (`label`, `value`, one-line `description`). The first model for a provider is its default: it's selected when the user switches providers, and `resolveAiModel` substitutes it for a saved ID that's no longer listed, so retiring a model never strands users. `DEFAULT_AI_SETTINGS.model` must stay equal to the first OpenAI model (a unit test checks this). Prefer stable models over previews, which providers retire with little notice.
3. **New provider** (rare): add it to `AI_PROVIDERS` and `AI_PROVIDER_OPTIONS`, and to `AI_PROVIDER_IDS` and `createProviderModel` in `server/utils/aiGenerate.ts` (the route's zod enum uses `AI_PROVIDER_IDS`). Install the `@ai-sdk/<provider>` package with `pnpm add`. Map provider-specific errors in `server/utils/aiErrorHandler.ts`, and extend the "listed models" test with the provider's request shape.
4. **Structured output**: `server/utils/aiGenerate.ts` calls `generateText` with `Output.object({ schema })` (AI SDK 7), and the system prompt goes in `instructions`. System messages inside `messages` are rejected. The "listed models" test in `tests/unit/server/utils/aiGenerate.test.ts` sends every listed model through its real provider (with `fetch` stubbed, no key needed) and asserts it requests native JSON-schema output. Reasoning models (GPT-6, Claude Opus 5.5) reject the forced tool call older SDK paths use, so a model that fails this test won't work in production.
5. **Tests**: update `tests/unit/composables/useAiSettings.test.ts` and any tests that assert on model lists, then run `pnpm vitest run tests/unit/composables/useAiSettings.test.ts tests/unit/server`.
6. **E2E**: AI e2e specs mock `/api/ai/generate`, so they only cover the settings UI. A real end-to-end check needs a key in the app UI via `/run-app`, and must never be committed.
