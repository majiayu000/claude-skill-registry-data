---
name: defense-incident-response
description: >
  Run an incident end to end — detect, scope, contain, eradicate, recover, learn. Load for "we've
  been breached", "incident response", "contain this host", "we found malware/an intrusion", or to
  build an IR plan. Complements defense-dfir-triage (evidence collection) with the response process
  around it.
domain: defense
type: methodology
stability: locked
modes: [defense]
severity: info
mitre: []
tools: [velociraptor, edr, timesketch, thehive]
schema_version: 1
---

# Incident response

## When it applies
A confirmed or suspected compromise needs a coordinated response — not just analysis, but decisions
about containment, eviction, and recovery under time pressure.

## Why it works
A repeatable lifecycle keeps a stressful event from becoming chaos: it sequences the actions so you
scope before you contain, contain before you tip off the adversary, and eradicate fully before you
recover — the mistakes that turn one incident into three.

## Method (NIST / PICERL lifecycle)
1. **Prepare** (before): comms plan, roles, logging, backups, and access ready. You don't want to
   build these mid-incident.
2. **Identify & scope**: what's the initial evidence, which hosts/identities/data are involved, when
   did it start? Build a timeline; collect volatile evidence first (`defense-dfir-triage`).
3. **Contain**: isolate affected hosts (network quarantine, not power-off — preserve memory),
   disable compromised accounts, revoke tokens/keys. Do it broadly enough to matter but coordinate
   so you don't tip off an adversary mid-scoping.
4. **Eradicate**: remove persistence (services, tasks, startup, cloud roles), rotate all exposed
   credentials, patch the entry vector. Scope drives this — miss a foothold and they return.
5. **Recover**: restore from known-good, monitor closely for re-entry, phase systems back.
6. **Lessons learned**: timeline, root cause, what detection would have caught it sooner → feed
   `defense-detection-engineering`.

## Gotchas
- Powering off destroys memory evidence; isolate instead.
- Partial eradication (missing one C2 or one cloud role) = re-compromise within days.
- Rotate *all* credentials the attacker could have touched, not just the obvious one.

## Verify success
The adversary is fully evicted (no persistence, all exposed creds rotated), systems restored from a
trusted baseline, a timeline + root cause are documented, and a new detection covers the entry path.

## References
NIST SP 800-61r2; SANS PICERL; the `defense-dfir-triage` and `defense-detection-engineering` skills.
