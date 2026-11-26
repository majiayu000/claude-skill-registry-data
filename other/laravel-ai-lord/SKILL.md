---
name: laravel-ai-lord
description: Lord skill for Laravel AI SDK, Laravel MCP server, Laravel Boost, and AI agent integration in Laravel 12/13 apps. Do not use for laravel filament lord tasks — use `laravel-filament-lord` instead. Do not use for laravel testing lord tasks — use `laravel-testing-lord` instead.
triggers:
  - laravel ai lord
  - laravel ai
  - laravel mcp
  - laravel boost
  - ai sdk
  - laravel agent
  - hitl
  - human in the loop
  - laravel llm
  - ذكاء اصطناعي لارافيل
personas:
  - ARCH
  - API
  - DEV
  - SEC
  - AI
  - ML
tech_stack:
  - laravel-ai-sdk
  - laravel-13
  - php-8-5
lord: true

---

# Laravel AI Lord

[OBJ] Integrate LLMs, agents, MCP servers, and AI tooling into Laravel 12/13 applications using first-party packages.

## Problem

Laravel 13 (Mar 2026) introduced a first-party AI SDK, MCP server package, and Boost (AI agent context). Ad-hoc integrations leak keys, bypass rate limits, skip human approval for destructive tool calls, and fail to leverage vector search. This skill enforces secure, idiomatic, production-grade AI integration.

## Rules

1. [REQ] **Use `laravel/ai` (v0.11+)** for all LLM calls. Never call OpenAI/Anthropic/Gemini SDKs directly — use `Ai::provider('openai')->text(...)` for abstraction, key rotation, and unified logging.
2. [REQ] **Keys in `config/ai.php` + `.env` only.** Never hardcode API keys. Use `AI_OPENAI_API_KEY`, `AI_ANTHROPIC_API_KEY`, etc. Rotate via `php artisan ai:keys:rotate`.
3. [REQ] **Streaming by default.** Use `Ai::stream(...)` for chat/completion — SSE-compatible, reduces TTFB. Avoid blocking `text()` for user-facing responses.
4. [REQ] **Embeddings + vector search.** Use `AsVector` Eloquent cast + `whereVectorSimilarTo('embedding', $query, $k)`. Requires `pgvector` (PostgreSQL) or `mysql-vector` extension.
5. [REQ] **Human-in-the-Loop (HITL) for destructive tools.** `Ai::agent(tools: [...], hitl: true)` — approve/deny/modify tool calls before execution. Mandatory for tools that write to DB, send emails, or call external APIs.
6. [REQ] **Tool definitions as PHP closures.** Tools are typed closures with JSON Schema: `Ai::tool(name: 'get_order', schema: [...], handler: fn($args) => ...)`.
7. [REQ] **Use `laravel/mcp` (v1.0-beta)** to expose your app as an MCP server for AI clients (Cursor, Claude, etc.). Tools/resources/prompts auto-discovered via attributes.
8. [REQ] **Use `laravel/boost` (v2.7+)** for AI agent context — versioned docs, guidelines, skills, MCP tools. `php artisan boost:publish` generates context bundle.
9. [REQ] **Rate-limit AI endpoints.** Use `RateLimiter::for('ai', ...)` — per-user, per-IP. LLM calls are expensive; prevent abuse.
10. [REQ] **Log token usage.** `Ai::logUsage()` records input/output tokens, cost, latency per call. Monitor with `ai:usage:report`.
11. [REQ] **Retry with exponential backoff.** `Ai::retry(times: 3, backoff: 100)` — handles 429, 500, timeout. Never retry 400/401/403.
12. [REQ] **Validate AI outputs.** Use `Ai::validate($output, schema: [...])` — JSON Schema validation. Reject malformed AI responses.
13. [PROHIBIT] Never expose raw API keys to frontend. All AI calls server-side only.
14. [PROHIBIT] Never skip HITL for tools with side effects (DB writes, emails, payments).
15. [PROHIBIT] Never use `file_get_contents` for AI API calls — use the SDK for streaming, retries, error handling.

## Commands

- `composer require laravel/ai` — install AI SDK
- `composer require laravel/mcp` — install MCP server
- `composer require laravel/boost` — install AI agent context
- `php artisan ai:keys:rotate` — rotate API keys
- `php artisan ai:usage:report` — token usage report
- `php artisan boost:publish` — publish AI context bundle

## References

- https://laravel.com/docs/ai-sdk
- https://laravel.com/docs/13.x/mcp
- https://laravel.com/docs/13.x/boost
- https://packagist.org/packages/laravel/ai
