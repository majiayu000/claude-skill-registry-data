---
name: simple-cloudflare
description: Guide the user through a Cloudflare setup for a domain, including DNS, SSL, HSTS, caching, security headers, and email anti-spoofing (SPF, DKIM, DMARC). Use when the user asks to set up, audit, or troubleshoot Cloudflare settings. Not for general coding questions that only mention Cloudflare.
metadata:
  author: denniemok
  version: "1.0.0"
license: MIT
---

# Simple Cloudflare

Guide the user through setting up or auditing a domain on Cloudflare. You cannot change the dashboard, so the user makes each change. Give one step at a time with the exact path and value, wait for them to confirm, and verify with commands when you can. Never ask for passwords, API tokens, or secrets.

## 1. Gather facts

Read the repo first (README, deploy config, `.env.example`, headers files), then ask only what is missing:

- Domain and the hosts needed, such as the site, an API host, and other apps
- Where each host is served: Cloudflare Pages or Workers, or an origin like Vercel, Render, or DigitalOcean
- Whether it uses WebSockets, embeds, third-party scripts, or forms that need bot protection
- Whether the domain sends email, receives email, or neither, and which provider

Then walk through the sections below in order. Skip what does not apply.

## 2. DNS

- Add one record per host. Proxy (orange cloud) web hosts and API hosts.
- Use single-level hosts like `deal-api.example.com`. Free Universal SSL covers `example.com` and `*.example.com`, not nested names like `*.deal.example.com`.
- Never proxy mail records (MX, and the CNAMEs used for DKIM). Set them to DNS only.
- Pages custom domains are attached in the Pages project. Origin providers need the custom domain added on their side too.

## 3. SSL/TLS

SSL/TLS, Edge Certificates:

| Setting | Value |
|---------|-------|
| Encryption mode | Full (strict), which needs a valid certificate on the origin |
| Always Use HTTPS | On |
| Minimum TLS version | 1.2 |
| Automatic HTTPS Rewrites | On |

HSTS:

| Setting | Value |
|---------|-------|
| Enable HSTS | On |
| Max age | 1 month at first |
| Include subdomains | On, once every subdomain serves HTTPS |
| No-Sniff header | On |
| Preload | Off, it is hard to undo |

## 4. Security

- Security, Bot Fight Mode: On. If real users report problems, check Security, Events before loosening app limits.
- Read the client IP from `CF-Connecting-IP` on the origin, and do not parse `X-Forwarded-For` by hand.
- Optional: use Turnstile on public forms. Create a widget with the real hostnames. The site key goes in the frontend build, the secret key goes only on the server, never in Cloudflare or the repo.

## 5. Cache Rules

Caching, Cache Rules. Every matching rule runs, top to bottom, and a later rule overrides an earlier one. This is not first-match-wins.

| # | Match | Action |
|---|-------|--------|
| 1 | API hosts | Bypass cache |
| 2 | Site hosts and static paths (`/assets/`, `/images/`, and so on) | Eligible for cache, Edge TTL 1 month, Browser TTL respect origin |
| 3 | Site hosts and everything except those static paths | Bypass cache |

Rule 3 must use `not (...)` over the static paths, or it overrides Rule 2. Keep the HTML shell uncached so deploys show up at once. After a deploy, purge only the HTML if users see stale pages. Hashed asset filenames need no purge.

## 6. Security headers

Rules, Transform Rules, Modify Response Header. Scope every rule to a host and never use "All incoming requests" when apps differ.

| Header | Value |
|--------|-------|
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | `camera=(), microphone=(), geolocation=(), payment=(), usb=()` |
| `Content-Security-Policy` | Built from what the app loads, see below |
| `X-Frame-Options` | `DENY` on admin paths only. Use CSP `frame-ancestors` where embedding is needed |

HSTS and `X-Content-Type-Options` come from the SSL/TLS settings above, do not repeat them here. Apply these rules to site hosts, not API hosts.

CSP starter, adjust to the app:

