---
name: xai
description: Use for xAI/Grok API capabilities through the lfg xai_grok MCP — text generation, web search, X/Twitter search, image/video generation, and TTS. Load when the user wants Grok-connected xAI tools beyond built-in host tools, or when search_tool should target xai_* MCP tools.
---

# xAI (Grok-connected)

One skill for all **lfg `xai_grok` MCP** tools (`~/.grok/plugins/lfg/mcp-runtimes/xai-grok-mcp`). Use this skill instead of guessing tool names.

## Setup check

1. Run `lfg setup --run` (or reinstall) so the plugin ships `xai_grok` in `.mcp.json` and this `skills/xai` directory under `~/.grok/plugins/lfg/skills/xai`.
2. Credentials (priority): dedicated `~/.grok/xai-grok-mcp-auth.json` via **`lfg xai auth set-api-key`**, **`lfg xai auth set-oauth`**, or the MCP tools `xai_auth_set_api_key` / `xai_auth_set_oauth`; then `XAI_API_KEY`; then read-only Grok host `~/.grok/auth.json` (host file is never written by xai_grok MCP). Never log tokens or keys.
3. Do not use `/mcps` OAuth authenticate (`i`) for `xai_grok`: Grok only runs that host-managed OAuth flow for HTTP/SSE MCP servers, while `xai_grok` is local stdio. Use `xai_auth_*` tools instead.

## Tool flow (all capabilities)

1. `search_tool` with a specific query, e.g. `"xai web search"`, `"xai x search"`, `"xai image generate"`.
2. Call the qualified MCP tool via `use_tool` using the **exact** schema from step 1 (server is typically `xai_grok`; tool names use underscores: `xai_web_search`, not hyphens).

## Capability router

| User intent | MCP tool | `search_tool` hint |
|-------------|----------|-------------------|
| Draft, rewrite, summarize, reason (no live web) | `xai_generate_text` | `xai generate text` |
| Current web info + citations | `xai_web_search` | `xai web search` |
| X/Twitter posts, handles, real-time social | `xai_x_search` | `xai x search` |
| Still images (Grok Imagine) | `xai_image_generate` | `xai image generate` |
| Video (text/image/reference) | `xai_video_generate` | `xai video generate` |
| Speech / TTS | `xai_tts` | `xai tts` |

Details and example payloads: [references/tools.md](references/tools.md).

## Cross-cutting rules

- **Text vs search:** Use `xai_generate_text` for closed-book generation; use `xai_web_search` or `xai_x_search` when recency or sources matter.
- **X evidence:** Treat posts as leads or primary-source quotes only with relevant account identity; corroborate facts via web/docs before asserting them as settled.
- **Artifacts:** Image/video tools may return URLs, base64, or local paths under `.grok-xai-artifacts` when the schema supports `artifact_dir`.
- **Fallback:** If `xai_grok` is disconnected, say so explicitly; use host-native `web_search` / `x_search` only if the user still wants a fallback.

## Credential safety

Use credentials exposed by the Grok host or MCP server only. Never print, quote, summarize, or store OAuth tokens, refresh tokens, bearer tokens, or API keys.
