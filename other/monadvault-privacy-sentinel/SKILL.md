---
name: monadvault-privacy-sentinel
description: "Audit MonadVault material for privacy leakage, unsafe sharing, missing consent, excessive access, memory-scope mistakes, provider exposure, and publication risk. Use when a Steward asks whether something is safe to store, remember, send, export, disclose, or publish; requests redaction or a privacy review; or reviews Monad settings, Vault Memory, Share Capsules, public copy, prompts, capability permissions, third-party data, credentials, or sensitive personal information."
---

# MonadVault Privacy Sentinel

## Overview

Use this skill as a privacy and sovereignty review pass. It identifies leakage, missing consent, scope creep, publication risk, provider exposure, and misleading claims.

This is not legal advice. For legal compliance decisions, recommend qualified review.

## Routing

- Use this skill to audit and classify risk, then recommend required changes.
- Use `monadvault-share-capsule-builder` to draft the public artifact after privacy blockers are resolved.
- Use `monadvault-vault-memory-curator` to turn approved source material into scoped memory candidates.

## Review Workflow

1. Identify the surface:
   - private memory
   - Monad configuration
   - capability scope
   - Share Capsule
   - public directory listing
   - export
   - provider-bound prompt
2. Classify the data: personal, confidential, third-party, regulated, sacred/cultural, credential/secret, public, or operational.
3. Check exposure path:
   - retained in Vault
   - visible to a Monad
   - sent to an LLM provider
   - published in a Share Capsule
   - visible to visitors
   - included in export
4. Review consent and least privilege.
5. Assign findings:
   - `Blocker`: do not store, send, or publish until fixed.
   - `High`: serious risk requiring explicit confirmation and mitigation.
   - `Medium`: fix or disclose before use.
   - `Low`: clarity or hygiene improvement.
6. Provide a revised safer version when useful.

## Output Contract

Return:

- `Decision`: clear, conditional, or block
- `Findings`
- `Required changes`
- `Safer rewrite` when applicable
- `Consent questions`
- `Residual risk`

Use [privacy-review-checklist.md](references/privacy-review-checklist.md) for a systematic pass.

## Guardrails

- Do not approve publication of private Vault Memory by implication.
- Treat secrets, credentials, payment data, raw identifiers, and third-party private data as blockers unless the user supplies a valid and narrow reason.
- Prefer explicit wording: say what is private, what is public, and what may be sent to providers.
- Keep the review practical. Do not bury blockers under long general warnings.
