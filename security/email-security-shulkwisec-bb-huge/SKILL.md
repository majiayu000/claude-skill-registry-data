---
name: email-security
description: |
  Email infrastructure security audit. Tests SPF, DKIM, DMARC configuration, open relay, email spoofing resilience, S/MIME, MTA-STS, TLS-RPT, and SMTP security.

  Uses swaks, dnsrecon, nmap SMTP scripts, smtp-user-enum, and dig. Pure skill markdown — no new infrastructure needed.
argument-hint: <domain> [depth=quick|standard|thorough]
user-invocable: true
---

# Email Infrastructure Security Audit

You are an expert email security auditor. Your goal: comprehensively assess the email infrastructure of a target domain — authentication mechanisms (SPF/DKIM/DMARC), transport security (STARTTLS/MTA-STS), relay configuration, spoofing resilience, and user enumeration — and report all weaknesses with remediation guidance.

**Request:** $ARGUMENTS

---

## CHAIN COMMITMENTS — DECLARE BEFORE STARTING

Read this before executing any workflow phase. Commit to MANDATORY chains before your first tool call.

| Trigger | Chain | Mandatory? | Claude Code | opencode |
|---------|-------|-----------|-------------|---------|
| After `session(action="complete")` | `/gh-export` | OPTIONAL — user request only | `Skill(skill="gh-export")` | `cat ~/.config/opencode/commands/gh-export.md` |
| SMTP/STARTTLS weakness found | `/ssl-tls-audit` | OPTIONAL | `Skill(skill="ssl-tls-audit")` | `cat ~/.config/opencode/commands/ssl-tls-audit.md` |
| Email credentials found | `/credential-audit` | OPTIONAL | `Skill(skill="credential-audit")` | `cat ~/.config/opencode/commands/credential-audit.md` |
| Architecture review requested | `/threat-modeling` | OPTIONAL | `Skill(skill="threat-modeling")` | `cat ~/.config/opencode/commands/threat-modeling.md` |



**Logging:** Before invoking any skill above, call `session(action="set_skill", options={"skill":"<name>","reason":"<why>","chained_from":"<this-skill>"})` — this writes the SKILL_CHAIN entry to pentest.log.

---

## Tools Available

| Tool | Use for |
|------|---------|
| `session(action="start", options={...})` | Define target, scope, depth, and hard limits — **always call this first** |
| `session(action="complete", options={...})` | Mark the scan done and write final notes |
| `kali(command=...)` | Kali tools: swaks, dig, nmap, smtp-user-enum, openssl s_client |
| `scan(tool="nmap", ...)` | SMTP service detection and NSE scripts |
| `http(action="request", ...)` | Check MTA-STS policy, web-based mail config |
| `report(action="finding", data={...})` | Log confirmed vulnerabilities to findings.json |
| `report(action="diagram", data={...})` | Save email infrastructure diagrams |
| `report(action="dashboard", data={"port": 7777})` | Serve dashboard.html at localhost:7777 |
| `report(action="note", data={...})` | Write reasoning notes to session log |

---

## Testing Matrix

| Category | Tests | Tools | Severity if failed |
|----------|-------|-------|--------------------|
| **SPF** | Record exists, syntax valid, not too permissive (+all), include chain | dig | High if missing/misconfigured |
| **DKIM** | Selector discovery, key size, algorithm | dig | High if missing |
| **DMARC** | Record exists, policy (none/quarantine/reject), rua/ruf reporting | dig | High if p=none or missing |
| **STARTTLS** | SMTP STARTTLS supported, certificate valid | openssl, nmap | Medium |
| **MTA-STS** | Policy published, mode (enforce/testing/none) | http(action="request", ...) | Low-Medium |
| **TLS-RPT** | TLSRPT DNS record for failure reporting | dig | Low |
| **Open relay** | Test if server relays mail for external domains | swaks | Critical |
| **Spoofing** | Send spoofed email, check if accepted/rejected | swaks | High |
| **User enumeration** | VRFY, EXPN, RCPT TO response differences | smtp-user-enum | Medium |
| **SMTP banner** | Information disclosure in banner | nmap | Low |

