---
name: dns
description: "Set up DNS records, SSL/TLS certificates, subdomains, SPF/DKIM/DMARC email authentication, and health-check failover routing for Route53, Cloudflare, or GCP Cloud DNS — with optional Terraform output"
version: "2.0.0"
category: deploy
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Do NOT pause for confirmation.
Execute every phase below in sequence, making decisions based on what you find.

============================================================
PHASE 0 — INPUT
============================================================

$ARGUMENTS may contain:
- A domain: `example.com` or `app.example.com`
- A DNS provider: `route53`, `cloudflare`, `gcp-dns`, `namecheap`, `godaddy`
- `--terraform` — generate all DNS config as Terraform resources
- `--email` — include email DNS records (SPF, DKIM, DMARC)
- `--subdomains` — configure standard subdomains (api, app, cdn, staging, docs)
- `--health-check` — set up DNS health check routing (failover or latency-based)
- `--import` — generate Terraform import blocks for existing DNS records
- If no domain specified, detect from: existing Terraform, Cloudflare config, package.json homepage, environment variables

============================================================
PHASE 1 — CURRENT STATE ANALYSIS
============================================================

Scan the project for existing DNS configuration:

**Terraform DNS resources**:
- `aws_route53_zone`, `aws_route53_record`
- `cloudflare_zone`, `cloudflare_record`
- `google_dns_managed_zone`, `google_dns_record_set`

**Application config**:
- Domain references in: `vercel.json`, `netlify.toml`, `wrangler.toml`
- `DOMAIN`, `BASE_URL`, `APP_URL` in environment variables
- `next.config.js` — `assetPrefix`, `images.domains`
- `CNAME` file (GitHub Pages)

**Infrastructure references**:
- CloudFront distribution domain names
- Load balancer DNS names (ALB, NLB)
- S3 website endpoints
- Cloud Run service URLs
- Kubernetes ingress hosts

**SSL/TLS certificates**:
- ACM certificates in Terraform (`aws_acm_certificate`)
- Let's Encrypt references (`certbot`, Caddy auto-TLS)
- Cloudflare SSL settings
- Self-signed certificates (flag for replacement)

Compile a list of:
- Current domain and all subdomains in use
- Where each domain/subdomain points (target/origin)
- Current SSL/TLS status per domain

============================================================
PHASE 2 — DNS RECORD GENERATION
============================================================

Generate DNS records for all required domains. Organize by record type:

**Root domain** (`example.com`):
```
A     example.com    ->  {load balancer IP or CDN}
AAAA  example.com    ->  {IPv6 address if available}
```
- For AWS: use ALIAS record to CloudFront or ALB
- For Cloudflare: use proxied A/CNAME record (orange cloud)
- For bare domain with CNAME target: use ALIAS/ANAME (provider-specific)

**Standard subdomains** (if `--subdomains`):

| Subdomain | Record | Target | Purpose |
|-----------|--------|--------|---------|
| `www` | CNAME | `example.com` | www redirect |
| `api` | CNAME | ALB/Cloud Run/API Gateway | API endpoint |
| `app` | CNAME | CDN/Vercel/Netlify | Frontend app |
| `cdn` | CNAME | CloudFront/Cloudflare | Static assets |
| `staging` | CNAME | Staging environment | Pre-production |
| `docs` | CNAME | GitHub Pages/Gitbook | Documentation |
| `status` | CNAME | Status page provider | Uptime monitoring |
| `mail` | MX/CNAME | Email provider | Mail routing |

**Terraform format** (if `--terraform`):

Generate Route53, Cloudflare, or GCP Cloud DNS resources based on detected provider. Include:
- Zone resource with proper tagging (`Project`, `Environment`, `ManagedBy`)
- A/ALIAS record for root domain pointing to CDN or load balancer
- CNAME records for each subdomain
- Variable references for all environment-specific values (no hardcoded IPs)

**Cloudflare specifics**:
- Set `proxied = true` for A/CNAME records behind Cloudflare proxy
- Set `ttl = 1` (auto) for proxied records

**GCP Cloud DNS specifics**:
- Enable DNSSEC with `state = "on"`
- Append trailing dot to `dns_name`

============================================================
PHASE 3 — SSL/TLS CERTIFICATE SETUP
============================================================

Configure SSL certificates for all domains:

**AWS ACM**:
- Wildcard certificate covering `*.{domain}` and root domain
- DNS validation with Route53 records (auto-validated via Terraform)
- CloudFront certificates MUST be in `us-east-1` — use a separate provider alias
- `create_before_destroy = true` lifecycle for zero-downtime renewal

**Cloudflare**:
- SSL mode: Full (strict) — origin must have valid certificate
- Enable Universal SSL (automatic, covers root + www)
- For origin certificates: generate Cloudflare Origin CA cert (15-year validity)

**Let's Encrypt** (self-hosted):
- Generate Certbot command for certificate acquisition
- Set up auto-renewal cron: `0 0 1 * * certbot renew --quiet`
- Or use Caddy/Traefik for automatic TLS

============================================================
PHASE 4 — EMAIL DNS (if --email)
============================================================

