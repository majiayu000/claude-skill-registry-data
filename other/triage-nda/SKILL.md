---
name: triage-nda
description: Rapidly triage an incoming NDA and classify it as GREEN (standard approval), YELLOW (counsel review), or RED (full legal review). Use when a new NDA arrives from sales or business development, when screening for embedded non-solicits, non-competes, or missing carveouts, or when deciding whether an NDA can be signed under standard delegation.
argument-hint: "<NDA file or text>"
---

# /triage-nda -- NDA Pre-Screening

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Triage the NDA: @$1

Rapidly triage incoming NDAs against standard screening criteria. Classify the NDA for routing: standard approval, counsel review, or full legal review.

**Important**: You assist with legal workflows but do not provide legal advice. All analysis should be reviewed by qualified legal professionals before being relied upon.

## Workflow

### Step 1: Accept the NDA

Accept the NDA in any format:
- **File upload**: PDF, DOCX, or other document format
- **URL**: Link to the NDA in a document system
- **Pasted text**: NDA text pasted directly

### Step 2: Load NDA Playbook

Look for NDA screening criteria in local settings (e.g., `legal.local.md`).

**If no NDA playbook is configured:**
- Proceed with reasonable market-standard defaults
- Defaults applied:
  - Mutual obligations required (unless the organization is only disclosing)
  - Term: 2-3 years standard, up to 5 years for trade secrets
  - Standard carveouts required: independently developed, publicly available, rightfully received from third party, required by law
  - No non-solicitation or non-compete provisions
  - No residuals clause (or narrowly scoped if present)
  - Governing law in a reasonable commercial jurisdiction

### Step 3: Quick Screen

Evaluate the NDA against each screening criterion:

#### 1. Agreement Structure
- Type identified: Mutual NDA, Unilateral (disclosing party), or Unilateral (receiving party)
- Appropriate for context
- Standalone agreement (not embedded in larger commercial agreement)

#### 2. Definition of Confidential Information
- Reasonable scope
- Marking requirements workable
- Exclusions present
- No problematic inclusions

#### 3. Obligations of Receiving Party
- Standard of care: Reasonable care
- Use restriction: Limited to stated purpose
- Disclosure restriction: Limited to need-to-know
- No onerous obligations

#### 4. Standard Carveouts
All of the following should be present:
- Public knowledge
- Prior possession
- Independent development
- Third-party receipt
- Legal compulsion

#### 5. Permitted Disclosures
- Employees, contractors/advisors, affiliates, legal/regulatory

#### 6. Term and Duration
- Agreement term: 1-3 years standard
- Confidentiality survival: 2-5 years standard
- Not perpetual

#### 7. Return and Destruction
- Obligation triggered on termination or request
- Retention exception for legal/compliance
- Certification reasonable (not sworn affidavit)

#### 8. Remedies
- Injunctive relief acknowledgment is standard
- No pre-determined damages
- Not one-sided

#### 9. Problematic Provisions to Flag
- No non-solicitation
- No non-compete
- No exclusivity
- No standstill
- No residuals clause (or narrowly scoped)
- No IP assignment or license
- No audit rights

#### 10. Governing Law and Jurisdiction
- Reasonable jurisdiction
- Consistent governing law and jurisdiction
- No mandatory arbitration

### Step 4: Classify

#### GREEN -- Standard Approval
All standard criteria met. No problematic provisions.
**Action**: Approve via standard delegation of authority.

#### YELLOW -- Counsel Review Needed
Minor deviations present but NDA not fundamentally problematic.
**Action**: Counsel can likely resolve in a single review pass.

#### RED -- Significant Issues
Critical issues present (missing carveouts, non-compete, IP assignment, etc.).
**Action**: Do not sign; requires negotiation or counterproposal.

### Step 5: Generate Triage Report

```
## NDA Triage Report

**Classification**: [GREEN / YELLOW / RED]
**Parties**: [party names]
**Type**: [Mutual / Unilateral]
**Term**: [duration]
**Governing Law**: [jurisdiction]

## Screening Results

| Criterion | Status | Notes |
|-----------|--------|-------|
| Mutual Obligations | [PASS/FLAG/FAIL] | [details] |
| Definition Scope | [PASS/FLAG/FAIL] | [details] |
| Standard Carveouts | [PASS/FLAG/FAIL] | [details] |
| [etc.] | | |

## Issues Found
### [Issue -- YELLOW/RED]
**What**: [description]
**Risk**: [what could go wrong]
**Suggested Fix**: [specific language or approach]

## Recommendation
[Specific next step]
```

## Common NDA Issues and Standard Positions

### Overbroad Definition of Confidential Information
**Standard position**: Limited to non-public information disclosed in connection with stated purpose.

### Missing Independent Development Carveout
**Risk**: Could create claims that internally-developed products were derived from counterparty's confidential information.

### Non-Solicitation of Employees
**Standard position**: Does not belong in NDAs. If insisted upon, limit to targeted solicitation with short term (12 months).

### Broad Residuals Clause
**Standard position**: Resist. If required, limit to unaided memory, exclude trade secrets and patents.

### Perpetual Confidentiality Obligation
**Standard position**: 2-5 years. Trade secrets may warrant longer protection.
