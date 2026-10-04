---
description: Document a legal decision with rationale and risk acceptance
---

# Decision Memo

Document a legal decision for "$ARGUMENTS". Record the decision question, alternatives considered, rationale, accepted risks, and conditions for future review.

> **Note:** AI-generated legal content does not constitute legal advice. Consult a qualified attorney for decisions with significant legal exposure.

## Prerequisites

None — this is a utility skill.

## Process

1. **State the decision question clearly:**
   - Frame the question as a specific, answerable decision (e.g., "Should we include an arbitration clause or allow litigation?" not "What should we do about disputes?")
   - Scope the decision to a single, well-defined choice

2. **Document context and constraints:**
   - Business context driving the need for a decision
   - Legal constraints (regulatory requirements, contractual obligations, precedent)
   - Timeline and urgency factors
   - Budget or resource constraints that limit options

3. **List alternatives considered:**
   - Document a minimum of 2-3 alternatives
   - For each alternative, provide:
     - **Description** — what this option entails
     - **Pros** — benefits and advantages
     - **Cons** — drawbacks and risks
     - **Legal risk level** — Low/Medium/High
     - **Cost/effort estimate** — relative cost or effort to implement

4. **Record the final decision and rationale:**
   - State the chosen option clearly
   - Explain why this option was selected over the others
   - Reference specific pros that were decisive
   - Acknowledge specific cons that were accepted as trade-offs

5. **Document accepted risk:**
   - What could go wrong with this decision
   - Likelihood of negative outcomes (Low/Medium/High)
   - Potential impact if negative outcomes materialize
   - Any mitigating factors or safeguards in place

6. **Record decision metadata:**
   - Who made or approved the decision
   - Date of the decision
   - Stakeholders consulted
   - Any dissenting opinions or concerns raised

7. **Define review and revisit conditions:**
   - Specific triggers that would require reconsideration (e.g., regulatory change, threshold breach, contract renewal)
   - Scheduled review date if applicable
   - Metrics or indicators to monitor

8. **Tag with relevant legal area:**
   - Contracts, Privacy, Intellectual Property, Employment, Compliance, Corporate, Litigation, Regulatory, or other applicable area

9. **Write the artifact** by appending to `.metapowers/legal/$ARGUMENTS/decision-log.md`:
   - If the file does not exist, create it with frontmatter:

     ```
     ---
     description: Legal decision log for $ARGUMENTS
     ---
     ```

   - Append a new decision entry with a horizontal rule separator (`---`) between entries
   - Each entry includes:
     - **Decision ID** — sequential number (e.g., DEC-001)
     - **Date** — date of the decision
     - **Decision Question** — the question being decided
     - **Context and Constraints** — factors driving the decision
     - **Alternatives Considered** — each alternative with pros, cons, and risk level
     - **Decision** — the chosen option
     - **Rationale** — why this option was selected
     - **Accepted Risk** — risks acknowledged with likelihood and impact
     - **Decision Maker(s)** — who made or approved the decision
     - **Legal Area** — tagged category
     - **Review Conditions** — triggers for reconsideration

## Output

The decision memo appended to `.metapowers/legal/$ARGUMENTS/decision-log.md`. Present a summary to the user highlighting:
- The decision question and chosen option
- Key rationale points
- Primary risks accepted and their mitigation
- When the decision should be revisited
