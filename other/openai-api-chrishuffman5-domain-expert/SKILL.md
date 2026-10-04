---
name: openai-api
description: "OpenAI platform API expert: the Responses API (`POST /v1/responses`) as the primary surface, Chat Completions migration posture and the Assistants API sunset, current model IDs and per-MTok pricing (GPT-5.6 sol/terra/luna, GPT-5.x, GPT-4.1, GPT-4o, o-series, embeddings, realtime, image, Sora), function tools and strict mode, built-in tools (web search, file search, code interpreter, computer use, image generation), Structured Outputs via `text.format`, SSE streaming events, conversation state (`previous_response_id` vs the Conversations API), background mode, the Batch API, prompt caching and its 1.25x write fee on GPT-5.6+, rate-limit tiers and headers, the Files and Vector Stores APIs, and the Realtime API. WHEN: \"Responses API\", \"/v1/responses\", \"api.openai.com\", \"OPENAI_API_KEY\", \"openai-python\", \"openai-node\", \"output_text\", \"instructions parameter\", \"previous_response_id\", \"Conversations API\", \"store: false\", \"background: true\", \"starting_after\", \"sequence_number\", \"gpt-5.6\", \"gpt-5.6-sol\", \"gpt-5.6-terra\", \"gpt-5.6-luna\", \"OpenAI pricing\", \"cached_tokens\", \"cache_write_tokens\", \"prompt_cache_key\", \"prompt_cache_breakpoint\", \"prompt_cache_options\", \"text.format\", \"json_schema\", \"strict: true\", \"Structured Outputs\", \"function_call_output\", \"call_id\", \"tool_choice\", \"allowed_tools\", \"parallel_tool_calls\", \"web_search tool\", \"file_search\", \"vector store\", \"code_interpreter container\", \"computer_call\", \"image_generation tool\", \"response.output_text.delta\", \"Batch API\", \"custom_id\", \"x-ratelimit-remaining-tokens\", \"usage tier\", \"Chat Completions migration\", \"response_format\", \"Assistants API sunset\", \"gpt-realtime\", \"gpt-image-2\". Do NOT use for: choosing between OpenAI/Anthropic/Google models on capability or price tiers — that's `model-selection`; Anthropic Messages API mechanics — that's `claude-api`; running GPT models through Azure AI Foundry, Bedrock, Vertex, or OpenRouter — that's `inference-providers`; building agent loops, handoffs, guardrails, or sessions with the OpenAI Agents SDK — that's `openai-agents-sdk`; the Codex CLI/harness — that's `codex`; training or tuning models beyond the eligible-base-model list — that's `fine-tuning`; grading model output or building graders — that's `evals`; the MCP protocol, transports, or writing MCP servers — that's `mcp`; prompt-injection taxonomy and agent threat modeling — that's `ai-security`; container/VM isolation for tool execution — that's `sandboxing`."
license: MIT
---

# OpenAI Platform API

One endpoint carries almost everything: `POST /v1/responses`. Tools, structured outputs, streaming, caching, state, and background execution are all parameters on that request. Chat Completions is the older, still-supported shape; Batch, Files, Vector Stores, and Realtime are the surrounding infrastructure.

## Volatility rule — verify before you quote

Model IDs, prices, context windows, tier thresholds, deprecation dates, and cache-pricing rules move faster than this skill. Every fact here is a snapshot of OpenAI's docs as of **2026-08-05**, with the exact source URL at the bottom of each file.

Re-check the cited URL before putting a price into a budget, a model ID into production config, or a deprecation date into a migration plan. Never quote a number for a model this skill does not list — say it is unverified and point at the pricing page.

Two dates are close enough to act on now:

- **Assistants API full sunset: 2026-08-26.** A different, older product than Chat Completions. If a codebase still calls Assistants/Threads/Runs, migration is urgent, not optional.
- **Evals platform: read-only 2026-10-31, full shutdown 2026-11-30.** Do not build new tooling on `/v1/evals`.

Chat Completions itself is **not** deprecated and has no announced sunset date. Do not tell a user otherwise.

## Routing

