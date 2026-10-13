---
name: recon-arsenal
description: >
  One line: port/host/service discovery tool arsenal for authorized engagements. Pack in trigger
  signals so it auto-loads: "new target", "enumerate", "scan", an in-scope target,
  open-port lists needing deeper enum. Authorized, in-scope targets only.
domain: recon
type: arsenal
stability: locked
modes: [pentest, bugbounty]
schema_version: 1
---

# Recon / enumeration arsenal

Tool selection for port/host/service discovery on **authorized lab targets only**
(in-scope hosts recorded in `scope.txt`). Pick the tool, run the exact command,
log the reasoning in `notes.md`.

## 1. Port / service scanning

**nmap** — the workhorse; scriptable, accurate service/version detection, keeps you honest.
- `nmap -sC -sV -oA recon/nmap-tcp $TARGET` — `-sC` default NSE scripts, `-sV` version detection, `-oA` writes .nmap/.gnmap/.xml (feed later tools).
- `nmap -p- --min-rate 5000 -oA recon/nmap-allports $TARGET` — `-p-` all 65535 ports, `--min-rate` forces pace so it finishes.
- `nmap -sC -sV -p 22,80,445 -oA recon/nmap-targeted $TARGET` — re-scan only the ports `-p-` found, deeply.
- `nmap -sU --top-ports 100 -oA recon/nmap-udp $TARGET` — `-sU` UDP; slow, so cap to top ports.
- `nmap -sV --version-intensity 9 -p 4444 $TARGET` — max probe effort on a stubborn/unknown service port.
- `nmap -Pn -sC -sV $TARGET` — `-Pn` skip host-discovery ping (hardened hosts often drop ICMP → "host down").
- `nmap --script "smb-enum-shares,smb-os-discovery" -p445 $TARGET` — targeted NSE; `--script vuln` for a vuln sweep.
- Gotcha: run the fast `-p-` sweep FIRST, then `-sC -sV` only the open ports — scripts on all 65535 ports wastes minutes.

**rustscan** — sweeps all ports in seconds, then hands off to nmap; use it to find the open set fast.
- `rustscan -a $TARGET --range 1-65535 -- -sC -sV` — everything after `--` is passed straight to nmap.
- Gotcha: on flaky VPN, add `--ulimit 5000` and lower `-b` (batch) or it drops ports.

**masscan** — asynchronous, fastest for wide ranges; prefer it over rustscan/nmap for whole /24 subnet sweeps.
- `masscan -p1-65535 10.129.0.0/24 --rate 1000 -oL recon/masscan.txt` — `--rate` packets/sec (keep modest on VPN).
- Gotcha: no version detection — always re-scan the hits with `nmap -sV`.

## 2. Host discovery / ping sweep

**nmap -sn** — quick liveness map of a subnet without port-scanning.
- `nmap -sn 10.129.0.0/24 -oA recon/hosts` — `-sn` ping-only, no ports.

**fping** — faster mass-ping alternative; good in a script loop.
- `fping -a -g 10.129.0.0/24 2>/dev/null` — `-a` show alive only, `-g` generate range.

## 3. DNS & vhost discovery

**dig** — first check for a zone transfer, the easy win.
- `dig axfr @$TARGET domain.local` — AXFR full zone dump if the DNS server allows it.
- `dig any domain.local @$TARGET` — pull all records.

**dnsenum** — automated brute + AXFR + record enum in one shot.
- `dnsenum --dnsserver $TARGET domain.local`

**gobuster dns** — subdomain brute-force against a DNS server.
- `gobuster dns -d domain.local -r $TARGET -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt`

**ffuf (vhost fuzzing)** — find name-based virtual hosts behind one IP via the `Host:` header.
- `ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -u http://$TARGET -H "Host: FUZZ.domain.local" -fs 0` — `-fs` filter by size; set it to the wildcard/default page size to hide noise.

**gobuster vhost** — same idea, gobuster syntax.
- `gobuster vhost -u http://domain.local --append-domain -w <wordlist>`

