---
description: Validate the top solution and produce actionable recommendations with evidence
---

# Deliver

Converge on the final recommendation for "$ARGUMENTS". Validate the top solution concept(s) with evidence, refine the approach, and produce actionable recommendations.

## Prerequisites

Read `.metapowers/research/$ARGUMENTS/01-discover.md`, `.metapowers/research/$ARGUMENTS/02-define.md`, and `.metapowers/research/$ARGUMENTS/03-design.md`.

If `03-design.md` does not exist, tell the user:

> Phase 3 (Design) has not been completed for "$ARGUMENTS". Run `/research:design $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check and log to `.metapowers/research/$ARGUMENTS/skip-log.md`.

## Process

1. **Read all prior artifacts:**
   - Read `.metapowers/research/$ARGUMENTS/01-discover.md` for original research
   - Read `.metapowers/research/$ARGUMENTS/02-define.md` for problem statement and success criteria
   - Read `.metapowers/research/$ARGUMENTS/03-design.md` for recommended solutions and validation plan

2. **Validate the top solution(s):**
   - Use WebSearch to find evidence supporting or contradicting the recommended approach
   - Use WebFetch to read detailed case studies of similar implementations
   - Look for: success stories, failure modes, edge cases, unintended consequences
   - Test each assumption identified in the Design phase

3. **Assess against success criteria:**
   - Review each success criterion from the Define phase
   - For each criterion, document evidence that the solution meets it (or doesn't)
   - Flag any criteria that can't be validated with desk research alone

4. **Refine recommendations:**
   - Adjust the solution based on validation findings
   - Add implementation considerations discovered during validation
   - Identify quick wins vs. long-term investments
   - Note dependencies and prerequisites

5. **Write the artifact** to `.metapowers/research/$ARGUMENTS/04-deliver.md` with sections:
   - **Executive Summary** — one-paragraph recommendation
   - **Validation Findings** — evidence for/against the solution, organized by assumption
   - **Success Criteria Assessment** — each criterion with evidence status
   - **Final Recommendation** — refined solution with implementation approach
   - **Action Items** — prioritized next steps with owners/timelines if applicable
   - **Risks & Mitigations** — remaining risks and how to handle them
   - **Research Journey** — brief timeline of what was discovered across all 4 phases

## Output

The final deliverable written to `.metapowers/research/$ARGUMENTS/04-deliver.md`. Present a summary to the user highlighting:
- The final recommendation (1-2 sentences)
- Confidence level based on evidence strength
- Top 3 action items
- Key risks to watch
