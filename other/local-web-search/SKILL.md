---
name: local-web-search
description: Use when the user asks for web search that should run via the local-160 Responses API with web_search tool (base URL like https://proxy.example.com, model gpt-5.2-codex(xhigh)). Includes script to query the local endpoint and return summary + citations; use for periodic news monitoring and on-demand searches.
---

# Local Web Search (local-160)

Use the local Responses API with `web_search` to get web results and citations.

## Quick start

1. Ensure env vars are set **or** Keychain entries are configured (see `references/CONFIG.md`).
2. Run the script:

```bash
/usr/bin/python3 {baseDir}/scripts/local_web_search.py --query "<your query>" --mode live
```

Optional (explicit .env path):

```bash
/usr/bin/python3 {baseDir}/scripts/local_web_search.py \
  --env-file ~/.openclaw/workspace/.env \
  --query "<your query>" \
  --mode cached
```

Timeout default is 1200s. Override via `--timeout` or `LOCAL_160_TIMEOUT`.
Note: web_search responses can be slow; 5–10 minutes is common and up to ~20 minutes is possible. Don’t treat it as failure unless it exceeds your timeout.

## Output handling

- Default output: one-sentence summary + up to 5 citations.
- Use `--json` when you need full tool output for parsing.
- Use `--mode live|cached|disabled` to control external web access.

## When to use

- For web lookups when local-160 supports `web_search`.
- For scheduled news monitoring that should use local-160 search.

## Troubleshooting

- 401/403: key missing/invalid.
- 5xx: local gateway down or base URL wrong.
