---
name: compliance-lord
description: Lord skill for regulatory compliance mapping — EU AI Act, NIST AI RMF, ISO 42001. Translates regulatory requirements into enforceable aiZee policy rules. Do not use for legal compliance tasks — use `legal-compliance` instead. Do not use for marketing compliance tasks — use `marketing-compliance` instead.
triggers:
  - compliance lord
  - compliance
  - eu ai act
  - nist ai rmf
  - iso 42001
  - regulatory
  - امتثال
  - تنظيم
personas:
  - LEGAL
  - SEC
  - ARCH
  - PRODUCT
  - DOC
tech_stack: []
lord: true

---

# Compliance Lord

[OBJ] Map regulatory requirements to enforceable aiZee rules. Compliance is not a document — it is a policy gate.

## Problem

Gartner published the first Magic Quadrant for AI Governance Platforms (June 2026). Enterprises need a governance program of record for EU AI Act, ISO 42001, and NIST AI RMF. PDFs and wikis are not enforcement.

## Rules

1. [REQ] **EU AI Act mapping.** Map aiZee rules to EU AI Act articles:
   - Art. 9 (Risk management) → `runtime/policy.py` risk classification
   - Art. 10 (Data governance) → `runtime/supply_chain_guard.py` + data provenance
   - Art. 12 (Logging) → `runtime/audit.py` tamper-evident log
   - Art. 13 (Transparency) → `runtime/composite_identity.py` attribution
   - Art. 14 (Human oversight) → `runtime/guardian.py` human-in-the-loop
   - Art. 15 (Accuracy/robustness) → `eval/reliability.py` reliability@k
2. [REQ] **NIST AI RMF mapping.** Map to four functions:
   - GOVERN → `global-roles.md` + policy engine
   - MAP → `runtime/spec_engine.py` spec-driven context
   - MEASURE → `eval/reliability.py` + `eval/harness.py`
   - MANAGE → `runtime/agent_gateway.py` + `runtime/guardian.py`
3. [REQ] **ISO 42001 mapping.** Map to AI management system clauses:
   - Clause 4 (Context) → `spec.md` + `ACTIVE_CONTEXT.md`
   - Clause 6 (Planning) → `workflows/01-planning.md`
   - Clause 8 (Operation) → `runtime/kernel.py` 5-gate pipeline
   - Clause 9 (Performance evaluation) → `eval/harness.py` + `aizee test --full`
   - Clause 10 (Improvement) → `workflows/06-maintenance.md` + `Memory.md`
4. [REQ] **Risk tier classification.** Classify every AI action into tiers:
   - `minimal` (code formatting) → auto-allow
   - `limited` (code generation) → allow + audit
   - `high` (deploy, DB migration) → ask + human approval
   - `unacceptable` (mass PII collection) → deny always
