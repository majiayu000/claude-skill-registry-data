---
name: pal-mcporter
description: Run PAL MCP tools (precommit, codereview, secaudit, debug, apilookup, listmodels, etc.) via the `mcporter` CLI against the PAL stdio MCP server (`uvx … pal-mcp-server`) instead of configuring PAL as a Codex MCP server in `~/.codex/config.toml`. Use when you want shell/script-friendly PAL runs, want to avoid MCP tool-schema context overhead, or need PAL access in an environment without Codex MCP wiring.
---

# PAL via MCPorter

## Quick start

- See which tools are available (from the bundled generated CLI help):
  - `bash "<path-to-skill>/scripts/pal"`
- Print copy/pastable examples for every tool currently exposed by your PAL server:
  - `bash "<path-to-skill>/scripts/pal" examples`
- Run a fast self-test (validates bundled CLI + PAL server startup; no live model call):
  - `bash "<path-to-skill>/scripts/pal" selftest`
- Run self-test including live model calls (costs tokens; requires an API key):
  - `bash "<path-to-skill>/scripts/pal" selftest --live`
- Call tools:
  - `bash "<path-to-skill>/scripts/pal" -o json version`
  - `bash "<path-to-skill>/scripts/pal" -o json listmodels`
  - `bash "<path-to-skill>/scripts/pal" -o markdown apilookup --prompt "OpenAI Responses API streaming"`
  - `bash "<path-to-skill>/scripts/pal" -o markdown chat --prompt "ping" --working-directory-absolute-path "$PWD" --model auto`

## Workflow

1) Read the embedded tool list.
   - `bash "<path-to-skill>/scripts/pal"`
2) Use examples to find minimal calls / argument shapes (recommended).
   - `bash "<path-to-skill>/scripts/pal" examples`
3) Call the tool via the bundled CLI.
   - Prefer `--raw '{...}'` for complex payloads and optional parameters.
   - Global flags (`-o/--output`, `-t/--timeout`) must come **before** the tool name.
4) Treat stdout as the tool result.
   - Use `-o markdown` for readability or `-o json` when you want structured output.

## Does this match `pal-mcp-server`?

Mostly. This skill runs PAL via `uvx … pal-mcp-server` and bundles a CLI generated from PAL’s tool schemas via `mcporter generate-cli`. If upstream adds/removes tools, the bundled CLI may need to be regenerated.

- Check which PAL version you’re running: `bash "<path-to-skill>/scripts/pal" -o json version`
- Source-of-truth tool surface (live): `bash "<path-to-skill>/scripts/pal" examples`

## Notes (from upstream + schemas)

- Tool surface can be reduced with `DISABLED_TOOLS` (helpful for clients that ingest tool schemas). Upstream often recommends: `analyze,refactor,testgen,secaudit,docgen,tracer` to save context.
- Upstream PAL supports multi-turn threads via `continuation_id`, but this skill runs PAL in ad-hoc STDIO mode (fresh server per invocation), so continuations generally won’t resume across separate `pal` commands.
- Prefer passing files via `absolute_file_paths` (and images via `images`) rather than pasting large blobs into prompts.

## Selftest knobs

- `PAL_SELFTEST_CLI_NAME`: which CLI `clink` should call in `selftest --live` (auto-detects `codex`, `claude`, `gemini` if present in `PATH`)
- `PAL_SELFTEST_MODEL`: optionally override the model used during `selftest --live` (when supported by the tool)
- `PAL_SELFTEST_THINKING_MODE`: defaults to `minimal`

## Configuration

This skill uses ad-hoc stdio mode (no `mcporter.json` required) and ships a bundled CLI at `scripts/pal-cli.js`.

Set these env vars when needed:

- `OPENAI_API_KEY` (required for OpenAI-backed PAL usage; alternatives include `GEMINI_API_KEY`, `OPENROUTER_API_KEY`, etc.)
- `PAL_DEFAULT_MODEL` (default: `auto`; forwarded as `DEFAULT_MODEL` when `DEFAULT_MODEL` is unset)
- `PAL_MCP_FROM` (default: `git+https://github.com/BeehiveInnovations/pal-mcp-server.git`)
- `MCPORTER_VERSION` (default pinned in `"<path-to-skill>/scripts/pal"`)
- `PAL_MCPORTER_TIMEOUT_MS` (default: `120000`)
- `DISABLED_TOOLS` (PAL setting; comma-separated tool names to hide/disable in the server; unset/empty enables all)

## Notes

- `bash "<path-to-skill>/scripts/pal"` is the quick “what’s available?” view; use `examples` when you need parameter shapes.
- STDIO mode inherits your shell environment automatically; avoid passing secrets via `--env KEY=value` unless you have to.
- If PAL startup is slow (first `uvx` run), increase timeouts with `PAL_MCPORTER_TIMEOUT_MS` or `-t <ms>`.
