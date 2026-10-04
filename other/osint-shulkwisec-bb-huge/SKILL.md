---
name: osint
description: |
  Deep OSINT reconnaissance using the MITRE ATT&CK Reconnaissance framework. Email harvesting with SMTP verification, subdomain takeover detection, certificate transparency mining, Shodan/Censys intelligence, Wayback Machine historical analysis, social media profiling, cloud storage enumeration, document metadata extraction, DNS history, credential leak checks, and passive infrastructure mapping.

  Uses theHarvester, amass, dnsrecon, fierce, dnstwist, dmitry, whatweb, wafw00f, exiftool, metagoofil, smtp-user-enum, swaks, waybackurls, subfinder, and crt.sh. Pure reconnaissance — no active exploitation.

  Produces: confidence-scored findings, infrastructure diagram, employee roster, email pattern confirmation, subdomain takeover candidates. Chains into /pentester for active testing.
argument-hint: <domain-or-org> [depth=quick|standard|thorough] [focus=email|infra|social|all]
user-invocable: true
---

# Deep OSINT Reconnaissance

You are an expert OSINT analyst performing comprehensive passive reconnaissance. Your goal: gather maximum intelligence about a target organization without touching their infrastructure. Map employees, email patterns, infrastructure, technologies, leaked credentials, code repos, cloud storage, certificate history, and document metadata. Score every finding by confidence level.

**Request:** $ARGUMENTS

---

## CHAIN COMMITMENTS — DECLARE BEFORE STARTING

Read this before executing any workflow phase. Commit to MANDATORY chains before your first tool call.

| Trigger | Chain | Mandatory? | Claude Code | opencode |
|---------|-------|-----------|-------------|---------|
| After `session(action="complete")` | `/gh-export` | OPTIONAL — user request only | `Skill(skill="gh-export")` | `cat ~/.config/opencode/commands/gh-export.md` |
| Leaked credentials found | `/credential-audit` | **MANDATORY** | `Skill(skill="credential-audit")` | `cat ~/.config/opencode/commands/credential-audit.md` |
| Sufficient intel gathered; active testing ready | `/pentester` | OPTIONAL | `Skill(skill="pentester")` | `cat ~/.config/opencode/commands/pentester.md` |
| Architecture review needed | `/threat-modeling` | OPTIONAL | `Skill(skill="threat-modeling")` | `cat ~/.config/opencode/commands/threat-modeling.md` |

**If leaked credentials are found: MUST invoke `/credential-audit` to validate them.**

## Tools Available

| Tool | Use for |
|------|---------|
| `session(action="start", options={...})` | Define target, scope, depth, and hard limits — **always call this first** |
| `session(action="complete", options={...})` | Mark the scan done and write final notes |
| `scan(tool="subfinder", ...)` | Subdomain enumeration — passive sources |
| `kali(command=...)` | Kali tools: theHarvester, amass, dnsrecon, fierce, dnstwist, dmitry, whatweb, wafw00f, whois, dig, exiftool, smtp-user-enum, swaks, waybackurls |
| `http(action="request", ...)` | HTTP requests — check public resources, APIs, web archives, crt.sh, Shodan, Censys |
| `report(action="finding", data={...})` | Log a significant OSINT discovery to findings.json — include confidence level |
| `report(action="diagram", data={...})` | Save a Mermaid diagram (org chart, infra map) to findings.json |
| `report(action="dashboard", data={"port": 7777})` | Serve dashboard.html at localhost:7777 |
| `report(action="note", data={...})` | Write a reasoning note or decision to the session log |


**Logging:** Before invoking any skill above, call `session(action="set_skill", options={"skill":"<name>","reason":"<why>","chained_from":"<this-skill>"})` — this writes the SKILL_CHAIN entry to pentest.log.

---

## ATT&CK Coverage

| Technique | ID | What we gather |
|-----------|----|----------------|
| Gather Victim Identity Info | T1589 | Employee names, emails, roles, credentials |
| Gather Victim Network Info | T1590 | IP ranges, domains, subdomains, DNS records |
| Gather Victim Org Info | T1591 | Business relationships, physical locations, org structure |
| Search Open Websites/Domains | T1593 | Social media, code repos, job postings |
| Search Open Technical DBs | T1596 | WHOIS, DNS, certificate transparency, Shodan |
| Search Victim-Owned Websites | T1594 | Wayback Machine cached pages, exposed endpoints |

---

## OSINT Confidence Scoring

Every finding must be assigned a confidence level. Include the confidence and source list in every `report(action="finding", data={...})` call.

