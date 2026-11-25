---
name: write-rfp
description: Writes a request for proposal with background, scope, numbered requirements, response format, weighted evaluation criteria and timeline, so vendor answers are comparable. Use before inviting bids.
license: CC0-1.0
metadata:
  version: 1.0.0
  kind: prompt
  category: operations
  source: https://hermes-ide.com/prompts/write-rfp
  catalog: 2026.1014.1
---

# Write a request for proposal

## Inputs

- [PROJECT] (required): What you need and why - organisation background, the problem, goals, budget range if you will share it, and who the buyer is.
- [REQUIREMENTS] (required): Your requirements, in any form - functional needs, volumes, service levels, security, integration, legal or compliance needs. Mark the non-negotiable ones if you can.
- [DEADLINE] (optional): When proposals are due or when the work must start, for example "proposals by 15 March, go-live by 1 June".

Take each value from the invocation or the user’s message. If a required value is missing, ask for it once.

<context>
You write RFPs that get comparable, honest proposals. Vendors answer what you ask, so the RFP must state the problem clearly, separate mandatory from desirable requirements, tell vendors exactly how to structure their response and pricing, and say how proposals will be judged. You describe needs and outcomes, never one vendor's product, so the process stays fair and competitive.
</context>

<task>
Write an RFP for:

<project>
[PROJECT]
</project>

<requirements>
[REQUIREMENTS]
</requirements>

Deadline: [DEADLINE]

1. Introduction and background: who the buyer is, the situation, and why they are going to market now. Keep confidential details out unless the input clearly allows them.
2. Objectives: three to five outcomes the buyer wants, measurable where possible.
3. Scope of work: what is in scope, what is out of scope, and the deliverables.
4. Requirements: rewrite the input as numbered, testable requirements (R1, R2…), each labelled `Mandatory` or `Desirable`, grouped by theme (functional, service levels, security and data, integration, support and training, legal and compliance). Each must be a single, checkable statement. Ask vendors to answer every requirement with `Meets`, `Partially meets` or `Does not meet` plus an explanation.
5. Proposal format: required sections, page limit, and a structured pricing template (one-off costs, recurring costs, unit rates, assumptions, price validity) so prices can be compared like for like.
6. Evaluation criteria with weights summing to 100, and the statement that failing any mandatory requirement disqualifies a proposal.
7. Timeline: issue date, deadline for vendor questions, answers to questions, proposal due date, shortlist and demos, decision, contract start. Work back from the given deadline; if none was given, propose a realistic schedule (typically three to six weeks for responses) as `[CONFIRM]`.
8. Commercial terms and submission: contract type, key terms the buyer expects, confidentiality, how and where to submit, single point of contact (as a placeholder).
9. Open items: everything you had to leave as a placeholder.
</task>

<constraints>
- Do not name or describe a specific vendor's product in requirements.
- Do not invent budgets, legal clauses, certifications or dates. Use `[CONFIRM: …]` placeholders and list them under Open items.
- Requirements must be testable: replace vague words ("user-friendly", "fast", "robust") with measurable statements or flag them for the buyer to quantify.
- Recommend that the buyer's legal or procurement team review the final RFP and contract terms, in one line in Open items.
</constraints>

<output_format>
A Markdown document titled `Request for Proposal: <project name>` with the sections in this order: Introduction, Background, Objectives, Scope of work, Requirements (table: ID | Requirement | Mandatory or Desirable), Proposal format (including the pricing template as a table), Evaluation criteria (table: Criterion | Weight), Timeline (table: Milestone | Date), Commercial terms, Submission and contact, Open items (checklist).
</output_format>
