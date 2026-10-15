---
name: Cloudflare
description: Manage Cloudflare zones, DNS records, and cache via API token.
requires:
  bins: []
  env:
    - CLOUDFLARE_API_TOKEN
---

# Cloudflare

Use this skill to read or modify Cloudflare zones and DNS records, or purge
cache. Backed by the `cloudflare` extension hitting `api.cloudflare.com/client/v4`.

## Use when

- "List my Cloudflare zones"
- "Add / update / delete an A record for `domain.tld`"
- "Purge Cloudflare cache for this site"
- "What name servers does this zone use?"

## Do not use when

- Non-Cloudflare DNS providers (Route53, Namecheap)
- Low-level DNS lookups / dig-style queries — use `dns-tools`
- Cloudflare Workers / Pages deploy — not exposed yet

## Tools

- `status` — token + write/purge gate state
- `list_zones` — optional `name` exact match, `per_page`
- `list_dns_records` — requires `zone_id`; filters `type`, `name`, `per_page`
- `create_dns_record` — `zone_id`, `type`, `name`, `content`; optional `ttl`, `proxied`
- `update_dns_record` — `zone_id`, `record_id`; any of `type`/`name`/`content`/`ttl`/`proxied`
- `delete_dns_record` — `zone_id`, `record_id`
- `purge_cache` — `zone_id` + `purge_everything` OR `files`/`hosts`/`tags`

## Write gates

Destructive ops require explicit env flags:

- `CLOUDFLARE_ALLOW_WRITES=true` — create/update/delete DNS records
- `CLOUDFLARE_ALLOW_PURGE=true` — purge cache

Without the gate, writes fail with `-32041`.

## Token scopes

Recommended token perms: `Zone:Read`, `DNS:Edit`, `Cache Purge:Purge`.
Scope the token to specific zones in the Cloudflare dashboard.
