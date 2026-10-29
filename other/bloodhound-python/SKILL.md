---
name: bloodhound-python
description: "Collect Active Directory data with BloodHound.py from Linux: users, groups, sessions, local admins, ACLs and trusts, zipped for the graph. Use when you have domain credentials and need attack paths before touching hosts. Not for live host triage (use netexec) or AD CS enumeration (use certipy)."
---

# BloodHound.py

BloodHound.py is the Linux collector for the BloodHound graph. It authenticates to the DC over LDAP, pulls users, groups, computers, OUs, GPOs, ACLs and trusts, then optionally fans out to every computer to ask who is a local admin and who is logged on. The output is JSON that you zip and drop into BloodHound; all analysis then happens offline, which is the point.

This box runs **bloodhound 1.9.0**, which announces itself as `BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)`. That banner is a compatibility statement, not decoration: the zip uses the BloodHound 4.x collector layout, not the SharpHound CE layout. Confirm which server and schema version you are feeding before you collect, because a mismatched zip imports as an empty or partial graph.

## When to use

| Goal | Collection | Command shape |
| --- | --- | --- |
| Full path graph, quiet | `-c DCOnly` | `bloodhound-python -c DCOnly -d corp.local -u alice -p pw -ns 10.10.10.10` |
| Everything except logged-on users | `-c All` | `bloodhound-python -c All ... --zip` |
| Default set: groups, admins, sessions, trusts | `-c Default` | `bloodhound-python -c Default ...` |
| Local admin edges only | `-c LocalAdmin` | one SAMR call per computer |
| Session edges only | `-c Session` | one SRVSVC call per computer |
| Logged-on users from registry | `-c LoggedOn` | needs admin on each target |
| ACL and object property edges | `-c ACL,ObjectProps` | DC LDAP only, large result sets |
| Kerberos-only DC | `-k` | `KRB5CCNAME` plus `-ns` and FQDN |
| Re-collect a subset later | `--computerfile` | allowlist of FQDNs |

## Prerequisites

- `bloodhound-python --help` renders; version banner says `BloodHound.py for BloodHound LEGACY`. On this host it is at `~/.local/bin/bloodhound-python`.
- Any valid domain account works for `DCOnly`; `LocalAdmin` and `Session` need reachability to every workstation and, on modern Windows, administrative rights for the RPC calls to return data.
- Name resolution decides success. `-ns <dc-ip>` plus `-d corp.local` is usually enough; when it is not, put the DC in `/etc/hosts` and pass `-dc dc01.corp.local`.
- Kerberos runs need a synchronised clock (`chronyc makestep` if you are root) and a ccache in `KRB5CCNAME`.
- Collect into a dedicated directory; the collector writes into the current working directory and a re-run overwrites same-named files.

## Core invocations

