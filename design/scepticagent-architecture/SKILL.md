---
name: scepticagent-architecture
description: ScepticAgent internal architecture reference. Use whenever the user asks how the extension works, wants to add a new AI provider, add a new highlight category, debug communication between components, understand the agent loop or streaming, or work with provider routing and the Gemini CORS proxy.
---

## Communication flow

```
Side Panel (app.js)
  │  chrome.runtime.connect("agent") — one port per request
  ▼
Service Worker (background.js)
  │  fetch() to provider API
  ▼
AI Provider (Anthropic / OpenAI / Gemini)
```

Two parallel port connections fire on page open via `Promise.all`:
1. `streamViaPort("analyze")` — full analysis with agent loop
2. `quickHighlightPage()` — fast highlight scan

## Port message types

| Message | Meaning |
|---------|---------|
| `{ type: "status", message }` | Progress label shown in UI |
| `{ type: "tool_call", name, label }` | Tool being invoked |
| `{ type: "text_delta", text }` | Streamed text chunk |
| `{ type: "highlight_item", highlight, index }` | One highlight, emitted in real-time |
| `{ type: "highlights_result", summary, categorySummaries }` | Final highlights metadata |
| `{ type: "done" }` | Stream complete |
| `{ type: "error", message }` | Error — stops streaming |

## Agent loop (Claude only)

`runAgentLoop` / `runHighlightsAgentLoop` — up to 12 iterations (4 for highlights).
Stop reasons:
- `end_turn` → break
- `pause_turn` → continue (server-side web_search still running)
- `tool_use` → run `fetch_url`, re-submit with results

Tools: `web_search_20250305` (server-side, Anthropic-hosted), `fetch_url` (client-side, `fetchUrl()` in background.js).

## Streaming parser

`parseAgentStream(response, port, onTextDelta?)` reads the Anthropic SSE stream.
Optional `onTextDelta` callback intercepts text chunks — used by highlights to extract JSON objects in real-time via `extractCompleteHighlights()`.

## Real-time highlight extraction

`extractCompleteHighlights(buffer, fromPos)` — brace-depth character scanner that finds complete `{"phrase":...}` JSON objects in a mid-stream buffer without waiting for the full response. Returns `{ highlights, nextPos }`.

## Provider routing

`getProviderConfig()` reads `provider`, `${p}Key`, `${p}Model` from `chrome.storage.local`.

- `"anthropic"` → full agent loop with tools
- `"openai"` → `runOpenAIStream` — SSE streaming, no tools
- `"gemini"` → `runGeminiStream` + `geminiProxyFetch` — non-streaming, proxied through content script

## Gemini CORS proxy

Service workers send `Origin: chrome-extension://[id]` which Google's API rejects.
Fix: `geminiProxyFetch()` sends the request to the content script via `chrome.tabs.sendMessage`. The content script fetches from the page's `http/https` origin, which Google accepts.
Use `Content-Type: text/plain` + key as URL query param to avoid CORS preflight (simple request).

## Settings storage keys

| Key | Description |
|-----|-------------|
| `provider` | `"anthropic"` / `"openai"` / `"gemini"` |
| `anthropicKey` / `openaiKey` / `geminiKey` | API keys |
| `anthropicModel` / `openaiModel` / `geminiModel` | Selected model |
| `apiKey` | Legacy Anthropic key (still read for backwards compat) |

## Adding a new provider — checklist

- [ ] Add `const XXX_API_BASE` constant in `background.js`
- [ ] Add to `getProviderConfig()` key/model maps
- [ ] Implement `runXxxStream(port, apiKey, model, systemText, messages, signal)`
- [ ] Branch in `handleAnalyze`, `handleChat`, `handleHighlights`
- [ ] Add provider tab to `options/index.html` and logic to `options/app.js`
- [ ] Add API domain to `host_permissions` in `manifest.json`
- [ ] Update `CLAUDE.md` and `README.md`

## Adding a new highlight category — checklist

- [ ] Add to `LABELS` object and add `.ra-hl-{category}` CSS rule in `content.js`
- [ ] Add to `CAT_META` in `sidepanel/app.js`
- [ ] Add `.scan-pill.{cat}`, `.hl-dot.{cat}`, `.hl-item-dot.{cat}`, `.summary-bullet-{cat}` in `sidepanel/style.css`
- [ ] Add scan pill and legend entry in `sidepanel/index.html`
- [ ] Add category description in `buildHighlightsPrompt()` in `background.js`
- [ ] Update `CLAUDE.md` and `README.md`

## Known limitations

- **Gemini**: no streaming (`generateContent` only), no tool use, no real URLs in `source_url`
- **OpenAI**: no tool use, single-turn only
- **Highlights agent loop**: Claude only — non-Claude providers use `handleHighlightsSimple`
- **Page content**: truncated to 8000–10000 chars before sending to AI
