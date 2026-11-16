---
name: honeypot-tarpits
description: Lightweight detection techniques that work without a SIEM. Covers fake admin paths, decoy .env files, canary tokens, fake API keys planted in JS bundles, and tarpits that slow automated scanners. Invoke when public services see constant automated probing, when complementing fail2ban and WAF rules, or when high-signal detection is needed on a small budget.
---

# Honeypots and Tarpits

A honeypot is a resource that exists only to be hit by attackers. Anyone who interacts with it is, by definition, doing something they should not be. That makes honeypots one of the highest-signal detection mechanisms available — almost zero false positives, and trivial to operate at small scale.

This skill covers practical, low-effort patterns for solo operators and small teams. Not enterprise deception platforms (Thinkst Canary, etc., are excellent if you can afford them — but the same ideas work DIY).

## When to invoke

- Public services see constant automated probing (fail2ban catches most but you want better signal)
- You want detection without a full SIEM
- Complementing existing WAF rules
- After reconnaissance against a specific service (set traps for the next scan)
- You want early warning if a credential leaked (canary tokens)

## Honeypot pattern 1 — fake admin paths

Common scanner targets — `/wp-admin/`, `/administrator/`, `/manager/`, `/phpmyadmin/`, `/.git/config` — are reliable signals of automated probing. If you serve a real-looking 200 response and capture the source, you have an attacker IP/UA before they reach anything real.

```nginx
# nginx — fake admin endpoint
location ~ ^/(wp-admin|administrator|phpmyadmin|manager/html|.git/config|.env)$ {
    access_log /var/log/nginx/honeypot.log honeypot_fmt;
    add_header Content-Type text/plain;
    return 200 "OK";    # Looks fake, but the goal is the log entry, not realism
}

# Optional: in a separate http block, structured logging
log_format honeypot_fmt escape=json '{'
  '"time":"$time_iso8601",'
  '"ip":"$remote_addr",'
  '"path":"$request_uri",'
  '"method":"$request_method",'
  '"ua":"$http_user_agent",'
  '"referer":"$http_referer"'
'}';
```

Pipe `/var/log/nginx/honeypot.log` to your alerting (Loki + Grafana alert, Better Stack, a tiny daemon that pings a webhook). Every hit is an attacker.

Optional escalation: feed honeypot-hit IPs straight to fail2ban or Cloudflare WAF block.

```bash
# /etc/fail2ban/filter.d/honeypot.conf
[Definition]
failregex = ^.*"ip":"<HOST>".*$
ignoreregex =
```

```ini
# /etc/fail2ban/jail.local
[honeypot]
enabled  = true
filter   = honeypot
logpath  = /var/log/nginx/honeypot.log
maxretry = 1
bantime  = 24h
```

One hit = one day ban. Aggressive, but justified — nobody legitimately fetches `/.env`.

**False-positive risk**: search-engine bots occasionally hit weird paths from leaked logs. Whitelist verified Googlebot / Bingbot via reverse-DNS before banning.

## Honeypot pattern 2 — decoy `.env` and config files

Same idea, slightly more elaborate. A fake `.env` with realistic-shaped fake values lets you detect not just that someone scanned, but also if they tried to *use* what they found.

```bash
# /var/www/decoy/.env — serve at path /
# IMPORTANT: when you build your own decoy, generate the canary values
# from canarytokens.org so each token fires its own alert. Do NOT copy
# the placeholders below verbatim — they exist here purely for shape.

DB_HOST=127.0.0.1
DB_PORT=5432
DB_USER=app_user
DB_PASS=<canary-placeholder-replace-with-real-canary>
AWS_ACCESS_KEY_ID=<aws-canary-placeholder>
AWS_SECRET_ACCESS_KEY=<aws-canary-secret-placeholder>
STRIPE_SECRET_KEY=<stripe-canary-placeholder>
```

Two layers of detection:

