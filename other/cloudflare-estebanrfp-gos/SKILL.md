---
name: cloudflare
description: Manage Cloudflare domains, DNS records, SSL settings, zone configuration, firewall rules, tunnels, cache, and analytics via the Cloudflare API. Use when the user asks to set up a domain, add/edit/delete DNS records, configure SSL, manage Cloudflare Tunnels, purge cache, view analytics, or any Cloudflare account management task.
---

# Cloudflare (GenosOS)

Manage Cloudflare zones, DNS, SSL, tunnels, cache, firewall, and analytics directly via `web_fetch` to the Cloudflare API. No CLI, no curl, no external dependencies.

## Setup

Store your Cloudflare API token in config:
```
config set env.CLOUDFLARE_API_TOKEN your-token-here
```

For tunnel operations, also set:
```
config set env.CLOUDFLARE_ACCOUNT_ID your-account-id
```

Create tokens at: https://dash.cloudflare.com/profile/api-tokens

## API Base

All requests use: `https://api.cloudflare.com/client/v4`

Headers: `{ "Authorization": "Bearer {token}", "Content-Type": "application/json" }`

**Important:** Read the token from config first: `config get env.CLOUDFLARE_API_TOKEN`

## Verify Token

```
web_fetch({
  url: "https://api.cloudflare.com/client/v4/user/tokens/verify",
  headers: { "Authorization": "Bearer {token}" }
})
```

## Zones

### List zones
```
web_fetch({
  url: "https://api.cloudflare.com/client/v4/zones",
  headers: { "Authorization": "Bearer {token}" }
})
```

### Filter by domain
```
web_fetch({
  url: "https://api.cloudflare.com/client/v4/zones?name=example.com",
  headers: { "Authorization": "Bearer {token}" }
})
```

### Get zone details
```
web_fetch({
  url: "https://api.cloudflare.com/client/v4/zones/{zone_id}",
  headers: { "Authorization": "Bearer {token}" }
})
```

## DNS Records

### List records
```
web_fetch({
  url: "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?per_page=100",
  headers: { "Authorization": "Bearer {token}" }
})
```

Filter by type/name: `?type=A&name=api.example.com`

### Create record
```
web_fetch({
  url: "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records",
  method: "POST",
  headers: { "Authorization": "Bearer {token}", "Content-Type": "application/json" },
  body: '{"type":"A","name":"api.example.com","content":"1.2.3.4","proxied":true,"ttl":1}'
})
```

### Update record
```
web_fetch({
  url: "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}",
  method: "PUT",
  headers: { "Authorization": "Bearer {token}", "Content-Type": "application/json" },
  body: '{"type":"A","name":"api.example.com","content":"5.6.7.8","proxied":true,"ttl":1}'
})
```

### Delete record
```
web_fetch({
  url: "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}",
  method: "DELETE",
  headers: { "Authorization": "Bearer {token}" }
})
```

### Export all records
```
web_fetch({
  url: "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?per_page=500",
  headers: { "Authorization": "Bearer {token}" }
})
```

## SSL

### Get current mode
```
web_fetch({
  url: "https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/ssl",
  headers: { "Authorization": "Bearer {token}" }
})
```

### Set SSL mode
```
web_fetch({
  url: "https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/ssl",
  method: "PATCH",
  headers: { "Authorization": "Bearer {token}", "Content-Type": "application/json" },
  body: '{"value":"strict"}'
})
```

Modes: `off`, `flexible`, `full`, `strict`

## Zone Settings

### List all settings
```
web_fetch({
  url: "https://api.cloudflare.com/client/v4/zones/{zone_id}/settings",
  headers: { "Authorization": "Bearer {token}" }
})
```

### Update a setting
```
web_fetch({
  url: "https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/{setting_id}",
  method: "PATCH",
  headers: { "Authorization": "Bearer {token}", "Content-Type": "application/json" },
  body: '{"value":"on"}'
})
```

## Cache

### Purge everything
```
web_fetch({
  url: "https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache",
  method: "POST",
  headers: { "Authorization": "Bearer {token}", "Content-Type": "application/json" },
  body: '{"purge_everything":true}'
})
```

### Purge specific URLs
```
web_fetch({
  url: "https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache",
  method: "POST",
  headers: { "Authorization": "Bearer {token}", "Content-Type": "application/json" },
  body: '{"files":["https://example.com/styles.css","https://example.com/app.js"]}'
})
```

## Firewall Rules

```
web_fetch({
  url: "https://api.cloudflare.com/client/v4/zones/{zone_id}/firewall/rules",
  headers: { "Authorization": "Bearer {token}" }
})
```

## Page Rules

```
web_fetch({
  url: "https://api.cloudflare.com/client/v4/zones/{zone_id}/pagerules",
  headers: { "Authorization": "Bearer {token}" }
})
```

## Tunnels

Requires `CLOUDFLARE_ACCOUNT_ID`. Read it: `config get env.CLOUDFLARE_ACCOUNT_ID`

### List tunnels
```
web_fetch({
  url: "https://api.cloudflare.com/client/v4/accounts/{account_id}/cfd_tunnel",
  headers: { "Authorization": "Bearer {token}" }
})
```

### Create tunnel
```
web_fetch({
  url: "https://api.cloudflare.com/client/v4/accounts/{account_id}/cfd_tunnel",
  method: "POST",
  headers: { "Authorization": "Bearer {token}", "Content-Type": "application/json" },
  body: '{"name":"my-tunnel","tunnel_secret":"<base64-random-32-bytes>","config_src":"cloudflare"}'
})
```

### Get tunnel details
```
web_fetch({
  url: "https://api.cloudflare.com/client/v4/accounts/{account_id}/cfd_tunnel/{tunnel_id}",
  headers: { "Authorization": "Bearer {token}" }
})
```

### Delete tunnel
```
web_fetch({
  url: "https://api.cloudflare.com/client/v4/accounts/{account_id}/cfd_tunnel/{tunnel_id}",
  method: "DELETE",
  headers: { "Authorization": "Bearer {token}" }
})
```

## Analytics

```
web_fetch({
  url: "https://api.cloudflare.com/client/v4/zones/{zone_id}/analytics/dashboard?since=-1440",
  headers: { "Authorization": "Bearer {token}" }
})
```

`since` in minutes: `-1440` = last 24h, `-60` = last hour

## Typical Workflows

### Point domain to server
1. List zones to get zone ID
2. Create A record: `type=A, name=example.com, content=1.2.3.4, proxied=true`
3. Create www CNAME: `type=CNAME, name=www, content=example.com, proxied=true`

### Set up email (MX + SPF)
1. Create MX record: `type=MX, name=example.com, content=mx.provider.com, proxied=false, priority=10`
2. Create TXT record: `type=TXT, name=example.com, content="v=spf1 include:provider.com ~all", proxied=false`

### Enable strict SSL
1. PATCH `/zones/{zone_id}/settings/ssl` with `{"value":"strict"}`

## Safety Rules

**Always confirm with the user before:**
- Deleting DNS records
- Changing SSL mode
- Modifying firewall rules
- Purging cache
- Deleting tunnels

**Safe to do freely:**
- Listing/reading zones, records, settings, analytics
- Verifying token

## Workflow

1. Read token: `config get env.CLOUDFLARE_API_TOKEN`
2. Build API URL with endpoint
3. Use `web_fetch` with Bearer auth
4. Save zone IDs in [MEMORY] for faster access

## Reference

For DNS record types, SSL modes, and API details: see `references/api-guide.md`
