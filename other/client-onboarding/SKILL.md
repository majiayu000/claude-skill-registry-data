---
name: client-onboarding
description: Client onboarding orchestrator — intake form, contract, first invoice, delivery plan, client portal. Links contract-studio and invoice-manager.
personas:
  - FREELANCE
triggers:
  - client onboarding
  - onboarding
  - استقبال عميل
  - kickoff
  - client intake
  - استقبال
  - بدء مشروع
tech_stack:
  - documenso/documenso
  - invoiceninja/invoiceninja
  - chatwoot/chatwoot

---
[SKILL] client-onboarding
[OBJ] Turn a signed deal into a smooth, professional start. Run a repeatable intake→contract→invoice→kickoff flow that sets expectations and reduces early churn.

[RULES]
1. [REQ] Onboarding sequence (fixed order): (1) Intake form → (2) Contract via `contract-studio` → (3) First invoice via `invoice-manager` → (4) Delivery plan → (5) Kickoff call → (6) Client portal/handbook.
2. [REQ] Intake form fields: goals, scope, budget, timeline, stakeholders, communication channel, access needs. Store responses; never start work before intake complete.
3. [CMD] Context7 IDs: `documenso/documenso` (template→fields→sign→audit), `invoiceninja/invoiceninja` (client→invoice→payment), `chatwoot/chatwoot` (client inbox, MIT).
4. [REQ] Contract before work: always generate the engagement contract (NDA/SOW/MSA) via `contract-studio` and get signature before any deliverable. No signature = no start.
5. [REQ] First invoice: deposit/milestone-1 invoice issued on contract sign per `invoice-manager`. Net terms stated clearly (e.g., Net-7).
6. [REQ] Delivery plan: milestones, dates, review rounds, deliverables, acceptance criteria. Share in kickoff; align with `dispute-resolution` escalation path.
7. [REQ] Arabic/RTL: bilingual intake + contract + invoice when client is Arabic; RTL templates via `arabic-freelance`; currency in SAR/AED/EGP as appropriate.
8. [REQ] Portal/handbook: a single source of truth (Notion/Sheets/AIOS) with links, timeline, and contacts. Reduces "where is X" tickets.
9. [REQ] Kickoff agenda: recap goals, confirm scope, set cadence (weekly/ biweekly), define success metric, assign owners.
10. [REQ] Memory: record client profile, preferences, risks to `aizee memory add` for retention (`client-retention`).

[PROHIBIT]
1. No deliverable before contract signature.
2. No kickoff without a written delivery plan.
3. No PII in unsecured notes/commits.
4. No scope creep accepted during onboarding without change-order.
