---
name: orbit-vdp
description: Verify a WordPress plugin meets the EU Cyber Resilience Act mandate (effective 2026) — every commercial WP plugin sold in the EU must have a published Vulnerability Disclosure Program (VDP). Checks for SECURITY.md / security.txt / public VDP page + contact channel + response SLA. Use when the user says "VDP", "vulnerability disclosure", "EU CRA", "cyber resilience act", "security.txt", or before launching any commercial plugin in the EU.
---

# 🪐 orbit-vdp — EU CRA Vulnerability Disclosure Program audit

The EU Cyber Resilience Act mandates a published VDP for every commercial WordPress plugin sold in the EU as of 2026. Plugins without one cannot be legally sold to EU users. This skill verifies compliance.

---

## Runtime — fetch live before auditing (DO THIS FIRST)

When this skill is invoked:

1. **Fetch in parallel**:
   - https://patchstack.com/whitepaper/state-of-wordpress-security-in-2026/ → current EU VDP requirement context
   - https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act → official EU CRA page (legal source)
   - https://disclose.io/ → modern VDP boilerplate
   - https://datatracker.ietf.org/doc/html/rfc9116 → security.txt RFC

2. **Synthesize**:
   - "Is the EU CRA actually in effect today?" (check EC date)
   - "What's the minimum VDP must include per the latest guidance?"
   - "Is `security.txt` (RFC 9116) sufficient or does the plugin need a full SECURITY.md?"

3. **Audit the plugin** against fetched current rules.

---

## What this skill checks

### 1. SECURITY.md present in plugin repo
```markdown
# Security Policy — My Plugin

## Reporting a Vulnerability
We take security seriously. To report a vulnerability:

- Email: security@example.com (PGP key: <fingerprint>)
- HackerOne: hackerone.com/my-plugin
- We respond within 72 hours.

## Supported Versions
Active support: latest minor of the current major.
Security-only support: previous major for 6 months after major bump.

## Disclosure Timeline
- We confirm receipt within 72 hours
- We aim to patch within 30 days for high severity
- Coordinated disclosure: we publish details ≥ 30 days after patch ships
```

### 2. security.txt (RFC 9116) at well-known location

```
# /.well-known/security.txt
Contact: mailto:security@example.com
Contact: https://example.com/.well-known/vdp
Expires: 2027-01-01T00:00:00.000Z
Encryption: https://example.com/pgp-key.txt
Acknowledgments: https://example.com/security/acknowledgments
Preferred-Languages: en
Canonical: https://example.com/.well-known/security.txt
Policy: https://example.com/security/policy
Hiring: https://example.com/jobs
```

If your plugin is sold from a website, the website should serve this. If your plugin's repo is public, the repo should also have a `SECURITY.md`.

### 3. Public VDP page on the seller's website
Customers (and security researchers) need to find the disclosure path without digging. Recommended URL: `/security` or `/.well-known/vdp`. Linked from the plugin's WP.org page + your store page.

### 4. Response SLA published
**Whitepaper intent:** A VDP without a response SLA is a black hole. Researchers won't bother reporting if the plugin's response time is unknown / months. Patchstack's 2026 report shows the median time-to-first-exploit is 5 hours — the response SLA matters.

Recommended SLAs:
- Acknowledge receipt: ≤ 72 hours
- Triage + severity rating: ≤ 7 days
- Patch + release for Critical: ≤ 30 days
- Public disclosure timing: ≥ 30 days post-patch (coordinated)

### 5. Safe harbour clause
The VDP should explicitly grant researchers safe harbour:

> "We will not pursue legal action against researchers who report vulnerabilities in good faith and follow this policy. Acting in good faith includes: not destroying / modifying user data, not hindering plugin operation, and giving us reasonable time to respond before public disclosure."

### 6. EU CRA-specific clauses
Per the CRA (2026), commercial plugins must:
- Maintain a vulnerability disclosure policy
- Provide a "single point of contact" for reports
- Issue security updates throughout the product's expected lifetime
- Report exploited vulnerabilities to ENISA within 24h

These are LEGAL obligations — non-compliance can mean €15M / 2.5% of global turnover fines.

### 7. Acknowledgments page
Listing past researchers who've responsibly disclosed — culturally important + signals legitimacy.

---

## Output

```markdown
# VDP Audit — my-plugin · 2026-04-30

> Per EU Cyber Resilience Act (fetched digital-strategy.ec.europa.eu 2026-04-30):
> Commercial WP plugins sold in EU MUST have published VDP. Non-compliance: €15M / 2.5% global turnover fine.

## Current state
- ❌ No SECURITY.md in plugin repo
- ❌ No security.txt at https://example.com/.well-known/security.txt (404)
- ❌ No /security page on plugin website
- ❌ No published response SLA
- ❌ No safe-harbour clause anywhere

## Severity: CRITICAL — cannot legally sell in EU as-is

## Action plan
1. Create SECURITY.md in repo (template available at disclose.io)
2. Add /.well-known/security.txt to plugin website (RFC 9116 format)
3. Publish /security page on store with full policy
4. Add safe-harbour clause
5. Designate single point-of-contact per CRA
6. Document patch SLA + ENISA reporting workflow
```

---

## Pair with

- `/orbit-cve-check` — find vulns to disclose responsibly
- `/orbit-sec-supply-chain` — VDP also covers your dependencies
- `/orbit-wp-security` — proactive vuln finding

---

## Smoke test

Input: a plugin with no SECURITY.md and no security.txt.
Expected:
- CRITICAL severity
- 5 specific action items
- Cites EC and Patchstack pages with today's fetch date

---

## Embedded fallback rules (offline)
- EU CRA enforces VDP for commercial plugins as of 2026
- SECURITY.md should be in plugin repo
- security.txt at /.well-known/security.txt (RFC 9116)
- Response SLA: 72h ack / 7d triage / 30d patch
- Safe harbour clause for researchers
- Designate single point-of-contact per CRA
- ENISA reporting within 24h for exploited vulns

## Sources & Evergreen References

### Live sources (fetched on every run)
- [EU Cyber Resilience Act](https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act)
- [Patchstack 2026 Security Report](https://patchstack.com/whitepaper/state-of-wordpress-security-in-2026/)
- [disclose.io VDP boilerplate](https://disclose.io/)
- [security.txt RFC 9116](https://datatracker.ietf.org/doc/html/rfc9116)
- [ENISA reporting guidance](https://www.enisa.europa.eu/)

### Last reviewed
2026-04-30 — fetch on every run; CRA enforcement details may shift through 2026
