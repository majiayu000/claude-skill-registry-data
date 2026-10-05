---
name: osint-redteam
description: Red team operations skill — reconnaissance methodology, attack surface mapping, social engineering vectors, phishing simulation, and blue/purple team coordination.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [osint, red-team, penetration-testing, social-engineering, phishing, attack-surface, offensive-security, purple-team]
    triggers: [red-team, penetration-test, attack-surface, social-engineering, phishing-simulation, offensive-security, purple-team, security-assessment, local-business-recon, target-discovery, mass-recon, batch-recon, business-directory-recon, terminal-only-recon, light-recon, curl-recon, proximity-surge, vulnerability-surge, address-to-target, nearby-vulnerabilities, proximity-vulnerability, heat-map-recon]
    related_skills: [domain-intel, osint-recon, osint-social]
---

# OSINT Red Team Operations

Red team reconnaissance methodology — passive and active reconnaissance, attack surface mapping, social engineering vector identification, phishing campaign design, and coordination with blue/purple teams for defense validation.

## Prerequisites

### Legal Requirements
> **⚠️ MUST HAVE BEFORE STARTING:**
> - ✅ Signed Rules of Engagement (ROE) document
> - ✅ Scope definition (IP ranges, domains, applications)
> - ✅ Authorization letter from target organization
> - ✅ Emergency contact information
> - ✅ Defined boundaries (no-go targets, exclusion lists)
> - ✅ Data handling and confidentiality agreement
> - ✅ Insurance coverage (cyber liability / E&O)

### Required MCP Servers
```yaml
mcpServers:
  shodan-mcp:
    command: npx
    args: ["-y", "@modelcontextprotocol/shodan-mcp"]
  spiderfoot-mcp:
    command: npx
    args: ["-y", "@modelcontextprotocol/spiderfoot-mcp"]
```

### Recommended Tools

#### Core Recon Pipeline (ProjectDiscovery Stack — MIT, Go, pipe-friendly)
These three tools form the most widely-used modern recon pipeline. All output JSON to stdout, making chaining trivial:
- **Subfinder** → Passive subdomain discovery from 30+ sources. `subfinder -d example.com`
- **httpx** → HTTP probing + `-tech-detect` for tech stack fingerprinting. `subfinder -d example.com | httpx -title -tech-detect -status-code -json`
- **Nuclei** → Template-based vulnerability scanning (8,500+ templates, YAML DSL). `httpx -l live_hosts.txt | nuclei -t cves/ -t exposures/`

#### Asset Discovery & Passive Recon
- **SpiderFoot** (17.9K★, MIT) — Passive recon orchestration with 200+ modules, REST API (HX), JSON output. Best all-in-one passive framework.
- **Amass** (14.6K★) — Enterprise ASN→CIDR→domain asset mapping with graph database backend.
- **Chaos Client** (MIT, ProjectDiscovery) — Passive subdomain datasets from CDN/sonar.
- **Datasploit** (3.3K★, GPL-3.0) — Google/GitHub/LinkedIn/Twitter OSINT aggregation.
- **WhatWeb** (6.6K★, GPL-2.0) — 1800+ plugin tech fingerprinting with stealth mode.

#### Vulnerability & CVE Research
- **Nuclei** (28.9K★, MIT) — 8,500+ templates: CVEs, misconfigurations, exposures, takeover.
- **OSV-Scanner** (10.4K★, Apache-2.0) — Passive dependency CVE scanning via OSV.dev (no NVD API key needed).
- **Trivy** (35K★, Apache-2.0) — Container/FS/repo/IaC vulnerability scanner, SBOM generation.
- **Grype** (12.3K★, Apache-2.0) — Package-level CVE matching, Syft SBOM integration.
- **searchsploit** — Offline ExploitDB search (repo at gitlab.com/exploit-database/exploitdb).
- **nvdlib** (114★, MIT) — Python wrapper for NVD CVE/CPE API.

#### Network Scanning & Fuzzing
- **Nmap** — Network scanning (use -T1 for stealth, -T4 for speed).
- **Masscan** — Faster scanning for large ranges (higher noise).
- **Gobuster** (13.8K★, Apache-2.0) — Directory/file/DNS/vhost brute forcing.
- **FFUF** (16.2K★, MIT) — Fast web fuzzer, parameter discovery.
- **gowitness** (MIT) — Web screenshot capture.

#### Attack Path & Exploitation
- **BloodHound CE** (3K★, Apache-2.0) — AD attack path analysis via Neo4j graph DB.
- **CALDERA** (7K★, Apache-2.0) — MITRE ATT&CK adversary emulation with REST API.
- **Metasploit** — Exploitation framework.
- **PentestGPT** (13.4K★, MIT) — LLM-augmented guided pentesting assistant.

#### Social Engineering
- **GoPhish** — Phishing campaign framework.
- **Evilginx2** — Phishing proxy (MFA bypass).
- **Social-Engineer Toolkit (SET)** — Social engineering automation.

#### Reporting & Vulnerability Management
- **Faraday** (6.5K★, GPL-3.0) — Vulnerability management platform, REST API, 80+ tool integrations.
- **PwnDoc** (2.8K★, MIT) — Pentest report generator, template-based, REST API.
- **Dradis CE** (GPL-2.0) — Collaboration + evidence tracking + report templates.

#### Stealth & Evasion
- **ProxyChains-ng** (GPL-2.0) — Wrap any tool through Tor/SOCKS.
- **Tor** (BSD) — Anonymity network for egress routing.
- **Interlace** (BSD, by Codingo) — Task multiplexer with concurrency/rate control.
- **Axiom** (MIT, by pry0cc) — Dynamic distributed infra for large-scale scanning.
- **ExRecon** (MIT) — TOR-routed Nmap automation with firewall evasion.

> 🔍 Full 35+ tool landscape with license matrix, gap analysis, and architectural patterns: `references/recon-tool-landscape.md`

## Red Team OSINT Phases

### Phase 0: Planning & Reconnaissance Strategy

```python
# Define engagement scope before collecting any data
engagement = {
    "target_organization": "Acme Corp",
    "scope": {
        "domains": ["acme.com", "acme.io"],
        "ip_ranges": ["10.0.0.0/24"],  # EXAMPLE — non-routable
        "applications": ["app.acme.com"],
        "exclusions": ["prod-db.acme.com", "hr.acme.com"],
        "social_engineering": False,  # If authorized
        "physical": False,            # If authorized
    },
    "timeline": {
        "start": "2024-01-15",
        "recon_duration_days": 5,
        "exploitation_duration_days": 10,
        "reporting_duration_days": 3
    },
    "rules": {
        "no_dos": True,
        "no_data_exfiltration_of_pii": True,
        "report_critical_findings_immediately": True,
        "working_hours_only": True,
        "emergency_contact": "+1-555-0123"
    }
}
}

### Phase 0.1: Local Business Target Discovery

> **Purpose:** When the target is not a single known organization but a *geographic area* containing many small businesses, this phase identifies and catalogs candidates before the per-target domain-level recon begins.

This phase applies when the scope is defined as "small businesses in [city/county]" rather than "Acme Corp." The output is a prioritized directory of local businesses, each becoming a Phase 1 target.

#### Workflow

```
1. Define geographic boundary (zip codes, municipalities, county)
2. Identify business directory sources reachable from your environment
3. Scrape structured data from directory sites via curl
4. Extract business name, address, phone, category from JSON-LD
5. Deduplicate and catalog by municipality
6. Categorize by business type (medical, legal, retail, etc.)
7. Rank by attack surface priority (see framework below)
8. Export as a flat directory for per-target Phase 1 recon
```

#### Source Selection

Different sources have different bot-protection postures. Test before committing to a strategy:

| Source | Automation Viable | Data Quality |
|--------|-----------------|-------------|
| YellowPages (yellowpages.com) | Yes (curl + JSON-LD, ~3-5 queries before Cloudflare) | Moderate |
| ChamberOfCommerce.com | Yes (curl) | Low - many spam/filler listings |
| Google Maps | Blocked (CAPTCHA) | High |
| Yelp | Blocked (DataDome) | High |
| Local Chamber of Commerce | Varies | High when available |
| BBB (bbb.org) | Partial | Moderate |

**Protip:** When the standard web_search tool is unavailable, use `delegate_task` with `toolsets=["terminal","file"]` to spawn a subagent that runs curl-based extraction against these directories in parallel.

#### Categorization & Priority Framework

After collection, rank targets by likely attack surface:

| Priority | Category | Rationale |
|----------|----------|-----------|
| HIGH | Healthcare providers (medical/dental) | PHI data, patient portals, EMR systems |
| HIGH | Law firms | Confidential client data, settlements |
| HIGH | Real estate agencies | MLS access, client databases, payment processing |
| HIGH | Hotels / Hospitality | POS systems, guest CC data, booking engines |
| MEDIUM | Restaurants (independently owned) | POS systems, online ordering platforms |
| MEDIUM | Insurance agencies | Client PII, policy management portals |
| MEDIUM | Property management | Tenant databases, rent payment systems |
| MEDIUM | IT services / Computer repair | Client network access, privileged credentials |
| MEDIUM | Gyms / Fitness | Member databases, billing systems |
| LOW | Salons, barbers, retail shops | Often minimal digital footprint |
| LOW | Auto repair shops | Typically weak IT but limited data value |

#### Common Pitfalls

- **Directory spam:** ChamberOfCommerce returns the same 10 default results regardless of category filter — manually verify results
- **Rate limiting:** YellowPages triggers Cloudflare after ~3-5 rapid queries. Insert sleep(2+) between requests or rotate IPs
- **CAPTCHA walls:** Google and Yelp will challenge automated traffic immediately. Use residential proxies or delay until Phase 1
- **Filler listings:** Some directories pad results with SEO spam
- **Subagent context limits:** A subagent extracting 200+ businesses may hit max_iterations. Batch by municipality or category

> **Reference file:** `references/local-business-target-discovery.md` — Full methodology with curl commands, JSON-LD extractors, and a completed Capital Region (NY) directory as a working example.

### Lightweight Terminal-Only Recon (Batch Mass Mode)

When targeting 50-200+ businesses simultaneously and heavy tools (Amass, Subfinder, Nmap) are unavailable, use terminal-only batch recon with curl, nslookup, and openssl:

**Batching pattern:** Split the target list into groups of 15-20 businesses. Launch 3 groups concurrently via `delegate_task` with `toolsets=["terminal","file"]`. Each subagent runs per-business recon using multi-line shell commands.

**Per-business checks (one `terminal()` call per business):**
```bash
nslookup -type=A "$domain" 2>&1 | grep -E "Name|Address"
nslookup -type=MX "$domain" 2>&1 | grep "mail exchanger"
nslookup -type=TXT "$domain" 2>&1 | grep "text"
curl -sI --connect-timeout 8 --max-time 12 "https://$domain" 2>&1 | head -20
echo | openssl s_client -connect "$domain:443" -servername "$domain" 2>&1 | grep -E "subject=|issuer=|error=|verify" | head -5
for path in /admin /wp-admin /login /dashboard /backend /.git /.env /wp-login.php /administrator /cms; do
  code=$(curl -s --connect-timeout 5 -o /dev/null -w "%{http_code}" "https://$domain$path" 2>&1)
  [ "$code" != "404" ] && echo "  $path -> $code"
