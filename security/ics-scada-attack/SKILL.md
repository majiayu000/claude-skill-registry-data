---
name: ics-scada-attack
description: "Ics Ics Scada Attack."
domain: cybersecurity
---

|
| SCADA | Supervisory Control and Data Acquisition - architecture for remote monitoring and control of industrial processes via RTUs and communication infrastructure |
| IDS/IPS for OT | Intrusion Detection/Prevention Systems designed for industrial protocols, using both signature-based and anomaly-based detection methods |
| Process Anomaly | Deviation in physical process behavior (temperature, pressure, flow) that may indicate cyber manipulation of control systems |
| Man-in-the-Middle (MITM) | Attack intercepting communication between SCADA master and field devices to modify commands or spoof sensor readings |
| Replay Attack | Capturing legitimate SCADA traffic and replaying it to mask malicious changes to the process (used by Stuxnet) |
| Protocol Anomaly | Deviation from expected industrial protocol behavior including unauthorized function codes, unusual polling patterns, or command sequences |

## Tools & Systems

- **Dragos Platform**: OT cybersecurity platform with threat detection powered by Dragos threat intelligence on ICS-targeting activity groups
- **Nozomi Networks Guardian**: OT/IoT visibility and threat detection using asset intelligence, anomaly detection, and vulnerability assessment
- **Claroty xDome**: Cyber-physical systems protection with continuous threat monitoring and alert prioritization
- **Suricata with ET Open ICS rules**: Open-source IDS/IPS with community-maintained rules for industrial protocol detection
- **Zeek (Bro) with OT scripts**: Network security monitor with protocol analyzers for Modbus, DNP3, and BACnet

## Common Scenarios

### Scenario: Detecting TRITON-Style Attack on Safety Systems

**Context**: An OT security monitoring system alerts on unusual TriStation protocol traffic to a Triconex safety controller from an IP address that is not the authorized SIS engineering workstation.

**Approach**:
1. Immediately verify the source IP of the TriStation traffic - is it the authorized SIS engineering workstation or a compromised host?
2. Check if there is an authorized maintenance activity scheduled for the SIS controllers
3. Capture full packet payload of the TriStation communication for forensic analysis
4. Alert the process safety team - SIS compromise is a safety-critical event
5. If unauthorized, isolate the source host from the network immediately
6. Verify SIS controller logic integrity by comparing running logic against known-good backup
7. Check all engineering workstations in the facility for TRITON indicators (trilog.exe, inject.bin)

**Pitfalls**: Never assume SIS traffic anomalies are false positives - TRITON demonstrated that sophisticated attackers specifically target safety systems. Do not restart the SIS controller without first verifying firmware and logic integrity. Avoid alerting only the IT SOC; the process safety team must be immediately engaged for any SIS-related incident.

## Output Format

```
SCADA Attack Detection Report
===============================
Detection Time: YYYY-MM-DD HH:MM:SS UTC
Detection Source: [IDS/Anomaly Detector/Process Monitor]

ALERT DETAILS:
  Alert ID: [unique identifier]
  Severity: Critical/High/Medium/Low
  Attack Category: [Protocol Anomaly/Process Manipulation/Unauthorized Access]
  MITRE ATT&CK for ICS: [Technique ID and name]

  Source: [IP/hostname]
  Target: [IP/hostname - device type]
  Protocol: [Modbus/DNP3/S7comm/etc]
  Detail: [Specific finding description]

BASELINE COMPARISON:
  Normal: [Expected behavior]
  Observed: [Actual behavior that triggered alert]
  Deviation: [How the observed differs from baseline]

RECOMMENDED RESPONSE:
  1. [Immediate containment action]
  2. [Verification step]
  3. [Escalation path]
```
