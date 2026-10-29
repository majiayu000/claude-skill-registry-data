---
name: hydra
description: "Guess and spray credentials online with THC Hydra across ssh, rdp, smb, ftp, ldap2 and http forms, with thread limits that respect lockout policy. Use when you have users, a candidate password list and a reachable service. Not for offline cracking (use john or hashcat) and not for Kerberos pre-auth enumeration (use kerbrute)."
---

# Hydra

Hydra is a parallel, protocol-aware login guesser. Each module speaks the real service handshake, so a hit is a working credential rather than a string match. The risk profile is the opposite of an offline cracker: every attempt is an authentication event on the target, and account lockout is a real, irreversible failure.

This host runs Hydra v9.5 with protocol modules `smb2`, `afp`, `ncp`, `oracle` and `sapr3` **not compiled in**. `smb` is present and does NTLM; use it, not `smb2`.

## When to use

| Service | Module | Optional argument |
| --- | --- | --- |
| Linux/Unix shell | `ssh` | none |
| Windows remote desktop | `rdp` | domain as URL path |
| Windows file sharing | `smb` | `-m "local lmv2"` or hash mode |
| FTP | `ftp` | none |
| Web login form (POST) | `http-post-form` | URL, body, condition |
| HTTP basic auth | `http-get` | URL and path |
| Directory service | `ldap2` | bind DN as URL path |
| Mail, DB, VNC, SNMP | `smtp`, `mysql`, `vnc`, `snmp` | see `-U <module>` |

For anything Kerberos-aware (user enumeration without lockout, AS-REP roasting) use kerbrute or NetExec instead. For hashes you already hold, crack offline with john.

## Prerequisites

- `hydra -h` prints `Hydra v9.5`. Binary at `/usr/bin/hydra`.
- Valid usernames. A spray against a guessed user list wastes the lockout budget; enumerate first.
- `-U <module>` before every new module: it prints the module's optional parameters, which differ wildly.
- Wordlists at `/opt/wordlists`: `users-top.txt`, `pass-top1m.txt`, `rockyou.txt`, `pass-1050.txt`.
- Know the lockout policy (`nxc smb <dc> -u u -p p --pass-pol`) before sending the first attempt.

## Core invocations

```sh
# 1. Straight dictionary attack, one user against a known list
hydra -l alice -P /opt/wordlists/pass-1050.txt ssh://10.0.0.20 -t 4

# 2. Spray: one password across many users, low thread count
hydra -L /opt/wordlists/users-top.txt -p 'Spring2026!' ssh://10.0.0.20 -t 2 -o spray.txt

# 3. Cheap wins first: null password, login-as-password, reversed login
hydra -l alice -e nsr ssh://10.0.0.20

# 4. FTP with a single password and a user list
hydra -L users.txt -p 'ftp' ftp://10.0.0.50

# 5. RDP, with the Windows domain appended to the URL path
hydra -L users.txt -p 'Welcome1' rdp://10.0.0.30/corp

# 6. SMB local account test with NTLMv2 (module default is local + domain)
hydra -l administrator -p 'P@ssw0rd' smb://10.0.0.30 -m "local lmv2"

# 7. SMB pass-the-hash style: LM:NT in the password field
hydra -l administrator -p 'aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0' smb://10.0.0.30 -m "local hash"

# 8. Web form POST: ^USER^ and ^PASS^ are placeholders, F= is the failure string
hydra -l admin -P /opt/wordlists/pass-1050.txt 10.0.0.60 http-post-form \
  '/login:username=^USER^&password=^PASS^:F=Invalid credentials'

# 9. Same form but keyed on success instead of failure
hydra -l admin -P pass.txt 10.0.0.60 http-post-form \
  '/login:user=^USER^&pass=^PASS^:S=Sign out'

# 10. HTTP basic auth
hydra -L users.txt -P /opt/wordlists/pass-1050.txt 10.0.0.60 http-get /admin/

# 11. LDAP simple bind, DN as the URL path with ^USER^ substituted
hydra -L users.txt -p 'Summer2026!' ldap2://10.0.0.10/cn=^USER^,cn=users,dc=corp,dc=local

# 12. Several hosts at once, global parallelism cap
hydra -L users.txt -p 'Spring2026!' -M hosts.txt -T 8 ssh

# 13. Brute force a short numeric PIN (not for real passwords)
hydra -l admin -x 4:4:1 10.0.0.70 http-post-form '/pin:pin=^PASS^:F=wrong'

# 14. Machine-readable results plus a strict wait between attempts
hydra -L users.txt -P pass.txt rdp://10.0.0.30 -o hits.json -b json -W 3 -t 1

# 15. Resume an aborted run instead of restarting the whole list
hydra -R
```

## Flags that matter