```sh
# 1. the default safe collection: DC LDAP, no computer fan-out
bloodhound-python -c DCOnly -d corp.local -u alice -p 'Winter2026!' \
  -ns 10.10.10.10 -dc dc01.corp.local

# 2. full graph except logged-on users, zipped for import
bloodhound-python -c All -d corp.local -u alice -p 'Winter2026!' \
  -ns 10.10.10.10 --zip -op corp

# 3. default set (group, localadmin, session, trusts)
bloodhound-python -c Default -d corp.local -u alice -p 'Winter2026!' \
  -ns 10.10.10.10

# 4. pass-the-hash collection with no plaintext password
bloodhound-python -c DCOnly -d corp.local -u alice \
  --hashes aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0 \
  -ns 10.10.10.10

# 5. Kerberos only, using a ccache from getTGT.py
export KRB5CCNAME=$PWD/alice.ccache
bloodhound-python -c All -d corp.local -u alice -k -no-pass \
  -ns 10.10.10.10 -dc dc01.corp.local --zip

# 6. the two loud methods, run deliberately and separately
bloodhound-python -c LocalAdmin -d corp.local -u alice -p 'Winter2026!' \
  -ns 10.10.10.10 --zip -op localadmin
bloodhound-python -c Session -d corp.local -u alice -p 'Winter2026!' \
  -ns 10.10.10.10 --zip -op sessions

# 7. logged-on users, only worth it with admin rights on the targets
bloodhound-python -c LoggedOn -d corp.local -u da-alice -p 'Winter2026!' \
  -ns 10.10.10.10 --zip

# 8. ACL-heavy collection, then tune concurrency down
bloodhound-python -c ACL,ObjectProps -d corp.local -u alice -p 'Winter2026!' \
  -ns 10.10.10.10 -w 5 --zip

# 9. limit computer methods to a known list of hosts
bloodhound-python -c Session -d corp.local -u alice -p 'Winter2026!' \
  -ns 10.10.10.10 --computerfile hosts.txt

# 10. hardened DC: LDAP over TLS with channel binding
bloodhound-python -c DCOnly -d corp.local -u alice -p 'Winter2026!' \
  -ns 10.10.10.10 --use-ldaps --ldap-channel-binding

# 11. cross-domain collection against a trusted domain
bloodhound-python -c DCOnly -d child.corp.local -u alice -p 'Winter2026!' \
  -ns 10.10.10.11 -dc dc01.child.corp.local

# 12. verbose run when the graph comes back thin or empty
bloodhound-python -c Session -d corp.local -u alice -p 'Winter2026!' \
  -ns 10.10.10.10 -v -w 3
```

## Flags that matter

| Flag | Effect | Cost |
| --- | --- | --- |
| `-c` | collection methods, comma separated | the only real traffic dial |
| `-d` | domain to collect | required |
| `-u` / `-p` | credentials, `user@domain` form allowed | plaintext on the command line |
| `--hashes` | `LM:NT` pass-the-hash | avoids plaintext |
| `-k` / `-no-pass` | Kerberos from `KRB5CCNAME` | quietest auth path |
| `--auth-method` | `auto`, `ntlm`, `kerberos` | force NTLM when Kerberos fails on SPN issues |
| `-ns` | nameserver for lookups | required when DNS is wrong |
| `-dc` / `-gc` | pin the DC or global catalog | avoids bad autodiscovery |
| `-w` | worker threads for computer enumeration | default 10; lower it on fragile networks |
| `--exclude-dcs` | skip DCs in computer methods | reduces noise on the most watched hosts |
| `--computerfile` | allowlist of FQDNs | bounds the blast radius |
| `--zip` | compress output into one archive | import convenience, no traffic change |
| `-op` | output filename prefix | keep collections distinguishable |
| `--use-ldaps` | LDAP over 636 | needed on hardened DCs |
| `--ldap-channel-binding` | enforce channel binding | forces LDAPS |
| `--dns-timeout` | per-query DNS timeout | raise on slow resolvers |
| `--disable-pooling` | single-process ACL parsing | debugging only, much slower |
| `--disable-autogc` | do not auto-select a global catalog | fixes odd GC errors |
| `--cachefile` | reuse cached computer data | experimental; reuses stale data |

## Workflow

1. **Start with `DCOnly`.** It touches only the DC, gives you users, groups, ACLs, trusts and containers, and answers most "who can do what" questions without a single workstation connection.
2. **Read the graph before collecting more.** If the DC-only graph already shows a path to Domain Admin, stop; every additional method adds exposure for no new answer.
3. **Add `LocalAdmin` when you need lateral edges.** It is the method that finds "this service account is local admin on twelve servers", which is what makes relay and dumping worthwhile.
4. **Add `Session` deliberately.** Sessions change hourly; collect close to the moment you act, not days earlier.
5. **Treat `LoggedOn` as a privilege.** It needs admin on each target and reads registry session data; on a hardened estate it will mostly return nothing.
6. **Zip and hand off.** Import into BloodHound, run the shortest-path queries, and keep the zip as evidence of what the graph said at that time.
7. **Re-collect with `-op` prefixes.** Never overwrite a collection you have already reported on.