| Request | Load |
|---|---|
| Create params, response object, conversation state, background mode, SDK setup | `references/responses-api.md` |
| Model IDs, context windows, pricing across every family | `references/models-and-pricing.md` |
| Moving off `chat.completions` — field-by-field mapping and order of operations | `references/migrate-from-chat-completions.md` |
| Function tool schemas, strict mode, `tool_choice`, round trip | `references/function-calling.md` |
| Web search, file search, code interpreter, computer use, image generation | `references/built-in-tools.md` |
| `text.format`, JSON Schema subset, refusals | `references/structured-outputs.md` |
| SSE event names and the consumption loop | `references/streaming.md` |
| Batch JSONL format, limits, statuses | `references/batch.md` |
| Cache thresholds, TTLs, breakpoints, the 1.25x write fee | `references/prompt-caching.md` |
| Tiers, limit dimensions, response headers | `references/rate-limits.md` |
| Files API, Vector Stores API, chunking, search | `references/files-and-vector-stores.md` |
| WebRTC/WebSocket/SIP, session types, realtime models | `references/realtime.md` |

## Request essentials

Base host `api.openai.com`, versioned path prefix `/v1`. Authenticate with an API key supplied via the `OPENAI_API_KEY` environment variable — both official SDKs read it automatically, so `OpenAI()` / `new OpenAI()` needs no arguments.

```python
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-5.6",
    instructions="You are a helpful assistant.",
    input="Write a one-sentence bedtime story about a unicorn.",
)
print(response.output_text)
```

Three input surfaces replace the single `messages` array: `instructions` for system/developer guidance, `input` for the turn (a plain string, or an array of items with `role` in `developer`/`user`/`assistant`), and `output` for typed result items. `output_text` is an SDK convenience accessor that concatenates text items — reach for the typed `output` array whenever tool calls or reasoning items are in play.

Beware a naming inconsistency in OpenAI's own docs: guide examples use the bare `model: "gpt-5.6"` while the models page enumerates `gpt-5.6-sol`, `gpt-5.6-terra`, and `gpt-5.6-luna`. Confirm which exact string your account accepts before shipping config, and pin it explicitly — never build on an assumed evergreen alias.

## Responses vs Chat Completions

Use Responses for all new work. OpenAI's position: "While Chat Completions remains supported, Responses is recommended for all new projects."

The structural differences that break a naive port:

| Aspect | Chat Completions | Responses |
|---|---|---|
| Input | `messages` array | `input` + `instructions` |
| Output | `choices[0].message.content` | `output_text` or typed `output[]` |
| Item types | messages only | messages, reasoning, function calls, tool outputs |
| State | you replay the transcript | `previous_response_id`, Conversations API, or manual replay |
| Tools | you implement everything | built-in web search, file search, code interpreter, computer use, MCP |
| Structured outputs | `response_format` | `text.format` |
| Function definitions | externally tagged | internally tagged |

OpenAI's claimed gains from migrating: ~3% on SWE-bench and 40–80% better cache utilization, because reasoning and tool context persist across turns instead of being rebuilt. Treat both as vendor claims, not measured facts for your workload.

Migrate in this order — simple text flows, then endpoint/output handling, then a state-management decision, then function definitions, then Structured Outputs schemas, then streaming handlers, then rollout. Details in `references/migrate-from-chat-completions.md`.

## Conversation state

Three strategies, and the choice is a cost decision as much as an architecture one.

- **`previous_response_id`** — chain each call to the prior response id. Simple, but **every previous input token in the chain is re-billed as input on every subsequent call**. Long chains get expensive quickly; prompt caching is what makes them tolerable, so structure prompts for cache hits (below) before reaching for chaining.
- **Conversations API** — `conversations.create()`, then pass `conversation=<id>`. Durable across sessions and devices, stores messages, tool calls, and tool outputs, and is **exempt from the 30-day TTL** that applies to plain stored responses.
- **Manual replay** — you own the transcript. Required when `store: false` is mandated.

`store` defaults to true with 30-day retention. Set `store: false` for data-minimization; you then cannot chain by id and must replay context yourself.

Context window counts **input + output + reasoning tokens against one ceiling**. Reasoning tokens are invisible in your prompt but consume the same budget — size `max_output_tokens` with that in mind on reasoning models.