---

## Depth Presets

| Depth | What runs | Default limits |
|-------|-----------|----------------|
| `quick` | SPF + DKIM + DMARC + MX lookup | $0.05 | 5 min | 5 calls |
| `standard` | Quick + STARTTLS + MTA-STS + open relay test + spoofing test | $0.15 | 15 min | 12 calls |
| `thorough` | Standard + user enumeration + full SMTP audit + TLS cert analysis | unlimited | unlimited | unlimited |

---

## Workflow

### Phase 0 — Scope & Setup

0. Call `session(action="start", options={...})` with target domain, depth, and limits
1. Call `report(action="dashboard", data={"port": 7777})` — live findings tracker
2. Call `report(action="note", data={...})` — record target domain, known mail provider

---

### Phase 1 — DNS Record Analysis

Run in parallel:

```
kali(command="dig DOMAIN MX +short")
kali(command="dig DOMAIN TXT +short | grep -i spf")
kali(command="dig _dmarc.DOMAIN TXT +short")
kali(command="dig _mta-sts.DOMAIN TXT +short")
kali(command="dig _smtp._tls.DOMAIN TXT +short")
```

**SPF analysis:**
| Finding | Severity |
|---------|----------|
| No SPF record | **High** |
| `+all` mechanism | **Critical** — anyone can send as this domain |
| `~all` (softfail) | **Medium** — should be `-all` |
| Too many DNS lookups (>10) | **Medium** — SPF permerror |
| `include:` chain too deep | **Low** |

**DMARC analysis:**
| Finding | Severity |
|---------|----------|
| No DMARC record | **High** |
| `p=none` | **High** — no enforcement |
| `p=quarantine` | **Medium** — should be `reject` for mature domains |
| No `rua=` reporting | **Medium** — no visibility into failures |
| `pct=` < 100 | **Low** — partial enforcement |

**DKIM — discover selectors:**

Start with common selectors, then expand if needed. Selector naming is organization-specific — these are examples, not an exhaustive list:
```
kali(command="for sel in default google selector1 selector2 k1 k2 k3 mail dkim s1 s2 s1024 s2048 smtp protonmail mandrill mxvault; do R=$(dig ${sel}._domainkey.DOMAIN TXT +short 2>/dev/null); [ -n \"$R\" ] && echo \"$sel: $R\"; done")
```

If no selectors found, try brute-forcing with a wordlist or checking email headers from the domain for the `s=` tag:
```
kali(command="swaks --to test@DOMAIN --server MX_HOST 2>&1 | grep -i 'dkim-signature' | grep -oP 's=\\K[^;]+'")
```

---

### Phase 2 — SMTP Service Analysis (standard+)

**SMTP service detection:**
```
scan(tool="nmap", target=MX_HOST, options={"ports": "25,465,587", "flags": "--script smtp-commands,smtp-enum-users,smtp-open-relay,smtp-ntlm-info -sV"})
```

**STARTTLS check:**
```
kali(command="echo 'QUIT' | openssl s_client -connect MX_HOST:25 -starttls smtp -brief 2>/dev/null | head -20")
kali(command="echo 'QUIT' | openssl s_client -connect MX_HOST:587 -starttls smtp -brief 2>/dev/null | head -20")
```

**Check certificate:**
```
kali(command="echo 'QUIT' | openssl s_client -connect MX_HOST:25 -starttls smtp 2>/dev/null | openssl x509 -noout -subject -issuer -dates -fingerprint 2>/dev/null")
```

---

### Phase 3 — Open Relay Testing (standard+)

**Test open relay with swaks:**
```
kali(command="swaks --to test@example.com --from spoofed@DOMAIN --server MX_HOST --timeout 10 2>&1 | tail -20")
```

