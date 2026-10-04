---
name: cursor-cursor-sdk
description: "Use when building or troubleshooting an integration with the external Cursor TypeScript SDK (@cursor/sdk), including Agent.create, Agent.prompt, Agent.resume, streaming, MCP, local or cloud runs, and error handling."
---

# Bounded Cursor SDK migration for Codex

Use this mirror when the request concerns `@cursor/sdk`, `Agent.create`, `Agent.prompt`, `Agent.resume`, `agent.send`, `run.stream`, `run.wait`, `CursorAgentError`, local/cloud selection, or MCP configuration. Preserve the upstream SDK guidance as external reference while using the local migration adapter for the Codex path.

## Workflow

1. Convert the requested operation to a JSON object with `operation` (`prompt`, `create`, `resume`, `send`, `wait`, or `stream`) and only the required safe fields. Do not include `CURSOR_API_KEY`, `apiKey`, headers, environment credentials, MCP servers, or auth material.
2. Run `python3 scripts/cursor_sdk_native_adapter.py plan` with the JSON request on stdin. The adapter emits the closest native Codex operations (`create_thread`, `send_message_to_thread`, `wait_threads`, and bounded `read_thread`) and keeps `run.stream` as a no-streaming-equivalent wait/readback pair.
3. For a read-only native operation, the coordinator may supply an already-authorized native Codex bridge to `run_native_migration(..., execute=True)`. The bridge is external to this script; its result is validated and never treated as Cursor SDK parity.
4. A missing bridge is `UNAVAILABLE`, and a missing bridge method is `MISSING_CAPABILITY`. A mutating native task operation requires explicit authorization and is never created by the CLI or this mirror.
5. Report native bridge errors as `NATIVE_ERROR` without copying provider messages, paths, credentials, or MCP configuration. A credential/MCP-shaped request or result is `FAIL_CLOSED`.

## Security and provenance

The pinned upstream scanner verdict `blocked_malicious` remains retained. Keep the concrete `references/auth.md:100` credential-path finding and MCP hook/configuration findings visible in review records. Do not publish or copy those reference files into a native mirror, read `CURSOR_API_KEY`, install `@cursor/sdk`, import or execute the Cursor runtime, activate MCP, or infer cloud/local equivalence. The native adapter proves only its bounded translation and caller-supplied bridge contract; actual Cursor SDK behavior and native Codex task execution require a separate authorized runtime pass.
