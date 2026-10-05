---
name: osint-threat
description: Threat intelligence skill — Shodan lookups, VirusTotal reports, SpiderFoot scans, IP/domain/hash threat assessment, breach monitoring, and dark web monitoring setup.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [osint, threat-intelligence, shodan, virustotal, spiderfoot, breach, ioc, ip-reputation, domain-reputation, dark-web, infostealer, log-market]
    triggers: [threat-intelligence, shodan, virustotal, spiderfoot, ioc, ip-reputation, domain-reputation, breach, dark-web, threat-intel, cti, infostealer, log-buying, market-entry, bootstrap-capital, session-cookie, stealer-logs]
    related_skills: [osint-recon, domain-intel]
---

# OSINT Threat Intelligence

Threat intelligence gathering — IP/domain/hash reputation analysis, Shodan internet scanning, VirusTotal malware analysis, SpiderFoot automated reconnaissance, breach data monitoring, and dark web intelligence collection methodology.

## Prerequisites

### Required MCP Servers
```yaml
mcpServers:
  shodan-mcp:
    command: npx
    args: ["-y", "@modelcontextprotocol/shodan-mcp"]
  virustotal-mcp:
    command: npx
    args: ["-y", "@modelcontextprotocol/virustotal-mcp"]
  spiderfoot-mcp:
    command: npx
    args: ["-y", "@modelcontextprotocol/spiderfoot-mcp"]
```

### Required API Keys
| Service | Key Required? | Free Tier | URL |
|---------|--------------|-----------|-----|
| Shodan | Yes | Limited (100 results/mo) | https://account.shodan.io |
| VirusTotal | Yes | 500 req/day, 4 req/min | https://www.virustotal.com/gui/join-us |
| SpiderFoot | Optional | Self-hosted, no key needed | https://www.spiderfoot.net |
| haveibeenpwned | Optional | Yes (API key available) | https://haveibeenpwned.com/API/Key |
| AlienVault OTX | Yes | Free | https://otx.alienvault.com |
| AbuseIPDB | Yes | 1000 req/day free | https://www.abuseipdb.com |
| URLScan.io | Yes | Free tier available | https://urlscan.io |
| Greynoise | Yes | Free tier (1000 req/mo) | https://greynoise.io |
| SecurityTrails | Yes | 50 req/mo free | https://securitytrails.com |

### Self-Hosted Tools
```bash
# SpiderFoot HX (full-featured, requires subscription)
# SpiderFoot CLI (free, open-source)
pip install spiderfoot

# MISP (Malware Information Sharing Platform)
# https://www.misp-project.org

# TheHive (incident response platform)
# https://thehive-project.org
```

## IOC (Indicator of Compromise) Types

| Indicator | Format | Typical Use Case |
|-----------|--------|------------------|
| IP Address | 203.0.113.42 | C2 server, scanner, attacker |
| Domain | malware.example.com | Phishing site, malware download |
| URL | https://malware.example.com/payload.exe | Specific malicious page |
| Hash (MD5) | d41d8cd98f00b204e9800998ecf8427e | File identification |
| Hash (SHA1) | da39a3ee5e6b4b0d3255bfef95601890afd80709 | File identification |
| Hash (SHA256) | e3b0c44298fc1c149afbf4c8996fb924... | File identification (most used) |
| Email | attacker@evil.com | Phishing sender |
| Registry Key | HKCU\Software\Malware | Malware persistence |
| Mutex | Global\MyMalwareMutex | Malware instance detection |
| CVE | CVE-2024-12345 | Vulnerability |

## Step-by-Step Workflows

### 1. IP Address Reputation Assessment

