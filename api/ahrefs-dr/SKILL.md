---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: ahrefs-dr
description: >
  Get a site Domain Rating (DR) from the Ahrefs free public APIv3 endpoint.
  Use when the user asks for DR, domain rating, Ahrefs rating, or site
  authority for a domain or URL. ALWAYS load this skill for those tasks.
---

# Ahrefs Domain Rating

Fetch **Domain Rating** with the free public endpoint. **Free** means
Ahrefs does not charge API units. It does **not** mean open access.
A missing Bearer token returns `403 Forbidden`. Always send a free
APIv3 key.

Always fetch the current docs first. Never pipe through `head`, `tail`,
`sed -n`, `awk`, `| less`, or any command that truncates:

```bash
curl -sL https://docs.ahrefs.com/en/api/reference/public/get-domain-rating-free
```

Docs: https://docs.ahrefs.com/en/api/reference/public/get-domain-rating-free

## Auth

API key lives in `~/.config/opencode/skills/ahrefs-dr/.env` as
`AHREFS_API_KEY`. Load it. Never print the key. Never commit `.env`.
If the value is empty, stop and ask the user to paste a key from
https://app.ahrefs.com/account/api-keys

```bash
set -a
source ~/.config/opencode/skills/ahrefs-dr/.env
set +a
test -n "$AHREFS_API_KEY"
```

Free account is enough. Generate the key in Account settings → API keys.
Send it as `Authorization: Bearer <token>`.

## Get DR

`target` is required. Pass a domain or a URL. Use `--data-urlencode` so
query chars stay valid.

```bash
curl -sS --fail-with-body -G 'https://api.ahrefs.com/v3/public/domain-rating-free' \
  --data-urlencode 'target=playwriter.dev' \
  -H 'Accept: application/json' \
  -H "Authorization: Bearer $AHREFS_API_KEY"
```

Response:

```json
{
  "domain_rating": {
    "domain_rating": 20.0,
    "license": "http://ahrefs.com/legal/domain-rating-license"
  }
}
```

Print the number as **DR**. Always add attribution: **Domain Rating by Ahrefs**
(https://ahrefs.com/). License: http://ahrefs.com/legal/domain-rating-license

## Rules

- Always use this free public endpoint. Do not call paid Site Explorer
  endpoints for DR.
- Pass the host only when the user gives a full URL unless they ask for
  that exact URL as `target`.
- On `401`, the key is missing or invalid. Stop. Do not retry with a
  guessed key.
- On `429`, wait and retry once. Do not loop.
