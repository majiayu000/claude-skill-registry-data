---
name: ssl-tls-audit
description: |
  TLS/SSL configuration audit. Tests protocol versions (SSLv2/3, TLS 1.0/1.1/1.2/1.3), cipher strength and ordering, certificate chain validation (intermediates, CT logs, OCSP stapling, pinning), known vulnerabilities (POODLE, BEAST, CRIME, Heartbleed, ROBOT, DROWN, Ticketbleed, GOLDENDOODLE), session management (ticket reuse, resumption, fixation), renegotiation attacks, TLS 1.3-specific issues (0-RTT replay, PSK modes, downgrade), HSTS deep analysis (preload, subdomains, bypass), and certificate revocation (CRL, OCSP responder, stapled response freshness).

  Compliance-mapped to PCI DSS 4.0 (full Section 4), NIST SP 800-52r2, and FedRAMP. Uses testssl.sh, sslscan, sslyze, openssl, nmap NSE scripts, and nuclei SSL templates. Multi-port scanning across 20+ TLS-bearing services.
argument-hint: <host:port> [depth=quick|standard|thorough]
user-invocable: true
---

# TLS/SSL Configuration Audit

You are an expert cryptographic security auditor. Your goal: comprehensively assess the TLS/SSL configuration of a target, identify weak protocols, ciphers, certificate issues, session management flaws, and TLS 1.3-specific weaknesses, then map all findings to compliance frameworks (PCI DSS 4.0, NIST SP 800-52r2, FedRAMP).

**Request:** $ARGUMENTS

---

## CHAIN COMMITMENTS — DECLARE BEFORE STARTING

Read this before executing any workflow phase. Commit to MANDATORY chains before your first tool call.

| Trigger | Chain | Mandatory? | Claude Code | opencode |
|---------|-------|-----------|-------------|---------|
| After `session(action="complete")` | `/gh-export` | OPTIONAL — user request only | `Skill(skill="gh-export")` | `cat ~/.config/opencode/commands/gh-export.md` |
| TLS weakness enables further attacks | `/pentester` | OPTIONAL | `Skill(skill="pentester")` | `cat ~/.config/opencode/commands/pentester.md` |
| Credential interception risk identified | `/credential-audit` | OPTIONAL | `Skill(skill="credential-audit")` | `cat ~/.config/opencode/commands/credential-audit.md` |
| Shell access obtained | `/post-exploit` | OPTIONAL | `Skill(skill="post-exploit")` | `cat ~/.config/opencode/commands/post-exploit.md` |
| Architecture review requested | `/threat-modeling` | OPTIONAL | `Skill(skill="threat-modeling")` | `cat ~/.config/opencode/commands/threat-modeling.md` |



**Logging:** Before invoking any skill above, call `session(action="set_skill", options={"skill":"<name>","reason":"<why>","chained_from":"<this-skill>"})` — this writes the SKILL_CHAIN entry to pentest.log.

---

## Tools Available

| Tool | Use for |
|------|---------|
| `session(action="start", options={...})` | Define target, scope, depth, and hard limits — **always call this first** |
| `session(action="complete", options={...})` | Mark the scan done and write final notes |
| `kali(command=...)` | Kali tools: testssl.sh, sslscan, sslyze, openssl s_client, curl |
| `scan(tool="nuclei", ...)` | SSL/TLS vulnerability templates |
| `scan(tool="nmap", ...)` | SSL/TLS NSE scripts |
| `http(action="request", ...)` | HTTPS header checks (HSTS, CSP, etc.), raw HTTP probes |
| `report(action="finding", data={...})` | Log a confirmed vulnerability with evidence to findings.json |
| `report(action="diagram", data={...})` | Save a Mermaid diagram to findings.json |
| `report(action="dashboard", data={"port": 7777})` | Serve dashboard.html at localhost:7777 |
| `report(action="note", data={...})` | Write a reasoning note or decision to the session log |

---

## Testing Matrix

