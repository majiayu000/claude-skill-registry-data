---
name: debug-orchestrator
description: Debug the AI orchestrator pipeline. Diagnose step failures, cost tracking issues, plan generation problems, and execution errors.
---

# Debug Orchestrator

Diagnose and fix issues in the AI orchestrator (Director) pipeline, which takes a text prompt and auto-generates a complete animated clip through 27 sequential steps.

## Purpose

The orchestrator is the most complex system in ProAnimate. It calls Gemini to generate a ClipPlan JSON, then executes each step by writing to Zustand stores. Failures can occur at plan generation, individual step execution, API rate limits, or cost tracking.

## Steps

1. **Identify the failure phase** by checking `useOrchestratorStore`:
   - `phase: 'prompt'` -- user has not submitted yet.
   - `phase: 'planning'` -- Gemini is generating the ClipPlan. Failures here are API errors.
   - `phase: 'review'` -- plan generated, user reviewing. No execution yet.
   - `phase: 'executing'` -- step-by-step execution in progress. Check `currentStepIndex` and `steps[i].status`.
   - `phase: 'complete'` -- all steps finished. Check for skipped/failed steps.
   - `phase: 'error'` -- fatal error. Check `error` field.

2. **Debug plan generation failures** (`phase: 'planning'`):
   - Gemini API key missing: `VITE_GEMINI_API_KEY` not set in `.env`.
   - Gemini API error: rate limits (429), quota exceeded, model unavailable.
   - Invalid JSON response: Gemini returned malformed JSON. The orchestrator uses `responseMimeType: 'application/json'` but sometimes Gemini wraps output in markdown fences.
   - Plan validation: the ClipPlan must have `canvas`, `background`, `characters`, `dialogue` sections. Missing sections cause downstream step failures.
   - Google Search grounding: enabled via `tools: [{ googleSearch: {} }]` in the request. Can fail if grounding API is unavailable.

3. **Debug step execution failures** (`phase: 'executing'`):
   - Check `steps[currentStepIndex].status` for `'error'` and `steps[currentStepIndex].error`.
   - Non-fatal steps that do not abort execution: `generate-music`, `setup-stock-media`, `setup-sound-effects` (defined in `NON_FATAL_STEPS`).
   - Common step failures by type:
     - `setup-canvas` -- invalid aspect ratio or dimensions in the plan.
     - `setup-background` -- Lottie animation ID not found in `sampleAnimations`.
     - `setup-characters` / `generate-characters` -- saved character not found, or AI generation API error.
     - `generate-voices` -- ElevenLabs API error (invalid API key, rate limit, character limit exceeded). Cost: ~$0.30/1000 chars.
     - `setup-dialogue` -- mismatched character IDs between plan and created characters.
     - `generate-music` -- ElevenLabs music generation failure. Non-fatal.
     - `setup-text-overlays` -- font family not in allowed list, invalid position.
     - `setup-html-templates` -- template ID not found in `BUILTIN_TEMPLATES`, or template content parse error.
     - `generate-svg-objects` -- Gemini 2.5 Pro SVG generation failure.
     - `setup-stock-media` -- Pixabay API key missing or search returned no results.
     - `quality-gate` -- QA score below threshold (does not abort, just reports).
     - `finalize-timeline` -- duration calculation error, usually from missing dialogue audio.

4. **Debug cost tracking**:
   - Cost entries are accumulated in `useOrchestratorStore.cost.entries[]`.
   - Each entry has: `service` (gemini/elevenlabs/gemini-pro), `operation`, `inputTokens`, `outputTokens`, `cost`, `credits`.
   - Gemini 2.0 Flash pricing: $0.10/1M input, $0.40/1M output.
   - Gemini 2.5 Pro pricing (SVG gen): $1.25/1M input, $10.00/1M output.
   - ElevenLabs: $0.30/1000 characters.
   - If costs seem wrong, check that `addCostEntry()` is called in each step executor.

5. **Debug execution context** (`_ctx` in store):
   - The `ExecutionContext` is shared across steps and holds: character IDs, generated voice data, media URLs.
   - Steps read from and write to context. If a step is skipped via `skipStep()`, downstream steps may fail due to missing context values.
   - `retryFromStep(index)` re-executes from a specific step, but does not re-run earlier steps. Context from earlier steps must already be present.

6. **Debug the step executor registry**:
   - `getStepExecutor(stepType)` returns the executor function for a step type.
   - Each step executor is in `src/services/orchestrator/steps/`.
   - If a step type has no executor, it silently succeeds (no-op).

## Key Files

| Purpose | Path |
|---------|------|
| Main orchestrator service | `src/services/orchestrator.ts` |
| Orchestrator store | `src/stores/useOrchestratorStore.ts` |
| Orchestrator types | `src/types/orchestrator.ts` |
| Step executors directory | `src/services/orchestrator/steps/` |
| Plan builder | `src/services/orchestrator/planBuilder.ts` |
| Step builder | `src/services/orchestrator/stepBuilder.ts` |
| Chat-based plan refiner | `src/services/orchestrator/chatRefiner.ts` |
| Orchestrator constants | `src/services/orchestrator/constants.ts` |
| Server-side runner | `server/services/orchestratorRunner.ts` |
| Orchestrator panel UI | `src/components/panels/orchestrator/OrchestratorPanel.tsx` |
| Execution phase UI | `src/components/panels/orchestrator/ExecutionPhase.tsx` |
| Cost breakdown UI | `src/components/panels/orchestrator/CostBreakdown.tsx` |

## Common Issues

- **"Gemini API key not configured"**: Set `VITE_GEMINI_API_KEY` in the root `.env` file and restart the dev server.
- **Plan has empty dialogue array**: Gemini sometimes omits dialogue. Check the prompt template in `buildPlanPrompt()`. Ensure the user prompt mentions what characters should say.
- **"Character not found" in setup-characters**: The plan references a saved character by name, but no match was found in `useSavedCharactersStore`. Character matching uses fuzzy name comparison.
- **ElevenLabs rate limit (429)**: Too many TTS requests. The orchestrator does not batch requests -- each dialogue line is a separate API call. Add delays between calls if needed.
- **Step stuck at "running"**: An async operation never resolved. Check the browser console for unhandled promise rejections. Common cause: network timeout on API calls.
- **Retrying a step does not work**: The execution context (`_ctx`) may be missing data from earlier steps. If characters were generated in step 4, retrying from step 6 expects them to already exist.
- **Google Search grounding disabled**: Remove `tools: [{ googleSearch: {} }]` from the request body if the grounding API is not available in your region.

## Examples

Check orchestrator state:
```ts
const state = useOrchestratorStore.getState()
console.log('Phase:', state.phase)
console.log('Current step:', state.currentStepIndex, state.steps[state.currentStepIndex])
console.log('Error:', state.error)
console.log('Total cost:', state.cost.totalCost)
```

Retry a failed step:
```ts
const store = useOrchestratorStore.getState()
await store.retryFromStep(5) // retry from step index 5
```

Skip a non-critical step:
```ts
const store = useOrchestratorStore.getState()
store.skipStep(8) // skip step at index 8
```
