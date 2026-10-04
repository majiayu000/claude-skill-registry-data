---
model_tier: inherit
name: dpa-review
description: "Use when reviewing a DPA as controller or processor against GDPR Art. 28 — GREEN/YELLOW/RED gap frame, never a final call. Triggers on \"review this DPA\", \"check this DPA\"."
status: active
tier: senior
council_depth: deep
domain: process
recommended_for_user_types: [legal]
workspaces:
  - legal-review-prep
packs:
  - legal-review-prep
trust:
  level: advisory
install:
  removable: true
---

# dpa-review

## When to use

- A counterparty sends a DPA (their paper or yours) and the question is *where the GDPR Art. 28 obligations are met, partial, or missing* — before an attorney spends time on it.
- An existing processing relationship is being re-papered (new sub-processor chain, new transfer route, new scope) and the Art. 28 surface must be re-walked.
- You need a structured gap frame and the open questions an attorney must resolve — not a redline and not a verdict.

Do NOT use for clause-level redlining of a general contract (route to `contract-review`), for the regulatory-regime delta read in isolation (route to [`privacy-review`](../privacy-review/SKILL.md)), or for the classification / retention / transfer-mechanism operational surface (route to [`data-handling-judgment`](../data-handling-judgment/SKILL.md)). This skill walks the Art. 28 *agreement*; those skills produce the inputs it cites.

## Procedure

### Step 0: Establish jurisdiction and refuse if out of scope

1. Read the DPA's governing-law / jurisdiction clause. Tag the output `Jurisdiction: EU` or `Jurisdiction: DE`.
2. If the DPA is governed by a non-EU/DE regime with no GDPR nexus (e.g. a pure US state-privacy regime), **refuse the gap review**: say "consult licensed local counsel". Note as an open question that GDPR may still apply extraterritorially under Art. 3 (EU-established controller/processor, or offering to / monitoring EU data subjects) — for the attorney to confirm.
3. No default positions ship. Read acceptable values (sub-processor notice window, audit frequency, liability cap, breach-notice deadline) from `legal-practice-profile`. Until configured, every such value is a `[configure]` placeholder in the output, not a guess.

### Step 1: Fix the role — controller or processor

The Art. 28 reading forks on which side you are.

- **You are the controller** → you instruct. Read whether the agreement binds the *processor* to your instructions, confidentiality, security, sub-processor flow-down, assistance, deletion, and audit *rights for you*.
- **You are the processor** → you are bound. Read whether the obligations imposed are deliverable as written (audit cadence you can sustain, deletion you can actually perform, sub-processor flow-down you can pass down).
- **Joint / unclear** → flag it as the first open question; Art. 26 joint-controllership changes the frame.

### Step 2: Walk the Art. 28(3) requirements as a checklist FLOOR (not ceiling)

For each, assign GREEN (present + adequate) / YELLOW (present but weak/ambiguous) / RED (missing or contradicts Art. 28):

1. **(a) Documented instructions** — processing only on the controller's documented instructions, incl. for transfers.
2. **(b) Confidentiality** — persons authorised to process are under a confidentiality commitment.
3. **(c) Security — Art. 32** — appropriate technical and organisational measures named (not "industry-standard" alone).
4. **(d) Sub-processors** — prior authorisation (general or specific), notice of changes + objection right, and **flow-down** of equivalent Art. 28 terms.
5. **(e) Data-subject-rights assistance** — processor assists the controller in responding to DSR requests.
6. **(f) Breach + DPIA assistance — Art. 33/34/35/36** — breach-notification assistance with a deadline, plus assistance with DPIAs and prior consultation.
7. **(g) Deletion / return** — at end of provision, delete or return all personal data + copies, at the controller's choice.
8. **(h) Audit / inspection** — make available the information needed to demonstrate compliance + allow and contribute to audits/inspections.
9. **International transfer — Chapter V** — any transfer outside the EEA has a valid mechanism (adequacy / SCCs with module + version / BCR) and, where required, supplementary measures. Schrems-II transfer-impact assessment is an open question, not a checkbox.

The nine are the floor; flag anything beyond them that materially shifts risk (liability cap, indemnity, deletion-vs-legal-hold conflict).

### Step 3: Frame the gaps and the open questions

1. Produce the GREEN/YELLOW/RED frame, one line per Art. 28(3) item + transfers.
2. For every YELLOW/RED, write the **open question an attorney must resolve** — not a redline. ("(d) names no objection window — is `[configure]` acceptable, or must a specific window be negotiated?")
3. Surface any `[configure]` placeholder that blocked a GREEN/YELLOW/RED call.