| Flag | Effect | Note |
| --- | --- | --- |
| `-l` / `-L` | single login / login file | file must be one name per line |
| `-p` / `-P` | single password / password file | spray mode is one `-p` with many `-L` |
| `-C` | combined `login:pass` file | replaces `-L`/`-P` |
| `-t N` | parallel connects per target, default 16 | lower to 2-4 on AD |
| `-T N` | parallel connects overall with `-M`, default 64 | total budget across hosts |
| `-s PORT` | non-default port | required when the service is moved |
| `-S` | SSL connect | for HTTPS and implicit TLS services |
| `-f` / `-F` | stop at first hit, per host / globally | omit when spraying, you want all hits |
| `-e nsr` | try null, login-as-password, reversed | one pass, no wordlist |
| `-u` | loop users instead of passwords | matches spray thinking |
| `-x MIN:MAX:CHARSET` | generated passwords, `a` lower, `A` upper, `1` digits | brute force only; loud |
| `-m OPT` | module options | see `-U <module>` |
| `-o FILE` / `-b FORMAT` | write results, text/json/jsonv1 | evidence trail |
| `-w` / `-W` | response timeout / wait between connects | `-W` is your only politeness control |
| `-I` / `-R` | ignore restore file / restore it | `hydra.restore` in the cwd |
| `-K` | do not redo attempts already failed | mass-scan efficiency |
| `-V` / `-v` / `-d` | show attempt / verbose / debug | `-d` prints raw request and response |
| `-4` / `-6` | IPv4 / IPv6 | IPv6 needs `[]` around addresses |

## Workflow

1. **Enumerate users first.** Spraying against guesses burns lockout budget on accounts that do not exist.
2. **Read the lockout policy and the logon-hours window.** If threshold is 5, plan at most 2-3 attempts per account per window.
3. **Get the module's parameters** with `hydra -U <module>`; the URL path and `-m` semantics are module-specific.
4. **Test the mechanism on one account you own** or a known-bad credential, and confirm the failure message (`-d` shows it).
5. **Spray one good password across the user list** with `-t 2`, `-W 1`. For forms, verify the failure string first to avoid false positives.
6. **Collect hits** with `-o` and `-b json`, then validate them in a tool that reports real access (`nxc smb`, `ssh`) rather than trusting hydra's socket.
7. **Escalate**: new credential -> reproduce on other hosts -> look for reuse across the estate.
8. **Stop and reassess** if the target starts returning lockouts; hydra cannot see that, only the SOC can.

## OPSEC and telemetry

- Every attempt is a real login. Windows logs 4625 per failure and 4624 per success; Linux writes `Failed password` to auth.log; SSH may add fail2ban bans after a handful of tries.
- Thread count is the loudest variable. Default `-t 16` against AD will lock accounts before it finds anything.
- Lockout is irreversible within the window: a bad spray can deny service to real users and is an incident on its own.
- `http-post-form` false positives come from guessing the failure string wrong; `-d` and a single manual request settle it.
- Hydra identifies itself in some protocols; `-q` hides connection errors, not the attempts.
- Proxying is possible via `HYDRA_PROXY` / `HYDRA_PROXY_HTTP` (socks5://, http://, or a file of up to 64 proxies). Chaining through a pivot keeps your IP out of the target logs but does not reduce the event count.
- Results files (`-o`, `hydra.restore`) contain plaintext credentials and pending state in the working directory.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| Module refuses to start | service not compiled in (smb2, oracle, sapr3, afp, ncp) | use `smb`, or a different tool (NetExec for SMB2 features) |
| Every attempt fails with an auth-method error | service uses keys or MFA | stop; try ssh keys or a session hijack instead |
| Every attempt fails with `connect error` | wrong port or TLS required | add `-s PORT` / `-S`, confirm with `nmap -p` |
| All combinations report success | wrong `F=` failure string | fix the condition string, add `S=` for a positive match |
| 0 valid passwords after a few attempts | accounts locked by policy | wait out the window, lower `-t`, coordinate |
| Runs die mid-way with child/connection errors | target rate-limited or service crashed | reduce `-t`, add `-W`, verify the service is still up |
| `hydra.restore already exists` | previous run left state | `-I` to ignore or `-R` to resume deliberately |
| RDP hits nothing but manual login works | domain or NLA mismatch | append `/domain` to the URL, confirm NLA is on |
| SMB auth fails with valid credentials | wrong dialect | `-m "local lmv2"` or `-m "local ntlm"` |

## Verification

```sh
hydra -h | head -3                        # expect: Hydra v9.5
hydra -h | grep -o "Supported services:.*" # confirm smb, rdp, ldap2, http-post-form are listed
hydra -U smb | tail -8                    # expect: module help with local/hash dialect notes
hydra -U http-post-form | tail -12        # expect: syntax and F=/S= condition explanation
hydra -U whatever 2>&1 | tail -2          # expect: generic text; -U cannot prove a module is compiled
```

Evidence to keep for each run: the exact command, target list, thread count, `-o` output file and the corresponding authentication events on the target.

## Related skills

- [netexec](../netexec/SKILL.md) for validated spraying with `--continue-on-success` and `--pass-pol`
- [kerbrute](../kerbrute/SKILL.md) for user enumeration without lockout risk
- [john](../john/SKILL.md) once you have hashes instead of a live service
- [metasploit](../metasploit/SKILL.md) for auxiliary login scanners and stored credentials
- [toolchain-router](../toolchain-router/SKILL.md) to confirm online guessing is the right move