---
name: recon-active
description: "Use when you have written authorization and need to directly probe the target: DNS zone transfer attempts, authoritative NS interrogation, subdomain brute forcing, reverse DNS sweeps, ICMP and TCP host discovery, and initial service discovery with dig, nmap, masscan, gobuster, and ffuf. Builds on the passive baseline from recon-passive and turns it into verified, attributable findings. Covers AXFR attempts, DNS wordlist attacks, ping sweeps with safe pacing for in-scope ranges, and logging habits that keep the work audit-clean."
version: 1.0.0
domain: recon
lifecycle: stable
last_verified: "2026-10-23"
requires:
  - recon-passive
extends: []
relates: []
tools:
  - name: dig
    version: 9.18
  - name: nmap
    version: "7.98"
  - name: masscan
    version: 1.3.2
  - name: gobuster
    version: 3.6
  - name: ffuf
    version: 2.1
---
Active reconnaissance sends packets to the target's own infrastructure. It is
noisy, attributable, and only acceptable inside a signed scope. This skill
takes the passive baseline from recon-passive (subdomain lists, name servers,
IP ranges) and verifies it by direct probing: zone transfers, DNS brute
forcing, reverse lookups, host discovery sweeps, and first-touch service
discovery. The output is a verified map of live hosts and entry points that
the nmap-methodology skill then scans in depth.

## Quick Workflow

1. Reconfirm the signed scope and log the exact commands you plan to run.
2. Attempt DNS zone transfers against every authoritative name server.
3. Interrogate delegation, glue records, and DNSSEC posture directly.
4. Brute force subdomains with gobuster or ffuf against the authoritative servers.
5. Run reverse DNS sweeps over the in-scope IP ranges.
6. Discover live hosts with ping sweeps (nmap host discovery, masscan ping).
7. Do light first-touch service discovery on confirmed live hosts.
8. Merge results with the passive baseline and hand the verified map to nmap-methodology.

## 1. Zone transfer attempts

A misconfigured name server may hand you the entire zone file in one query.
Try AXFR against each authoritative server found during passive recon. One
successful transfer replaces hours of brute forcing.

```bash
for ns in $(dig +short example.com NS @1.1.1.1); do
  echo "== Trying AXFR against $ns =="
  dig AXFR example.com @"$ns" +short | head -40
done
```

A refusal looks like `Transfer failed.` or a `REFUSED` status. A success dumps
records. Also try IXFR (incremental transfer) in case AXFR is blocked but IXFR
is forgotten:

```bash
dig IXFR=1 example.com @ns1.example.com +short | head -40
```

Log every attempt with a timestamp, successful or not. Zone transfers are one
of the first things a defender's DNS logs will show.

## 2. Direct DNS interrogation

Now you may query the authoritative servers themselves. Check delegation
health, glue records, and whether DNSSEC is actually validating.

```bash
dig +trace example.com
dig example.com NS @ns1.example.com +norecurse
dig example.com DNSKEY @1.1.1.1 +dnssec +multi
dig nonexistent12345.example.com @ns1.example.com
```

`+trace` shows the full delegation chain from the roots; lame delegations and
dangling NS records show up here. The last query tests for wildcard DNS: if a
random name resolves, brute forcing needs filtering (see Edge cases). Check
for zone walking on DNSSEC-signed zones using NSEC records (nmap-methodology
covers NSE scripts, but a manual check is cheap):

```bash
dig example.com NSEC @ns1.example.com +short
```

## 3. Subdomain brute forcing

Brute forcing resolves a wordlist of candidate names against the target's DNS.
Point the tools at the authoritative server when you want speed, or at a
public resolver when you want less direct noise. Always set a delay if the
scope owner asked for quiet scanning.

```bash
gobuster dns -d example.com -r 203.0.113.10 -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -t 50 -o gobuster-dns.txt
```

```bash
ffuf -u http://203.0.113.10 -H "Host: FUZZ.example.com" -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -mc 200,301,302,403 -o ffuf-dns.json
```

The ffuf variant catches virtual hosts: names that resolve but only answer on
specific Host headers, which pure DNS brute forcing misses. Merge new names
into the master list and resolve them:

```bash
sort -u gobuster-dns.txt >> all-subs.txt
sort -u all-subs.txt -o all-subs.txt
```

Watch for DNS rate limiting: sudden timeouts across the whole wordlist mean
the server or a middlebox is throttling you. Back off, lower threads, and
continue.

## 4. Reverse DNS sweeps

PTR records map IPs back to names and often reveal naming conventions,
internal hostnames, and forgotten assets. Sweep the in-scope ranges.

```bash
for i in $(seq 1 254); do
  dig +short -x 203.0.113.$i @1.1.1.1
done | sort -u > ptr-sweep.txt
```

For larger ranges, parallelize or use nmap's reverse DNS:

```bash
nmap -sn -n 203.0.113.0/24 --disable-arp-ping -oG - | grep -i "host:" | head -30
```

Record every PTR name; internal-style names like `vpn-02.example.com` or
`db-replica-1.example.com` are high value targets for later phases.

## 5. Host discovery

Before port scanning, find which IPs are actually alive. Start with the
least invasive methods and escalate only as needed. Never sweep ranges
outside the signed scope.

```bash
nmap -sn 203.0.113.0/24 -oN ping-sweep.txt
```

```bash
sudo masscan --ping 203.0.113.0/24 --rate 1000 -oL masscan-ping.txt
```

nmap `-sn` does ARP ping on local networks, ICMP echo, and TCP SYN to common
ports, which catches hosts that block ICMP. masscan is far faster for large
ranges but louder. If the network blocks ICMP entirely, use TCP ping against
likely-open ports:

```bash
nmap -sn -PS80,443,22 203.0.113.0/24 -oN tcp-ping-sweep.txt
```

Hosts that answer ARP but nothing else are usually firewalled; note them as
"alive but filtered" rather than dead.

## 6. First-touch service discovery

Do one light pass to learn which services exist before committing to full
scans. A top-ports SYN scan with service detection off is fast and gives you
the shape of the network.

```bash
nmap -sS --top-ports 100 --open 203.0.113.0/24 -oN top100.txt
```

This is deliberately shallow: open ports only, no version detection, no
scripts. The full treatment (scan types, timing, evasion, NSE) belongs to
nmap-methodology. If even this feels too loud for the rules of engagement,
sample a few key hosts instead of the whole range.

## 7. Merge and verify

Active results replace passive guesses. Rebuild the master target list:
every confirmed live host, every verified subdomain with its current IP,
every PTR name, and notes on which hosts are filtered. Mark anything from
passive recon that did not confirm as unverified, do not silently drop it;
a host that ignores your ping sweep may still be reachable on specific ports.

## Edge cases

- Wildcard DNS makes brute forcing useless unless you filter. Find the
  wildcard IP first (resolve a random name), then exclude results that return
  it, or use gobuster's built-in wildcard detection.
- DNS servers that rate limit will start dropping queries mid-wordlist. The
  symptom is a burst of timeouts; the fix is fewer threads and retries, not
  more aggression.
- Some authoritative servers answer queries only over TCP, or only from
  certain networks. If UDP queries time out, retry with `+tcp`.
- Hosts behind a firewall may answer ARP on a local segment but no IP
  traffic. nmap marks them up; treat them as filtered, not open.
- Cloud and CDN fronted targets (Cloudflare, AWS) mean the IPs you sweep
  belong to the provider, not the client. Confirm ownership before scanning
  shared infrastructure, and check the scope for cloud exclusions.
- IPv6 ranges are huge; never sweep a /64. Enumerate IPv6 only from
  DNS-discovered addresses and neighbor discovery on local segments.

## Escalation

When standard discovery stalls: try alternate host discovery probes (TCP ACK
ping `-PA`, UDP ping `-PU`, SCTP `-PY`) for hosts that ignore echo and SYN.
For DNS, enumerate via DNSSEC NSEC walking if the zone is signed without
NSEC3. Try common SRV records (`_sip._tcp`, `_ldap._tcp`, `_kerberos._tcp`)
which reveal service hostnames directly. If ping sweeps find nothing but you
know hosts exist, scan the full port range on a sample of IPs without host
discovery (`-Pn`); some networks drop all discovery probes but answer on
real ports. Document every escalation; each one is louder than the last.

## Detection and defender view

Active recon is visible. Defenders see: AXFR attempts in DNS server logs,
bursts of NXDOMAIN responses from brute forcing (a classic SIEM alert),
reverse DNS sweeps as PTR query floods, ICMP sweeps on perimeter IDS, and SYN
packets to closed ports from host discovery. A good blue team correlates the
source IP across all of these within minutes. Reduce your footprint by using
the agreed scanning window, throttling query rates, and scanning from the
approved source IP only. Never try to hide active scanning inside someone
else's infrastructure; spoofing source IPs during an authorized test destroys
trust and may be illegal. Your scan logs are your alibi: keep them complete.

## Key references

- MITRE ATT&CK T1595 Active Scanning
- MITRE ATT&CK T1595.001 Scanning IP Blocks
- MITRE ATT&CK T1595.002 Vulnerability Scanning
- MITRE ATT&CK T1590.002 DNS
- MITRE ATT&CK T1018 Remote System Discovery
- MITRE ATT&CK T1046 Network Service Discovery
- CWE-200 Exposure of Sensitive Information to an Unauthorized Actor
- nmap host discovery docs: https://nmap.org/book/man-host-discovery.html
- gobuster docs: https://github.com/OJ/gobuster
- ffuf docs: https://github.com/ffuf/ffuf
