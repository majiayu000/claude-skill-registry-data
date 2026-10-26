---
name: business-analysis
description: Use when turning a user request into acceptance criteria — eliciting requirements, checking docs/INDEX.md for existing logic, writing Given-When-Then criteria for the architect.
---

# Business Analysis

## Read first

- **Always read `docs/INDEX.md` before drafting anything.** Find and reuse
  existing business logic instead of re-deriving or duplicating it.

## Elicitation

- Turn a loose user request into structured requirements: what's the actual
  goal, who's affected, what's explicitly out of scope.

## Acceptance criteria format

- Write acceptance criteria in **Given-When-Then** form. (This project
  standardizes on Given-When-Then; the source material used a plain "As a…"
  story format — this is a deliberate upgrade, not an oversight.)
- Still capture the user story framing where useful: "As a … / I want … / so
  that …" — but the AC themselves are Given-When-Then.

## Traceability

- Keep an explicit chain: requirement → acceptance criterion → test. A reviewer
  should be able to point at a test and know which AC it satisfies.

## Discipline

- Prioritize requirements when there are several.
- Eliminate ambiguity — vague requirements become the architect's and
  developer's problem later, at higher cost.
- Hold scope: don't let the AC quietly grow beyond the original request.
- Validate drafts early with whoever can confirm intent, rather than polishing
  in isolation.

---
Source: getelyxai.com/en/blog/business-analyst-best-practices
