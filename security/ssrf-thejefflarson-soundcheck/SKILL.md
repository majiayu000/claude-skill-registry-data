---
name: ssrf
description: Detects HTTP requests to user-controlled URLs that can reach internal services
  or cloud metadata endpoints. Use when writing code that makes HTTP requests
  to URLs constructed from user input, fetches resources from caller-specified
  addresses, or proxies requests on behalf of users. Also invoke when
  implementing webhook receivers or URL preview features.
---

# SSRF Security Check (A10:2025 / API7:2023)

## What this checks

Protects against Server-Side Request Forgery where an attacker tricks the server into
making requests to internal services, cloud metadata endpoints, or arbitrary external
hosts. Exploitation leads to internal network scanning, credential theft from cloud
metadata APIs (169.254.169.254), and access to services behind firewalls.

## Vulnerable patterns

- Outbound HTTP fetch where the URL, host, or scheme comes from request input with no validation
- Webhook callback or URL-preview feature that follows whatever the caller supplies
- URL-fetch APIs that follow redirects by default, letting an allowlisted host 302 to an internal IP
- Hostname-only allowlists that do not also check the resolved IP — vulnerable to DNS rebinding

## Fix immediately

Flag the vulnerable code, explain the risk, and suggest a fix establishing these
properties. **Proxy, webhook, and URL-preview features are the highest-risk shapes** —
the scheme/host/IP/redirect checks must actually run at the call site before the
outbound request; a comment saying "URL should be validated" satisfies nothing if the
next line still fetches the raw URL. Translate to the language and HTTP client of the
audited file — use that stack's documented URL parser, DNS resolver, and redirect
controls.

1. **Scheme is restricted to `https` (and `http` only for trusted internal use).** Reject `file:`, `gopher:`, `ftp:`, `dict:`, and other schemes that SSRF toolkits exploit.
2. **Host is checked against an allowlist, and the resolved IP is checked against a blocklist covering private, loopback, and link-local ranges** — IPv4 `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `127.0.0.0/8`, `169.254.0.0/16` and IPv6 `::1/128`, `fc00::/7`, `fe80::/10`. Resolve-then-check defeats DNS rebinding: an allowlisted hostname can still resolve to `169.254.169.254`. Language-idiomatic checks that cover the same ranges are equivalent to explicit CIDR comparisons.
3. **Redirects are disabled, or each redirect target is re-validated against the same allowlist.** A lone allowlisted host can still 302 to an internal IP.
4. **The check actually runs.** A blocklist declared and never evaluated does not satisfy any of the above — the comparison must be present at the call site, before the outbound request.

## Verification

- [ ] Every outbound HTTP request using a caller-supplied URL validates the scheme, host, and resolved IP against an allowlist or blocklist before the request is sent
- [ ] Cloud metadata and link-local addresses are blocked — either via explicit CIDR entries covering `169.254.0.0/16`, `fe80::/10`, and `fc00::/7`, or via language-idiomatic checks that cover the same ranges. Declaring a list without evaluating it does not satisfy this
- [ ] HTTP redirects are disabled, or each redirect target is re-validated against the same allowlist
- [ ] DNS resolution results are checked for private/loopback/link-local IPs before connecting

## References

- CWE-918 ([Server-Side Request Forgery](https://cwe.mitre.org/data/definitions/918.html))
- [OWASP A10:2025 Server-Side Request Forgery](https://owasp.org/Top10/A10_2021-Server-Side_Request_Forgery_%28SSRF%29/)
- [OWASP API7:2023 Server Side Request Forgery](https://owasp.org/API-Security/editions/2023/en/0xa7-server-side-request-forgery/)
