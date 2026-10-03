---
name: soc-hunting-ntlm
description: "Soc Hunting Ntlm."
domain: cybersecurity
---

|
| **Splunk / Elastic SIEM** | Log aggregation and correlation for Event 4624 analysis, IP-hostname mismatch detection, and NTLM downgrade monitoring |
| **Microsoft Sentinel** | Cloud SIEM with KQL queries for NTLM relay detection and built-in analytics rules for PetitPotam |
| **CrowdStrike Falcon Identity Protection** | Detects NTLM relay attacks against domain controller accounts regardless of coercion method used |
| **Responder** | LLMNR/NBT-NS/mDNS poisoning tool used by attackers -- understanding its behavior is essential for detection |
| **ntlmrelayx (Impacket)** | Multi-protocol NTLM relay tool developed by Fox-IT -- used in testing and by adversaries |
| **PingCastle** | Active Directory security assessment tool that audits SMB signing, LDAP signing, and NTLM configuration |
| **Zeek** | Network security monitor for capturing SMB signing negotiation, LLMNR traffic, and DCE-RPC activity |
| **Sigma** | Vendor-agnostic detection rule format for portable NTLM relay detection rules |

## Common Scenarios

### Scenario 1: Responder Poisoning with NTLM Relay to File Server

**Context**: A SOC analyst observes multiple Event 4624 LogonType 3 entries on a file server (10.10.20.100) where the WorkstationName field shows different workstation names but the IpAddress field consistently shows 10.10.5.50, a host not in the IT asset inventory.

**Approach**:
1. Query Event 4624 on 10.10.20.100 filtered for IpAddress=10.10.5.50: find 15 successful NTLM logons in 30 minutes from 8 different user accounts
2. Cross-reference 10.10.5.50 with DHCP logs and DNS: host is not a registered domain member, MAC address shows a Linux-based NIC
3. Query Zeek network logs for 10.10.5.50: identify LLMNR responses (UDP 5355) to multiple workstations and SMB connections to 10.10.20.100
4. Confirm IP-hostname mismatch: WorkstationName values (WS-FINANCE01, WS-HR03, etc.) all resolve to different IPs in DNS, not 10.10.5.50
5. Check SMB signing on 10.10.20.100: RequireSecuritySignature is False, enabling the relay attack
6. Contain: block 10.10.5.50 at the switch, force password reset for all 8 affected accounts, enable SMB signing on the file server
7. Remediate: disable LLMNR and NBT-NS via GPO, enforce SMB signing domain-wide

**Pitfalls**:
- Dismissing the multiple logons as normal network activity without checking the IP-hostname correlation
- Not checking SMB signing status on the target server to understand why the relay succeeded
- Only resetting the password for one user instead of all accounts that were relayed

### Scenario 2: PetitPotam Relay to AD Certificate Services

**Context**: During a threat hunt, an analyst finds Event 4624 LogonType 3 on the AD CS server (ADCS01) showing the domain controller machine account (DC01$) authenticating via NTLM from IP 10.10.5.50, which is not the DC's IP address (10.10.1.10).

**Approach**:
1. Confirm the anomaly: DC01$ should only authenticate from 10.10.1.10, but Event 4624 shows authentication from 10.10.5.50 via NTLM (not Kerberos)
2. Check for certificate enrollment: query AD CS logs for certificate requests from DC01$ around the same timestamp -- find a certificate issued for DC01$
3. Identify the attack: PetitPotam coerced DC01 to authenticate to 10.10.5.50, which relayed the authentication to ADCS01 to request a certificate for DC01$
4. Assess impact: with a DC certificate, the attacker can authenticate as DC01$ and perform DCSync to extract all domain credentials
5. Revoke the fraudulently issued certificate immediately
6. Check for DCSync activity: query Event 4662 for directory replication from non-DC sources
7. Contain: isolate 10.10.5.50, revoke certificate, patch EFS (MS-EFSRPC), enforce EPA on AD CS, require LDAP signing on all DCs

**Pitfalls**:
- Not recognizing that machine account NTLM authentication from an unexpected IP is a critical indicator of coercion + relay
- Failing to check AD CS for fraudulent certificate issuance, which represents the actual objective of the attack
- Not auditing LDAP signing and EPA on AD CS servers, which would have prevented the relay

## Output Format

```
Hunt ID: TH-NTLM-RELAY-[DATE]-[SEQ]
Alert Severity: Critical
MITRE Technique: T1557.001 (LLMNR/NBT-NS Poisoning and SMB Relay)

Relay Indicators:
  Victim Account: [Domain\Username or Machine$]
  WorkstationName: [Victim hostname from Event 4624]
  Expected Source IP: [IP matching WorkstationName in DNS/DHCP]
  Actual Source IP: [Attacker/relay IP from Event 4624 IpAddress field]
  Target Host: [Server receiving the relayed authentication]

Authentication Details:
  Event ID: 4624
  LogonType: 3 (Network)
  AuthenticationPackage: NTLM
  LmPackageName: [NTLM V1 or NTLM V2]
  LogonProcess: [NtLmSsp]
  Timestamp: [Event time]

Signing Status:
  Target SMB Signing: [Required/Not Required]
  Target LDAP Signing: [Required/Not Required]
  LDAP Channel Binding: [Required/Not Required]

Poisoning Evidence:
  LLMNR Activity: [Detected/Not Detected from relay IP]
  NBT-NS Activity: [Detected/Not Detected from relay IP]
  Coercion Method: [PetitPotam/DFSCoerce/PrinterBug/Unknown]

Risk Assessment: [Critical - relay from DC / High - relay from user account]
Recommended Actions:
  - Immediate: [Block relay IP, reset affected credentials]
  - Short-term: [Enable SMB/LDAP signing, disable LLMNR/NBT-NS]
  - Long-term: [Migrate to Kerberos, enforce EPA, restrict NTLM via GPO]
```
