---
name: enum4linux-ng
description: "Enumerate Windows and Samba hosts over SMB and LDAP with enum4linux-ng: null and guest sessions, users, groups, shares, password policy, RID cycling, structured JSON/YAML output. Use when you have no credentials or only weak ones. Not for authenticated subnet sweeps (use netexec) or graph collection (use bloodhound-python)."
---

# enum4linux-ng

enum4linux-ng is a rewrite of the classic `enum4linux` Perl script. It wraps Samba's `rpcclient`, `smbclient`, `net` and `nmblookup`, parses their output into structured data, and writes JSON or YAML. Where the original printed whatever the tools said, this one tells you which checks succeeded, which were denied, and which were inconclusive, and keeps going after a failure.

It is the tool you reach for before you own a credential: anonymous session, guest session, or one low-privilege account, extracting users, groups, shares, password policy and OS build from a single host.

What it gives you that `nxc` does not: a per-check verdict for a genuinely anonymous session, Samba-side RPC (`rpcclient`) instead of impacket's, password policy with no credential at all, NetBIOS name and workgroup discovery, share-name brute forcing with `-s`, and one JSON document that records a refused check as a refusal instead of silently omitting it. `nxc` is faster, sweeps whole subnets, and validates credentials; this tool goes deeper on a single host you cannot authenticate to.

**Host status.** The Samba client tools are installed here (`samba-common-bin` provides `nmblookup` and `net`), so `enum4linux-ng --help` runs and the wrapper executes normally. A host without them exits before parsing arguments with `[!] The following dependend tools are missing: nmblookup, net`; install `smbclient samba-common-bin` first.

## When to use

| Goal | Flag set | Why |
| --- | --- | --- |
| Everything, one shot | `-A` | `-U -G -S -P -O -N -I -L` in one pass |
| Everything except NetBIOS | `-As` | same minus `-N`; use when NetBIOS is filtered |
| Users and groups by name | `-U -G` | SAMR `enumdomusers` / `enumdomgroups` |
| Group membership detail | `-Gm -d` | adds members and per-object detail |
| Shares and per-share access | `-S` | `netshareenumall` plus connection test |
| Password policy before spraying | `-P` | lockout threshold and duration |
| OS build and role | `-O` | version fingerprint from SMB |
| Domain info from a DC | `-L` | LDAP/LDAPS, DCs only |
| Users by RID when names are hidden | `-R` | RID cycling, no failed logons |
| Share name guessing | `-s` | brute force from a wordlist |

## Prerequisites

- Samba client tools (`nmblookup`, `net`, `rpcclient`, `smbclient`) on PATH. Without them the tool exits immediately.
- TCP 445 (or 139) reachable; LDAP 389/636 for `-L`.
- No credentials for a null session. If null is refused, try guest with `-u guest -p ''`, and only then a real low-privilege account.
- Set `NO_COLOR=1` when capturing output to a file or a report.
- Wordlists: `/opt/wordlists/web-common.txt` for `-s`, `users-top.txt` for `-k`.

## Core invocations

```sh
# 1. anonymous everything against one host
enum4linux-ng -A 10.10.10.5

# 2. same, skipping the NetBIOS lookup that usually times out
enum4linux-ng -As 10.10.10.5

# 3. null session, users and groups only
enum4linux-ng -U -G 10.10.10.5

# 4. guest session when anonymous is refused
enum4linux-ng -A -u guest -p '' 10.10.10.5

# 5. authenticated enumeration with a real account
enum4linux-ng -A -u alice -p 'Winter2026!' -w CORP 10.10.10.5

# 6. pass-the-hash, no plaintext
enum4linux-ng -A -u alice -H 31d6cfe0d16ae931b73c59d7e0c089c0 10.10.10.5

# 7. Kerberos ticket auth
enum4linux-ng -A -u alice -K /tmp/alice.ccache 10.10.10.5

# 8. local account on a workgroup machine, not the domain
enum4linux-ng -A -u Administrator -p 'P@ssw0rd' --local-auth 10.10.10.5

# 9. password policy only: cheap, and it prevents lockouts later
enum4linux-ng -P 10.10.10.5

# 10. RID cycling with explicit ranges and a bulk lookup size
enum4linux-ng -R 100 -r 500-1200,2000-2500 -k administrator,guest 10.10.10.5

# 11. share brute force from a wordlist
enum4linux-ng -s /opt/wordlists/web-common.txt -u guest -p '' 10.10.10.5

# 12. structured output for the report
enum4linux-ng -A 10.10.10.5 -oJ findings/dc01 -oY findings/dc01

# 13. both formats plus detail on every user and group
enum4linux-ng -A -d -oA findings/dc01 -u alice -p 'Winter2026!' 10.10.10.5

# 14. domain controller: add LDAP, which is where -L earns its place
enum4linux-ng -A -L -u alice -p 'Winter2026!' -w CORP dc01.corp.local
```

## Flags that matter

