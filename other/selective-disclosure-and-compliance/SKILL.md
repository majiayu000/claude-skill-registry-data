---
name: selective-disclosure-and-compliance
description: Use when the agent must balance privacy with compliance on eERC — selective disclosure to auditors/regulators, proving facts without revealing everything, and designing a compliance model that keeps user privacy intact.
category: Privacy Deep-Dive
difficulty: Advanced
version: "0.2.0"
---

# Selective Disclosure & Compliance

## Overview
"Private" and "compliant" are not opposites. eERC is built for **selective disclosure**: confidentiality for everyone by default, with controlled, authorized visibility for an auditor — without weakening privacy for non-audited flows. This skill is the design layer over [[eerc-auditor-compliance]].

## Mechanisms
1. **Auditor selective decryption.** Every operation encodes an auditor PCT, so a designated auditor can decrypt history via `auditorDecrypt()`. Only the auditor can; other users still see nothing ([[eerc-auditor-compliance]]).
2. **Per-user disclosure.** A user can reveal their own balance/history by sharing decrypted values (or proofs of them) — they hold the decryption key ([[eerc-key-management]]).
3. **Rotatable auditors.** Change the auditor without redeploying; rotation is forward-looking.
4. **Encrypted metadata for audit context.** Attach invoice/reference data decryptable by the counterparty and auditor ([[eerc-encrypted-metadata]]).

## Designing a compliance model
- **Decide the auditor scope.** Whole-contract auditor vs designated per-deployment. Document who holds the key and why.
- **Minimize disclosure.** Disclose to the auditor only; avoid making data public. Default to confidentiality.
- **Data handling.** Define retention/processing of decrypted data per jurisdiction (KYC/AML).
- **On a private L1**, combine with participant gating (KYC at the allowlist) for a defense-in-depth, regulator-friendly setup ([[combining-eerc-with-private-l1]], [[evergreen-institutional]]).

## Privacy/compliance trade-off matrix
| Need | Approach |
|---|---|
| Regulator can audit all flows | contract auditor key |
| User proves solvency/balance to a third party | user-side disclosure of decrypted balance |
| KYC'd participants only | private L1 allowlists ([[l1-transaction-allowlist]]) |
| Confidential references for reconciliation | encrypted metadata |

## Common Pitfalls
- **All-or-nothing thinking.** You don't have to make data public to be compliant — use the auditor channel.
- **Over-disclosure.** Granting broad access "to be safe" erodes the whole point.
- **Assuming rotation re-grants history.** It doesn't ([[eerc-key-management]]).

## AI Agent Prompt
> "Act as a compliance architect. Design a selective-disclosure model for my eERC deployment: who audits, what they can decrypt, how users self-disclose, and how it maps to my KYC/AML obligations without making data public."

## References
See `references/README.md` (academy compliance + auditability, EncryptedERC AuditorManager).
