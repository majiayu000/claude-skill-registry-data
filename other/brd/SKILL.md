---
name: brd
owner: baseline
description: Draft a Business Requirements Document (BRD) for cross-functional or stakeholder-heavy work that needs more structure than an intake. Use after `/intake` when the request spans multiple systems/teams, carries regulatory weight, or needs formal sign-off. Output lives at `docs/brd/<slug>.md`.
disable-model-invocation: true
---

# BRD — Business Requirements Document

You are drafting a BRD. BRDs are heavier than intakes — they exist when a request needs explicit sign-off from named business stakeholders, and when the **why** and the **what** must survive independently of the **how** (the spec).

**Use a BRD when:**
- Multiple teams or external stakeholders need to align.
- Regulatory, legal, or compliance concerns shape the requirements.
- Business milestones or contractual dates are tied to the work.
- Budget or headcount implications warrant an approved scope.

**Don't use a BRD for:** single-team feature work, quickfixes, or internal refactors. Those need an intake + spec, nothing more.

## Prerequisite

Either `/intake` has completed (there's a corresponding `docs/intake/<slug>.md`), OR the user is starting directly at BRD because the intake exists upstream (e.g., in Linear/Jira) and they want to formalize it here.

## Inputs

- The intake document (if any) — it supplies **Problem** and **Goal**.
- The user's additional context about stakeholders, timelines, and compliance.
- `template.md` in this skill directory.

## Steps

1. If a corresponding intake exists at `docs/intake/<slug>.md`, read it. Map **Problem → Business objective** and **Goal → Executive summary**.
2. Read `template.md`. Every heading must appear in the output.
3. For each section, write content that answers the questions in the template comments. If unknown, list the gap under **Open questions** — never fabricate stakeholder names, dates, or dollar amounts.
4. Name every requirement with an ID: `BR-001`, `BR-002`, … for business reqs; `FR-001`, … for functional; `NFR-001`, … for non-functional. Downstream spec AC will reference these IDs.
5. Write to `docs/brd/<slug>.md` (same slug as the intake, if one exists).
6. Tell the user: "BRD drafted at `docs/brd/<slug>.md`. Sign-offs required from: <list>. Open questions: N. Next: `/scout` (or get sign-offs first if you want to freeze scope)."

## Drafting rules

- **Requirements are testable, not aspirational.** "The system shall support peak traffic" is aspirational. "The system shall sustain 500 RPS with P95 < 200ms" is testable.
- **Separate business from functional from non-functional.** A mixed list becomes unactionable.
- **Risks must have owners.** "Risk: the vendor API could change" with no owner is noise. Either name who monitors it or delete it.
- **Sign-offs are names, not titles.** "Head of Compliance" can't sign — their replacement, who is a specific person, can.
- **Do not write the solution.** The BRD says what must be true; the spec says how. If you catch yourself writing "we'll use Kafka", stop — that belongs in `/spec`.