Configure email authentication records to prevent spoofing:

**SPF** (Sender Policy Framework):
```
TXT  example.com  "v=spf1 include:_spf.google.com include:amazonses.com ~all"
```
- Adjust `include:` based on detected email provider (Google Workspace, Microsoft 365, AWS SES, SendGrid, Postmark)
- Always end with `~all` (soft fail) or `-all` (hard fail)

**DKIM** (DomainKeys Identified Mail):
- Provider-specific DKIM CNAME records
- Multiple DKIM records for multiple senders (transactional + marketing)

**DMARC** (Domain-based Message Authentication):
```
TXT  _dmarc.example.com  "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com; ruf=mailto:dmarc@example.com; pct=100"
```
- Start with `p=none` to monitor, then move to `p=quarantine`, then `p=reject`
- `rua` for aggregate reports, `ruf` for forensic reports

**MX records** (mail routing):
- Google Workspace: `aspmx.l.google.com` priority 10 + alternates
- Microsoft 365: `{tenant}.mail.protection.outlook.com`
- Self-hosted: `mail.example.com`

**Additional email records**:
- `autodiscover` CNAME for Outlook auto-configuration
- `_imaps._tcp` SRV for IMAP service discovery

============================================================
PHASE 5 — HEALTH CHECK ROUTING (if --health-check)
============================================================

Set up DNS-level health checks for failover or latency-based routing:

**AWS Route53 health checks**:
- HTTPS health check on `/health` endpoint, 30s interval, 3 failure threshold
- Failover routing policy with PRIMARY and SECONDARY targets
- Low TTL (60s) on failover records for fast switchover

**Cloudflare load balancing**:
- Configure origin pools (primary + fallback)
- Health check monitors (HTTP/HTTPS)
- Steering policy: failover, round-robin, or latency-based

**Latency-based routing** (multi-region):
- Separate Route53 records per region with `latency_routing_policy`
- Each record pointed to the regional origin

============================================================
PHASE 6 — VALIDATION
============================================================

After generating configuration, verify:

1. **No conflicting records** — check for duplicate A/CNAME on same name
2. **CNAME restrictions** — CNAME cannot coexist with other record types on same name
3. **TTL values** — production records should use reasonable TTLs (300-3600s)
4. **Missing records** — warn if www redirect, SSL validation records, or MX records are absent
5. **DNSSEC** — recommend enabling if provider supports it


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After completing deployment/infrastructure changes, validate:

1. Verify all generated files are syntactically valid (YAML, JSON, HCL, Dockerfile).
2. Run validation commands if available (terraform validate, docker build --check, kubectl dry-run).
3. Verify no secrets, credentials, or sensitive values are hardcoded.
4. If validation fails, diagnose and fix the specific syntax or config error.
5. Repeat up to 2 iterations.

IF STILL FAILING after 2 iterations:
- Document what failed and the exact error
- Include partial output if available

============================================================
OUTPUT
============================================================

```
## DNS Configuration Complete

### Domain: {domain}
### Provider: {provider}

### Records Generated
| Type | Name | Value | TTL | Notes |
|------|------|-------|-----|-------|
| A | {domain} | {target} | 300 | Root domain |
| CNAME | www | {domain} | 300 | www redirect |
| CNAME | api | {alb/origin} | 300 | API endpoint |
| TXT | {domain} | v=spf1... | 3600 | SPF |
| TXT | _dmarc | v=DMARC1... | 3600 | DMARC |

### SSL/TLS
- Certificate: {ACM/Cloudflare/Let's Encrypt}
- Coverage: {domain}, *.{domain}
- Auto-renewal: {yes/no}

### Files Created
{list of files}

### Nameservers (if new zone)
{ns1, ns2, ns3, ns4 — update at registrar}
```

============================================================
NEXT STEPS
============================================================

1. If new zone: update nameservers at your domain registrar
2. Wait for DNS propagation (up to 48 hours, usually minutes)
3. Verify records: `dig +short example.com A` and `dig +short example.com MX`
4. Verify SSL: `curl -vI https://example.com 2>&1 | grep 'SSL certificate'`
5. Test email authentication: send test email and check headers for SPF/DKIM/DMARC pass
6. Set up monitoring for DNS resolution and certificate expiration
7. If using DMARC with `p=none`, monitor reports for 2 weeks then tighten to `p=quarantine`


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /dns — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

============================================================
DO NOT
============================================================

- Do NOT set TTL below 60 seconds without good reason (DDoS amplification risk)
- Do NOT use CNAME at zone apex — use ALIAS, ANAME, or A record instead
- Do NOT create MX records pointing to IP addresses — use hostnames
- Do NOT use `p=reject` DMARC policy without first monitoring with `p=none`
- Do NOT create DNS records for services that do not exist yet
- Do NOT delete existing DNS records — only add or modify
- Do NOT hardcode IP addresses that may change — use CNAME to stable DNS names
- Do NOT skip SSL/TLS setup — all domains must serve over HTTPS
- Do NOT create wildcard DNS records unless specifically needed (security risk)
- Do NOT overwrite existing Terraform DNS resources without reading them first
