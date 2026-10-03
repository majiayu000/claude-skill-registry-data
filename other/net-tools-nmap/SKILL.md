---
name: net-tools-nmap
description: "| | 10.10.5.23 | 445/tcp | SMB | Windows Server 2012 R2 | MS17-010 (EternalBlue) | | 10."
domain: cybersecurity
---

|
| 10.10.5.23 | 445/tcp | SMB | Windows Server 2012 R2 | MS17-010 (EternalBlue) |
| 10.10.8.100 | 443/tcp | Apache httpd | 2.4.29 | CVE-2021-41773 (Path Traversal) |
| 10.10.12.5 | 3306/tcp | MySQL | 5.6.24 | CVE-2016-6662 (RCE) |
| 10.10.3.77 | 161/udp | SNMP | v2c | Public community string |

### Recommendations
1. Patch MS17-010 on 10.10.5.23 immediately -- Critical RCE vulnerability
2. Upgrade Apache httpd to 2.4.58+ on 10.10.8.100
3. Upgrade MySQL to 8.0.x on 10.10.12.5 and restrict bind address
4. Change SNMP community strings from "public" on 10.10.3.77
```
