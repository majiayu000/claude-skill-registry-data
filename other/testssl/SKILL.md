---
type: skill
name: testssl
description: TLS/SSL testing with testssl.sh for certificate validation, protocol checks, cipher analysis, and vulnerability detection.
used_by: [ad-hoc]
last_updated: "2026-03-17"
doc_source: https://testssl.sh/
---

# testssl.sh

testssl.sh is a free command-line tool that checks TLS/SSL encryption on any port of any server. It tests protocols, ciphers, vulnerabilities, and certificate details without requiring installation of additional libraries.

---

## Table of Contents

- [Installation](#installation)
- [Core Concepts](#core-concepts)
- [Basic Usage](#basic-usage)
- [Protocol Checks](#protocol-checks)
- [Cipher Checks](#cipher-checks)
- [Vulnerability Checks](#vulnerability-checks)
- [Certificate Checks](#certificate-checks)
- [Output Formats](#output-formats)
- [AWS Integration](#aws-integration)
- [Common AWS Validation Scans](#common-aws-validation-scans)
- [Interpreting Results](#interpreting-results)
- [Troubleshooting](#troubleshooting)
- [References](#references)

---

## Installation

```bash
brew install testssl
```

**Command:** `testssl.sh` — always use this exact name. Do NOT use `./testssl.sh`.

To verify: `which testssl.sh` → `/opt/homebrew/bin/testssl.sh`

---

## Core Concepts

| Concept | Description |
|:--------|:------------|
| **Protocol** | TLS version (SSLv2, SSLv3, TLS 1.0, 1.1, 1.2, 1.3) |
| **Cipher Suite** | Encryption algorithm combination (key exchange + bulk cipher + MAC) |
| **Certificate Chain** | Server cert → intermediate CA(s) → root CA |
| **HSTS** | HTTP Strict Transport Security — forces HTTPS |
| **OCSP Stapling** | Server-side certificate revocation check |
| **Forward Secrecy** | Past sessions can't be decrypted if long-term key is compromised |
| **Vulnerability** | Known TLS/SSL attacks (Heartbleed, POODLE, BEAST, etc.) |

### Severity Mapping

testssl.sh uses its own severity labels. Map to plugin severities:

| testssl.sh | Plugin Severity | Meaning |
|:-----------|:----------------|:--------|
| CRITICAL | CRITICAL | Actively exploitable (e.g., Heartbleed on unpatched server) |
| HIGH | HIGH | Weak protocol/cipher in use (e.g., SSLv3, RC4) |
| MEDIUM | MEDIUM | Suboptimal configuration (e.g., no HSTS, weak DH params) |
| LOW | LOW | Minor issues (e.g., no OCSP stapling) |
| INFO | INFORMATIONAL | Not a vulnerability (e.g., supported cipher list) |
| OK | — | Check passed, no issue |

---

## Basic Usage

### Full scan (all checks)

```bash
testssl.sh <hostname>
```

### Scan specific port

```bash
testssl.sh <hostname>:8443
```

### Protocol-only scan (quick)

```bash
testssl.sh -p <hostname>
```

### SNI (Server Name Indication) — required for shared hosting / CloudFront

```bash
testssl.sh --sni <hostname> <ip_or_cname>
```

---

## Protocol Checks

### Test all protocols

```bash
testssl.sh -p <hostname>
```

Tests: SSLv2, SSLv3, TLS 1.0, TLS 1.1, TLS 1.2, TLS 1.3

### Expected secure state

| Protocol | Expected | Finding if enabled |
|:---------|:---------|:-------------------|
| SSLv2 | NOT offered | CRITICAL if offered |
| SSLv3 | NOT offered | HIGH if offered (POODLE) |
| TLS 1.0 | NOT offered | HIGH — deprecated since 2020 |
| TLS 1.1 | NOT offered | HIGH — deprecated since 2020 |
| TLS 1.2 | Offered | OK |
| TLS 1.3 | Offered | OK (best) |

---

## Cipher Checks

### Test all ciphers

```bash
testssl.sh -E <hostname>
```

### Test specific cipher categories

```bash
testssl.sh -e <hostname>        # Per-protocol cipher listing
testssl.sh --cipher-per-proto <hostname>  # Same as -e
```

### Key cipher concerns

| Issue | Severity | Examples |
|:------|:---------|:---------|
| NULL ciphers | CRITICAL | No encryption at all |
| EXPORT ciphers | CRITICAL | Weak keys (40/56-bit) — FREAK attack |
| RC4 ciphers | HIGH | Known biases — prohibited by RFC 7465 |
| DES/3DES ciphers | HIGH | SWEET32 attack — 64-bit block size |
| No forward secrecy | MEDIUM | ECDHE/DHE not offered |
| Weak DH params | MEDIUM | DH < 2048 bits — Logjam attack |

---

## Vulnerability Checks

### Test all known vulnerabilities

```bash
testssl.sh -U <hostname>
```

### Individual vulnerability tests

```bash
testssl.sh --heartbleed <hostname>    # CVE-2014-0160
testssl.sh --poodle <hostname>        # CVE-2014-3566
testssl.sh --beast <hostname>         # CVE-2011-3389
testssl.sh --freak <hostname>         # CVE-2015-0204
testssl.sh --logjam <hostname>        # CVE-2015-4000
testssl.sh --drown <hostname>         # CVE-2016-0800
testssl.sh --robot <hostname>         # Return Of Bleichenbacher's Oracle Threat
testssl.sh --ticketbleed <hostname>   # CVE-2016-9244
testssl.sh --lucky13 <hostname>       # CVE-2013-0169
testssl.sh --winshock <hostname>      # CVE-2014-6321
```

### Vulnerability quick reference

| Vulnerability | CVE | Severity | What it exploits |
|:-------------|:----|:---------|:----------------|
| Heartbleed | CVE-2014-0160 | CRITICAL | OpenSSL memory leak — reads server memory |
| POODLE | CVE-2014-3566 | HIGH | SSLv3 CBC padding oracle |
| BEAST | CVE-2011-3389 | MEDIUM | TLS 1.0 CBC IV prediction |
| FREAK | CVE-2015-0204 | HIGH | RSA export cipher downgrade |
| Logjam | CVE-2015-4000 | HIGH | DH export downgrade (< 1024-bit) |
| DROWN | CVE-2016-0800 | HIGH | SSLv2 cross-protocol attack on TLS |
| ROBOT | — | HIGH | Bleichenbacher RSA padding oracle |
| SWEET32 | CVE-2016-2183 | MEDIUM | 64-bit block cipher birthday attack (3DES) |
| CCS Injection | CVE-2014-0224 | HIGH | OpenSSL ChangeCipherSpec injection |

---

## Certificate Checks

### Test certificate only

```bash
testssl.sh -S <hostname>
```

### What to check

| Check | Issue if failed | Severity |
|:------|:---------------|:---------|
| Expiry | Certificate expired or < 30 days remaining | HIGH (expired) / MEDIUM (expiring) |
| Chain completeness | Missing intermediate CA | MEDIUM |
| Self-signed | Not trusted by clients | HIGH |
| CN/SAN mismatch | Certificate doesn't match hostname | HIGH |
| Key size | RSA < 2048 bits or EC < 256 bits | HIGH |
| Signature algorithm | SHA-1 signed | HIGH |
| Revocation | OCSP revoked | CRITICAL |
| Wildcard scope | Overly broad wildcard (e.g., `*.com`) | MEDIUM |
| CT (Certificate Transparency) | Not logged in CT logs | LOW |

---

## Output Formats

### JSON output (best for automation)

```bash
testssl.sh --jsonfile results.json <hostname>
```

### JSON pretty-printed

```bash
testssl.sh --jsonfile-pretty results.json <hostname>
```

### CSV output

```bash
testssl.sh --csvfile results.csv <hostname>
```

### HTML output

```bash
testssl.sh --htmlfile results.html <hostname>
```

### Log file

```bash
testssl.sh --logfile results.log <hostname>
```

### Combine formats

```bash
testssl.sh --jsonfile-pretty results.json --htmlfile results.html <hostname>
```

---

## AWS Integration

### Feedback Loop Integration

testssl.sh is used for **External Probe** path checks — testing actual TLS/SSL configuration from outside the AWS account. Like nmap, testssl.sh results bypass the pipeline and return directly. While AWS CLI checks verify *configuration* (e.g., security policy on an ALB listener), testssl.sh verifies *actual TLS behavior* as seen by clients.

### Endpoint Discovery

Before running testssl, discover the endpoint using AWS CLI:

| Service | Discovery Command | Endpoint |
|:--------|:------------------|:---------|
| ALB/NLB | `aws elbv2 describe-load-balancers --query 'LoadBalancers[].DNSName'` | DNS name |
| CLB | `aws elb describe-load-balancers --query 'LoadBalancerDescriptions[].DNSName'` | DNS name |
| CloudFront | `aws cloudfront list-distributions --query 'DistributionList.Items[].DomainName'` | Domain name |
| API Gateway | `aws apigateway get-rest-apis --query 'items[].{id:id,name:name}'` → `{id}.execute-api.{region}.amazonaws.com` | Constructed URL |
| EC2 (direct HTTPS) | `aws ec2 describe-instances --query 'Reservations[].Instances[].PublicIpAddress'` | Public IP |
| RDS (TLS) | `aws rds describe-db-instances --query 'DBInstances[].Endpoint.Address'` | Endpoint address |
| OpenSearch | `aws opensearch describe-domains --query 'DomainStatusList[].Endpoints'` | HTTPS endpoint |
| Elasticache (Redis 6+) | `aws elasticache describe-replication-groups --query 'ReplicationGroups[].NodeGroups[].PrimaryEndpoint'` | Endpoint |

### AWS-Managed TLS Policies

AWS services use predefined security policies. testssl.shvalidates what's *actually negotiated*, which may differ from the configured policy:

| Service | Policy Setting | CLI to Check Config |
|:--------|:--------------|:-------------------|
| ALB | `aws elbv2 describe-listeners --query 'Listeners[].SslPolicy'` | Security policy name |
| CLB | `aws elb describe-load-balancers --query 'LoadBalancerDescriptions[].ListenerDescriptions[].Listener.Protocol'` | Protocol |
| CloudFront | `aws cloudfront get-distribution --query 'Distribution.DistributionConfig.ViewerCertificate.MinimumProtocolVersion'` | Min TLS version |
| API Gateway | `aws apigateway get-domain-names --query 'items[].securityPolicy'` | TLS_1_0 or TLS_1_2 |

**Key insight:** AWS manages the TLS termination for ALB, CloudFront, and API Gateway. You can't install custom ciphers — you pick a security policy. testssl.shvalidates that the policy delivers what you expect.

---

## Common AWS Validation Scans

### ALB/NLB — Full TLS audit

```bash
# Discover ALB endpoint
aws elbv2 describe-load-balancers --query 'LoadBalancers[].{Name:LoadBalancerName,DNS:DNSName,Type:Type}' --output table

# Full testssl.shscan
testssl.sh --jsonfile-pretty alb-results.json <alb-dns-name>
```

### CloudFront — Verify minimum TLS version

```bash
# Discover distributions
aws cloudfront list-distributions --query 'DistributionList.Items[].{Id:Id,Domain:DomainName,MinTLS:ViewerCertificate.MinimumProtocolVersion}' --output table

# Test actual TLS — must use SNI for CloudFront
testssl.sh --sni <custom-domain-or-cloudfront-domain> <cloudfront-domain>
```

### API Gateway — Custom domain TLS check

```bash
# Discover custom domains
aws apigateway get-domain-names --query 'items[].{Domain:domainName,Policy:securityPolicy}' --output table

# Test TLS on custom domain
testssl.sh <custom-domain>

# Test TLS on default endpoint
testssl.sh <api-id>.execute-api.<region>.amazonaws.com
```

### EC2 — Direct HTTPS service

```bash
# Test HTTPS on a specific port
testssl.sh <public-ip>:443
testssl.sh <public-ip>:8443
```

### RDS — TLS connection verification

RDS uses STARTTLS (not pure TLS), so the `--starttls` flag is required:

```bash
testssl.sh --starttls mysql <rds-endpoint>:3306    # MySQL/Aurora MySQL
testssl.sh --starttls postgres <rds-endpoint>:5432  # PostgreSQL/Aurora PostgreSQL
```

Without `--starttls`, testssl.shwill attempt a pure TLS handshake on the database port, which will fail or produce misleading results.

### OpenSearch — HTTPS enforcement

```bash
testssl.sh <opensearch-endpoint>:443
```

---

## Interpreting Results

### What to report as findings

The canonical check definitions (confirmed/false_positive conditions and severities) are in `skills/validation-rules/probes.md` → TLS/SSL (testssl.sh). The table below is a quick reference only.

| testssl.sh Result | Plugin Action | Severity |
|:--------------|:-------------|:---------|
| SSLv2/SSLv3 offered | CONFIRMED | CRITICAL/HIGH |
| TLS 1.0/1.1 offered | CONFIRMED | HIGH |
| Only TLS 1.2+ offered | No finding | — |
| Heartbleed vulnerable | CONFIRMED | CRITICAL |
| POODLE vulnerable | CONFIRMED | HIGH |
| Certificate expired | CONFIRMED | HIGH |
| Certificate expiring < 30 days | CONFIRMED | MEDIUM |
| Self-signed certificate | CONFIRMED (unless internal) | HIGH |
| Weak key (RSA < 2048) | CONFIRMED | HIGH |
| No forward secrecy | CONFIRMED | MEDIUM |
| No HSTS | CONFIRMED | MEDIUM |
| Missing OCSP stapling | CONFIRMED | LOW |
| All checks pass | FALSE_POSITIVE | — |

### Config vs Runtime discrepancies

When testssl.shresults differ from AWS CLI configuration:

| Scenario | Meaning |
|:---------|:--------|
| Config says TLS 1.2 only, testssl.shshows TLS 1.0 | Misconfigured policy or wrong listener — **testssl.shis ground truth** |
| Config says old policy, testssl.shshows TLS 1.2+ only | AWS may have deprecated old ciphers — testssl.shconfirms actual state |
| testssl.shtimes out | Endpoint may not serve TLS, or firewall blocks — flag as ERROR |

**Rule:** When config and runtime disagree, **runtime (testssl) wins**. The actual TLS handshake is what clients experience.

---

## Troubleshooting

### Connection timeout

```bash
# Check if port is open first
nmap -Pn -p 443 <hostname>

# If filtered, testssl.shcan't help — network issue
```

### SNI required (CloudFront, shared ALBs)

```bash
# Use --sni flag
testssl.sh --sni <expected-hostname> <ip-or-cname>
```

### STARTTLS protocols

Supported `--starttls` protocol identifiers:

| Protocol | Port | Example |
|:---------|:-----|:--------|
| `smtp` | 25/587 | `testssl.sh --starttls smtp <mailserver>:25` |
| `ftp` | 21 | `testssl.sh --starttls ftp <ftpserver>:21` |
| `mysql` | 3306 | `testssl.sh --starttls mysql <rds-endpoint>:3306` |
| `postgres` | 5432 | `testssl.sh --starttls postgres <rds-endpoint>:5432` |
| `imap` | 143 | `testssl.sh --starttls imap <mailserver>:143` |
| `pop3` | 110 | `testssl.sh --starttls pop3 <mailserver>:110` |
| `xmpp` | 5222 | `testssl.sh --starttls xmpp <server>:5222` |
| `ldap` | 389 | `testssl.sh --starttls ldap <server>:389` |

### Scan too slow

```bash
# Protocol-only scan (fastest single-host check)
testssl.sh -p <hostname>

# Parallel testing for multiple hosts (requires file input)
testssl.sh --mode parallel --file hosts.txt
```

### OpenSSL version issues

```bash
# Use a specific OpenSSL binary:
testssl.sh --openssl /path/to/openssl <hostname>

# Use the system default (testssl.sh auto-detects):
testssl.sh <hostname>
```

---

## References

- https://testssl.sh/
- https://github.com/drwetter/testssl.sh
- https://testssl.sh/doc/testssl.1.html
- https://docs.aws.amazon.com/elasticloadbalancing/latest/application/create-https-listener.html#describe-ssl-policies
- https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/secure-connections-supported-viewer-protocols-ciphers.html

