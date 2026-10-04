---
model_tier: medium
name: traefik
description: "Use when setting up Traefik as a local reverse proxy — real domains on 127.0.0.1, trusted HTTPS via mkcert, automatic service discovery, and multi-project routing."
domain: devops
workspaces:
  - engineering
packs:
  - engineering-base
---

# Traefik Skill

## When to use

Use this skill when:
- Setting up local development with real domain names and trusted HTTPS
- Configuring SSL certificates (self-signed, mkcert, ACME via Namecheap/AWS)
- Routing multiple Docker projects through a single reverse proxy
- Embedding external services (Grafana, etc.) that require HTTPS/same-origin

## Procedure: Set up Traefik

### 0. Understand current setup

Before changing any routing configuration:

1. **Check existing proxy setup** — is Traefik already running? Check `docker ps | grep traefik`.
2. **Review docker-compose** — read `docker-compose.yml` for existing labels and network config.
3. **Check DNS/hosts** — review `/etc/hosts` or dnsmasq for existing domain mappings.

### Architecture

Traefik acts as a **local reverse proxy** that:
1. Resolves real domains (e.g., `local.example.dev`, `app.test`) to `127.0.0.1`
2. Terminates HTTPS with trusted certificates
3. Auto-discovers Docker services via labels (no manual config per service)
4. Routes requests to the correct container based on hostname

```
Browser → https://app.example.com
    → DNS resolves to 127.0.0.1 (via /etc/hosts or dnsmasq)
    → Traefik (port 443) picks up the request
    → Routes to app container (based on Docker labels)
```

## DNS Resolution (domains → 127.0.0.1)

**Option A: `/etc/hosts` (simple, per-domain)**

```
127.0.0.1  local.example.dev
127.0.0.1  grafana.local.example.dev
```

**Option B: dnsmasq (wildcard, all subdomains — preferred)**

```bash
brew install dnsmasq
echo 'address=/.local.example.dev/127.0.0.1' >> /opt/homebrew/etc/dnsmasq.conf
sudo brew services restart dnsmasq
sudo mkdir -p /etc/resolver
echo 'nameserver 127.0.0.1' | sudo tee /etc/resolver/local.example.dev
```

## Certificate Strategies

Choose based on project needs:

