---
name: traefik
description: "Deploy Traefik edge router and reverse proxy; configure dynamic Docker/Kubernetes discovery, middleware chains, rate limiting, and automatic ACME TLS."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-09-13"
tags: ["traefik", "reverse-proxy", "ingress", "docker", "kubernetes", "letsencrypt", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Traefik Cloud-Native Edge Router & Reverse Proxy AI Skill Guide

## Overview & Engine Architecture

Traefik is a modern HTTP reverse proxy and ingress controller designed for microservices and containerized environments. Unlike traditional proxies that require static configuration files and manual service reloads, Traefik automatically discovers services in real-time by querying infrastructure providers (Docker daemon, Kubernetes API, Consul, Nomad). Its request pipeline is divided into **EntryPoints** (ports), **Routers** (rule-based matching), **Middlewares** (request/response transformations and security), and **Services** (load-balanced upstream targets), paired with automatic **ACME TLS** (Let's Encrypt) certificate management.

Claude operates as a Principal Ingress & Cloud Network Engineer, specializing in **Traefik v3 routing architectures**, **Kubernetes IngressRoute CRDs**, **Docker label discovery**, **middleware security chains (rate limiting, forward auth, security headers)**, and **automated wildcard TLS certificate provisioning**.

### Traefik Request Pipeline Topology

```
┌─────────────────────────────────────────────────────────────┐
│                 Traefik Request Lifecycle                   │
│                                                             │
│  Client Traffic (HTTPS :443 / HTTP :80)                     │
│  └── EntryPoints (web, websecure)                           │
│                                                             │
│  Routers (Rules & TLS Termination)                          │
│  ├── Rule: `Host('api.example.com') && PathPrefix('/v1')`   │
│  └── TLS Resolver: Automated ACME Let's Encrypt Challenge   │
│                                                             │
│  Middleware Pipeline (Chained Filters & Transformations)    │
│  ├── 1. RateLimiter (Protect against volumetric abuse)      │
│  ├── 2. SecurityHeaders (HSTS, CSP, X-Frame-Options)        │
│  └── 3. StripPrefix (Remove '/v1' prefix before upstream)   │
│                                                             │
│  Services & Upstream Load Balancers                         │
│  └── Weighted Round-Robin ──> Container Pods A, B, C        │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Strict File Permissions on ACME Storage**: Traefik will refuse to generate or load TLS certificates if `acme.json` has loose permissions. Always initialize `acme.json` with `chmod 600` before starting the container.
2. **Deterministic Middleware Ordering**: Always apply defensive middlewares in correct sequence: rate-limiting first, followed by authentication/authorization (ForwardAuth or BasicAuth), followed by path/header modifications (StripPrefix, AddPrefix).
3. **HTTP to HTTPS Global Redirection**: Enforce HTTPS redirection directly at the `web` EntryPoint level rather than duplicating redirect rules on every individual router.
4. **Resilient Upstream Health Checks**: Configure periodic HTTP health checks on services (`traefik.http.services.<name>.loadbalancer.healthcheck.path`) to automatically eject unhealthy container replicas.

---

## Production Docker Compose Automation: Edge Gateway with Automated TLS

Save this file as `docker-compose.yml` to launch an enterprise Traefik edge proxy with automated TLS and a protected backend service:

```yaml
version: "3.8"

services:
  traefik:
    image: traefik:v3.1
    container_name: traefik
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./traefik-data/acme.json:/acme.json
    command:
      - "--global.checknewversion=false"
      - "--global.sendanonymoususage=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.web.http.redirections.entrypoint.to=websecure"
      - "--entrypoints.web.http.redirections.entrypoint.scheme=https"
      - "--entrypoints.websecure.address=:443"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--certificatesresolvers.myresolver.acme.tlschallenge=true"
      - "--certificatesresolvers.myresolver.acme.email=admin@example.com"
      - "--certificatesresolvers.myresolver.acme.storage=/acme.json"
    labels:
      - "traefik.enable=true"
      # Secure headers middleware
      - "traefik.http.middlewares.sec-headers.headers.sslredirect=true"
      - "traefik.http.middlewares.sec-headers.headers.stsseconds=315360000"
      - "traefik.http.middlewares.sec-headers.headers.browserxssfilter=true"
      - "traefik.http.middlewares.sec-headers.headers.framedeny=true"

  app:
    image: nginxdemos/hello:plain-text
    container_name: demo-app
    restart: unless-stopped
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.app.rule=Host(`app.example.com`)"
      - "traefik.http.routers.app.entrypoints=websecure"
      - "traefik.http.routers.app.tls.certresolver=myresolver"
      - "traefik.http.routers.app.middlewares=traefik-sec-headers@docker"
      - "traefik.http.services.app.loadbalancer.server.port=80"
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **`permissions of acme.json are too open, expected 0600, got 0644`** | Host created `acme.json` with standard file creation umask permissions. | Run `touch acme.json && chmod 600 acme.json` on the host, then restart Traefik. |
| **`404 Not Found` when browsing to configured domain** | Incoming HTTP `Host` header does not match the Router `Rule` (e.g., mismatched subdomain or port), or container not exposed. | 1. Check Traefik logs for loaded routers.<br>2. Verify `Host('domain.com')` rule matches exactly.<br>3. Ensure `traefik.enable=true` label is present. |
| **`502 Bad Gateway` returned by Traefik** | Upstream container port is wrong or container is attached to an isolated Docker network. | 1. Explicitly set `traefik.http.services.<name>.loadbalancer.server.port=<internal_port>`.<br>2. Ensure Traefik and upstream containers share a common Docker network. |
| **ACME TLS challenge fails: timeout on verification** | Port 80/443 blocked by external firewall or ISP, or DNS A/AAAA records point to wrong IP. | 1. Verify external public DNS points to host IP.<br>2. Test port 80 accessibility from outside network (`curl -I http://domain.com`). |

---

## Command Line Syntax & Operational Recipes

```bash
# 1. Initialize ACME certificate store with mandatory security permissions
mkdir -p traefik-data && touch traefik-data/acme.json && chmod 600 traefik-data/acme.json

# 2. Inspect active Traefik container logs for dynamic routing updates
docker logs -f traefik

# 3. Test HTTP to HTTPS redirection using curl
curl -Iv http://app.example.com

# 4. Verify SSL certificate expiration and SAN names
openssl s_client -connect app.example.com:443 -servername app.example.com
```

---

## Agent Operational Directive

> **MANDATORY**: Always declare `providers.docker.exposedbydefault=false` in container environments so that newly launched developer or database containers are not inadvertently routed to the public internet.
