---
name: tools-nmap
description: >
  Operate nmap and masscan for port/service scanning of in-scope hosts — scan-type selection
  (SYN/connect/UDP), version and OS detection, NSE vuln scripts, output formats, and the
  masscan-wide-then-nmap-deep pattern. Load when recon surfaces hosts/IPs and you need open ports,
  service versions, or OS fingerprints. Signals: nmap, masscan, -sV -sC -O, --script vuln,
  -p1-65535, --rate, "dnet: Failed to open device", top-ports, -oX.
domain: tools
type: technique
stability: learning
modes: [pentest, bugbounty, defense]
severity: info
mitre: [T1595.001, T1046]
tools: [nmap, masscan]
schema_version: 1
---

# nmap & masscan port scanning

## When it applies
You have in-scope hosts or IP ranges (confirmed in `scope.txt` — see `tradecraft-scope-roe`) and
need the network attack surface: open ports, service versions, OS guesses. This is the
active-scanning step that follows passive enumeration (`recon-subdomain-enum`, `recon-arsenal`) and
feeds service-specific testing (`network-service-attacks`, `web-arsenal` for anything HTTP).

## Why it works
nmap crafts raw packets to classify ports (open/closed/filtered) and then speaks each discovered
service's protocol just enough to fingerprint its version; its NSE script engine adds per-service
checks on top. masscan trades per-host depth for raw speed (its own TCP stack, millions of pps), so
the efficient pattern is: masscan for breadth across many hosts/ports, nmap for depth on the hits.

## Method
1. **Host discovery on a range** (skip port scan): `nmap -sn 192.168.1.0/24`.
2. **Pick the scan type:**
   ```bash
   nmap -sS target            # SYN half-open scan — default when root; fast, less logging
   nmap -sT target            # full TCP connect — use when unprivileged or raw sockets fail
   nmap -sU --top-ports 100 target   # UDP is slow; always bound it to top ports
   ```
3. **Identify what is listening:**
   ```bash
   nmap -sV --version-intensity 5 -sC target   # service versions + default scripts
   nmap -O target                              # OS fingerprint (needs root)
   nmap -A target                              # OS + version + scripts + traceroute (loud)
   ```
4. **Size the port list to the phase:** `-F` (fast, top 100) for a first look; `-p 22,80,443` for a
   targeted check; `-p-` for full 65535 when the rules of engagement allow the noise.
5. **NSE scripts after fingerprinting** — never `--script vuln` as a first move:
   ```bash
   nmap --script vuln target                              # known-vuln checks (loud)
   nmap --script smb-enum-shares,smb-enum-users target    # SMB surface
   nmap --script http-enum,http-vuln* -p 80,443 target    # web surface
   ```
6. **Always save output** for the engagement record: `-oN` normal, `-oX` XML (importable, feeds
   other tools — e.g. `ncrack -iX scan.xml`), `-oG` greppable.
7. **Wide/fast with masscan, then deep with nmap:**
   ```bash
   masscan -p1-65535 target --rate=1000              # rate is packets/sec — tune to the link
   masscan -p80,443,8080 10.0.0.0/24 --rate=500 --banners
   masscan -p1-65535 10.0.0.0/8 --rate=10000 -e eth0 --excludefile exclude.txt
   ```
   `--excludefile` is how you hard-exclude out-of-scope addresses from a wide sweep; masscan output
   flags (`-oJ/-oX/-oG`) mirror nmap's.

## Gotchas
- **Windows: `dnet: Failed to open device eth0`** — raw-socket scans fail on some Windows installs;
  fall back to `nmap -sT -sV --top-ports 50 -Pn -T3 target` (connect scan, no host-discovery
  dependency). If it still fails, record it as an environment limitation and continue with
  HTTP-layer recon — do not let nmap block the engagement.
- **Targets behind Cloudflare/CDN** — a full raw port scan of a CDN edge tells you almost nothing
  and burns rate budget; pivot to the application layer (HTTPS/API/JS) instead.
- **Scanner output is not a finding** — a `vuln` script hit or an open port is a lead; verify
  exploitability before it goes in the report (`reporting-triage-validation`).
- **Rate = detection + DoS risk** — high `--rate` / `-T5` trips IDS and can flatten weak services;
  match tempo to the RoE. masscan against ranges you don't own is exactly what `scope.txt` forbids.
- **`-Pn` when hosts "look down"** — many hosts drop ICMP; `-Pn` skips ping discovery, at the cost
  of scanning dead hosts.
- **SYN scan needs root** — `-sS` as an unprivileged user silently degrades or errors; use `-sT`.

## Verify success
You have a saved scan file (`-oX`/`-oN`) whose results you can restate as: live hosts, open ports,
service + version per port, and a prioritized list of which services get deep testing next — every
entry inside `scope.txt`.

## References
nmap.org reference guide; NSE script library; masscan GitHub (robertdavidgraham). Pipeline context:
`automation-recon-pipeline`; next step per service: `network-service-attacks`.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
