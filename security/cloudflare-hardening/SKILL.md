---
name: cloudflare-hardening
description: Harden a site behind Cloudflare end-to-end, from account to zone to origin. Covers DNS hygiene, origin-IP protection via Authenticated Origin Pulls and IP allowlisting, WAF managed rules, Bot Fight Mode, rate limiting, Transform Rules for security headers, Zero Trust Access for admin paths, and R2 / Pages security. Invoke when onboarding a domain, when the origin IP may be exposed, or after an attack.
---

# Cloudflare Hardening

Cloudflare gives you a powerful edge layer for free, but its defaults are conservative — most of the protection is opt-in. This skill walks the security-relevant settings and the ones that catch people out.

Applies to Cloudflare's main product (DNS + Proxy + WAF + Workers/Pages/R2). Not Magic Transit / Spectrum specifics.

## When to invoke

- Domain just onboarded to Cloudflare
- Site behind CF was scraped, brute-forced, or DDoSed
- Origin IP may be exposed (showed up in `dnshistory`, accidentally A-recorded)
- Periodic review of an existing public site
- Setting up Cloudflare Pages or R2 with a custom domain

## Step 1 — Lock the account itself

Before site settings, harden the account.

- **2FA on the account** with WebAuthn / hardware key, not SMS
- **API tokens, not Global API Key** — Global API Key has account-wide power and cannot be scoped
- **Audit Logs** — `Account → Audit Log` shows who did what; review monthly
- **Members** — separate humans from automation; each automation gets its own scoped token

API tokens: scope to **specific zones + specific permissions**. A common mistake is creating a "DNS edit" token at account level when only one zone needs it.

## Step 2 — DNS and proxy posture

```
Zone → DNS → Records
```

- **All public hostnames proxied (orange cloud)** unless you have a specific reason for grey-cloud (e.g. mail records — MX must be grey)
- **Origin IP must not be in any public DNS record** — common leaks:
  - Direct A record for `direct.example.com` or `origin.example.com` left over
  - MX pointing to a host on the same IP as the web origin (move mail to a separate IP/host)
  - SPF/TXT records containing IP literals that match the origin
- **DNSSEC** — enable in `DNS → Settings`. Requires DS record at the registrar.
- **CAA records** — restrict who can issue certs for your domain. Cloudflare adds these automatically if you turn it on.

If your origin IP is known-leaked, **rotate it** — provider panel usually lets you re-assign. Pair with origin allowlist (next step).

## Step 3 — Origin allowlist (defense-in-depth)

Cloudflare proxy is useless if attackers can hit the origin IP directly. Two complementary controls:

**1. Authenticated Origin Pulls** — origin only accepts TLS connections that present Cloudflare's client cert.

```
Zone → SSL/TLS → Origin Server → Authenticated Origin Pulls
```

Then on your origin nginx:

```nginx
ssl_client_certificate /etc/ssl/cloudflare/authenticated_origin_pull_ca.pem;
ssl_verify_client on;
```

**2. Firewall the origin to Cloudflare's IPs only** — at the VPS, restrict 80/443 to CF's published ranges:

```bash
# Fetch and ufw-allow only Cloudflare IPs (refresh on a cron)
sudo ufw delete allow 80/tcp
sudo ufw delete allow 443/tcp
for ip in $(curl -s https://www.cloudflare.com/ips-v4); do
  sudo ufw allow from "$ip" to any port 80,443 proto tcp comment 'cloudflare'
done
for ip in $(curl -s https://www.cloudflare.com/ips-v6); do
  sudo ufw allow from "$ip" to any port 80,443 proto tcp comment 'cloudflare-v6'
done
sudo ufw reload
```

Either alone is acceptable; both is best. Without one of them, the proxy provides little hardening because attackers will bypass it.

## Step 4 — TLS

```
Zone → SSL/TLS
```

- **Encryption mode**: **Full (strict)** — anything less either allows MITM (Full, not strict) or runs plaintext between CF and origin (Flexible). Flexible is a footgun; do not use.
- **Minimum TLS Version**: 1.2 minimum, 1.3 if your audience tolerates it
- **Always Use HTTPS**: on
- **Automatic HTTPS Rewrites**: on
- **HSTS** — apply via `Edge Certificates → HSTS`. `max-age=31536000`, `includeSubDomains`, preload only if you understand the lock-in.

## Step 5 — WAF and Bot management

```
Zone → Security → WAF
```

- **Managed Rules → Cloudflare Managed Ruleset**: on, default action `Managed Challenge`
- **OWASP Core Ruleset**: on, but watch for false positives — start in Log mode, then escalate
- **Custom Rules** for your stack:

