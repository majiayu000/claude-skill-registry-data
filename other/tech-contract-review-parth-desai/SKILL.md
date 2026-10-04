---
name: "tech-contract-review-parth-desai"
description: "Contract Review for Tech and general contract. Smart redflagging feature to show the problems."
metadata:
  author: "Parth Desai"
  license: "agpl-3.0"
  version: "2026-05-24"
---

# Tech Contract Review — Lawve Plugin for Anthropic

## Purpose

Precision contract analysis for tech-sector agreements. Goal: zero open ambiguity. Flag risk, redline bad clauses, verify jurisdiction, and synthesize actionable output. Operates like a senior tech-transactional lawyer with red pen ready.

---

## Scope — Contract Types Covered

| Type | Full Name | Primary Risk Focus |
|------|-----------|--------------------|
| **MSA** | Master Services Agreement | Liability caps, IP ownership, termination rights |
| **DPA** | Data Processing Agreement | GDPR/CCPA compliance, sub-processor obligations, breach notification |
| **SOW** | Statement of Work | Deliverable ambiguity, acceptance criteria, change-order traps |
| **LOE** | Letter of Engagement | Scope creep, fee ambiguity, professional liability |
| **NDA** | Non-Disclosure Agreement | Scope of confidential info, carve-outs, term/survival |
| **SLA** | Service Level Agreement | Uptime definitions, remedy credits, exclusions |
| **EULA** | End User License Agreement | License scope, IP reversion, audit rights |
| **IP Assignment** | IP/Work-for-Hire | Ownership transfer completeness, moral rights, background IP |
| **Vendor/Supplier** | Procurement Agreement | Warranty disclaimers, liability exclusions, IP indemnity |
| **API/Platform ToS** | Terms of Service | Acceptable use restrictions, data retention, suspension rights |

---

## Review Workflow

### Step 1 — Contract Intake

Before reviewing, establish:

1. **Document type** — identify which contract type(s) above apply
2. **Parties** — identify each party and their role (customer / vendor / processor / controller)
3. **Effective date & term**
4. **Governing law & jurisdiction** — see Jurisdiction Analysis section
5. **Execution status** — draft, signed, or in negotiation?

### Step 2 — Jurisdiction Analysis

**ALWAYS perform jurisdiction analysis first.** It affects how every clause is interpreted.

#### Key Questions
- What governing law clause applies? (e.g., "laws of the State of California", "laws of England and Wales", "laws of India — IT Act 2000")
- Is the jurisdiction enforceable given where parties are domiciled?
- Does it conflict with mandatory local law (e.g., GDPR for EU data subjects overrides a non-EU governing law clause)?
- Is there a dispute resolution mechanism? (court / arbitration / mediation) — and in which seat?

#### Jurisdiction-Specific Flags

| Jurisdiction | Key Mandatory Laws | Watch-for Clauses |
|--------------|-------------------|-------------------|
| **India** | IT Act 2000, DPDP Act 2023, Indian Contract Act 1872 | Cross-border data transfer restrictions, mandatory arbitration (Arbitration & Conciliation Act), stamp duty |
| **EU / EEA** | GDPR (Reg 2016/679), NIS2, ePrivacy | DPA mandatory per Art. 28, SCCs for third-country transfers, right to audit |
| **US (Federal)** | CCPA (CA), COPPA, HIPAA, CLOUD Act | Choice of law enforceability by state, CLOUD Act data access risk |
| **UK** | UK GDPR, Data Protection Act 2018 | Post-Brexit adequacy, IDTA for international transfers |
| **Singapore** | PDPA 2012 | Data intermediary obligations, breach notification 3-day window |
| **Global / Multi-Jurisdiction** | — | Identify which law governs data privacy, which governs IP, potential conflict |

> **Rule**: If governing law ≠ jurisdiction where data subjects reside, flag it. Privacy law follows the data subject, not the contract.

### Step 3 — Clause-by-Clause Analysis

Scan ALL clauses. For each, classify:

- 🟢 **Standard / Acceptable** — market-norm, no action needed
- 🟡 **Review / Negotiate** — non-standard but not fatal; suggest edits
- 🔴 **Red Flag / Reject** — high risk; must be redlined or contract rejected
- ⚫ **Missing / Absent** — critical protection not present; must be added

#### Clause Category Checklist

**A. Definitions**
- [ ] "Confidential Information" — is it over/under-broad?
- [ ] "Intellectual Property" — does it include pre-existing IP? Background IP?
- [ ] "Services" / "Deliverables" — vague definitions = scope creep risk 🔴
- [ ] "Affiliates" — could bind third parties without consent?

**B. Payment & Fees**
- [ ] Payment milestones tied to ambiguous deliverables 🔴
- [ ] Unilateral fee increase clauses 🔴
- [ ] Late payment interest rates — check usury limits per jurisdiction
- [ ] Expense reimbursement — capped or uncapped?

**C. Intellectual Property**
- [ ] Work-for-hire vs. license — who owns deliverables? 🔴
- [ ] Background IP retained by vendor — is grant-back clause present?
- [ ] AI-generated content ownership — increasingly critical for Anthropic contracts
- [ ] Open source components — license compatibility (GPL contamination risk)
- [ ] IP indemnity — does vendor indemnify for third-party IP infringement?

**D. Data Protection (heightened for Anthropic/AI contracts)**
- [ ] Data controller vs. processor designation — matches reality? 🔴
- [ ] Sub-processor obligations — approval mechanism required (GDPR Art. 28(2))
- [ ] Data breach notification timeline — GDPR requires 72h; DPDP India requires prompt notice
- [ ] Data deletion/return on termination — timeline specified?
- [ ] Cross-border transfer mechanism — SCCs / adequacy / IDTA / BCRs?
- [ ] Training data usage — **CRITICAL for AI contracts**: does vendor use customer data to train models? 🔴
- [ ] Audit rights — customer right to audit processor's compliance?

**E. Confidentiality**
- [ ] Scope of NDA obligations — mutual or one-way?
- [ ] Carve-outs — publicly known, independently developed, required by law?
- [ ] Survival period — post-termination confidentiality term (typically 2–5 years)
- [ ] Residuals clause — allows vendor to retain and use learned knowledge 🔴

**F. Liability**
- [ ] Liability cap — amount and basis (fees paid in 12 months is standard)
- [ ] Consequential/indirect damage exclusion — one-way or mutual?
- [ ] Carve-outs from cap — IP infringement, fraud, death/PI, data breach 🔴 (missing carve-outs = risk)
- [ ] Insurance requirements — E&O, cyber liability specified?

**G. Indemnification**
- [ ] IP infringement indemnity — vendor indemnifies customer? 🔴 if absent
- [ ] Data breach indemnity — tied to processor obligations?
- [ ] Third-party claims — "defend, indemnify, hold harmless" — is "defend" present?
- [ ] Indemnity procedure — timely notice, control of defense required?

**H. Warranties & Representations**
- [ ] Functionality warranty — does software/service perform per specs?
- [ ] Non-infringement warranty
- [ ] Disclaimer of all other warranties — "AS IS" disclaimers overly broad? 🟡
- [ ] Virus/malware warranty
- [ ] Compliance with laws warranty

**I. Termination**
- [ ] Termination for convenience — notice period? fees payable?
- [ ] Termination for cause — cure period defined? (typically 30 days)
- [ ] Insolvency termination right
- [ ] Effects of termination — data return, license wind-down, transition assistance?
- [ ] Auto-renewal with inadequate notice period 🔴

**J. Dispute Resolution**
- [ ] Jurisdiction clause — mandatory exclusive? matches governing law? enforceable?
- [ ] Arbitration vs. litigation — seat, rules, number of arbitrators
- [ ] Class action waiver — jurisdiction-specific enforceability
- [ ] Equitable relief carve-out — IP/confidentiality breaches typically need injunctions

