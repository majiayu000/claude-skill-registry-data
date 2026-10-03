---
name: net-lateral
description: "Net Lateral."
domain: cybersecurity
---

--|
| **Lateral Movement** | Post-compromise technique where attackers pivot between systems to reach targets |
| **Pass-the-Hash** | Using stolen NTLM hash for authentication without knowing the plaintext password |
| **Pass-the-Ticket** | Using stolen Kerberos TGT/TGS tickets for authentication across the domain |
| **PsExec** | Sysinternals tool (and attack technique) for remote process execution via SMB and named pipes |
| **WMI Execution** | Using Windows Management Instrumentation for remote command execution via DCOM or WinRM |
| **Admin Share** | Default Windows administrative shares (C$, ADMIN$, IPC$) used for remote system management |

## Tools & Systems

- **Splunk Enterprise Security**: SIEM platform for correlating Windows events, Sysmon, and network flows
- **Microsoft Defender for Identity**: Cloud service detecting lateral movement via domain controller monitoring
- **BloodHound**: Active Directory attack path analysis tool for identifying lateral movement opportunities
- **CrowdStrike Falcon**: EDR platform with lateral movement detection and automated containment
- **Zeek (Bro)**: Network monitor generating connection logs for SMB, RDP, and WinRM traffic analysis

## Common Scenarios

- **PsExec Spread**: Attacker uses PsExec to execute malware across 20 workstations — detect via service creation events
- **RDP Pivoting**: Compromised VPN account used to RDP through multiple internal hosts — detect via Logon_Type 10 chains
- **WMI Recon and Execution**: Attacker uses WMI for discovery then execution — detect via WmiPrvSE child processes
- **Pass-the-Hash Campaign**: Stolen local admin hash used across subnet — detect via NTLM Logon_Type 3 to multiple hosts
- **Scheduled Task Persistence**: Remote scheduled task created on domain controller — detect via EventCode 4698 from non-admin source

## Output Format

```
LATERAL MOVEMENT DETECTION REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Period:       2024-03-15 14:00 to 18:00 UTC
Source:       192.168.1.105 (WORKSTATION-042)

Movement Path:
  14:23  192.168.1.105 → 10.0.5.20  (DC-PRIMARY) — PtH via NTLM Type 3
  14:25  10.0.5.20 → 10.0.5.21     (DC-BACKUP)  — Kerberos ticket reuse
  14:28  10.0.5.20 → 10.0.10.15    (FILESERVER-01) — PsExec service creation
  14:32  10.0.10.15 → 10.0.10.20   (DB-PRIMARY) — WMI remote execution
  14:35  10.0.10.20 → 10.0.10.25   (DB-BACKUP)  — SMB admin share access

Techniques Detected:
  T1550.002 — Pass-the-Hash (NTLM authentication to DC)
  T1021.002 — PsExec (remote service installation)
  T1047     — WMI Execution (WmiPrvSE child process)
  T1021.002 — SMB Admin Share (C$ access on DB-BACKUP)

Affected Systems: 5 hosts across 2 network segments
User Account:     admin_compromised (Domain Admin)
Containment:      All 5 hosts isolated at 14:45 UTC
```
