---
name: web-reader
description: Fetches the content of any URL and returns clean Markdown text. Suitable for scenarios where users share links and need to read, analyze, summarize, or translate web page content.
license: MIT
---

## Capability Overview

A Jina AI Reader proxy service deployed on AWS Lambda that fetches and parses target web page content via JWT authentication, automatically removes noise such as ads, navigation, and scripts, and returns structured Markdown text.

| Field | Description |
|-------|-------------|
| Endpoint | `GET https://api-ELbWqODdAgNY@36oqjsxjo775h3odjp3eev3y740deicu.lambda-url.us-west-2.on.aws/{url}` |
| Response Format | `text/plain` (Markdown by default) |
| Authentication | platform_managed (`INTEGRATIONS_API_KEY`) |

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | Yes | The full URL of the target web page, appended directly after the Base URL |

**Optional Request Headers (output behavior control):**

| Header | Type | Description |
|--------|------|-------------|
| `X-Return-Format` | string | Return format: `markdown` (default) / `html` / `text` / `screenshot` / `pageshot` |
| `X-With-Images-Summary` | boolean | Whether to append an image description summary |
| `X-With-Links-Summary` | boolean | Whether to append a links summary |
| `X-Target-Selector` | string | CSS selector to extract content from specific elements only |
| `X-Remove-Selector` | string | CSS selector to remove specific elements |
| `X-Timeout` | number | Page load timeout (seconds) |
| `X-No-Cache` | boolean | Set to `true` to disable cache and force re-fetch |
| `Accept` | string | Set to `text/event-stream` to enable streaming response (SSE) |

**Response Example:**

```
Title: Example Domain

URL Source: http://example.com

Markdown Content:
# Example Domain

This domain is for use in illustrative examples in documents...
```

**Response Headers:**

| Header | Description |
|--------|-------------|
| `Content-Type` | `text/plain; charset=utf-8` |
| `x-usage-tokens` | Number of tokens consumed by this request |
| `cf-cache-status` | Cloudflare cache status |
| `x-amzn-RequestId` | AWS Lambda request ID |

**Error Codes:**

| HTTP Status | Description |
|-------------|-------------|
| 200 | Success; response body is the parsed Markdown text |
| 401 | JWT Token missing or invalid |
| 403 | Token valid but target URL is blocked by GFW |

---

## Generation-Phase Usage (Direct Agent Invocation)

```typescript
const apiKey = process.env["INTEGRATIONS_API_KEY"]!; // platform_managed key injected by the platform

/**
 * Fetches the target web page and returns its content in Markdown format.
 * @param targetUrl - The full URL of the target web page
 * @param options - Optional output control parameters
 * @param options.returnFormat - Return format, default is markdown
 * @param options.withImagesSummary - Whether to append an image summary
 * @param options.withLinksSummary - Whether to append a links summary
 * @param options.targetSelector - CSS selector to extract specific elements only
 * @param options.removeSelector - CSS selector to remove specific elements
 * @param options.timeout - Page load timeout (seconds)
 * @param options.noCache - Whether to disable cache
 * @param options.accept - Accept request header; set to `text/event-stream` to enable SSE streaming mode, default is `text/html`
 * @returns The web page's Markdown text content (non-streaming) or an SSE stream (streaming)
 */
async function fetchWebPage(
  targetUrl: string,
  options?: {
    returnFormat?: "markdown" | "html" | "text" | "screenshot" | "pageshot";
    withImagesSummary?: boolean;
    withLinksSummary?: boolean;
    targetSelector?: string;
    removeSelector?: string;
    timeout?: number;
    noCache?: boolean;
    accept?: "text/html" | "text/event-stream";
  }
): Promise<string> {
  const encodedUrl = encodeURIComponent(targetUrl);
  const endpoint =
    `https://api-ELbWqODdAgNY@36oqjsxjo775h3odjp3eev3y740deicu.lambda-url.us-west-2.on.aws/${encodedUrl}`;

  const headers: Record<string, string> = {
    "X-Gateway-Authorization": `Bearer ${apiKey}`,
  };

  if (options?.returnFormat) headers["X-Return-Format"] = options.returnFormat;
  if (options?.withImagesSummary !== undefined) {
    headers["X-With-Images-Summary"] = String(options.withImagesSummary);
  }
  if (options?.withLinksSummary !== undefined) {
    headers["X-With-Links-Summary"] = String(options.withLinksSummary);
  }
  if (options?.targetSelector) headers["X-Target-Selector"] = options.targetSelector;
  if (options?.removeSelector) headers["X-Remove-Selector"] = options.removeSelector;
  if (options?.timeout !== undefined) headers["X-Timeout"] = String(options.timeout);
  if (options?.noCache) headers["X-No-Cache"] = "true";
  if (options?.accept) headers["Accept"] = options.accept;

  const response = await fetch(endpoint, { method: "GET", headers });

  if (response.status === 401) throw new Error("Authentication failed: JWT Token missing or invalid");
  if (response.status === 403) throw new Error("Target URL is blocked by GFW and cannot be accessed");
  if (!response.ok) throw new Error(`HTTP error: ${response.status}`);

  return await response.text();
}

