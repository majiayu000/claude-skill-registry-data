---
name: network-ntlm-relay
description: >
  Coerce and relay NTLM authentication for lateral movement and privilege escalation (relay to SMB,
  LDAP, ADCS). Load in an AD network with a foothold, on "NTLM relay", "responder", "coerce",
  no/absent SMB signing, or PetitPotam/PrinterBug. Signals: LLMNR/NBT-NS traffic, SMB signing off, MS-RPRN/EFSRPC.
domain: network
type: technique
stability: learning
modes: [pentest]
severity: critical
mitre: [T1557.001, T1187]
cwe: [CWE-294, CWE-290]
tools: [responder, ntlmrelayx, coercer, petitpotam]
schema_version: 1
---

# NTLM coercion & relay

## When it applies
You're on an AD network (unauthenticated or with a foothold) and want to move laterally or escalate
without cracking passwords. If SMB signing isn't enforced (or you target LDAP/ADCS), you can relay
a victim's NTLM authentication to a service and act as them.

## Why it works
NTLM authentication isn't bound to the channel: if you can make a machine/user authenticate to *you*
(coercion or poisoning), you forward that authentication to another service. Without signing
(SMB) or channel binding (LDAP/HTTP), the target accepts it, and you get access as the coerced identity —
often a computer account with local admin elsewhere, or a DC to ADCS.

## Method
1. **Get victims to authenticate to you**:
   - **Poisoning**: `responder -I eth0` answers LLMNR/NBT-NS/mDNS for mistyped names → captures/relays auth.
   - **Coercion**: force a specific machine (esp. a DC) to auth to you — `coercer`, `PetitPotam`
     (MS-EFSRPC), PrinterBug (MS-RPRN), `dfscoerce`.
2. **Find relay targets**: hosts with **SMB signing not required** (`nxc smb <range> --gen-relay-list`),
   or LDAP/LDAPS on DCs, or the ADCS web enrollment endpoint.
3. **Relay**: `impacket-ntlmrelayx -tf targets.txt -smb2support` (SMB), `-t ldaps://DC` (LDAP — e.g.
   grant RBCD or DCSync), or `-t http://CA/certsrv/certfnsh.asp --adcs` (**ESC8** → cert for a DC → DA,
   chain with `ad-adcs`).
4. **Escalate**: relayed to LDAP → set **RBCD** on a computer you control → impersonate DA on it;
   relayed to ADCS → auth as the DC.

## Gotchas
- Turn off Responder's SMB/HTTP servers when using ntlmrelayx (port conflict).
- SMB signing **required** blocks SMB relay — pivot to LDAP/ADCS relay instead.
- Coercing a DC + ADCS ESC8 is the reliable domain-takeover combo; PetitPotam often works unauthenticated.

## Verify success
Access/action as the relayed identity — a session/command on a target host, RBCD set, a cert issued
for a DC, or hashes dumped — demonstrating relay-based movement/escalation.

## References
impacket ntlmrelayx; SpecterOps relay research; PetitPotam/Coercer; "Certified Pre-Owned" (ESC8).
