---
name: c2-redirectors
description: Use when designing or deploying a redirector for an authorized red team operation or a lab command and control exercise. Covers redirector tiers that shield the team server, domain fronting concepts and why providers now block them, nginx and Apache filtering rules that forward only profile traffic, decoy content, redirector OPSEC, certificate and domain hygiene, and detection by defenders through TLS fingerprints, passive DNS, and decoy probing.
version: 1.0.0
domain: c2
lifecycle: stable
last_verified: "2026-10-27"
requires:
  - c2-fundamentals
extends: []
relates:
  - network-pivoting
  - c2-sliver-operations
  - c2-cobalt-strike-operations
tools:
  - name: nginx
    version: "1.26.x"
  - name: Apache HTTP Server
    version: "2.4.x"
  - name: OpenSSL
    version: "3.x"
  - name: Python
    version: "3.12"
---

A redirector is a sacrificial front door for command and control. It sits
between in-scope targets and the team server, forwards only traffic that
matches the agreed beacon profile, and answers everything else with
plausible decoy content. This skill is for authorized red team work and
lab environments only, under a signed rules of engagement. The team server
address must never appear in target-facing traffic, and the redirector
itself must be treated as disposable infrastructure that defenders may
find, block, and burn.

## Quick Workflow

1. Confirm the rules of engagement allow a redirector, and record the approved domains, ports, and traffic profile.
2. Provision a short-lived host for the redirector only, separate from the team server host.
3. Register a domain you own for the engagement, and issue a fresh certificate for it.
4. Write filtering rules that forward only the beacon URI, method, headers, and user agent from the profile.
5. Serve a believable decoy site on every other path, and test it from an unprofiled client.
6. Point implants at the redirector domain, never at the team server address.
7. Monitor redirector logs for stray hits, rotate on burn, and tear the host down at engagement end.

## 1. Redirector tiers

A single-tier design is one redirector in front of one team server. It is
simple, cheap, and the right default for a lab or a short engagement. A
two-tier design adds a second redirector layer, often in a different
provider or region, so burning the outer tier does not expose the inner
one. Only add tiers you can actually operate and monitor. Every extra
hop adds latency, another TLS termination point, and another log source
to watch, and an unmonitored tier is worse than no tier at all.

Keep roles strictly separated. The redirector terminates TLS, filters,
and proxies. The team server issues tasks and stores results. Nothing
else runs on either host. No SSH exposed to the internet without key
authentication and an allowlist, no extra web applications, no shared
credentials between tiers or engagements.

```bash
# Harden the redirector host before it serves anything
sudo apt update && sudo apt upgrade -y
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw enable
sudo systemctl disable --now apache2 2>/dev/null || true
ss -tlnp | grep -E "443|22"
```

The last command confirms only the expected ports are listening. If
anything else is listening, remove it before the engagement starts.

## 2. Filtering with nginx

Filtering is the whole point. A redirector that proxies everything is
just a public doorway to the team server. Forward only the exact
combination the profile defines, typically a specific URI plus a
plausible user agent and method. Everything else, including scanners,
sandboxes, and curious analysts, gets the decoy.

```nginx
server {
    listen 443 ssl;
    server_name cdn-updates.example.net;
    ssl_certificate /etc/nginx/c2.crt;
    ssl_certificate_key /etc/nginx/c2.key;
    ssl_protocols TLSv1.2 TLSv1.3;

    location /api/v2/config {
        if ($http_user_agent != "Mozilla/5.0 (Windows NT 10.0; Win64; x64)") {
            return 404;
        }
        limit_except GET POST {
            deny all;
        }
        proxy_pass https://10.0.0.5:8443;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location / {
        root /var/www/decoy;
        index index.html;
    }
}
```

Note the team server address in `proxy_pass` is a private address on
the operator side of the infrastructure, never a value the target
network can resolve or reach directly. Replace `10.0.0.5` with the real
team server address for the engagement, and keep that address out of
every implant, document, and log that leaves the operator network.

```bash
# Validate the config, reload, then test both paths
sudo nginx -t && sudo systemctl reload nginx

# Profiled request should reach the team server path
curl -sk -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" \
  https://cdn-updates.example.net/api/v2/config -o /dev/null -w "profiled %{http_code}\n"

# Unprofiled request should get the decoy, never the team server
curl -sk https://cdn-updates.example.net/api/v2/config -o /dev/null -w "unprofiled %{http_code}\n"
curl -sk https://cdn-updates.example.net/ -o /dev/null -w "decoy %{http_code}\n"
```

