---
name: site-server-audit
description: Audit a public-facing site or server for common misconfigurations without sending exploit traffic. Covers DNS hygiene, TLS and HSTS, security headers, exposed paths (.git, .env, backups), cookie flags, and software fingerprinting. Invoke when onboarding a new client site, before launch, after infrastructure changes, or as periodic re-audit.
---

# Site / Server Audit

A read-only, non-intrusive checklist for assessing the security posture of a website you have authorization to audit. Every check is passive — it does not exploit, brute-force, or modify the target.

## When to invoke

- Onboarding a new client site, before deploy, after an infrastructure change
- Periodic re-audit (quarterly is a reasonable cadence for production)
- After any security advisory affecting the stack (Apache/nginx/PHP/WordPress/Node)
- When deciding whether to put a site behind Cloudflare or migrate hosting

## Required inputs

- A target hostname you are authorized to audit
- Optionally: doc-root path if you have shell access (for file-side checks)

If you do not have written authorization for the target, **stop**. This skill is for owners and authorized auditors.

## Audit — DNS

```bash
# Authoritative records and chain of trust
dig +short A example.com
dig +short AAAA example.com
dig +short MX example.com
dig +short TXT example.com
dig +short CAA example.com   # missing CAA means any CA can issue certs for you
dig +dnssec +short example.com | grep -i 'RRSIG\|ad'   # DNSSEC presence

# Mail-auth records (only meaningful if the domain sends mail)
dig +short TXT example.com | grep -i 'v=spf1'
dig +short TXT _dmarc.example.com
dig +short TXT default._domainkey.example.com   # adjust selector
```

Flags:
- Missing CAA → consider adding one pinning your CA(s)
- Missing DMARC or `p=none` on a domain that sends mail → spoofing risk
- DNSSEC absent → optional, but recommended for high-value domains

## Audit — TLS / HTTPS

```bash
# Cert chain, expiry, SANs
echo | openssl s_client -servername example.com -connect example.com:443 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates -ext subjectAltName

# Protocol + cipher (modern only)
nmap --script ssl-enum-ciphers -p 443 example.com   # if nmap is available

# HSTS + redirect chain
curl -sI https://example.com | grep -i 'strict-transport-security\|^location'
curl -sI http://example.com | grep -i '^location\|^HTTP/'   # should 301/308 to https
```

Flags:
- Cert expires in < 30 days
- TLS 1.0 / 1.1 still enabled
- HSTS missing or `max-age` < 6 months
- HTTP does not redirect to HTTPS

## Audit — security headers

```bash
curl -sI https://example.com | grep -iE \
  'content-security-policy|x-frame-options|x-content-type-options|referrer-policy|permissions-policy|cross-origin-(opener|embedder|resource)-policy'
```

Baseline expectation for a modern site:

| Header | Why |
|---|---|
| `Strict-Transport-Security: max-age=31536000; includeSubDomains` | Force HTTPS |
| `Content-Security-Policy` | Defense-in-depth against XSS |
| `X-Content-Type-Options: nosniff` | Block MIME confusion |
| `Referrer-Policy: strict-origin-when-cross-origin` | Don't leak full URLs |
| `Permissions-Policy: camera=(), microphone=(), geolocation=()` | Disable unused powerful features |

`X-Frame-Options` is largely superseded by CSP `frame-ancestors`, but still useful for legacy browsers.

## Audit — exposed paths

```bash
# Common high-signal misconfigurations. 404 is good, 200 is a finding.
for p in \
  /.git/config \
  /.git/HEAD \
  /.env \
  /.env.production \
  /.env.local \
  /wp-config.php.bak \
  /wp-config.php~ \
  /backup.zip \
  /dump.sql \
  /phpinfo.php \
  /.DS_Store \
  /server-status \
  /.well-known/security.txt \
  /robots.txt
do
  code=$(curl -s -o /dev/null -w '%{http_code}' "https://example.com$p")
  echo "$code $p"
done
```

Flags:
- Any `200` on a dotfile or backup path → immediate remediation
- `200` on `/server-status` or `/server-info` → restrict by IP
- `/.well-known/security.txt` missing → recommended (RFC 9116) for vuln disclosure

## Audit — cookies

```bash
curl -sI https://example.com | grep -i '^set-cookie'
```

Every cookie should have `Secure`, `HttpOnly` (unless explicitly needed in JS), and `SameSite=Lax` or stricter. Session cookies without these flags are a finding.

## Audit — software fingerprint

```bash
curl -sI https://example.com | grep -iE '^(server|x-powered-by|x-generator|x-aspnet-version)'
# WordPress generator tag
curl -s https://example.com | grep -oE '<meta name="generator" content="[^"]+"'
# Common JS-framework bundles + their versions in /_next, /static, etc.
```

Goal: identify outdated WP cores, PHP versions, Express, etc. Don't publish version banners — but as auditor you need them to map known CVEs.

## Audit — file-side (if you have shell access)

```bash
# Writable doc-root files (should be rare)
find /path/to/docroot -type f -perm -o+w 2>/dev/null

# World-readable .env / config
find /path/to/docroot \( -name '.env*' -o -name 'wp-config.php' -o -name 'config.php' \) -perm -o+r 2>/dev/null

# Files owned by the web user (often indicates writable-by-web — pivot risk)
find /path/to/docroot -user www-data -type f 2>/dev/null | head -50
```

## Producing the report

Group findings by severity. A useful template:

```
# Audit Report — example.com — 2026-MM-DD

## Critical (fix today)
- [.git/config exposed at /.git/config → returns 200]
  Remediation: block dot-directories at the webserver, remove repo from docroot.

## High (fix this week)
- [No HSTS header]
  Remediation: add Strict-Transport-Security on the edge.

## Medium (fix this sprint)
- ...

## Low / informational
- ...
```

Always include the exact command/URL used to produce each finding so the owner can re-verify after fixing.

## What this skill will not do

- Send any traffic that could plausibly be construed as exploitation (no auth probing, no fuzzing, no SQLi/XSS payloads).
- Audit a target you have not stated authorization for.
- Recommend disabling existing security controls.
