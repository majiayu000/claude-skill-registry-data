---
name: tls-pro
description: Deploy and harden TLS — certificate lifecycle, modern cipher configuration, HSTS, and certificate-transparency monitoring.
category: security
---

## Overview

TLS is the encryption backbone of the internet, but "we have HTTPS" is not a security statement — weak protocols, expired certificates, and missing HSTS are evergreen findings. Professional TLS practice covers the full lifecycle: provisioning, configuration hardening, renewal automation, and monitoring.

This skill gives you the defensive playbook: what "good TLS" looks like in 2026, how to automate it, and how to catch the failures before your users (or auditors) do.

TLS is infrastructure: invisible when it works, catastrophic when it fails at 2 AM on a holiday. Professional TLS practice treats certificates like production dependencies — inventoried, monitored, and automated — because every expired certificate in history was 'someone's job to remember' right up until it was not.

## When to use

- Configuring or reviewing TLS on web servers, APIs, load balancers, and mail.
- Setting up certificate issuance and automated renewal (ACME/Let's Encrypt or internal PKI).
- Remediating scanner findings: weak ciphers, old protocols, missing HSTS, expired certs.
- Monitoring certificate transparency logs for rogue certificates.

## Core concepts

- **Modern baseline:** TLS 1.2+ only (1.3 preferred); disable SSL 2/3, TLS 1.0/1.1. Strong cipher suites with forward secrecy (ECDHE); disable NULL, RC4, 3DES, and export ciphers.
- **Forward secrecy:** with ECDHE/DHE suites, a future key compromise does not decrypt past traffic. Non-negotiable for sensitive services.
- **Certificate lifecycle:** issuance → deployment → monitoring → automated renewal → revocation. Manual renewal is an outage waiting to happen — automate with ACME.
- **HSTS:** `Strict-Transport-Security` with long max-age, includeSubDomains, and preload submission — eliminates SSL-stripping downgrade attacks. Deploy carefully: it is hard to undo.
- **Certificate Transparency (CT):** all public certs are logged; monitor CT logs for certificates issued for your domains that you did not request — early warning of mis-issuance or attack prep.
- **Internal PKI:** for service-to-service mTLS, run an internal CA with short-lived certificates and automated issuance rather than stretching public certs into internal roles.

- **Cipher suite ordering.** Server-side preference for strong, forward-secret suites ensures negotiated connections use the best mutually supported option, not the client's weakest.
- **OCSP and revocation.** Plan for revocation checking (OCSP stapling preferred) — a compromised certificate you cannot revoke is a lingering exposure.
- **TLS for service-to-service.** mTLS between services gives you authentication plus encryption; short-lived, auto-rotated service certificates beat long-lived shared ones.

## Practical workflow

1. **Inventory:** list every TLS endpoint (public and internal): web, API, mail, VPN, admin consoles. Note certificate source, expiry, and protocol/cipher support.
2. **Harden configuration:** apply a modern profile (TLS 1.2+ / 1.3, strong ciphers, forward secrecy); verify with a scanner (test for protocol/cipher support, not just "HTTPS responds").
3. **Automate issuance and renewal:** ACME for public certs with renewal at <30 days and alerting at 21/14/7 days; internal CA with automated short-lived certs for services.
4. **Deploy HSTS:** start with short max-age, verify no HTTP-only dependencies break, then extend and add includeSubDomains; consider preload for top domains.
5. **Monitor continuously:** expiry alerting, CT-log monitoring for unauthorized issuance, and configuration-drift checks (a deploy that re-enables TLS 1.0 should page someone).
6. **Handle incidents:** compromised key → revoke, reissue, investigate issuance logs; mis-issued cert → contact the CA, monitor CT; keep a runbook, because expiry outages happen at 2 AM.

### TLS review checklist

- [ ] TLS 1.2+ only; weak protocols/ciphers disabled; forward secrecy enabled
- [ ] Certificates valid, correctly chained, from a trusted CA; SANs cover all names
- [ ] Renewal automated; expiry alerts at multiple thresholds
- [ ] HSTS deployed with includeSubDomains (preload where appropriate)
- [ ] CT monitoring active for owned domains
- [ ] Internal services use internal CA / mTLS, not public certs stretched thin
- [ ] Config verified by scanner after every infrastructure change

### Sustaining the practice

- Scan all endpoints quarterly; alert on configuration drift immediately
- Review CT logs weekly for unauthorized issuance on your domains
- Test renewal automation by observing an actual renewal, not just the config
- Include TLS endpoints in change-management review for infra changes

### Metrics that prove it works

- % of endpoints on the modern TLS profile (scanner-verified)
- Certificate-expiry incidents (target: zero)
- CT-log alerts actioned within SLA
- Renewal automation coverage % of all certificates

## Common pitfalls

- **Manual renewals.** Every manual process eventually misses a renewal. Automate or accept the outage.
- **HSTS without testing.** includeSubDomains on a domain with HTTP-only subdomains breaks them with no easy rollback. Stage the rollout.
- **Ignoring internal TLS.** "It's inside the VPC" is not encryption. Internal traffic carries the same credentials and data — encrypt it, ideally with mTLS.
- **Wildcard cert sprawl.** One compromised wildcard key affects every subdomain. Prefer scoped certificates and short lifetimes.
- **No CT monitoring.** Mis-issued certificates are only caught if someone watches the transparency logs. Watch them.
- **Cipher "compatibility" exceptions that never expire.** Legacy-client cipher allowances become permanent. Document, time-box, and review.
- **Forgetting mail and legacy protocols.** Web gets hardened while SMTP, IMAP, and old integrations stay on weak TLS. Inventory all TLS, not just HTTPS.
- **HSTS preload without a rollback plan.** Preload is effectively irreversible short-term. Stage max-age increases and verify every subdomain first.
- **Mixed-content and downgrade gaps.** HTTPS pages loading HTTP resources or HSTS-less subdomains leave downgrade paths open. Audit the full page, not just the main URL.
- **Forgetting certificate transparency for internal CAs.** Internal mis-issuance needs monitoring too — log and alert on internal CA issuance anomalies.