| Strategy | Tool | Trust | Use when |
|---|---|---|---|
| **Self-signed** | openssl | Manual trust via keychain | Quick local dev, no external deps |
| **mkcert** | mkcert | Auto-trusted local CA | Local dev, easiest setup |
| **ACME (Namecheap)** | lego + DNS-01 | Real CA (Let's Encrypt) | Real domain, Namecheap DNS |
| **ACME (AWS Route53)** | lego + DNS-01 | Real CA (Let's Encrypt) | Real domain, AWS DNS |

### Self-signed (openssl)

```bash
mkdir -p traefik/certificates
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout traefik/certificates/_.${CERT_DOMAIN}.key \
  -out traefik/certificates/_.${CERT_DOMAIN}.crt \
  -subj "/CN=*.${CERT_DOMAIN}" \
  -addext "subjectAltName=DNS:*.${CERT_DOMAIN},DNS:${CERT_DOMAIN}"

# Trust on macOS
sudo security add-trusted-cert -d -r trustRoot \
  -k /Library/Keychains/System.keychain traefik/certificates/tls.crt
```

### mkcert (simplest for local dev)

```bash
brew install mkcert && mkcert -install
mkcert "local.example.dev" "*.local.example.dev"
```

### ACME via Lego container (real certs)

```yaml
# docker-compose.yml
lego:
  image: goacme/lego:latest
  profiles: [manual]   # Only run on demand
  volumes:
    - ./traefik/certificates:/etc/lego
```

```bash
# Namecheap DNS-01
docker compose run --rm \
  -e NAMECHEAP_API_USER -e NAMECHEAP_API_KEY \
  lego --dns namecheap \
  --domains "*.${CERT_DOMAIN}" --email "admin@${CERT_DOMAIN}" \
  --path /etc/lego run

# AWS Route53 DNS-01
docker compose run --rm \
  -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_REGION \
  lego --dns route53 \
  --domains "*.${CERT_DOMAIN}" --email "admin@${CERT_DOMAIN}" \
  --path /etc/lego run
```

### Taskfile integration for cert management

```yaml
# certificates/generate.yml (included in main Taskfile)
tasks:
  selfsigned:
    desc: Generate self-signed certificate for ${CERT_DOMAIN}
    cmds: [...]

  namecheap:
    desc: Generate ACME certificate via Namecheap DNS-01
    cmds: [...]

  aws:
    desc: Generate ACME certificate via AWS Route53 DNS-01
    cmds: [...]
```

```yaml
# Main Taskfile
trust:
  desc: Add cert to macOS keychain
  cmds:
    - sudo security add-trusted-cert -d -r trustRoot \
        -k /Library/Keychains/System.keychain traefik/certificates/tls.crt

untrust:
  desc: Remove cert from macOS keychain
  cmds:
    - sudo security delete-certificate -c "*.${CERT_DOMAIN}" \
        /Library/Keychains/System.keychain

cert:setup:
  desc: Generate and trust self-signed certificate
  deps: [generate:selfsigned, trust]
```

## Traefik Container

```yaml
traefik:
  image: traefik:v3.2   # or v2.11 for older setups
  command:
    - --providers.docker=true
    - --providers.docker.exposedbydefault=false
    - --providers.file.directory=/etc/traefik/dynamic
    - --providers.file.watch=true
    - --entrypoints.web.address=:80
    - --entrypoints.websecure.address=:443
  ports:
    - "${TRAEFIK_HTTP_PORT:-80}:80"
    - "${TRAEFIK_HTTPS_PORT:-443}:443"
  volumes:
    - /var/run/docker.sock:/var/run/docker.sock:ro
    - ./traefik/dynamic:/etc/traefik/dynamic:ro
    - ./traefik/certificates:/certs:ro
```

### TLS dynamic config

```yaml
# traefik/dynamic/tls.yml
tls:
  certificates:
    - certFile: /certs/tls.crt
      keyFile: /certs/tls.key
```

## Service Labels

### Basic pattern (HTTP → HTTPS redirect + TLS)

```yaml
my-service:
  labels:
    - "traefik.enable=true"
    # HTTP router (redirect to HTTPS)
    - "traefik.http.routers.myapp.rule=Host(`${CERT_HOST}`)"
    - "traefik.http.routers.myapp.entrypoints=web"
    - "traefik.http.routers.myapp.middlewares=myapp-https-redirect"
    - "traefik.http.middlewares.myapp-https-redirect.redirectscheme.scheme=https"
    - "traefik.http.middlewares.myapp-https-redirect.redirectscheme.port=${TRAEFIK_HTTPS_PORT}"
    # HTTPS router
    - "traefik.http.routers.myapp-secure.rule=Host(`${CERT_HOST}`)"
    - "traefik.http.routers.myapp-secure.entrypoints=websecure"
    - "traefik.http.routers.myapp-secure.tls=true"
    - "traefik.http.services.myapp.loadbalancer.server.port=80"
```

### Subdomain routing

```yaml
grafana:
  labels:
    - "traefik.enable=true"
    - "traefik.http.routers.grafana-secure.rule=Host(`grafana.${CERT_HOST}`)"
    - "traefik.http.routers.grafana-secure.entrypoints=websecure"
    - "traefik.http.routers.grafana-secure.tls=true"
    - "traefik.http.services.grafana.loadbalancer.server.port=3000"
```

### Path-based routing

```yaml
horizon:
  labels:
    - "traefik.http.routers.horizon-secure.rule=Host(`${CERT_HOST}`) && PathPrefix(`/horizon`)"
```

## Integration Patterns

### With NGINX

Traefik sits **in front of** NGINX — does NOT replace it:

```
Traefik (443) → NGINX (80 internal) → PHP-FPM
```

NGINX keeps: PHP-FPM routing, Xdebug header detection, static files.
Traefik adds: real domains, HTTPS, multi-service routing.

### Standalone

Traefik routes directly to the app container:

```
Traefik (443) → App container (80 internal)
```

### Multi-project (shared Traefik)

One Traefik instance routes to multiple projects via shared network:

```yaml
networks:
  traefik-public:
    external: true   # docker network create traefik-public
```

```
traefik
├── local.example.dev      → api-service
├── grafana.local.example.dev → grafana
├── other.local.example.dev → other-service
└── app.test               → frontend
```

## Middleware Examples

```yaml
# Rate limiting
- "traefik.http.middlewares.rate-limit.ratelimit.average=100"

# Basic auth
- "traefik.http.middlewares.auth.basicauth.users=admin:$$apr1$$..."

# CORS
- "traefik.http.middlewares.cors.headers.accesscontrolalloworiginlist=*"
```

## Related

- **Skill:** `docker` — Docker setup, compose services, container architecture
- **Skill:** `devcontainer` — DevContainer and Codespaces setup
- **Skill:** `grafana` — Grafana dashboards (benefits from HTTPS for embedding)
- **Skill:** `dashboard-design` — Grafana embedding requires same-origin/HTTPS
- **Rule:** `docker-commands.md` — all commands run inside Docker containers

### Validate

- Verify Traefik dashboard is accessible and shows all expected services.
- Confirm HTTPS works with trusted certificates (no browser warnings).
- Check that each service has correct Docker labels for routing.
- Test DNS resolution: `curl -I https://your-domain.localhost` should return 200.

## Output format

1. Traefik configuration with routing rules and TLS setup
2. Docker labels or dynamic config for service discovery

## Gotcha

- Traefik requires Docker labels on each service — a missing label means the service isn't routed.
- mkcert certificates must be trusted by the OS — `mkcert -install` is a one-time setup step.
- The model forgets to add the Traefik network to docker-compose services — no network = no routing.

## Do NOT

- Do NOT expose internal services without authentication.
- Do NOT use self-signed certificates when mkcert is available.

## Auto-trigger keywords

- Traefik
- reverse proxy
- local domains
- HTTPS
- mkcert
