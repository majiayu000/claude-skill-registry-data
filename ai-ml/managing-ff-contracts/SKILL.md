---
name: managing-ff-contracts
version: "1.0.0"
description: >
  Manages the full contract lifecycle for FlashFusion client engagements — from proposal to signed document to archive. Selects the right template (NDA, SOW, change order, or MSA), populates it with targeted questions, applies AI-specific clauses, and walks through the DocuSeal send workflow.

  Activate when the user mentions: contract, proposal, SOW, statement of work, NDA, non-disclosure, change order, scope creep, DocuSeal, send for signature, engagement letter, client agreement, retainer agreement, "client wants to proceed", "ready to close", "new client", "need a contract for", "out of scope", "client asking for more", "client signed", "how do I invoice", "deliverable definition", or any mention of formalizing a client engagement.
---

# FF Contract Manager

Generates and manages client-facing legal documents for FlashFusion. Covers the full lifecycle: detect document type → targeted questions → generate with AI clauses → DocuSeal workflow → archive.

Default posture: opinionated and fast. Recommend the right template and populate it. Don't ask for things that can be inferred from context.

---

## DEPENDENCY_DECLARATION

| Tool | Status | Purpose |
|---|---|---|
| DocuSeal | ✅ Connected | E-signature workflow for all client documents (Step 4) |

> **Note:** All signing operations run exclusively through DocuSeal. If DocuSeal is unreachable, stop at Step 4 and notify the user — do not fall back to email attachment delivery.

---

## Step 1: Detect Document Type

| Context signal | Document |
|---|---|
| New prospect / pre-sales conversation | **Mutual NDA** |
| "client wants to proceed" / new project / quoting | **SOW** + MSA (if first engagement) |
| "client asking for X that wasn't in scope" | **Change Order** |
| Ongoing / monthly work | **MSA** + SOW amendment |
| Website, audit app, platform | **Platform T&S / Privacy Policy** |

If unclear, ask one question only: "Is this a new client, an existing client with a scope change, or a platform user?"

---

## Step 2: Clarifying Questions

Ask only what's missing. Never more than 5 things.

**For SOW:**
1. Client name and contact name
2. Service type — `workshop | audit | implementation-build | retainer | training`
3. Deliverables (what does done look like — be specific)
4. Timeline: start date, milestones, final delivery date
5. Pricing: fixed fee total, or hourly rate + estimate

**For NDA:**
1. Other party name and signatory
2. Purpose of disclosure in one sentence
3. Any specific carve-outs needed?

**For Change Order:**
1. The original SOW number/date
2. What is being added
3. Additional cost and revised timeline

**For MSA:**
1. Client legal entity name
2. Payment terms preference (Net-15 or Net-30)
3. Any non-standard client requests?

---

## Step 3: Generate Document

Use the template matching the document type. Replace every `{{PLACEHOLDER}}` — do not leave any unfilled.

### AI-Specific Clause Checklist

Run this on every SOW and MSA before presenting. Add missing clauses inline.

- [ ] **IP Ownership** — "Client owns all deliverables defined in this SOW. Consultant retains rights to general methodologies, prompt frameworks, and tooling developed independently of Client's proprietary data."
- [ ] **AI Tool Disclosure** — "Delivery may involve AI language models, automation platforms, and third-party APIs. Client acknowledges this as part of the agreed delivery methodology."
- [ ] **Data Handling** — "Client data will not be used to train AI models. Consultant will not input Client data classified as confidential into AI systems without prior written consent for each data category."
- [ ] **Deliverable Specificity** — Every AI agent, workflow, or automation deliverable must define: inputs, outputs, and success criteria. "An AI agent that handles X" is not sufficient.
- [ ] **Platform Change Language** — "Deliverables are defined as point-in-time builds. Changes to underlying AI models, APIs, or third-party platforms after delivery do not constitute material changes to this SOW."

Flag any missing clause with `[MISSING — ADD BEFORE SEND]` in-line.

---

## Step 4: DocuSeal Workflow

1. **Template exists?**
   - Yes → load and populate in DocuSeal UI
   - No → upload generated document → define signature fields → save as reusable template

2. **Signatories** — standard order is client signs first, Kyle countersigns:
   - Signer 1: `{{CLIENT_NAME}} <{{CLIENT_EMAIL}}>`
   - Signer 2: `[EMAIL]`

3. **Reminder** — set 3-day auto-reminder if no response

4. **Send** — from DocuSeal UI or via API. Do not email document attachments.

### DocuSeal Error Handling

If a DocuSeal operation fails, identify the failure mode and respond exactly as shown. Do not retry silently.

| Failure Mode | Signal | Required Response |
|---|---|---|
| **Invalid signatory email** | DocuSeal rejects envelope with "invalid email", "recipient not found", or "delivery failed" | State the error explicitly: "DocuSeal rejected the signatory email `{{CLIENT_EMAIL}}`. Please verify the address is correct and confirm before I resubmit." Do not retry until user provides a corrected address. |
| **File format rejection** | DocuSeal returns a format error or "unsupported file type" on DOCX upload | Inform user: "DocuSeal rejected the DOCX — converting to PDF and resubmitting." Convert the generated document to PDF, then resubmit to DocuSeal. If conversion is not available in session, provide the PDF conversion instruction to the user. |
| **Expired session / auth timeout** | DocuSeal returns 401, "session expired", "unauthorized", or the MCP tool call fails with an auth error | Stop immediately. Do not retry. State: "DocuSeal session has expired. Please re-authenticate via Settings → Connectors → DocuSeal, then confirm to resubmit." Resume only after user confirms re-authentication. |

---

## Step 5: Archive

After all parties sign:

- **Google Drive:** `FlashFusion/Clients/{{CLIENT_NAME}}/Contracts/{{YYYY-MM}}_{{doc_type}}_signed.pdf`
- **Notion:** Update client record — contract status, date signed, Drive link

---

## FlashFusion Standard Payment Terms

Embed these in every SOW and MSA. Do not negotiate without flagging:

- Fixed scope: 50% deposit on signing, 50% on final delivery
- Retainer: monthly invoicing on the 1st, Net-15
- Late payment: 1.5% monthly fee after 15 days; work paused after 30 days
- Kill fee: 25% of remaining contract value if Client cancels after kickoff

---

## Quality Gate

Before presenting any document:

- [ ] All `{{PLACEHOLDER}}` fields resolved — zero left blank
- [ ] AI clause checklist complete
- [ ] Payment terms match FlashFusion standard (or deviation flagged)
- [ ] Scope section specific enough to function as a scope-creep reference
- [ ] Signatures section present with correct signatory names

If any item fails: fix before presenting. Never surface an incomplete document.

---

## Anti-Patterns

- **Don't generate a generic template** — every document must have FlashFusion's name, the specific client, and real deliverable language
- **Don't skip AI clauses for small engagements** — a $500 workshop still needs IP and data handling language
- **Don't send via email attachment** — DocuSeal only; email attachments create version-control problems
- **Don't let verbal agreements stand** — if a client says "we're good to go," the next output is an NDA or SOW, not a project kickoff
- **Don't leave "an AI agent that handles X" as a deliverable** — always push for specificity: inputs, outputs, success criteria