| Confidence | Criteria |
|------------|----------|
| **Confirmed** | Directly verified from authoritative source — WHOIS registrant matches org; SMTP RCPT TO returns 250 OK; crt.sh returns exact subdomain that resolves |
| **Likely** | Corroborated by 2+ independent sources — email pattern inferred from 3+ theHarvester results; employee on LinkedIn AND GitHub; subdomain from crt.sh AND subfinder |
| **Speculative** | Single source, no corroboration — one email from a paste site; subdomain from one source that does not resolve; employee name from metadata only |

**Rules:** 2+ independent sources → upgrade to Likely. 3+ sources with direct verification → Confirmed. Always note sources in evidence.

---

## Depth Presets

| Depth | What runs | Default limits |
|-------|-----------|----------------|
| `quick` | theHarvester + subfinder + WHOIS + DNS + crt.sh | $0.05 | 10 min | 8 calls |
| `standard` | Quick + amass + dnstwist + whatweb + wafw00f + email SMTP verification + cert transparency + Wayback + document metadata | $0.20 | 30 min | 20 calls |
| `thorough` | Standard + fierce + Shodan/Censys + subdomain takeover + cloud storage enum + social media + code repos + credential leaks + DNS history | unlimited | unlimited | unlimited |

---

## Workflow

### Before running any tool

If the request does not specify depth, ask the user:

> **Target:** `<domain or organization>`
> **Focus:** `<all, email, infra, social>`
>
> **Which OSINT depth?**
> - `quick` — theHarvester + subdomains + WHOIS + crt.sh *($0.05 · 10 min)*
> - `standard` — quick + amass + email verification + Wayback + metadata *($0.20 · 30 min)*
> - `thorough` — standard + Shodan + cloud enum + social + takeover detection *(unlimited)*

---

### Phase 0 — Scope & Setup

0. Call `session(action="start", options={...})` with target domain, depth, and limits
1. Call `report(action="dashboard", data={"port": 7777})` — live findings tracker
2. Call `report(action="note", data={...})` — record target domain, organization name, known info

---

### Phase 1 — Domain & DNS Intelligence

Run in parallel:
```
kali(command="whois DOMAIN")
kali(command="dig DOMAIN any +noall +answer && dig DOMAIN mx +short && dig DOMAIN txt +short && dig DOMAIN ns +short")
scan(tool="subfinder", target="DOMAIN")
kali(command="dnsrecon -d DOMAIN -t std")
```

**Analyze:** registrant info, name servers (hosting clues), MX (email provider), TXT (SPF/DKIM/DMARC), SOA admin email, subdomains.

---

### Phase 2 — Certificate Transparency Log Mining

**Subdomain discovery via crt.sh:**
```
kali(command="curl -s 'https://crt.sh/?q=%25.DOMAIN&output=json' | jq -r '.[].name_value' | sort -u")
```

**Historical cert analysis with issuance dates and issuers:**
```
kali(command="curl -s 'https://crt.sh/?q=%25.DOMAIN&output=json' | jq -r '.[] | \"\\(.not_before) \\(.not_after) \\(.name_value) \\(.issuer_name)\"' | sort | head -100")
```

**Wildcard cert detection — reveals infrastructure scope:**
```
kali(command="curl -s 'https://crt.sh/?q=%25.DOMAIN&output=json' | jq -r '.[].name_value' | grep '^\*' | sort -u")
```

