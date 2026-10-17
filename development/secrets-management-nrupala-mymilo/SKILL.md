---
name: secrets-management
description: Keep secrets secret — stores, scoping, rotation, leak response, and zero secrets in code or logs.
version: 1
triggers: secrets, api keys, rotate keys, leaked secret, secret store, credentials hygiene
category: Security & privacy
blurb: Keep secrets secret — one store, tight scoping, routine rotation and a leak-response plan.
archetype: knowledge
example: A key leaked in a repo — what do I do, in what order?
---

# Secrets Management

Secrets are liabilities with an expiry you choose. Store them centrally, scope them tightly, rotate them on schedule — or they will leak.

## When to use
- Any credential: API keys, tokens, certificates, DB passwords, signing keys.
- Setting up a new service, CI pipeline, or agent integration.
- Handling a suspected leak.

## Method
1. **Single source of truth**: a secret store (vault, OS keychain, 1Password/Bitwarden, SOPS, CI secret store) — environments *reference* secrets, they never define them in files.
2. **Zero in code/logs/artifacts**: pre-commit scanning (gitleaks-class) + CI scans; scrub error outputs; mask in CI logs; no secrets in chat, screenshots, or issue trackers.
3. **Scope tightly**: one secret per purpose + environment; least privilege permissions; separate dev/stage/prod sets; never reuse across environments.
4. **Short-lived where possible**: JIT tokens, OIDC-to-cloud federation, workload identities — replace static keys with ephemeral ones.
5. **Rotation as routine**: calendar-driven rotation for statics; on staff/tool changes; on any suspicion. Rotate ≠ delete first: issue new → migrate → revoke old.
6. **Leak response**: assume compromise → revoke/rotate immediately → scan usage logs → assess blast radius → document. No "it's probably fine".
7. **Inventory**: register what secret exists, where, owner, rotation date; review quarterly.
8. **Local dev**: developer secrets via local store/env injection — not a shared `.env` floating in repos or drives.

## Quality gates
- [ ] Scanners in the loop (pre-commit + CI) with zero findings.
- [ ] Secret inventory current with owners + rotation dates.
- [ ] No secret readable in repo history for live systems (or rotated post-exposure).
- [ ] Leak-response runbook exists.

## Red lines
- No secrets in code, config files, logs, chat, or email — ever.
- No reuse of one secret across environments or services.

## Related
`authentication-authorization` · `ci-cd-pipeline` · `secure-build-pattern`.
