---
name: domain-dns-ops
description: >-
  Operates domains and DNS: registrars, Cloudflare zones and records, nameserver delegation, vanity
  domains, redirects, and DNS/HTTP verification. Use when setting up or debugging DNS records,
  redirects, or propagation.
source: "https://github.com/steipete/agent-scripts"
attribution: "steipete/agent-scripts by Peter Steinberger"
version: "1.0.0"
license: MIT
---

# Domain/DNS Ops

> **Attribution:** Sourced from [steipete/agent-scripts](https://github.com/steipete/agent-scripts) by [Peter Steinberger](https://github.com/steipete).

## When to Use

- Setting up DNS zones and records on Cloudflare
- Configuring vanity domains, redirects, and nameserver delegation
- Verifying DNS propagation and HTTP redirect chains

## Golden Path (new vanity domain → Cloudflare → redirect)

1. **Decide routing model**
   - Page Rule redirect (small scale, per-zone).
   - Bulk Redirects (account-level).
   - Worker route (fallback).

2. **Cloudflare zone**
   - Create zone in Cloudflare dashboard, then confirm:
     ```bash
     curl -s "https://api.cloudflare.com/client/v4/zones?name=example.com" \
       -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" | jq '.result[0] | {id, name, status}'
     ```

3. **Nameservers**
   - Update nameservers at your registrar to Cloudflare's NS records.

4. **DNS placeholders (so CF can terminate HTTPS)**
   - Proxied apex `A` → `192.0.2.1` (placeholder)
   - Proxied wildcard `A` → `192.0.2.1`

5. **Redirect setup**
   - Page Rule: destination URL + `301` permanent redirect.
   - Or use Cloudflare Bulk Redirects for multiple domains.

6. **Verify**

```bash
# DNS check
dig +short example.com @1.1.1.1

# HTTPS redirect
curl -I https://example.com
# Expect: HTTP/2 301 or 302 with Location header
```

## Common Commands

```bash
# Check if domain resolves to Cloudflare
dig +short example.com @1.1.1.1

# Check HTTP/HTTPS redirect
curl -sIL https://example.com | grep -E "HTTP/|Location:"

# Check DNS propagation
dig +short example.com @8.8.8.8
dig +short example.com @1.1.1.1
```

## Guardrails

- Confirm registrar before debugging Cloudflare "invalid nameservers" (often "wrong registrar").
- Prefer reversible steps; verify after each change (NS → DNS → redirect).
- Do not print API tokens or secrets.
