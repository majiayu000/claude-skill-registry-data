---
name: ics-net-firewall
description: "Ics Ics Net Firewall."
domain: cybersecurity
---

|
| Tofino Xenon | Belden/Hirschmann industrial firewall appliance with deep packet inspection for OT protocols |
| Deep Packet Inspection (DPI) | Examining message payload content beyond headers to enforce fine-grained rules on industrial protocol operations |
| Inline Bridge Mode | Transparent deployment mode where the firewall sits between network segments without requiring IP changes |
| Fail-Open | Safety mode where firewall passes all traffic if the appliance fails, maintaining process availability |
| Loadable Security Module (LSM) | Tofino plugin module providing protocol-specific DPI for Modbus, EtherNet/IP, OPC, or other protocols |
| Central Management Platform (CMP) | Tofino centralized management server for deploying and managing policies across multiple Tofino appliances |

## Output Format

```
TOFINO DEPLOYMENT REPORT
===========================
Date: YYYY-MM-DD
Appliances Deployed: [count]

PER-APPLIANCE SUMMARY:
  [Appliance ID]:
    Mode: Inline Bridge
    Failsafe: Fail-Open
    Protected Assets: [count]
    Rules: [count]
    DPI Protocols: [list]

RULE SUMMARY:
  Allow Rules: [count]
  Deny Rules: [count]
  DPI-Enforced Rules: [count]

MONITORING:
  Blocked Packets (24h): [count]
  DPI Violations (24h): [count]
```