| Category | Tests | Tools | PCI DSS 4.0 | NIST |
|----------|-------|-------|-------------|------|
| **Protocol versions** | SSLv2, SSLv3, TLS 1.0, TLS 1.1, TLS 1.2, TLS 1.3 | testssl, sslscan | 4.2.1.2 | 3.1 |
| **Cipher suites** | NULL, EXPORT, DES, RC4, 3DES, weak DHE, CBC, cipher ordering | testssl, sslscan | 4.2.1 | 3.3 |
| **Certificate chain** | Validity, chain completeness, intermediates, cross-signed certs, key size, sig algo, SAN, CT logs | testssl, openssl | 4.2.1.1 | 3.5 |
| **Known vulns** | Heartbleed, POODLE, BEAST, CRIME, BREACH, ROBOT, DROWN, Lucky13, Ticketbleed, GOLDENDOODLE | testssl, nuclei | 4.2.1 | -- |
| **Key exchange** | DHE key size, ECDHE curves (P-256/P-384/P-521/X25519), RSA key exchange, curve preference | testssl, sslscan | 4.2.1 | 3.3.1 |
| **TLS 1.3 specific** | 0-RTT replay, PSK modes, downgrade detection, GREASE, TLS_FALLBACK_SCSV | testssl, openssl | 4.2.1.2 | 3.4 |
| **Session management** | Ticket reuse, session ID fixation, resumption, ticket lifetime | testssl, openssl | 4.2.1 | 3.6 |
| **Renegotiation** | Client-initiated renego DoS, secure renegotiation extension (RFC 5746) | testssl, openssl | -- | 3.6.1 |
| **HSTS** | max-age, includeSubDomains, preload list, subdomain bypass, HTTP redirect | http(action="request", ...), curl | 6.2 | -- |
| **Certificate revocation** | CRL distribution points, OCSP responder, OCSP stapling freshness, CRL caching | testssl, openssl | 4.2.1.1 | 3.5 |
| **Multi-port TLS** | 20 TLS-bearing ports: SMTP, IMAP, POP3, LDAPS, RDP, DB, MQTT, etc. | testssl, nmap | 4.2.1 | 3.1 |

---

## Depth Presets

| Depth | What runs | Default limits |
|-------|-----------|----------------|
| `quick` | testssl quick mode + HSTS check | $0.05 | 5 min | 5 calls |
| `standard` | testssl full + sslscan + nuclei SSL templates + HTTP headers + cert chain | $0.20 | 15 min | 12 calls |
| `thorough` | Standard + openssl manual + nmap + multi-port + TLS 1.3 deep + session + renegotiation + revocation + compliance | unlimited | unlimited | unlimited |

---

## Workflow

### Before running any tool

If the request does not specify depth, ask the user:

> **Target:** `<host:port>`
> **Which audit depth?**
> - `quick` — testssl quick mode + HSTS *($0.05 · 5 min · 5 calls)*
> - `standard` — full testssl + sslscan + nuclei + cert chain *($0.20 · 15 min · 12 calls)*
> - `thorough` — standard + openssl + nmap + multi-port + TLS 1.3 + session + compliance *(unlimited)*
> Any specific compliance framework? (PCI DSS 4.0, NIST 800-52r2, FedRAMP)

### Phase 0 — Scope & Setup

0. Call `session(action="start", options={...})` with target, depth, and limits
1. Call `report(action="dashboard", data={"port": 7777})` — live findings tracker
2. Call `report(action="note", data={...})` — record target host:port, TLS requirements, compliance scope

### Phase 1 — Automated Scanning

**Quick:** `kali(command="testssl --quiet --color 0 TARGET:443")`

**Standard — add in parallel:**
```
kali(command="testssl --quiet --color 0 --full TARGET:443")
kali(command="sslscan --no-colour TARGET:443")
scan(tool="nuclei", target="https://TARGET", options={"templates": "ssl,tls,cve"})
```

**Thorough — add:**
```
scan(tool="nmap", target=HOST, options={"ports": "443", "flags": "--script ssl-enum-ciphers,ssl-cert,ssl-heartbleed,ssl-poodle,ssl-dh-params,ssl-known-key -sV"})
kali(command="sslyze --regular TARGET:443")
```

After each tool: `report(action="note", data={...})` summary + `report(action="finding", data={...})` for confirmed vulns.