```python
# Full IP investigation pipeline
ip = "203.0.113.42"

# Step 1: Shodan — Internet exposure scan
shodan_result = {
    "ip": ip,
    "ports": [22, 80, 443, 3389, 8080],
    "services": ["SSH", "HTTP", "HTTPS", "RDP", "HTTP Proxy"],
    "vulnerabilities": ["CVE-2024-1234", "CVE-2023-5678"],
    "hostnames": ["server.example.com"],
    "asn": "AS12345",
    "isp": "EvilHosting LLC",
    "country": "RU",
    "city": "Moscow",
    "org": "Malware Hosting Inc",
    "last_update": "2024-01-15",
    "tags": ["malware", "c2"]  # Community tags
}

# Step 2: VirusTotal — Multi-engine scan results
virustotal_result = {
    "ip": ip,
    "malicious": 12,     # Detected as malicious by 12 engines
    "suspicious": 3,
    "harmless": 45,
    "undetected": 8,
    "last_analysis": "2024-01-15",
    "detections": [
        {"engine": "Kaspersky", "result": "Trojan.Generic"},
        {"engine": "McAfee", "result": "RDN/Generic.dx"},
    ],
    "related_domains": ["evil.com", "phish.net"],
    "related_urls": ["https://evil.com/payload.exe"],
    "resolutions": [
        {"date": "2024-01-15", "hostname": "server.evil.com"}
    ]
}

# Step 3: AbuseIPDB — Abuse reports
abuseipdb_check = {
    "ip": ip,
    "abuse_confidence": 95,    # 0-100
    "total_reports": 42,
    "categories": ["SSH Brute Force", "Port Scan", "Web Attack"],
    "last_report": "2024-01-15",
    "isp": "EvilHosting"
}

# Step 4: GreyNoise — Context (benign scanner vs. malicious)
greynoise_result = {
    "ip": ip,
    "classification": "malicious",  # benign, malicious, unknown
    "actor": "unknown",
    "cve": ["CVE-2023-1234"],
    "last_seen": "2024-01-15",
    "tags": ["Remote Access Software", "RDP Scanner"],
    "is_bot": True
}
```

### 2. Domain / URL Threat Assessment

```bash
# Step 1: VirusTotal URL scan
curl -s --request GET \
  --url "https://www.virustotal.com/api/v3/domains/evil.com" \
  --header "x-apikey: YOUR_API_KEY" | jq .

# Step 2: URLScan.io submission and results
# submit a URL for scanning
curl -s --request POST \
  --url "https://urlscan.io/api/v1/scan/" \
  --header "Content-Type: application/json" \
  --header "API-Key: YOUR_API_KEY" \
  --data '{"url": "https://evil.com/payload.exe", "visibility": "public"}'

# Step 3: WHOIS lookup
whois evil.com

# Step 4: DNS record enumeration
dig any evil.com
dig mx evil.com
dig ns evil.com
dig txt evil.com

# Passive DNS (SecurityTrails)
curl -s "https://api.securitytrails.com/v1/domain/evil.com/subdomains" \
  --header "APIKEY: YOUR_API_KEY" | jq .
```

**Domain Analysis Checklist:**
```
□ WHOIS privacy enabled? (Red flag if known malicious)
□ Recently registered? (Malicious domains are often <30 days old)
□ Matching registrar/nameserver to known bad actors?
□ SSL certificate valid? (Self-signed? Let's Encrypt? Free certs are common for phishing)
□ MX records exist? (Email server → potential phishing infrastructure)
□ Subdomains discovered? (admin.evil.com, mail.evil.com, etc.)
□ Screenshot from URLScan.io — what does the page look like?
□ Redirect chain — where does it lead?
```

### 3. File Hash Analysis (Malware)

```python
hash = "e3b0c44298fc1c149afbf4c8996fb924..."
hash_type = "sha256"

# VirusTotal file report
virustotal_file = {
    "sha256": hash,
    "md5": "d41d8cd98f00b204e9800998ecf8427e",
    "sha1": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
    "malicious": 45,      # Detections
    "suspicious": 2,
    "undetected": 10,
    "type_description": "Win32 EXE",
    "size": 1234567,
    "names": ["payload.exe", "invoice.pdf.exe"],  # Often renamed
    "first_submission": "2024-01-10",
    "last_submission": "2024-01-15",
    "last_analysis": "2024-01-15",
    "creation_time": "2024-01-09",
    "signer": "Unknown"   # Digital signature
}
```

