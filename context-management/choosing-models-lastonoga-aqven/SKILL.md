---
name: choosing-models
description: "Picks models for AQVEN agents on any provider from its data and probes: provider_options, rate limits, fallbacks. Use first when an agent costs too much or needs a cheaper or fallback model, before editing agents/ or providers, on 429 or MODEL_FEATURE_UNSUPPORTED."
---

## MUST

- The owner picks providers and models, and any judges he named ("Owner's rules" in `AGENTS.md`). Change that
  set, or one setting across many agents, only after the owner says yes.
- When a check contradicts what runs showed, report it to the owner as a likely engine bug, with numbers (runs
  that passed, the code the check gave). Never swap models to satisfy the check.
- An agent file has no key for what a model can do: the provider's model data suggests, the real node proves. A
  new model gets `models check --live`, then one call on the real node with its output type and the input kind it
  will read (image, audio, video, PDF, long text). `--live` sends one small text request per output mode: it
  proves the mode, not the media, the length or the schema.
- Set reasoning on purpose in every agent file, with the key its provider reads; never leave the default
  unrecorded. The level is a factor like the model: start where the owner's latency and cost contract points, and
  measure it (an `agent` factor over agent files that differ only in reasoning) before calling it right.
- Facts in an agent's `description` name their source: a probe, a series id, a provider's model page, or "from
  another project, unverified here".
- A 429 is not fixed with `limits.rpm`: the model's rate-limit lane and the provider's `on_rate_limit` handle it.

## Procedure