**wfuzz** — flexible fallback when you need custom filtering.
- `wfuzz -c -w <wordlist> -H "Host: FUZZ.domain.local" -u http://$TARGET --hh <hide-chars>`
- Gotcha: any hostname you discover must go in `/etc/hosts` (`$TARGET domain.local sub.domain.local`) — `*.local` names don't resolve otherwise, and vhost routing needs the Host header to match.

## 4. SMB / RPC / NetBIOS

**enum4linux-ng** — modern rewrite; one command dumps shares, users, groups, OS, null sessions.
- `enum4linux-ng -A $TARGET` — `-A` all enumeration.

**smbclient** — list and browse shares directly.
- `smbclient -N -L //$TARGET` — `-N` no password (null session), `-L` list shares.
- `smbclient -N //$TARGET/share` — connect to one share.

**rpcclient** — null-session RPC; enumerate users/SIDs when SMB shares are locked down.
- `rpcclient -U "" -N $TARGET` — then `enumdomusers`, `queryuser 0x<rid>`.

**nmblookup** — NetBIOS name/workgroup resolution.
- `nmblookup -A $TARGET` — `-A` query by IP.

**netexec (nxc / crackmapexec)** — fast auth + share sweep, great for spraying/null checks.
- `nxc smb $TARGET -u '' -p '' --shares` — null-session share listing.
- `nxc smb $TARGET -u user -p pass --shares` — authenticated view once you have creds.
- Gotcha: `crackmapexec` is deprecated → use `nxc` (netexec); same flags.

## 5. SNMP

**snmpwalk** — dump the MIB when SNMP (UDP 161) is open; often leaks users, processes, routes.
- `snmpwalk -c public -v2c $TARGET` — `-c public` default community string, `-v2c` version.

**onesixtyone** — brute the community string first if `public` fails.
- `onesixtyone -c /usr/share/seclists/Discovery/SNMP/common-snmp-community-strings.txt $TARGET`

## 6. NFS

**showmount** — list exported shares before mounting.
- `showmount -e $TARGET` — `-e` show exports; then `mount -t nfs $TARGET:/export /mnt/nfs`.

## 7. Quick service probes

**nc** — grab a raw banner on any TCP port.
- `nc -nv $TARGET 21` — `-n` no DNS, `-v` verbose.

**curl** — inspect HTTP headers/redirects without a browser.
- `curl -sI http://$TARGET` — `-s` silent, `-I` headers only (Server, redirects, cookies).

**ldapsearch** — anonymous bind against LDAP (389) leaks the naming context / users.
- `ldapsearch -x -H ldap://$TARGET -b "dc=corp,dc=local"` — `-x` simple auth, `-b` search base.
- `ldapsearch -x -H ldap://$TARGET -s base namingcontexts` — find the base DN first.

**ftp** — anonymous login check on 21.
- `ftp $TARGET` → login `anonymous` / any password; `ls -la` for readable/writable dirs.

## 8. All-in-one

**autorecon** — fires the whole suite (nmap + per-service enum) and files the output; use as a background first pass while you work leads manually.
- `autorecon $TARGET` — writes structured `results/` per host.
- Gotcha: on real engagements, **manual > automated** — autorecon is a starting map, not a substitute for reading each service yourself.

## Gotchas / discipline
- Hardened hosts frequently show ports `filtered` and drop ICMP → always add `-Pn`, and `--min-rate 5000` so scans don't stall.
- Always run a full `-p-` scan AFTER the top-1000 — the interesting service (WinRM 5985, a dev port, a hidden vhost) is often up in the high ports.
- UDP is slow and unreliable — scan `--top-ports 100` only, don't wait on a full `-sU -p-`.
- Re-scan discovered ports with `-sC -sV`; a fast sweep tells you *what's open*, not *what it is*.
- Golden rule: **when stuck, enumerate more** — a missed service, subdomain, or share is far more likely than a missing exploit.
