---
name: domain-intel
description: "Passive domain reconnaissance using Python stdlib — subdomain discovery via crt.sh, SSL/TLS certificate inspection, WHOIS lookups (100+ TLDs), DNS records (A/AAAA/MX/NS/TXT/CNAME), domain availability checks, and bulk multi-domain analysis. Zero dependencies, zero API keys. Triggers on requests like 'find subdomains', 'check ssl cert', 'whois lookup', 'is this domain available', 'bulk check these domains'."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [dns, whois, ssl, domain, recon, osint, subdomain, network]
    triggers: [domain, subdomain, whois, dns-lookup, ssl-certificate, osint, recon, bulk-domain]
    related_skills: [osint-redteam, osint-recon]
---

# Domain Intelligence

Passive domain intelligence using only Python stdlib and public data sources.
**Zero dependencies. Zero API keys. Works out of the box.**

Use this when you need quick domain recon without installing any tools or
registering for API keys — WHOIS lookup, SSL certificate inspection, DNS
records, subdomain discovery, and bulk analysis, all via stdlib + public
endpoints.

---

## When to Use

- "Find subdomains for example.com"
- "Check the SSL certificate on api.example.com"
- "WHOIS lookup for this domain"
- "What DNS records does this domain have?"
- "Is this domain available?"
- "Bulk check these 10 domains"

## Capabilities

| Feature | How | Limits |
|---------|-----|--------|
| Subdomain discovery | crt.sh certificate transparency logs | Up to ~1000 entries per domain |
| SSL/TLS cert inspection | socket + ssl module | Live connection to target |
| WHOIS lookup | Direct TCP to authoritative TLD servers | 100+ TLDs supported |
| DNS records | Google DNS-over-HTTPS (MX/NS/TXT/CNAME), system DNS (A/AAAA) | Rate-limited by Google DoH (~150 req/sec) |
| Domain availability | Multi-signal (DNS + WHOIS + SSL probe) | Single-domain only per check |
| Bulk analysis | Parallel per-domain processing | Up to 20 domains at once |

## Data Sources

- **crt.sh** — Certificate Transparency logs (subdomain discovery)
- **WHOIS servers** — Direct TCP to 100+ authoritative TLD servers
- **Google DNS-over-HTTPS** — MX/NS/TXT/CNAME resolution
- **System DNS** — A/AAAA records (via stdlib `socket.getaddrinfo`)
- **Live SSL handshake** — Certificate inspection via `ssl.wrap_socket`

## Quick Reference

### Subdomain Discovery
```python
import urllib.request, json, ssl

def find_subdomains(domain: str) -> list[str]:
    """Discover subdomains via crt.sh certificate transparency."""
    ctx = ssl.create_default_context()
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    with urllib.request.urlopen(url, context=ctx) as resp:
        entries = json.loads(resp.read().decode())
    return sorted({e['name_value'] for e in entries})
```

### WHOIS Lookup
```python
import socket

def whois(domain: str, server: str = "whois.verisign-grs.com", port: int = 43) -> str:
    """Query a WHOIS server directly over TCP."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(15)
    sock.connect((server, port))
    sock.send(f"{domain}\r\n".encode())
    response = b""
    while chunk := sock.recv(4096):
        response += chunk
    sock.close()
    return response.decode(errors="replace")
```

### SSL Certificate Inspection
```python
import ssl, socket

def inspect_cert(host: str, port: int = 443) -> dict:
    """Return certificate fields from a live SSL handshake."""
    ctx = ssl.create_default_context()
    with socket.create_connection((host, port), timeout=10) as sock:
        with ctx.wrap_socket(sock, server_hostname=host) as ssock:
            cert = ssock.getpeercert()
    return {
        "subject": dict(cert["subject"][0]),
        "issuer": dict(cert["issuer"][0]),
        "not_before": cert["notBefore"],
        "not_after": cert["notAfter"],
        "san": cert.get("subjectAltName", []),
        "serial": cert.get("serialNumber"),
    }
```

### DNS Records (via Google DoH)
```python
import urllib.request, json

def dns_lookup(domain: str, rtype: str = "A") -> list[str]:
    """Fetch DNS records via Google DNS-over-HTTPS."""
    url = f"https://dns.google/resolve?name={domain}&type={rtype}"
    with urllib.request.urlopen(url) as resp:
        data = json.loads(resp.read().decode())
    return [a["data"] for a in data.get("Answer", [])]
```

## Common Pitfalls

1. **WHOIS rate limiting** — Some TLD WHOIS servers throttle rapid queries. Add a `time.sleep(1)` between bulk WHIOS lookups.

2. **crt.sh truncation** — The JSON endpoint may return at most ~1000 entries per domain. For very large domains, use cursor-based pagination or the SQL interface.

3. **SSL cert wildcards** — `*.example.com` SANs match subdomains but not the bare domain. Check both `example.com` AND `*.example.com` entries in SAN lists.

4. **Google DoH rate limits** — Sustained bursts above ~150 req/sec return 429. Add jitter or switch to system DNS for A/AAAA queries under heavy load.

5. **System DNS spoofing** — On untrusted networks, A/AAAA records from `socket.getaddrinfo` may be poisoned. Prefer Google DoH for sensitive queries.

6. **No IPv6 guarantee** — Some WHOIS servers may not have IPv6 connectivity. Use `socket.AF_INET` explicitly if IPv6 is unreliable on the scanning host.

## Cross-References

- `security/osint-redteam` — Full red-team reconnaissance pipeline (requires Go tools, Nuclei, API keys). Use this skill for lightweight stdlib-only lookups before pulling out the heavy tooling.

## Verification Checklist

- [ ] Single subdomain discovery returns expected results for a known domain
- [ ] WHOIS lookup returns registrant details for a .com domain
- [ ] SSL cert inspection returns subject, issuer, and SAN fields
- [ ] DNS lookup returns at least A and MX records
- [ ] Bulk analysis (5+ domains in parallel) completes without timeout or 429
