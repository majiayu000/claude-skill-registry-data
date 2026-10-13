---
name: network-email-security
description: >
  Email security review: dissect phishing samples (headers, URLs, attachments), assess a domain's
  spoofability via SPF/DKIM/DMARC alignment, recognize BEC patterns, and audit tenant anti-phishing
  controls incl. OAuth consent abuse. Load on phishing email analysis, .eml header review,
  "can this domain be spoofed", DMARC/SPF checks, or BEC investigation. Signals: Received chain,
  Authentication-Results, dmarc p=none, ~all vs -all, reply-to mismatch, lookalike domains.
domain: network
type: checklist
stability: learning
modes: [pentest, bugbounty, defense]
severity: high
mitre: [T1566, T1566.002, T1078]
cwe: [CWE-290]
tools: [dig, nslookup, urlscan]
schema_version: 1
---

# Email security & phishing analysis

## When it applies
Two authorized jobs (`tradecraft-scope-roe`): **(a) defensive** — dissect a reported phishing
email or BEC attempt, extract IOCs, and recommend tenant controls (`defense-*` context); **(b)
offensive** — assess whether an in-scope domain can be spoofed (SPF/DKIM/DMARC posture) as
findings for a report. Sending simulated phishing is a separate, **pentest-only** track — load
`social-eng-methodology` first and never run it against a bug-bounty target. Never re-deliver
malicious samples to real users, and never mass-test third-party domains.

## Why it works
Spoofing succeeds when a domain's authentication records are missing, weak (`~all`, `p=none`), or
misaligned — the receiving server then has no cryptographic reason to reject a forged `From`. And
even with perfect auth, the *display name* and *Reply-To* are unauthenticated, which is what BEC
abuses. Reading full original headers exposes the truth the mail client hides.

## Method
1. **Full original headers** ("show original" / view source). Read the `Received` chain
   bottom-up — only the hops added by *your* infrastructure are trustworthy; early hops are
   sender-supplied. Check `From` vs `Return-Path` vs `Reply-To` consistency and the
   `Authentication-Results` header added by the receiving server.
2. **Auth records of the sender domain:**
   ```
   dig TXT example.com                 # SPF — note -all (hard fail) vs ~all (soft) vs missing;
                                       # >10 DNS lookups voids the record entirely
   dig TXT _dmarc.example.com          # DMARC — p=none only monitors; also check sp= (subdomains)
                                       # and rua (reporting); note relaxed vs strict alignment
   dig TXT <selector>._domainkey.example.com   # DKIM — selectors come from the DKIM-Signature header
   ```
3. **Content & URLs.** Defang and detonate links in a sandbox (urlscan.io), not in a browser.
   Compare link text vs href; check lookalike/punycode domains against the real brand.
4. **Attachments.** Static analysis / sandbox only — never open on a live host; route through
   `defense-malware-triage`.
5. **BEC pattern check.** Display-name impersonation of an exec, urgency + payment/wire/gift-card
   framing, `Reply-To` redirected to a free-mail or lookalike domain, thread hijacking.
6. **Tenant control review** (defensive engagements): anti-phishing policy, external-sender
   tagging, MFA coverage, and OAuth app consent grants — consent phishing rides legitimate
   identity providers, so audit authorized third-party apps (ties into `web-account-takeover`).
7. **Weaponize the IOCs** — sender addresses, reply-to, URLs/domains, attachment hashes feed
   `defense-detection-engineering` / `defense-threat-hunting` so the finding becomes a detection.

## Gotchas
- **`p=none` is not protection** — it only reports; likewise `~all` lets spoofed mail through as
  "soft fail". Only `-all` + `p=reject` (or `quarantine`) actually blocks.
- **Subdomains are separate** — without `sp=` in the DMARC record, `mail.example.com` may be
  spoofable when `example.com` isn't.
- **Display-name spoofing passes every check** — auth validates the domain, not the human name.
  The real signal is the `From` address domain and `Reply-To`.
- **Missing DKIM selector** — you can't query DKIM without the selector; pull it from the
  `DKIM-Signature` header's `s=` tag, or try common ones (`google`, `selector1`, `default`).
- **Forwarded mailing lists break SPF legitimately** — don't flag a false positive; alignment and
  DKIM survival matter more there.
- **Never click or detonate outside a sandbox**, and never send test phishing to third parties
  without explicit written authorization.

## Verify success
A written verdict per domain (SPF policy, DKIM validity, DMARC enforcement + alignment, spoofable
yes/no with the exact gap), plus — for sample analysis — a complete IOC list and concrete tenant
recommendations, each traceable to a header line or DNS record.

## References
RFC 7208 (SPF) / 6376 (DKIM) / 7489 (DMARC); urlscan.io; M365/Google anti-phishing policy docs.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