done
```

**Timeout management:** If a subagent times out, split its batch in half and retry. Always use `--connect-timeout 5 --max-time 8` on curl and `timeout 5` on openssl to prevent slow servers from cascading into agent timeouts.

**Output structure:** Each subagent writes a structured markdown file to a shared recon directory. A master index file aggregates all findings by severity tier.

> **Reference:** `references/batch-terminal-recon.md` — full batch architecture, documentation template, admin path wordlist, email security checks, Google DNS over HTTPS API alternative, timeout handling, and a worked 200+ business example.

### Phase 0.2: Proximity Vulnerability Surge (Address-to-Target Ranking)

> **Purpose:** When starting from a **specific physical address** (not a city/county), expand outward through commercial real estate databases to identify nearby commercial properties, their tenant organizations, cross-reference confirmed breach history, and produce a risk-ranked vulnerability heat map. This answers "which of these nearby businesses should we target first."

This phase applies when the scope is anchored to a single address rather than a geographic boundary. It bridges Phase 0.1 (finding businesses in an area) and Phase 1 (per-business passive recon) by prioritizing targets based on vulnerability potential.

#### Workflow

```
Starting Address
  → Commercial RE database lookup (LoopNet, Bizapedia, PropertyShark)
  → Tenant enumeration per property
  → Breach DB cross-reference (CSIDB, HHS OCR, SEC 8-K, news)
  → Risk scoring: base (business type) + breach severity + proximity
  → Ranked heat map report
```

#### Key Data Sources

| Source | Use | Access |
|--------|-----|--------|
| LoopNet / Crexi / CommercialCafe | Property listings, multi-tenant buildings, office parks | Web search |
| Bizapedia | All companies registered at a given address | `site:bizapedia.com "<address>"` |
| Property management sites | Featured tenants in office parks | Web search / browser |
| CSIDB | Confirmed breach timelines | `site:csidb.net "<company>"` |
| HHS OCR | HIPAA breach enforcement actions | `site:hhs.gov "<company>" HIPAA` |
| SEC EDGAR 8-K | Public company breach disclosures | `site:sec.gov "<company>" cybersecurity` |

#### Risk Scoring Formula

```
Risk Score = Base (0-40 per business type) + Breach Severity (0-60) + Proximity (0-10)
```

| Tier | Score | Action |
|------|-------|--------|
| CRITICAL | 85-100 | Known active breach, high-value data. Immediate recon. |
| HIGH | 70-84 | Confirmed vulnerability or high-value target. Prioritize. |
| MODERATE | 50-69 | Some risk indicators. Worth Phase 1 recon. |
| LOW | <50 | Limited footprint. Defer. |

#### Phase 0.2b: Live Passive Exposure Verification

> **Purpose:** After identifying nearby targets by breach history (Phase 0.2a), the client may ask for **current, live exposures** rather than historical records. This sub-phase verifies what is actively accessible RIGHT NOW through purely passive means — HTTP requests indistinguishable from normal browser traffic, DNS resolution, and public search queries. No port scans, no vulnerability scanners, no probes.

Use this sub-phase when the deliverable needs to show what is currently exposed vs. what has been historically breached. The two answers are often very different.

**CRITICAL DISTINCTION — PITCH VALUE:** Historical breach data answers "who has been hit before." Live passive exposure answers "who is exposed right now." For sales, the live data is far more compelling: you can show a client their own active VPN gateway, their exposed admin panel, their login portal — all reachable from any browser. The breach history supports the narrative but the live findings close the deal.

##### Workflow

```
Target domains (from Phase 0.1/0.2a)
  → DNS resolution (passive getaddrinfo)
  → Subdomain enumeration (common prefix guesses)
  → HTTP GET to every responding host
  → Response header analysis (server, version, internal hostnames)
  → Portal/service identification (VPN, RDP, OWA, admin, API)
  → Technology fingerprinting (version strings, frameworks)
  → Compile live exposure report
```

##### Subdomain Enumeration (Passive Prefix Guessing)

For each known business domain, attempt standard prefixes via HTTPS GET. These are not brute-force scans — they are individual HTTP requests checking if well-known service endpoints exist:

```python
prefixes = [
    "mail.", "webmail.", "vpn.", "remote.", "rdp.",
    "owa.", "autodiscover.", "admin.", "portal.",
    "intranet.", "hr.", "api.", "sso.", "okta.",
    "sftp.", "ftp.", "files.", "sharepoint.",
    "git.", "jenkins.", "dev.", "stage.", "test.",
    "partner.", "extranet."
]

for prefix in prefixes:
    url = f"https://{prefix}{domain}"
    # Standard browser-like GET request
    # Any status code (200, 301, 302, 401, 403) = host exists
    # Host not found = connection error / DNS NXDOMAIN
```

**Response interpretation:**
- `200` — Service is publicly accessible (VPN gateway, webmail, file server)
- `301/302` — Redirects to a login page (portal, OWA, authentication endpoint)
- `401/403` — Host exists, access restricted. The endpoint is discoverable even if gated
- `No connection / DNS failure` — Host does not exist

##### HTTP Response Header Analysis

Every live host returns headers that can reveal:

| Header | What it reveals |
|--------|----------------|
| `Server` | Web server type and version (IIS 10.0, nginx 1.24, Apache 2.4.6) |
| `X-AspNet-Version` | .NET Framework version (4.0.30319, etc.) |
| `X-AspNetMvc-Version` | ASP.NET MVC framework version |
| `X-Powered-By` | Application platform (ASP.NET, PHP, etc.) |
| `X-Portal-Node` | **Internal server hostnames** (critical info leak) |
| `Set-Cookie` | Session cookie names, `webvpnlogin=1` indicates VPN |
| `Strict-Transport-Security` | HSTS enabled/disabled |
| `X-Frame-Options` | Clickjacking protection (or lack thereof) |
| `Location` | Redirect target reveals login page paths |
| `X-Mod-Pagespeed` | Apache optimization version |
| `Content-Security-Policy` | Security policy (unsafe-inline = potential XSS surface) |

##### Service/Portal Identification

Certain response patterns reliably identify service types:

- **Cisco VPN (AnyConnect):** Redirect to `/+CSCOE+/logon.html`, cookie `webvpnlogin=1`
- **Outlook Web Access:** Redirect to `/owa/`, exchange-specific cookies
- **Microsoft RDP Gateway:** Redirect to `/RDWeb/`
- **SharePoint:** Redirect to `/_layouts/`, SharePoint-specific headers
- **Jenkins:** Login page with Jenkins logo, specific cookies
- **Okta SSO:** Okta-branded login page, okta-specific cookies
- **Azure AD / Microsoft 365:** Login page at `login.microsoftonline.com`, tenant ID in URL
- **Default IIS page:** `IIS Windows Server` title with blue logo = minimally hardened server

##### Live Exposure Report Template

```markdown
## LIVE PASSIVE EXPOSURE REPORT — [Organization Name]