**K. Force Majeure**
- [ ] Cyber attacks / ransomware — included or excluded? 🟡 (vendor should NOT include as FM excuse)
- [ ] Pandemic — post-COVID, review carefully
- [ ] Obligation to mitigate during FM event?
- [ ] Customer right to terminate if FM exceeds threshold period?

**L. Miscellaneous / Boilerplate**
- [ ] Entire agreement / integration clause — are all prior commitments captured?
- [ ] Amendment procedure — written only? email sufficient?
- [ ] Assignment — can vendor assign to acquirer without consent? 🔴
- [ ] Waiver — non-waiver clause present?
- [ ] Severability — does it include reconstruction obligation?
- [ ] Notices — physical + email; effective when received or sent?

---

### Step 4 — Suspicious Clause Detection (Sus Flags)

**Always flag and redline these patterns:**

#### 🔴 Critical Sus Patterns

| Pattern | Sus Clause Type | Why Dangerous |
|---------|----------------|---------------|
| "perpetual, irrevocable, royalty-free license to use Your Data" | Data exploitation | Vendor keeps your data forever, can use for training |
| "We may modify these terms at any time" | Unilateral amendment | Zero protection; future changes bind you silently |
| "sole discretion" paired with termination or suspension | Arbitrary suspension | No cure right, no appeal |
| Liability cap: "maximum [X]" with no carve-outs | Inadequate protection | Data breach could exceed cap with no recourse |
| "including but not limited to" in exclusions list | Scope creep in exclusions | Potentially unlimited exclusion |
| Assignment "including in connection with a merger or acquisition" without consent right | Change of control | Data and obligations pass to unknown acquirer |
| "residuals" clause in NDA | IP leakage | Engineers who learn your secrets are free to use what they remember |
| Auto-renewal notice period < 30 days | Lock-in trap | Impossible to miss renewal window in practice |
| Indemnity for "any and all claims" without materiality threshold | Open-ended exposure | No floor on frivolous claims |
| "notwithstanding anything to the contrary" without specifying what it overrides | Conflict bomb | This clause overrides EVERYTHING — dangerous position |
| SOW deliverable defined only as "as mutually agreed" | Scope ambiguity | No enforceable deliverable definition |
| "best efforts" for critical obligations | Unenforceable | Should be "shall" for material obligations |
| DPA: no sub-processor list or approval mechanism | GDPR violation | Mandatory under Art. 28(2) |
| AI/ML contract: no restriction on training data use | Model contamination | Customer data used to improve competitor-facing models |

---

### Step 5 — Redlining Output

For each 🔴 and 🟡 clause, produce:

```
CLAUSE: [Section X.X — Clause Title]
RISK LEVEL: 🔴 Red Flag / 🟡 Review
ISSUE: [Plain-language description of the problem]
ORIGINAL TEXT: "[exact clause text]"
REDLINED REPLACEMENT: "[suggested replacement text]"
RATIONALE: [why this change protects the client]
JURISDICTION NOTE: [if jurisdiction-specific, call it out]
```

---

### Step 6 — Active Research (Web Search Integration)

When reviewing:
- Look up **current regulatory requirements** for identified jurisdiction (GDPR, DPDP Act, CCPA updates)
- Search for **case law** on specific clause types if jurisdiction is identified
- Check if **DPA adequacy decisions** are current for cross-border data transfers
- Verify **Anthropic's current DPA template** against contract if reviewing a vendor DPA
- Research **industry standard benchmarks** for liability caps in SaaS/AI contracts

Use web search for:
- "GDPR adequacy decision [country] 2024"
- "India DPDP Act 2023 requirements DPA"
- "standard SaaS liability cap benchmark"
- "CCPA amendment [year] requirements"

---

### Step 7 — Contract Summary Output

After full review, produce structured summary:

```
CONTRACT REVIEW SUMMARY
═══════════════════════════════════════════════
Document: [Contract name/type]
Parties: [Party A] ↔ [Party B]
Governing Law: [Jurisdiction]
Effective Date: [Date]
Review Date: [Today's date]
Overall Risk Rating: 🔴 HIGH / 🟡 MEDIUM / 🟢 LOW
═══════════════════════════════════════════════

CRITICAL ISSUES (must fix before signing):
1. [Issue description + section reference]
2. ...

RECOMMENDED CHANGES (negotiate if possible):
1. [Issue description + section reference]
2. ...

MISSING PROTECTIONS (add these clauses):
1. [Missing clause description]
2. ...

JURISDICTION ALERTS:
- [Any mandatory law conflicts]

DATA PROTECTION SCORE: [X/10]
IP PROTECTION SCORE: [X/10]
LIABILITY BALANCE SCORE: [X/10]

RECOMMENDATION: ✅ Acceptable / ⚠️ Negotiate First / 🚫 Do Not Sign
═══════════════════════════════════════════════
```

---

## Contract Type Deep-Dives

### MSA (Master Services Agreement)
Key principle: MSA sets the legal framework; SOWs execute under it. Watch for:
- SOW prevails over MSA conflict — or vice versa? (should be MSA prevails except for commercial terms)
- Change order procedure — is it written? timeline for approval?
- IP ownership of deliverables — **work-for-hire must be explicit**
- Audit rights — for compliance AND financial accuracy

### DPA (Data Processing Agreement)
GDPR Art. 28 mandatory elements — ALL must be present:
- Subject matter, nature, purpose, type of data, categories of data subjects
- Duration of processing
- Obligations and rights of controller
- Sub-processor approval and obligations
- Data return or deletion on termination
- Cooperation with supervisory authority
- Security measures (Art. 32 reference)

For India DPDP Act 2023:
- "Data Fiduciary" (controller) vs. "Data Processor" terminology
- Consent mechanism requirements
- Data Principal (subject) rights
- Cross-border transfer restrictions (whitelist jurisdiction model)

### SOW (Statement of Work)
Golden rule: if it is not written, it is not in scope. Flag:
- Deliverables defined in functional terms, not technical specs
- Acceptance criteria: **must be objective, measurable, time-bound**
- Deemed acceptance after X days without objection — flag period length
- Change management: no written change order = no scope change (protect this)
- Payment tied to milestones vs. calendar — milestone preferred

### LOE (Letter of Engagement)
Simpler than MSA but same IP and liability risks. Watch:
- Professional liability — is it capped? At what?
- Engagement scope — is it specific enough to avoid later disputes?
- Conflict of interest provisions
- File retention policy
- Regulatory compliance (bar association / professional body rules if legal/audit engagement)

---

## Red Lines (Non-Negotiable for Anthropic-Context Contracts)

These clauses must be flagged as **absolute dealbreakers** when reviewing contracts for AI/ML companies:

1. **Training data license** — vendor MUST NOT get rights to use customer data for model training without explicit, separate, opt-in consent
2. **Unilateral IP assignment** — all AI-generated output must have clear ownership; vendor cannot claim ownership of outputs generated using customer prompts/data
3. **Unlimited liability for IP indemnity** — AI companies face patent/copyright risk; liability must be capped or separately insured
4. **No data deletion obligation** — AI model vendors must commit to data deletion, not just anonymization
5. **Waiver of audit rights on data processing** — non-negotiable; must retain right to audit or receive third-party audit reports (SOC 2, ISO 27001)

---

## Output Formats

| Situation | Output Format |
|-----------|--------------|
| Quick question ("is this clause ok?") | Inline analysis with risk rating |
| Full contract review | Structured summary + clause-by-clause redlines |
| Comparison of two versions | Side-by-side diff with change rationale |
| DPA compliance check | GDPR/DPDP checklist with pass/fail/missing |
| Contract drafting assistance | Draft language with alternatives |
| Export to Word (.docx) | Use docx skill — redlines as tracked changes |

---

## Important Disclaimers (Always Include in Output)

> ⚠️ **This analysis is AI-generated legal guidance, not legal advice.** Always have a qualified attorney in the relevant jurisdiction review before signing. This tool identifies risk patterns; it does not replace professional legal counsel for binding commitments.
