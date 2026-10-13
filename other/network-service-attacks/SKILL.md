---
name: network-service-attacks
description: >
  Attack non-web network services surfaced by recon. Load when nmap shows services like SMB
  (445), RPC (135), LDAP (389), SNMP (161), NFS (2049), SMTP (25), FTP (21), RDP (3389),
  databases (3306/5432/1433/6379/27017). Signals: open non-HTTP ports, service+version banners.
domain: network
type: technique
stability: learning
modes: [pentest]
severity: high
mitre: [T1210, T1046]
tools: [netexec, enum4linux-ng, smbclient, snmpwalk, showmount, nmap]
schema_version: 1
---

# Network service enumeration & attack

## When it applies
Recon exposed non-web services. Each is its own attack surface: anonymous access, default/weak
creds, known-CVE versions, and info leaks that feed the next step. (See `recon-arsenal` for the
discovery arsenal; this is the exploit routing per service.)

## Why it works
Internal-style services are frequently deployed with defaults, anonymous binds, or no auth
because they were "not meant to be exposed". Version banners map straight to public exploits.

## Method
1. **Always version-map first** — the exact product+version is the fastest lead (`nmap -sCV`).
2. **Route by service**:
   - **SMB (445)**: `nxc smb <ip> -u '' -p ''` (null session), `enum4linux-ng`, list shares
     (`smbclient -L //ip -N`), check for `EternalBlue`/signing; spray creds with netexec.
   - **LDAP (389/636)**: anonymous bind dump (`ldapsearch -x -H ldap://ip -b <base>`) → users.
   - **SNMP (161)**: `snmpwalk -v2c -c public ip` — leaks processes, users, routes, sometimes creds.
   - **NFS (2049)**: `showmount -e ip`; mount world-readable exports, check `no_root_squash`.
   - **SMTP (25)**: `VRFY`/`RCPT` user enumeration.
   - **DBs**: try default creds; Redis (6379) often unauth (→ `web-ssrf-gopher-redis-rce` if internal).
3. **Map version → CVE**: `searchsploit <product version>`; verify before firing.

## Gotchas
- Null/anonymous first — it's free and frequently works before any exploit.
- SNMP community `public`/`private` and defaults are the quiet win people skip.
- Confirm a CVE actually matches the exact version; wrong minor version = wasted exploit.

## Verify success
Access or credentials from a service (share contents, LDAP users, a DB login), or confirmed
exploitation of a versioned CVE — feeding foothold/privesc.

## References
Service-enum references (HackTricks, 0xdf); netexec wiki; GTFOBins/searchsploit.
