---
name: http-client
description: Full-featured HTTP client with method, headers, body support, and automatic HTML text extraction
activation_keywords: [http, request, api, curl, get, post, put, delete, webhook, fetch, url]
execution_mode: server
---

# HTTP Client Skill

Provides full HTTP client capabilities beyond simple URL fetching:
- Support all HTTP methods: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS
- Custom headers and query parameters
- JSON and form-encoded request bodies
- Response status, headers, and body inspection
- **Automatic text extraction**: HTML pages are automatically stripped of tags and converted to readable text

Use `builtin_http_client` tool with fields:
- `method`: HTTP method (GET, POST, PUT, PATCH, DELETE, etc.)
- `url`: the target URL (https only)
- `headers`: (optional) JSON object of headers
- `body`: (optional) request body string
- `content_type`: (optional) content type for body (default: application/json)

Note: Private/local hosts are blocked for security.

## When to use HTTP Client vs Browser

- **Prefer `builtin_http_client`** for calling HTTPS APIs, webhooks, and **reading page-like URLs** where a single GET/POST and **HTML → text** (or raw body) is enough. No DOM, no in-page clicks, no JavaScript rendering in a browser engine.
- **Use `builtin_browser`** (skill **`builtin_skill.browser_client`**) only on the **AI TaskMeta desktop**: it opens a **visible Chrome** and uses **CDP** (navigate, DOM actions, text for the model). It is **not** headless and **not** server-side HTTP. For **API-only** fetch, use **`builtin_http_client`**. The API server does not run desktop browser tools.
- **Summary**: HTTP Client = server-side HTTPS fetch; Browser = desktop visible Chrome automation. Prefer HTTP when a single request and HTML/body text is enough.