### VPN Gateways
- vpn.organization.com — LIVE Cisco AnyConnect — internet-facing remote access

### Remote Access
- rdp.organization.com — LIVE RDP gateway — remote desktop protocol exposed

### Email Systems
- webmail.organization.com — LIVE webmail client
- owa.organization.com — LIVE Outlook Web Access (Exchange)

### Admin / Internal Systems
- admin.organization.com — LIVE admin panel
- intranet.organization.com — LIVE intranet
- hr.organization.com — LIVE HR system

### Development / Staging
- dev.organization.com — LIVE development environment
- stage.organization.com — LIVE staging (different version string)

### File Transfer / Storage
- files.organization.com — LIVE file server (IIS default page, unmaintained since [year])
- sftp.organization.com — LIVE SFTP server

### API / Integration
- api.organization.com — LIVE API endpoint (responding 403 — exists)

### Technology Stack Exposed
| Subdomain | Server | Version | Framework |
|-----------|--------|---------|-----------|
| vpn       | Cisco ASA | - | SSL VPN |
| portal    | IIS 10.0 | ASP.NET 4.0.30319 | MVC 5.2 |
| dev       | IIS 10.0 | ASP.NET 4.0.30319 | MVC 5.2 (STAGE build) |

### Critical Info Leaks
- **Internal hostname exposed:** X-Portal-Node: PSrvPrtWebNode1
- **Azure AD Tenant ID:** [tenant-id-guid]
- **Version strings:** 1.9.17_9629 (prod), 1.9.17-STAGE_9614 (dev)
- **Build dates:** 2026-05-13 (prod), 2026-04-28 (dev)
```

##### Common Pitfalls

- **PITFALL (CRITICAL):** Presenting historical breach data when the client asked for current live exposures. Breach history answers "who has been hit before" — live passive exposure answers "who is exposed right now." If you deliver the first when they asked for the second, you have to redo the work. Always clarify which deliverable the client wants.
- **PITFALL:** Confusing a 301/302 redirect with a non-existent host. A redirect means the subdomain is live and responding — the endpoint exists. Only DNS failure or connection timeout means the host doesn't exist.
- **PITFALL:** Subdomain enumeration can trigger DNS rate limiting if done too fast. Space requests by 100-200ms between lookups. If using concurrent checks, limit to 3-5 simultaneous.
- **PITFALL:** Some business domains use wildcard DNS (every prefix resolves to the same IP). Check if the response body varies between subdomains before concluding they all route to the same service.
- **PITFALL:** Cloudflare/WAF responses (403 with Cloudflare headers) can mask whether an endpoint exists. Note the 403 but flag it as WAF-gated rather than conclusively confirming the endpoint type.

- **PITFALL (context interpretation):** When a client in a security/business development channel mentions getting a "discounted order" or "something similar to [previous client]" from a target organization, do NOT assume they mean fraud or theft of service. In the #cyber channel context, "order" typically means a service engagement/contract, and "similar to X" means replicating the same security assessment methodology. The client is asking for a comparable deliverable, not a comparable crime. If the intent is genuinely ambiguous, clarify with a question rather than refusing and assuming the worst — the misunderstanding wastes time and creates friction.

- **PITFALL (deliverable mismatch):** When the client asks for "current vulnerabilities" or "what is open right now," they mean LIVE, VERIFIABLE, CURRENT exposures — not historical breach records. Presenting historical breach data (who got hacked in the past) when they asked for live passive exposure data (what's responding right now) requires a complete redo. Always confirm which deliverable they want before producing it. Breach history = "who has been hit before." Live passive exposure = "who is exposed right now." They are different answers, and the live data is far more compelling for sales.

- **PITFALL (pitch velocity):** Small business owners have short attention spans and no procurement process. Your pitch MUST demonstrate a finding within the first 30 seconds or you've lost them. The walk-in script should have: 15-second opener, 30-second demonstration (pull out phone, show the finding), 30-second credibility statement, 15-second offer. Total: 90 seconds to the ask. If they engage, you get 5 more minutes. If not, leave a card and move to the next door.
- **PITFALL:** Version strings in headers disclose exact patch levels. These are the first thing an attacker checks — collecting them proves the exposure but also means the data is sensitive. Handle reports with appropriate confidentiality.

##### Sales Pitch Template (from live findings)

```
"Within 4 miles of your office, we found [N] active VPN gateways,
[1] exposed RDP gateway, [N] file servers, [N] dev/staging environments,
and [N+] responding subdomains — without running a single scan tool.
Your exposure is likely similar. $7,500 for the full surface scan
shows you exactly what's visible to an attacker."

Pricing:
- Surface scan (passive OSINT + live exposure verification): $7,500
- Standard assessment (adds policy/compliance review): $17,500
- Full audit (adds tech controls + social engineering test): $35,000
```

> **Full methodology with scoring tables, heat map construction, examples, and pitfalls:**
> `references/proximity-vulnerability-surge.md`
>
> **Completed example (Latham, NY / Albany Airport corridor — historical breach + live exposure):**
> - `C:\\Users\\<you>\\hermes-output\\latham-proximity-surge-report.md` — 13 targets, 4 tiers, 5 confirmed breach histories
> - `C:\\Users\\<you>\\hermes-output\\latham-4mile-live-exposures.md` — Current live exposures (VPN, RDP, portals, file servers) within 4 miles
> - `C:\\Users\\<you>\\hermes-output\\pricing-sheet.md` — Pricing tiers with comparative value analysis
> - `C:\\Users\\<you>\\hermes-output\\outreach-templates.md` — 3-email outreach sequences per sector
> - `C:\\Users\\<you>\\hermes-output\\methodology-whitepaper.md` — Legal defensibility documentation
> - `C:\\Users\\<you>\\hermes-output\\latham-bagel-poc-package.md` — Small business POC demonstration package (verified API key exposure + email spoofing + missing headers)
> - `C:\\Users\\<you>\\hermes-output\\latham-bagel-shop-pitch-package.md` — Small business pitch deck with pricing, outreach script, competitive positioning

### Phase 0.2c: POC Development & Client Demonstration

> **Purpose:** After identifying live passive exposures (Phase 0.2b), the client may ask for a **Proof of Concept** showing the vulnerabilities are real and exploitable — not just theoretical. This sub-phase validates findings through additional passive checks and packages them into a demonstrable presentation.

This sub-phase bridges technical findings and sales conversion. A list of exposures is interesting. A live demonstration that proves the vulnerability works closes deals.

#### CRITICAL DISTINCTION — POC vs EXPLOITATION:
A POC proves a vulnerability exists without causing harm. Keep it to **read-only, passive verification**. Never:
- Access or download data from the target system
- Modify, delete, or encrypt anything
- Use credentials obtained from the exposure
- Escalate from the exposed service into the internal network
- Run exploit code against the target

If the client asks for an actual penetration test, that requires a separate signed Rules of Engagement.

#### POC Workflow

```
Live exposures (from Phase 0.2b)
  → Select 1-3 high-signal findings (things the client can see/understand)
  → Verify each finding with read-only passive checks
  → Document the verification (screenshots, command output, curl responses)
  → Package into a 5-minute demonstration script
  → Price the full assessment
```

#### POC #1: Exposed API Key Verification (Small Business)

Most small businesses embed Google Maps API keys in their website source code for location widgets, store locators, or embedded maps. These keys are often unrestricted.

**Verification steps:**

```python
# Step 1: Find API keys in public page source
# Search page source for AIza... pattern (Google API keys)
import re
import urllib.request

response = urllib.request.urlopen("https://targetbusiness.com/")
body = response.read().decode('utf-8')
keys = re.findall(r'AIza[0-9A-Za-z\-_]{35}', body)

# Step 2: Test each key against Google Geocoding API (read-only)
for key in keys:
    test_url = f"https://maps.googleapis.com/maps/api/geocode/json?address=Test+Location&key={key}"
    try:
        req = urllib.request.urlopen(test_url, timeout=10)
        data = json.loads(req.read())
        if data.get('status') == 'OK':
            print(f"VALID & UNRESTRICTED — this key works for anyone")
            # The geocode response proves the key is active
    except:
        pass
