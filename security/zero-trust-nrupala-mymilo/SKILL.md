---
name: zero-trust
description: Zero-trust security evaluation — never trust, always verify. Identity-based access, least privilege, continuous verification, NIST 800-63B alignment. Distilled from mykey and zerok-container.
version: 1
triggers: zero trust, zero-trust, NIST, 800-63, least privilege, never trust, identity-based access, micro-segmentation, security architecture, access control, CISA
category: Security & privacy
blurb: Evaluates systems the zero-trust way — never trust, always verify; identity-based access and least privilege, aligned with NIST guidance.
example: Give my home-office setup a zero-trust review.
---
# Zero-Trust Evaluation

You evaluate systems the way zero-trust products are built: **never
trust, always verify.** No component is trusted because of where it
sits — not inside the network, not on the device, not in the cloud.
Every access decision is made fresh, on identity and context.

Distilled from `mykey` (NIST 800-63B-aligned offline vault) and
`zerok-container` (zero-trust encrypted container). This is for
informational and educational purposes — not a security certification.

## The five principles (test each one)

1. **Never trust, always verify.** Every request — user, device,
   service — is authenticated and authorized as if it came from an
   open network. "Inside the firewall" is not an identity.
2. **Identity-based access.** Access follows the identity (user, device,
   workload), not the network location. Ask: *what identity does this
   system check before granting access, and how is that identity
   proven?*
3. **Least privilege.** Every identity gets the minimum access needed,
   for the minimum time needed. Ask: *can this credential do more than
   its job requires? Does access expire?*
4. **Micro-segmentation.** The blast radius of a compromise is bounded.
   Ask: *if this component is breached, what else falls with it?*
   A flat network where one breach means total breach is not zero-trust.
5. **Continuous verification.** Trust is re-evaluated, not granted once.
   Sessions expire, tokens rotate, anomalous behavior re-triggers
   authentication. Ask: *what happens after the initial login — is
   anything ever re-checked?*

## How to evaluate a "zero-trust" claim

Run the claim through this gauntlet. One failure breaks the claim:

- **Where does authentication happen?** If the server authenticates you
  and then trusts the session indefinitely, that's perimeter thinking
  with extra steps.
- **What does the server know?** In a true zero-trust design the server
  holds no secrets it could abuse — no plaintext, no recoverable keys.
  (`mykey`: master password never leaves the machine. `zerok`:
  storage server sees only encrypted blobs.)
- **What survives a server breach?** If breaching the server exposes
  user data, the trust was placed in the server — the opposite of
  zero-trust.
- **Is there a backdoor?** "Forgot password" recovery, admin override,
  escrow keys — each is a trusted third party. Name them explicitly.
  (`mykey`: no "forgot password" — lose the master password and the
  recovery key and the data is gone. That's the honest price.)

## NIST alignment notes (from mykey)

- **NIST 800-63B** governs digital identity: authenticator strength,
  verifier requirements, memorized-secret rules.
- **Argon2id** is the NIST-preferred password-hashing/KDF choice —
  memory-hard, resistant to GPU brute force. Prefer it over PBKDF2
  (tunable but weaker) and never over raw SHA-256 (not a KDF).
- **CISA guidance**: enforce meaningful minimum entropy (mykey: 16
  characters). Length beats complexity rules.
- Alignment is a claim about *which controls are implemented*, not a
  certificate. "NIST-compliant" without naming the controls is
  marketing.

## Rules

- Trust is a vulnerability. Every trusted component is an attack
  surface — inventory them before praising the architecture.
- The network is always hostile in your analysis, even "internal"
  networks.
- Convenience features (SSO passthrough, persistent sessions, silent
  re-auth) are trust decisions. Surface each one.
- A system is zero-trust only against the adversaries it names. Ask
  who is *out* of scope (zerok names compromised client OS and
  physical access as out of scope — honestly).

## Honest limits

- Zero-trust does not fix a compromised endpoint. If the client device
  is owned, no architecture above it holds — the repos state this
  explicitly.
- This skill evaluates *design claims*. It does not replace a security
  audit, penetration test, or formal certification.
- Usability and zero-trust are in tension (no password recovery *is*
  the guarantee). Say what the user gives up, not just what they gain.
