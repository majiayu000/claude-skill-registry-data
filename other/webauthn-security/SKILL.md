---
name: webauthn-security
description: Use when assessing or implementing WebAuthn and passkeys
  on an authorized engagement. Covers registration and authentication
  ceremonies, attestation review, common implementation flaws, and
  fallback security. Also use when replacing passwords with phishing
  resistant MFA.
version: 1.0.0
domain: auth
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [auth-attacks, session-management-security, phishing-defense]
tools:
  - name: Python
    version: "3.12"
  - name: Burp Suite
    version: "2026.2"
---

WebAuthn gives phishing resistant authentication: the credential is
bound to the origin, so a fake site cannot use it. This skill covers
authorized assessment and implementation review: the ceremonies,
what to verify server side, and the flaws that undo the phishing
resistance. Test with your own accounts and test authenticators.

## Quick Workflow

1. Map the flows: registration, authentication, and recovery or
   fallback.
2. Review the server side verification: challenge, origin, and
   signature checks.
3. Test the ceremony parameters: what the server actually enforces.
4. Check attestation: what is verified and what it proves.
5. Test the fallback: is the recovery path weaker than WebAuthn.
6. Check credential management: multiple keys, revocation, and
   synced passkeys.
7. Verify the phishing resistance claim end to end.
8. Report with the exact verification gaps.

## 1. Ceremony verification checklist

```bash
# Server must verify on registration:
# - challenge matches the session's challenge (and is single use)
# - origin matches the expected RP ID origin exactly
# - attestation signature valid (per the chosen attestation level)
# - credential ID not already registered to another user
# Server must verify on authentication:
# - challenge fresh and single use
# - origin correct
# - signature valid with the stored public key
# - signCount increased (clone detection) or handled per policy
echo "each missing check is a finding; origin and challenge are critical"
```

```bash
# Test with Burp (your test account):
# 1. capture a registration ceremony
# 2. replay the same attestation response -> must fail (challenge reuse)
# 3. tamper the origin in a proxied response -> must fail
# 4. register the same credential for two users -> must fail
echo "automate the negative tests; they are the whole assessment"
```

## 2. Fallback review

```bash
# The fallback decides the real security:
# - SMS fallback: the phishing resistance is gone; note it
# - helpdesk reset: review the verification procedure
# - still password only for some users: segment the risk honestly
echo "report: WebAuthn coverage % and the fallback strength per cohort"
```

## Edge cases

- Synced passkeys (iCloud, Google). Convenience up, device bound
  guarantee down; document the tradeoff.
- Attestation set to none. Fine for most; know what you lose
  (authenticator provenance).
- The RP ID covers subdomains oddly. Verify the exact origin
  matching; subdomain issues break the phishing resistance.

## Escalation

- Ceremony check missing: demonstrate the bypass (replay or
  origin confusion) with test credentials.
- Library handles it all: still verify the integration; most flaws
  are in the glue, not the library.

## Detection and defender view

WebAuthn deployments detect attacks through attestation failures,
signCount anomalies (cloned credentials), and fallback abuse
rates. They defend with strict ceremony verification, monitored
fallbacks, and user education on passkey management. The durable
win is structural: origin bound credentials remove whole phishing
categories by construction.

## Key references

- W3C Web Authentication Level 2/3.
- CWE-287 (Improper Authentication): ceremony flaws.
- FIDO Alliance deployment guidance.
