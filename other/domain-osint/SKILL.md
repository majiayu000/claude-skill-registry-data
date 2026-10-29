---
name: domain-osint
description: Use when investigating domains, DNS history, certificates,
  and hosting infrastructure from public sources on an authorized
  engagement. Covers RDAP and WHOIS lookups, DNS enumeration past and
  present, certificate transparency mining, passive DNS pivoting, ASN and
  BGP analysis, and infrastructure link analysis. Use when mapping an
  organization's external footprint, when triaging a suspicious domain
  from a phishing email, or when linking attacker infrastructure.
version: 1.0.0
domain: osint
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [osint-methodology]
tools:
  - name: Python
    version: "3.12"
  - name: BIND
    version: 9.20
  - name: curl
    version: 8.5
---

Domains are the skeleton of internet infrastructure, and almost every
fact about them is public: who registered them, where they resolve,
what certificates they hold, and what they resolved to last year. This
skill covers domain and DNS OSINT on public sources for authorized
work: triaging suspicious domains, mapping an organization's footprint,
and linking infrastructure. Respect rate limits, terms of service, and
privacy law; use only public data.

## Quick Workflow

1. Start with the domain as given: normalize it (lowercase, strip
   URL wrappers, handle punycode).
2. Pull RDAP/WHOIS for registrar, creation date, and status flags.
3. Resolve current DNS (A, AAAA, MX, NS, TXT, SOA) and note TTLs.
4. Mine certificate transparency for subdomains and issuance history.
5. Check passive DNS history for past IPs and nameservers.
6. Pivot: which other domains share the IP, ASN, nameserver, or
   certificate.
7. Score the domain (age, registrar, patterns) and record a verdict.
8. Archive the evidence with timestamps and move on.

## 1. RDAP and WHOIS

RDAP is the modern, structured replacement for WHOIS. Use it first.

```bash
# RDAP lookup (JSON, structured, rate-limited politely)
curl -s "https://rdap.verisign.com/com/v1/domain/example.com" | python3 -m json.tool | head -60

# Key fields to read: creation date, registrar, status flags
# (clientHold, serverHold), nameservers, last update

# Classic whois as fallback
whois example.com | grep -iE "creation|registrar|status|name server" | head -20
```

Red flags in registration data: created days ago, privacy-protected
on a domain impersonating a brand, registrar known for abuse, status
flags showing recent changes. Note that GDPR redaction hides most
registrant data on gTLDs now; work with what is public (dates,
registrar, nameservers, statuses).

## 2. Current DNS enumeration

```bash
# Full record sweep with dig (BIND 9.x)
for t in A AAAA MX NS TXT SOA CAA; do
  echo "== $t =="
  dig +short example.com $t
done

# Zone transfer attempt (usually refused; note the refusal, do not force it)
dig axfr example.com @ns1.example.com

# Check DNSSEC
dig +dnssec example.com SOA | grep -E "RRSIG|ad flag"

# Reverse DNS on the hosting IP
dig +short -x 93.184.216.34
```

Record what matters: hosting IP and ASN, mail provider (MX), TXT
records (SPF, DKIM selectors, verification tokens that leak SaaS
usage), and nameserver provider. A domain with MX pointing at a free
mailbox provider while impersonating a bank is a strong phishing
signal.

## 3. Certificate transparency

Every public TLS certificate is logged. crt.sh is the standard
interface.

```bash
# All subdomains ever certified for a domain
curl -s "https://crt.sh/?q=%25.example.com&output=json" \
  | python3 -c "
import json,sys
seen=set()
for e in json.load(sys.stdin):
    for n in e['name_value'].splitlines():
        n=n.strip().lower()
        if n and not n.startswith('*'):
            seen.add(n)
print('\n'.join(sorted(seen)))"

# Issuance timeline: when were certs issued (bursts suggest campaigns)
curl -s "https://crt.sh/?q=%25.example.com&output=json" \
  | python3 -c "
import json,sys
from collections import Counter
c=Counter(e['entry_timestamp'][:10] for e in json.load(sys.stdin))
for d in sorted(c): print(d, c[d])"
```

For a suspicious domain, check: certificate age vs domain age (a cert
issued yesterday on a week-old domain is typical for phishing),
issuer (free ACME issuers are normal now, so this is weak signal
alone), and subject alternative names shared with other domains.

## 4. Passive DNS and history

Passive DNS shows where a domain pointed in the past, which links
current infrastructure to old campaigns.

```bash
# ViewDNS or similar public passive DNS (respect terms, low volume)
curl -s "https://api.viewdns.info/propagation/?domain=example.com" | head -20

# Historical approach with local data: query common public resolvers
# and compare against your notes from previous investigations
for r in 1.1.1.1 8.8.8.8 9.9.9.9; do
  echo "== $r =="; dig +short example.com A @$r
done
```

What to look for: IP changes right before a campaign, moves between
ASNs (bulletproof hosting hops), and long-dormant domains suddenly
activated. Keep your own notes; your history file becomes passive DNS
for your team.

## 5. Infrastructure pivoting

One domain is a thread; pull it to find the sweater.