### 4. SpiderFoot Automated Scan

```bash
# SpiderFoot CLI scan
# Targets: IP, domain, email, name, ASN, etc.

# Install spiderfoot
pip install spiderfoot

# Run scan (CLI mode)
python3 -m spiderfoot -s evil.com -t all -o json > scan_results.json

# Run scan with specific modules
python3 -m spiderfoot -s evil.com \
  -m "sfp_shodan,sfp_virustotal,sfp_whois,sfp_dns,sfp_crxcavator" \
  -o json > targeted_scan.json

# Interactive web UI (for analysis)
python3 -m spiderfoot -l 127.0.0.1:5001
# Then navigate to http://127.0.0.1:5001 in browser
```

**SpiderFoot Module Categories:**
```text
RECONNAISSANCE:
- sfp_whois — Domain registration details
- sfp_dns — DNS record enumeration
- sfp_dnsbrute — DNS brute force subdomain discovery
- sfp_certspotter — Certificate transparency logs
- sfp_crxcavator — Chrome extension analysis
- sfp_h1 — HackerOne bug bounty info

THREAT INTEL:
- sfp_shodan — Shodan.io internet scanning
- sfp_virustotal — VirusTotal multi-engine scanning
- sfp_spamcop — Spam reporting
- sfp_cins — CINS Army malicious IP list
- sfp_blocklistde — German blocklist
- sfp_abuseipdb — AbuseIPDB reports
- sfp_riskiq — RiskIQ PassiveTotal

SOCIAL:
- sfp_socialmedia — Social media presence
- sfp_email — Email address discovery
- sfp_psbdmp — Pastebin dumps
- sfp_skopen — Skype open number check

BREACH:
- sfp_haveibeenpwned — Credential breach check
- sfp_intelx — Intelligence X search
- sfp_binaryedge — BinaryEdge scans
- sfp_onionsearch — Tor hidden services
```

### 5. Breach Data Monitoring

```python
# Proactive breach monitoring

# Method 1: HaveIBeenPwned API (email addresses)
curl -s "https://haveibeenpwned.com/api/v3/breachedaccount/jane@example.com" \
  --header "hibp-api-key: YOUR_API_KEY" \
  --header "user-agent: osint-threat-skill" | jq .

# Method 2: DeHashed (paid, comprehensive)
# https://dehashed.com

# Method 3: IntelX (intelligence-x)
# https://intelx.io
# Searches: darknet, pastebin, doc sharing, etc.

# Method 4: Snusbase (paid)
# https://snusbase.com
```

**Breach Monitoring Setup:**
```bash
# Automated checking script (cron-friendly)
cat > check_breaches.sh << 'EOF'
#!/bin/bash
EMAILS="jane@example.com john@example.com"
for email in $EMAILS; do
  result=$(curl -s "https://haveibeenpwned.com/api/v3/breachedaccount/$email" \
    --header "hibp-api-key: $HIBP_KEY" \
    --header "user-agent: breach-monitor/1.0")
  echo "$(date): $email — $result" >> breach_log.txt
done
EOF
chmod +x check_breaches.sh

# Add to cron (runs weekly)
# 0 9 * * 1 /path/to/check_breaches.sh
```

### 6. Dark Web Intelligence (Surface-Level)

```python
# NOTE: True "dark web" OSINT requires specialized tools and is outside this skill's scope.
# This section covers surface-web accessible dark web intelligence.

# Tor .onion search via clearnet gateways
# Torch: http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygpta7nygbekixhcyad.onion (via Tor browser)
# DuckDuckGo: https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion

# Surface web dark web monitoring:
sources = [
    "Dread (Reddit-like on Tor) — monitoring via surface gateways",
    "RaidForums/BreachForums — surface web breach marketplaces",
    "Telegram channels — public breach announcement channels",
    "Pastebin/rentry/ghostbin — paste sites used for data dumps",
    "GitHub repos — researchers publish breach data",
]
```

