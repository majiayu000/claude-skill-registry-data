---
description: Audit current legal posture — identify gaps in policies, contracts, and compliance
---

# Legal Audit

Conduct a comprehensive legal audit of "$ARGUMENTS". Inventory existing legal documents, check them against industry standards, and identify gaps requiring remediation.

> **Note:** AI-generated legal content does not constitute legal advice. Consult a qualified attorney.

## Prerequisites

None — this is a Phase 0 Assess skill.

## Process

1. **Inventory existing legal documents:**
   - Contracts (customer, vendor, partner, employment)
   - Policies (privacy policy, acceptable use, data retention, security)
   - Terms of service and end-user license agreements
   - Compliance documentation and certifications
   - Corporate governance documents

2. **Check each against industry standards:**
   - Read `plugins/legal/shared/compliance-checklist.md` for reference
   - Compare document coverage against standard legal frameworks
   - Verify documents are current (not expired or outdated)
   - Check for internal consistency across documents

3. **Identify gaps:**
   - Missing policies that should exist for the business type
   - Expired or outdated contracts requiring renewal
   - Non-compliant documents that fail to meet regulatory requirements
   - Incomplete coverage areas (e.g., no data processing agreements)

4. **Categorize gaps by severity and urgency:**
   - **Critical** — immediate legal exposure or regulatory violation
   - **High** — significant risk if not addressed within 30 days
   - **Medium** — should be addressed within 90 days
   - **Low** — improvement opportunity, no immediate risk

5. **Prioritize remediation:**
   - Rank gaps by severity x urgency
   - Estimate effort for each remediation item
   - Identify quick wins vs. long-term projects
   - Recommend sequencing of remediation work

6. **Write the artifact** to `.metapowers/legal/$ARGUMENTS/00-assess.md` with heading:

   ## Legal Audit

   Include sections:
   - **Document Inventory** — all existing legal documents cataloged
   - **Standards Comparison** — how each document measures against benchmarks
   - **Gap Analysis** — missing, expired, or non-compliant items
   - **Severity Matrix** — gaps categorized by severity and urgency
   - **Remediation Priorities** — ordered action items with effort estimates

## Output

The legal audit written to `.metapowers/legal/$ARGUMENTS/00-assess.md`. Present a summary to the user highlighting:
- Total documents inventoried vs. gaps found
- Critical and high-severity items requiring immediate attention
- Top 3 recommended remediation actions