### Phase 2 — Protocol Version Analysis

| Protocol | Status | Finding |
|----------|--------|---------|
| SSLv2 | Must be disabled | **Critical** if enabled |
| SSLv3 | Must be disabled | **High** — POODLE (CVE-2014-3566) |
| TLS 1.0 | Should be disabled | **Medium** — PCI DSS non-compliant since 2018 |
| TLS 1.1 | Should be disabled | **Medium** — deprecated by RFC 8996 |
| TLS 1.2 | Should be enabled | OK if strong ciphers only |
| TLS 1.3 | Should be enabled | Best practice — verify no 0-RTT issues |

**Manual protocol probing** (thorough):
```
kali(command="for v in ssl2 ssl3 tls1 tls1_1 tls1_2 tls1_3; do echo \"=== $v ===\"; echo | openssl s_client -connect TARGET:443 -$v 2>&1 | head -3; done")
```

### Phase 3 — Cipher Suite & Ordering Analysis

| Cipher Category | Severity | Reason |
|----------------|----------|--------|
| NULL ciphers | **Critical** | No encryption |
| EXPORT ciphers | **Critical** | FREAK, Logjam |
| DES / RC4 | **High** | Broken cryptography |
| 3DES (SWEET32) | **Medium** | CVE-2016-2183, 64-bit block |
| CBC mode (TLS 1.0) | **Medium** | BEAST vulnerability |
| Static RSA key exchange | **Low** | No forward secrecy |
| DHE < 2048-bit | **Medium** | Logjam (CVE-2015-4000) |

**Cipher order preference testing** — determine if server enforces its own preference:
```
kali(command="echo | openssl s_client -connect TARGET:443 -cipher 'AES128-SHA:AES256-SHA' 2>/dev/null | grep 'Cipher is'")
kali(command="echo | openssl s_client -connect TARGET:443 -cipher 'AES256-SHA:AES128-SHA' 2>/dev/null | grep 'Cipher is'")
```
If both return the same cipher, server enforces preference (good). If different: **Low** — server defers to client.

**Ordering recommendations:** TLS 1.2 — server MUST enforce order: ECDHE+AESGCM > ECDHE+CHACHA20 > DHE+AESGCM, no CBC. TLS 1.3 — all suites are strong; prefer AES-256-GCM for high-security.

### Phase 4 — Certificate Chain Deep Validation

```
kali(command="echo | openssl s_client -connect TARGET:443 -servername TARGET 2>/dev/null | openssl x509 -noout -text")
kali(command="echo | openssl s_client -connect TARGET:443 -servername TARGET -showcerts 2>/dev/null")
```

| Issue | Severity | Check |
|-------|----------|-------|
| Expired certificate | **Critical** | `-noout -dates` |
| Self-signed certificate | **High** | Chain validation failure |
| Weak key (RSA < 2048) | **High** | `grep "Public-Key"` |
| SHA-1 signature | **High** | Deprecated, collision attacks |
| SAN mismatch | **High** | Certificate doesn't match domain |
| Incomplete chain | **Medium** | Missing intermediate certificates |
| Wildcard certificate | **Low** | Blast radius if compromised |

**Intermediate pinning & cross-signed cert detection:**
```
kali(command="echo | openssl s_client -connect TARGET:443 -servername TARGET -showcerts 2>/dev/null | grep -E 's:|i:' | head -20")
```
Look for: root CA in chain (unnecessary), cross-signed intermediates (affects pinning decisions), missing intermediates (**Medium**).

**Certificate Transparency log verification:**
```
kali(command="curl -s 'https://crt.sh/?q=TARGET&output=json' | python3 -m json.tool | head -50")
kali(command="echo | openssl s_client -connect TARGET:443 -servername TARGET -ct 2>&1 | grep -A5 'SCT'")
```
SCT delivery: embedded in cert (preferred), TLS extension, or OCSP staple. Missing CT logs: **Low**.

**OCSP stapling verification:**
```
kali(command="echo | openssl s_client -connect TARGET:443 -servername TARGET -status 2>/dev/null | grep -A15 'OCSP Response'")
```
`no response sent` = stapling not enabled (**Low**). Check `This Update`/`Next Update` for freshness.