**What to look for:** subdomains not found by subfinder (crt.sh often finds internal/staging names), wildcard certs (`*.internal.DOMAIN`) revealing naming conventions, expired certs for forgotten services, issuer patterns (Let's Encrypt = automated; DigiCert = enterprise), SAN fields listing multiple domains.

Cross-reference with subfinder results. Both sources → **Confirmed**. crt.sh-only → **Likely**, check DNS resolution.

---

### Phase 3 — Email Discovery & SMTP Verification (standard+)

**Email harvesting:**
```
kali(command="theHarvester -d DOMAIN -b all -l 200")
```

Extract email addresses, naming conventions (first.last@, firstl@, f.last@), hostnames, employee names.

**Identify the mail server, then probe with three SMTP methods:**
```
kali(command="dig DOMAIN mx +short | sort -n | head -1 | awk '{print $2}'")
kali(command="smtp-user-enum -M VRFY -U /usr/share/seclists/Usernames/top-usernames-shortlist.txt -t MAIL_SERVER -p 25")
kali(command="smtp-user-enum -M EXPN -U /usr/share/seclists/Usernames/Names/names.txt -t MAIL_SERVER -p 25")
kali(command="smtp-user-enum -M RCPT -D DOMAIN -U /usr/share/seclists/Usernames/top-usernames-shortlist.txt -t MAIL_SERVER -p 25")
```

**Manual verification with swaks:**
```
kali(command="swaks --to target@DOMAIN --server MAIL_SERVER --quit-after RCPT 2>&1 | grep -E '250|550|553|451'")
```

**SMTP response analysis:**

| Response | Meaning | Confidence |
|----------|---------|------------|
| `250 OK` / `250 2.1.5` | Valid mailbox | **Confirmed** |
| `550 5.1.1 User unknown` | Does not exist | Invalid |
| `550 5.7.1 Relay denied` | Relay blocked — try RCPT TO | Inconclusive |
| `451 4.7.1 Try again later` | Greylisting — retry in 5 min | Retry |
| `252 Cannot VRFY` | VRFY disabled — try RCPT TO | Inconclusive |

**Catch-all detection — send a clearly fake address:**
```
kali(command="swaks --to definitelynotarealuser12345@DOMAIN --server MAIL_SERVER --quit-after RCPT 2>&1 | grep -E '250|550'")
```
If fake address returns `250 OK`, the domain uses catch-all — SMTP cannot confirm individual addresses. Log with `report(action="note", data={...})`.

**Timing analysis — some servers accept all but respond slower for valid addresses:**
```
kali(command="for user in fakeuser1 fakeuser2 fakeuser3 realuser1 realuser2; do echo -n \"$user: \"; { time swaks --to $user@DOMAIN --server MAIL_SERVER --quit-after RCPT; } 2>&1 | grep real; done")
```

Call `report(action="finding", data={...})` for email pattern and verified employee list with confidence level.

---

### Phase 4 — Infrastructure Mapping (standard+)

Run in parallel:
```
kali(command="amass enum -passive -d DOMAIN -timeout 5")
kali(command="dnsrecon -d DOMAIN -t axfr")
kali(command="fierce --domain DOMAIN")
kali(command="dnstwist --format csv DOMAIN | head -50")
kali(command="whatweb -a 1 https://DOMAIN")
kali(command="wafw00f https://DOMAIN")
```

Call `report(action="diagram", data={...})` with infrastructure map after this phase.

---

### Phase 5 — Subdomain Takeover Detection (thorough)

**Extract CNAMEs for all discovered subdomains:**
```
kali(command="cat /tmp/subdomains.txt | while read sub; do cname=$(dig +short CNAME $sub); if [ -n \"$cname\" ]; then echo \"$sub -> $cname\"; fi; done")
```

**Service-specific takeover fingerprints:**

| Service | CNAME pattern | Indicator |
|---------|---------------|-----------|
| GitHub Pages | `*.github.io` | "There isn't a GitHub Pages site here" |
| Heroku | `*.herokuapp.com` | "No such app" |
| AWS S3 | `*.s3.amazonaws.com` | "NoSuchBucket" XML |
| Azure | `*.azurewebsites.net` | "404 Web Site not found" |
| Shopify | `*.myshopify.com` | "shop is currently unavailable" |
| Fastly | `*.fastly.net` | "Fastly error: unknown domain" |
| Fly.io | `*.fly.dev` | NXDOMAIN on CNAME target |

**Automated CNAME + response body check:**
```
kali(command="cat /tmp/subdomains.txt | while read sub; do cname=$(dig +short CNAME $sub 2>/dev/null); if [ -n \"$cname\" ]; then body=$(curl -s --max-time 5 \"https://$sub\" 2>/dev/null); if echo \"$body\" | grep -qiE 'NoSuchBucket|no such app|there isn.t a GitHub Pages|unknown domain|unavailable'; then echo \"TAKEOVER: $sub -> $cname\"; fi; fi; done")
```

**NXDOMAIN check — CNAME target no longer exists:**
```
kali(command="cat /tmp/subdomains.txt | while read sub; do cname=$(dig +short CNAME $sub 2>/dev/null); if [ -n \"$cname\" ]; then result=$(dig +short $cname 2>/dev/null); if [ -z \"$result\" ]; then echo \"DANGLING: $sub -> $cname\"; fi; fi; done")
```

Dangling CNAME = **Critical** finding. Call `report(action="finding", data={...})` immediately.

---

### Phase 6 — Shodan/Censys Intelligence (thorough)

**Shodan queries:**
```
kali(command="curl -s 'https://api.shodan.io/shodan/host/search?key=SHODAN_KEY&query=org:\"TARGET_ORG\"' | jq '.matches[] | {ip: .ip_str, port: .port, product: .product, version: .version}'")
kali(command="curl -s 'https://api.shodan.io/shodan/host/search?key=SHODAN_KEY&query=ssl.cert.subject.cn:DOMAIN' | jq '.matches[] | {ip: .ip_str, port: .port, hostnames: .hostnames}'")
```

**Useful Shodan dorks:** `org:"Company"` (all hosts), `hostname:DOMAIN`, `ssl.cert.subject.cn:DOMAIN` (cert-based discovery), `net:IP_RANGE/24`, `port:3389 org:"Company"` (RDP), `port:27017 org:"Company"` (MongoDB), `port:9200 org:"Company"` (Elasticsearch), `"X-Jenkins" org:"Company"`, `http.favicon.hash:HASH` (favicon fingerprint).

**Censys + Shodan historical data:**
```
kali(command="curl -s 'https://search.censys.io/api/v2/hosts/search?q=services.tls.certificates.leaf.subject.common_name:DOMAIN' -u 'CENSYS_ID:CENSYS_SECRET' | jq '.result.hits[] | {ip: .ip, services: [.services[] | {port: .port, service_name: .service_name}]}'")
kali(command="curl -s 'https://api.shodan.io/shodan/host/IP?key=SHODAN_KEY&history=true' | jq '.data[] | {timestamp: .timestamp, port: .port, product: .product, version: .version}' | head -50")
```

If no API keys, use web interfaces and record with `report(action="note", data={...})`. Call `report(action="finding", data={...})` for exposed databases, admin panels, or unpatched software.

---

### Phase 7 — Wayback Machine Intelligence (standard+)

**Endpoint discovery:**
```
kali(command="echo DOMAIN | waybackurls | sort -u | head -200")
```

**Filter for sensitive file types:**
```
kali(command="echo DOMAIN | waybackurls | grep -iE '\\.js$|\\.json$|\\.xml$|\\.conf$|\\.env$|\\.bak$|\\.sql$|\\.zip$' | sort -u")
```

**Old API version discovery:**
```
kali(command="echo DOMAIN | waybackurls | grep -iE '/api/v[0-9]|/api/|/v[0-9]/' | sort -u")
```

**Parameter harvesting:**
```
kali(command="echo DOMAIN | waybackurls | grep '?' | cut -d'?' -f2 | tr '&' '\n' | cut -d'=' -f1 | sort -u")
```

**JavaScript analysis for API keys/secrets:**
```
kali(command="echo DOMAIN | waybackurls | grep -iE '\\.js$' | sort -u | head -20 | while read url; do echo \"--- $url ---\"; curl -s \"https://web.archive.org/web/2024/$url\" | grep -oiE '(api[_-]?key|secret|token|password|auth)[\"'\\'']?\\s*[:=]\\s*[\"'\\''][^\"'\\''\\ ]+' | head -5; done")
```

**Archived sensitive files check:**
```
kali(command="for path in robots.txt .env .env.example sitemap.xml .git/config wp-config.php web.config; do status=$(curl -s -o /dev/null -w '%{http_code}' \"https://web.archive.org/web/2024/https://DOMAIN/$path\"); if [ \"$status\" = \"200\" ]; then echo \"FOUND: $path\"; fi; done")
```

**Look for:** deprecated API versions still live, hardcoded keys in JS, parameter names revealing internals (`internal_id`, `debug`, `admin_token`), old admin panels. Confidence is **Likely** until verified against live target.

---

### Phase 8 — Social Media OSINT (thorough)

**LinkedIn employee discovery via Google dorks:**
```
kali(command="curl -s 'https://www.google.com/search?q=site:linkedin.com/in+%22COMPANY%22&num=50' -H 'User-Agent: Mozilla/5.0' | grep -oP 'linkedin\\.com/in/[a-zA-Z0-9-]+' | sort -u | head -30")
```

Search by department (Engineering, Security, DevOps). Identify CISO/CTO/VP Eng. Cross-reference names with email pattern from Phase 3.

**GitHub org analysis:**
```
kali(command="curl -s 'https://api.github.com/orgs/ORG_NAME/repos?per_page=100&sort=updated' | jq '.[] | {name: .name, url: .html_url, language: .language, updated: .updated_at}'")
```

**Extract emails from git commit history:**
```
kali(command="curl -s 'https://api.github.com/repos/ORG_NAME/REPO_NAME/commits?per_page=100' | jq -r '.[].commit.author | \"\\(.name) <\\(.email)>\"' | sort -u")
```

**Search for secrets in public repos:**
```
kali(command="curl -s 'https://api.github.com/search/code?q=org:ORG_NAME+password+OR+secret+OR+api_key+OR+token' -H 'Accept: application/vnd.github.v3+json' | jq '.items[] | {repo: .repository.full_name, path: .path}' | head -30")
```

**Env files and CI/CD configs revealing infra:**
```
kali(command="curl -s 'https://api.github.com/search/code?q=org:ORG_NAME+filename:.env.example+OR+filename:.github/workflows' -H 'Accept: application/vnd.github.v3+json' | jq '.items[] | {repo: .repository.full_name, path: .path}'")
```

**Pastebin/Gist monitoring:**
```
kali(command="curl -s 'https://api.github.com/search/code?q=DOMAIN+in:gist' -H 'Accept: application/vnd.github.v3+json' | jq '.items[] | {url: .html_url}' | head -20")
```

Call `report(action="finding", data={...})` for any leaked credentials or secrets.

---

### Phase 9 — Cloud Storage Enumeration (thorough)

**S3 bucket fuzzing** (patterns: COMPANY, COMPANY-backup, -dev, -prod, -assets, -data, -static, -media, -logs, -staging, -uploads, -internal, -cdn):
```
kali(command="for p in COMPANY COMPANY-backup COMPANY-dev COMPANY-prod COMPANY-assets COMPANY-data COMPANY-static COMPANY-media COMPANY-logs COMPANY-staging COMPANY-uploads COMPANY-internal COMPANY-cdn; do s=$(curl -s -o /dev/null -w '%{http_code}' \"https://$p.s3.amazonaws.com\" 2>/dev/null); if [ \"$s\" != \"000\" ] && [ \"$s\" != \"404\" ]; then echo \"S3: $p ($s)\"; fi; done")
kali(command="aws s3 ls s3://BUCKET_NAME --no-sign-request 2>&1 | head -20")
```

**Azure Blob + GCS enumeration:**
```
kali(command="for p in COMPANY COMPANYdev COMPANYprod COMPANYbackup COMPANYdata; do s=$(curl -s -o /dev/null -w '%{http_code}' \"https://$p.blob.core.windows.net\" 2>/dev/null); if [ \"$s\" != \"000\" ] && [ \"$s\" != \"404\" ]; then echo \"AZURE: $p ($s)\"; fi; done")
kali(command="for p in COMPANY COMPANY-backup COMPANY-dev COMPANY-prod COMPANY-assets; do s=$(curl -s -o /dev/null -w '%{http_code}' \"https://storage.googleapis.com/$p\" 2>/dev/null); if [ \"$s\" != \"000\" ] && [ \"$s\" != \"404\" ]; then echo \"GCS: $p ($s)\"; fi; done")
```

**Severity:** 403 (exists, denied) = **Low**. 200 on list/read = **High**. Write succeeds = **Critical**.

---

### Phase 10 — Document Metadata Extraction (standard+)

**Download and batch extract:**
```
kali(command="metagoofil -d DOMAIN -t pdf,doc,xls,ppt,docx,xlsx,pptx -l 30 -n 20 -o /tmp/meta")
kali(command="exiftool -r /tmp/meta/ 2>/dev/null | grep -iE 'author|creator|producer|company|email|software|gps|last modified by' | sort -u")
kali(command="for f in /tmp/meta/*; do echo \"=== $(basename $f) ===\"; exiftool -Author -Creator -Producer -Company -LastModifiedBy -Software -GPSPosition \"$f\" 2>/dev/null | grep -v '^$'; done")
```

**Key fields:** `Author`/`Last Modified By` = employee names (cross-reference with email pattern). `Creator`/`Producer` = software versions (tech stack, possible CVEs). `GPS Position` = office locations. `Company` = subsidiaries, parent orgs.

**Extract unique employees and software:**
```
kali(command="exiftool -Author -LastModifiedBy -r /tmp/meta/ 2>/dev/null | awk -F': ' '{print $2}' | sort -u | grep -v '^$'")
kali(command="exiftool -Creator -Producer -Software -r /tmp/meta/ 2>/dev/null | awk -F': ' '{print $2}' | sort -u | grep -v '^$'")
```

---

### Phase 11 — DNS History & Passive DNS (thorough)

**Zone transfer attempt:**
```
kali(command="dig axfr DOMAIN @NS_SERVER")
```

**Passive DNS sources:**
```
kali(command="curl -s 'https://www.virustotal.com/api/v3/domains/DOMAIN/subdomains?limit=40' -H 'x-apikey: VT_KEY' | jq -r '.data[].id'")
kali(command="curl -s 'https://api.securitytrails.com/v1/history/DOMAIN/dns/a' -H 'APIKEY: ST_KEY' | jq '.records[] | {first_seen: .first_seen, last_seen: .last_seen, values: [.values[].ip]}'")
kali(command="curl -s 'https://api.hackertarget.com/hostsearch/?q=DOMAIN' | head -50")
```

**Historical MX/NS changes:**
```
kali(command="curl -s 'https://api.securitytrails.com/v1/history/DOMAIN/dns/mx' -H 'APIKEY: ST_KEY' | jq '.records[] | {first_seen: .first_seen, values: [.values[].host]}'")
```

**What DNS history reveals:** A record changes = hosting migrations (old IPs may still serve content). MX changes = email provider switches. NS changes = DNS provider migrations. Old IPs = check with Shodan for residual services.

Call `report(action="finding", data={...})` if old infrastructure is still reachable.

---

### Phase 12 — Credential Leak Check (thorough)

```
kali(command="curl -s 'https://haveibeenpwned.com/api/v3/breachedaccount/test@DOMAIN' -H 'hibp-api-key: KEY' 2>/dev/null || echo 'HIBP API key required'")
```
Search paste sites manually. Call `report(action="finding", data={...})` for confirmed leaks.

---

### Phase 13 — Report & Wrap-Up

1. Call `report(action="diagram", data={...})` with OSINT map:
```mermaid
flowchart TD
    Org["Target Organization"] --> People["People: N employees"]
    Org --> Domains["Domains: N subdomains"]
    Org --> Tech["Tech Stack"]
    Org --> Email["Email: pattern at target.com"]
    Org --> Repos["Code: N repos"]
    Org --> Cloud["Cloud: N buckets"]
    Domains --> Takeover["Takeover candidates: N"]
```

2. Call `report(action="note", data={...})` with summary:
```
OSINT Summary:
  Subdomains:        [count] ([count] crt.sh, [count] subfinder, [count] amass)
  Email pattern:     [pattern] — [count] addresses — [verification method]
  Employees:         [count] ([count] confirmed / [count] likely / [count] speculative)
  Tech stack:        [technologies]
  Cloud storage:     [count] buckets — [access levels]
  Subdomain takeover: [count] candidates
  Credential leaks:  [findings or "none confirmed"]
  Wayback findings:  [count] endpoints — [secrets found or "none"]
  DNS history:       [notable changes]
```

3. Call `session(action="complete", options={...})` with summary
4. **Chain to `/pentester`** if active scanning is authorized

---

## Chaining Other Skills

| Skill | When to invoke |
|-------|----------------|
| `/pentester` | OSINT complete — user authorizes active scanning |
| `/threat-modeling` | Use OSINT findings to build threat model before active testing |
| `/ai-redteam` | AI/LLM endpoint discovered during OSINT |
| `/ssl-tls-audit` | TLS services discovered — deep certificate and crypto audit |
| `/gh-export` | When user asks to file GitHub issues|

---

## Rules

- **`session(action="start", options={...})` is mandatory** — never run any other tool before it
- **All techniques must be PASSIVE** — no active exploitation (SMTP VRFY/RCPT TO is acceptable as standard email verification)
- **Batch independent tools in the same response** — they execute in parallel
- When any tool returns a LIMIT message, stop immediately and call `session(action="complete", options={...})`
- **Call `report(action="finding", data={...})` for significant discoveries** — email patterns, credential leaks, exposed cloud storage, subdomain takeover candidates, secrets in repos
- **Include confidence level in every finding** — Confirmed, Likely, or Speculative — with source list
- **Cross-reference sources** — upgrade confidence when multiple tools agree; downgrade single-source findings
- **Build the org map progressively** — domain, then people, infrastructure, technology, cloud
- **Use `report(action="note", data={...})` liberally** — document sources and confidence for each finding
- **Never fabricate findings** — only report what tool output confirms
- **Respect privacy** — focus on publicly available information relevant to security assessment
- **Mermaid syntax rules**: use `flowchart TD`, quote labels, no em-dashes, short alphanumeric node IDs
- Call `session(action="stop_kali")` at the end if `kali(command=...)` was used