```

**Why this works as a POC:**
- Client can see the key in their own page source
- The key works when pasted into a browser URL bar
- They understand "anyone can use this on my billing account" in 30 seconds
- No technical knowledge needed to understand the impact

**PITFALL:** Some Google API keys are restricted by HTTP referrer. Test with a direct curl request (no referer header) to see if the restriction is actually enforced. A key that says "restricted" in the Google Cloud Console but works without a referrer check is effectively unrestricted.

#### POC #2: Email Spoofability Verification

Check if a domain can be impersonated via email.

**Verification steps (passive, no email sent):**

```bash
# Check SPF record
nslookup -type=txt targetdomain.com | grep -i spf
# If no "v=spf1" found — domain has no SPF record

# Check DMARC record
nslookup -type=txt _dmarc.targetdomain.com | grep -i dmarc
# If no DMARC or p=none — domain policy allows spoofing
```

**Client demonstration:**
> "Your domain has no SPF record. I could send an email that looks like it comes from your business, and most email providers would deliver it to your customers' inboxes. Your suppliers, your delivery partners — anyone who trusts emails from your domain is at risk."

**PITFALL:** DMARC may be set (p=reject) while SPF is missing. Point out that DMARC without SPF has incomplete authentication data — the email can still be spoofed because there's no authorized sender list to validate against. SPF and DMARC work together; one without the other leaves a gap.

#### POC #3: Missing Security Headers

Check if a web application has basic browser security protections.

```bash
# Check response headers for common security headers
curl -sI https://target.com/ | grep -iE "strict-transport-security|content-security-policy|x-content-type-options|x-frame-options|referrer-policy|permissions-policy"
# If empty — none of these protections are active
```

**Client demonstration:**
> "Your ordering portal returns none of the six standard security headers. That means customer sessions have no HTTPS enforcement, no clickjacking protection, no XSS prevention. For a site where customers enter their credit card info, this needs to be fixed."

#### The 5-Minute Client Demo

Structured presentation that converts findings into a sale:

```
:00 — Open the target's website in a browser
:30 — Right-click -> "View Page Source", search for "AIza"
:45 — Copy the API key, paste into browser URL bar with geocode request
1:00 — Show the JSON response with "status": "OK"
1:15 — "This key works. Anyone can use it on your account."

1:30 — Open terminal, show nslookup for SPF record
2:00 — "No SPF record. I could send emails from your domain."

2:15 — Show HTTP headers (or lack thereof)
2:30 — "No security headers. Customer sessions are unprotected."

3:00 — "For $750-$2,500 I do a full surface scan that maps your entire digital footprint and gives you a prioritized fix list."

5:00 — Hand them the one-page report. Close.
```

#### Small Business Conversion Pipeline

The conversion from technical finding to paying client follows a different path for small businesses vs enterprise:

| Step | Enterprise | Small Business |
|------|-----------|----------------|
| Hook | Regulatory risk, compliance fines | "This code could cost you money" |
| Delivery | Formal report, PowerPoint | In-person, show them in their browser |
| Price | $7,500-$65,000 | $750-$2,500 |
| Decision maker | Procurement + CISO | Owner (one person) |
| Close timing | 2-4 weeks | Same day if in person |
| Competition | CrowdStrike, Big 4 | Nobody (they've never been pitched) |

**Small business pricing tiers:**

| Service | Price | What's Included |
|---------|-------|-----------------|
| **Surface Scan** | $750 | Full passive OSINT: API keys, exposed credentials, security headers, email security, third-party risks |
| **Standard Assessment** | $2,500 | Surface scan + POS integration review + employee phishing simulation + written report |
| **Annual Protection Plan** | $1,500/yr | Quarterly re-scan + dark web monitoring + incident response phone support |

**Competitive advantage:** Most small businesses have never had ANY security assessment. No MSP or IT company has ever shown them their own API key in their own website code. You walk in with a specific, verifiable finding and you have their attention immediately.

**PITFALL (context interpretation):** When a client in a security/business development context mentions getting a "discounted order" or "similar to [previous client]" from a target, do NOT assume they mean fraud. In the #cyber channel context, "order" typically means a service order/engagement, and "similar to Manhattan" means replicating the same security assessment methodology. If ambiguous, clarify rather than refuse.

#### Reference Files

- `references/small-business-poc-pipeline.md` — Complete POC development methodology with Google API key testing, email spoofing verification, header scanning, and the 5-minute client demonstration script
- `C:\\Users\\<you>\\hermes-output\\latham-bagel-poc-package.md` — Completed small business POC example (Latham Bagel Shop)
- `C:\\Users\\<you>\\hermes-output\\latham-bagel-shop-pitch-package.md` — Completed small business pitch package with pricing, outreach templates, and competitive positioning

### Phase 0.2d: Pre-Qualification & Client Acquisition

> **Purpose:** Before walking into a target business (or sending an email), verify that:
> 1. They do NOT have an existing IT/security vendor who would block the sale
> 2. The decision maker is accessible (owner-operator, partner, solo practitioner)
> 3. They have the budget capacity for the target service tier
> 4. The provable finding is specific enough to demonstrate in 30 seconds

This sub-phase converts passive technical findings into a closed sale. The technical work (Phases 0.2a-0.2c) identifies what's exposed. This phase sells the fix.

#### Pre-Qualification Checklist

Before approaching any target, verify these signals:

| Signal | How to Check | Green Light | Red Light |
|--------|-------------|-------------|-----------|
| Existing IT vendor | Check website footer for "designed by", "hosted by", "managed by". Search for "MSP" or "IT support" + business name. | No vendor references found | Footer says "Managed by [MSP]", branded hosting support portal |
| Decision maker | Is the business a sole proprietorship, partnership, or LLC with identifiable owner? | Individual doctor/CPA/lawyer listed by name, "owner-operated", "family-owned" | Franchise, corporate chain, "corporate office" listed |
| Business has digital footprint | Domain resolves, website exists, takes appointments/orders online | Active website, online ordering, patient portal | No website, no online presence (no digital attack surface to sell) |
| Industry has compliance pressure | Healthcare (HIPAA), financial (FTC Safeguards, GLBA), real estate (BEC) | HIPAA-covered, handles client/patient financial data | Low-regulation retail, no sensitive data handled |
| Finding is demonstrable | You can show the finding on your phone in <30 seconds | WP admin login, exposed API key, accessible portal | Finding is abstract (version disclosure, server header) |

**If two or more red lights, skip the target.** The close rate is too low to justify the time.

#### IT Vendor Detection (Detailed)

When a small business has an MSP or IT vendor, the website often reveals it:

```bash
# Check website footer for vendor references
curl -s https://business.com/ | grep -iE "designed by|developed by|powered by|hosted by|managed by|site by"

# Check WHOIS for hosting provider
# GoDaddy, Wix, Squarespace = minimal IT support
# Dedicated server, enterprise host = may have MSP

# Check if the website is a basic template
# Templates suggest no dedicated developer = no IT vendor blocking
```

**Decision logic:**
- **No vendor found + simple hosting (GoDaddy, Wix, Squarespace):** Clean path. Pitch aggressively.
- **No vendor found + professional hosting (AWS, Azure, dedicated server):** May have an IT person but not a security-specific vendor. You're selling security, not IT management — different service.
- **Vendor found (managed IT provider, web development agency):** They already spend money on tech. The question is whether that vendor covers security. Most don't. Lead with "your IT provider manages your computers. I test your security. Different thing."

#### Walk-In Methodology (Highest Conversion)

For targets within walking distance of your starting location, walk-in is the most effective approach:

**The 90-second script:**

```text
:00  "Hi, I'm [Name]. I'm doing local security assessments out of [nearby landmark]."
:15  "I noticed something on your website I wanted to make you aware of."
:30  *Pull out phone, show the finding* "See this? This is your [WP admin / API key / exposed portal]."
:45  "Anyone on the internet can see this. For a [title company / dental practice / CPA firm], that's a problem because [specific risk]."
1:00  "I do full surface scans for local businesses. $X. Takes two days. You get a written report with specific fixes."
1:15  "I'm in the area all week. Want me to put together a scan for you?"
1:30  *Wait for response*
```

**If they say yes:** Collect contact info. Deliver the scan within 48 hours. Close on report delivery.
**If they say "tell me more":** Expand to 5 minutes. Show the second finding. Talk about the local breach numbers ($175K BST, $500K Albany ENT).
**If they say "not interested":** "No problem. Here's my card. If you change your mind, I'm local." Move to next target.
**If they say "our IT guy handles that":** "IT guys manage computers and passwords. Security testing is a different thing. I found this in 30 seconds — want me to show him what I found so he can fix it?"

#### Email Methodology (for trophy targets)

For larger targets where walk-in isn't appropriate (breached firms, corporate offices):

```text
Subject: Security assessment — [Firm Name], Latham

Hi [Name],

I'm a security consultant based in [town]. I came across your firm through [reference point — industry news, known breach, public record].

I work with [professional services firms / medical practices / local businesses] on external security assessments — finding what's publicly visible before someone else finds it.

I do a one-time surface scan that maps your external digital footprint and identifies exposures. It's passive, nondisruptive, and takes about a week.

If you're open to it, I'd be happy to come by for 20 minutes and show you a sample. If it's useful, great. If not, no harm done.