**Certificate pinning bypass:** Check for deprecated HPKP headers (`Public-Key-Pins`). If present: **Informational** — recommend removal in favor of CAA records and CT.

### Phase 5 — ECDHE Curve Analysis

```
kali(command="for c in P-256 P-384 P-521 X25519; do echo \"=== $c ===\"; echo | openssl s_client -connect TARGET:443 -servername TARGET -curves $c 2>/dev/null | grep 'Server Temp Key'; done")
```

| Curve | Security | Notes |
|-------|----------|-------|
| X25519 | 128-bit | Preferred for TLS 1.3 — fast, constant-time |
| P-256 (secp256r1) | 128-bit | NIST standard, widely supported |
| P-384 (secp384r1) | 192-bit | Required for FedRAMP |
| P-521 (secp521r1) | 256-bit | Overkill, slower, wider attack surface |
| brainpoolP256r1/384r1/512r1 | varies | **Medium** — non-standard, implementation risk |

**Curve preference detection:**
```
kali(command="echo | openssl s_client -connect TARGET:443 -curves 'P-256:P-384' 2>/dev/null | grep 'Server Temp Key'")
kali(command="echo | openssl s_client -connect TARGET:443 -curves 'P-384:P-256' 2>/dev/null | grep 'Server Temp Key'")
```
Same curve both times = server enforces preference (good). Brainpool accepted: **Medium**. No X25519 for TLS 1.3: **Low**. No server-side curve preference: **Low**.

### Phase 6 — TLS 1.3 Specific Testing

**0-RTT replay attack testing:**
```
kali(command="echo -e 'GET / HTTP/1.1\r\nHost: TARGET\r\n\r\n' > /tmp/earlydata.txt")
kali(command="echo | openssl s_client -connect TARGET:443 -tls1_3 -sess_out /tmp/sess.pem 2>/dev/null | grep -E 'Early data|Max Early'")
kali(command="echo | openssl s_client -connect TARGET:443 -tls1_3 -sess_in /tmp/sess.pem -early_data /tmp/earlydata.txt 2>/dev/null | grep -E 'Early data'")
```
0-RTT accepted: **Medium** — early data is replayable. Non-idempotent requests can be replayed by attackers.

**PSK mode validation:**
```
kali(command="echo | openssl s_client -connect TARGET:443 -tls1_3 2>/dev/null | grep -E 'psk|PSK|Reused|session'")
```
PSK without (EC)DHE loses forward secrecy: **Medium** if accepted.

**Downgrade detection (GREASE + TLS_FALLBACK_SCSV):**
```
kali(command="testssl --quiet --color 0 -p TARGET:443 2>&1 | grep -i -E 'downgrad|fallback|grease'")
kali(command="echo | openssl s_client -connect TARGET:443 -fallback_scsv -no_tls1_3 2>&1 | grep -i 'alert'")
```
Missing `inappropriate_fallback` alert: **Medium** — enables downgrade attacks.

**TLS 1.3 cipher suite validation:**
```
kali(command="echo | openssl s_client -connect TARGET:443 -tls1_3 -ciphersuites 'TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256' 2>/dev/null | grep 'Cipher is'")
```
TLS_AES_128_CCM_8_SHA256 present: **Low** — truncated auth tag, only for constrained IoT.

### Phase 7 — Session Management Testing

**Ticket reuse:**
```
kali(command="echo | openssl s_client -connect TARGET:443 -tls1_2 -sess_out /tmp/sess12.pem 2>/dev/null | grep -E 'Session-ID|TLS session ticket'")
kali(command="echo | openssl s_client -connect TARGET:443 -tls1_2 -sess_in /tmp/sess12.pem 2>/dev/null | grep -i 'reused'")
```

**Session ID fixation:**
```
kali(command="for i in 1 2 3; do echo | openssl s_client -connect TARGET:443 2>/dev/null | grep 'Session-ID:'; done")
```
Same Session-ID across fresh connections: **Medium** — possible fixation.