// Usage example
const markdown = await fetchWebPage("https://example.com", {
  withLinksSummary: true,
});
console.log(markdown);
```

---

## Post-Generation Usage (Invocation via Edge Function within the App)

### Edge Function Code

```typescript
// edge-functions/web-reader.ts
import { serve } from "https://deno.land/std/http/server.ts";

serve(async (req: Request): Promise<Response> => {
  /**
   * Web Reader Edge Function
   * Receives frontend requests, injects the platform API key, and forwards them to the upstream Jina Reader service.
   * Request body: { url: string, options?: {...} }
   * Response: { content: string }
   */
  if (req.method !== "POST") {
    return new Response("Method Not Allowed", { status: 405 });
  }

  // --- Parse client request ---
  let targetUrl: string;
  let returnFormat: string | undefined;
  let withImagesSummary: boolean | undefined;
  let withLinksSummary: boolean | undefined;
  let targetSelector: string | undefined;
  let removeSelector: string | undefined;
  let timeout: number | undefined;
  let noCache: boolean | undefined;

  try {
    const body = await req.json();
    targetUrl = body.url;
    if (!targetUrl) throw new Error("Missing url");
    returnFormat = body.returnFormat;
    withImagesSummary = body.withImagesSummary;
    withLinksSummary = body.withLinksSummary;
    targetSelector = body.targetSelector;
    removeSelector = body.removeSelector;
    timeout = body.timeout;
    noCache = body.noCache;
  } catch {
    return new Response(JSON.stringify({ error: "Invalid request body" }), {
      status: 400,
      headers: { "Content-Type": "application/json" },
    });
  }

  // --- Inject platform API key (must never be exposed to the frontend) ---
  const apiKey = Deno.env.get("INTEGRATIONS_API_KEY");
  if (!apiKey) {
    return new Response(JSON.stringify({ error: "Server configuration error" }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }

  // --- Build request headers ---
  const upstreamHeaders: Record<string, string> = {
    "X-Gateway-Authorization": `Bearer ${apiKey}`,
  };
  if (returnFormat) upstreamHeaders["X-Return-Format"] = returnFormat;
  if (withImagesSummary !== undefined) {
    upstreamHeaders["X-With-Images-Summary"] = String(withImagesSummary);
  }
  if (withLinksSummary !== undefined) {
    upstreamHeaders["X-With-Links-Summary"] = String(withLinksSummary);
  }
  if (targetSelector) upstreamHeaders["X-Target-Selector"] = targetSelector;
  if (removeSelector) upstreamHeaders["X-Remove-Selector"] = removeSelector;
  if (timeout !== undefined) upstreamHeaders["X-Timeout"] = String(timeout);
  if (noCache) upstreamHeaders["X-No-Cache"] = "true";

  // --- Call upstream service ---
  const encodedUrl = encodeURIComponent(targetUrl);
  const upstream = await fetch(
    `https://api-ELbWqODdAgNY@36oqjsxjo775h3odjp3eev3y740deicu.lambda-url.us-west-2.on.aws/${encodedUrl}`,
    { method: "GET", headers: upstreamHeaders }
  );

  // Forward authentication/filtering errors
  if (upstream.status === 401 || upstream.status === 403) {
    const errText = await upstream.text();
    return new Response(JSON.stringify({ error: errText || `Upstream error: ${upstream.status}` }), {
      status: upstream.status,
      headers: { "Content-Type": "application/json" },
    });
  }

  // Forward quota/balance errors
  if (upstream.status === 429 || upstream.status === 402) {
    const errText = await upstream.text();
    return new Response(errText, {
      status: upstream.status,
      headers: { "Content-Type": "application/json" },
    });
  }

  if (!upstream.ok) {
    return new Response(
      JSON.stringify({ error: `Upstream error: ${upstream.status}` }),
      { status: 502, headers: { "Content-Type": "application/json" } }
    );
  }

  const content = await upstream.text();
  return new Response(JSON.stringify({ content }), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
});
```

### Frontend Client Code (Web / MiniProgram Universal)

**Recommended approach (when supabase client is available):**

```typescript
/**
 * Fetches web page content via Edge Function.
 * @param url - The full URL of the target web page
 * @param options - Optional output control parameters
 * @returns Web page Markdown text
 */
async function fetchWebPage(
  url: string,
  options?: {
    returnFormat?: "markdown" | "html" | "text" | "screenshot" | "pageshot";
    withImagesSummary?: boolean;
    withLinksSummary?: boolean;
    targetSelector?: string;
    removeSelector?: string;
    timeout?: number;
    noCache?: boolean;
  }
): Promise<string> {
  const { data, error } = await supabase.functions.invoke("web-reader", {
    body: { url, ...options },
  });
  if (error) throw error;
  if (!data?.content) throw new Error("Response content is empty");
  return data.content;
}
```

**Fallback approach (when supabase client is unavailable):**

```typescript
/**
 * Fetches web page content via Edge Function using native fetch.
 * @param url - The full URL of the target web page
 * @param options - Optional output control parameters
 * @returns Web page Markdown text
 */
async function fetchWebPage(
  url: string,
  options?: {
    returnFormat?: "markdown" | "html" | "text";
    withImagesSummary?: boolean;
    withLinksSummary?: boolean;
    targetSelector?: string;
    removeSelector?: string;
    timeout?: number;
    noCache?: boolean;
  }
): Promise<string> {
  const res = await fetch(`${import.meta.env.VITE_SUPABASE_URL}/functions/v1/web-reader`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url, ...options }),
  });

  if (res.status === 429) {
    const err = await res.json();
    throw new Error(`Quota exhausted: ${err.message ?? res.statusText}`);
  }
  if (res.status === 402) {
    const err = await res.json();
    throw new Error(`Insufficient balance: ${err.message ?? res.statusText}`);
  }
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);

  const json = await res.json();
  if (!json.content) throw new Error("Response content is empty");
  return json.content;
}
```

---

## Parameters

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | Yes | The full URL of the target web page, including scheme (e.g. `https://example.com`) |
| `returnFormat` | string | No | Return format: `markdown` (default) / `html` / `text` / `screenshot` / `pageshot` |
| `withImagesSummary` | boolean | No | Whether to append an image description summary to the content |
| `withLinksSummary` | boolean | No | Whether to append a links summary at the end of the content |
| `targetSelector` | string | No | CSS selector to extract content from specific page elements only |
| `removeSelector` | string | No | CSS selector to remove specific elements from the result |
| `timeout` | number | No | Timeout for waiting for the page to load (seconds) |
| `noCache` | boolean | No | Set to `true` to disable cache and force re-fetch |
| `accept` | string | No | `Accept` header value: `text/html` (default) or `text/event-stream` (enable SSE streaming mode) |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `content` | string | Structured Markdown text of the target web page, including title, body, and optional image summary and links list |

