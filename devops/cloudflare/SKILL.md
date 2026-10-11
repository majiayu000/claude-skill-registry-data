---
name: cloudflare
description: Cloudflare — DNS, Workers, Pages, Tunnels, WAF, R2, KV.
---

# Cloudflare

## Credentials Protocol — Collect Before Acting

**Before any Cloudflare task**, instruct the user to provide the required credentials securely.

| Task | Required credentials |
|------|----------------------|
| DNS changes | API Token with `Zone:DNS:Edit` scope |
| Workers deploy | API Token with `Account:Workers Scripts:Edit` scope |
| Pages deploy | API Token with `Account:Cloudflare Pages:Edit` scope |
| Tunnel setup | API Token with `Account:Cloudflare Tunnel:Edit` scope |
| Zero Trust / Access | API Token with `Account:Access:Edit` scope |
| WAF / Rate Limiting | API Token with `Zone:Firewall Services:Edit` scope |
| R2 operations | API Token with `Account:Workers R2 Storage:Edit` scope |
| KV operations | API Token with `Account:Workers KV Storage:Edit` scope |

Always request **scoped API Tokens** — never the Global API Key. Set TTL and IP restrictions where practical.

| Who calls the API | Where the token lives |
|---|---|
| **An agent, in this session** | The `cloudflare` integration: the user runs `devteam integration connect cloudflare` in their own terminal, and the agent calls through `devteam integration call`. Load `skills/integrations/cloudflare-api/SKILL.md` — never ask for the token in chat or have it exported |
| CI, Wrangler, application code | A CI/platform secret exposed as `$CLOUDFLARE_API_TOKEN` (+ `$CLOUDFLARE_ACCOUNT_ID`, `$CLOUDFLARE_ZONE_ID`) |

---

## Service Detection

| Signal | Service |
|--------|---------|
| `wrangler.toml` | Workers (and/or Pages) |
| `pages.dev` subdomain or Pages project | Pages |
| `cloudflared` binary or tunnel config | Tunnels |
| `.sentryclirc` mentions Cloudflare | Integrated Workers |
| Zone / DNS config in CI | DNS management |

---

## Account & Zone IDs

```bash
curl -s -X GET "https://api.cloudflare.com/client/v4/zones" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" | jq '.result[] | {name, id}'
```

---

## Key Config Patterns

**Workers**: define `name`, `main`, `compatibility_date` in `wrangler.toml`. Secrets via `wrangler secret put` — never in `wrangler.toml`.

**Pages**: `wrangler pages deploy dist/ --project-name=my-project`. CI via `cloudflare/pages-action@v1`.

**DNS**: `"proxied": true` activates CDN/WAF; `"proxied": false` is pure DNS.

**KV**: globally replicated, eventually consistent. Use for config and feature flags — not for strongly consistent data.

**R2**: S3-compatible, no egress fees. S3 SDK compatible via `https://<ACCOUNT_ID>.r2.cloudflarestorage.com`.

Load `references/workers.md` for: full `wrangler.toml` templates, deploy commands, KV/R2/Durable Objects/Service bindings, Zero Trust Access setup.

Load `references/dns-and-pages.md` for: DNS CRUD API examples, Pages deploy and CI/CD, custom domains, Tunnels setup, WAF rules, rate limiting, cache rules.

---

## Debugging Checklist

| Symptom | Where to look |
|---------|--------------|
| DNS not resolving | Dashboard → DNS → confirm record exists and TTL propagated |
| SSL error | Dashboard → SSL/TLS → check mode (Full vs Full Strict) |
| Worker not updating | `wrangler tail` for live logs; check deployment status |
| Tunnel unreachable | `cloudflared tunnel info <name>`; check service health |
| Unexpected 403/block | Dashboard → Security → Events (WAF log) |
| Cache not working | Check `CF-Cache-Status` response header; review Cache Rules |
| Rate limit false positives | Switch to `simulate` mode; review Security → Events |

---

## Before Declaring Done

- [ ] Scoped API Token used (not Global API Key); token stored in secret manager
- [ ] `.env` excluded from git; `CLOUDFLARE_API_TOKEN` referenced as env var in CI and code; agent-run API calls went through `devteam integration call`
- [ ] Workers secrets set via `wrangler secret put` — not in `wrangler.toml`
- [ ] DNS records confirmed with correct `proxied` setting
- [ ] WAF/rate limiting rules tested in `simulate` mode before enforcing