## OPSEC and telemetry

- `DCOnly` is LDAP to one host: no 4624 storm, no workstation contact. The DC records the bind (4624 type 3, or 4768/4769 when Kerberos) and, if LDAP diagnostic logging is raised, 1644 events with your query text.
- `LocalAdmin` opens SAMR to every computer in scope. Each target logs a network logon (4624 type 3) from your IP with the collecting account, and bulk SAMR local-admin enumeration is exactly what EDR rules watch for on workstations.
- `Session` calls `NetSessionEnum` over SRVSVC on every computer. Same 4624 type 3 pattern, plus a burst of RPC connections that a network sensor sees as one host sweeping 445 across the range.
- `LoggedOn` reads registry session keys and calls `NetWkstaUserEnum`; it requires admin and fails loudly in logs when it does not have it.
- `ACL` reads `nTSecurityDescriptor` on every object: the largest LDAP result set in the whole tool, and the one most likely to trip DC performance alerting.
- There is no single "BloodHound ran" event. The signature is fan-out: one source IP, one account, hundreds of short SMB sessions in a few minutes. Use `-w`, `--exclude-dcs` and `--computerfile` to shape it.
- SharpHound leaves a binary on disk (`SharpHound.exe`/`.ps1`) and generates 4688 and script-block 4104 events on the host it runs from. BloodHound.py leaves nothing on the target at all, which is why it is preferred when you already have Linux access.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `LDAPSocketOpenError` or immediate timeout | wrong `-ns`, or 389 filtered | pass `-dc <ip>`, try `--use-ldaps` |
| `Could not resolve ...` on most computers | DNS does not answer for client FQDNs | add `-ns <dc-ip>`; check `--dns-timeout` |
| Empty sessions but collection "succeeded" | no admin on targets, so SRVSVC returns nothing | accept it, or use `LoggedOn` with a DA account |
| `KRB_AP_ERR_SKEW` | clock drift | sync time, or drop to `--auth-method ntlm` |
| `KRB_AP_ERR_MODIFIED` / SPN errors | connecting by IP with Kerberos | use the FQDN in `-dc` and `-ns` |
| Zip will not import into BloodHound CE | legacy collector format | import into BloodHound 4.x, or collect with SharpHound CE |
| ACL parsing crashes or hangs | process pooling bug | add `--disable-pooling` |
| Output split into `_01.json`, `_02.json` | large result sets | expected; zip it, do not merge by hand |
| Collection finishes in seconds with tiny files | wrong domain or a collection method that found nothing | re-run with `-v` and confirm the method name |
| `-c All` still has no logged-on users | by design, `All` excludes `LoggedOn` | add `LoggedOn` explicitly |

## Verification

```sh
bloodhound-python --help | head -3     # usage block renders
bloodhound-python -v 2>&1 | head -3    # BloodHound.py for BloodHound LEGACY
ls -1 *_users.json *_computers.json    # expected output files
unzip -l <prefix>_<timestamp>_bloodhound.zip
```

Expected: the LEGACY banner, then JSON files named `<prefix>_<YYYYmmddHHMMSS>_users.json`, `_computers.json`, `_groups.json`, `_domains.json`, `_gpos.json`, `_ous.json`, `_containers.json`, and `_sessions.json` only when sessions were collected. Keep the command line, the zip, and the collection timestamp.

## Related skills

- [netexec](../netexec/SKILL.md) for credential validation and ad-hoc LDAP queries between collections
- [impacket](../impacket/SKILL.md) to act on the delegation and ACL edges the graph reveals
- [certipy](../certipy/SKILL.md) for the AD CS edges that need a separate collector
- [enum4linux-ng](../enum4linux-ng/SKILL.md) when you have no credentials yet
- [toolchain-router](../toolchain-router/SKILL.md) to decide between this and SharpHound