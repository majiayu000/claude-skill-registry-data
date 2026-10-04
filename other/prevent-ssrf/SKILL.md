---
name: prevent-ssrf
description: Use when building features that fetch URLs or make HTTP requests based on user-supplied input — web scrapers, webhook receivers, URL preview services, import-from-URL features, or any server-side HTTP client.
source: 'OWASP Server-Side Request Forgery Prevention Cheat Sheet (owasp.org/www-project-cheat-sheets); OWASP Top 10 2021 A10; CWE-918'
tags: [security, owasp, ssrf, server-side-request-forgery, web, developer, cloud]
---

# Prevent SSRF

Block server-side request forgery by validating and allowlisting URLs before making server-side HTTP requests — preventing attackers from using your server as a proxy to reach internal metadata endpoints, databases, or cloud infrastructure.

## Why This Is Best Practice

**Adopted by:** OWASP added SSRF as its own category in Top 10 2021 (A10) due to increasing severity in cloud environments. AWS, GCP, and Azure now offer IMDS v2 (token-required metadata endpoints) specifically to mitigate SSRF. Google exposed $31,337 in SSRF bug bounties. Capital One's 2019 breach (100M records) was executed entirely via SSRF exploiting AWS EC2 metadata at `169.254.169.254`.
**Impact:** In cloud environments, SSRF can reach the instance metadata service (IMDS) and retrieve IAM credentials, enabling full cloud account takeover without any direct database access. Capital One breach (2019) affected 100M+ records via a WAF SSRF vulnerability. Netflix, GitLab, and Shopify have all paid significant SSRF bug bounties. In containerized environments, SSRF can reach Kubernetes API servers on internal networks.
**Why best:** Denylist-based approaches (blocking `169.254.169.254`, `localhost`, `127.0.0.1`) fail because attackers bypass them with DNS rebinding, IPv6 addresses (`::1`, `::ffff:127.0.0.1`), decimal encoding (`2130706433` = `127.0.0.1`), or redirects. Allowlist-based validation (permitting only known external domains) is the only reliable defense.

Sources: OWASP SSRF Prevention Cheat Sheet; Capital One breach report (2019); AWS IMDS v2 documentation; CWE-918

## Steps

1. **Use an allowlist of approved URL patterns** — define which domains/URLs your feature should reach:

   ```python
   ALLOWED_DOMAINS = {'api.example.com', 'uploads.example.com', 'cdn.partner.com'}

   from urllib.parse import urlparse
   import ipaddress

   def validate_url(url):
       parsed = urlparse(url)
       if parsed.scheme not in ('http', 'https'):
           raise ValueError("Only HTTP/HTTPS allowed")
       hostname = parsed.hostname
       if hostname not in ALLOWED_DOMAINS:
           raise ValueError(f"Domain not allowed: {hostname}")
       return url
   ```

2. **Block all private and link-local IP ranges after DNS resolution** — resolve the hostname and check the resulting IP, not just the domain name:

   ```python
   import socket
   import ipaddress

   BLOCKED_RANGES = [
       ipaddress.ip_network('10.0.0.0/8'),
       ipaddress.ip_network('172.16.0.0/12'),
       ipaddress.ip_network('192.168.0.0/16'),
       ipaddress.ip_network('127.0.0.0/8'),
       ipaddress.ip_network('169.254.0.0/16'),   # AWS/GCP/Azure IMDS
       ipaddress.ip_network('::1/128'),
       ipaddress.ip_network('fc00::/7'),
   ]

   def is_safe_ip(hostname):
       try:
           ip = ipaddress.ip_address(socket.gethostbyname(hostname))
       except (socket.gaierror, ValueError):
           return False
       return not any(ip in net for net in BLOCKED_RANGES)
   ```

3. **Prevent DNS rebinding** — resolve DNS once and use the resolved IP for the actual connection:

   ```python
   import requests
   from requests.adapters import HTTPAdapter

   class SSRFSafeAdapter(HTTPAdapter):
       def send(self, request, **kwargs):
           # Resolve and validate before sending
           hostname = urlparse(request.url).hostname
           if not is_safe_ip(hostname):
               raise SecurityError("Blocked SSRF attempt")
           return super().send(request, **kwargs)

   session = requests.Session()
   session.mount('http://', SSRFSafeAdapter())
   session.mount('https://', SSRFSafeAdapter())
   ```

4. **Disable HTTP redirects, or re-validate after each redirect**:

   ```python
   # Option A: disable redirects entirely
   response = requests.get(url, allow_redirects=False)

   # Option B: validate each redirect destination
   def safe_get(url, max_redirects=3):
       for _ in range(max_redirects):
           resp = requests.get(url, allow_redirects=False)
           if resp.is_redirect:
               url = resp.headers['Location']
               validate_url(url)   # re-validate the redirect target
           else:
               return resp
       raise SecurityError("Too many redirects")
   ```

5. **In cloud environments, enforce IMDS v2** — IMDSv2 requires a PUT request to obtain a token before accessing metadata. Even if SSRF reaches the endpoint, the attacker cannot get credentials without the token step.

   AWS: Set `HttpTokens: required` on EC2 instance metadata options.
   GCP: Block `metadata.google.internal` via VPC firewall rules.
   Azure: Enable IMDS v2 (managed identity with required tokens).

6. **Use an isolated outbound proxy for user-facing fetch features** — route all user-driven HTTP requests through a dedicated proxy with strict allowlist enforcement, separate from your internal service traffic. Prevents SSRF from reaching internal microservices.

## Rules

- DNS rebinding bypasses hostname checks — always resolve and check the IP, not just the hostname.
- Redirects are SSRF vectors — an allowlisted URL that redirects to `http://169.254.169.254` will bypass hostname-only checks.
- IPv6 addresses, decimal IP encoding, and URL-encoded characters are all bypass vectors — use a normalized IP comparison after resolution.
- File URI (`file:///etc/passwd`) and other non-HTTP schemes must be blocked explicitly.

## Common Mistakes

- **Blocking by regex pattern on the URL string** — `if '169.254' in url` is bypassed by `http://0251.0376.0251.0376/` (octal encoding).
- **Allowing redirects without re-validation** — the initial URL passes the check, then a redirect targets an internal service.
- **Only protecting web-facing features** — PDF generators, email link unfurling, and webhook delivery systems are common SSRF vectors.
- **Denylist without allowlist** — blocking known bad IPs creates a whack-a-mole game; allowlist known good domains instead.
