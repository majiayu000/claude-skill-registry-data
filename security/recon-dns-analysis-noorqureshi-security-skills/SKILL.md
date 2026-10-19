---
name: recon-dns-analysis
description: >
  Deep DNS analysis for attack surface — record mining, zone transfers, DNSSEC/NSEC walking, and
  dangling records. Load during recon, on "DNS", a domain in scope, or hunting takeovers/origin
  IPs. Signals: a root domain, CNAMEs, MX/TXT/SPF, NS servers, subdomains to resolve.
domain: recon
type: technique
stability: learning
modes: [bugbounty, pentest]
severity: info
mitre: [T1590.002]
tools: [dig, dnsx, dnsrecon, fierce]
schema_version: 1
---

# DNS analysis

## When it applies
Early recon and anytime you want surface/intel from DNS: subdomains, mail/infra hints, cloud
providers, dangling records (takeover leads), and origin IPs hiding behind a CDN.

## Why it works
DNS is a public map of an org's infrastructure. Records leak providers (CNAME → SaaS), mail and
SPF/DMARC hosts, and misconfigurations (open zone transfer dumps everything; NSEC lets you walk a
DNSSEC zone). Stale records point at deprovisioned services (→ takeover).

## Method
1. **Enumerate records**: `dig ANY domain`, plus explicit `A AAAA CNAME MX TXT NS SOA` — TXT/SPF
   reveal third parties; MX reveals mail infra.
2. **Zone transfer** (rare but total): find NS (`dig NS domain`), then `dig axfr @ns1 domain` —
   a successful AXFR dumps every record.
3. **DNSSEC walking**: if NSEC is used, walk the chain to enumerate names (`dnsrecon -t zonewalk`).
4. **Dangling / takeover leads**: resolve CNAMEs; ones pointing at unclaimed SaaS → `web-subdomain-takeover`.
5. **Origin discovery**: historical DNS (SecurityTrails), SPF-listed IPs, and cert SANs can reveal
   the real origin behind a CDN (bypass the WAF later).

## Gotchas
- AXFR is usually refused — but when it works it's the whole zone; always try the NS servers.
- CDN/proxied records hide the origin; pivot to cert/historical data, not the proxied A record.
- Wildcard DNS inflates brute-force — detect and filter it (`dnsx` wildcard handling).

## Verify success
A richer map: resolvable subdomains, provider/infra hints, any AXFR/NSEC dump, and takeover or
origin-IP leads to hand to the next skill.

## References
`dig`/`dnsrecon` docs; SecurityTrails; OWASP Amass; can-i-take-over-xyz.