I'll follow up with a call later this week.

Best,
[Name]
```

**Follow-up sequence:**
- Day 1: Send email
- Day 3: Follow-up call ("I sent an email about security assessments — did you have a chance to look?")
- Day 7: Brief follow-up email with a specific finding from your local work
- Day 14: Either move on or walk in — you're in the area anyway

#### Objection Handling

| Objection | Response |
|-----------|----------|
| "We have a web guy" | "Web guys build sites. They don't test security. I found three things he missed in 30 seconds. Want me to show you?" |
| "We have an IT company" | "IT companies manage computers and passwords. Website security is a different specialty. Your IT vendor is great at keeping your network running — I test what's visible from the outside." |
| "We're too small to be hacked" | "That's exactly what Beacon Stone & Co. thought. They paid $175K in fines. Hackers don't care about size — they care about easy targets. Small businesses get hit because nobody's watching." |
| "Can you send me a proposal?" | "I'm right here. Give me 5 minutes and I'll show you exactly what I found. Then you decide if you need the proposal." |
| "How much?" (before you've shown value) | "$X for the full scan. I'll show you exactly what you're getting before you commit." |
| "How do I know you're legit?" | "I showed you a problem with your own website that you didn't know existed. That's proof. Here are my references." |

#### Pricing by Business Type

| Business Type | Recommended Tier | Price | Decision Maker | Close Speed |
|---------------|-----------------|-------|----------------|-------------|
| Restaurant / Retail | Surface Scan | $750-$1,500 | Owner on site | Same day |
| Solo professional (CPA, dentist, chiropractor) | Surface Scan + Standard | $1,500-$2,500 | Solo owner | Same day |
| Partnership practice (dental group, law firm) | Standard Assessment | $2,500-$3,500 | Partner(s) | 1-3 days |
| Medium firm (30+ employees, regulated) | Standard + Annual | $3,500-$7,500 | Managing partner | 1-2 weeks |
| Already-breached enterprise | Full Audit | $7,500-$17,500 | Compliance team | 1-4 weeks |

#### Walking Route Planning

When targeting a geographic cluster (business park, commercial corridor), optimize your route:

```python
# Sort targets by distance from starting point
# Group by building (multi-tenant buildings = multiple pitches in one stop)
# Order by: proximity -> value -> decision speed

route = [
    # Same building (highest priority)
    {"stop": "AAA Title Agency", "distance": "0 mi (same complex)", "ticket": "$2,500-$5,000"},
    
    # 0.1 mi walk
    {"stop": "678 Troy-Schenectady (3 businesses in one building)", "distance": "0.1 mi", "ticket": "$6,500 total"},
    
    # 0.3 mi walk  
    {"stop": "Capital Region Health Park (2 dental practices)", "distance": "0.3 mi", "ticket": "$6,000 total"},
    
    # 0.5 mi walk
    {"stop": "7 Airport Park Blvd (CPA firm)", "distance": "0.5 mi", "ticket": "$2,500-$3,500"},
    
    # 1.0 mi walk (trophy)
    {"stop": "Beacon Stone & Co. (already breached)", "distance": "1.0 mi", "ticket": "$7,500-$17,500"},
]
```

**Expected conversion:** 30-50% of walk-in pitches result in a paid engagement.
**Expected revenue per route:** $15K-$50K depending on density and target quality.
**Time investment:** 2-3 hours of walking + 3-5 days of scan + report delivery.

#### Referral Engine

After every paid engagement, ask:

> "I'm trying to help local businesses in [area]. If you know any other [dentists / CPAs / real estate offices] who should get checked, send them my way. I'll give you 10% off your next re-scan if they sign."

This turns one close into a network.

#### Reference Files

- `C:\\Users\\<you>\\hermes-output\\latham-master-consolidated-report.md` — Full 17-target consolidated report with walking route, pitches, and pricing
- `C:\\Users\\<you>\\hermes-output\\latham-sales-methodology.md` — Sales methodology with objection handling, timing, and custom script per target
- `C:\\Users\\<you>\\hermes-output\\bst-outreach-plan.md` — Email outreach plan for Beacon Stone & Co. (trophy target) with confirmed email addresses and follow-up sequence

### Phase 1: Passive Reconnaissance (No Target Touching)

```bash
# 1. Domain Discovery
# --------------------
# Enumerate all domains owned/used by target
# Methods: WHOIS, reverse WHOIS, SSL cert transparency, search engines

# Reverse WHOIS — find other domains owned by same registrant
whois acme.com | grep "Registrant"

# Certificate Transparency — find domains via SSL certs
curl -s "https://crt.sh/?q=%25.acme.com&output=json" | jq -r '.[].name_value' | sort -u

# Google dorking for subdomains
site:acme.com -www -mail -blog

# 2. Employee Discovery
# --------------------
# Find employees on LinkedIn, GitHub, company websites
# Google dork: site:linkedin.com/in "Acme Corp"
# GitHub: search for @acme.com emails in commits

# 3. Technology Stack Identification
# --------------------
# BuiltWith (web): https://builtwith.com/acme.com
# Wappalyzer (browser extension) — manual visit
# WhatWeb (tool)
whatweb acme.com

# 4. Third-Party Exposure
# --------------------
# Check for:
# - S3 buckets: acme-assets, acme-backup, acme-data (try common names)
# - GitHub repos: search "Acme Corp" for leaked code
# - Pastebin: search for acme.com IPs/creds
# - Shodan: search for acme.com IP ranges
# - HaveIBeenPwned: check @acme.com email domain
```

**Passive Recon Data Sources:**
```text
DNS:
- crt.sh (Certificate Transparency)
- SecurityTrails (passive DNS)
- CommonCrawl (historical DNS)
- DNSDumpster (DNS recon)

Company:
- LinkedIn (employees, tech stack from job postings)
- Glassdoor (internal tools mentioned in reviews)
- SEC Filings (partners, acquisitions, subsidiaries)
- Crunchbase (funding, office locations)
- Google Patents/USPTO (tech IP)

Infrastructure:
- Shodan (exposed services)
- Censys (SSL certs + services)
- VirusTotal (domain relationship graph)
- BuiltWith / Wappalyzer (tech stack)
- Netcraft (hosting history)

Leak/Exposure:
- GitHub (code leaks, config files)
- Pastebin/rentry (credential dumps)
- Telegram (breach channels)
- HaveIBeenPwned (domain breach reports)
```

### Phase 2: Active Reconnaissance (Target Interaction)

#### Stealth & Evasion Fundamentals

Before any active probing, assess the detection posture of the target. The goal is to appear as organic web traffic, not an automated scan:

**Timing profiles** — Human browsing has natural variance. Batch requests with Gaussian-distributed delays (μ=15s, σ=5s between probes) rather than fixed intervals. Rotate periods of activity (5-10 min) with idle windows (20-60 min) to mimic a human tabbing between applications.

**Request fingerprints** — Every HTTP request should carry a realistic header set from a real browser: varied User-Agent (rotate from a pool of actual Chrome/Firefox/Safari UAs), a non-empty Referer chain, Accept-Language, and a cookie jar maintained across the session. Avoid tool-specific defaults (nmap's default UA, nuclei's `Nuclei/X.X.X`, ffuf's `Fuzz Faster U Fool`).

**Egress routing** — Route all traffic through Tor (proxychains-ng) or a rotating proxy pool. Set circuit lifetimes (~10 min for Tor) so the source IP changes before any threshold-based WAF rule would fire. For larger engagements, Axiom (MIT) spins up ephemeral VMs distributed across cloud providers.

**Rate discipline** — Define max requests per minute / hour / day and apply exponential decay: N requests in the first window, N/2 in the next, N/4 in the next. A target that sees a linear scan pattern is more likely to treat it as automated than one that sees geometrically decaying interest.

**Noise budget** — Treat every probe as consuming a "noise budget." Passive intelligence (Phase 1) should answer 80% of questions before Phase 2 begins. Active probes confirm hypotheses, not discover them.

> 🛡️ **GAP**: No FOSS tool implements organic-traffic recon as a first-class feature. For building a slow-roll proxy that wraps any tool with jitter, UA rotation, referer chains, and rate decay, see `references/recon-tool-landscape.md` (Component A: slow-roll-proxy).

```bash
# 1. Subdomain Enumeration
# --------------------
# Amass (comprehensive)
amass enum -d acme.com -o amass_enum.txt

# Subfinder (fast, API-based)
subfinder -d acme.com -all -o subdomains.txt

# DNS brute force
dnsrecon -d acme.com -D /usr/share/wordlists/dns_big.txt -t brt

# 2. Port Scanning
# --------------------
# Nmap — Top ports scan (stealth)
nmap -sS -Pn -p- --min-rate=1000 -T4 -oA nmap_scan acme.com

# Nmap — Service version + OS detection
nmap -sV -sC -O --top-ports=1000 -oA nmap_detail acme.com

