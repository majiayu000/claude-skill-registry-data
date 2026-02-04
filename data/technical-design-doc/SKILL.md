---
name: "technical-design-doc"
description: "Generates clear technical design documents with architecture, trade-offs, and rollout plans."
---

# Technical Design Document Creator

## Purpose

Use this skill to create design docs that:

- Align stakeholders on what is being built and why.
- Capture architecture and trade-offs explicitly.
- Provide a durable reference for implementation and future changes.

---

## When to Use

- Cross-team or cross-service changes.
- New user-facing features with non-trivial backend impact.
- Data model changes, migrations, and new storage systems.
- Major performance, reliability, or security projects.

---

## Design Doc Structure

A good design doc should cover:

1. **Overview**

   - One-paragraph summary of the problem and proposed solution.
   - Expected impact at a high level.

2. **Background and Context**

   - Current behavior and pain points.
   - Relevant metrics, incidents, or user feedback.
   - Links to prior designs or ADRs.

3. **Goals and Non-Goals**

   - Goals: What success looks like.
   - Non-goals: Explicitly out-of-scope aspects to prevent scope creep.

4. **Requirements and Constraints**

   - Functional requirements.
   - Non-functional: performance, availability, security, privacy, compliance, cost, deadlines.

5. **Proposed Solution**

   - Architecture diagrams and component overviews.
   - Data flow and control flow (sequence diagrams where useful).
   - Key algorithms or logic at a high level.

6. **Alternatives Considered**

   - Briefly describe 2–3 options and why they were rejected.
   - Include “do nothing” when relevant.

7. **Impact Analysis**

   - On existing systems, APIs, clients, and data.
   - Operational impact: on-call, runbooks, observability.
   - Risks and mitigations.

8. **Testing and Validation**

   - Unit, integration, and end-to-end testing strategy.
   - Load/performance testing plans.
   - Rollback and failure drills, if applicable.

9. **Rollout Plan**

   - Milestones and phases.
   - Feature flagging or staged rollout strategy.
   - Monitoring during rollout; success criteria.

10. **Open Questions and Future Work**

    - Areas needing further exploration.
    - Potential follow-ups that are explicitly out of the current scope.

---

## Usage Guidance

- Optimize for clarity over completeness. If a section is not applicable, say why.
- Draw diagrams where they clarify non-trivial flows or boundaries.
- Keep the document living: update when significant decisions or constraints change.

---

## Examples of Good Prompts

- “Create a full design doc using this template for the following feature description.”
- “Given this high-level idea, flesh it out into a design doc with at least two alternative solutions.”
- “Review this existing design doc using the template; identify missing sections and key risks.”
