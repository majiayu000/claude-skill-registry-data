---
name: claude-api
description: "Claude Messages API expert: current model IDs and pricing (Fable 5, Opus 5, Sonnet 5, Haiku 4.5 and legacy 4.x), context windows and max output, custom tool use and the tool_use/tool_result round trip, server tools (web search, web fetch, code execution, tool search, advisor, MCP connector) and client tools (bash, text editor, computer use, memory), SSE streaming and delta types, prompt caching breakpoints and TTLs, the Message Batches API, the Files API, token counting, rate limits and spend tiers, adaptive/extended thinking and the effort parameter, and structured JSON outputs plus strict tool use. WHEN: \"Messages API\", \"api.anthropic.com\", \"anthropic-version\", \"claude-opus-5\", \"claude-sonnet-5\", \"model ID\", \"Claude pricing\", \"cost per token\", \"MTok\", \"cache_control\", \"prompt caching\", \"cache_creation_input_tokens\", \"tool_use block\", \"tool_result\", \"tool_choice\", \"strict tool use\", \"output_config\", \"effort parameter\", \"budget_tokens\", \"adaptive thinking\", \"stream: true\", \"input_json_delta\", \"message_delta\", \"count_tokens\", \"ITPM\", \"OTPM\", \"429 rate limit\", \"batch API\", \"msgbatch\", \"Files API\", \"file_id\", \"web_search_20250305\", \"code_execution\", \"computer_20251124\", \"mcp_toolset\", \"advisor tool\", \"tool search tool\", \"pause_turn\". Do NOT use for: choosing between Anthropic/OpenAI/Google frontier models on capability tiers — that's `model-selection`; building an agent loop, sessions, or subagents with the Claude Agent SDK — that's `claude-agent-sdk`; configuring the Claude Code harness (settings.json, permissions, hooks, plugins, headless CI) — that's `claude-code`; the MCP protocol itself, transports, OAuth, or writing/consuming MCP servers beyond the API's `mcp_toolset` wiring — that's `mcp`; authoring SKILL.md files — that's `agent-skills`; prompt-injection taxonomy, OWASP GenAI Top 10, and agent threat modeling — that's `ai-security`; VM/container isolation and egress control for agent execution — that's `sandboxing` (and the containers plugin for Kubernetes depth); training or tuning models — that's `fine-tuning`; grading model or agent output — that's `evals`; OpenAI's platform API (Responses API, Chat Completions) — that's `openai-api`; running Claude through Bedrock/Vertex or an aggregator (endpoints, auth, throughput) — that's `inference-providers`."
license: MIT
---

# Claude Messages API

The raw HTTP API: `POST` a `messages` array, get a `Message` back with typed content blocks. Everything else — tools, caching, batches, thinking, structured outputs — is a parameter on that one request shape.

## Volatility rule — verify before you quote

Model IDs, prices, rate-limit tiers, dated tool-version strings, and beta headers all move. Every fact in this skill is a snapshot of Anthropic's docs as of **2026-08-05**, with the exact source URL at the bottom of each file.

Always re-check the cited source URL before putting a price into a budget, a model ID into production config, or a beta header into a deploy. Never quote a number for a model this skill does not list — say it is unverified and point at the pricing/models pages.

## Routing

| Request | Load |
|---|---|
| Model IDs, context windows, pricing, batch/fast-mode rates, tool token overhead | `references/models-and-pricing.md` |
| Custom tool schemas, `tool_choice`, round trip, tool search tool | `references/tool-use.md` |
| Web search, web fetch, code execution container | `references/server-tools.md` |
| Computer use: actions, display sizing, coordinate scaling | `references/computer-use.md` |
| `mcp_servers` + `mcp_toolset` wiring, allowlists, auth | `references/mcp-connector.md` |
| Executor/advisor pairing, advisor caching and cost control | `references/advisor-tool.md` |
| SSE event flow, delta types, mid-stream errors | `references/streaming.md` |
| `cache_control`, breakpoints, TTLs, minimum cacheable tokens | `references/prompt-caching.md` |
| Message Batches API, Files API | `references/batches-and-files.md` |
| RPM/ITPM/OTPM tiers, response headers, `count_tokens` | `references/rate-limits-and-token-counting.md` |
| `thinking`, `budget_tokens`, `output_config.effort` | `references/thinking-and-effort.md` |
| `output_config.format`, JSON Schema support matrix, `strict` | `references/structured-outputs.md` |
| "Does this work on the model generation I'm on?" | `references/versions/claude-4-5-and-earlier.md`, `claude-4-6.md`, `claude-4-7-plus.md` |