# Masscan — Faster for large ranges
masscan 10.0.0.0/24 -p0-65535 --rate=10000

# 3. Web Application Reconnaissance
# --------------------
# HTTP probing (which hosts are web servers?)
httpx -l subdomains.txt -o live_hosts.txt

# Web technology fingerprinting
httpx -l live_hosts.txt -tech-detect -o tech_stack.txt

# Directory/file brute forcing
gobuster dir -u https://app.acme.com -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt

# Parameter discovery
ffuf -u https://app.acme.com/FUZZ -w parameters.txt

# 4. Email/User Enumeration
# --------------------
# Check for email disclosure patterns
# Common: info@, admin@, support@, contact@, hr@
# Employee email pattern: first.last@acme.com, flast@acme.com

# LinkedIn to email (if authorized)
# Use linkedin2username or similar tools
# Verify via: https://email-format.com
```

### Phase 3: Attack Surface Mapping

```python
# Create comprehensive attack surface map
attack_surface = {
    "external_ips": [
        {"ip": "203.0.113.1", "ports": [80, 443], "service": "nginx 1.24"},
        {"ip": "203.0.113.2", "ports": [22, 443, 3389], "service": "OpenSSH 8.9, IIS, RDP"},
        {"ip": "203.0.113.3", "ports": [3306], "service": "MySQL (should not be public!)"},
    ],
    "domains": [
        "acme.com (main)",
        "app.acme.com (web application)",
        "mail.acme.com (Exchange OWA)",
        "vpn.acme.com (OpenVPN)",
        "dev.acme.com (development server — dev is always juicy)",
        "acme-backup.s3.amazonaws.com (exposed S3 bucket — high priority!)",
    ],
    "employees": [
        {"name": "John Doe", "role": "IT Admin", "email_pattern": "j.doe@acme.com"},
        {"name": "Jane Smith", "role": "CEO", "email": "j.smith@acme.com"},
    ],
    "tech_stack": {
        "web": "React 18, Node.js 20",
        "cdn": "Cloudflare",
        "email": "Exchange 2019 (OWA exposed)",
        "analytics": "Google Analytics, Hotjar",
        "hosting": "AWS (us-east-1)",
    },
    "vulnerabilities_identified": [
        "CVE-2024-1234 — nginx before 1.25 vulnerable to ...",
        "Exposed S3 bucket (READ permission)",
        "OWA login page with default password policy (no lockout observed)",
        "dev.acme.com accessible without VPN",
    ],
    "high_value_targets": [
        "VPN Concentrator (vpn.acme.com)",
        "Exchange Server (mail.acme.com)",
        "Admin Portal (admin.acme.com)",
        "CI/CD Pipeline (jenkins.acme.com)",
        "Git Server (git.acme.com)",
    ]
}
```

### Phase 3.5: Stack-to-CVE Correlation & Knowledge Graph

After mapping the attack surface, correlate every discovered technology to known vulnerabilities. This is the bridge between "what's running" and "what can we exploit."

#### Workflow
```python
# For every discovered service with version information:
services_discovered = [
    {"name": "nginx", "version": "1.24.0", "confidence": 0.95},
    {"name": "php", "version": "8.1.12", "confidence": 0.90},
    {"name": "jquery", "version": "3.6.0", "confidence": 0.85},
    {"name": "openssh", "version": "8.9p1", "confidence": 0.80},
]

for svc in services_discovered:
    # 1. Generate CPE 2.3 identifier
    cpe = f"cpe:2.3:a:{svc['vendor']}:{svc['name']}:{svc['version']}:*:*:*:*:*:*:*"
    
    # 2. Query NVD API + OSV.dev for matching CVEs
    cves = query_nvd_cpe(cpe)  # rate-limited
    
    # 3. Cross-reference with ExploitDB and Nuclei templates
    for cve in cves:
        cve.exploit_available = search_exploitdb(cve.id)
        cve.nuclei_template = check_nuclei_template(cve.id)
    
    # 4. Assign confidence score
    #    1.0 = exact version match with known PoC
    #    0.8 = version range match, exploit available
    #    0.5 = product match, no version confirmation
    #    0.2 = product version guess from similar fingerprint
    cve.confidence = compute_confidence(svc, cve)
```

#### Knowledge Graph Storage
For persistent cross-session intelligence, store findings in a structured graph:

```
Target → Domains → Hosts → Services → Technologies
                                            ↓
                                       CVE Matches
                                            ↓
                                    Attack Paths & Vectors
```

Typical schema (PostgreSQL with JSONB or Neo4j):
- **recon_technologies**: name, version, category, CPE, confidence, source (header/body/JS/error)
- **recon_cves**: cve_id, CVSS, severity, description, exploit_available, nucleus_template, PoC URLs
- **recon_attack_paths**: entry_point, attack_vector, CVE, MITRE technique/tactic, chain_step

Useful knowledge graph queries:
- "Find all services with CVSS > 9.0 that have public exploits"
- "Map the shortest attack path from external service X to internal service Y"
- "Which technologies have changed since last week's scan?"
- "Show all services using nginx < 1.25 across all targets"

> 🗺️ **GAP**: No production-grade FOSS tool provides general-purpose version→CPE→CVE correlation with confidence scoring. WPScan (WP-only) and Retire.js (JS-only) are the closest. For a general correlator, see `references/recon-tool-landscape.md` (Component B: tech-to-cve).

```bash
# Passive CVE lookup utilities
# OSV.dev API (no key needed)
curl -s "https://api.osv.dev/v1/query" \
  -H "Content-Type: application/json" \
  -d '{"package":{"name":"nginx","ecosystem":"Packagist"},"version":"1.24.0"}'

# NVD API (rate-limited, 5 req/30s free)
curl -s "https://services.nvd.nist.gov/rest/json/cves/2.0?cpeName=cpe:2.3:a:nginx:nginx:1.24.0"

# searchsploit offline lookup
searchsploit nginx 1.24
```

### Phase 4: Social Engineering Vector Identification

```python
# Social engineering reconnaissance

# Information Gathering for Phishing/Spear Phishing
social_vectors = {
    "personal_details": {
        "hobbies": ["Member of ACME Hiking Club (public LinkedIn post)"],
        "conferences": ["Attended DefCon 2023 (Twitter post)"],
        "promotions": ["John promoted to CISO in Dec 2023 (LinkedIn)"],
        "email_signature_format": "Found in public email thread on Google Groups"
    },
    "organization_context": {
        "current_events": "Company just launched product X (blog post)",
        "vendor_relationships": ["Uses AWS, Salesforce, Slack (job postings)"],
        "internal_tools": "Jira, Confluence, ServiceNow (Glassdoor reviews)",
        "office_locations": "San Francisco HQ, Austin office (website)"
    },
    "physical_access_vectors": {
        "badge_design": "Photo from conference (employee wore badge)",
        "tailgating_potential": "Single entrance, RFID badge reader",
        "reception_language": "Phone greeting: 'Acme Corp, how can I help you?'",
        "office_hours": "8AM-6PM (Google Maps business hours)"
    }
}
```

**Social Engineering Attack Types (Authorized Only):**

```text
1. PHISHING (Email-based)
   - Generic phishing: "Your package has been delayed — click here"
   - Spear phishing: Targeted to specific role (IT, Finance, Exec)
   - Whaling: Targeting C-suite executives
   - BEC (Business Email Compromise): Impersonating a vendor/executive

2. VISHING (Voice-based)
   - IT support callback: "Your computer has been compromised..."
   - Vendor impersonation: "Calling from AWS about your account..."
   - HR/benefits: "Open enrollment reminder — verify your account"

3. SMISHING (SMS-based)
   - Package delivery: "USPS — confirm your address to receive package"
   - Security alert: "Suspicious login detected — verify now"

4. PHYSICAL (On-site)
   - Tailgating: Following authorized personnel through secured doors
   - Badge cloning: Off-the-shelf RFID skimmers
   - USB drops: Malicious USB drives in parking lot/reception
   - Shoulder surfing: Observing PIN entry or screen content
