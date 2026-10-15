---
name: claude-api
description: "Build apps with the Claude API or Anthropic SDK. TRIGGER when: code imports `anthropic`/`@anthropic-ai/sdk`/`claude_agent_sdk`, or user asks to use Claude API, Anthropic SDKs, or Agent SDK. DO NOT TRIGGER when: code imports `openai`/other AI SDK, general programming, or ML/data-science tasks."
license: Complete terms in LICENSE.txt
---
# Building LLM-Powered Applications with Claude

Use this skill for Claude API, Anthropic SDK, and Agent SDK implementation work. Start with the simplest surface that satisfies the task, detect the project language, then load only the relevant language-specific files.

## Defaults

Unless the user requests otherwise, use Claude Opus 4.6 with the exact model string `claude-opus-4-6`, adaptive thinking (`thinking: {type: "adaptive"}`) for non-trivial work, and streaming for long input, long output, or high `max_tokens`. Use SDK final-message helpers such as `.get_final_message()` / `.finalMessage()` when individual stream events are not needed.

Do not invent model IDs or append date suffixes. If an exact model is not in the cached table in `references/operating-reference.md`, read `shared/models.md` or current official docs before using it.

## Language Routing

Detect language from project files before loading examples:

| Signals | Read |
|---|---|
| Python files, `pyproject.toml`, `requirements.txt` | `python/` |
| TypeScript/JavaScript files, `package.json` | `typescript/` |
| Java/Kotlin/Scala files, JVM build files | `java/` |
| `go.mod` or Go files | `go/` |
| Ruby files or `Gemfile` | `ruby/` |
| C# project/files | `csharp/` |
| PHP files or `composer.json` | `php/` |
| Raw HTTP or unsupported language | `curl/` |

If multiple languages are plausible, use the current file/question context or ask one clarifying question.

## Surface Selection

Default order:

1. **Claude API single call** for classification, summarization, extraction, Q&A, and simple generation.
2. **Claude API + tool use** for code-orchestrated workflows and custom tools.
3. **Agent SDK** when Claude itself needs built-in file, web, terminal, permission, or MCP capabilities.
4. **Custom agent loop** only when the task is open-ended and the added cost/risk is justified.

Before building an agent, check complexity, value, viability, and cost of error. If any fails, use a simpler surface.

## Architecture Rules

- Everything routes through the Messages API unless a supporting endpoint is specifically needed.
- Use SDK tool runners/helpers instead of hand-rolled loops where possible.
- Use `output_config: {format: ...}` for structured outputs; do not use deprecated `output_format`.
- Use typed SDK request/response/error types instead of redefining them.
- Do not silently truncate oversized inputs; discuss chunking, summarization, or file APIs.

## Reading Guide

Load only what the task needs:

- Basic request/response: `{lang}/claude-api/README.md`
- Streaming UI: `{lang}/claude-api/README.md` + `{lang}/claude-api/streaming.md`
- Tool use / function calling / structured outputs: `{lang}/claude-api/README.md` + `shared/tool-use-concepts.md` + `{lang}/claude-api/tool-use.md`
- Batch processing: `{lang}/claude-api/README.md` + `{lang}/claude-api/batches.md`
- Reused file uploads: `{lang}/claude-api/README.md` + `{lang}/claude-api/files-api.md`
- Agent SDK: `{lang}/agent-sdk/README.md` + `{lang}/agent-sdk/patterns.md`
- HTTP errors: `shared/error-codes.md`
- Current official docs: `shared/live-sources.md`

Read `references/operating-reference.md` for the full language matrix, decision tree, model table, thinking/effort rules, compaction details, WebFetch guidance, and pitfalls.

## Current Critical Pitfalls

- Opus 4.6 / Sonnet 4.6 use adaptive thinking; do not use deprecated `budget_tokens` unless an older model is explicitly requested.
- Opus 4.6 does not support assistant-prefill control; use structured outputs or prompt instructions.
- Large `max_tokens` responses require streaming to avoid timeouts.
- Parse tool-call inputs with JSON parsers, not raw string matching.
- Prefer SDK helpers and SDK-exported types over custom wrappers and duplicate interfaces.
- For reports/documents/visualizations, consider code execution and Files API outputs when appropriate.

## When to Fetch Current Docs

Use current official documentation when the user asks for latest/current behavior, cached data appears stale, or the requested feature is not covered locally. Reference URLs are in `shared/live-sources.md`.