| Flag | Effect | Note |
| --- | --- | --- |
| `-A` | all simple checks incl. NetBIOS | also the default when no other option is given |
| `-As` | all except NetBIOS lookup | safer on filtered networks |
| `-U` / `-G` / `-Gm` | users / groups / groups with members | `-Gm` costs one extra call per group |
| `-S` | shares via RPC plus access check | access check makes a connection per share |
| `-P` | password policy | lockout threshold, duration, min length |
| `-O` | OS information | build number narrows the exploit shortlist |
| `-L` | LDAP/LDAPS domain info | DCs only; needs 389 or 636 |
| `-I` | printer information | legacy path, often disabled |
| `-R [BULK]` | RID cycling, optional bulk size | default ranges are narrow |
| `-r` | RID ranges, e.g. `500-550,1000-1050` | widen deliberately |
| `-k` | known usernames for SID resolution | comma separated, default shortlist |
| `-s` | brute-force share names from a file | noisy on large lists |
| `-u` / `-p` | credentials | `-p ''` for a null or guest password |
| `-H` | NT hash auth | mutually exclusive with `-p` and `-K` |
| `-K` | Kerberos ticket file | mutually exclusive with `-p` and `-H` |
| `--local-auth` | authenticate to the local SAM | workgroup hosts and local admins |
| `-w` | workgroup or domain name | when autodetection guesses wrong |
| `-d` | detailed users and groups | applies to `-U`, `-G`, `-R` |
| `-t` | connection timeout in seconds | default 10 |
| `-v` | verbose, show the Samba commands | the first thing to try when a check fails |
| `--keep` | keep the generated `smb.conf` | pairs with `-v` |
| `-oJ` / `-oY` / `-oA` | JSON / YAML / both | extension added automatically |

## Workflow

1. **Anonymous first.** `-A` with no credentials. Note which sections return data and which return `unknown` or `error`; that split tells you whether the host allows null sessions at all.
2. **Guest second.** `-u guest -p ''`. Many estates disable null but forget the guest account.
3. **Policy before passwords.** `-P` gives you the lockout threshold. Spraying without it is how accounts get locked and how you get noticed.
4. **RID cycle to recover hidden names.** When `-U` returns nothing but the host answers SAMR, `-R` with wider `-r` ranges maps RIDs to names without a single failed logon.
5. **Shares with an identity.** Anonymous share lists are usually empty; repeat `-S` with the weakest valid credential you hold.
6. **Persist and parse.** `-oJ` and read the JSON with `jq` rather than re-running the tool. It is slower and noisier than parsing.
7. **Pivot.** Feed usernames to `nxc` or `kerbrute`, shares to `smbclient.py`, and policy to your spray planner.

## OPSEC and telemetry

- A null session is an anonymous network logon: 4624 type 3 with `Security ID: ANONYMOUS LOGON` on the target. Some estates do not log anonymous logons at all, which is exactly why the technique survives.
- Guest attempts that fail produce 4625 with the guest account name; a handful is normal background noise, hundreds is you.
- `-U`, `-G`, `-S` and `-P` are SAMR/LSARPC calls over `\srvsvc`, `\samr`, `\lsarpc` named pipes. They are not audited by default, but EDR products hook these pipes and will flag the sequence.
- `-R` cycling issues one `LookupSids` per RID batch; the target sees a long-running SAMR session. It creates no failed authentications, so it does not risk lockouts.
- `-L` binds to LDAP as the supplied account (or anonymously). The DC logs the bind and, with diagnostic logging, 1644 events.
- `-s` share guessing opens a connection per candidate name; a large wordlist against one host is a visible burst on 445.
- No file is dropped on the target and no service is created. The footprint is entirely connection metadata, which is why this is a good first tool and a poor one to repeat.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `[!] The following dependend tools are missing: nmblookup, net` | Samba client not installed | install `smbclient samba-common-bin` (already present on this host) |
| `Could not connect to target` | 445 filtered or host down | verify with `nmap -p445`; try `--local-auth` host on 139 |
| Everything returns `unknown` / `error` | null sessions disabled and no credentials | supply `-u`/`-p`, or fall back to `netexec` |
| `-N` hangs for the full timeout | NetBIOS name service blocked | use `-As` instead of `-A` |
| Users listed but groups empty | SAMR partially restricted | try `-Gm`, or authenticate |
| Password policy all zeros | anonymous cannot read it | `-P` with any valid account |
| `-R` finds nothing | RID restriction or SIDs filtered | widen `-r`, pass `-k` with a known account, or accept the block |
| LDAP section empty on a DC | signing or channel binding required | use a credential; the tool's LDAP path is not configurable |
| `-oJ` writes nothing | a directory was passed instead of a filename prefix | pass a full path prefix; `.json`/`.yaml` is appended for you |
| `-S` prints `Found 0 share(s) for user ...` | anonymous or guest cannot list shares | retry with a real account; the message names the identity it used |
| `-U` empty but `-R` resolves names | `enumdomusers` restricted, SAMR lookups still allowed | rely on `-R`, widen `-r` ranges |

## Verification

```sh
enum4linux-ng 2>&1 | head -3        # banner plus any missing-dependency warning
which rpcclient smbclient net nmblookup
enum4linux-ng -As 10.10.10.5 -oJ /tmp/enum-dc01 && jq 'keys' /tmp/enum-dc01.json
```

Expected on a working host: `ENUM4LINUX - next generation (v1.3.10)`, then per-section progress, then a JSON file whose top-level keys include `users`, `groups`, `shares`, `policy`, `printers`, `os_info`, `sessions` and `services`. On this machine expect only the banner and the missing-tools warning. Keep the JSON as the evidence artefact; it records which checks ran and what each returned.

## Related skills

- [netexec](../netexec/SKILL.md) for validated credentialed enumeration once you have a password or hash
- [impacket](../impacket/SKILL.md) for `lookupsid.py` (RID cycling without Samba) and `smbclient.py`
- [bloodhound-python](../bloodhound-python/SKILL.md) for graph collection after this reconnaissance
- [certipy](../certipy/SKILL.md) for the AD CS surface that SMB enumeration cannot see