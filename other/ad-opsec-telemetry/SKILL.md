---
name: ad-opsec-telemetry
description: >
  The telemetry each Active Directory technique generates and what alerts a defender:
  Kerberoasting produces Event 4769 with RC4 encryption (0x17) and an MDI alert, DCSync
  produces Event 4662 with the DS-Replication-Get-Changes GUID, AS-REP roasting produces
  Event 4768 with no pre-auth, LSASS dumping is blocked by EDR, plus a lateral-movement
  telemetry table by protocol (SMB/WMI/WinRM/RDP/DCOM). Use this whenever you run or plan an
  offensive AD technique and need to know what noise it makes, when writing the engagement's
  detection notes, or when a defender wants to know what to monitor. Teaches red teamers
  what is loud and blue teamers what to watch. Standard-tooling knowledge, no vendor engine.
---

# AD OPSEC and Telemetry

Every technique leaves a trace. The goal here is not evasion. It is knowing the noise
profile of each action so you can document it for the client before the engagement, pick
the quieter of two functionally equivalent techniques, and correlate what you did with what
their SOC saw. For a defender, read the same tables backwards: they are the events to
monitor and alert on.

Two rules of engagement throughout:

- **Document the noise.** Tell the client what each high-signal action generated, with the
  event ID and the source IP, so they can find it in their logs.
- **Coordinate the loud ones.** DCSync, mass spraying, coercion at scale, and LSASS dumps
  need explicit client sign-off or an end-of-engagement window when detection no longer
  matters.

Microsoft Defender for Identity (MDI) is the sensor that matters most in AD; it reads DC
traffic directly and ships tuned detections for most of what follows.

---

## Kerberoasting: Event 4769, RC4 (0x17)

Requesting service tickets for accounts with SPNs, to crack offline.

- **Event 4769** (Kerberos service ticket requested) fires for each SPN targeted. The tell
  is `Ticket Encryption Type = 0x17 (RC4-HMAC)`. Attackers request RC4 because the
  resulting hash cracks fastest, but a service that normally uses AES suddenly requested
  with RC4 is the classic signature.
- **MDI**: "Suspected Kerberoasting attack" is on by default and triggers on the volume and
  RC4 pattern.
- Requesting all SPNs at once amplifies the signal. Targeting one high-value account is far
  quieter than roasting the whole domain.

```bash
GetUserSPNs.py corp.local/user:pass -dc-ip <dc_ip> -request -outputfile roast.txt
```

- **MITRE**: T1558.003 (Steal or Forge Kerberos Tickets: Kerberoasting).
- **Defender watch**: 4769 with 0x17 for accounts that otherwise use AES; a single principal
  requesting many distinct SPN tickets in a short window.
- **Remediation**: strong (25+ char) service-account passwords or gMSA; AES-only on service
  accounts; monitor 4769 by encryption type.

---

## AS-REP Roasting: Event 4768, no pre-auth

Cracking accounts that have Kerberos pre-authentication disabled, no valid credential
needed to request the roastable material.

- **Event 4768** (TGT requested) with `Pre-Authentication Type = 0`. Normal accounts always
  pre-authenticate; a 4768 with no pre-auth is the signature.
- **MDI**: "Suspected AS-REP Roasting attack."

```bash
GetNPUsers.py corp.local/ -usersfile users.txt -dc-ip <dc_ip> -no-pass -format hashcat
```

- **MITRE**: T1558.004 (AS-REP Roasting).
- **Defender watch**: 4768 with pre-auth type 0; any account carrying `DONT_REQUIRE_PREAUTH`.
- **Remediation**: remove `DONT_REQUIRE_PREAUTH` wherever possible; strong passwords on
  accounts that genuinely need it; alert on the flag being set.

---

## DCSync: Event 4662, replication GUIDs

Replicating credentials out of the DC using directory-replication rights. High severity,
never transparent, so coordinate before running.

- **Event 4662** (operation on a directory object) with the replication rights GUIDs:
  - `1131f6aa-9c07-11d1-f79f-00c04fc2dcd2`: DS-Replication-Get-Changes
  - `1131f6ad-9c07-11d1-f79f-00c04fc2dcd2`: DS-Replication-Get-Changes-All
- **MDI**: "Suspected DCSync attack (replication of directory services)": a critical alert
  in any competent SOC.
- The source host in the DC logs is your machine's IP, not a real DC. That mismatch (a
  non-DC requesting replication) is itself the detection.

```bash
secretsdump.py corp.local/user:pass@dc01.corp.local -just-dc-user krbtgt
```

- **MITRE**: T1003.006 (OS Credential Dumping: DCSync).
- **Defender watch**: 4662 with the Get-Changes GUIDs from any principal that is not a DC;
  replication requests sourced from non-DC IPs.