## Request essentials

Base host `api.anthropic.com`. Send `x-api-key`, `anthropic-version: 2023-06-01`, and `content-type: application/json` on every call.

Endpoints this skill covers: `/v1/messages/count_tokens`, `/v1/messages/batches`, `/v1/files`, `GET /v1/models`.

Always pin a model ID explicitly and treat it as a snapshot. From Claude 4.6 onward, **dateless IDs are pinned snapshots too** — `claude-opus-4-6` is not an evergreen pointer, so a "latest model" alias strategy does not exist and upgrades are always a deliberate config change.

Never reuse token estimates across a 4.7 boundary. Claude Fable 5, Mythos 5, and Opus 4.7+ use a newer tokenizer that produces **~30% more tokens for the same text** than pre-4.7 models — recount with `count_tokens` against the target model when migrating.

Query capabilities programmatically rather than hardcoding a matrix: `GET /v1/models` returns `max_input_tokens`, `max_tokens`, and `capabilities`.

A modern request is the classic body plus three optional config surfaces — `output_config` (effort + JSON format), `cache_control`, and `tools`/`mcp_servers`:

```json
{
  "model": "claude-opus-5",
  "max_tokens": 4096,
  "cache_control": {"type": "ephemeral"},
  "system": "You are a helpful assistant.",
  "messages": [{"role": "user", "content": "..."}],
  "tools": [{"type": "code_execution_20250825", "name": "code_execution"}],
  "output_config": {"effort": "medium"}
}
```

Dated type strings (`code_execution_20250825`, `web_search_20260318`, `computer_20251124`, `tool_search_tool_bm25_20251119`, `advisor_20260301`) are the tool's **spec version**, not a release date to ignore. Newer versions add capabilities and sometimes require a newer backing version of another tool — web search/fetch `_20260209`+ require `code_execution_20260120`+. Check the per-tool version tables in the references before copying a type string between projects.

## Model choice inside the Claude lineup

Current lineup and full price tables live in `references/models-and-pricing.md`. Read it before any cost estimate. Cross-vendor comparison (Anthropic vs OpenAI vs Google) is not this skill — that is `model-selection`.

Shape of the lineup as of 2026-08-05: Fable 5 / Mythos 5 / Opus 5 / Sonnet 5 all carry **1M-token context and 128k max output** with always-available adaptive thinking; Haiku 4.5 is 200k/64k and is the last mainstream model on manual extended thinking.

Long context is not a premium tier on Claude 4.6+ — the **full 1M window bills at standard per-token rates**, so a 900k-token request costs the same per token as a 9k one. Do not architect chunking purely to dodge a long-context surcharge that no longer exists.

Two multipliers change the math and are easy to forget: `inference_geo: "us"` applies **1.1x** to every token category on Claude 4.6+ (400 error on earlier models), and Fast mode (research preview, Opus 5 / Opus 4.8 only) reprices to $10/$50 per MTok and is unavailable in batches.

## Tool use

Client tools run in your code; server tools run on Anthropic's infrastructure and need no handler. Getting this wrong is the most common design error — you never write an executor for `web_search`, and you always write one for `bash`, `text_editor`, `computer`, and `memory` even though Anthropic supplies their schemas.

Round-trip rules that break requests when violated:

- Append the assistant's content array **unchanged**, then a `user` message carrying `tool_result` with the matching `tool_use_id`. Never hand-rebuild the assistant turn.
- Server-tool results arrive already embedded in the response — never send a `tool_result` for a `srvtoolu_...` ID.
- Round-trip opaque fields verbatim: `encrypted_content` / `encrypted_index` from web search, `advisor_redacted_result`, thinking `signature`. Mutating them 400s.
- `tool_choice` is `auto` (default), `any`, `{"type":"tool","name":...}`, or `none`. Add `disable_parallel_tool_use: true` to cap at one call per turn.
- Set `"strict": true` on a tool definition when the call must validate against `input_schema` — cheaper than retry loops.

Every tool you attach costs input tokens on every request, before Claude does anything. Budget the tool-use system-prompt overhead (286–804 tokens depending on model and `tool_choice`) plus per-tool costs — bash +244/+325, text editor +700, computer use 735 — from `references/models-and-pricing.md`.

When the catalog grows past ~10 tools or ~10k tokens of definitions, switch to the **tool search tool** with `defer_loading: true` rather than trimming descriptions; selection accuracy degrades past 30–50 loaded tools. See `references/tool-use.md`.

## Server tools

