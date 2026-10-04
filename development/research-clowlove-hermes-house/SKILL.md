---
name: research
description: ML research frameworks for building and optimizing AI systems with declarative programming.
version: 1.0.0
metadata:
  hermes:
    tags: [mlops, research]
    related_skills: ['dspy']
---

# Research

ML research frameworks for declarative AI system building.

## Domain Reconnaissance

Passive domain reconnaissance using Python stdlib — no API keys required.

### Capabilities
- **Subdomain discovery**: DNS enumeration for subdomains
- **SSL certificate inspection**: View cert details, expiry, SANs
- **WHOIS lookups**: Domain registration info
- **DNS records**: A, AAAA, MX, NS, TXT, CNAME queries
- **Domain availability checks**: Check if domains are registered
- **Bulk multi-domain analysis**: Analyze multiple domains at once

### Quick Commands
```python
import ssl, socket, dns.resolver

# SSL cert inspection
ctx = ssl.create_default_context()
with ctx.wrap_socket(socket.sock(("example.com", 443)), server_hostname="example.com") as s:
    cert = s.getpeercert()
    print(cert['notAfter'], cert['subjectAltName'])

# DNS records
answers = dns.resolver.resolve("example.com", "MX")
for rdata in answers:
    print(rdata.exchange, rdata.preference)
```

## Sub-skills

- **dspy**: DSPy: declarative LM programs, auto-optimize prompts, RAG