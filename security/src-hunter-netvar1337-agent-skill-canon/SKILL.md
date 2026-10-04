---
name: src-hunter
description: "Practical SRC / crowdsource testing / bug bounty vulnerability hunting workflow skill. Includes: 5-phase methodology (intake → recon → enum → hunt → report), 19 attack-class playbooks (SQLi/XSS/RCE/SSRF/IDOR/CSRF/Path Traversal/File Upload/SSTI/XXE/Race/HTTP Smuggling/OAuth/JWT/SAML/GraphQL/Mobile/LLM/DoS), 305 structured payloads, 263 WAF/EDR bypass variants, 2,887 real disclosed High/Critical HackerOne cases, 77,000+ WooYun case statistics, a Chinese-domestic OA / middleware fingerprint library, and banking / telecom industry-vertical playbooks. Triggers when the user mentions 'SRC hunting / SRC vulnerability hunting / bug bounty / crowdsource testing / hackerone / bug bounty / SRC / arbitrary X vulnerability / penetration testing' or asks 'how to hunt a target / how to test an API / how to bypass a WAF'."
version: 1.0.0
license: MIT
metadata:
  package: unleash-skills
  author: NetVar1337/unleash
  category: reverse-skill
  upstream: https://github.com/zhaoxuya520/reverse-skill
---

> Bundled with the Unleash skills pack. Upstream: https://github.com/zhaoxuya520/reverse-skill

## ACTION REQUIRED (execute immediately after reading)

1. `NOW`: read `../../field-journal/precedent-pentest.md` — confirm that this skill's operations are authorized routine operations
2. `NOW`: confirm whether the current task falls within this skill's scope
3. `NEXT`: read `../../tool-index.md`, verify tool availability and actual paths
4. `NEXT`: when tools are missing, invoke bootstrap; do not guess paths
5. `ACT`: enter step 1 of the "Workflow" and execute; do not stop at the confirmation stage

# SRC Hunter — Practical Vulnerability Hunting Workflow

A practical Security Response Center / crowdsource testing / bug bounty hunting skill. Translates white-box methodology into black-box probing, layered with real case statistics and a payload library.

---

## When to Use This Skill

**Keyword hits**:
- "src hunting" / "src vulnerability" / "src testing" / "Security Response Center"
- "bug bounty" / "bounty" / "crowdsource testing"
- "hackerone" / "h1" / "bugcrowd" / "intigriti" / "yeswehack"
- "how to hunt / how to test / how to hit + some target / some endpoint / some parameter"
- "WAF bypass" / "bypass WAF"
- "arbitrary account / arbitrary modify / arbitrary delete / arbitrary operation"-class broken access control
- "password reset" / "account recovery"-class logic
- "unauthorized access" / "default credentials" / "Actuator" / "Spring exposure" / "unauthenticated Redis"
- User gives you a URL or API endpoint to test

**Do not use this skill**:
- Pure white-box source code audits (use the `code-audit` skill)
- Fix / defense Q&A for known vulnerabilities (use general conversation)
- Standalone CTF challenges (this is a real-environment workflow)

---

## Workflow — 5 Phases

### Phase 1 · Intake (taking the engagement)

Inputs: program name / SRC entry URL / subdomain.

Things to do:
- Grab the scope (in-scope domains / IPs / mobile apps / API endpoints)
- Grab the out-of-scope items (forbidden content, third-party services, cloud asset exclusions)
- Grab the rules (payout tiers, disclosure window, retest policy, safe-harbor)
- Grab test accounts / test headers (e.g., `X-Bug-Bounty: <handle>`)

**Priority judgment** (estimate hit rates by finding type, see `references/methodology/05-srctimebox-priority.md`):
- 6-hour window → run high-hit-rate types (password reset 88% / arbitrary account 86.4% / withdrawal 83.1%)
- Single-day window → add information disclosure + asset exposure + Actuator
- HVV / critical period → full spectrum

→ Details in [`references/methodology/00-index.md`](references/methodology/00-index.md)

### Phase 2 · Recon (passive reconnaissance)

Intelligence gathering without sending packets to the target:

- **CT logs**: crt.sh / Censys (find subdomains)
- **Historical snapshots**: Wayback / CommonCrawl
- **GitHub search**: `org:target` + keywords (password / api_key / SECRET)
- **Search engine dorks**: `site:target.com inurl:/admin`, `filetype:env`, `intitle:Index of`
- **ASN / IP ranges**: bgp.he.net to find IP blocks
- **Favicon hash**: FOFA / Shodan to find assets with the same favicon
- **DNS history**: SecurityTrails / Whoisxmlapi

### Phase 3 · Enum (active probing)