## Background mode

Set `background: true` for long-running work, then poll `responses.retrieve(id)` until a terminal status (`completed`, `failed`, `cancelled`, `incomplete`). Only background responses can be cancelled — `POST /v1/responses/{id}/cancel`, idempotent.

Combine `background: true` with `stream: true` to get events immediately while execution continues server-side. Track each event's `sequence_number` as a resume cursor and reconnect with `starting_after` after a dropped connection — this is the only reliable recovery path for a long background stream.

Zero Data Retention projects force `store=false` on background responses; data lives ~10 minutes on disk purely to support polling. Do not design a ZDR background flow that assumes retrievability later.

## Tools

Function tools are internally tagged — `type`, `name`, `description`, `parameters`, `strict` sit at the top level of the tool object, not nested under a `function` key as in Chat Completions. This is the single most common port error.

Round-trip rules that break requests when violated:

- Append the model's `output` items to your input array **unchanged**, then push a `function_call_output` item carrying the matching `call_id` — not the item `id`. Those are two different fields on the same object.
- `arguments` arrives as a **JSON-encoded string**; parse it. It is never a dict.
- Set `"strict": true` and satisfy its schema rules (`additionalProperties: false` everywhere, every property in `required`, optional fields typed as `["string", "null"]`). Cheaper than a retry loop.
- `tool_choice` is `"auto"` (default), `"required"`, `"none"`, a forced `{"type": "function", "name": ...}`, or an `allowed_tools` object restricting the callable set without forcing one.
- Parallel calls are on by default on GPT-5 and later; `parallel_tool_calls: false` caps a turn at zero or one call.

Keep the active toolset under ~20 functions. Every definition consumes input tokens on every request — defer rarely-used tools via tool search rather than trimming descriptions into uselessness.

## Built-in tools

| Tool type | What it does | Sharpest constraint |
|---|---|---|
| `web_search` | OpenAI-run search with `url_citation` annotations | Inline citations **must** be visible and clickable in your UI |
| `file_search` | Retrieval over vector stores | Files must reach `completed` status before they are searchable |
| `code_interpreter` | Sandboxed Python container | Container dies after **20 minutes idle**; data is unrecoverable |
| `computer` | Screenshot → batched actions loop | Requires `gpt-5.6` (or `gpt-5.4`); send screenshots at `detail: "original"` |
| `image_generation` | In-conversation image generation/editing | `gpt-image-2` does **not** support transparent backgrounds |

Prefer `web_search` over the legacy `web_search_preview` type — the old string still works but misses newer options (`filters`, `search_content_types`, `external_web_access`, `return_token_budget`).

Code interpreter memory tiers are `1g` (default), `4g`, `16g`, `64g`; above-default tiers bill at built-in-tool rates, so do not raise the tier speculatively. Persist anything you need out of the container before it expires.

Full option tables in `references/built-in-tools.md`.

## Structured outputs

Prefer `text: { format: { type: "json_schema", strict: true, schema: ... } }` over prompt-and-parse. Better still, use the SDK helpers — `client.responses.parse(text_format=YourPydanticModel)` in Python, `zodTextFormat(schema, "name")` in JS — so the schema and your types cannot drift.

Design to the supported subset. `allOf`, `not`, `dependentRequired`, and `if`/`then`/`else` are **unsupported** and will not silently degrade. The root must be an object, not an `anyOf`. Hard caps: 5,000 total properties, 10 nesting levels, 120,000 schema characters, 1,000 enum values across all properties.

Handle three distinct terminal cases, not one: a schema-valid payload, a `refusal` item (safety), and `incomplete_details.reason` of `max_output_tokens` or `content_filter`. Code that assumes only the first will crash in production.

Not available on `gpt-3.5-turbo` or `gpt-4-turbo` — those need legacy JSON mode.

## Streaming

Set `stream: true` and iterate events. Handle unknown event types gracefully; OpenAI adds them.

