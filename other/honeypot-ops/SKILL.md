---
name: honeypot-ops
description: Use when deploying and operating honeypots for detection
  and intelligence on your own network. Covers honeypot types,
  deployment safety, alert tuning, and turning captures into
  detections. Also use when you want early warning of lateral
  movement or internet scanning.
version: 1.0.0
domain: soc
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [threat-hunting, siem-detections, suricata-ids]
tools:
  - name: Python
    version: "3.12"
---

Honeypots are systems with no legitimate users: anyone who touches
them is suspicious by definition. This skill covers running them
safely on your own network: choosing the type, deploying without
creating risk, tuning the alerts, and converting what you catch into
real detections. Deploy only on networks you own or are authorized
to defend.

## Quick Workflow

1. Define the goal: early warning, intel collection, or deception
   for a specific threat.
2. Choose the type: low interaction (fake services) or high
   interaction (real systems, isolated).
3. Deploy safely: isolated VLAN, no route to production, resource
   limits, and monitoring of the honeypot itself.
4. Seed believable content: fake credentials, files, and services
   that attract the right attention.
5. Tune alerts: every touch is an alert, but prioritize by behavior.
6. Collect and analyze: payloads, credentials tried, and TTPs.
7. Convert to detections: the attacker's tools become your rules.
8. Maintain: refresh content, patch the honeypot, and review
   placement.

## 1. Safe deployment

```bash
# Deployment checklist (your network, isolated segment):
# - dedicated VLAN with no route to production or the internet out
# - firewall: allow inbound to honeypot, deny honeypot-initiated out
# - resource limits so it cannot be used for mining or DDoS
# - logging shipped off the box in real time
# - documented owner and decommission date
echo "a honeypot that can attack others is a liability, not a sensor"
```

```bash
# Low interaction example: fake SSH that logs attempts (cowrie style)
# - record: source IP, credentials tried, commands typed
# - alert: any successful login (should be impossible with fake creds)
# High interaction: real VM, snapshot before, revert after each compromise
```

## 2. From capture to detection

```python
#!/usr/bin/env python3
"""Honeypot intel to detection ideas."""
captures = [
    ("ssh brute force", "user list", "blocklist + alert on user enum"),
    ("new malware hash", "sha256", "hunt hash across the fleet"),
    ("novel exploit attempt", "payload", "write sigma rule, test in lab"),
]
for what, artifact, action in captures:
    print(f"captured {what} ({artifact}) -> {action}")
```

## Edge cases

- Attackers fingerprint the honeypot and avoid it. Refresh banners
  and content; perfect realism is not required for tripwire value.
- The honeypot is compromised and used for outbound attacks. The
  egress deny rule is what saves you; verify it regularly.
- Alert fatigue from internet background noise. Tune: alert on
  interaction depth, not just port knocks.

## Escalation

- Honeypot shows targeted TTPs (not spray and pray): escalate to
  threat hunting; someone is interested in you specifically.
- Compromise of a high interaction host: treat as an incident on
  the isolated segment and rebuild from snapshot.

## Detection and defender view

Honeypots are detection, not prevention: their alerts are high
fidelity because false positives are rare. Attackers evade them by
avoiding obviously fake systems, so placement matters more than
realism: put them where lateral movement must pass. The durable
value is the intel loop: what touches the honeypot today becomes
the detection for the whole network tomorrow.

## Key references

- MITRE ATT&CK T1598 (Phishing for Information): honeypot adjacent.
- Honeypot deployment safety literature.
- Related skills: threat-hunting, siem-detections.