5. [REQ] **Audit trail retention.** Audit logs retained per regulatory minimum (EU AI Act: 6 months post-deployment; ISO: per org policy). `runtime/audit.py` rotation respects this.
6. [REQ] **Data residency.** Flag actions that move data across residency boundaries (PDPL for Saudi, GDPR for EU). Cross-boundary = WARN + LEGAL review.
7. [REQ] **Right to explanation.** Every high-tier action must produce a human-readable explanation from the audit trail. `audit.read_entries()` + `composite_identity.resolve()`.
8. [REQ] **Model card.** Every model in `runtime/agent_catalog.py` has a model card: provider, tier, training cutoff, known limitations.
9. [REQ] **Incident reporting.** `workflows/19-incident-response.md` extended with regulatory notification timelines (EU AI Act Article 73: 15 days for ordinary serious incidents, 2 days for widespread infringement or critical-infrastructure disruption, 10 days where a death occurred).
10. [REQ] **Conformity assessment.** Before release, run `aizee compliance check` — maps all rules to regulatory articles and reports coverage gaps.
11. [REQ] **Documentation as evidence.** `Memory.md`, `CHANGELOG.md`, `spec.md` serve as compliance evidence. Stale docs = compliance gap.
12. [REQ] **Third-party AI.** Any third-party AI tool (Cursor, Claude, Copilot) used in the SDLC must be registered in `runtime/agent_catalog.py` with its risk tier.
13. [PROHIBIT] Deploying a high-tier AI action without human approval + audit trail.
14. [PROHIBIT] Deleting audit logs before regulatory retention minimum.
15. [PROHIBIT] Cross-residency data movement without LEGAL persona review.
16. [PROHIBIT] Claiming compliance without a completed `aizee compliance check` report.
17. [REQ] **EU AI Act Digital Omnibus.** Regulation (EU) 2026/1744 published 24 July 2026, in force 27 July 2026. Annex III high-risk deferred to 2 December 2027. Annex I high-risk deferred to 2 August 2028. Article 5 original prohibitions in force since 2 February 2025; Digital Omnibus new prohibitions effective 2 December 2026. Article 50 transparency (chatbot disclosure, AI-content labeling) in force 2 August 2026 — NOT deferred. Penalties up to €35M or 7% of global turnover.
18. [REQ] **UAGT crosswalk.** Map aiZee rules to Unified AI Governance Taxonomy (8 regulation-stable domains) reconciling ISO 42001, NIST AI RMF, and EU AI Act. One audit, three frameworks.
19. [REQ] **ISO 42001 UKAS certifications.** UKAS-accredited certifications went live January 2026. ISO 42001 is now procurement table stakes. EU AI Act Article 40 allows harmonized standards (likely ISO 42001) for presumption of conformity.
20. [REQ] **MITRE mapping.** Map aiZee detection rules to MITRE ATLAS v2026.06, ATT&CK v19.1, CWE 4.20, and CSA AI Controls Matrix v1. Cross-reference with OWASP LLM/ASI Top 10s.
21. [REQ] **Article 50 transparency.** Ensure AI-generated content is labeled, chatbot disclosure is present, and deepfake detection metadata is attached. Non-compliance = penalty.
22. [REQ] **Incident notification timelines.** EU AI Act Article 73: 15 days for ordinary serious incidents (Art 73(2)); 2 days for widespread infringement or serious and irreversible disruption of critical infrastructure (Art 73(3)); 10 days where a person has died (Art 73(4)). Update `workflows/19-incident-response.md` with regulatory notification templates per tier.
23. [ALIGN] **Gartner/Forrester market alignment.** Align aiZee governance features with Gartner Magic Quadrant for Enterprise AI Coding Agents (May 2026) [VERIFY: cite licensed copy] and Forrester Agentic Development Platforms Landscape, Q3 2026 (RES198045) [VERIFY: cite licensed copy]. 12-field audit schema for procurement. These are market alignment targets, NOT legal compliance requirements.
24. [REQ] **Vendor independence.** Position against market consolidation (Promptfoo→OpenAI, Portkey→Palo Alto, Langfuse→ClickHouse, Helicone→Mintlify, Lakera→Check Point). Open, self-hostable governance = competitive moat.
25. [PROHIBIT] Claiming EU AI Act compliance without Digital Omnibus deadline tracking.

## Compliance Check Output

```
aizee compliance check
→ EU AI Act: 6/6 articles mapped (Art. 9, 10, 12, 13, 14, 15)
→ NIST AI RMF: 4/4 functions mapped (GOVERN, MAP, MEASURE, MANAGE)
→ ISO 42001: 5/5 clauses mapped (4, 6, 8, 9, 10)
→ Risk tiers: 4/4 defined (minimal, limited, high, unacceptable)
→ Audit retention: 6 months (EU AI Act compliant)
→ Coverage gaps: 0
```

## References

- Gartner Magic Quadrant for AI Governance Platforms (June 2026).
- EU AI Act Articles 9-15.
- NIST AI RMF 1.0 (GOVERN/MAP/MEASURE/MANAGE).
- ISO/IEC 42001:2023 (AI management system).
- Exceeds AI: 7-step governance framework (NIST + ISO alignment).
