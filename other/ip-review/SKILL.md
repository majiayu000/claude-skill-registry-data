---
description: Review intellectual property assignments, licenses, and ownership
---

# IP Review

Review intellectual property provisions for "$ARGUMENTS". Analyze ownership structures, license grants, assignment provisions, and open-source implications to identify IP-related risks and traps.

> **Note:** AI-generated legal content does not constitute legal advice. Consult a qualified attorney.

## Prerequisites

Check that `.metapowers/legal/$ARGUMENTS/00-assess.md` exists. If it does not exist, stop and tell the user:

> "Run an Assess skill first (e.g. `/legal:risk-assessment $ARGUMENTS`) to generate the prerequisite assessment artifact."

If the user passes `--skip-checks`, bypass this check and log the skip to `.metapowers/legal/$ARGUMENTS/skip-log.md` with a timestamp and the reason "Prerequisite check skipped for ip-review".

## Process

1. **Read inputs:**
   - Read `.metapowers/legal/$ARGUMENTS/00-assess.md` for risk and jurisdiction context
   - Read IP-related provisions from the document provided by the user

2. **Analyze ownership structure:**
   - **Background IP** — pre-existing IP each party brings to the relationship
   - **Foreground IP** — IP created during the engagement
   - **Joint IP** — IP created collaboratively (ownership, licensing, and exploitation rights)
   - Verify clear delineation between background and foreground IP

3. **Review work-for-hire vs. assignment provisions:**
   - Does the relationship qualify for work-for-hire under applicable law?
   - If assignment is used, is it present assignment ("hereby assigns") or future obligation?
   - Are moral rights addressed (waiver or retention)?
   - Is consideration adequate for the scope of assignment?

4. **Analyze license grants:**
   - **Scope** — what IP is licensed and for what purpose
   - **Exclusivity** — exclusive vs. non-exclusive
   - **Sublicensing** — right to sublicense and any restrictions
   - **Territory** — geographic scope of the license
   - **Duration** — term of the license (fixed, perpetual, tied to agreement)
   - **Revocability** — can the license be revoked and under what conditions

5. **Assess open-source implications:**
   - Do any open-source licenses conflict with IP assignment or exclusivity?
   - Are there copyleft obligations that could affect proprietary code?
   - Is there an open-source usage policy referenced or required?
   - Check for license compatibility between open-source components

6. **Evaluate freedom to operate:**
   - Can each party continue its business without infringing on rights granted?
   - Are there restrictions that limit future product development?
   - Do non-compete or non-solicit provisions affect IP exploitation?

7. **Review invention disclosure obligations:**
   - Are there obligations to disclose inventions created during the engagement?
   - What is the scope of disclosure (only related inventions or all inventions)?
   - Are there time-limited obligations that extend beyond the agreement?

8. **Flag common IP traps:**
   - Overly broad assignment (all IP, not just project-related)
   - Missing background IP carve-out (existing IP inadvertently assigned)
   - Perpetual irrevocable licenses without adequate consideration
   - Ambiguous ownership of derivative works
   - No license-back for assigned IP needed in ongoing operations
   - IP representations without adequate knowledge qualifiers

9. **Write the artifact** to `.metapowers/legal/$ARGUMENTS/02-review.md` with frontmatter:

   ```
   ---
   description: IP review for $ARGUMENTS
   ---
   ```

   Include sections:
   - **Ownership Analysis** — background IP, foreground IP, and joint IP breakdown
   - **Assignment and Work-for-Hire** — structure, adequacy, and moral rights
   - **License Grant Summary** — scope, exclusivity, territory, duration per license
   - **Open-Source Assessment** — compatibility analysis and copyleft risks
   - **Freedom to Operate** — impact on each party's ongoing business
   - **Invention Disclosure** — obligations and scope
   - **IP Traps Identified** — flagged issues with risk explanation
   - **Recommendations** — specific actions to mitigate IP risks

## Output

The IP review written to `.metapowers/legal/$ARGUMENTS/02-review.md`. Present a summary to the user highlighting:
- Ownership structure (who owns what, and is it clearly defined?)
- IP traps identified and their severity
- Open-source compatibility concerns
- Top recommendations for IP protection
