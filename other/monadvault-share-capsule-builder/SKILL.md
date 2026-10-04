---
name: monadvault-share-capsule-builder
description: "Draft, revise, or review a public, unlisted, invite-only, or paid MonadVault Share Capsule. Use when a Steward asks to share or publish a Monad, write a Monad Directory listing, prepare public instructions, define visitor boundaries or engagement terms, disclose memory behavior, list visible capabilities, create sample prompts, describe access or pricing, or separate a public Monad surface from private Vault Memory."
---

# MonadVault Share Capsule Builder

## Overview

Use this skill to prepare the public version of a Monad. A Share Capsule is not the private Monad; it is a curated public package of description, instructions, terms, and explicitly declassified material.

## Routing

- Use this skill to draft the public artifact and visitor-facing terms.
- Use `monadvault-privacy-sentinel` for the final leakage, consent, and provider-exposure audit.
- Use `monadvault-found-monad` when the private Monad's identity or boundaries are not yet defined.

## Workflow

1. Confirm publication intent: private preview, unlisted, public directory, paid access, or collaborator review.
2. Separate private material from public material.
3. Draft or refine public components:
   - public Monad name and summary
   - public instructions
   - intended audience
   - allowed and disallowed use
   - installed capabilities visible to visitors
   - memory policy
   - sample prompts
   - access and pricing language
4. Run a privacy check mentally; recommend Privacy Sentinel for anything sensitive or ambiguous.
5. Remove claims that imply professional authority, guaranteed outcomes, hidden memory access, or private training.
6. Produce a capsule draft and a review checklist.

## Output Contract

Return:

- `Publication mode`
- `Directory summary`
- `Public instructions`
- `Visitor boundaries`
- `Visible capabilities`
- `Memory disclosure`
- `Sample prompts`
- `Access terms`
- `Pre-publication blockers`

Use [share-capsule-template.md](references/share-capsule-template.md) for a copyable draft.

## Guardrails

- Never include private Vault Memory unless the Steward explicitly says it is selected and declassified.
- Do not write as if visitors own or can edit the Monad.
- Do not promise clinical, legal, financial, spiritual, or guaranteed outcomes.
- Paid access language should distinguish provider cost, platform fee, and Steward margin when those details are known.
