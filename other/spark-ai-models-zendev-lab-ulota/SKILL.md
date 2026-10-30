---
name: spark-ai-models
description: >
  Use when adding or updating Spark AI provider models or their compact and
  preflight metrics, especially baidu-oneapi, Grok, Claude, GPT, DeepSeek,
  OneAPI, context windows, output budgets, prices, thinking maps, or transports.
---

# Spark AI model catalog

Owner: `packages/spark-llm-providers`. Catalog, gateway rewrites, and measured windows live
in `baidu-oneapi.ts`. Do not guess vendor ids, context, or prices.

## Workflow

1. Identify the change: new model, metric correction, or both.
2. Research current vendor docs (and gateway ids). Record source URLs and the
   exact numbers. If docs conflict with a live gateway, keep both in comments
   and register the **gateway ceiling** for `contextWindow`.
3. Edit the existing provider owner. For Baidu, follow
   [reference.md](reference.md). Do not add a second catalog or public alias.
4. If this is a successor model, replace the predecessor in default enable
   (see Baidu OneAPI). Update tests and `packages/spark-llm-providers/README.md`.
5. Run the package and registry tests listed in the reference.

## Research rules

- Prefer the vendor's current model and pricing pages over training memory,
  blogs, or aggregator tables.
- Model id uses a **dot** when the vendor does (`grok-4.6`, not `grok-4-6`).
- `contextWindow` is the prompt+output ceiling Spark compact/preflight uses.
  On Baidu, **measured provider input** beats advertised vendor context.
- `maxTokens` is Spark's output budget, not always the vendor max. If the
  vendor lists no output cap, keep the same-family budget unless measurement
  says otherwise.
- Spark `cost` is USD per million tokens:
  `{ input, output, cacheRead, cacheWrite }`. Use headline rates (Baidu/Spark
  do not model xAI `≥200k` 2× long-context pricing). If the vendor has no
  cache-write fee, set `cacheWrite` to the input rate like existing Grok rows.
- `thinkingLevelMap` only remaps Spark levels that differ from the transport.
  Confirm whether `xhigh` is real, aliased to `high`, or invalid.

## Baidu OneAPI

- Claude and DeepSeek → `anthropic-messages`. GPT-5.6 and Grok →
  `openai-responses` (`BAIDU_ONEAPI_OPENAI_RESPONSES_MODEL_IDS`).
- Local id and gateway id can differ (`claude-opus-5` → `Opus 5`). GPT/Grok
  are currently 1:1.
- Adding a model also requires `GATEWAY_MODEL_BY_ID` plus the `models[]` row.
- Catalog and default enable are separate. Keep the predecessor catalog row
  unless the user asks to delete it. Default `enabledModels` is the current
  frontier only: when a successor ships (grok-4.5 → grok-4.6), **replace** the
  old id in `DEFAULT_SPARK_ENABLED_MODEL_PATTERNS` with the new one. Do not leave
  both enabled, and do not use `baidu-oneapi/*`.
- Add the previous bundled default (including `baidu-oneapi/*`) as a legacy set
  that migrates onto the new list. A user's custom scope, such as
  `baidu-oneapi/*` alone, must not be rewritten.
- Prove default enable with membership tests: new id in `enabledModelIds`, old
  id out. Do not freeze the whole catalog as the scope contract.

## Metric edits

Changing only windows or prices still needs tests and README notes. Do not
advertise a round number (1M, 256k) when the gateway hard-fails earlier.
