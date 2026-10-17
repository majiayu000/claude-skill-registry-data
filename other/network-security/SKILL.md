---
name: network-security
description: Secure network paths and exposure — segmentation, TLS everywhere, DNS/email auth, WAF/tunnels, egress control.
version: 1
triggers: network security, tls, segmentation, waf, dns security, secure network
category: Security & privacy
blurb: Secure the network paths — segmentation, TLS everywhere, DNS and email authentication.
archetype: knowledge
example: Review the network exposure of my home server setup.
---

# Network Security

The network is an attack surface: shrink what's reachable, encrypt what moves, and know exactly what's exposed — always.

## When to use
- New service going live; new domain/tunnel/port.
- Hardening home-lab, box, or cloud setups.
- Reviewing "why can anyone reach this?" incidents.

## Method
1. **Exposure inventory**: maintain the list of public endpoints (domains, ports, tunnels) and what serves each. If it's not on the list, it's not allowed public.
2. **Default-deny posture**: everything listens on loopback unless a list entry justifies exposure; prefer tunnels (cloudflared/SSH, authenticated) over open ports.
3. **Segmentation**: separate services into trust zones (public edge / app / data / admin); admin planes never share the public path.
4. **TLS everywhere**: valid certs (auto-renew + monitor expiry), HSTS on web, no plaintext protocols (HTTP/FTP/telnet) on any path; modern TLS config only.
5. **DNS + email auth**: registrar lock + 2FA; DNSSEC where possible; SPF, DKIM, DMARC on every sending domain; monitor DMARC reports.
6. **Edge protection**: CDN/WAF in front of web (rate limits, bot rules); DDoS posture on the provider; don't roll your own edge.
7. **Egress control**: outbound allowlists for servers that don't need the internet; log unexpected egress.
8. **Evidence**: network events logged (denied + accepted), reviewed on change and on incident.

## Quality gates
- [ ] Exposure inventory current; every public entry has an owner.
- [ ] No plaintext protocol paths; cert expiry monitored.
- [ ] SPF/DKIM/DMARC present on sending domains.
- [ ] Admin access only via authenticated path (tunnel/VPN/SSO), never open ports.

## Red lines
- No admin/DB panels exposed to the internet ("temporarily").
- No default credentials anywhere; no unauthenticated tunnels.

## Related
`firewall-engineering` · `zero-trust-architecture` · `authentication-authorization`.
