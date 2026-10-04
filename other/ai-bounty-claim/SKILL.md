---
name: ai-bounty-claim
description: Claim the AI bounty on tDVV by delegating to the canonical repo SKILL and its branch docs; this public skill is AA/CA only and requires explicit write confirmation.
compatibility: opencode
---

# AI Bounty Claim

This project-local OpenCode skill is a thin bootstrap wrapper. The canonical instructions live in `SKILL.md` at the repository root.

## Use this skill when

- the user wants to claim the AI bounty on `tDVV`
- the user wants to use `email` to recover/login before an `AA/CA` claim
- the user needs AA/CA onboarding, sync preflight, or AA/CA diagnostics on `tDVV`

## Required steps

- Read `SKILL.md` at the repository root first and treat it as the source of truth.
- Choose exactly one branch and then read the matching files in `references/flows/` and `references/examples/`.
- Treat this public bounty skill as `AA/CA only`; accept `CA` as the same route alias.
- Require `@portkey/ca-agent-skills >= 2.3.0` for the AA/CA route because claim now depends on `manager-sync-status` / `portkey_manager_sync_status`.
- Before any AA/CA chain write, resolve local context and `caHash`, run `manager-sync-status`, run `GetHolderInfo(caHash)`, and stop unless both manager sync and holder lookup are ready on `tDVV`.
- If a user asks for the old EOA route, explain that this public skill no longer supports it and redirect them to AA/CA onboarding or diagnostics.
- Never infer a fee problem from `Holder is not found` or `CA holder not found`.
- Never ask the user to paste an exchange or custodial address.
- Before any chain write, show the manager signer, manager sync status, holder lookup status, `caHash`, CA contract raw address, reward contract raw address, method chain, receiver semantics, reward amount, and gas note, then require explicit confirmation.
- If a transaction fails, surface the exact chain error and stop.
