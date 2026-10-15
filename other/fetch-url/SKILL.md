---
name: Fetch URL
description: HTTP GET/POST utility with size cap, SSRF guard, retries, and circuit breaker.
requires:
  bins: []
  env: []
---

# Fetch URL

Use this skill to download remote HTTP(S) content — raw API calls, web
pages, JSON endpoints, small files — safely. Private and metadata hosts
are blocked by default to prevent SSRF.

## Use when

- "Fetch this URL"
- "What does this API return?"
- Pipeline: fetch → `pdf-extract` → `summarize_text`
- Fetch a webhook payload or a small data file
- Check a public HTTP endpoint (status + headers)

## Do not use when

- Downloading binaries/archives > 50 MB (hard cap; the LLM context can't
  hold them anyway)
- Long-poll / streaming / SSE / WebSocket — this is one-shot request/response
- Authenticated APIs with complex OAuth flows — use a purpose-built
  extension (github, whisper, summarize) that owns the auth
- Calling internal services — set `allow_private: true` only on
  explicitly trusted operator calls

## Tools

### `status`
No arguments. Returns limits, policy, default timeout, user-agent.

### `fetch_url`
- `url` (string, required) — `http://` or `https://` only
- `method` (string, optional) — GET/POST/PUT/DELETE/HEAD/PATCH/OPTIONS (default GET)
- `headers` (object, optional) — `{"content-type": "application/json", ...}`
- `body` (string, optional) — request body as raw string; caller sets Content-Type
- `max_bytes` (integer, optional) — response cap. Default 5 MB, hard max 50 MB
- `timeout_secs` (integer, optional) — per-request timeout. Default 15s, max 120s
- `allow_private` (boolean, optional) — override SSRF guard. Default false

Returns `{status, final_url, headers, content_type, truncated, bytes_read, body_text?, body_base64?}`.

`body_text` is set for text-like content-types (text/*, json, xml, yaml,
javascript) if UTF-8 decodable. Otherwise `body_base64` is set and
`body_text` is null.

## Execution guidance

- **Start with a small `max_bytes`** (e.g. 100 000) when probing an unknown
  endpoint — you can always retry with a larger cap.
- Default timeout (15s) is fine for APIs; bump to 60–120s only for large
  files.
- If `status` is 4xx (-32002 error), the body preview is in the error
  message — read it before retrying.
- If `status` is 5xx (-32003), retries already exhausted inside the
  extension; do **not** retry from the LLM side — back off instead.
- `blocked_host` error (-32020) → the URL points to a private IP /
  loopback / metadata endpoint. Do **not** pass `allow_private=true`
  unless the operator explicitly asked to hit an internal service.
- `truncated: true` means the body was cut at `max_bytes`. Warn the user
  or re-fetch with a bigger cap if needed.
- For multi-step fetch-and-process, wrap the chain in TaskFlow so a
  restart doesn't re-fetch.

## Common pipelines

### URL → summary

```
1. fetch_url { url, max_bytes: 50000 }
2. summarize_text { text: body_text, length: "medium" }
```

### URL → PDF → summary

```
1. fetch_url { url: "https://.../doc.pdf", max_bytes: 5000000 }
2. (operator saves body_base64 to /tmp/doc.pdf)
3. pdf-extract.extract_text { path: "/tmp/doc.pdf", max_chars: 50000 }
4. summarize_text { text, length: "long" }
```

(Auto-saving to disk from inside the LLM is not yet supported — a future
extension `fetch_url_save` could do that safely.)