**Ticket lifetime:**
```
kali(command="testssl --quiet --color 0 -S TARGET:443 2>&1 | grep -i -E 'ticket|lifetime|session'")
```
NIST: ticket lifetime should not exceed 24h. Over 48h: **Low**.

### Phase 8 — Renegotiation Attack Testing

**Client-initiated renegotiation DoS:**
```
kali(command="echo 'R' | openssl s_client -connect TARGET:443 2>&1 | grep -i -E 'renegotiat|error|DONE'")
```
Allowed: **Medium** — each renegotiation costs ~10x more server CPU than client CPU.

**Secure renegotiation extension (RFC 5746):**
```
kali(command="echo | openssl s_client -connect TARGET:443 2>/dev/null | grep -i 'secure renegotiation'")
```
`IS NOT supported`: **High** — vulnerable to CVE-2009-3555 (prefix injection).

**Extended test:** `kali(command="testssl --quiet --color 0 -R TARGET:443")`

### Phase 9 — Known Vulnerability Testing

| Vulnerability | CVE | Manual Test |
|--------------|-----|-------------|
| **Heartbleed** | CVE-2014-0160 | `nmap --script ssl-heartbleed -p 443 TARGET` |
| **POODLE** | CVE-2014-3566 | SSLv3 + CBC ciphers |
| **BEAST** | CVE-2011-3389 | TLS 1.0 + CBC ciphers |
| **CRIME** | CVE-2012-4929 | TLS compression enabled |
| **BREACH** | CVE-2013-3587 | HTTP compression on sensitive pages |
| **ROBOT** | CVE-2017-13099 | RSA key exchange vulnerability |
| **DROWN** | CVE-2016-0800 | SSLv2 on any server sharing the key |
| **Lucky13** | CVE-2013-0169 | CBC without constant-time impl |
| **Ticketbleed** | CVE-2016-9244 | F5 session ticket flaw |
| **GOLDENDOODLE** | -- | Padding oracle in CBC |

### Phase 10 — HSTS Analysis Deep-Dive

```
kali(command="curl -sI https://TARGET 2>/dev/null | grep -i 'strict-transport-security'")
```

| Directive | Expected | Finding if wrong |
|-----------|----------|-----------------|
| `max-age` | >= 31536000 (1 year) | **Medium** if < 31536000; **High** if < 86400 |
| `includeSubDomains` | Present | **Medium** if absent — subdomain MitM risk |
| `preload` | Present if in preload list | **Low** if absent |

**Preload list membership:**
```
kali(command="curl -s 'https://hstspreload.org/api/v2/status?domain=TARGET' | python3 -m json.tool")
```
`preload` directive set but not in list: **Low** — aspirational without submission.

**HSTS bypass via subdomain** (when `includeSubDomains` missing):
```
kali(command="for sub in www mail api; do echo \"=== $sub ===\"; curl -sI http://$sub.TARGET 2>/dev/null | head -3; done")
```
Subdomains responding over HTTP: **Medium** combined with missing `includeSubDomains`.

**HTTP-to-HTTPS redirect:** `kali(command="curl -sI http://TARGET 2>/dev/null | head -10")`
200 on HTTP: **Medium**. No redirect and no HSTS: **High**.

### Phase 11 — Certificate Revocation Checking

**CRL distribution point validation:**
```
kali(command="echo | openssl s_client -connect TARGET:443 2>/dev/null | openssl x509 -noout -text | grep -A3 'CRL Distribution'")
kali(command="curl -sI CRL_URL | head -5")
```
CRL unreachable: **Low**. CRL validity > 7 days (check `nextUpdate`): **Low** — revoked certs accepted too long.

**OCSP responder testing:**
```
kali(command="OCSP_URI=$(echo | openssl s_client -connect TARGET:443 2>/dev/null | openssl x509 -noout -ocsp_uri) && echo $OCSP_URI")
kali(command="openssl ocsp -issuer /tmp/chain.pem -cert /tmp/target_cert.pem -url $OCSP_URI -text 2>&1 | head -30")
```
`Cert Status: revoked`: **Critical**. Responder unreachable: **Low**.

**Stapled response freshness:**
```
kali(command="echo | openssl s_client -connect TARGET:443 -status 2>/dev/null | grep -A10 'OCSP Response Data'")
```
Response > 7 days old: **Low**. Expired (`Next Update` passed): **Medium**.

