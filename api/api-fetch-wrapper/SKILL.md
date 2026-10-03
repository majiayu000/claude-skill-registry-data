---
name: api-fetch-wrapper
description: Wrap a public HTTP API (Open-Meteo weather as the demo) with credential handling, error normalisation, and a single retry on transient network failures. Demonstrates the production-shaped baseline for any "skill that calls an external service" — env-based secrets, structured error output, no leaked API keys in logs, and a deliberate retry policy. The Open-Meteo endpoint used here is keyless on purpose so the example runs without setup; replace `OPEN_METEO_URL` with your own host and add `process.env.MY_API_KEY` for an auth'd version.
version: "1.0"
license: MIT
metadata:
  category: integration
  tag:
    - example
    - http
    - external-api
    - typescript
---

# api-fetch-wrapper

The case that breaks first in production — a skill that hits an external service. This example covers the four things every such skill needs: secret handling, retry policy, error normalisation, and no-leak-on-failure logging.

## Contract

**Input** (stdin, JSON):

```json
{ "latitude": 52.52, "longitude": 13.41 }
```

**Output** (stdout, JSON):

```json
{
  "temperatureC": 18.4,
  "windSpeedKmh": 12.6,
  "fetchedAt": "2026-05-19T08:00:00.000Z"
}
```

**Errors** — written to stderr as `{"error": "...", "cause": "..."}` and exit code `1`. Error messages NEVER include the raw upstream response body (it might echo a secret); they include the upstream status code and a short canonical reason.

## Required environment

| Var | Purpose |
|---|---|
| `OPEN_METEO_URL` | Optional override of the upstream host. Defaults to `https://api.open-meteo.com`. |
| *(none for auth)* | Open-Meteo is keyless. For an auth'd API, the same skeleton reads `process.env.YOUR_API_KEY` and passes it via `Authorization` header. |

## Run locally

```bash
cd examples/api-fetch-wrapper
bun install
echo '{"latitude":52.52,"longitude":13.41}' | bun run src/index.ts
```

## Adapt this

- **Different API** — replace the URL, query params, and response shape. The retry / error-mapping skeleton stays.
- **API-key auth** — read `process.env.YOUR_API_KEY` once at the top, pass it via `Authorization: Bearer ${apiKey}`, and ensure the key never appears in error messages.
- **Stronger retry** — bump `MAX_ATTEMPTS`, add exponential backoff with jitter, or distinguish 5xx (retry) vs 4xx (do not retry) explicitly.
- **Cache** — wrap the fetch in a TTL cache when the upstream rate-limits.
