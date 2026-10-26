---
name: store-readiness
description: Audit the app against App Store / Google Play submission rules before submitting. Use before a release or submission, or when the user mentions store review, rejection, "ready to ship", or ASO.
allowed-tools: Read, Grep, Glob, AskUserQuestion, Bash(npm run store:check*), Bash(git diff*)
---

## Context

- Automated checks: !`npm run store:check 2>&1 | tail -30`

## Task

Produce a store-readiness verdict from the automated output above plus the manual rules in
[`docs/store/checklist.md`](../../../docs/store/checklist.md) (the `STORE-*` catalog).

1. **Report the automated findings** (`STORE-*` with severity) from `npm run store:check` — placeholder
   copy, template identity, account-deletion path, privacy manifest, target SDK.
2. **Walk the MANUAL rules** that automation can't check, and mark each PASS / FAIL / NEEDS-INPUT with
   its rule ID:
   - Demo account + live backend at review (STORE-APL-2.1-DEMO); no dead buttons/placeholders.
   - Metadata/screenshots match the build; name ≤30 (STORE-APL-2.3-META).
   - IAP + working **Restore Purchases**; subscription discloses price + EULA + Privacy + auto-renew
     (STORE-APL-3.1.1/3.1.2). Google: Play Billing (STORE-GP-BILLING).
   - Privacy Nutrition Labels / Data safety match real + SDK behaviour (STORE-APL-LABELS / STORE-GP-DATASAFETY).
   - Sign in with Apple if social login is offered (STORE-APL-4.8).
   - **4.3 originality (STORE-APL-4.3-UNIQUE):** ask the user (AskUserQuestion) for the **one-sentence
     differentiator** — what makes this app not a re-skin. If they can't state one, that's a FAIL.
3. End with `## Verdict: READY | BLOCKED` (any P1 FAIL ⇒ BLOCKED) and the exact next actions, citing
   rule IDs and [`docs/store/submission-runbook.md`](../../../docs/store/submission-runbook.md).