```

**Phishing Campaign Design (GoPhish):**

```python
# GoPhish campaign structure example
campaign = {
    "name": "Q1 Phishing Test — AWS Billing Alert",
    "target_group": "IT Department (filtered from LinkedIn)",
    "email_template": {
        "subject": "URGENT: AWS Billing Alert — Action Required",
        "sender": "aws-billing@amazon.com",
        "body": """
            <h2>AWS Billing Alert</h2>
            <p>Your account has exceeded the budget threshold of $10,000.</p>
            <p>Please review your charges immediately:</p>
            <p><a href="{{.URL}}">Review AWS Billing</a></p>
            <p>Failure to respond within 24 hours may result in service suspension.</p>
            <p>- AWS Billing Team</p>
        """,
    },
    "landing_page": {
        "url": "https://login-aws-verify.com",  # ROE-authorized domain
        "template": "AWS Login Clone (captures credentials)"
    },
    "metrics": {
        "sent": 50,
        "opened": 30,
        "clicked": 15,
        "credentials_submitted": 8,
        "reported_to_security": 2
    }
}
```

### Phase 5: Purple Team Coordination

```python
# Purple team testing: Red and Blue working together
purple_team_exercise = {
    "participants": {
        "red_team": "Lead + 2 operators (OSINT + exploitation)",
        "blue_team": "SOC lead + analyst + incident responder",
        "purple_lead": "Coordinates scenarios and validates detections"
    },
    "scenarios": [
        {
            "id": "PT-001",
            "name": "External Recon Detection",
            "red_action": "Passive DNS enumeration via SecurityTrails",
            "blue_detection": "DNS logs: unexpected query patterns",
            "validation": "✅ Detected (3 queries before block)"
        },
        {
            "id": "PT-002",
            "name": "Phishing Campaign Detection",
            "red_action": "Spear phishing email to IT department",
            "blue_detection": "Email gateway: sender domain analysis",
            "validation": "❌ Missed (user clicked, credentials captured)",
            "recommendation": "Implement DMARC strict policy + MFA + user training"
        }
    ]
}
```

**Detection Gap Analysis Template:**
```markdown
## Detection Gap: PT-002 (Phishing)

### Red Team Action
- Sent 50 phishing emails spoofing AWS billing
- Landing page captured 8 sets of Active Directory credentials
- 2 users reported to security (after submitting credentials)

