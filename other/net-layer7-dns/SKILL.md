---
name: net-layer7-dns
description: "Net Layer7 Dns."
domain: cybersecurity
---

--|
| **DNS Tunneling** | Technique encoding data within DNS queries/responses to exfiltrate data or establish C2 channels through DNS |
| **DGA** | Domain Generation Algorithm — malware technique generating pseudo-random domain names for C2 resilience |
| **Shannon Entropy** | Mathematical measure of randomness in a string — high entropy (>3.5) in domain names indicates DGA or tunneling |
| **TXT Record Abuse** | Using DNS TXT records (designed for text data) as a high-bandwidth channel for data tunneling |
| **DNS over HTTPS (DoH)** | DNS queries encrypted over HTTPS (port 443), bypassing traditional DNS monitoring |
| **Passive DNS** | Historical record of DNS resolutions showing which IPs a domain resolved to over time |

## Tools & Systems

- **Splunk Stream**: Network traffic capture add-on providing parsed DNS query data for SIEM analysis
- **Zeek (Bro)**: Network security monitor generating detailed DNS transaction logs for analysis
- **Cisco Umbrella (OpenDNS)**: Cloud DNS security platform blocking malicious domains and logging query data
- **Infoblox DNS Firewall**: DNS-layer security providing RPZ-based blocking and detailed query logging
- **Farsight DNSDB**: Passive DNS database for historical domain resolution lookups and infrastructure mapping

## Common Scenarios

- **Cobalt Strike DNS Beacon**: Detect periodic TXT queries with encoded payloads to C2 domain
- **Data Exfiltration**: Large volumes of unique subdomain queries encoding stolen data in Base64/hex
- **DGA Malware**: Detect DNS queries to algorithmically generated domains (high entropy, no web content)
- **DNS-over-HTTPS Bypass**: Employee using DoH to bypass corporate DNS filtering and monitoring
- **Slow Drip Exfiltration**: Low-volume DNS tunneling staying below threshold alerts (requires baseline comparison)

## Output Format

```
DNS EXFILTRATION ANALYSIS — WORKSTATION-042
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Period:       2024-03-14 to 2024-03-15
Source:       192.168.1.105 (WORKSTATION-042, Finance Dept)

Findings:
  [CRITICAL] DNS tunneling detected to evil-tunnel[.]com
    Query Volume:       12,847 queries in 18 hours
    Avg Subdomain Len:  63 characters (normal: <20)
    Avg Entropy:        3.82 (threshold: 3.5)
    Query Types:        TXT (89%), A (11%)
    Estimated Data:     ~4.7 MB exfiltrated via DNS
    Rate:               0.58 kbps (slow drip pattern)

  [HIGH] DGA-like domains resolved
    Unique DGA Domains: 247 domains resolved
    Pattern:            15-char random alphanumeric.xyz TLD
    Entropy Range:      3.6 - 4.1

Process Attribution:
  Process:   svchost_update.exe (masquerading — not legitimate svchost)
  PID:       4892
  Parent:    explorer.exe
  Hash:      SHA256: a1b2c3d4... (VT: 34/72 malicious — Cobalt Strike beacon)

Containment:
  [DONE] Host isolated via EDR
  [DONE] Domain evil-tunnel[.]com added to DNS sinkhole
  [DONE] Incident IR-2024-0448 created
```
