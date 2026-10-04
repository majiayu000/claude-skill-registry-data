---
name: DNS
description: Configure DNS records correctly with proper TTLs, email authentication, and migration strategies.
metadata: {"clawdbot":{"emoji":"🌍","os":["linux","darwin","win32"]}}
---

## Pre-Migration TTL

- Lower TTL to 300s at least 48h before changing records—current TTL must expire first
- Check current cached TTL before planning: `dig +nocmd +noall +answer example.com`
- After migration stable 24h, raise TTL back to 3600-86400s
- Test with multiple resolvers: Google (8.8.8.8), Cloudflare (1.1.1.1), local ISP—they cache independently

## Email Authentication (All Three Required)

- SPF alone insufficient—DKIM and DMARC both needed for deliverability
- DMARC record: `_dmarc.example.com TXT "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com"`
- SPF must be single TXT record—multiple SPF records invalid; use `include:` for multiple sources
- SPF ending: `-all` (reject) or `~all` (soft fail)—never `+all` or `?all`
- Verify complete setup with mail-tester.com after configuration

## CAA Records

- Limits which Certificate Authorities can issue certs for domain—prevents unauthorized issuance
- Basic: `example.com. CAA 0 issue "letsencrypt.org"`
- Wildcard requires separate entry: `CAA 0 issuewild "letsencrypt.org"`
- Incident reporting: `CAA 0 iodef "mailto:security@example.com"`
- Without CAA, any CA can issue—set explicitly for security-conscious domains

## www Handling

- Configure both apex and www—or redirect one to other; leaving www unconfigured breaks links
- Pick canonical form and stick to it: www → apex OR apex → www
- HTTPS redirect requires cert for both variants before redirect works
- Test both URLs explicitly after setup

## Debugging Commands

- `dig +trace example.com`—full resolution chain from root; reveals where problem occurs
- `dig @ns1.provider.com example.com`—query authoritative nameserver directly, bypasses cache
- Compare authoritative vs cached response—mismatch indicates propagation in progress
- Check all relevant record types—A working doesn't mean AAAA, MX, or TXT are correct

## Cloudflare Proxy Behavior

- Orange cloud (proxied) hides origin IP—breaks SSH, mail, game servers; use grey cloud for non-HTTP
- Proxied records ignore your TTL setting—Cloudflare controls caching
- CNAME flattening at apex works in Cloudflare but causes confusion when migrating away
- Universal SSL only on proxied records—DNS-only requires origin certificate

## Wildcard Records

- `*.example.com` does not match apex `example.com`—both need explicit records
- Explicit subdomain record takes precedence over wildcard
- Wildcard SSL certificates require separate issuance—use DNS challenge with Let's Encrypt