```text
default-src 'self'; script-src 'self' https://challenges.cloudflare.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self' data:; connect-src 'self' https://<api-host> wss://<api-host>; frame-src https://challenges.cloudflare.com; object-src 'none'; base-uri 'self'; frame-ancestors 'none'
```

- `'self'` is only the site host, so allow the API host in `connect-src` explicitly, and `wss://` for WebSockets.
- Add each third party the app really uses (fonts, analytics, Turnstile). Do not add `unsafe-eval`.
- Trial changes first: set the header as `Content-Security-Policy-Report-Only`, exercise the whole app, read the console, then switch to enforced. To roll back in an emergency, switch back to report-only.

## 7. Origin verification (optional)

Stops people from hitting the origin directly. Rules, Transform Rules, Modify Request Header: Set static `X-Origin-Verify` to a random secret, and store the same value on the origin server. The origin only trusts `CF-Connecting-IP` when the header matches. It is a request header only. Never set it as a response header, that leaks the secret.

## 8. Email anti-spoofing

Add these in DNS as DNS only records. Anyone can send mail with your domain in the From address unless these exist. Work in this order.

SPF, TXT on the root (`@`):

```text
v=spf1 include:<provider-spf> -all
```

- Only one SPF record per name. Merge providers into one line, and stay under 10 DNS lookups.
- Use `~all` while testing, then `-all`.
- If Cloudflare Email Routing receives mail, include `_spf.mx.cloudflare.net`.

DKIM: the sending provider gives a CNAME or TXT at `<selector>._domainkey`. Add it exactly as given, DNS only, then enable signing in the provider.

DMARC, TXT at `_dmarc`:

```text
v=DMARC1; p=none; rua=mailto:<report-address>
```

Roll out in stages. Start with `p=none` and read the reports, move to `p=quarantine`, then `p=reject` once every legitimate sender passes. Use `pct=` to ramp up if needed. A free report reader such as Cloudflare DMARC Management or dmarcian makes the reports readable.

If the domain sends no email, lock it down now:

| Type | Name | Content |
|------|------|---------|
| TXT | `@` | `v=spf1 -all` |
| TXT | `_dmarc` | `v=DMARC1; p=reject; sp=reject; adkim=s; aspf=s` |
| TXT | `*._domainkey` | `v=DKIM1; p=` |
| MX | `@` | `0 .` (null MX, priority 0) |

For a domain that only receives through Email Routing, keep its MX and SPF, and set DMARC to `p=reject` since it sends nothing.

## 9. Verify

Run these and read the output with the user. On Windows PowerShell use `curl.exe` and `Select-String` in place of `curl` and `grep`.

```bash
curl -sI https://example.com | grep -iE "strict-transport|content-security|referrer|permissions|x-content|cf-cache"
# static file: run twice, the first may be MISS
curl -sI https://example.com/assets/app.js | grep -iE "cf-cache-status|^age|cache-control"
curl -sI https://example.com/assets/app.js | grep -iE "cf-cache-status|^age|cache-control"
curl -sI https://api.example.com/health | grep -i cf-cache-status
nslookup -type=TXT example.com
nslookup -type=TXT _dmarc.example.com
```

Expect:
- HSTS, nosniff, Referrer-Policy, Permissions-Policy, and CSP on site hosts
- `cf-cache-status: HIT` on the static file's second request (an `age` header confirms it), and `DYNAMIC` or `BYPASS` on the HTML and the API
- If the static file stays `DYNAMIC`, a bypass rule is overriding the cache rule, so check that Rule 3 excludes the static paths
- No `X-Origin-Verify` in any response
- One SPF record, a DMARC record, and DKIM passing on a real test email (check the message headers for `spf=pass dkim=pass dmarc=pass`)

## Checklist

- DNS records proxied, mail records DNS only
- SSL Full (strict), Always HTTPS, TLS 1.2, HSTS set
- Bot Fight Mode on
- Cache Rules 1 to 3 in order, Rule 3 excludes static paths
- Header rules host-scoped, CSP tested in report-only first
- Origin verification secret matches on the server, never in responses
- SPF, DKIM, and DMARC in place, and a lockdown set for domains that send no email
- Verification commands pass