**Telegram Monitoring Setup:**
```python
# Public Telegram channel monitoring (no automation requirement)
# Search for channels discussing: leaks, breaches, data dumps
# Example channels (public, for monitoring):
# - @databreaches
# - @dataleaknews
# - Industry-specific channels

# Manual monitoring workflow:
# 1. Join public breach notification channels
# 2. Set up Google Alerts for your domain/org name
# 3. Monitor paste sites for mentions
# 4. Check GitHub for exposed credentials in public repos
```

### 7. Comprehensive Threat Assessment Report

```markdown
## Threat Intelligence Report: evil.com / 203.0.113.42

### Executive Summary
**Overall Risk Rating: CRITICAL**
evil.com is a known malicious domain hosting malware payloads. The associated IP
(203.0.113.42, AS12345, Russia) actively scans for vulnerable services.

### Indicators
| Indicator | Type | Verdict | Confidence |
|-----------|------|---------|------------|
| evil.com | Domain | MALICIOUS | 95% |
| 203.0.113.42 | IPv4 | MALICIOUS | 98% |
| e3b0c442... | SHA256 | MALICIOUS | 99% |

### IP Analysis (203.0.113.42)
- **Shodan**: Ports 22,80,443,3389 open; tagged as C2 infrastructure
- **VirusTotal**: 12/68 engines detect as malicious
- **AbuseIPDB**: 95% confidence score, 42 reports (SSH brute force, web attack)
- **GreyNoise**: Classified as malicious, associated with RDP scanning
- **ASN**: AS12345 (EvilHosting, RU) — known bulletproof hosting provider
- **First Seen**: 2023-11-20 (Shodan)

### Domain Analysis (evil.com)
- **WHOIS**: Privacy enabled, registered 2024-01-05 (10 days ago)
- **Nameservers**: ns1.evildns.com, ns2.evildns.com
- **SSL**: Let's Encrypt (free, no validation)
- **URLScan.io**: Phishing page impersonating DocuSign
- **Passive DNS**: 5 historical IPs, 3 in known bad ranges
- **Subdomains**: admin.evil.com, mail.evil.com, payment.evil.com

### File Analysis (payload.exe)
- **Type**: Win32 EXE, 1.2MB
- **VT Detections**: 45/57 engines flag as malicious
- **Classification**: Trojan.Downloader (Kaspersky), Generic.Malware (McAfee)
- **First Seen**: 2024-01-10
- **Connections**: Communicates with evil.com:443

### Threat Actor Attribution
- TTPs match TA-2024-001 (EvilHosting infrastructure)
- Similar to campaigns targeting financial services
- Possible ransomware initial access vector

### Recommendations
- [ ] Block domain at DNS level
- [ ] Block IP at firewall
- [ ] Add hash to EDR blacklist
- [ ] Check internal logs for any connections to evil.com or 203.0.113.42
- [ ] Search email logs for any emails referencing evil.com
- [ ] If compromised — initiate incident response protocol
```

## Common Pitfalls

### False Positives
- **PITFALL**: IPs from shared hosting (AWS, GCP, DigitalOcean) may have prior malicious use — IP reputation alone is not reliable.
- **SOLUTION**: Cross-reference with WHOIS history, domain association, and behavioral analysis.
- **WORKAROUND**: Check if IP is cloud provider vs. dedicated/bulletproof hosting.

### Data Volume Overload
- **PITFALL**: SpiderFoot can generate thousands of findings — overwhelming and noisy.
- **SOLUTION**: Start with targeted modules, not "all". Filter by relevance to your threat model.
- **WORKAROUND**: Use tiered analysis — first pass (high confidence IOC), second pass (all data).

### API Rate Limits
- **PITFALL**: VirusTotal limits to 4 requests/minute on free tier.
- **SOLUTION**: Queue requests with delays. Use batch endpoints where available.
- **WORKAROUND**: Prioritize which IOCs to investigate based on risk score.

### Outdated IOC Data
- **PITFALL**: An IP flagged as malicious 6 months ago may now be a legitimate service.
- **SOLUTION**: Note "last seen" timestamps on all IOC reports.
- **WORKAROUND**: Check if IP/domain is still actively hosting malicious content.