| # | Step | Exit criterion |
|---|---|---|
| 1 | Read "Owner's rules": the providers allowed, price ceiling, what is banned, any judges he named; `providers` in `aqven.yaml` shows what is declared | the frame is known |
| 2 | Candidates from each allowed provider's own model data, not from names or memory: a direct provider's model pages and docs (its models endpoint needs the owner's key: ask him to run it); an aggregator's public catalogue (step 6); what a local or self-hosted server serves. Across model families where the allowed providers offer them. Many candidates: screen, then confirm (`designing-experiments`) | a table of enough candidates to span the price and capability range the frame allows, from several families where available |
| 3 | Per candidate, whatever the provider, one column each with its source: the input kinds the flow sends (text, image, PDF, audio, video); structured output for the node's type; tool calling when the agent has `tools`, `mcp_servers` or `subagents`; context window against the longest input plus the answer; the longest answer; price per input and output token, and reasoning, image or audio prices; reasoning controls (off, efforts, mandatory); the rate limits of the owner's key; retention against the provider's `data_policy` | no empty cell; what no source states is written as unknown |
| 4 | Name the model `<provider id>:<model name>`: the id is an entry of `providers` in `aqven.yaml` (`E_PROVIDER_UNKNOWN` otherwise), the name is the provider's own spelling. Direct: `anthropic:<model id>`, `google:<model id>`, `openai:<model id>`; `bedrock:<model or inference profile id>`; aggregator: `openrouter:<author>/<slug>`; local: `ollama:<tag>` with `base_url` on the provider; any other OpenAI-compatible server: a provider with `kind: "openai_compatible"`, `base_url` and an id outside the catalog. `anthropic`, `google`, `groq`, `mistral`, `cohere`, `bedrock`, `huggingface` and `xai` need their extra, `uv add "aqven[<name>]"` (`E_PROVIDER_EXTRA_MISSING`) | `aqven_check` clean on every model string |
| 5 | The agent file: `description` with the source of every claim; `settings.max_tokens` above the expected output plus any reasoning; `settings.provider_options` for what only this provider takes, reasoning first, at a starting level taken from the latency and cost contract, in the values its model pages list: `reasoning_effort` on OpenAI Chat Completions (`openai-chat`), `reasoning` with `effort` on OpenAI Responses (`openai`), `thinking` on `anthropic`, `reasoning` on `openrouter`, `thinking_config` on `google`, `reasoning_effort` on `xai` and on `mistral` (`none` or `high`), the model's own field on `bedrock`. `google`, `mistral` and `xai` send only the keys the provider catalog lists, `cohere` none: `W_PROVIDER_OPTIONS_IGNORED` names every key left out, and a model whose reasoning no key reaches keeps its default, so write that in `description` and measure latency. `output.mode` from `models check`; `output.on_error`, `output.on_refusal`, `output.on_truncated` | `aqven_check` clean; reasoning set, or its default recorded |
| 6 | The provider is an aggregator (`openrouter` and similar): run "When the provider is an aggregator" below for every candidate on it | upstreams chosen, single-upstream candidates flagged |
| 7 | The provider in `aqven.yaml`: `on_rate_limit` `auto` (default: the model pauses for `retry-after`, else 2 s doubling to 60 s, parallel calls halve and grow back, a call gives up after 10 attempts or 120 s), `fixed` with `retry_wait_seconds` and `retry_attempts`, or `fail` to hand over to `fallback_models` at once; `limits.concurrency` is the starting parallelism per model (8 when unset), `limits.rpm` only the provider's own limit. Every `<provider>:<model>` is a lane of its own | the strategy fits the latency contract |
| 8 | `fallback_models` that read the same input kinds, inside "Owner's rules", on the same provider or another declared one. `settings.provider_options` belong to the agent: every fallback gets the same keys, and a provider may reject a key it does not know or leave it out (`W_PROVIDER_OPTIONS_IGNORED`), so a fallback on another provider needs keys both take, proven by its own probe. `E_OUTPUT_MODE_UNSUPPORTED` checks the output modes of every model of the agent | the fallback stays inside the frame and accepts the agent's options |
| 9 | Does the model take the input kind and its size (image, PDF, audio, video, a long document against the context window): the engine keeps no table. Read the provider's data, then one run on a real case of that kind and size: `run_start` `{flow_id, mode: "live", dataset_item_id, agent_overrides: {<node_id>: <candidate agent>}}` puts the candidate on the real node with no flow edit and no series; a provider refusal comes back as `MODEL_FEATURE_UNSUPPORTED` naming the attachment | every input kind proven by a run |
| 10 | Prove it on the real node: `uv run aqven models check <agent> --project <package> --live --provider-options '<the agent's provider_options as JSON>'` (the modes); `uv run aqven models shapes <agent> --project <package> --live` for a nested output; then `run_start` with `agent_overrides` on a real case of each input kind, as at step 9. One run proves one case; the model decision is an `agent` factor (step 11). Read latency, `tokens_out` and error codes; a model three times slower than the rest goes to the owner before he finds it | every agent `ok`, the real-node run finished, latency within the contract, outliers reported |
| 11 | Compare models on the project's labelled data with a negative control, as an `agent` factor (`designing-experiments`); synthetic data is only a sanity check | the model decision rests on real labels |
| 12 | One change at a time. A setting rolled out to many models (reasoning, `max_tokens`, routing) waits for the owner's yes, then each model is measured before and after on the same few cases: `run_start` with `agent_overrides` per case, or a small `dev` series read with `series_outputs` (`latency_ms`, `cost_usd` per row); one case of latency is noise | a before-and-after table per model |

The CLI probes read keys from the environment and `<package>/.env`. Keys saved in Studio settings are visible only
to the project server: when your shell has no key, do not search for it; ask the owner to run the probe.

A direct provider, reasoning switched off through the key Anthropic reads (the example shows the key; the level
is the node's own, measured):

```yaml
description: "Sorts support tickets into queues; prompted mode and PDF input proven by run <run_id>"
model: "anthropic:claude-haiku-4-5"
settings:
  max_tokens: 4000
  provider_options:
    thinking:
      type: "disabled"
output:
  mode: "prompted"
  on_refusal: "retry"
```

On OpenAI Chat Completions the same agent takes `reasoning_effort` under `provider_options` instead, with one of
the efforts its model page lists.

### When the provider is an aggregator

An aggregator (OpenRouter, a gateway) serves one model through several upstream providers, and they differ in
parameters, quantization, limits and uptime. For each candidate on it:

| # | Sub-step | Exit criterion |
|---|---|---|
| a | The catalogue. OpenRouter: `curl -s 'https://openrouter.ai/api/v1/models?input_modalities=<kind>&supported_parameters=structured_outputs'`, fields `architecture.input_modalities` (`text`, `image`, `file`, `audio`, `video`), `context_length`, `pricing`, `supported_parameters` (`structured_outputs`, `response_format`, `tools`, `reasoning`), `reasoning` (`mandatory`, `supported_efforts`, `default_enabled`) | the step 3 columns filled from it |
| b | The upstreams: `curl -s https://openrouter.ai/api/v1/models/<author>/<slug>/endpoints`, fields `tag` (the slug `provider.order` takes), `provider_name`, `quantization`, `max_completion_tokens`, `supported_parameters`, `supports_tool_choice`, `status`, `uptime_last_30m`. A candidate with one upstream has nowhere to send a 429: flag it | single-upstream candidates flagged |
| c | Routing in `settings.provider_options.provider`: `order`, `allow_fallbacks`, `require_parameters: true`, `quantizations`. A pinned `order` with `allow_fallbacks: false` leaves an upstream 429 nowhere to go: allow fallbacks or set `fallback_models`. `routing` on the provider in `aqven.yaml` replaces the agent's `provider` object: put `data_collection` and `zdr` into the agent's instead | an upstream order chosen |
| d | `reasoning` per model at the level chosen at step 5 (`effort`, down to `"none"` or `"minimal"`, or `enabled: false`); where the catalogue's `reasoning.mandatory` is true, the lowest of `supported_efforts` is the floor | reasoning set per model |

```yaml
description: "Sorts support tickets into queues; prompted mode and PDF input proven by run <run_id>"
model: "openrouter:google/gemini-2.5-flash-lite"
settings:
  max_tokens: 4000
  provider_options:
    provider:
      order:
      - "google-vertex"
      - "google-ai-studio"
      allow_fallbacks: true
      require_parameters: true
    reasoning:
      enabled: false
output:
  mode: "prompted"
  on_refusal: "retry"
```

## Pitfalls

| What goes wrong | Do instead |
|---|---|
| Candidates taken from one provider's list while "Owner's rules" allowed several | step 2 over every allowed provider |
| A weaker model picked because its profile was unknown | the provider's data suggests, the real node decides |
| Reasoning and `output.mode: tool` set without a live probe: every attempt `MODEL_FEATURE_UNSUPPORTED` | `models check --live` first |
| The profile said `tool` works, live it gave `MODEL_NO_STRUCTURED_OUTPUT`; a big series ran without `--live` | probe live before a series |
| Every model passed `models check --live`, then the real node failed in four ways: the schema too large, no upstream for the request's parameters, `tool_choice` unsupported, no structured output | one call on the real node, with its output type and input kind |
| One variant failed every attempt with `MODEL_FEATURE_UNSUPPORTED` and nobody looked until the series ended | `series_get` `view: "summary"` at the first snapshot: failure groups per variant (`running-series`) |
| A candidate re-checked with `agent_overrides` on three cases and reported as better than the current model | one run proves one case; a comparison is an `agent` factor on labelled data (step 11) |
| Reasoning left at each model's default: two models took 80 s per call against 5 s for the rest, and the owner noticed first | decide reasoning when the agent is written; report latency outliers from the first run |
| A "low" reasoning effort switched reasoning on for a model that had it off, and latency and price jumped | set reasoning explicitly per model and measure |
| A reasoning key written for one provider, copied to an agent on another: rejected, or dropped without a word | the key that provider documents, tried with `--provider-options` first |
| `provider_options` in another provider's keys on a `google`, `mistral` or `xai` model, believed to work | `aqven_check` without `W_PROVIDER_OPTIONS_IGNORED`: the keys the provider catalog lists for that provider |
| A fallback on another provider failed every call on the agent's `provider_options` | fallbacks whose providers take the same keys, each probed |
| Truncation at `max_tokens` misread as a model or prompt failure | `finish_reason: length`, `truncated`: on a model without reasoning raise `settings.max_tokens`; on a reasoning model the hidden reasoning used the budget (`tokens_out` near the limit, little visible answer), so cap reasoning or switch it off |
| A block of settings rolled out to every model at once and judged on one case's latency | only when the owner asks; before and after per model on several cases |
| A claim from another project written into an agent's `description` as a fact | cite a probe, a series or a model page, or mark it unverified |
| `OUTPUT_SCHEMA_REJECTED` on a large enum list, answered with a model swap | a contract problem: `designing-output-contracts` |
| Frontier models picked without looking at price, or left as fallbacks after the owner banned them | "Owner's rules" bound fallbacks too |
| Two models tied on synthetic cases; on real labelled cases they split, and one also flagged a refund request on tickets that only asked for an invoice copy | compare on real labelled data with a negative control |
| A check rejected a model that real runs had shown working, and the owner's model set was changed without asking | report a likely engine bug with the numbers, keep the owner's set |
| On an aggregator, a candidate served by one upstream answered 429 to every probe | flag it at sub-step b; `fallback_models` |
| On an aggregator, `allow_fallbacks: false` on an agent pinned to two upstreams, inside a `parallel` whose join needs every branch: upstream 429s turned a holdout series `invalid` | allow fallbacks or add `fallback_models` |
| `rpm` lowered to fight 429 from a paid model | the lane handles it; `rpm` is the provider's own limit only |
| The key searched for in the shell environment | the server holds Studio keys; ask the owner |
| On an aggregator, quantization `unknown` on closed models read as missing data | it is normal for closed models |

## Tools and commands

- `uv run aqven models check <agent> --project <package> --live`, with `--provider-options '<json>'` to try a
  provider setting before writing it; the probe does not read the agent's own `provider_options`.
- `uv run aqven models shapes <agent> --project <package> --live`.
- A provider's own model pages; an aggregator's public catalogue with `curl`, as above. AQVEN has no catalogue
  command.
- macOS has no GNU `timeout`: run a long probe in the background instead of wrapping it.
- Agent files for many models come from a builder in `scripts/` (`building-flows`).
- `aqven` MCP `aqven_check`, `run_start` (`mode: "live"`, `dataset_item_id`, `agent_overrides`), `run_get_node`,
  `series_get` (`view: "summary"`), `series_outputs`.
- `uv run aqven run <flow_id> --input <file.json> --agent <node>=<agent>` goes through the project server when one
  runs on this root, and starts an engine of its own only when none does; it takes a JSON input, not a dataset case.

## References

- `references/integrations/model-providers.md`: declaring a provider, the model name per kind of provider, how
  to find and verify candidates, `provider_options` per provider, keys, `limits`, `on_rate_limit` and lanes. Read
  at steps 1 to 8.
- `references/integrations/openrouter-model-selection.md`: the aggregator page: catalogue and upstream fields,
  routing, reasoning on OpenRouter. Read at step 6.
- `references/engine/check-providers.md`, `references/engine/check-shapes.md`: the two probes and what they do
  not prove. Read at step 10.
- `references/reference/agents.md`, `references/reference/project.md`: every key of an agent and of
  `aqven.yaml`. Read before editing either file.
- `references/reference/provider-catalog.md`: built-in providers, their key variables and extras. Read at step 4.
- `references/concepts/what-happens-when-a-model-is-called.md`: outcomes and their policies, truncation on
  reasoning models. Read at step 5.
- `references/mcp-cli/runs.md`: `run_start` with `dataset_item_id` and `agent_overrides`, the node id it takes
  and its errors. Read at step 9.
