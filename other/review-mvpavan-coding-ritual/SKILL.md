---
name: review
description: Use for a critic review of any artifact, a substantive review of code or of a spec or plan, or to verify and act on review findings. Skip routine final diff inspection; to interrogate the author instead, use grilling.
---

# Review

Routine final diff inspection follows AGENTS.md without requiring this workflow.

## Critic review

A critic is an independent reviewer, never the author; the user chooses its model.
Give a thorough opinion, then every finding with its severity and supporting
evidence; for code, cite `file:line`. The coordinator filters by severity afterward.
`APPROVE` means no open BLOCKER or MAJOR; otherwise `REVISE`. APPROVE covers only
what was verified; list unverified requirements, never approve them. For a
non-code artifact, the critic receives the artifact and its purpose.

## Severity

Severity follows consequence: BLOCKER for severe safety/data-loss or operational
failure; MAJOR for acceptance or correctness issues blocking trust; MINOR for
nonblocking improvements. Preference alone is not a finding. When the plan or
brief mandates what this review calls a defect, report it as MAJOR, labelled
plan-mandated; the user decides.

## Select a mode

- Code (`inline`, `spec`, `quality`, `re-review`): `references/code.md`; dispatched
  reviewers and structured re-reviews also use `references/review-contract.md`.
- Document (a spec or plan): *Document review* below.
- `feedback`: verify and act on incoming findings within authorization, using
  `references/feedback.md`. Producing a review is read-only, whereas applying
  feedback requires implementation authority.

## Document review

Check the document against current repository context and authoritative project
docs for internal inconsistency, missing constraints, unverifiable claims, scope
bloat, missing tests or verification, and relevant security, data or performance
risks. Report findings; edit the document only when the requester asked for fixes
to be applied, and then only unambiguous wording or structure. Surface
decision-level issues instead of rewriting intent.