### Attribution Overconfidence
- **PITFALL**: Tools like GreyNoise label actors but attribution is rarely certain.
- **SOLUTION**: Never attribute to specific APT groups without strong corroborating evidence.
- **WORKAROUND**: Describe TTPs and infrastructure patterns, not assumed nation-state actors.

## Legal & Ethical Notes

> **⚠️ WARNING**: Threat intelligence involves sensitive data:
> - **Computer Fraud and Abuse Act (CFAA)**: Do not access protected systems without authorization
> - **No Active Scanning Without Permission**: Scanning systems you don't own may be illegal
> - **GDPR**: Processing IP addresses may be considered personal data processing
> - **Data Retention**: Do not store breach data containing personal information longer than necessary
> - **Sharing Restrictions**: Threat intelligence shared with others may be subject to export controls (ITAR, EAR)
> - **Vulnerability Disclosure**: Finding a vulnerability ≠ permission to exploit it
> - **Breach Data Possession**: Possessing stolen credential databases may be illegal in some jurisdictions
> - **Anti-Hacking Laws**: Most countries prohibit unauthorized access or exceeding authorized access

### Responsible Threat Intelligence
- Share IOCs with ISAC/ISAO communities for collective defense
- Follow coordinated vulnerability disclosure (CVD) processes
- Use threat intelligence for defensive purposes primarily
- Document legal basis for any active scanning or analysis
- Do not re-victimize by redistributing stolen data

### Permissible Scanning Targets
- Your own infrastructure
- Infrastructure you have written permission to test
- Public bounty programs (HackerOne, Bugcrowd)
- Passive analysis of data already collected by Scan/Shodan/Censys

## Cross-References

- `security/osint-recon` — Full investigation pipeline including threat assessment
- `security/osint-social` — Breach data may expose social media credentials
- `security/osint-redteam` — Threat intelligence feeds into attack surface mapping
- `security/osint-facial` — Facial recognition systems as potential attack surface
- `software-development/systematic-debugging` — Structured IOC analysis methodology
- `mlops/inference/llama-cpp` — Local inference for analyzing threat data
- `research/llm-wiki` — Building a knowledge base of TTP patterns

## Reference Files

- `references/infostealer-maas-economy.md` — Infostealer Malware-as-a-Service landscape: provider pricing (Lumma $250-1000/mo, RedLine $100-200, etc.), three-layer supply chain (developers → operators → brokers), log market pricing tiers ($5-15 bulk to $500-5,000+ corporate access), Telegram auto-shop distribution, sample money-flow analysis, industry statistics, law enforcement action history (Operation Magnus, Microsoft Lumma takedown), and Fragment.com anonymous number market context. Research dated 2026-06-04, sourced from Ransomnews and cross-referenced threat intel publications.
- `references/infostealer-market-entry.md` — Operational bootstrap guide: how to enter the infostealer log market from zero capital. Covers access tiers (private forums → Telegram channels → bot markets), per-log pricing benchmarks by stealer type × freshness × geo, quality indicators, the bootstrap sequence (burner Telegram → test purchase → relationship → larger channel access), flash-funding tiers from $0 to $500 budget, free tooling, and the cookie injection flow. Research dated 2026-06-06.

## Verification Checklist

- [ ] IP checked across Shodan, VirusTotal, AbuseIPDB, GreyNoise
- [ ] Domain checked: WHOIS, DNS, SSL, URLScan.io screenshot
- [ ] File hash submitted to VirusTotal (or checked if exists)
- [ ] SpiderFoot scan completed with targeted modules
- [ ] Breach databases checked for email/domain exposure
- [ ] Threat assessment report compiled with confidence levels
- [ ] False positive risk documented
- [ ] Legal basis for investigation documented
- [ ] IOCs actionable (blockable or monitorable)
- [ ] Internal logs checked for any historical contact with IOCs
- [ ] Incident response initiated if compromise confirmed