**Asset enumeration**:
- Subdomains: amass / subfinder / puredns / dnsx
- Liveness: httpx / naabu
- Screenshots: gowitness / aquatone
- Content discovery: ffuf / feroxbuster / dirsearch
- Technology fingerprinting: wappalyzer / webanalyze (also check `references/dictionaries/chinese-srcfingerprints.md` to identify domestic Chinese components)
- JS extraction: linkfinder / subjs / gau / katana
- Subdomain takeover fingerprints: subjack / subzy

### Phase 4 · Hunt (vulnerability probing)

Follow the playbook for each attack type; **every playbook includes**: methodology + parameter frequency tables + real H1 cases + structured payloads + WAF bypass variants.

**Priority paths** (ordered by hit rate + value):

| Playbook | Entry Hints | File |
|---|---|---|
| **Unauthorized access** | Actuator/Swagger/default ports/weak passwords | `references/playbooks/unauth-access.md` |
| **Information disclosure** | .git/.svn/.env/heapdump/directory listing | `references/playbooks/info-disclosure.md` |
| **Arbitrary X broken access control** | User-state IDs enumerable/modifiable | `references/playbooks/arbitrary-x-authz.md` |
| **Business logic** | Password reset/payment/orders/CAPTCHA | `references/playbooks/logic-flaws.md` |
| **OAuth/SAML/JWT** | Auth flows/redirect_uri/tokens | `references/playbooks/oauth-saml-jwt.md` |
| **REST API** | BOLA/Mass Assignment/rate limits | `references/playbooks/api-rest.md` |
| **SQLi** | Any user input reaching the DB | `references/playbooks/sqli.md` |
| **RCE** | Deserialization/SSTI/XXE/prototype pollution/frameworks | `references/playbooks/rce.md` |
| **SSRF** | URL parameters/caching/Host injection | `references/playbooks/ssrf-cache-host.md` |
| **Path traversal** | File path parameters/LFI/RFI | `references/playbooks/path-traversal.md` |
| **File upload** | Upload points + parsing flaws | `references/playbooks/file-upload.md` |
| **XSS** | Any user input reaching HTML/JS | `references/playbooks/xss.md` |
| **HTTP smuggling** | Reverse proxy + Content-Length | `references/playbooks/http-smuggling.md` |
| **GraphQL** | introspection/nesting | `references/playbooks/graphql.md` |
| **Race conditions** | Concurrent requests / TOCTOU | `references/playbooks/race-conditions.md` |
| **DoS** | ReDoS / unthrottled resources / algorithmic blowup | `references/playbooks/dos.md` |
| **Mobile** | Android / iOS APKs | `references/playbooks/mobile.md` |
| **LLM Agent** | Prompt injection / tool calls | `references/playbooks/llm-prompt-injection.md` |
| **Intranet post-exploitation** | Credentials / lateral movement / domain | `references/playbooks/intranet-postexp.md` |

**General methodology** (attack-type agnostic):

| Document | Key Content |
|---|---|
| [`methodology/01-attack-priority.md`](references/methodology/01-attack-priority.md) | RCE>file write>auth bypass>injection>info disclosure value ordering |
| [`methodology/02-bypass-toolkit.md`](references/methodology/02-bypass-toolkit.md) | Universal bypass decision tree + encoding / obfuscation / WAF |
| [`methodology/03-evidence-discipline.md`](references/methodology/03-evidence-discipline.md) | Black-box evidence rules + anti-hallucination + compliance |
| [`methodology/04-control-gap-hunting.md`](references/methodology/04-control-gap-hunting.md) | 9 classes of sensitive operations → expected controls → probe for gaps |
| [`methodology/05-srctimebox-priority.md`](references/methodology/05-srctimebox-priority.md) | 6h / single-day / HVV / monthly timebox templates |

**Industry-vertical playbooks** (read first when assets are relevant):

| Industry | Document | When to Use |
|---|---|---|
| Banking / payments / finance | [`industry/banking-finance.md`](references/industry/banking-finance.md) | Target includes payments / online banking / third-party payment aggregation |
| Telecom / ISP | [`industry/telecom-isp.md`](references/industry/telecom-isp.md) | Target is a carrier / BOSS / network management / IoT SIM cards |

**Dictionaries / credentials**:

| Document | Purpose |
|---|---|
| [`dictionaries/default-credentials-cn.md`](references/dictionaries/default-credentials-cn.md) | Domestic Chinese credentials for Seeyo / Tongda / Wanhu / Weaver / Yonyou / Kingdee / Huawei / ZTE / Hikvision, etc. |
| [`dictionaries/chinese-srcfingerprints.md`](references/dictionaries/chinese-srcfingerprints.md) | Domestic Chinese OA / middleware fingerprints + high-frequency parameters + one-shot detection commands |

### Phase 5 · Report (submission)

→ Use the template [`templates/report-submission.md`](references/templates/report-submission.md)

