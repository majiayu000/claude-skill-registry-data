---
name: DNS Tools
description: Resolve DNS records (A, AAAA, MX, TXT, CNAME, NS, SOA, SRV, CAA), PTR reverse, and WHOIS.
requires:
  bins: []
  env: []
---

# DNS Tools

Low-level DNS lookups and WHOIS. Backed by the `dns-tools` extension using
`hickory-resolver` (pure Rust, no `dig` binary).

## Use when

- "What's the A/MX/TXT/NS record for `domain.tld`?"
- "Reverse lookup `1.2.3.4`"
- "Who owns this domain?" (WHOIS)
- Verifying DNS propagation after a Cloudflare change

## Do not use when

- Modifying records — use `cloudflare` (or the relevant provider skill)
- Deep port scans or HTTP probing — use `endpoint-check` / `fetch-url`

## Tools

- `status` — resolver info
- `resolve` — `name` + optional `type` (A default). Supports A/AAAA/CNAME/MX/TXT/NS/SOA/SRV/CAA
- `reverse` — `ip` → PTR names
- `whois` — `domain`; queries `whois.iana.org` then follows referral to the TLD server

## Notes

- Resolver reads `/etc/resolv.conf`; falls back to Cloudflare 1.1.1.1 if missing
- WHOIS body is truncated at 8 KB