```
# Block direct access to wp-admin from outside your country (adjust)
(http.request.uri.path contains "/wp-admin" or http.request.uri.path contains "/wp-login.php")
  and ip.geoip.country ne "AT"
→ Action: Managed Challenge

# Block known abusive paths
http.request.uri.path in {"/.git/config" "/.env" "/wp-config.php.bak" "/server-status"}
→ Action: Block

# Tighten login endpoints
http.request.uri.path eq "/wp-login.php" and http.request.method eq "POST"
→ Action: Managed Challenge

# Hide xmlrpc unless you actually use it
http.request.uri.path eq "/xmlrpc.php"
→ Action: Block
```

- **Bot Fight Mode** (free tier): on. Catches dumb scrapers. False positives are rare.
- **Super Bot Fight Mode** (paid): better, distinguishes verified bots from definitely-automated traffic.
- **Rate Limiting Rules** — free tier gives one rule; use it well:

```
http.request.uri.path eq "/wp-login.php" → 5 requests / 1 minute per IP → Block 10m
```

## Step 6 — Security headers via Transform Rules

You can inject headers without touching the origin. `Rules → Transform Rules → Modify Response Header`:

```
Set: Strict-Transport-Security  =  max-age=31536000; includeSubDomains
Set: X-Content-Type-Options     =  nosniff
Set: Referrer-Policy            =  strict-origin-when-cross-origin
Set: Permissions-Policy         =  camera=(), microphone=(), geolocation=(), interest-cohort=()
Set: Content-Security-Policy    =  <see below — app-specific>
```

CSP is too app-specific to template here. Start in **`Content-Security-Policy-Report-Only`** with a permissive baseline, watch the reports for a week, tighten, then promote to enforcing.

## Step 7 — Zero Trust Access for admin paths

`/wp-admin`, `/admin`, `/staging`, `/api/internal/*` should not be reachable from the open internet for most projects. Cloudflare Zero Trust (free for ≤ 50 users) gives you SSO-gated access:

```
Cloudflare Zero Trust → Access → Applications → Add → Self-hosted
```

- Application domain: `*.example.com/wp-admin*`
- Identity provider: Google/GitHub/email-OTP
- Policy: `Allow → emails in @yourcompany.com` or specific list

Now `/wp-admin` requires SSO before traffic reaches the origin at all. Brute-force on the WP login endpoint stops being your problem.

## Step 8 — Cache and Page Rules

(New zones: Page Rules are being phased out in favor of `Cache Rules`, `Configuration Rules`, `Origin Rules`, and `Single Redirects`.)

- **Cache static assets aggressively**, but never cache responses with `Set-Cookie` or auth headers
- **Bypass cache for** `/wp-admin/*`, `/wp-login.php`, `/cart/*`, `/checkout/*`, `/api/*` — auth and per-user content
- **Always Use HTTPS** as a Configuration Rule, not a workaround
- **Single Redirect** is the modern replacement for the "forward url" Page Rule

## Step 9 — Cloudflare Pages security

If you use Pages:

- **Branch deploy previews** are public by default — gate them with Access if they contain anything non-public
- **Environment variables** marked as Secret are not exposed to client bundles, but `NEXT_PUBLIC_*` and similar prefixes still go to the browser. Audit which env vars exist and where they end up.
- **`_headers` file** in the output directory applies headers per path — convenient for static-site CSP
- **Custom domain CNAME** must be a CF-orange-clouded record on a CF-managed zone

## Step 10 — R2 buckets

- **Public buckets** — only for content actually meant to be public. Check `Bucket → Settings → Public access`.
- **Custom domain on R2** — use it for public assets; never bind sensitive buckets to public custom domains
- **CORS** — restrict origins, do not use `*` unless you understand it
- **Object listing** — disable public listing; serve specific objects, not directory enumeration

## Step 11 — Audit and monitoring

```
Zone → Security → Events
Zone → Analytics → Security
```

- Review weekly for the first month, then monthly
- Look for: unusual ASNs, sustained 4xx/5xx from one source, spikes in Managed Challenge issuances
- For paid tiers: alerts on rule actions, expensive queries to Workers

## Step 12 — Periodic re-audit

Once a quarter, walk through:

- [ ] All DNS records still in use; remove orphans
- [ ] No DNS record exposes origin IP
- [ ] Authenticated Origin Pulls + origin firewall still in place
- [ ] WAF rules still match current app paths
- [ ] CSP still matches frontend (after deploys it can drift)
- [ ] No new public R2 buckets without intent
- [ ] No new long-lived API tokens with broad scope; rotate ones older than 90 days
- [ ] Zero Trust app list matches current team

## What this skill will not do

- Recommend Flexible SSL or any setting that allows plaintext between CF and origin
- Help bypass Cloudflare protection on a site you do not own
- Endorse leaving origin IP discoverable when the site is intentionally proxied
