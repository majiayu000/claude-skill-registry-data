---
name: contract-studio
description: Generate sign-ready freelance contracts (NDA/SOW/MSA/IP-transfer) from reusable bilingual clauses, then hand off to documenso for e-signature + audit. Free-first, RTL-aware, human legal review required.
personas:
  - FREELANCE
  - LEGAL
triggers:
  - contract studio
  - contract
  - IP transfer
  - اتفاقية
tech_stack:
  - documenso/documenso

---
[SKILL] contract-studio
[OBJ] Produce sign-ready NDA / SOW / MSA / IP-transfer contracts from reusable, bilingual (Arabic/English) clause libraries, then hand off to the `documenso` plugin (template → fields → sign → audit) for legally binding e-signature. Always flag clauses for human legal review before signature.

[RULES]
1. [REQ] Intake first: capture parties, scope, deliverables, milestones, payment terms, IP ownership, confidentiality, jurisdiction, term/termination.
2. [REQ] Template selection: NDA (mutual/one-way confidentiality), SOW (scope + milestones + acceptance), MSA (master terms + order forms), IP-transfer (assignment of rights). Reuse clause blocks; never invent jurisdiction-specific law.
3. [REQ] Bilingual + RTL: generate Arabic (dir="rtl", Arabic numerals optional) and English; mark which is governing language. For Arabic-platform clients (Mostaql/Khamsat) default to RTL Arabic with SAR/AED/EGP pricing where relevant.
4. [CMD] Context7 IDs: `documenso/documenso` — extract the template→fields→sign→audit pattern (recipient roles, field anchors, signed PDF + audit trail).
5. [REQ] Hand-off: emit a documenso-ready template (fields: signer name/email/role, date, signature) and instruct the user to send via the documenso plugin. Do not sign on the user's behalf.
6. [REQ] Human review gate: every contract must carry a visible "⚠ Requires human legal review before signing" notice. Mark high-risk clauses (liability caps, indemnity, non-compete, IP assignment) for explicit attorney sign-off.
7. [REQ] Free-first: documenso (AGPL, self-host or free tier) is the default e-sign path; closed alternatives only as parity.
8. [REQ] Storage: save the final template + signed artifact references via `StorageFactory`; never embed PII/secrets in skill output or logs.

[PROHIBIT]
1. No auto-signing — a contract is never executed without explicit human approval + e-signature.
2. No inventing legal text for a specific jurisdiction's statutes; flag for a licensed attorney.
3. No storing client PII, signer credentials, or signed documents outside the approved storage backend.
