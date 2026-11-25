---
name: distil
description: Fetch web pages as clean Markdown and search the web via the distil.net proxy
version: 1.0.5
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins:
        - "node"
        - "npm"
        - "curl"
      env:
        - "DISTIL_API_KEY"
    primaryEnv: "DISTIL_API_KEY"
    install:
      - kind: node
        package: "distil-proxy"
        bins: [distil]
---

# Distil Skill

Gives agents discoverable, consistent access to the Distil proxy — no manual URL construction, no remembering headers or API keys.

Distil converts web pages into clean Markdown, saving 60–80% of tokens for LLM consumption.

## Setup

1. Get your API key from https://distil.net (sign up or use your existing key)
2. Install the `distil` CLI:

   ```bash
   npm install -g distil-proxy
   ```
3. Set the `DISTIL_API_KEY` environment variable

## Commands

```bash
# Fetch any URL as clean Markdown
distil fetch https://example.com

# Search the web and get results as Markdown
distil search "best practices for Go error handling"

# Multi-word queries work naturally — no quoting needed
distil search top 10 AI companies 2025

# Take a screenshot of a web page and return it as an image
distil screenshot https://example.com

# Render a web page (such as a single page javascript app) before trying to extract markdown
distil render https://example.com

# Fetch a URL and return its raw content bypassing any attempt to render markdown
distil raw https://example.com

# Fetch a URL and return its content without using the cache
distil nocache https://example.com
```

## Options

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `DISTIL_API_KEY`   | (none, required) | API key |
| `DISTIL_PROXY_URL` | `https://proxy.distil.net` | Proxy base URL (override for self-hosted) |

## Output

- `distil fetch` — returns page content as Markdown on stdout
- `distil search` — returns search results with titles, URLs, descriptions, and page content as Markdown on stdout
- Errors are written to stderr; non-zero exit code on failure

## Examples

```bash
# Research a topic
distil search "OpenClaw agent framework"

# Read documentation
distil fetch https://docs.github.com/en/rest

# Force fresh fetch (bypass cache)
DISTIL_PROXY_URL=https://proxy.distil.net distil nocache https://news.ycombinator.com
```

## Fallback — Direct curl

If you prefer to call the proxy directly:

```bash
# Fetch a page
curl -s "https://proxy.distil.net/https://example.com" \
  -H "X-Distil-Key: YOUR_API_KEY"

# Search the web
curl -s "https://proxy.distil.net/search?q=your+query" \
  -H "X-Distil-Key: YOUR_API_KEY" \
  -H "Accept: text/markdown"
```
