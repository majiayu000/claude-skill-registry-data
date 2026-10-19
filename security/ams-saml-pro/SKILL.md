---
name: saml-pro
description: Deploy SAML SSO securely — assertion hardening, metadata management, and defense against signature and XML attacks.
category: security
---

## Overview

SAML 2.0 remains the backbone of enterprise SSO, federating authentication between identity providers (IdPs) and service providers (SPs) via signed XML assertions. Its XML complexity is also its risk: signature-wrapping, XXE, and assertion-manipulation vulnerabilities have a long history. Defensive SAML practice is strict validation and minimal trust.

This skill covers secure SAML deployment: hardening assertions, managing metadata and certificates, and defending against the known vulnerability classes — from the defender's side.

SAML's XML complexity is a historical source of subtle vulnerabilities — which is why the defensive posture is radical simplicity: use a maintained library, validate strictly, trust minimally, and test the negative cases deliberately. Every SAML integration that 'just works' without negative testing is carrying unverified assumptions about what it rejects.

## When to use

- Implementing SAML SSO for enterprise applications (as SP or IdP).
- Reviewing an existing SAML integration flagged in a pentest or audit.
- Rotating SAML signing certificates without breaking SSO.
- Troubleshooting SSO failures securely (without weakening validation to "make it work").

## Core concepts

- **Trust model:** the SP trusts assertions signed by the IdP's key, for the expected audience, within validity windows. Every element of that trust must be validated — signature, issuer, audience, timestamps, conditions.
- **Assertion validation checklist:** valid XML signature over the expected elements, trusted signing certificate, correct Issuer, AudienceRestriction matching your entity ID, NotBefore/NotOnOrAfter enforced with small clock skew, and no duplicate or unexpected attributes trusted blindly.
- **Known attack classes (defend against):** signature wrapping (signature validates but assertion content differs — validate what you verify), XXE in XML parsing (disable external entities/DTD), assertion replay (enforce OneTimeUse / short validity + session tracking), and IdP key confusion.
- **Metadata:** exchange via signed, TLS-fetched metadata; pin expected entity IDs and certificates; treat metadata refresh as a security-sensitive process.
- **Certificate rotation:** dual-publish new certificates in metadata before cutover; monitor both; retire old only after confirming no traffic uses it.
- **AuthnContext:** request and honor appropriate assurance levels (e.g., require MFA context for sensitive apps); do not accept a weaker context than policy demands.

- **Single logout (SLO) complexity.** SLO across federated apps is notoriously fragile — decide explicitly whether you need it, and if so, test every binding; many deployments are safer with well-managed session lifetimes instead.
- **Attribute authority hardening.** If group memberships drive authorization, the IdP's attribute source (directory, HR system) is a security boundary — protect its provisioning pipeline accordingly.
- **Federation with external partners.** Cross-organization SAML multiplies trust complexity — pin metadata, limit attribute release, and review partner integrations on a schedule.

## Practical workflow

1. **Design the integration:** choose IdP/SP roles, define required attributes (minimal — NameID plus what the app needs), and the assurance level (MFA required?).
2. **Exchange metadata securely:** fetch over TLS, verify signatures where provided, and pin entity IDs. Never accept unsigned metadata from an untrusted channel.
3. **Implement strict validation:** use a well-maintained SAML library (never hand-rolled XML signature validation); enforce the full validation checklist; disable DTD/external entities in the XML parser.
4. **Harden the SP:** validate assertions before creating sessions; map attributes defensively (do not trust email as immutable identity without IdP guarantees); set sane session lifetimes independent of assertion validity.
5. **Test the negative cases:** expired assertions, wrong audience, tampered attributes, replayed assertions, and unsigned responses must all be rejected — test these in staging deliberately.
6. **Operate:** monitor SSO failures and anomalies (spikes in failures can indicate attacks or breakage); rotate signing certs with dual-publish; keep an IdP-initiated vs SP-initiated inventory and disable unused bindings.

### SAML validation checklist (SP side)

- [ ] XML signature valid, from the pinned IdP certificate, covering the assertion
- [ ] Issuer matches expected IdP entity ID; Audience matches SP entity ID
- [ ] Timestamps enforced (NotBefore/NotOnOrAfter, ≤5 min skew)
- [ ] InResponseTo matches the outstanding request (SP-initiated)
- [ ] OneTimeUse honored; replayed assertion IDs rejected
- [ ] XML parser hardened: no external entities, no DTD processing
- [ ] Attributes mapped minimally; privileged roles never derived from unvalidated attributes

### Sustaining the practice

- Re-run negative-case tests after every library or IdP upgrade
- Monitor federation metadata expiry and signature validity
- Review attribute mappings annually — apps accumulate trusted attributes over time
- Keep a runbook for IdP outages: how do users work when SSO is down?

### Metrics that prove it works

- Certificate-expiry incidents (target: zero, via dual-publish monitoring)
- SSO failure anomaly rate (spikes investigated)
- Negative-case test coverage in staging (rejection tests passing)
- Metadata freshness across all integrations

## Common pitfalls

- **Hand-rolled signature validation.** XML signature validation is notoriously subtle — use maintained libraries, never custom code.
- **Validating the signature but using unverified content.** Signature-wrapping attacks exploit exactly this gap: verify that what you validated is what you consume.
- **Ignoring AudienceRestriction.** Accepting assertions meant for another SP enables cross-application attacks.
- **Weakening validation to fix integration issues.** "Just disable audience checking until it works" becomes permanent. Fix the config, not the validation.
- **No certificate rotation plan.** Expired IdP/SP certs cause company-wide SSO outages. Dual-publish and monitor.
- **Trusting attributes for authorization blindly.** Group/role attributes drive access — ensure they come from the trusted IdP and cannot be self-asserted.
- **IdP-initiated SSO left enabled unused.** Every enabled binding is attack surface. Disable IdP-initiated flows where SP-initiated suffices.
- **Clock-skew failures blamed on users.** Intermittent SSO failures are often clock drift, not user error. Monitor skew and set sane tolerances.
- **Debugging by disabling validation in production.** Temporary validation bypasses for troubleshooting have a way of becoming permanent. Debug in staging with logging, never by weakening production checks.
- **Ignoring the NameID format.** Mismatched or unstable NameIDs cause account-linking bugs and potential impersonation. Pin the expected format and treat changes as security events.
