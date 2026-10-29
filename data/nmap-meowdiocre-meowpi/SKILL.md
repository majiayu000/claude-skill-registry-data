---
name: nmap
description: "Map live hosts, TCP and UDP ports, service versions and NSE findings with Nmap 7.94SVN, and write evidence files other tools can consume. Use when you need to know what a network or host exposes before touching it. Not for web content discovery (use ffuf or feroxbuster) or exploit execution (use nuclei or sqlmap)."
---

# Nmap

Nmap answers four separate questions: which hosts are alive, which ports are open, what software listens on them, and what the scripts can prove about that software. Run them as separate phases. One `-A` invocation mixes all four, multiplies traffic, and produces output nobody can diff.

This host runs 7.94SVN (2023) with 606 NSE scripts in `/usr/share/nmap/scripts`. The service probe database is old; treat version output as a hint and confirm with a banner grab.

## When to use

| Question | Phase | Command shape |
| --- | --- | --- |
| Which hosts are up on a subnet | discovery | `nmap -sn -n 10.10.10.0/24` |
| Which of the common ports are open | TCP triage | `nmap -Pn -n -sS --top-ports 1000 -T4 host` |
| Every TCP port, fast | full TCP | `nmap -Pn -n -sS -p- --min-rate 2000 host` |
| What version is listening | service detection | `nmap -Pn -n -sS -sV -p 22,80,443 host` |
| Safe default checks | NSE default | `nmap -Pn -n -sC -p 22,80 host` |
| Known-weak service checks | NSE vuln | `nmap -Pn -n --script vuln -p 445 host` |
| UDP services (DNS, SNMP, NTP) | UDP | `nmap -Pn -n -sU --top-ports 100 host` |
| Machine-readable evidence | output | `-oA scans/<name>` on every phase |

Do not use Nmap for HTTP path discovery, TLS configuration grading, or SQL injection. It can tell you port 443 is open and which product answers; it cannot tell you what the app does.

## Prerequisites

- `nmap --version` must print `7.94SVN`. Root or `CAP_NET_RAW` is required for `-sS`, `-sU`, `-O` and raw NSE probes; without it use `-sT`.
- `-Pn` is mandatory on filtered networks: most targets drop ICMP and the discovery phase will otherwise report every host down.
- `-n` stops reverse DNS. On a /24 that saves minutes and avoids leaking the target list to the resolver.
- This box has 2 vCPU. `--min-rate` above roughly 2000 starts losing responses and inflates false `filtered` states.
- Write output from the first packet: `-oA` keeps normal, XML and grepable forms under one basename.

## Core invocations

```sh
# 1. host discovery only, no DNS, no port scan
nmap -sn -n 10.10.10.0/24 -oA scans/discovery

# 2. fastest useful TCP picture: 1000 common ports, SYN scan, timing 4
nmap -Pn -n -sS --top-ports 1000 -T4 10.10.10.5 -oA scans/top1000

# 3. all 65535 TCP ports with a fixed packet rate and one retry
nmap -Pn -n -sS -p- --min-rate 2000 --max-retries 1 10.10.10.5 -oA scans/tcp-all

# 4. service and version detection only on ports already known open
nmap -Pn -n -sS -sV -p 22,80,443,8080 10.10.10.5 -oA scans/services

# 5. default NSE scripts plus version, the standard triage pair
nmap -Pn -n -sS -sV -sC -p 22,80,443 10.10.10.5 -oA scans/triage

# 6. raise probe intensity when a version stays "unknown"
nmap -Pn -n -sS -sV --version-intensity 7 -p 8443 10.10.10.5

# 7. NSE by category: safe checks first, then vuln only where warranted
nmap -Pn -n --script "default,safe" -p 21,22,80,443 10.10.10.5
nmap -Pn -n --script vuln -p 445,3389 10.10.10.5

# 8. NSE by name pattern, with arguments
nmap -Pn -n --script "http-title,http-headers,ssl-enum-ciphers" -p 80,443 10.10.10.5
nmap -Pn -n --script "http-brute" --script-args "http-brute.path=/admin" -p 80 10.10.10.5

# 9. selective UDP, low retries, hard host timeout (UDP is slow by nature)
nmap -Pn -n -sU -p 53,67,69,111,123,137,161,500,1900,5353 --max-retries 1 --host-timeout 10m 10.10.10.5

# 10. scan a list, skip hosts you do not own
nmap -Pn -n -sS -iL live.txt --exclude 10.10.10.1,10.10.10.254 -oA scans/batch

# 11. quieter timing for an IDS-sensitive segment
nmap -Pn -n -sS -T2 --max-rate 100 --scan-delay 200ms -p 1-1024 10.10.10.5

# 12. explain state decisions and hide closed ports
nmap -Pn -n -sS --reason --open -p 1-1024 10.10.10.5

# 13. one host, everything, only when the noise is acceptable
nmap -Pn -n -A 10.10.10.5 -oA scans/aggressive

# 14. quick reachability check before a scan campaign
nmap -Pn -n -sS -p 80,443 --reason 10.10.10.5
```