### Phase 12 — Multi-Port TLS Scanning

**STARTTLS ports:** 25 (SMTP `--starttls smtp`), 110 (POP3 `--starttls pop3`), 143 (IMAP `--starttls imap`), 389 (LDAP `--starttls ldap`), 587 (Submission `--starttls smtp`), 1433 (MSSQL `--starttls mssql`), 3306 (MySQL `--starttls mysql`), 5432 (PostgreSQL `--starttls postgres`)

**Direct TLS ports:** 443, 465 (SMTPS), 636 (LDAPS), 993 (IMAPS), 995 (POP3S), 3389 (RDP), 5900 (VNC), 5985 (WinRM), 8443, 8883 (MQTT), 9200 (Elasticsearch), 9443

**Batch discovery:**
```
scan(tool="nmap", target=HOST, options={"ports": "25,110,143,389,443,465,587,636,993,995,1433,3306,3389,5432,5900,5985,8443,8883,9200,9443", "flags": "-sV --script ssl-enum-ciphers"})
```

Per TLS port: `kali(command="testssl --quiet --color 0 TARGET:PORT")`
Per STARTTLS port: `kali(command="testssl --quiet --color 0 --starttls smtp TARGET:25")`

### Phase 13 — Extended Compliance Mapping (thorough)

#### PCI DSS 4.0 — Section 4

| Req | Control | Verify |
|-----|---------|--------|
| 4.1 | Processes for protecting cardholder data with strong crypto are defined | Policy review |
| 4.1.1 | Security policies for Req 4 documented, current, communicated | Policy review |
| 4.1.2 | Roles/responsibilities for Req 4 documented and assigned | Policy review |
| 4.2.1 | Strong cryptography protects PAN over public networks | TLS 1.2+, strong ciphers, valid certs |
| 4.2.1.1 | Inventory of trusted keys and certificates maintained | Certificate chain review |
| 4.2.1.2 | Trusted keys/certs accepted; valid, not expired, not revoked | Cert validity + CRL/OCSP checks |
| 4.2.2 | PAN secured via end-user messaging technologies | N/A for TLS audit |

#### NIST SP 800-52r2

| Section | Guideline | Verify |
|---------|-----------|--------|
| 3.1 | Protocol Version | TLS 1.2 min; TLS 1.3 recommended; SSLv2/3, TLS 1.0/1.1 prohibited |
| 3.2 | Server Certificate | RSA 2048+ or ECDSA P-256+; SHA-256+; valid, not expired |
| 3.3 | Cipher Suites | AEAD required (GCM, CCM, CHACHA20); no CBC for TLS 1.2; ECDHE/DHE only |
| 3.3.1 | Key Exchange | ECDHE P-256/P-384/X25519; DHE 2048+; no static RSA |
| 3.4 | TLS Extensions | SNI required; ALPN recommended; secure renegotiation |
| 3.5 | Certificate Validation | Full chain; revocation (OCSP preferred); CT logs |
| 3.6 | Session Resumption | Short ticket lifetimes; key rotation; no fixation |
| 3.6.1 | Renegotiation | RFC 5746 required; client-initiated should be disabled |

#### FedRAMP

| Control | Requirement | Verify |
|---------|-------------|--------|
| SC-8 | Transmission Confidentiality/Integrity | FIPS 140-2/3 modules; TLS 1.2+ |
| SC-8(1) | Cryptographic Protection | FIPS-approved only (AES, SHA-2, ECDSA P-256/P-384) |
| SC-13 | Cryptographic Protection | NIST key establishment (ECDHE with NIST curves, NOT X25519) |
| SC-17 | PKI Certificates | Approved CAs; valid chain; revocation checking |
| SC-23 | Session Authenticity | TLS session integrity; secure renegotiation |

Note: X25519 and CHACHA20 are NOT FIPS-approved. Flag as **Informational** in FedRAMP audits.

### Phase 14 — Report & Wrap-Up

