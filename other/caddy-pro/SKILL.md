---
name: caddy-pro
description: Caddy guidance — automatic HTTPS, Caddyfile patterns, reverse proxying, and simple production deployments.
category: development
---

## Overview

Caddy is the web server with automatic HTTPS: point it at a domain and it obtains, installs, and renews TLS certificates on its own. Its Caddyfile format is the most readable in the category, and its defaults are secure. For single servers, small clusters, and teams tired of certificate management, Caddy removes an entire category of operational work.

Simplicity is the feature — Caddy won't replace nginx's module ecosystem or Traefik's dynamic discovery for complex setups, but for "serve this app over HTTPS correctly," it's unmatched. This skill covers Caddyfile patterns, reverse proxying, TLS behavior, and production deployment.

## When to use

- Serving a site or API over HTTPS with zero certificate hassle.
- Reverse-proxying to app servers simply and correctly.
- Choosing between Caddy, nginx, and Traefik.
- Writing Caddyfiles (matchers, handlers, snippets).
- Running Caddy in production (systemd, Docker, clustering).
- Using Caddy as a static file server.
- Extending Caddy with plugins (crowdsec, custom modules).

## Core concepts

- **Automatic HTTPS.** Caddy obtains certs via ACME (Let's Encrypt/ZeroSSL) on first request, renews automatically, and redirects HTTP→HTTPS by default. The criteria: a public DNS name Caddy can serve challenges for. This eliminates the most common TLS operational work.
- **The Caddyfile.** Site blocks with directives — declarative, minimal, readable. `reverse_proxy`, `file_server`, `php_fastcgi`, `respond` cover most needs. Snippets (`(name) { }` + `import`) DRY up repeated config.
- **Matchers.** Named matchers (`@api { path /api/* }`) select requests for handlers; `handle` blocks route exclusively (first match wins), `route` blocks run in order. Understanding `handle` vs `route` prevents routing surprises.
- **Reverse proxy.** `reverse_proxy localhost:3000` with automatic header passing (X-Forwarded-For/Proto set correctly), health checks (active/passive), and load balancing across upstreams. The defaults are right for most apps.
- **TLS details.** `tls` directive for DNS challenge (wildcards), custom certs, or internal CA; on-demand TLS for many dynamic domains (with rate-limit care); storage of certs (persist `/data`!).
- **ACME challenges.** HTTP/TLS-ALPN automatic; DNS challenge via provider plugins for wildcards or firewalled servers. Staging CA for testing; watch rate limits with many domains.
- **Static files.** `file_server` with `root`, `try_files` for SPAs, `encode gzip zstd` for compression, `header` for cache control. Precompressed file serving included.
- **Logging.** Structured JSON logs by default; `log` directive per site; tune for your log pipeline. Access logs with latency fields make performance debugging easy.
- **Security headers.** `header` directive for HSTS/CSP/X-Frame-Options — set deliberately; Caddy's defaults are safe but headers are your app's policy.
- **Plugins (xcaddy).** DNS providers, crowdsec, layer4, and more via custom builds. Plugins are compiled in — plan the build; don't hand-roll crypto-adjacent plugins.
- **API and config.** Caddy's admin API allows dynamic config changes (JSON); the Caddyfile adapts to JSON. Useful for automation; secure the admin endpoint (it's localhost-only by default).
- **Clustering.** Multiple Caddy instances sharing cert storage (via storage plugins: Redis, S3, Consul) for HA — certs issued once, shared everywhere.
- **Systemd/Docker.** Official systemd unit and Docker image; run as non-root where possible; persist `/data` (certs) and `/config`.

## Practical workflow

1. **Write the Caddyfile.** Site blocks per domain; reverse_proxy to apps; file_server for statics. Start minimal — Caddy's defaults handle TLS, HTTP→HTTPS, and headers.
   ```
   api.example.com {
     reverse_proxy 127.0.0.1:3000 127.0.0.1:3001 {
       lb_policy least_conn
       health_uri /health
     }
   }
   static.example.com {
     root * /srv/www
     file_server
     encode gzip zstd
     header Cache-Control "public, max-age=31536000, immutable"
   }
   ```
2. **Use snippets for shared config.** Security headers, logging, and common proxy settings defined once:
   ```
   (secure) {
     header {
       Strict-Transport-Security "max-age=31536000; includeSubDomains"
       X-Content-Type-Options "nosniff"
       X-Frame-Options "DENY"
     }
   }
   api.example.com {
     import secure
     reverse_proxy 127.0.0.1:3000
   }
   ```
3. **Validate and format.** `caddy fmt --overwrite` for canonical formatting; `caddy validate` before reloads; `caddy reload` for zero-downtime changes.
4. **Handle TLS edge cases.** DNS challenge for wildcards (`tls { dns cloudflare ... }` with plugin build); on-demand TLS with an `ask` endpoint for SaaS-style dynamic domains; persist `/data` always.
5. **Add matchers and routing.** `@api path /api/*` + `handle @api` blocks for path-based routing; `handle_path` stripping prefixes; test routing with curl before declaring victory.
6. **Configure logging.** JSON access logs with relevant fields; per-site logs; ship to your log pipeline; watch for upstream error patterns.
7. **Run in production.** Systemd unit (or Docker) with restart policies; non-root user; `/data` and `/config` persisted and backed up; admin API bound to localhost.
8. **Scale if needed.** Single Caddy handles surprising traffic; for HA, cluster with shared cert storage; monitor cert expiry and upstream health.

## Common pitfalls

- **Not persisting `/data`** — certificates reissued on every restart, hitting rate limits; persist and back up.
- **Testing ACME on production** — rate-limit lockout; use staging CA during setup.
- **On-demand TLS without `ask`** — anyone triggering cert issuance for arbitrary domains; gate with an ask endpoint.
- **`handle` vs `route` confusion** — routing behaving unexpectedly; `handle` is mutually exclusive, `route` is ordered.
- **HTTP challenge blocked** — firewall/proxy preventing port 80; use DNS challenge instead.
- **Forgetting `encode`** — uncompressed responses; enable gzip/zstd for text assets.
- **Plugin builds unmanaged** — hand-built binaries drifting; version and automate xcaddy builds.
- **Admin API exposed** — config API reachable remotely; keep it localhost-bound.
- **No health checks** — traffic to dead upstreams; configure active/passive checks.
- **Overriding defaults badly** — disabling automatic HTTPS or HTTP→HTTPS redirect without reason; the defaults are secure.
- **Single instance as SPOF** — no HA plan; cluster with shared storage when uptime demands it.
- **Ignoring logs** — structured logs available but unshipped; wire into your pipeline from day one.
- **Wildcard without DNS plugin** — HTTP challenge can't do wildcards; build with the DNS provider plugin.
