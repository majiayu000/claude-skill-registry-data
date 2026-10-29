---
name: bgp-security
description: Use when assessing BGP security on an authorized network
  engagement or lab. Covers route hijack concepts, RPKI validation
  review, BGP monitoring, and peer configuration audits. Also use when
  a client with their own ASN wants to know how exposed their prefixes
  are.
version: 1.0.0
domain: network
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [dns-enumeration, recon-active, threat-intel]
tools:
  - name: Python
    version: "3.12"
---

BGP decides how the internet routes traffic, and it trusts what peers
announce: a hijacked announcement can redirect a victim's traffic to
the attacker. This skill covers authorized assessment: reviewing a
network's BGP posture, checking RPKI coverage, monitoring for hijacks,
and auditing peer configurations. You do not announce anyone's
prefixes; assessment is review and monitoring, not active hijacking.

## Quick Workflow

1. Inventory the ASNs and prefixes the organization owns or depends
   on.
2. Check RPKI ROA coverage for every owned prefix.
3. Review BGP peer configurations: prefix filters, max prefix limits,
   and TTL security.
4. Monitor public BGP data for anomalies affecting the prefixes.
5. Assess the impact of a hijack: what traffic could be intercepted.
6. Check IRR records: are they accurate and maintained.
7. Review the incident response plan for a hijack event.
8. Report gaps with the specific prefix and the missing control.

## 1. RPKI and prefix inventory

```bash
# List owned prefixes (from the client's documentation, never guess)
cat /tmp/bgp/owned_prefixes.txt

# Check ROA coverage via a public RPKI validator API (read only)
for prefix in $(cat /tmp/bgp/owned_prefixes.txt); do
  echo "=== $prefix"
  curl -s "https://rpki-validator.example/api/roas?prefix=$prefix" | head -c 300
  echo
done
# No ROA = anyone can announce it and RPKI validators will not object
```

```python
#!/usr/bin/env python3
"""BGP posture checklist per prefix."""
prefixes = [
    {"prefix": "203.0.113.0/24", "roa": True, "irr": True},
    {"prefix": "198.51.100.0/24", "roa": False, "irr": True},
]
for p in prefixes:
    gaps = [k for k in ("roa", "irr") if not p[k]]
    print(f"{p['prefix']}: {'OK' if not gaps else 'MISSING ' + ','.join(gaps)}")
```

## 2. Peer configuration audit

```bash
# Review points for each eBGP peer (config review, your network or
# the client's with authorization):
# - prefix filter: only accept the prefixes the peer should announce
# - max-prefix: shut the session before a leak floods the table
# - TTL security (GTSM): packets must arrive with TTL 255 (direct peer)
# - MD5 or TCP-AO authentication on the session
# - no default route accepted from peers unless intended
grep -A5 "neighbor" /tmp/bgp/router_config.txt | head -40
```

```bash
# Monitor for hijacks using public route collectors (passive)
# Watch: origin AS changes for owned prefixes, more specific
# announcements, and new upstream paths
python3 - << 'PY'
print("monitor: RIPE RIS / RouteViews streams for owned prefixes")
print("alert on: origin change, unexpected more-specific, RPKI invalid")
PY
```

## Edge cases

- The organization has no ASN and uses provider space. The review
  shifts to the provider's posture and the contract terms.
- Anycast prefixes behave differently. Document the anycast design;
  hijack impact analysis changes.
- RPKI is deployed but not enforced (fail open). Recommend fail
  closed on invalid, staged carefully.

## Escalation

- Active hijack in progress: contact the upstream providers and the
  hijacking AS per the playbook; announce more specifics or ROAs as
  the plan dictates.
- No monitoring exists: set up alerting on origin changes before
  deeper work.

## Detection and defender view

Networks detect hijacks with BGP monitoring: origin changes, RPKI
invalid announcements, and latency shifts. They defend with RPKI ROAs
plus origin validation, strict prefix filters on peers, max prefix
limits, and an incident playbook with provider contacts ready. The
durable direction is RPKI everywhere and BGPsec where supported.

## Key references

- RFC 6480 (RPKI) and RFC 7454 (BGP operations security).
- MITRE ATT&CK T1590 and ICS T0806: network mapping context.
- MANRS (Mutually Agreed Norms for Routing Security) actions.
