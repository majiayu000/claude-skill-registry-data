---
name: recon-subdomain-enum
description: >
  Enumerate subdomains and live hosts to build the attack surface for a bug-bounty program or
  external assessment. Load at engagement start, on "recon", a root domain in scope, "find
  subdomains", or before content discovery. Signals: wildcard scope (*.target.com), a program
  scope list, a new external target.
domain: recon
type: technique
stability: learning
modes: [bugbounty]
severity: info
mitre: [T1595, T1590]
tools: [subfinder, amass, dnsx, httpx, naabu]
schema_version: 1
---

# Subdomain & live-host enumeration

## When it applies
External, in-scope, wildcard programs where surface = subdomains. Do this before hunting;
most bugs live on forgotten hosts (staging, dev, legacy, acquisitions).

## Why it works
Organizations sprint faster than they inventory. Passive sources (CT logs, DNS aggregators)
plus permutation/brute-force surface hosts nobody remembers — and those skip the hardening
the flagship app got.

## Method
1. **Passive** (fast, quiet): `subfinder -d target.com -all -silent` and `amass enum -passive
   -d target.com`. Pulls CT logs, PassiveDNS, search engines — no packets to the target.
2. **Resolve & dedupe**: `dnsx -l subs.txt -a -resp -silent` to keep only records that resolve
   (drops dead CT noise) and grab their IPs.
3. **Brute/permute** for hidden hosts: `puredns`/`shuffledns` with a DNS wordlist + `dnsgen`
   permutations (`dev-`, `-staging`, region prefixes) against resolvers.
4. **Probe live web**: `httpx -l resolved.txt -sc -title -tech-detect -cdn -silent` → status,
   title, tech, CDN. This is your ranked target list.
5. **Port sweep** where allowed: `naabu -l hosts.txt -top-ports 1000` to find non-web services.

## Gotchas
- Wildcard DNS (`*.target.com` → one IP) creates false positives — filter with `dnsx`/`puredns`
  wildcard detection before trusting a hit.
- Confirm each host is **in program scope** before probing; out-of-scope acquisitions are a trap.
- CDN/WAF IPs are shared — don't port-scan Cloudflare ranges; find origin instead.

## Verify success
A deduplicated list of resolving, in-scope hosts with status/title/tech — the input to
content discovery and per-class hunting.

## References
ProjectDiscovery docs (subfinder/httpx/dnsx/naabu); OWASP Amass; TomNomNom recon workflow.