---

## Notes

- **API Key Security**: `INTEGRATIONS_API_KEY` may only be read on the Edge Function server side; it must never be exposed to the frontend.
- **Error Handling**: Always handle 401 (invalid token), 403 (GFW filter), 429 (quota exceeded), and 402 (insufficient balance).
- **Billing**: This plugin is free (`original_price: 0.00`, `enable_billing: false`), but call counts are still recorded.
- **GFW Filtering**: The `filter_gfw` field in the JWT Payload controls whether GFW-blocked domains are filtered; blocked URLs will return 403.
- **URL Encoding**: The target URL must be encoded with `encodeURIComponent` before being appended to the path to prevent special characters from causing routing errors.
- **Response Format**: Returns Markdown in `text/plain` format by default; the Edge Function wraps it as `{ content: string }` JSON for convenient frontend consumption.
- **Streaming Response**: To receive content as a stream, set `Accept: text/event-stream` in the request headers. See the "SSE Streaming" section below for the implementation.

---

## SSE Streaming

When the request header is set to `Accept: text/event-stream`, the upstream service returns content as an SSE (Server-Sent Events) stream, with each SSE event carrying a partial Markdown text chunk. Streaming mode is suitable for real-time rendering of large pages.

### SSE Event Format

```
data: <partial Markdown text>

data: <more Markdown text>

data: [DONE]

```