### Blue Team Observations
- Email gateway did NOT flag the sender domain (sender was legitimate compromised account)
- No anomalous login alerts (geolocation didn't trigger — used local proxy)
- Credentials captured before MFA prompt → MFA not triggered
- 2 reports from users via the "Report Phishing" button → 15 min response time

### Gap Rating: CRITICAL
- MFA not challenged for first-time login from new device
- User training needs improvement (only 4% reported before clicking)
- Email gateway needs DMARC stricter enforcement

### Remediation Priority
1. [ ] Configure Conditional Access to require MFA on all new device logins (P1)
2. [ ] Deploy DMARC reject policy for all first-party domains (P1)
3. [ ] Monthly phishing simulation training for all users (P2)
4. [ ] Reduce phishing report response time to <5 minutes (P2)
```

### Phase 6: Reporting

```markdown
# RED TEAM ENGAGEMENT REPORT — Acme Corp

## Classification: CONFIDENTIAL — CLIENT PRIVILEGED

### 1. Executive Summary
Between 2024-01-15 and 2024-01-30, Acme Corp's red team conducted
a full-scope adversarial simulation against external infrastructure
and employees. Key findings: 12 vulnerabilities discovered, 3 critical,
4 high, 3 medium, 2 low. Initial access achieved in 4 days via
phishing. Full domain compromise in 8 days.

### 2. Key Metrics
- **Total Reconnaissance Time**: 4 days (passive + active)
- **Attack Surface Mapped**: 142 subdomains, 8 cloud assets, 34 employees identified
- **Phishing Success Rate**: 16% (8/50 credentials captured)
- **Initial Access Time**: 4 days from engagement start
- **Persistence Duration**: 10 days (undetected)
- **Critical Findings**: 3 (Exposed S3 bucket, RCE on dev server, Admin creds in GitHub)

### 3. Critical Findings
- **S3 Bucket Exposure**: acme-backup bucket has READ-WRITE permission for authenticated AWS users. 500GB of data exposed including PII.
- **CI/CD Compromise**: Jenkins at jenkins.acme.com has default credentials. Full source code and deployment credentials accessible.
- **Domain Admin Access**: Achieved via Pass-the-Hash from phished IT admin credentials.

### 4. Timeline
- Day 1-2: Passive recon → 55 subdomains, tech stack, employee list
- Day 3-4: Active recon → Exposed S3 bucket, Jenkins, dev server
- Day 5: Phishing campaign launched → 8 sets of creds captured
- Day 6-7: Lateral movement from IT admin → Domain Admin
- Day 8-10: Persistence via scheduled tasks + C2 beacon
- Day 11: Purple team validation and detection gap analysis
- Day 12-14: Remediation verification retesting

### 5. Recommendations
See detailed remediation plan in Appendix A.
```

## OPSEC Auditing: Staying Undetected

Red team operations generate data — tool output files, DNS queries, HTTP requests, log entries, and disk artifacts. Left unchecked, these can reveal the operation to the target or a third-party monitor. OPSEC auditing is a cross-cutting phase that runs **before, during, and after** every operation.

### Pre-operations Audit (before Phase 1)
- [ ] **Proxy chain verified** — all egress traffic routes through Tor or rotating proxies. No direct IP leak.
- [ ] **DNS isolation** — DNS queries go through the proxy chain, not the local resolver. No direct DNS to target domains.
- [ ] **Tool configuration** — default User-Agents replaced, default output paths overridden, telemetry/update checks disabled.
- [ ] **Environment clean** — no prior operation artifacts on the scanning host.
- [ ] **Identity separation** — no personal accounts, keys, or credentials accessible from the scanning environment.

### Mid-operations Audit (between phases)
- [ ] **IP check** — verify the proxy exit IP is not the real IP (e.g., `curl httpbin.org/ip` through the proxy chain).
- [ ] **Rate compliance** — actual request rate matches the configured profile. No accidental burst.
- [ ] **Log check** — verify no recon processes are leaking to event logs or syslog that weren't expected.
- [ ] **Jitter compliance** — inter-request timing fits the configured Gaussian distribution (not fixed intervals).

### Post-operations Cleanup
- [ ] **Process cleanup** — all recon tools exited cleanly. No lingering nmap/gobuster/nuclei processes.
- [ ] **Disk cleanup** — no output files left in `/tmp`, `%TEMP%`, or `output/` directories. Wipe or shred sensitive data.
- [ ] **Network cleanup** — no lingering connections, ARP cache entries, or NetBIOS cache entries from the scanning host.
- [ ] **Registry cleanup** (Windows hosts) — no tool traces in `HKCU\Software` or `HKLM\Software`.
- [ ] **Credential rotation** — any API keys, SSH keys, or tokens used during the operation are rotated immediately after.

### OPSEC Scoring
A practical way to measure and enforce OPSEC discipline:

| Component | Weight | Measure |
|-----------|--------|---------|
| Proxy integrity | 25% | Exit IP differs from real IP |
| DNS hygiene | 15% | No direct DNS to target domains |
| Jitter compliance | 15% | Timing within ±2σ of configured mean |
| Rate compliance | 10% | Requests ≤ configured max |
| Artifact cleanup | 15% | Zero disk artifacts post-op |
| Log footprint | 10% | Recon processes within expected noise |
| Tool compliance | 5% | Only approved FOSS tools in use |
| Identity isolation | 5% | No personal accounts accessible |

A score below 80/100 should halt operations until the gap is resolved.

| OPSEC Score | Grade | Action |
|-------------|-------|--------|
| 90–100 | A | Continue operations |
| 80–89 | B | Acceptable — note minor issues |
| 70–79 | C | Investigate before continuing |
| 60–69 | D | Stop and fix leaks |
| <60 | F | Emergency abort — clean up, reassess infra |

> 🔍 Runnable Python auditor covering IP/DNS/proxy/disk/process checks: `agent-universe/teams/07-recon-team/recon-auditor/tooling/audit_recon.py`

## Common Pitfalls

### Scope Creep (Accidental)
- **PITFALL**: Easy to accidentally scan out-of-scope IPs (cloud providers, shared hosting).
- **SOLUTION**: Precisely define scope. Use allow lists. Monitor all scanning activity.
- **WORKAROUND**: If you hit something out of scope — STOP, document, notify client.

### Operational Security (OPSEC) for Red Team
- **PITFALL**: Using personal accounts/infrastructure for red team ops.
- **SOLUTION**: Dedicated C2 infrastructure, burner VPS, separate VPN.
- **WORKAROUND**: Always assume blue team is monitoring. Use operational security measures.

### Blue Team Detection
- **PITFALL**: Modern EDR/SIEM can detect active scanning immediately.
- **SOLUTION**: Coordinate with blue team if testing is announced. Slow scans for covert ops.
- **WORKAROUND**: Use passive techniques first. Rate-limit active scans. Rotate source IPs.

### Legal Exposure
- **PITFALL**: Scan from a VPS in a jurisdiction with different computer crime laws.
- **SOLUTION**: Know the laws of ALL jurisdictions involved (target location, VPS location, your location).
- **WORKAROUND**: Use infrastructure in the same jurisdiction as the target when possible.

### Social Engineering Discovery
- **PITFALL**: Target may publicize your phishing test internally, ruining operation.
- **SOLUTION**: Separate social engineering from other phases. Use unique lures.
- **WORKAROUND**: Coordinate with designated point of contact for Phishing tests.

### Tool Noise
- **PITFALL**: Tools like Amass with all API keys enabled generate massive API calls.
- **SOLUTION**: Start minimal, add APIs as needed. Use concurrency limits.
- **WORKAROUND**: Test API availability before the engagement starts.

### LotL Reconnaissance Blind Spots
- **PITFALL**: Standard FOSS tools (Nmap, Nuclei, httpx) leave binary footprints, generate predictable process names, and create identifiable network patterns. An EDR watching for `nmap` process creation or `nuclei` HTTP headers will catch them immediately.
- **SOLUTION**: Living Off the Land (LotL) recon uses only built-in OS tools. On Windows: `nslookup` for DNS, `bitsadmin /transfer` and `certutil -urlcache` for HTTP downloads, `System.Net.Sockets.TcpClient` via PowerShell for raw port probes, `Invoke-WebRequest` for HTTP probing. On Linux: `dig`, `curl`, `/dev/tcp` shell sockets, `openssl s_client`.
- **PITFALL**: LotL techniques generate their own event logs. PowerShell `Invoke-WebRequest` generates Event ID 800 (script block logging). BITSAdmin generates Event ID 59. `nslookup` generates cmd.exe creation (4688). These are detectable if the target audits for them.
- **SOLUTION**: Choose techniques by event log footprint. `nslookup` interactive is nearly invisible. .NET `TcpClient` via PowerShell is moderate visibility (script block logging). BITSAdmin/CertUtil are high visibility (file downloads on disk). Match technique to the target's monitoring capability.
- **WORKAROUND**: For the complete Windows LotL technique catalog with event log mapping, see `references/living-off-the-land-recon.md`.

### Fixed-Interval Scanning
- **PITFALL**: Periodic requests at exact fixed intervals (once per second, per 5 seconds, etc.) are a strong WAF/IDS signature. Tools like FFUF, Gobuster, and Nmap default to fixed timing windows.
- **SOLUTION**: Use jitter. Wrap tools in a slow-roll proxy that applies Gaussian-distributed delays. Randomize intervals between requests (μ=15s, σ=5s).
- **WORKAROUND**: For Nmap, use `-T1` (paranoid) with `--scan-delay` configurable. For HTTP tools, pipe through a jitter proxy or use Interlace with randomized sleeps between tool invocations.

## Legal & Ethical Notes

> **⚠️ WARNING**: Red team operations carry significant legal and professional risk.
> **You MUST have ALL of the following before starting any activity:**

### Required Documentation
1. **Signed Rules of Engagement (ROE)** — scope, methods, timeline
2. **Written Authorization** — from authorized signatory (CTO, CSO, CIO, or above)
3. **Emergency Stop Procedures** — how client halts all activity
4. **Insurance** — Professional liability / Cyber E&O insurance
5. **Data Handling Agreement** — what happens to captured data
6. **Non-Disclosure Agreement** — for all team members
7. **Background Checks** — for all team members (if sensitive engagement)

### Mandatory Ethical Boundaries
- ❌ Never access systems outside the defined scope
- ❌ Never exfiltrate, modify, or delete production data (PII, PHI, financial)
- ❌ Never perform denial of service attacks (unless explicitly authorized)
- ❌ Never install backdoors that persist after engagement
- ❌ Never use social engineering against non-consenting third parties
- ❌ Never retain credentials, data, or access after engagement ends
- ✅ Always stop immediately if you encounter unanticipated sensitive data
- ✅ Always report critical vulnerabilities immediately (not just in final report)

### Professional Standards
- Follow PTES (Penetration Testing Execution Standard): http://www.pentest-standard.org
- Follow OWASP Testing Guide for web apps: https://owasp.org/www-project-web-security-testing-guide
- Follow OSSTMM for methodology: https://www.isecom.org/OSSTMM.3.pdf
- Report with evidence and reproducibility steps for each finding

## Concrete Implementation

A live implementation of this automated pipeline exists at:
- **`agent-universe/teams/07-recon-team/`** — 5 specialized agents (passive, active-slow, CVE-match, attack-planner, reporter) + 4 shared components (slow-roll-proxy, tech-to-cve, knowledge-graph, orchestrator)
- **Hermes Agent skills** (6 skills): `recon-orchestrator`, `recon-passive`, `recon-active-slow`, `recon-cve-match`, `recon-attack-plan`, `recon-report`

Each agent has: `AGENTS.md` · `README.md` · `config/config.yaml` · `.env.example` · `tooling/` with runnable Python scripts.

The shared components are the 4 custom builds that fill critical FOSS gaps:
- **`slow-roll-proxy/proxy.py`** — 1,200+ line organic traffic engine (TCP proxy + pipe wrapper modes, Gaussian jitter, UA rotation, referer chains, Tor routing, exponential rate decay)
- **`tech-to-cve/cve_match.py`** — Passive CVE correlator with 100+ CPE mappings, NVD + OSV API clients, semantic version matching, confidence scoring 0.0–1.0
- **`knowledge-graph/schema.sql`** — 8 PostgreSQL tables + 15 indexes + 5 attack path queries
- **`orchestrator/`** — 6 Hermes Agent skills for running each phase

```bash
# Run Phase 1 (passive recon):
cd agent-universe/teams/07-recon-team
python recon-passive/tooling/passive_recon.py example.com

# Run CVE correlation on discovered tech:
python shared/tech-to-cve/cve_match.py --tech nginx --version 1.24.0

# Start slow-roll proxy for stealth scanning:
python shared/slow-roll-proxy/proxy.py --mode proxy --port 8080 --profile human
```

## Cross-References

- `security/osint-recon` — Full reconnaissance pipeline integrated into red team ops
- `security/osint-threat` — Threat intelligence for understanding adversary TTPs
- `security/osint-social` — Social media recon for phishing/spear-phishing targets
- `security/osint-person` — Employee targeting and social engineering profiling
- `security/osint-business` — Business intelligence for vendor/partner attack vectors
- `security/osint-property` — Physical facility reconnaissance
- `security/osint-facial` — Identity verification during physical operations
- `software-development/systematic-debugging` — Systematic vulnerability analysis
- `software-development/web-scraping-scrapling` — Legitimate web data collection for recon
- `software-development/building-mcp-servers` — Building MCP servers for red team tooling
- **`references/proximity-vulnerability-surge.md`** — Address-anchored proximity vulnerability surge methodology: commercial RE mapping, tenant enumeration, breach cross-referencing, risk scoring, heat map construction. Bridges Phase 0.1 → Phase 1.
- **`references/recon-tool-landscape.md`** — Full 35+ tool catalog, license matrix, pipeline architecture, gap analysis, and build patterns for custom components (slow-roll proxy, tech→CVE correlator, knowledge graph schema)
- **`references/living-off-the-land-recon.md`** — Windows/Linux native OS-tool recon techniques with event log mapping, stealth ratings, and decision guide for choosing techniques by log footprint
- **`references/local-business-target-discovery.md`** — Geographic-area business target discovery methodology: source selection, curl-based JSON-LD extraction, categorization/priority framework, and a completed 200+ business Capital Region directory as a working example
- **`references/batch-terminal-recon.md`** — Batch per-business technical recon methodology for constrained environments: 15-20 business subagent batching, per-business command templates, documentation template, admin path wordlist, email security assessment commands, Google DNS over HTTPS API, timeout handling, and a worked 200+ business example
- **`scripts/tech-to-cve.py`** — Runnable CVE correlation script (generates CPE → queries NVD/OSV → returns confidence-scored CVEs)
- **`scripts/slow-roll-proxy.py`** — Runnable organic traffic engine (Gaussian jitter, UA rotation, Tor routing, rate decay)

## Related Skills

- `security/osint-business` — Business intelligence for vendor/partner attack vectors (active)
- `security/osint-social` — Social media recon for phishing/spear-phishing targets (active)
- `security/osint-threat` — Threat intelligence using individual security tools
- `mcp/mempalace-memory` — Persistent memory backend, useful for storing targeting data (active)

> **Note (May 2026)**: This skill's automated pipeline methodology was implemented as a full Reconnaissance Team at `agent-universe/teams/07-recon-team/`. The build components (slow-roll-proxy, tech-to-cve, knowledge-graph schema) are production code covering gaps that no existing FOSS tool fills. See the Concrete Implementation section above for runnable paths.

## Verification Checklist

- [ ] Rules of Engagement signed and on file
- [ ] Scope defined and communicated to entire team
- [ ] Emergency contact information distributed
- [ ] Passive recon completed (no target systems touched)
- [ ] Active recon completed within scope
- [ ] Attack surface map documented (domains, IPs, tech stack, employees)
- [ ] Social engineering vectors identified (if authorized)
- [ ] Phishing campaign designed and approved (if authorized)
- [ ] Purple team scenarios defined and coordinated
- [ ] Findings documented with evidence and reproducibility
- [ ] Critical findings reported immediately
- [ ] All test infrastructure decommissioned after engagement
- [ ] Client data destroyed per data handling agreement
- [ ] Final report delivered and debrief completed