### Step 4: Emit the artifacts

Produce `dpa-gap-frame.md` and `open-questions.md`. Each carries the `Jurisdiction:` tag and the attorney-review line. This skill does not opine; it prepares the attorney's review.

## Related Skills

**WHEN to use this**

- Reviewing a DPA against the GDPR Art. 28 surface, as controller or processor.
- Producing a gap frame + attorney open-questions before counsel review.

**WHEN NOT to use this**

- General contract clause redlines (liability, IP, term, termination) — route to `contract-review`.
- Which regime applies / regime delta read — route to [`privacy-review`](../privacy-review/SKILL.md).
- Data classification, retention windows, transfer-mechanism + supplementary-measures operational shape — route to [`data-handling-judgment`](../data-handling-judgment/SKILL.md).
- A binding legal conclusion — route to a licensed attorney; this skill never issues one.

## When the agent should load this

- "Kannst Du diese AVV / DPA gegen Art. 28 prüfen?"
- "Ein Kunde hat seinen Auftragsverarbeitungsvertrag geschickt — wo sind die Lücken?"

## Output

1. **`dpa-gap-frame.md`** — `Jurisdiction:` tag; role (controller/processor); one GREEN/YELLOW/RED line per Art. 28(3)(a)–(h) + Chapter V transfers; the attorney-review line.
2. **`open-questions.md`** — `Jurisdiction:` tag; one attorney-resolvable question per YELLOW/RED, plus every `[configure]` placeholder that blocked a call; the attorney-review line.

## Gotcha

- "Industry-standard security" satisfies neither Art. 28(3)(c) nor Art. 32 — the TOMs must be named; an unnamed measures clause is YELLOW at best, often RED.
- Sub-processor flow-down is the silent RED: the agreement names sub-processors but never binds them to equivalent Art. 28 terms, so the chain leaks obligations.
- The role fork is load-bearing — a processor-side review that reads the controller-side rights as if they were yours mis-frames every deliverability gap.
- "Delete OR return" at the controller's choice is the requirement; a clause that hard-codes deletion (ignoring legal-hold) or hard-codes return is a gap, not a convenience.
- A non-EU governing-law clause does not end the question — GDPR can still bite under Art. 3; refuse the gap review but hand the Art. 3 question to the attorney, never silently drop it.

## Do NOT

- Do NOT ship default values for notice windows, audit cadence, liability caps, or breach deadlines; read `legal-practice-profile` or emit `[configure]`.
- Do NOT issue a final legal call, a clearance, or a "this DPA is fine" — GREEN is a triage signal, not a sign-off. Cite `legal-safety-floor`.
- Do NOT review a DPA outside EU/DE scope as if it were in scope; refuse to gap-review and route to local counsel.
- Do NOT drop the `Jurisdiction:` tag or the attorney-review line from any output.

## Runnable example

Processor-side review of a customer's DPA, governed by German law.

- Step 0 — `Jurisdiction: DE`. In scope. `legal-practice-profile` not configured → notice window, audit cadence, breach deadline are `[configure]`.
- Step 1 — Role = **processor** (we host the customer's SaaS data). Frame reads deliverability, not rights.
- Step 2 — Art. 28(3) walk:
  - (a) documented instructions — GREEN.
  - (b) confidentiality — GREEN.
  - (c) security / Art. 32 — YELLOW ("appropriate measures per industry standard"; no TOMs annex named).
  - (d) sub-processors — RED (general authorisation granted, but **no flow-down** clause binding our sub-processors to equivalent terms, and objection window left blank = `[configure]`).
  - (e) DSR assistance — GREEN.
  - (f) breach assistance / Art. 33 — YELLOW (assistance promised, deadline blank = `[configure]`; can we meet the controller's own 72h clock?).
  - (g) deletion / return — YELLOW (hard-codes deletion; no return option, no legal-hold carve-out).
  - (h) audit — RED for us as processor (on-site audit "at any time, without notice" — not sustainable; cadence = `[configure]`).
  - Chapter V transfers — RED (our logging sub-processor is US-based; no SCC module/version named; Schrems-II TIA = open question).
- Step 3 — open questions, e.g.: *"(d) — add a flow-down clause and a `[configure]` objection window?"*; *"(h) — negotiate audit to `[configure]` cadence with notice?"*; *"Chapter V — which SCC module/version covers the US logging sub-processor, and is a TIA required?"*
- Step 4 — emit `dpa-gap-frame.md` + `open-questions.md`, both tagged `Jurisdiction: DE` and carrying:

> ⚠️ Attorney review required on material use. This is a draft for a licensed attorney, not legal advice and not a legal conclusion.
