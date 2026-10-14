---
name: nginx-pro
description: Nginx guidance — reverse proxy, load balancing, TLS, caching, rate limiting, and performance tuning.
category: development
---

## Overview

Nginx is the workhorse reverse proxy and web server of the internet: event-driven, memory-efficient, and configured through a declarative file format that rewards precision. It terminates TLS, load-balances to upstreams, caches aggressively, rate-limits, and serves static files — usually several of these at once in front of application servers.

Nginx configuration has sharp edges (location matching precedence, `if` inside location, proxy header subtleties) that produce subtle bugs. This skill covers the correct patterns for proxying, TLS, caching, and rate limiting, plus performance tuning and debugging.

## When to use

- Setting up nginx as a reverse proxy or load balancer.
- Configuring TLS (certificates, protocols, HSTS).
- Debugging routing issues (location matching, rewrites).
- Adding caching, compression, or rate limiting.
- Tuning nginx performance (workers, keepalive, buffers).
- Serving static files efficiently.
- Choosing between nginx, Traefik, Caddy, or HAProxy.

## Core concepts

- **Request processing phases.** Nginx processes requests through phases (rewrite, access, content); directives belong to specific contexts (`http`, `server`, `location`). Understanding contexts prevents half of all nginx bugs.
- **Location matching.** Prefix locations, `=` exact, `^~` preferential prefix, `~`/`~*` regex — evaluated in a specific precedence order. One regex in the wrong place hijacks routes silently. Test matching with real requests, not assumptions.
- **`if` is evil (in location).** The famous warning: `if` inside `location` has surprising behavior (only `return` and `rewrite ... last` are safe). Use `map` for conditional variables instead.
- **Reverse proxy basics.** `proxy_pass` with correct trailing-slash semantics (it matters enormously), `proxy_set_header` for Host/X-Forwarded-Proto/X-Real-IP, and `proxy_http_version 1.1` + `Connection ""` for keepalive to upstreams.
- **Upstream load balancing.** `upstream` blocks with round-robin (default), `least_conn`, `ip_hash`; health checks (passive via `max_fails`/`fail_timeout`, active with nginx Plus or openresty); keepalive connections to backends.
- **TLS.** `ssl_certificate`/`ssl_certificate_key`, modern protocols (`TLSv1.2 TLSv1.3`), strong ciphers, session tickets/resumption, OCSP stapling, HSTS. Test with SSL Labs; automate renewal (certbot or acme clients).
- **Caching.** `proxy_cache` with zones, cache keys, validity per status code, `stale-while-revalidate` patterns via `proxy_cache_use_stale`, and cache purging strategy. Cache static aggressively; cache HTML/API deliberately.
- **Rate limiting.** `limit_req_zone` (request rate, burst with nodelay) and `limit_conn_zone` (concurrent connections) — per IP or per key (API token). Rate limit login endpoints and expensive routes first.
- **Compression.** gzip (and brotli via module) for text assets; `gzip_static` serving precompressed files; minimum lengths to avoid compressing tiny responses.
- **Static files.** `root` vs `alias` (trailing slash semantics again), `try_files` for SPA fallbacks, `expires`/`Cache-Control` for immutable assets, `sendfile` + `tcp_nopush` for efficiency.
- **Rewrites and redirects.** `return 301` for simple redirects (fastest), `rewrite ... permanent` for pattern redirects; avoid rewrite loops; prefer `return` over `rewrite` when no regex is needed.
- **Logging.** Structured access logs (`log_format` with JSON), separate error log levels per context; log X-Request-ID for correlation with app logs.
- **Worker tuning.** `worker_processes auto`, `worker_connections`, `keepalive_timeout`, buffer sizes (`client_body_buffer_size`, `proxy_buffers`) — tune for your workload; defaults are conservative.
- **Security headers.** HSTS, X-Frame-Options, CSP, Referrer-Policy via `add_header` (remember: `add_header` in a location replaces server-level headers — a classic gotcha; use `more_set_headers` or repeat them).
- **WebSocket proxying.** `Upgrade`/`Connection` header mapping for WS upgrades; longer timeouts for idle WS connections.

## Practical workflow

1. **Structure configs.** `nginx.conf` (global) + `conf.d/` or `sites-enabled/` per site; test with `nginx -t` before every reload; version configs in git.
2. **Write the reverse proxy block.** Correct `proxy_pass` semantics, forwarded headers, keepalive to upstream:
   ```nginx
   upstream api { server 127.0.0.1:3000; server 127.0.0.1:3001; keepalive 32; }
   server {
     listen 443 ssl;
     server_name api.example.com;
     location / {
       proxy_pass http://api;
       proxy_http_version 1.1;
       proxy_set_header Connection "";
       proxy_set_header Host $host;
       proxy_set_header X-Forwarded-Proto $scheme;
       proxy_set_header X-Real-IP $remote_addr;
     }
   }
   ```
3. **Terminate TLS properly.** Full chain certificate, modern protocols/ciphers, OCSP stapling, HSTS (after verifying), automated renewal with deploy hooks that reload nginx.
   ```nginx
   ssl_protocols TLSv1.2 TLSv1.3;
   ssl_prefer_server_ciphers off;
   ssl_session_cache shared:SSL:10m;
   add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
   ```
4. **Add caching.** `proxy_cache_path` zone, cache key including relevant vary, validity rules, stale serving on upstream errors:
   ```nginx
   proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=1g inactive=60m;
   location /static/ {
     proxy_cache api_cache;
     proxy_cache_valid 200 1d;
     proxy_cache_use_stale error timeout updating;
     add_header X-Cache-Status $upstream_cache_status;
   }
   ```
5. **Rate-limit sensitive routes.** Zones per key, burst handling, separate stricter zones for auth endpoints:
   ```nginx
   limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
   location = /login { limit_req zone=login burst=3 nodelay; proxy_pass http://api; }
   ```
6. **Serve statics efficiently.** `try_files` for SPAs, immutable caching for hashed assets, `gzip_static` for precompressed files.
7. **Tune workers.** `worker_processes auto`, connections sized to traffic, keepalive timeouts aligned with clients, buffers for your payload sizes; benchmark before/after.
8. **Monitor and reload safely.** Stub status or the Prometheus exporter for metrics; `nginx -t && nginx -s reload` for zero-downtime config changes; watch error logs after every change.

## Common pitfalls

- **`proxy_pass` trailing slash** — `/api/` vs `/api` changing URI mapping silently; understand the difference.
- **`if` inside location** — unpredictable behavior; use `map` for conditionals.
- **`add_header` inheritance gotcha** — location-level `add_header` wiping server-level headers; repeat or use headers-more.
- **Missing forwarded headers** — apps generating wrong URLs/redirects; set Host and X-Forwarded-Proto.
- **No keepalive to upstreams** — new connection per request; `proxy_http_version 1.1` + keepalive.
- **Regex location hijacking** — a regex matching more than intended; order and test locations.
- **TLS misconfiguration** — old protocols, missing chain, no HSTS; test with SSL Labs.
- **Caching personalized content** — serving user A's page to user B; key caches carefully, bypass on cookies.
- **Unbounded client body** — huge uploads; set `client_max_body_size` deliberately.
- **No rate limiting** — brute-force and scrape abuse; limit auth and expensive endpoints.
- **Reload without testing** — `nginx -s reload` on broken config; always `nginx -t` first.
- **WebSocket timeouts** — default proxy timeouts killing idle WS; raise for WS locations with proper upgrade headers.
- **Root vs alias confusion** — wrong file paths served; know which directive appends the location.
