---
name: tools-arsenal
description: >
  Cross-domain pentest tool selection — which tool for which job, and which Security Skills skill to
  load for it. Load at engagement start or whenever a new surface appears and you need the right
  scanner/framework/wordlist. Signals: "which tool for", tool selection, arsenal, SecLists,
  PayloadsAllTheThings, searchsploit, "what do I scan this with".
domain: tools
type: arsenal
stability: learning
modes: [pentest, bugbounty, defense]
severity: info
schema_version: 1
---

# Tool selection arsenal

## When it applies
Engagement kickoff, a new surface just appeared, or you're staring at a job ("crack this hash",
"fuzz this endpoint", "exploit this CVE") and need the right tool fast. This is the routing layer
for the `tools` domain — it points at the tool *and* the Security Skills skill that teaches the
technique. Scope first, always: `tradecraft-scope-roe` + `scope.txt` before anything sends packets.

## By job

| Job | Tool | Deep skill |
|-----|------|-----------|
| Port/service discovery | nmap (masscan/rustscan for speed) | `tools-nmap`, `recon-arsenal` |
| Subdomain enum / live-host triage | subfinder → httpx | `recon-subdomain-enum`, `automation-recon-pipeline` |
| Web content/param discovery | feroxbuster, ffuf, arjun | `web-arsenal` (§2–3) |
| JS-aware crawling | katana, gospider | `recon-content-discovery` |
| Known-CVE/misconfig sweep | nuclei | `tools-nuclei`, `automation-nuclei-templates` |
| Manual web testing / intercept | Burp Suite (ZAP, mitmproxy as free/scriptable alts) | `tools-burp-suite` |
| Ground-truth HTTP / CDN 403s | curl | `tools-curl` |
| SQLi automation | sqlmap (ghauri as alt) | `tools-sqlmap`, `web-sqli` |
| SSTI automation | tplmap | `web-ssti` |
| Command injection automation | commix | `web-command-injection` |
| Offline hash cracking | hashcat (GPU), john (CPU) | `network-credential-cracking` |
| Online password attacks | hydra | `network-password-spraying` |
| Exploitation framework | Metasploit | `tools-metasploit`, `exploit-poc-development` |
| AD / Windows protocol work | impacket suite, netexec (nxc), BloodHound | `ad-pivot-arsenal`, `ad-kerberoasting` |
| Privesc enumeration | winPEAS/linpeas, Seatbelt, PowerUp | `privesc-enumeration`, `privesc-arsenal` |
| Local privilege abuse primitives | GTFOBins (Unix), LOLBAS (Windows) | `privesc-linux-gtfobins`, `privesc-windows-tokens` |
| Exploit lookup by fingerprint | searchsploit (offline Exploit-DB) | `recon-techstack-fingerprinting` |
| Agent-driven tool access | MCP bridges (kali-server, pentestMCP…) | `tools-mcp-bridges` |

## Wordlists & payload sources
- **SecLists** — the default corpus: `Discovery/Web-Content/raft-medium-directories.txt` and
  `directory-list-2.3-medium.txt` for dirs, `Discovery/DNS/subdomains-top1million-5000.txt` for
  vhosts/subdomains, `burp-parameter-names.txt` for params, `Passwords/Leaked-Databases/rockyou.txt`
  for cracking.
- **PayloadsAllTheThings** — per-vuln-class payload trees; **FuzzDB** — fuzzing dictionaries.
- **Target-specific beats generic** — `cewl <url> -m5` to harvest words from the target's own site.

## Vuln/exploit databases
Exploit-DB (+ offline `searchsploit`), NVD, MITRE CVE, Packet Storm. Look up by *fingerprinted
version*, not by product family — "Apache" is not a query, "Apache 2.4.49" is.

## Discipline
- Passive before active; active before exploitation. Log every command in the engagement workspace.
- Match rate to the RoE — scanners default to "as fast as possible", which is how you get banned or
  breach a bug-bounty program's limits.
- **Scanner output is a candidate list, not findings** — validate every hit manually
  (`reporting-triage-validation`) before it goes near a report.
- Install from official sources only; prefer distro/Kali packages over random binaries.

## References
awesome-pentest (enaqx); SecLists; PayloadsAllTheThings; HackTricks. Per-tool depth: the
`tools-*` skills in this domain.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