Test from a host that is not part of the engagement too. If the decoy
fails anywhere, fix it before any implant beacons, because the first
stray hit is often a defender or a scanner, not a target.

## 3. Domain fronting concepts

Domain fronting hid the true destination of a connection behind a
front domain hosted on the same content delivery network, by sending
one name in the TLS Server Name Indication and a different name in the
HTTP Host header. It worked because some providers routed on the Host
header while the network observer only saw the front domain. Major
providers have since blocked mismatched SNI and Host values, and
designing a current engagement around domain fronting is planning
around a dead technique.

What survives from the idea is the principle, not the trick. Use a
clean domain with a plausible name, valid TLS, and a real-looking
decoy site, so traffic to the redirector looks ordinary at a glance.
Do not buy a domain that mimics a real brand, do not typosquat a
client vendor, and do not front through a provider in a way that
violates its terms. If the rules of engagement forbid a technique,
that is the end of the discussion.

```bash
# Issue a fresh certificate for the engagement domain only
openssl req -x509 -newkey rsa:4096 -keyout c2.key -out c2.crt \
  -days 90 -nodes -subj "/CN=cdn-updates.example.net"

# Confirm the certificate name matches the redirector domain
openssl x509 -in c2.crt -noout -subject -dates
```

One certificate per engagement, one domain per engagement, and no
reuse after a burn. Reused infrastructure links engagements together
in passive DNS and certificate transparency logs.

## 4. Decoy content and OPSEC

The decoy is what defenders and scanners see, so it must hold up to a
casual look. A single static page with no links, no styling, and a
server banner that names the real stack fails that look immediately.
Build a small static site that matches the domain story, for example a
software update page for a fictional product, with a few internal
links, ordinary images, and no reference to testing, implants, or the
client.

```python
# Build a minimal decoy site and check every link resolves locally
import os

pages = {
    "index.html": "<html><body><h1>Update Center</h1><p>Check for updates.</p></body></html>",
    "about.html": "<html><body><h1>About</h1><p>Release notes and support.</p></body></html>",
}
os.makedirs("/tmp/decoy", exist_ok=True)
for name, html in pages.items():
    with open(os.path.join("/tmp/decoy", name), "w") as f:
        f.write(html)
print("decoy pages:", sorted(os.listdir("/tmp/decoy")))
```

OPSEC rules for the redirector tier are simple and non-negotiable.
Keep beacons inside agreed hours. Cap the number of sessions per
redirector so a flood does not stand out. Log forwarded requests and
rejected requests separately, and review the rejected log daily, because
a spike in rejections often means the domain was found. Rotate the
redirector domain on a pre-agreed trigger, such as a blocklist hit or
an unusual probing pattern, rather than improvising mid-engagement.
When the engagement ends, kill the host, revoke the certificate, and
park or release the domain.

## Edge cases

- A redirector that proxies on Host header alone forwards scanner traffic straight to the team server. Always filter on URI, method, and user agent together.
- TLS inspection on the target network defeats the decoy story and exposes beacon content. If inspection is in scope, either the rules cover it or you change channels.
- A burned domain that keeps beaconing tells defenders the implant is still alive. Kill sessions first, then retire the domain, in that order.
- Redirector and team server on the same host means one compromise or one blocklist entry kills both. Keep them on separate hosts and separate providers where the plan calls for it.
- Clock skew and stale DNS caching can send beacons to a retired redirector for hours. Set short DNS time to live values during rotation windows.
- A decoy that 404s on its own homepage is a louder signal than no decoy at all. Test the decoy from outside the operator network before go-live.

## Detection and defender view

Defenders find redirectors through certificate transparency logs for
newly registered domains, passive DNS showing a fresh domain pointing
at a short-lived host, JA3 TLS fingerprints that do not match real
browsers, beacon timing regularity, and decoy sites that do not match
their claimed purpose. A redirector that answers a scanner with the
team server handshake has already failed. Assume a competent blue team
will find a long-running redirector, share indicators with the
defensive contact after the engagement, and treat the time to detection
as a result, not a failure.

## Key references

- MITRE ATT&CK T1090 Proxy
- MITRE ATT&CK T1090.002 External Proxy
- MITRE ATT&CK T1071.001 Web Protocols
- MITRE ATT&CK T1568 Dynamic Resolution
- MITRE ATT&CK T1573 Encrypted Channel
- MITRE ATT&CK T1105 Ingress Tool Transfer
- CWE-200 Exposure of Sensitive Information to an Unauthorized Actor
- nginx docs: https://nginx.org/en/docs/
- Apache HTTP Server docs: https://httpd.apache.org/docs/