```bash
# Reverse IP: which domains share the host (use a passive DNS source)
# Then check each for registration patterns

# ASN lookup for the hosting IP
whois -h whois.cymru.com " -v 93.184.216.34"

# BGP origin check
curl -s "https://api.bgpview.io/ip/93.184.216.34" \
  | python3 -c "import json,sys; d=json.load(sys.stdin)['data'];
print(d['prefixes'][0]['asn']['asn'], d['prefixes'][0]['asn']['name'])"
```

Pivot points in order of reliability: exact IP match, same /24 with
matching registration patterns, shared nameserver, shared
certificate, shared ASN. Attackers share infrastructure to save money;
defenders link it to burn the whole cluster at once. Verify each link
before asserting it: shared Cloudflare IPs mean nothing, shared
bulletproof-host IPs mean a lot.

## 6. Scoring a suspicious domain

Triage checklist for a domain from a phishing email or alert:

```python
#!/usr/bin/env python3
"""Domain triage heuristics. Each hit adds suspicion; verify manually."""
import datetime

def triage(domain, created, registrar):
    score, reasons = 0, []
    age = (datetime.date.today() - created).days
    if age < 30:
        score += 30; reasons.append(f"very new: {age} days old")
    elif age < 180:
        score += 10; reasons.append(f"young: {age} days old")
    if any(k in domain for k in ["login", "verify", "secure", "update", "account"]):
        score += 15; reasons.append("contains lure keyword")
    if domain.count("-") >= 2 or sum(c.isdigit() for c in domain) >= 3:
        score += 10; reasons.append("suspicious characters")
    print(domain, "score:", score)
    for r in reasons: print(" -", r)

triage("secure-login-update-2026.example.com", datetime.date(2026, 10, 20), "cheap-registrar")
```

Combine with: does it resolve, does it serve a login page, does the
certificate match the brand, is it on any blocklist. A score is a
triage aid, not a verdict; always confirm with content inspection in
a safe sandbox.

## 7. Mapping an organization's footprint

For authorized external recon, systematize:

```bash
# 1. Subdomains from CT logs (see section 3), save to a file
# 2. Resolve them all
cat subdomains.txt | xargs -P 20 -I{} sh -c 'echo "{} $(dig +short {} A | head -1)"' \
  > resolved.txt

# 3. Group by IP/ASN to find hosting clusters
awk '{print $2}' resolved.txt | sort | uniq -c | sort -rn | head -20

# 4. Check each live host for a TLS cert and banner (light touch only)
```

Stay passive where possible; active port scanning needs explicit
authorization even from the outside. Document the boundary in the
collection plan.

## Edge cases

- Wildcard DNS returns an IP for every subdomain. Detect it by
  resolving a random non-existent name first; if it resolves, your
  subdomain list is polluted.
- DNS-based blocklists and sinkholes: a domain resolving to a known
  sinkhole IP is already neutralized; note it and move on.
- Privacy-protected WHOIS is the norm now. Do not try to bypass it;
  pivot on technical data (IPs, certs, nameservers) instead.
- IDN homographs: check punycode (`xn--`) forms; a domain that looks
  like a brand in the email client may be Cyrillic or Greek letters.
- Fast flux: IPs change every few minutes. Note the flux pattern
  itself as the finding; single snapshots mislead.
- Rate limits on crt.sh and RDAP: cache results, space queries, and
  never hammer public infrastructure from an investigation script.

## Escalation

- The domain is actively phishing your users: escalate to incident
  response, request takedown via the registrar and hosting provider,
  and submit to blocklist feeds.
- You find your own organization's data on attacker infrastructure:
  treat as an incident, preserve evidence, and engage the IR process.
- Registration data suggests an insider or partner: hand the finding
  to the investigation lead; do not contact the subject.
- You need non-public data (registrar logs, hosting customer info):
  that requires legal process. Route through legal, not through
  clever queries.
- Infrastructure links point to a large shared host: do not assert
  attribution on shared IPs alone; find a stronger pivot or mark it
  inconclusive.

## Detection and defender view

Domain OSINT cuts both ways:

- Attackers monitor certificate transparency for your new
  subdomains to find fresh targets. Watch CT logs for your own
  domains and investigate unexpected issuances.
- Attackers age domains and use reputable registrars to look
  legitimate. Do not rely on age alone; inspect content and
  behavior.
- Defenders can poison attacker recon with canary subdomains and
  monitor who resolves or probes them.
- Track typosquat registrations of your brand proactively and
  takedown the malicious ones before campaigns start.
- Your own DNS history is attacker intel: minimize stale records,
  remove forgotten subdomains, and keep SPF/DKIM tight so your
  domain is harder to spoof.

## Key references

- MITRE ATT&CK T1590.002 (DNS), T1593 (Search Open Websites and
  Domains), T1583.001 (Acquire Domains), T1566 (Phishing).
- RDAP specification (RFC 9082, 9083).
- crt.sh documentation: https://crt.sh/
- BIND 9 dig manual: https://bind9.readthedocs.io/
- Cymru IP to ASN mapping: https://www.team-cymru.com/