- **Remediation**: audit and minimize who holds Get-Changes / Get-Changes-All; alert on
  replication from non-DC sources; tier-0 isolation.

---

## LSASS dumping: blocked by EDR

Dumping process memory of `lsass.exe` to extract credentials.

- Modern EDR in blocking mode (CrowdStrike Falcon, SentinelOne, Defender for Endpoint)
  intercepts `MiniDumpWriteDump` against lsass. The result is a blocked/empty dump, a
  crashed process, or an immediate alert naming your tool.
- **Event 4688** (process creation) plus EDR-specific handle-to-lsass telemetry.

**Alternatives that avoid touching lsass live:**

- SAM/SYSTEM/SECURITY registry hive dump (local admin) → offline parsing.
- DPAPI offline extraction.
- Volume Shadow Copy of the hive + offline parse.
- gMSA / LAPS fetch over LDAP (no endpoint touch at all).

```bash
# Registry-hive route: avoids a live lsass handle
secretsdump.py -sam sam.save -system system.save LOCAL
```

- **MITRE**: T1003.001 (LSASS Memory).
- **Defender watch**: process handles opened to lsass with read/VM-read access; EDR
  memory-access alerts.
- **Remediation**: Credential Guard; LSASS as a protected process (RunAsPPL); EDR in
  blocking mode.

---

## BloodHound collection: a recognizable LDAP signature

- Collector queries have well-known shapes: `(objectCategory=computer)` pulling dozens of
  attributes, plus queries for `msDS-AllowedToDelegateTo`, delegation and ACL attributes in
  bulk.
- MDI and legacy ATA carry specific detection for BloodHound-style enumeration.
- Quieter collection requests only the attributes it needs (never `*`) and spreads queries
  over time instead of firing them all at connect.

- **MITRE**: T1087 (Account Discovery), T1069 (Permission Groups Discovery).
- **Defender watch**: a single principal issuing large attribute-heavy LDAP sweeps in a
  short window.

---

## Lateral movement: telemetry by protocol

When you need remote execution, the protocol you pick determines the noise. From loudest to
quietest:

| Protocol | Telemetry | OPSEC note |
|---|---|---|
| PsExec (SCM service install) | **Event 7045** service install — very visible, routinely EDR-blocked | Avoid when EDR is active |
| WMI exec | **Event 4688** process create — MDE detects | Quieter than PsExec |
| Scheduled task | **Event 4698/4702** task created — moderately visible | Acceptable |
| WinRM / PSRemoting | Legitimate channel, but **Event 4624** logon type 3 + PowerShell logs | Preferred when available |
| DCOM / MMC | Fewer known signatures | Best profile under EDR |

- **MITRE**: T1021 (Remote Services) and subtechniques; T1569.002 (Service Execution);
  T1053.005 (Scheduled Task); T1047 (WMI).
- **Rule**: record which protocol you used and its profile in the report, so the client can
  correlate with their endpoint logs.

---

## Coercion and NTLM relay: high-volume auth noise

- Coercion (PetitPotam, PrinterBug, DFSCoerce) forces a target to authenticate to you,
  producing inbound auth requests visible in SIEM. Coercing at scale generates hundreds of
  auth events.
- `ntlmrelayx` in automatic mode can capture credentials of real users in production, so
  coordinate before running it against a live environment.

- **MITRE**: T1187 (Forced Authentication), T1557.001 (LLMNR/NBT-NS Poisoning and SMB Relay).
- **Defender watch**: spikes of inbound authentications to a non-standard host; EFSRPC /
  spoolss / DFS RPC calls to unexpected destinations.
- **Remediation**: SMB signing enforced; LDAP channel binding; EPA on AD CS web endpoints;
  disable spooler on DCs.

---

## SMB null sessions: reconnaissance signal

- Windows Server 2016+ disables null sessions by default; some SOCs alert on the attempt as
  anonymous recon.
- When you hold credentials, always use them. Null session is a last-resort fallback only,
  and worth documenting when used.

- **MITRE**: T1135 (Network Share Discovery), T1087.

---

## Actions that require explicit coordination

Show a warning and get sign-off (or document that it ran) before any of these:

| Action | Why |
|---|---|
| DCSync | Critical MDI alert; your IP visible in DC logs |
| Password spraying | Risk of locking out real accounts |
| ntlmrelayx (auto) | May capture real users' credentials in production |
| Coercion at scale | Hundreds of auth requests, SIEM-visible |
| Kerberoasting all accounts | MDI volume alert; document targeted accounts |
| LSASS dump | EDR-detectable; risk of crashing the process |

---

## How to use this

Running a technique: check its row, warn the client about the events it will generate, and
prefer the quieter equivalent when there is one (WMI over PsExec, one SPN over the whole
domain, registry-hive over live lsass). Writing the report: turn these tables into the
detection-and-remediation section so the defender can find every action you took and close
the gap that let it work.
