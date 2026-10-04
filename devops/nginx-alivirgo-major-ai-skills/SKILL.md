---
name: nginx
description: "Configure Nginx web serving, reverse proxies, TLS termination, rate limits, and upstream load balancing; diagnose request failures."
category: cross-platform
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["nginx", "reverse-proxy", "ssl-tls", "load-balancing", "web-server", "http2", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Nginx High-Performance Reverse Proxy AI Skill Guide (Claude)

## Overview & Engine Architecture
Nginx is the world's most widely deployed high-performance HTTP server, reverse proxy, mail proxy, and generic TCP/UDP proxy. Claude operates as a Principal Infrastructure Architect and Site Reliability Engineer (SRE), specializing in **asynchronous event-driven architecture (`epoll`/`kqueue`)**, **hardened SSL/TLS termination (TLS 1.3, OCSP Stapling, HSTS)**, **dynamic upstream load balancing (`least_conn`, `ip_hash`)**, and **zero-downtime hot reloading (`nginx -s reload`)**.

### Nginx Master-Worker Process Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Nginx Process & Event Model                 │
│                                                             │
│  Master Process (Root privileges, parses config, binds ports)│
│  └── Spawns & Supervises Worker Processes                   │
│                                                             │
│  Worker Processes (Unprivileged `nginx`/`www-data` user)    │
│  ├── Event Loop (`epoll` Linux / `kqueue` BSD/macOS)        │
│  ├── Non-blocking Asynchronous Socket Multiplexing          │
│  ├── Microsecond Static Asset Disk Cache Engine             │
│  └── Upstream Connection Pool (Keepalive HTTP/1.1 to App)   │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Hardened Configuration Generation**: Author clean, production-grade `nginx.conf` files incorporating modern security headers (HSTS, Content-Security-Policy, X-Content-Type-Options, X-Frame-Options), rate limiting zones, and Gzip compression.
2. **Reverse Proxying & WebSocket Upgrades**: Configure `proxy_pass` blocks with proper header forwarding (`X-Forwarded-For`, `X-Forwarded-Proto`, `Host`) and bidirectional WebSocket upgrade blocks (`Upgrade`, `Connection "upgrade"`).
3. **Gateway Error Remediation (502 / 504 / 413)**: Rapidly identify root causes behind upstream connection drops, SELinux socket blocks, proxy read timeouts, and body payload truncation.
4. **SSL/TLS & Automated Certbot Integration**: Configure ACES/Let's Encrypt automated certificate renewals, intermediate certificate bundle assembly, and modern Mozilla intermediate cipher suites.

---

## Production Configuration Recipe: Hardened SSL Reverse Proxy & WebSockets

Save this configuration as `/etc/nginx/sites-available/api_gateway.conf`:

```nginx
# Rate Limiting Zone: 10MB memory zone, max 20 requests/sec per IP
limit_req_zone $binary_remote_addr zone=api_rate_limit:10m rate=20r/s;

# Upstream Backend Cluster with Keepalive
upstream backend_api_cluster {
    least_conn;
    server 127.0.0.1:8001 max_fails=3 fail_timeout=10s;
    server 127.0.0.1:8002 max_fails=3 fail_timeout=10s;
    keepalive 32;
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name api.enterprise.io;
    return 301 https://$host$request_uri;
}

# Production HTTPS Server Block
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name api.enterprise.io;

    # SSL Certificates (Full Chain + Private Key)
    ssl_certificate /etc/letsencrypt/live/api.enterprise.io/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.enterprise.io/privkey.pem;

    # Modern TLS Security & Ciphers
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:10m;
    ssl_session_tickets off;

    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 1.1.1.1 8.8.8.8 valid=300s;
    resolver_timeout 5s;

    # Security Headers
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;

    # Payload & Buffer Limits
    client_max_body_size 50M;
    client_body_buffer_size 128k;

    # Gzip Compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

    # API & WebSocket Reverse Proxy
    location / {
        limit_req zone=api_rate_limit burst=10 nodelay;

        proxy_pass http://backend_api_cluster;
        proxy_http_version 1.1;

        # WebSocket & Connection Upgrade Headers
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Standard Client Forwarding Headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Upstream Timeouts (e.g. For long-running AI / streaming requests)
        proxy_connect_timeout 60s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;
    }
}
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **`502 Bad Gateway` Error** | Upstream application process is stopped, listening on the wrong port, or blocked by Linux SELinux. | 1. Check upstream service status: `systemctl status myapp` or `curl 127.0.0.1:8001`.<br>2. On RHEL/CentOS, allow network connections via SELinux: `setsebool -P httpd_can_network_connect 1`.<br>3. Inspect `/var/log/nginx/error.log` for `Connection refused`. |
| **`504 Gateway Timeout` Error** | Upstream backend processing time exceeded `proxy_read_timeout` (default 60s). | 1. Increase timeouts in location block: `proxy_read_timeout 300s; proxy_connect_timeout 300s;`.<br>2. Enable SSE/Streaming buffering bypass: `proxy_buffering off;`. |
| **`413 Request Entity Too Large`** | File upload size exceeds default `client_max_body_size 1M`. | 1. In `http` or `server` context, add: `client_max_body_size 100M;`.<br>2. Test and reload: `nginx -t && nginx -s reload`. |
| **SSL Handshake Fails / Untrusted Cert Warning** | Incomplete certificate chain (`cert.pem` used instead of `fullchain.pem`). | 1. Point `ssl_certificate` to `fullchain.pem` (contains leaf + intermediate CA).<br>2. Test chain with `openssl s_client -connect api.enterprise.io:443 -servername api.enterprise.io`. |

---

## Command Line Syntax & Server Management

```bash
# 1. Test Configuration Syntax (Crucial before any reload)
nginx -t

# 2. Zero-Downtime Hot Reload
nginx -s reload

# 3. Inspect Live Error and Access Logs
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log

# 4. Generate Free Let's Encrypt SSL Certificate via Certbot
certbot --nginx -d api.enterprise.io
```

### Essential File & Directory Paths
- **Master Configuration**: `/etc/nginx/nginx.conf`
- **Site Configurations**: `/etc/nginx/sites-available/` and `/etc/nginx/sites-enabled/` (Debian/Ubuntu) or `/etc/nginx/conf.d/*.conf` (RHEL/Alpine)
- **Log Files**: `/var/log/nginx/access.log` and `/var/log/nginx/error.log`
- **Windows Nginx Path**: `C:\nginx\` (Execute `nginx.exe -s reload`)

---

## Agent Operational Directive
> **MANDATORY**: Always run `nginx -t` to validate syntax before executing `nginx -s reload` or restarting the system daemon. Never commit plain HTTP listeners without automatic 301 redirection to HTTPS in production environments.
