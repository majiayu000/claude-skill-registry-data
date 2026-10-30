---
name: hol-guard
description: "Install and use HOL Guard as a local pre-execution safety boundary for supported AI coding-agent harnesses, with explicit approval, receipt, and verification flows."
risk: safe
source: hashgraph-online/hol-guard-plugin
date_added: "2026-08-28"
license: Apache-2.0
---

# HOL Guard

Use HOL Guard when a user wants a local enforcement boundary around a supported AI coding-agent harness before consequential tool or command execution.

## Use this skill when

- Setting up HOL Guard for a detected local coding-agent harness
- Running an agent through HOL Guard rather than directly
- Reviewing Guard approvals, receipts, diagnostics, or protection state
- Verifying whether a supported harness is actually protected before work continues

## Do not use this skill when

- The user has not authorized changes to their local agent harness
- The target is an application/server authorization problem rather than a supported local harness
- The requested workflow would require bypassing a Guard denial, approval, or review gate

## Instructions

1. Check whether HOL Guard is installed without reading secrets using a cross-platform direct CLI probe:

   ```bash
   hol-guard --version
   ```

   If it is missing and the user requested runtime setup, prefer the isolated CLI install:

   ```bash
   pipx install hol-guard
   ```

2. Inspect Guard state and detect supported harnesses:

   ```bash
   hol-guard status
   hol-guard detect --json
   ```

   Use the exact harness identifier returned by `hol-guard detect --json`; do not maintain a guessed harness list.

3. For an authorized detected harness, use Guard-owned setup and validation:

   ```bash
   hol-guard bootstrap
   hol-guard install <harness>
   hol-guard run <harness> --dry-run
   hol-guard doctor <harness> --json
   ```

4. Run the harness through HOL Guard only after the dry run and diagnostics support it:

   ```bash
   hol-guard run <harness>
   ```

5. If Guard blocks or requires review, stop the protected action and inspect the decision instead of retrying unprotected:

   ```bash
   hol-guard approvals
   hol-guard approvals open <request-id>
   hol-guard receipts
   hol-guard diff <harness>
   ```

   Use the pending request ID returned by `hol-guard approvals`; do not invent an ID. Approval or denial must remain an explicit user decision after the risk reason and requested scope are understood.

6. Verify the resulting protection state with Guard-owned evidence:

   ```bash
   hol-guard status
   hol-guard doctor <harness> --json
   hol-guard receipts
   ```

## Safety boundaries

- Never read `.env` files as part of this workflow.
- Never bypass Guard approvals or convert deny, review-required, timeout, malformed, unavailable, or error states into an allow.
- Preserve host permissions, repository tests, validation, and required human review; HOL Guard does not replace them.
- Do not claim application/server authorization, downstream correctness, or protection for an unsupported harness.
- Do not mark a workspace protected until HOL Guard command output proves the state.

## Result

Report the commands run, the harness Guard detected, the protection or review state, the evidence available, and the exact next action if the user must intervene.

## Attribution

Adapted for this catalog from the maintained HOL Guard Agent Skill in `hashgraph-online/hol-guard-plugin`. HOL Guard is licensed under Apache-2.0. The bundled `LICENSE` file preserves the upstream license text.