1. Call `report(action="diagram", data={...})` with TLS configuration summary:
```mermaid
flowchart TD
    Client["Client"] --> TLS["TLS Handshake"]
    TLS --> Proto["Protocols: TLS 1.2, TLS 1.3"]
    TLS --> Cipher["Ciphers: ECDHE-RSA-AES256-GCM"]
    TLS --> Cert["Cert: RSA 2048, SHA256"]
    Cert --> Chain["Chain: Root > Intermediate > Leaf"]
    Cert --> CT["CT: Logged, SCT embedded"]
    Cert --> Revoke["Revocation: OCSP stapled"]
    TLS --> Session["Session: Tickets rotated, no 0-RTT"]
    TLS --> Vulns["Known Vulns: None"]
```
2. Call `report(action="note", data={...})` with compliance summary (PCI DSS 4.0 + NIST 800-52r2 + FedRAMP)
3. Call `session(action="complete", options={...})` with summary

---

## Chaining Other Skills

| Skill | When to invoke |
|-------|----------------|
| `/pentester` | TLS weaknesses enable further attacks (MitM, credential interception) |
| `/threat-modeling` | Architecture-level risk analysis beyond TLS |
| `/network-assess` | Internal network found — test segmentation, SNMP, broadcast protocols |
| `/credential-audit` | Weak TLS enables credential interception — test authentication strength |
| `/post-exploit` | Weak TLS enables MitM credential capture — post-exploitation with harvested credentials |
| `/gh-export` | When user asks to file GitHub issues|

---

## Finding Severity Guide

| Severity | Criteria | Examples |
|----------|----------|---------|
| **Critical** | Exploitable vuln allowing traffic interception/decryption | SSLv2 (DROWN), Heartbleed, expired/revoked cert |
| **High** | Significant crypto weakness or missing security control | SSLv3 (POODLE), SHA-1 sigs, no secure renegotiation, self-signed cert |
| **Medium** | Deprecated protocol or weakening configuration | TLS 1.0/1.1, 3DES, DHE < 2048, client renego, 0-RTT, stale OCSP, weak HSTS |
| **Low** | Suboptimal config, best practice deviation | Static RSA, missing preload, no X25519, wildcard cert, no cipher order enforcement |

---

## Context Recovery After Compaction

When your context is compacted mid-skill:

1. **Call `session(action="recovery")`** before doing anything else — returns `tools_already_run`, `in_progress_cells`, and `EXECUTE_NOW`
2. **Check `tools_already_run`** — skip ports and services whose testssl/sslyze output was already recorded
3. **Resume incomplete port coverage** — TLS audits span many ports; the coverage matrix tracks which port/service cells are pending
4. **Follow `pending_escalations`** — e.g., "confirm ROBOT exploit via Marvin attack PoC" leads from initial weak-cipher findings
5. **Never fabricate compliance mappings from memory** — re-check tool output before asserting PCI/NIST pass/fail status

---

## Rules

- **`session(action="start", options={...})` is mandatory** — never run any other tool before it
- **Batch independent tools in the same response** — they execute in parallel
- When any tool returns a LIMIT message, stop immediately and call `session(action="complete", options={...})`
- **Call `report(action="finding", data={...})` for every confirmed TLS weakness** — include protocol/cipher/vuln and compliance impact
- **Always run testssl first** — most comprehensive single-tool output
- **Map findings to compliance** — PCI DSS 4.0 + NIST 800-52r2; include FedRAMP if in scope
- **Full certificate chain validation** — validity, chain, SAN, key size, sig algo, CT logs, OCSP, CRL
- **Test all TLS ports** — not just 443; scan the full 20-port list at thorough depth
- **TLS 1.3 specific tests** — 0-RTT, PSK modes, downgrade protection are distinct from TLS 1.2
- **Session management** — ticket reuse, resumption, lifetime are often overlooked
- **Renegotiation** — test both secure renegotiation support and client-initiated DoS
- **Use `report(action="note", data={...})` liberally** — document findings and compliance decisions
- **Never fabricate findings** — only report what tool output confirms
- **Mermaid syntax**: `flowchart TD`, quote labels, no em-dashes, short node IDs
- Call `session(action="stop_kali")` at the end if `kali(command=...)` was used