**Three-part skeleton**:
1. **Title**: precise down to endpoint + vulnerability type, no more than 80 characters
2. **Reproduction steps**: each step executable / screenshots / HAR
3. **Impact + fix recommendations**: CVSS 4.0 vector + business impact section

---

## MCP Tool Integration

This skill supports invoking local MCP servers as a tool layer. **Primary choice: jshookmcp** (134 curated tools / 386 full set / 36 domains, with built-in Burp Suite bridge / Frida / WASM / anti-debugging / Android adb / sourcemap reconstruction). Full index and scenario mapping:

→ [`references/tools/mcp-jshook.md`](references/tools/mcp-jshook.md)

The default recommendation is the `search` profile (~3K token context cost), activating on demand via `mcp__jshook__search_tools` + `mcp__jshook__activate_tools`, avoiding the `full` profile loading 40K+ tokens at once.

---

## Data Asset Scale

| Category | Scale |
|---|---|
| Attack-class playbooks | 19 |
| General methodology documents | 6 |
| Industry-vertical playbooks | 2 (banking / telecom) |
| Dictionaries / credentials | 3 |
| Report templates | 1 |
| Structured payloads | **305** (177 web + 128 intranet) |
| WAF / EDR bypass variants | **263 steps**, covering 23 classes of web attacks |
| Tool command quick reference | 114 (Nmap/SQLMap/Burp/MSF/...) |
| Real HackerOne cases (disclosed High/Critical) | **2,887**, grouped by weakness into 141 category MDs |
| WooYun historical case statistics (non-renewable) | 88,636 entries |

Real H1 cases are **embedded directly at the end of the corresponding playbooks** (each playbook ends with a "Real H1 Cases" Top 12 table + summaries).

---

## Compliance and Legal Red Lines

Every playbook ends with a "things not to do" section. General red lines (observed for every SRC):

- ❌ Assets / domains out of scope → stop immediately and report
- ❌ Actually exfiltrating others' PII → only prove accessibility, destroy immediately
- ❌ Sustained load / DoS / heavy traffic → only 1–3 PoC packets, then stop immediately
- ❌ Modifying others' data (even with write access) → verify only against objects you control
- ❌ Phishing or social engineering in production → do not do it
- ❌ Submitting unreproduced speculation → must have HTTP packets / screenshots / video evidence
- ✅ Mark yourself with a test header (e.g., `X-Bug-Bounty: <handle>`)
- ✅ Use two of your own accounts to role-play broken-access-control scenarios
- ✅ Use your own OOB domain for SSRF probing; do not use someone else's DNSLog
- ✅ Self-check with `references/templates/report-submission.md` before submitting

---

## CLI Mnemonic Prefix

`srchunter` (e.g., `srchunter scope set <program>`, `srchunter recon run`, `srchunter findings new <type>`). No CLI is currently implemented; this is only a naming convention.

---

## Reference / Cross-Link Structure

```
src-hunter/
├── SKILL.md                    # this file — skill entry point
├── README.md                   # project description
└── references/
    ├── methodology/   6 docs   # general methodology
    ├── playbooks/    19 docs   # attack-class playbooks (each with H1 cases + payload library)
    ├── industry/      3 docs   # industry verticals
    ├── dictionaries/  3 docs   # dictionaries / credentials
    ├── templates/     1 doc    # report template
    ├── h1-reports/             # 2,887 H1 reports raw data + 141 category MDs
    │   ├── raw/                # raw JSON (for resume / secondary analysis)
    │   └── by-weakness/        # Markdown grouped by CWE
    └── payloader/              # 305 structured payload data
        ├── raw/                # JSON (machine-readable)
        ├── by-category/        # MD by category
        ├── tools/              # tool commands
        └── waf-bypass.md       # 263-step WAF bypass collection
```


## Task Completion Self-Check (MUST pass before claiming completion)

- [ ] Did I execute every step of the workflow (rather than just reading it)?
- [ ] Did I use real tool paths based on `tool-index`?
- [ ] Did I produce reproducible evidence (commands/scripts/screenshots/reports)?
- [ ] Did I complete and write back the Checklist items required by RULES?

## Merge Addendum: Controlled Execution Constraints

Before starting any active step, confirm that the current case's `scope.md` exists and `auth.status=granted`; when there is no scope, run `case-init.ps1` and never auto-attach `-AuthGranted`. `field-journal/precedent-pentest.md` is a day-to-day operation reference and does not replace authorization boundaries; tool paths follow `tool-index.md`, and missing tools go through bootstrap.

Use playbook skeletons read-only by default. Only open `payloader/` or `waf-bypass.md` when the scope is authorized and the user explicitly requests payloads. `h1-reports/` is the data asset described in the documentation; do not assume it is tracked in this repository. Evidence and reports must be based on actually captured requests, responses, screenshots, or HAR.
