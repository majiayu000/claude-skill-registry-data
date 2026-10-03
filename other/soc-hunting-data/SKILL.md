---
name: soc-hunting-data
description: "Soc Hunting Data."
domain: cybersecurity
---

|
| Splunk | SIEM for data volume analysis and SPL queries |
| Zeek | Network metadata for data flow analysis |
| Microsoft Defender for Cloud Apps | CASB for cloud exfiltration |
| Netskope | Cloud DLP and exfiltration detection |
| Suricata | Network IDS for protocol anomaly detection |
| RITA | DNS exfiltration and beacon detection |
| ExtraHop | Network traffic analysis for data flow |

## Common Scenarios

1. **Cloud Storage Exfiltration**: User uploads sensitive documents to personal Google Drive or Dropbox via browser.
2. **DNS Tunneling**: Malware exfiltrates data encoded in DNS subdomain queries to attacker-controlled nameserver.
3. **HTTPS Upload**: Compromised system POSTs large data blobs to C2 server over encrypted HTTPS.
4. **Email Attachment Exfiltration**: Insider forwards sensitive documents to personal email accounts.
5. **Staging and Compression**: Adversary stages data in compressed archives before slow exfiltration to avoid detection.

## Output Format

```
Hunt ID: TH-EXFIL-[DATE]-[SEQ]
Exfiltration Channel: [HTTP/DNS/Email/Cloud/USB]
Source: [Host/User]
Destination: [Domain/IP/Service]
Data Volume: [Bytes/MB/GB]
Time Period: [Start - End]
Protocol: [HTTPS/DNS/SMTP/SMB]
Files Involved: [Count/Types]
Risk Level: [Critical/High/Medium/Low]
Confidence: [High/Medium/Low]
```