`-oA` writes `scans/<name>.nmap`, `.xml` and `.gnmap`. Parse the XML with `xmlstarlet` or `python3`, not with regex over the normal output.

## Flags that matter

| Flag | Effect | Note |
| --- | --- | --- |
| `-sn` | discovery only | no ports scanned; works with `-PS`/`-PE` probes |
| `-Pn` | skip discovery, assume up | required behind ICMP filtering |
| `-n` / `-R` | never / always resolve DNS | `-R` is noisy and slow |
| `-sS` | TCP SYN scan | needs root; half-open, fast, still logged by NDR |
| `-sT` | TCP connect scan | full handshakes, works unprivileged |
| `-sU` | UDP scan | slow; pair with `--top-ports` and `--max-retries` |
| `-sV` | service/version probes | `--version-intensity 0-9` (default 7) |
| `-sC` | default NSE set | alias for `--script=default` |
| `--script <list>` | categories, files, or patterns | comma-separated; wildcards like `http-*` work |
| `--script-args` / `--script-help` | pass arguments / read script docs | check before running intrusive scripts |
| `-p` / `-p-` / `--top-ports` | port selection | `-p-` is all 65535 |
| `--min-rate` / `--max-rate` | packets per second floor / ceiling | floor is what makes `-p-` finish |
| `-T0` to `-T5` | timing template | `-T4` for LAN, `-T2` near IDS, `-T5` unreliable |
| `--max-retries` / `--host-timeout` | cap retransmits / give up per host | essential for UDP |
| `-oA` / `-oX` / `-oN` / `-oG` | all / XML / normal / grepable | `-oA` for anything you may revisit |
| `--open` / `--reason` | hide closed ports / show why | use both in reports |
| `-O` / `-A` | OS detection / `-sV -sC -O --traceroute` | `-A` is loud and often wrong on VMs |
| `-iL` / `--exclude` | target list / exclusions | keep scope in a file you can audit |
| `--traceroute` | path discovery | adds packets, useful for segmentation maps |

## Workflow

1. **Discovery.** `-sn -n` over the in-scope CIDR. Keep the `.gnmap`; extract live IPs with `awk '/Status: Up/{print $2}'`.
2. **Top-1000 TCP.** `-sS -T4` on live hosts only. This is the phase that usually finds the web ports.
3. **Full TCP** on hosts that matter. `-p- --min-rate 2000 --max-retries 1`; expect a few minutes, not an hour.
4. **Service and version** on the open-port list only. `-sV -sC` is one pass; do not repeat it per port.
5. **Targeted NSE.** Read `--script-help` for the service you found. Run `safe` and `default` on everything, `vuln` only on services you are authorized to poke, and never `brute` without a lockout policy.
6. **UDP selectively.** Only ports justified by the host role: 53 for DNS, 161 for SNMP, 123 for NTP, 137-139 for legacy Windows.
7. **Hand off.** Feed HTTP(S) URLs to [ffuf](../ffuf/SKILL.md) or [feroxbuster](../feroxbuster/SKILL.md), then [nuclei](../nuclei/SKILL.md). Feed SMB/SSH/WinRM to [netexec](../netexec/SKILL.md).