| Tool | What it does | Read |
|---|---|---|
| `web_search` | Anthropic-run search, citations always on | `references/server-tools.md` |
| `web_fetch` | Fetch a URL/PDF already present in context | `references/server-tools.md` |
| `code_execution` | Sandboxed Python 3.11 container, no internet | `references/server-tools.md` |
| `tool_search_tool_regex` / `_bm25` | Discover tools from a large deferred catalog | `references/tool-use.md` |
| `advisor` | Cheap executor consults a stronger advisor mid-turn | `references/advisor-tool.md` |
| MCP connector (`mcp_toolset`) | Call remote MCP servers without your own client | `references/mcp-connector.md` |

Always check platform availability before promising a server tool. Several — web search (dynamic filtering), web fetch, code execution, MCP connector, advisor — are **not available on Amazon Bedrock or Google Cloud**, and Microsoft Foundry needs a Hosted-on-Anthropic deployment. "It works on the Claude API" is not a statement about Bedrock.

Never enable `web_fetch` on a request that mixes untrusted input with sensitive data without constraints. The URL-validation rule (fetch only URLs already in context) blocks Claude-constructed exfiltration URLs, but `allowed_domains` and `max_uses` are the controls you actually configure. Never set `allowed_domains` and `blocked_domains` together — that is a 400.

Long server-tool turns can end `stop_reason: "pause_turn"`. Resume by resending the paused assistant content unchanged; do not treat it as an error or a completed turn.

## Thinking and effort

Manual extended thinking is a legacy path. `thinking: {"type": "enabled"}` is deprecated on Claude 4.6 and **returns 400 on Claude 4.7 and later** (Opus 4.7/4.8/5, Sonnet 5, Fable 5, Mythos 5), which support adaptive thinking only. Migrate to `{"type": "adaptive"}` plus `output_config.effort` — see `references/thinking-and-effort.md`.

`effort` defaults to `high` wherever it is supported, so setting `high` explicitly changes nothing. Step to `xhigh`/`max` for long-horizon agentic and coding work, `medium` for cost savings, `low` for subagents and latency-sensitive chat.

Hold `effort` and `budget_tokens` **constant across a cached conversation** — both are rendered into the prompt, so changing either invalidates cache breakpoints. This is the single most common silent cache-cost regression.

When running `xhigh`/`max` on Opus 4.7/4.8/5, set `max_tokens` to 64k+ so thinking and tool calls have room.

## Prompt caching

Use automatic caching (one top-level `cache_control`) for multi-turn conversations; use explicit block-level breakpoints when you need to cache independent sections (max **4 breakpoints**).

Place breakpoints on static prefixes — system prompt, tool definitions, large documents — and keep the last cached block byte-identical between requests. Any drift above the breakpoint is a full miss.

Caching failures are silent: prompts below the model minimum (512 on Opus 5/Fable 5/Mythos 5, up to 4,096 on Opus 4.6/4.5/Haiku 4.5) are simply not cached, with no error. Always verify via `cache_creation_input_tokens` / `cache_read_input_tokens` in `usage`.

Cache reads are the main throughput lever, not just a discount: for every current model except Haiku 3.5, `cache_read_input_tokens` do **not** count toward ITPM. An 80% hit rate against a 2M ITPM limit processes ~10M input tokens/minute.

Reach for `ttl: "1h"` (2x base input on the write) when the reuse window exceeds 5 minutes — long agent loops and batches especially.

## Streaming

Set `"stream": true`, or use the SDK stream helpers to accumulate the final `Message` and dodge HTTP timeouts on large `max_tokens`.

Accumulate `input_json_delta` fragments and parse **only after `content_block_stop`** — partial JSON is not valid JSON. Treat `usage` on `message_delta` as cumulative, not incremental, or you will double-count.

Handle unknown event types gracefully; Anthropic adds them under its versioning policy. Mid-stream `error` events (e.g. `overloaded_error`, the streaming form of HTTP 529) are normal and must be caught.

Interruption recovery differs by model generation — resend partial text as an `assistant` message on 4.5 and earlier, but as a **`user` continuation instruction** on 4.6+. Tool-use and thinking blocks cannot be partially recovered. Details in `references/streaming.md`.

## Batches, files, limits

Use the **Message Batches API** for anything latency-tolerant: 50% off input and output, most batches under an hour. Caps: 100,000 requests or 256 MB, 24-hour processing window, results downloadable for 29 days. Always match results by `custom_id` — order is not preserved.

