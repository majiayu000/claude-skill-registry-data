---
description: Check and update to the latest Claude model versions across the codebase
---

# Update Models

Check which Claude models are configured in the project and update to the latest versions.

## Steps

1. **Find current model references** by searching the codebase for model ID patterns:
   - `src/shared/lib/config/settings.ts` — default model settings (`agentModel`, `browserModel`, `summarizerModel`)
   - `src/renderer/components/settings/llm-tab.tsx` — model dropdown options and fallback values
   - `src/renderer/components/settings/browser-tab.tsx` — browser model dropdown options and fallback values
   - `agent-container/src/claude-code.ts` — model alias mapping (`toModelAlias` function)
   - Search broadly for any other hardcoded model IDs: `grep -r "claude-.*-[0-9]" src/ agent-container/src/`

2. **Check latest available models** by searching the web for:
   - Latest Claude model family versions (Opus, Sonnet, Haiku)
   - Latest model IDs on the Anthropic API
   - Any new model tiers or capabilities

3. **Present findings** showing:
   - Current model IDs used in each file
   - Latest available model IDs
   - What changed (new capabilities, context window, pricing changes)

4. **Ask the user** which models to update before making changes.

## How model resolution works

The codebase stores full model IDs (e.g., `claude-opus-4-6`) in settings and UI dropdowns. In `agent-container/src/claude-code.ts`, the `toModelAlias()` function maps these to SDK aliases (`opus`, `sonnet`, `haiku`). The Claude Agent SDK then resolves aliases to the actual latest model version.

This means:
- **UI dropdowns and defaults**: Use full model IDs for display (e.g., `claude-opus-4-6`, label `Claude 4.6 Opus`)
- **SDK calls**: Full model IDs get mapped to aliases via `toModelAlias()` — the SDK handles version resolution
- **Summarizer model** (`summarizerModel` in settings.ts): Uses `@anthropic-ai/sdk` directly with `client.messages.create()` — this takes the full model ID string as-is

## Key files to update

- `src/shared/lib/config/settings.ts` — default model values (`DEFAULT_SETTINGS.models`)
- `src/shared/lib/llm-provider/*-provider.ts` — each provider's `getAvailableModels()` dropdown list and `getDefaultModel()` (anthropic, platform, bedrock, openrouter). Note Bedrock uses region-prefixed IDs (`us.anthropic.claude-opus-4-8`) and OpenRouter may use its own format.
- `src/renderer/components/messages/composer-options-popover.tsx` — `FAMILY_LABEL` display strings (e.g. `opus: 'Opus 4.8'`)
- **`src/shared/lib/services/model-pricing.json` — add a pricing entry for every new model ID (see pricing note below)**
- Tests that assert defaults/labels: `settings.test.ts` (default-model assertions), `composer-options-popover.test.tsx` (trigger-label assertions)

## Important notes

- **Always add the new model ID to `src/shared/lib/services/model-pricing.json`.** Usage costing falls back to this table when a JSONL entry has no `costUSD` field, and `calculateCost()` in `usage-service.ts` **returns `0` for any model not in the table** — so a missing entry makes the new model's spend show as **$0** in the usage dashboard, silently. Mirror the previous version's pricing if the new model's pricing is unchanged (e.g. Opus 4.8 reused Opus 4.7's `$5`/`$25` in/out, `6.25`/`0.5` cache). Use the exact response model ID (e.g. `claude-opus-4-8`).
- The `toModelAlias()` function in `agent-container/src/claude-code.ts` maps any string containing "opus"/"sonnet"/"haiku" to the alias — so the exact version number in the model ID doesn't affect which model the agent runs (the bundled CLI resolves the alias), but it does affect what the user sees in the UI and how usage is costed. **The agent's actual model version is determined by the bundled Claude Code CLI's alias table, not by our pinned ID** — to change the agent's Opus version you must bump `@anthropic-ai/claude-agent-sdk` to a CLI whose `opus` alias points at the new version, then rebuild the container image. Verify the alias mapping offline: `LC_ALL=C grep -aoE '(sonnet|haiku|opus)[0-9]*:"claude-[a-z]+-4-[0-9]+' agent-container/node_modules/@anthropic-ai/claude-agent-sdk-<os>-<arch>/claude | sort -u`
- Haiku may not have a newer version when Opus/Sonnet do — check each independently
- Do NOT run `npm build` — use typecheck + lint to verify changes
