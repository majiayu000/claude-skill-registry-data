---
name: soc-tools-qradar
description: "Soc Tools Qradar."
domain: cybersecurity
---

--|
| **AQL** | Ariel Query Language — QRadar's SQL-like query language for searching events, flows, and offenses |
| **Offense** | QRadar's correlated incident grouping multiple events/flows under a single investigation unit |
| **Building Block** | Reusable rule component that categorizes events without generating offenses, used as input to correlation rules |
| **Magnitude** | QRadar's calculated offense severity combining relevance, severity, and credibility scores (1-10) |
| **Reference Set** | Dynamic lookup table in QRadar for whitelists, watchlists, and enrichment data used in rules |
| **QID** | QRadar Identifier — unique numeric ID mapping vendor-specific events to normalized categories |
| **Coalescing** | QRadar's mechanism for grouping related events into a single offense to reduce analyst workload |

## Tools & Systems

- **IBM QRadar SIEM**: Enterprise SIEM platform with event correlation, offense management, and AQL query engine
- **QRadar Pulse**: Dashboard framework for building custom visualizations of offense and event metrics
- **QRadar API**: RESTful API for automating reference set management, offense operations, and rule deployment
- **QRadar Use Case Manager**: App for mapping detection rules to MITRE ATT&CK framework coverage
- **QRadar Assistant**: AI-powered analysis tool helping analysts investigate offenses with natural language

## Common Scenarios

- **Brute Force to Compromise**: Correlate failed auth events with subsequent successful login from same source
- **Lateral Movement Chain**: Track authentication events across multiple internal hosts from a single source
- **C2 Beaconing**: Correlate periodic DNS queries with low-entropy payloads to unusual domains
- **Privilege Escalation**: Correlate user account changes (group additions) with prior suspicious authentication
- **Data Exfiltration**: Correlate large outbound flow volumes with prior internal reconnaissance activity

## Output Format

```
QRADAR OFFENSE INVESTIGATION — Offense #12345
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Offense Type:   Brute Force with Subsequent Access
Magnitude:      8/10 (Severity: 8, Relevance: 9, Credibility: 7)
Created:        2024-03-15 14:23:07 UTC
Contributing:   247 events from 3 log sources

Correlation Chain:
  14:10-14:22  — 234 Authentication Failures (EventCode 4625) from 192.168.1.105 to DC-01
  14:23:07     — Authentication Success (EventCode 4624) from 192.168.1.105 to DC-01 (user: admin)
  14:25:33     — New Process: cmd.exe spawned by admin on DC-01
  14:26:01     — Net.exe user /add detected on DC-01

Sources Correlated:
  Windows Security Logs (DC-01)
  Sysmon (DC-01)
  Firewall (Palo Alto PA-5260)

Disposition:    TRUE POSITIVE — Escalated to Incident Response
Ticket:         IR-2024-0432
```