- Each `data:` line carries a content chunk.
- Receiving `data: [DONE]` indicates the stream has ended.

### Generation-Phase SSE Streaming Example

```typescript
const apiKey = process.env["INTEGRATIONS_API_KEY"]!;

/**
 * Fetches the target web page in SSE streaming mode, processing returned Markdown chunks in real time.
 * @param targetUrl - The full URL of the target web page
 * @param onChunk - Callback function invoked each time a content chunk is received
 * @returns The complete Markdown text
 */
async function fetchWebPageSSE(
  targetUrl: string,
  onChunk?: (chunk: string) => void
): Promise<string> {
  const encodedUrl = encodeURIComponent(targetUrl);
  const endpoint =
    `https://api-ELbWqODdAgNY@36oqjsxjo775h3odjp3eev3y740deicu.lambda-url.us-west-2.on.aws/${encodedUrl}`;

  const response = await fetch(endpoint, {
    method: "GET",
    headers: {
      "X-Gateway-Authorization": `Bearer ${apiKey}`,
      "Accept": "text/event-stream",
    },
  });

  if (response.status === 401) throw new Error("Authentication failed: JWT Token missing or invalid");
  if (response.status === 403) throw new Error("Target URL is blocked by GFW and cannot be accessed");
  if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
  if (!response.body) throw new Error("Response body is empty, cannot read stream");

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let fullContent = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop() ?? "";

    for (const line of lines) {
      if (!line.startsWith("data:")) continue;
      const payload = line.slice(5).trim();
      if (payload === "[DONE]") break;
      if (payload) {
        fullContent += payload;
        onChunk?.(payload);
      }
    }
  }

  return fullContent;
}

// Example: stream-fetch and print in real time
await fetchWebPageSSE("https://example.com", (chunk) => {
  Deno.stdout.write(new TextEncoder().encode(chunk));
});
```

### Frontend SSE Streaming Example (Web Platform)

The frontend must relay the streaming request through an Edge Function, which needs to proxy the upstream SSE stream to the client.

```typescript
/**
 * Fetches a web page via Edge Function SSE proxy, processing content chunks in real time.
 * @param url - The full URL of the target web page
 * @param onChunk - Callback function invoked each time a content chunk is received
 * @returns The complete Markdown text
 */
async function fetchWebPageStream(
  url: string,
  onChunk?: (chunk: string) => void
): Promise<string> {
  const res = await fetch(`${import.meta.env.VITE_SUPABASE_URL}/functions/v1/web-reader`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept": "text/event-stream",
    },
    body: JSON.stringify({ url }),
  });

  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  if (!res.body) throw new Error("Response body is empty");

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let fullContent = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop() ?? "";

    for (const line of lines) {
      if (!line.startsWith("data:")) continue;
      const payload = line.slice(5).trim();
      if (payload === "[DONE]") break;
      if (payload) {
        fullContent += payload;
        onChunk?.(payload);
      }
    }
  }

  return fullContent;
}
```