### First 15 minutes

```sh
mkdir -p scans
nmap -sn -n 10.10.10.0/24 -oA scans/00-discovery
awk '/Status: Up/{print $2}' scans/00-discovery.gnmap > scans/live.txt
nmap -Pn -n -sS -sV -sC --top-ports 1000 -T4 -iL scans/live.txt -oA scans/01-top1000
nmap -Pn -n -sS -p- --min-rate 2000 --max-retries 1 -iL scans/live.txt -oA scans/02-tcp-all
nmap -Pn -n -sU --top-ports 50 --max-retries 1 --host-timeout 10m -iL scans/live.txt -oA scans/03-udp
```

Read `scans/01-top1000.nmap` while the full scan runs. Do not launch the UDP phase against a /24; scope it to hosts that showed UDP-dependent services.

## OPSEC and telemetry

- `-sS` never completes a handshake, but every SYN reaches the target's firewall and usually its NDR. Half-open is stealthier than `-sT`, not invisible.
- `-T4` plus `-p-` is a recognizable burst. Signature and flow sensors alert on exactly this pattern. Use `-T2 --max-rate 100` when detection matters more than time.
- `-sV` sends real probes: HTTP requests, TLS hellos, SMB negotiations. They appear in application logs with Nmap-derived payloads.
- `default` is mostly safe but not passive. `vuln` and `intrusive` scripts can crash old services or leave exploit artifacts; `dos` scripts are excluded from default scans for a reason.
- `--script vuln` runs 105 scripts on this install; each one may send several requests per port. Scope it by port and service.
- UDP probes to 161/1900 can look like amplification traffic to upstream filters.
- `-n` prevents DNS leakage. `-R` does the opposite and is visible to the resolver.
- Decoys, fragmentation and `--badsum` do not defeat modern flow analysis and mostly add noise.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| Every host is down without `-Pn` | ICMP and TCP discovery probes filtered | add `-Pn` |
| All 65535 ports `filtered` in seconds | egress firewall or host-based drop | `--reason`, try `-sT`, test one known port |
| Scan takes hours | low rate and retries on `-p-` | `--min-rate 2000 --max-retries 1`, narrow ports |
| Version shows `tcpwrapped` | load balancer or IPS closes after connect | `-sV --version-intensity 9`, or banner grab with `nc` |
| UDP results all `open|filtered` | no response is the normal UDP answer | scan fewer ports, `--max-retries 0`, accept ambiguity |
| `-sS` fails with permission error | not root / no raw socket capability | `sudo`, or `-sT` |
| NSE script errors on Lua | incompatible script or missing arg | `--script-help <name>`, drop that script |
| Output lost after a crash | no file output | always `-oA`; `--append-output` for additions |

## Verification

```sh
nmap --version | head -1                  # Nmap version 7.94SVN ( https://nmap.org )
ls /usr/share/nmap/scripts/*.nse | wc -l  # 606
nmap --script-help default | sed -n '3,4p' # address-info / Categories: default safe
nmap -Pn -n -sS -p 1 127.0.0.1            # 1/tcp closed tcpmux, no traceback
```

Keep, per phase: the exact command line, the target list, the start time, and the `-oA` basename. A port list without a timestamp is not evidence.

## Related skills

- [ffuf](../ffuf/SKILL.md) for content and parameter discovery on the HTTP ports found here
- [feroxbuster](../feroxbuster/SKILL.md) for recursive directory discovery
- [nuclei](../nuclei/SKILL.md) for template-based checks against live services
- [sqlmap](../sqlmap/SKILL.md) once a parameter looks injectable
- [netexec](../netexec/SKILL.md) for SMB, LDAP and WinRM follow-up
- [toolchain-router](../toolchain-router/SKILL.md) to pick a different tool