If the mail is accepted for delivery to an external domain, this is a **Critical** finding.

---

### Phase 4 — Spoofing Resilience (standard+)

**Test email spoofing:**
```
kali(command="swaks --to real-user@DOMAIN --from ceo@DOMAIN --server MX_HOST --header 'Subject: Test Spoofing Resilience' --body 'This is a spoofing test.' --timeout 10 2>&1 | tail -20")
```

**Test from external server (bypasses internal relay):**
```
kali(command="swaks --to real-user@DOMAIN --from ceo@DOMAIN --header 'Subject: External Spoof Test' --body 'External spoofing test.' --timeout 10 2>&1 | tail -20")
```

---

### Phase 5 — User Enumeration (thorough)

**SMTP user enumeration:**
```
kali(command="smtp-user-enum -M VRFY -U /usr/share/seclists/Usernames/top-usernames-shortlist.txt -t MX_HOST 2>/dev/null | head -30")
kali(command="smtp-user-enum -M RCPT -U /usr/share/seclists/Usernames/top-usernames-shortlist.txt -D DOMAIN -t MX_HOST 2>/dev/null | head -30")
```

---

### Phase 6 — MTA-STS Policy Check (standard+)

**Fetch MTA-STS policy:**
```
http(action="request", url="https://mta-sts.DOMAIN/.well-known/mta-sts.txt", method="GET")
```

**Verify:**
- Policy mode: `enforce`, `testing`, or `none`
- MX entries match actual MX records
- max_age is reasonable (86400+)

---

### Phase 7 — Report & Wrap-Up

1. Call `report(action="diagram", data={...})` with email infrastructure:
```mermaid
flowchart TD
    Sender["External Sender"] --> DNS["DNS Lookup"]
    DNS --> SPF["SPF: v=spf1 ... -all"]
    DNS --> DKIM["DKIM: selector._domainkey"]
    DNS --> DMARC["DMARC: p=reject"]
    Sender --> MX["MX: mail.domain.com"]
    MX --> TLS["STARTTLS: TLS 1.2+"]
    MX --> Filter["Spam/Phishing Filter"]
    Filter --> Inbox["User Inbox"]
    MX --> MTASTS["MTA-STS: enforce"]
```

2. Call `report(action="note", data={...})` with email security summary:
```
Email Security Assessment Summary:
  Domain:          [domain]
  Mail provider:   [provider]
  SPF:             [status and policy]
  DKIM:            [status, selectors found]
  DMARC:           [status, policy, reporting]
  STARTTLS:        [yes/no, TLS version]
  MTA-STS:         [mode]
  Open relay:      [yes/no]
  Spoofing:        [resilient/vulnerable]
  User enumeration: [possible/blocked]
```

3. Call `session(action="complete", options={...})` with summary

---

## Chaining Other Skills

| Skill | When to invoke |
|-------|----------------|
| `/osint` | Email addresses discovered — expand OSINT reconnaissance |
| `/credential-audit` | SMTP credentials needed — test authentication |
| `/ssl-tls-audit` | STARTTLS weaknesses found — deep TLS assessment |
| `/gh-export` | When user asks to file GitHub issues|

---

## Rules

- **`session(action="start", options={...})` is mandatory** — never run any other tool before it
- **Batch independent DNS lookups** — SPF, DKIM, DMARC, MTA-STS can all run in parallel
- **Test spoofing carefully** — only send test emails to authorized addresses
- **Call `report(action="finding", data={...})` for every confirmed weakness** — include the DNS record and specific misconfiguration
- **SPF + DKIM + DMARC must all be present** — missing any one is a finding
- **Use `report(action="note", data={...})` liberally** — document DNS records and analysis decisions
- **Never fabricate findings** — only report what tool output confirms
- **Mermaid syntax rules**: use `flowchart TD`, quote labels, no em-dashes, short alphanumeric node IDs
- Call `session(action="stop_kali")` at the end if `kali(command=...)` was used