1. **Anyone fetching the decoy** → log hit (same as the fake-admin pattern)
2. **Anyone using the credentials** → secondary alert. Set them up so any use triggers a webhook:
   - AWS canary keys: free via [canarytokens.org](https://canarytokens.org) — fires when used
   - Database canary: a real `app_user` user in your dev/staging DB with read-only access to a single decoy table; alert on any login attempt
   - Stripe canary: not really feasible at the Stripe layer; can detect via `/login`-shaped probes against your real Stripe endpoint patterns

## Honeypot pattern 3 — canary tokens

A canary token is a credential that exists only to fire an alert when used. canarytokens.org generates them for free; alternatives include Thinkst's commercial Canary platform.

Token types worth deploying:

- **AWS access keys** — embedded in code samples, "leaked" docs, decoy `.env`
- **GitHub tokens** — embedded in test repos, README examples
- **DNS-based** — a hostname that, when queried, fires an alert (great for spotting recon)
- **Web canary** — a URL that, when fetched, fires an alert
- **PDF/DOCX with embedded canary** — when opened, the document beacons home

Place them where attackers will find them but legitimate users won't:

- Decoy admin paths (above)
- A "legacy backups" S3 bucket name in a leaked-shaped paste
- A `developer.txt` file in `/static/` with "internal credentials, do not commit"
- Mailbox folders named "API_keys" or "Production_creds" in a shared inbox

The placement matters more than the token. If no attacker ever finds your canary, it doesn't fire.

## Honeypot pattern 4 — fake API keys in JS bundles

Frontend bundles get scraped automatically by tools looking for secrets that shouldn't be there. Plant fake keys with distinctive prefixes that you can grep on the wider web later.

```js
// In your build, intentionally embed:
window.__INTERNAL_API_KEY__ = "intk_CANARY_a4e0e74e6d8c4f9aab3e1c7d8e2f5a1b";
```

Then periodically search GitHub / pastebins / Discord for the string. If it shows up anywhere, you know your bundle was scraped and someone tried to use the value.

This is also useful as a tripwire on attacker-side automation that publishes "leaks" — your fake key in a paste means you caught a scanner.

## Tarpit pattern — slow down scanners

Tarpits respond to scanners with deliberate latency, holding their connections open and reducing the volume they can probe per minute. Useful where blocking outright would be too aggressive.

```nginx
# Slow response for known-bad UAs / paths
location ~ ^/(wp-admin|phpmyadmin|.env)$ {
    if ($http_user_agent ~* "(masscan|nikto|sqlmap|nmap|burpsuite|fuzz)") {
        # Slow down — keep the connection alive but unhelpful
        echo_sleep 10;       # requires nginx with echo module, or use a Lua snippet
        return 200 "";
    }
    return 200 "OK";
}
```

A simpler "sleep 5 seconds then 200" on known-bad paths costs you almost nothing per hit and significantly reduces scanner throughput. For HTTPS-heavy scanners, the TLS handshake plus the 5-second body delay measurably reduces their rate.

Don't tarpit paths where legitimate users might land — only attacker-only resources.

## Active-defense gotchas

A few patterns that sound clever but cause problems:

- **Returning fake "successful exploit" responses** to make scanners believe they got RCE. Tempting but legally murky — some jurisdictions consider this entrapment. Stick to logging.
- **Returning malware** to attackers. Don't. It is unambiguously illegal in most places and ethically out of bounds.
- **Hacking back** at IPs that hit honeypots. Don't. Same.
- **Blocking based on `User-Agent` alone**. UA is trivially forgeable; combine with behavior signals.
- **Mass-banning Tor exit nodes**. Tor users include legitimate journalists, dissidents, and the security-conscious. Block specific abuse patterns, not the network.

## Detection-only design pattern

Most teams should stay in **detection-only** mode for honeypots. Log, alert, optionally block — but don't try to deceive or counter-attack. The signal-to-noise on "anyone hit my honeypot" is so good that you barely need anything else.

```
Honeypot hit
   ↓
Structured log → centralized log store
   ↓
Alert (low-priority) — for tracking only
   ↓
If repeated from same source within window → escalate
   ↓
Optional: feed to WAF / fail2ban for block
```

The escalation rules separate one-off scanners from focused attackers.

## Operating honeypots — what to watch for

Per honeypot, a small dashboard:

- Hit count per day / per week (baseline)
- Spikes (recon wave)
- Repeat offenders by IP / ASN (focused attacker)
- Path popularity (which lure works)
- Geographic distribution

If a honeypot stops getting hits for a long time, attackers may have learned to skip it. Rotate paths / lures occasionally.

For canary tokens specifically: track which token is at which placement, so when one fires you immediately know which surface leaked.

## Quick deployment checklist

A first honeypot setup, in order of effort:

1. [ ] Add the fake admin-paths block to nginx, with structured logging
2. [ ] Pipe `honeypot.log` to your existing log destination
3. [ ] Set up a single alert: "any line in honeypot.log" → ping a webhook (Telegram, Slack, email)
4. [ ] Generate a free AWS canary token at canarytokens.org and put it in a decoy `.env` at a scanner-friendly path
5. [ ] Add a fail2ban jail with `maxretry=1` for the honeypot (verify Googlebot etc. won't trigger first)
6. [ ] Plant a distinctive fake key string in your JS bundle — search for it monthly
7. [ ] Once stable, add a tarpit for the noisiest paths

Total time: 30–60 minutes. Detection ROI: very high.

## What this skill will not do

- Recommend hacking back, retaliation, or any offensive action against scanners
- Endorse blocking entire ASNs / countries without specific cause
- Replace a real SOC for high-stakes environments