The events that carry the actual work: `response.output_text.delta` for text, `response.function_call_arguments.delta`/`.done` for tool arguments, `response.refusal.delta`, plus lifecycle (`response.created`, `response.completed`, `response.failed`) and per-tool progress events for file search and code interpreter. Never parse accumulated `function_call_arguments` fragments before the matching `.done` event — partial JSON is not JSON. Full event list in `references/streaming.md`.

## Batch

Use Batch for anything latency-tolerant: **50% off**, and it draws from a **separate, much higher rate-limit pool** so it does not compete with your synchronous traffic.

Caps: 50,000 requests and 200 MB per batch, `.jsonl` only, 2,000 batch creations per hour, and `"24h"` is the only completion window offered. Each line needs `custom_id`, `method`, `url`, `body`.

Always map results by `custom_id` — **output order does not match input order**. Output files auto-delete 30 days after completion; video outputs only stay downloadable 24 hours.

## Prompt caching

Caching is automatic on prefix match — the first ~256 tokens select the routing bucket — but it only engages above a **1,024-token minimum on GPT-5.6+** (1,024–2,048 and less consistent on earlier models). Short prompts are simply never cached; there is no error.

The cost model changed at GPT-5.6 and this catches people: **cache writes now bill at 1.25x the uncached input rate**. On earlier models writes were free. A high-churn prefix that used to be merely useless is now actively more expensive than not caching. Set `prompt_cache_options.mode: "explicit"` with `prompt_cache_breakpoint` markers after stable blocks to stop paying for automatic write attempts you never read back.

Structure every prompt static-first: instructions, examples, and tool definitions at the front, user-specific content at the end, byte-identical across requests. Set `prompt_cache_key` on requests that share a long prefix to improve routing. Verify with `cached_tokens` and `cache_write_tokens` in usage — never assume.

## Rate limits

Six tiers by cumulative spend (Free/$5/$50/$100/$250/$1,000 paid) with monthly usage caps from $100 to $200,000. Limits apply across RPM, TPM, RPD, TPD, IPM, and audio-minutes-per-minute — **whichever ceiling is hit first wins**, so 20 tiny requests can exhaust a 20-RPM limit while nowhere near TPM.

Read `x-ratelimit-remaining-requests`, `x-ratelimit-remaining-tokens`, and the matching `-reset-` headers rather than guessing, and honor `Retry-After` on a 429. Per-model numeric RPM/TPM values are not published on the rate-limits guide — read them from the account dashboard.

## Files and vector stores

Upload via `POST /v1/files` with a `purpose` (`assistants`, `batch`, `fine-tune`, `vision`, `user_data`, plus the three output/result variants). Limits: 512 MB per file, 2.5 TB per project, 1,000 upload requests/minute.

Deleting a file **removes it from every vector store that references it**. There is no per-store detach-on-delete; treat file deletion as a global operation.

Vector store defaults: `auto` chunking at 800 max tokens with 400 overlap; `static` allows 100–4,096. Search supports filters, `max_num_results` (1–50), re-ranking, and `rewrite_query`. Endpoint tables in `references/files-and-vector-stores.md`.

## Realtime

Three transports: WebRTC for browser/mobile clients capturing audio, WebSocket for server-side pipelines, SIP for telephony. Three session types on distinct paths — voice agents at `/v1/realtime` (full tool-calling), translation at `/v1/realtime/translations`, and transcription-only sessions.

Models: `gpt-realtime-2.1` (voice agents), `gpt-realtime-translate`, `gpt-live-transcribe`. Start sessions at reasoning effort `"low"` in production. Audio tokens are expensive — $32/MTok in, $64/MTok out on `gpt-realtime-2.1` — so budget realtime by audio minutes, not by text-token intuition.

## Cost estimation checklist

Never quote a per-request cost from the input/output columns alone. Sum:

1. Uncached input at the model's rate, plus cache reads at the cached-input rate.
2. **Cache writes at 1.25x input on GPT-5.6+** (free on earlier models).
3. Output tokens **including invisible reasoning tokens**.
4. Tool definition tokens, charged as input on every request that carries them.
5. Built-in tool charges — code interpreter memory tiers above `1g`, image generation output tokens by resolution/quality.
6. For chained conversations: the entire prior input, re-billed each turn under `previous_response_id`.
7. Multiplier: 0.5x for Batch.

## Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Tool schema rejected after porting | Chat Completions' externally-tagged `{"function": {...}}` shape | Flatten to internally-tagged `type`/`name`/`parameters` |
| Function result ignored | Submitted the item `id` instead of `call_id` | Use `call_id` on `function_call_output` |
| `arguments` treated as an object | It is a JSON string | `JSON.parse` / `json.loads` first |
| Strict mode 400 | Optional property omitted from `required` | Type it `["string","null"]` and keep it required |
| Schema rejected | `allOf`/`not`/`if-then-else` present | Rewrite within the supported subset |
| `cached_tokens` always 0 | Prompt under 1,024 tokens, or prefix drift | Move static content first; check byte-identity |
| Cache costs rose after upgrading to GPT-5.6 | Writes now bill 1.25x | Switch to explicit breakpoints, or stop caching churn |
| Batch results mismatched | Assumed output order matches input | Join on `custom_id` |
| Code interpreter file vanished | 20-minute idle container expiry | Download outputs before the container idles |
| 429 well under TPM | RPM/RPD hit first | Read `x-ratelimit-remaining-requests`; honor `Retry-After` |
| Background stream dies mid-run | No resume cursor tracked | Record `sequence_number`, reconnect with `starting_after` |
| Conversation cost grows superlinearly | Chained input re-billed every turn | Cache the static prefix, or replay a trimmed transcript |

## Diagnostic scripts

Local, offline, read-only — none of them make network calls or need an API key.

- `scripts/validate-strict-schema.py <schema.json>` — checks a Structured Outputs / strict-tool JSON Schema against the documented constraints (unsupported keywords, `additionalProperties`, required coverage, property/nesting/enum/size caps).
- `scripts/validate-batch-jsonl.py <input.jsonl>` — validates a Batch input file: per-line fields, supported `url` values, `custom_id` uniqueness, and the 50,000-request / 200 MB caps.
- `scripts/cache-prefix-diff.py <a.json> <b.json>` — reports the byte offset where two serialized request bodies diverge, so you can see exactly how much cacheable prefix two requests actually share.

## Not covered here

The corpus behind this skill does not include: OpenAI's error/HTTP status reference; the canonical Responses create-parameter table (`temperature`, `max_output_tokens`, `text.verbosity`, `truncation`, `include` are referenced in guides but were not confirmed against one authoritative schema page); the MCP built-in tool type's dedicated guide; the container-files sub-API paths; the full Realtime event catalog; per-model numeric rate limits; context windows and knowledge cutoffs for anything outside the GPT-5.6 trio; and SDKs other than Python and Node. Treat all of those as unverified and check the docs directly rather than accepting a confident answer.

## Sources

- https://developers.openai.com/api/docs/api-reference/responses
- https://developers.openai.com/api/docs/guides/text
- https://developers.openai.com/api/docs/guides/conversation-state
- https://developers.openai.com/api/docs/guides/background
- https://developers.openai.com/api/docs/guides/migrate-to-responses
- https://developers.openai.com/api/docs/guides/function-calling
- https://developers.openai.com/api/docs/guides/structured-outputs
- https://developers.openai.com/api/docs/guides/tools-web-search
- https://developers.openai.com/api/docs/guides/tools-file-search
- https://developers.openai.com/api/docs/guides/tools-code-interpreter
- https://developers.openai.com/api/docs/guides/tools-computer-use
- https://developers.openai.com/api/docs/guides/image-generation
- https://developers.openai.com/api/docs/guides/streaming-responses
- https://developers.openai.com/api/docs/guides/batch
- https://developers.openai.com/api/docs/guides/prompt-caching
- https://developers.openai.com/api/docs/guides/rate-limits
- https://developers.openai.com/api/docs/api-reference/files
- https://developers.openai.com/api/docs/api-reference/vector-stores
- https://developers.openai.com/api/docs/guides/realtime
- https://developers.openai.com/api/docs/libraries
- https://developers.openai.com/api/docs/models
- https://developers.openai.com/api/docs/pricing
- https://developers.openai.com/api/docs/guides/fine-tuning
- https://developers.openai.com/api/docs/guides/evals

Fetched: 2026-08-05
