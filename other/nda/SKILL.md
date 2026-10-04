---
description: Generate Non-Disclosure Agreement (mutual or one-way)
---

# Non-Disclosure Agreement

Generate a Non-Disclosure Agreement for "$ARGUMENTS". Produce a comprehensive NDA tailored to the parties, relationship type, and confidentiality needs.

> **Note:** AI-generated legal content does not constitute legal advice. Consult a qualified attorney.

## Prerequisites

Check that `.metapowers/legal/$ARGUMENTS/00-assess.md` exists. If it does not exist, stop and tell the user:

> "Run an Assess skill first (e.g. `/legal:risk-assessment $ARGUMENTS`) to generate the prerequisite assessment artifact."

If the user passes `--skip-checks`, bypass this check and log the skip to `.metapowers/legal/$ARGUMENTS/skip-log.md` with a timestamp and the reason "Prerequisite check skipped for nda".

## Process

1. **Read inputs:**
   - Read `.metapowers/legal/$ARGUMENTS/00-assess.md` for context on parties and risk profile
   - Read `plugins/legal/shared/contract-template.md` for standard contract provisions

2. **Determine NDA type:**
   - **Mutual (bilateral)** — both parties share confidential information
   - **One-way (unilateral)** — only one party discloses confidential information
   - Identify the disclosing and receiving parties

3. **Define parties:**
   - Full legal names and entity types
   - Jurisdictions of incorporation
   - Principal business addresses
   - Authorized signatories

4. **Draft the following sections:**

   - **Definition of Confidential Information** — broad definition with specific examples relevant to the business context (technical data, business plans, customer lists, financial information, trade secrets, product roadmaps, source code, algorithms, etc.)
   - **Exclusions from Confidential Information** — standard exclusions:
     - Information in the public domain (not through breach)
     - Information independently developed without use of confidential information
     - Information already known to the receiving party prior to disclosure
     - Information received from a third party without restriction
     - Information required to be disclosed by law or court order (with notice obligations)
   - **Permitted Use and Disclosure** — scope of permitted use (evaluation, negotiation, specific project), permitted recipients (employees, advisors, contractors with need-to-know)
   - **Obligations of Receiving Party** — duty of care (at least same as own confidential information, but no less than reasonable care), security measures, marking requirements, access limitations
   - **Term of Agreement and Survival Period** — agreement duration (typically 1-3 years), survival of confidentiality obligations beyond termination (typically 2-5 years, indefinite for trade secrets)
   - **Return or Destruction of Information** — obligation to return or certify destruction upon request or termination, exception for legally required archival copies
   - **Remedies** — acknowledgment that breach may cause irreparable harm, right to seek injunctive relief without posting bond (where permitted), right to recover attorneys' fees
   - **Governing Law** — choice of law, jurisdiction for disputes, venue selection

5. **Include standard provisions from contract template:**
   - No implied license or IP transfer
   - No obligation to complete a transaction
   - Relationship of parties (no partnership, agency, or joint venture)
   - Assignment restrictions
   - Severability
   - Entire agreement
   - Counterparts and electronic signatures
   - Amendment requirements (written, signed by both parties)

6. **Write the artifact** to `.metapowers/legal/$ARGUMENTS/01-draft.md` with frontmatter:

   ```
   ---
   description: Non-Disclosure Agreement draft for $ARGUMENTS
   ---
   ```

## Output

The NDA draft written to `.metapowers/legal/$ARGUMENTS/01-draft.md`. Present a summary to the user highlighting:
- NDA type (mutual or one-way)
- Parties identified
- Term and survival period
- Key protections included
- Areas flagged for attorney review
