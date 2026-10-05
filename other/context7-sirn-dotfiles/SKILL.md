---
name: context7
description: Retrieve documentation context for libraries using the Context7 API. Use when needing current library documentation (React, Python stdlib, Rust, etc.) BEFORE implementing or writing code.
---

Documentation context retrieval using the Context7 API.

## Prerequisites

Requires `CONTEXT7_API_KEY` environment variable to be set. API keys start with `ctx7sk`.

**Check before use:**

```bash
[ -z "$CONTEXT7_API_KEY" ] && echo "Error: CONTEXT7_API_KEY not set" || echo "OK: CONTEXT7_API_KEY is set"
```

**Note:** Never hardcode `CONTEXT7_API_KEY`. Always use the environment variable.

## Output Modes

| Flag | Value | Output format | Use case |
| --- | --- | --- | --- |
| `--output` | `json` _(default)_ | JSON (pretty) | Programmatic use, saving to file |
| `--output` | `compact` | JSON (no whitespace) | Piping to `jaq` |
| `--output` | `text` | Raw markdown from API | Quick review of documentation |

The `--output` flag accepts one of `json`, `compact`, or `text`.

## context

```bash
context7 [OPTIONS] LIBRARY_ID
context7 context [OPTIONS] LIBRARY_ID
```

Retrieve documentation context for a specific library.

| Flag | API param | Description |
| --- | --- | --- |
| `LIBRARY_ID` | `libraryId` | **Required.** Library identifier (e.g., `/facebook/react`) |
| `-q`, `--query` | `query` | **Required.** Natural language query about the topic |
| `-t`, `--tokens` | `tokensNum` | Token budget: integer or `"dynamic"` (default: dynamic) |
| `-v`, `--version` | _(in path)_ | Pin to exact version (e.g., `v15.1.8`) |
| `--timeout` | _(client)_ | Request timeout in seconds (default: 30) |
| `--output` | _(client)_ | Output format: `json`, `compact`, or `text` |

### Response (JSON modes)

```json
{
  "requestId": "...",
  "libraryId": "/facebook/react",
  "query": "useEffect hook",
  "response": "### Perform Side Effects in React Function Components...\n\nSource: https://..."
}
```

### Response (text mode)

Plain markdown with code examples and source references:

````markdown
### Perform Side Effects in React Function Components using useEffect Hook

Source: https://context7.com/facebook/react/llms.txt

The `useEffect` hook enables functional components to perform side effects...

```jsx
import { useState, useEffect } from "react";

function UserProfile({ userId }) {
  // ...
}
```
````

---

### React > Hooks > useEffect

Source: https://context7.com/facebook/react/llms.txt

The `useEffect` hook performs side effects in function components...

````

## Library ID Format

Library IDs follow the pattern `/owner/repo`:

| Example           | Description       |
| ----------------- | ----------------- |
| `/facebook/react` | React library     |
| `/vercel/next.js` | Next.js framework |
| `/expressjs/express` | Express.js    |
| `/python/cpython` | Python stdlib     |

## Examples

```bash
# Get documentation for React useEffect hook (default JSON output)
context7 /facebook/react -q "useEffect hook"

# Human-readable markdown output
context7 /facebook/react -q "useEffect hook" --output=text

# Pin to specific version
context7 /vercel/next.js -q "app router" -v "v15.1.8"

# Custom token budget
context7 /facebook/react -q "useState vs useReducer" --tokens 2000

# Compact JSON for piping to jaq
context7 /facebook/react -q "hooks" --output=compact | jaq '.response'

# Custom timeout for large libraries
context7 /rust-lang/rust -q "async trait" --timeout 60

# Save documentation to file
context7 /facebook/react -q "context API" --output=text > react-context.md
````

## Error Handling

| Status | Meaning | Action |
| --- | --- | --- |
| `200` | Success | Process normally |
| `202` | Accepted - Library not finalized | Wait and retry (handled automatically) |
| `301` | Moved - Library redirected | Follow redirect (handled automatically) |
| `400` | Bad Request | Check query parameters |
| `401` | Unauthorized - Invalid API key | Verify key (starts with `ctx7sk`) |
| `403` | Forbidden | Check library access permissions |
| `404` | Not Found | Verify the library ID |
| `422` | Unprocessable - Library too large/no code | Try different library |
| `429` | Too Many Requests | Wait for `Retry-After` header (handled automatically) |
| `500` | Internal Server Error | Retry with backoff |
| `503` | Service Unavailable | Retry later |

Exit codes: `0` = success, `1` = error, `2` = invalid arguments, `124` = timeout, `130` = interrupt.

## Rate Limits

- **Without API key**: Low rate limits, no custom configuration
- **With API key**: Higher limits based on plan
- View usage at https://context7.com/dashboard

The CLI automatically handles rate limits by respecting the `Retry-After` header and retrying up to 3 times.

## Best Practices

1. **Be specific with queries**: Use detailed natural language for better results.

   ```bash
   # Good
   context7 /facebook/react -q "How to implement authentication with middleware"

   # Less optimal
   context7 /facebook/react -q "auth"
   ```

2. **Use `--output=text` for quick review**: The API returns well-formatted markdown, perfect for reading directly.

3. **Cache responses**: Documentation updates infrequently, cache for hours or days.

4. **Use specific versions for reproducibility**: Pin to exact versions when you need consistent results across sessions.

   ```bash
   context7 /vercel/next.js -q "app router" -v "v15.1.8"
   ```

5. **Handle large libraries**: Some libraries (like `rust-lang/rust`) may take longer to process. Use `--timeout` to allow more time.

6. **Pipe through `jaq` for custom filtering**: Use `--output=compact` for efficient JSON processing.

   ```bash
   context7 /facebook/react -q "hooks" --output=compact | jaq '.response'
   ```

Always check that `CONTEXT7_API_KEY` is set before making requests.
