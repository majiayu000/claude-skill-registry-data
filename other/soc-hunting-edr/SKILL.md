---
name: soc-hunting-edr
description: "-| | T1003.001 | LSASS Memory -- dumping credentials from LSASS process | | T1003."
domain: cybersecurity
---

-|
| T1003.001 | LSASS Memory -- dumping credentials from LSASS process |
| T1003.002 | Security Account Manager -- extracting local account hashes from SAM |
| T1003.003 | NTDS -- extracting domain hashes from Active Directory database |
| T1003.004 | LSA Secrets -- extracting service account passwords |
| T1003.005 | Cached Domain Credentials -- extracting DCC2 hashes |
| T1003.006 | DCSync -- replicating credentials from domain controller |
| Credential Guard | Virtualization-based isolation of LSASS secrets |
| RunAsPPL | Protected Process Light for LSASS |

## Detection Queries

### Splunk -- LSASS Access Detection
```spl
index=sysmon EventCode=10
| where match(TargetImage, "(?i)lsass\.exe$")
| where GrantedAccess IN ("0x1FFFFF", "0x1F3FFF", "0x143A", "0x1F0FFF", "0x0040", "0x1010", "0x1410")
| where NOT match(SourceImage, "(?i)(csrss|lsass|svchost|MsMpEng|WmiPrvSE|taskmgr|procexp|SecurityHealthService)\.exe$")
| table _time Computer SourceImage SourceProcessId GrantedAccess CallTrace
```

### Splunk -- Credential Dumping Tool Detection
```spl
index=sysmon EventCode=1
| where match(CommandLine, "(?i)(sekurlsa|lsadump|kerberos::list|crypto::certificates)")
    OR match(CommandLine, "(?i)procdump.*-ma.*lsass")
    OR match(CommandLine, "(?i)comsvcs\.dll.*MiniDump")
    OR match(CommandLine, "(?i)ntdsutil.*\"ac i ntds\".*ifm")
    OR match(CommandLine, "(?i)reg\s+save\s+hklm\\\\(sam|security|system)")
    OR match(CommandLine, "(?i)vssadmin.*create\s+shadow")
| table _time Computer User Image CommandLine ParentImage
```

### KQL -- Microsoft Defender for Endpoint
```kql
DeviceEvents
| where Timestamp > ago(7d)
| where ActionType in ("LsassAccess", "CredentialDumpingActivity")
| project Timestamp, DeviceName, AccountName, InitiatingProcessFileName,
    InitiatingProcessCommandLine, ActionType, AdditionalFields
| sort by Timestamp desc
```

### Sigma Rule -- LSASS Credential Dumping
```yaml
title: LSASS Memory Credential Dumping Attempt
status: stable
logsource:
    product: windows
    category: process_access
detection:
    selection:
        TargetImage|endswith: '\lsass.exe'
        GrantedAccess|contains:
            - '0x1FFFFF'
            - '0x1F3FFF'
            - '0x143A'
            - '0x0040'
    filter:
        SourceImage|endswith:
            - '\csrss.exe'
            - '\lsass.exe'
            - '\MsMpEng.exe'
            - '\svchost.exe'
    condition: selection and not filter
level: critical
tags:
    - attack.credential_access
    - attack.t1003.001
```

## Common Scenarios

1. **Mimikatz sekurlsa**: Direct LSASS memory reading via `sekurlsa::logonpasswords` to extract plaintext passwords, NTLM hashes, and Kerberos tickets.
2. **ProcDump LSASS**: `procdump.exe -ma lsass.exe lsass.dmp` creating a memory dump for offline credential extraction.
3. **Comsvcs.dll MiniDump**: `rundll32.exe comsvcs.dll MiniDump [LSASS_PID] dump.bin full` using a built-in Windows DLL for LSASS dumping.
4. **NTDS.dit Extraction**: Creating a Volume Shadow Copy and copying NTDS.dit + SYSTEM hive for offline domain hash extraction with secretsdump.
5. **SAM Hive Export**: `reg save HKLM\SAM sam.save` followed by `reg save HKLM\SYSTEM system.save` for local account hash extraction.
6. **Task Manager Dump**: Right-clicking LSASS in Task Manager to create a memory dump -- a legitimate tool abused for credential theft.

## Output Format

```
Hunt ID: TH-CRED-[DATE]-[SEQ]
Host: [Hostname]
Dumping Method: [LSASS_Access/NTDS/SAM/DCSync]
Source Process: [Tool or process used]
Target: [LSASS/NTDS.dit/SAM/SECURITY]
Access Rights: [Granted access mask]
User Context: [Account performing the dump]
ATT&CK Technique: [T1003.00x]
Risk Level: [Critical/High/Medium]
Credentials at Risk: [Scope assessment]
```
