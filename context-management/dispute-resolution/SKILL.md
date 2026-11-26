---
name: dispute-resolution
description: Freelance dispute resolution — escrow, evidence, mediation, milestone release. Protects freelancer and client fairly.
personas:
  - FREELANCE
  - LEGAL
triggers:
  - dispute
  - نزاع
  - milestone release
  - رفض تسليم
  - dispute resolution
  - تحكيم
tech_stack:
  - documenso/documenso
  - invoiceninja/invoiceninja
  - chatwoot/chatwoot
---
[SKILL] dispute-resolution
[OBJ] Resolve freelance conflicts — non-payment, rejected delivery, scope fights — through evidence, platform escrow, and structured mediation, minimizing loss and reputation damage.

[RULES]
1. [REQ] Prevent first: every engagement uses `contract-studio` + platform escrow/milestones so disputes have a contractual baseline. No contract = higher risk.
2. [REQ] Evidence discipline: keep timestamps, messages, deliverable versions, approvals. A dispute is won/lost on documented evidence, not claims.
3. [CMD] Context7 IDs: `documenso/documenso` (signed contract + audit trail), `invoiceninja/invoiceninja` (invoice/payment record), `chatwoot/chatwoot` (comms log).
4. [REQ] Escrow flow (platform): request milestone release with evidence; if client rejects, invoke platform dispute with the record. Follow Upwork/Freelancer/Mostaql process exactly.
5. [REQ] Mediation ladder: (1) direct clarification, (2) offer revision within scope, (3) partial delivery/refund compromise, (4) platform/official mediation. Escalate in order.
6. [REQ] Scope defense: cite the signed SOW; reject out-of-scope without a change-order (see `client-onboarding`). Offer paid add-on instead.
7. [REQ] Arabic/RTL: Arabic-platform disputes (Mostaql/Khamsat) follow their Arabic ToS; Arabic evidence + RTL; tone per `arabic-freelance`.
8. [REQ] Documentation: log dispute, parties, evidence, steps, outcome to memory for pattern analysis (feeds `freelance-niche` risk profile).
9. [REQ] Reputation protection: stay professional; never public shaming; some platforms penalize. Prefer private resolution.
10. [REQ] Legal escalation: only after platform routes fail; advise user to consult a licensed attorney (no legal advice given).

[PROHIBIT]
1. No forged or altered evidence.
2. No off-platform "side settlement" that voids protections.
3. No using client data/hostage as leverage.
4. No dispute handled without the signed contract on file.
