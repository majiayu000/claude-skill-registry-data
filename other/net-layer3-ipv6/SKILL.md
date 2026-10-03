---
name: net-layer3-ipv6
description: "--| | mitm6 DNS Takeover | SUCCESS | Became IPv6 DNS for 147 hosts | | WPAD NTLM Relay | SUCCESS | Captured 23 NTLM authentications | | Domain Admin Relay | SUCCESS | Created rogue domain admin account | | IPv6 Port Scan | SUCCESS | All ports open (no ip6tables rules) |  ### Recommendations 1."
domain: cybersecurity
---

--|
| mitm6 DNS Takeover | SUCCESS | Became IPv6 DNS for 147 hosts |
| WPAD NTLM Relay | SUCCESS | Captured 23 NTLM authentications |
| Domain Admin Relay | SUCCESS | Created rogue domain admin account |
| IPv6 Port Scan | SUCCESS | All ports open (no ip6tables rules) |

### Recommendations
1. Deploy RA Guard on all access-layer switches (Critical)
2. Configure IPv6 ACLs mirroring IPv4 firewall rules (Critical)
3. Disable DHCPv6 client via Group Policy where IPv6 is not needed
4. Block IPv6 tunneling protocols (6to4, Teredo) at the firewall
5. Deploy IPv6-aware IDS rules for NDP spoofing detection
```