Never assume sync parameters carry over: `stream`, `speed`, `store`/`previous_thread_event_id`, `cache_hint`/`context_hint`, `max_tokens: 0`, and `research_preview_2026_02` are rejected inside a batch. Conversely, batches are the **only** path to 300k output tokens (beta header `output-300k-2026-03-24`).

Treat Files API uploads as **workspace-scoped, not user-scoped**. Any API key in the workspace can read any file, so never accept a `file_id` supplied by an end user — keep the user↔file mapping server-side.

`POST /v1/messages/count_tokens` is free, has its own RPM pool, and does not consume Messages rate limit. Use it for pre-flight sizing; treat the result as an estimate.

Retry on `429` using the `retry-after` header, and read `anthropic-ratelimit-*` headers rather than guessing. Rate limits are token-bucket, so a 60 RPM limit can 429 on a burst that averages under 60/minute. `max_tokens` does not affect OTPM accounting — there is no rate-limit reason to set it low.

## Structured outputs

Prefer `output_config.format` with a JSON Schema over prompt-and-parse; Claude returns schema-valid JSON in the text block with no retry loop. Use `strict: true` on tools for the same guarantee on tool inputs.

Design schemas to the supported subset — no recursion, no numeric or string-length constraints, `additionalProperties` only `false`. Validate business rules in your code, not in the schema. Full matrix in `references/structured-outputs.md`.

## Cost estimation checklist

Never quote a per-request cost from base input/output rates alone. Sum:

1. Uncached input + cache writes (1.25x at 5m, 2x at 1h) + cache reads (0.1x) at the model's base rate.
2. Tool-use system-prompt overhead + per-tool definition tokens, on every request that carries tools.
3. Output tokens including thinking tokens (`usage.output_tokens_details.thinking_tokens`).
4. Metered server tools: web search at $10/1,000 searches; standalone code execution at $0.05/hour/container past 1,550 free hours/org/month (free alongside `web_search_20260209`+/`web_fetch_20260209`+).
5. Advisor calls, billed at the **advisor model's** rates via `usage.iterations[]`.
6. Multipliers: 0.5x for batch, 1.1x for `inference_geo: "us"`, Fast-mode repricing.

## Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| 400 on `thinking.type: "enabled"` | Model is 4.7+ | Switch to adaptive thinking + `effort` |
| 400 on domain filters | `allowed_domains` and `blocked_domains` both set | Pick one |
| 400 on a search follow-up | `encrypted_content`/`encrypted_index` altered or dropped | Round-trip verbatim |
| 400 "all tools cannot be deferred" | Every tool has `defer_loading: true` | Leave the search tool non-deferred |
| 400 on a deferred tool | `cache_control` on a `defer_loading: true` tool | Move the breakpoint to a non-deferred tool |
| Cache hit rate ~0 | `effort`/`budget_tokens` changed, or prefix drift | Freeze both across the cached session |
| Costs higher than modeled | Tool definition overhead and thinking tokens omitted | Re-run the checklist above |
| Batch request rejected | `stream`/`speed`/`max_tokens: 0` present | Strip unsupported params |
| Turn ends unexpectedly | `stop_reason: "pause_turn"` | Resend paused assistant content unchanged |
| 429 under the per-minute average | Token-bucket burst enforcement | Smooth the request rate; honor `retry-after` |

## Diagnostic scripts

Read-only, safe against a live key.

- `scripts/list-models.sh` — `GET /v1/models`; confirms which model IDs and capability fields your key actually sees.
- `scripts/count-tokens.sh <payload.json>` — free `count_tokens` pre-flight for a request body.

## Not covered here

The corpus behind this skill does not include Anthropic's error/HTTP-status reference, SDK installation guides, the Threads (`store`/`previous_thread_event_id`) API, or Claude Managed Agents beyond the pricing and rate-limit figures cited. Treat anything about those as unverified and check the docs directly.

## Sources

- https://platform.claude.com/docs/en/about-claude/models/overview
- https://platform.claude.com/docs/en/about-claude/pricing
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool
- https://platform.claude.com/docs/en/agents-and-tools/mcp-connector
- https://platform.claude.com/docs/en/build-with-claude/streaming
- https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- https://platform.claude.com/docs/en/build-with-claude/batch-processing
- https://platform.claude.com/docs/en/build-with-claude/files
- https://platform.claude.com/docs/en/api/rate-limits
- https://platform.claude.com/docs/en/build-with-claude/token-counting
- https://platform.claude.com/docs/en/build-with-claude/extended-thinking
- https://platform.claude.com/docs/en/build-with-claude/effort
- https://platform.claude.com/docs/en/build-with-claude/structured-outputs

Fetched: 2026-08-05
