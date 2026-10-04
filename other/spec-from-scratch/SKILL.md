---
name: spec-from-scratch
description: Create a complete SPEC from scratch through an exhaustive requirements interview before any planning or implementation. Use this skill whenever the user asks to create, define, clarify, scope, or write a spec/SPEC/PRD/requirements document from an idea, especially when they want to avoid assumptions, start at "step zero," or prepare input for later planning workflows. This skill must question goals, requirements, constraints, edge cases, business rules, and acceptance criteria before drafting the final spec.
metadata:
  author: "Giuliano Lemes <giuice@gmail.com>"
---

# Spec From Scratch

Use this skill to turn an unclear idea into a complete, assumption-light Product SPEC. The core job is not writing first; it is discovering what must be true before a useful spec can exist.

This workflow is portable across coding agents and planning systems. Treat it as a pre-planning gate: after the SPEC is complete, the user may hand it to any planning method, implementation workflow, or project-management process.

## Operating principle

Do not draft the final SPEC until the user's goals, requirements, constraints, edge cases, business rules, and acceptance criteria are fully understood.

If critical information is missing, ask more questions. A polished spec built on hidden assumptions is worse than no spec because it makes uncertainty look settled.

## Interview mode: exhaustive rounds

There is one mode: **exhaustive**. Each round asks the maximum set of useful questions at once — never one question per message. Depth is guaranteed not by drip-feeding questions, but by a coverage gate (step 4) that forces follow-up rounds until every domain is `Clear`.

- **Round 1** asks every question that does not depend on a prior answer, covering all domains at once.
- **Later rounds** add questions only when (a) a prior answer unlocks new questions, or (b) the coverage gate marks a domain `Partial` or `Missing`. Defer dependent questions to the round after their prerequisite is answered.
- After each round, store the answers and update the coverage table before generating the next round.

## Workflow

### 1. Start with scope capture, then deliver round 1

Restate the raw idea in one or two sentences and derive a short kebab-case identifier for it — the spec slug (for example `checkout-redesign`, `domain-clarification`). Create a per-spec working directory `spec-interview/<slug>/`: every round file, the interview state, and the final SPEC for this idea live inside it, so multiple specs never collide and the folder name itself identifies the work. Detect whether the project produces code (see the test-strategy domain below). Then deliver the first exhaustive question round using the delivery rules in step 2.

Round 1 must include at least one question about each of these areas: goals, primary users, scope boundaries, business rules or constraints, edge cases/failure modes, and acceptance criteria or success signals. Aim wide — 7-10+ questions — so the shape of the problem is exposed in one pass.

Use questions with answer options. Mark exactly one option as `(Recommended)` unless the question truly has no sensible default. **Every question must also let the user write their own answer or attach a note** — never force a choice among fixed options only.

### 2. Deliver questions through a clickable UI

Pick the delivery channel based on the host agent's capabilities:

**Native UI path (preferred when available).** If the host provides a structured question UI with clickable options (for example, a question tool that renders selectable options), use it. Always include an `Other — write your own` choice and tell the user they may add a free-text note to any answer.

Caveat — question-count cap: some native question UIs limit how many questions one prompt can hold (for example, ~4). If that cap is below what the exhaustive round needs, do not shrink the round to fit the UI — switch to the HTML fallback path so the full round is delivered at once. Use the native UI only for small rounds (follow-ups) that fit under the cap.

**HTML fallback path.** If no native question UI exists, generate a self-contained HTML file at `spec-interview/<slug>/round-N.html` for the round. A ready-to-adapt template ships with this skill at `assets/interview-round.template.html` — copy it, set the `round`/`topic`, and replace the `QUESTIONS` array (it already demonstrates both single-choice `radio` and multiple-choice `checkbox` questions, plus the per-question note field and the copy/download logic). Keep the rest as-is. The file must:

- Be a single file with inline CSS and JS, **no network access** (it opens offline).
- Render each question with: a title; an optional `(Recommended)` badge; options as **radio** buttons (single choice) or **checkboxes** (multiple choice); and **always** a free-text `<textarea>` labeled `Other / note` for that question.
- Include a **Copy answers** button that builds a structured block and copies it to the clipboard. Format:

  ```json
  {
    "round": 1,
    "answers": [
      { "id": "q1", "selected": ["B"], "note": "" },
      { "id": "q2", "selected": ["A", "C"], "note": "also needs SSO" }
    ]
  }
  ```

- Optionally also offer a `Download answers.json` button as an alternative return path.
- Use associated `<label>`s and visible focus styles for accessibility.

Tell the user to fill the form, click **Copy answers**, and paste the block back into the chat (or share the downloaded file). When the block arrives, confirm the parse out loud (briefly restate what each answer was read as) before continuing.

### 3. Interview exhaustively by domain

Cover these domains before drafting:

1. **Problem and goals**
   - Problem being solved
   - Desired outcome
   - Primary and secondary users
   - Jobs to be done
   - Success metrics
   - Non-goals

2. **Scope and deliverables**
   - Product surface or system boundary
   - Must-have vs should-have vs later
   - User journeys
   - Inputs and outputs
   - Environments, platforms, or channels
   - Dependencies

3. **Requirements**
   - Functional requirements
   - Data requirements
   - Permission and access rules
   - Integrations
   - Reporting, notifications, or automation
   - Admin or support needs

4. **Business rules**
   - Eligibility rules
   - Pricing, billing, quotas, or limits
   - Workflow states and transitions
   - Approval rules
   - Compliance or policy constraints
   - Exceptions and overrides

5. **Constraints**
   - Technical constraints
   - Time, budget, staffing, and operational constraints
   - Existing systems that must be preserved
   - Security, privacy, legal, and regulatory constraints
   - Performance and reliability expectations
   - Localization, accessibility, and device constraints

6. **Edge cases and failure modes**
   - Empty, invalid, duplicate, stale, missing, or conflicting data
   - Partial completion and retry behavior
   - Offline or degraded dependencies
   - Abuse cases
   - Race conditions or concurrent edits
   - User mistakes and recovery paths

7. **Acceptance criteria and validation**
   - Observable behavior for each major flow
   - Given/When/Then scenarios
   - Definition of done
   - Test data or examples
   - UAT checklist
   - Launch or rollout criteria

8. **Test strategy** *(only when the project produces code)*
   - Target test levels (unit, integration, end-to-end)
   - TDD or test-after, and whether tests are written from the acceptance criteria
   - Test data, fixtures, and mocks
   - Test environments and CI expectations
   - Coverage or done-criteria for tests
   - Error and failure cases that must have tests

   Skip this domain entirely for non-code deliverables.

### 4. Track knowns and unknowns

After each round, persist the answers to `spec-interview/<slug>/state.md` so progress survives a dropped chat. Rewrite the whole file each round: the scope restatement from step 1 on the first line — so a later session can tell from the file alone what work this folder holds — then the answers so far grouped by domain, then the current coverage table. Then summarize progress in a compact state table:

```markdown
## Current understanding

| Area | Status | Notes |
|---|---|---|
| Goals | Clear / Partial / Missing | ... |
| Users | Clear / Partial / Missing | ... |
| Requirements | Clear / Partial / Missing | ... |
| Constraints | Clear / Partial / Missing | ... |
| Edge cases | Clear / Partial / Missing | ... |
| Business rules | Clear / Partial / Missing | ... |
| Acceptance criteria | Clear / Partial / Missing | ... |
| Test strategy (code only) | Clear / Partial / Missing / N/A | ... |

## Remaining unknowns

- [Unknown]
- [Unknown]
```

Do not mark a domain `Clear` on generic answers alone. Edge cases and business rules require concrete examples before they count as `Clear`. While any domain is below `Clear`, generate another round targeting only the weak or newly-unlocked areas — do not move on.

### 5. Apply the hard readiness gate

Before writing the final SPEC, explicitly run this gate:

```markdown
## SPEC readiness check

- Goals are specific and measurable: Pass / Missing
- Users and stakeholders are identified: Pass / Missing
- In-scope and out-of-scope boundaries are explicit: Pass / Missing
- Functional requirements are testable: Pass / Missing
- Business rules are explicit: Pass / Missing
- Constraints are explicit: Pass / Missing
- Edge cases and failure modes are covered: Pass / Missing
- Acceptance criteria are observable: Pass / Missing
- Every Must-priority functional requirement has at least one acceptance criterion: Pass / Missing
- Test strategy is defined (code projects only): Pass / Missing / N/A
- Open questions are non-blocking or intentionally deferred: Pass / Missing

Verdict: Ready / Not ready
```

If any item is `Missing`, the verdict is `Not ready` and you must run another round instead of drafting the final SPEC.

If the user asks to draft anyway, refuse the final SPEC politely and offer one of these alternatives:

- Continue the interview
- Produce a clearly labeled `Discovery Notes` summary, not a SPEC
- Narrow the scope so the readiness gate can pass

### 6. Write the final SPEC only when ready

When the readiness gate passes, save the SPEC to `spec-interview/<slug>/SPEC.md` using this default Product SPEC format:

```markdown
# SPEC: [Name]

Goal: [the desired outcome, in one sentence]

## 1. Summary
[Concise description of what is being built and why.]

## 2. Problem statement
[The problem, who has it, and why it matters.]

## 3. Goals and success metrics
### Goals
- ...

### Success metrics
- ...

## 4. Users and stakeholders
### Primary users
- ...

### Secondary users
- ...

### Stakeholders
- ...

## 5. Scope
### In scope
- ...

### Out of scope
- ...

## 6. User journeys
- ...

## 7. Functional requirements
Use stable requirement IDs:

| ID | Requirement | Priority | Acceptance signal |
|---|---|---|---|
| FR-001 | ... | Must | ... |

## 8. Business rules
Use stable rule IDs:

| ID | Rule | Rationale |
|---|---|---|
| BR-001 | ... | ... |

## 9. Data and integrations
### Data inputs
- ...

### Data outputs
- ...

### Integrations
- ...

## 10. Constraints and assumptions
### Constraints
- ...

### Assumptions
Only include assumptions explicitly confirmed by the user.
- ...

## 11. Edge cases and failure modes
| Case | Expected behavior |
|---|---|
| ... | ... |

## 12. Security, privacy, compliance, and abuse considerations
- ...

## 13. Accessibility, localization, and usability considerations
- ...

## 14. Acceptance criteria
Make each criterion TDD-ready by referencing the functional requirement(s) it validates. Use Given/When/Then where helpful:

- AC-001 (FR-001): Given ..., when ..., then ...

## 15. Test strategy
*(Include only for code projects; omit for non-code deliverables.)*
- Test levels: unit / integration / end-to-end and what each covers
- TDD or test-after, and how tests trace back to acceptance criteria
- Test data, fixtures, environments, and CI expectations
- Mandatory test cases, including error and failure paths

## 16. Validation and launch checklist
- ...

## 17. Open questions
Only include non-blocking questions. If any question blocks requirements, return to the interview instead.
- ...
```

## Question design rules

- Provide options that teach tradeoffs, not generic choices.
- Always give every question a free-text path: an `Other — specify` option plus room for a note.
- Defer dependent questions to a later round, after their prerequisite is answered.
- Recommend the safest or most scope-preserving option when uncertain.
- Prefer concrete language over abstract product jargon.
- Ask about negative space: what the product must not do.
- Ask about bad data, bad actors, failed dependencies, and user mistakes.
- Ask for examples whenever a rule or workflow could be interpreted multiple ways.
- Do not invent domain facts. If a detail matters and is unknown, ask.

## Handling different user styles

If the user is brief, offer defaults but keep the hard readiness gate.

If the user is domain-expert, ask sharper business-rule and edge-case questions instead of explaining basics.

If the user is overwhelmed, keep the round small (3-5 questions) and remind them they can answer by clicking options and adding a note.

If the user gives a large existing brief, extract what is already answered first, then build the round around the gaps only.

## Portable output note

When the user plans to use the result in another tool or agent, keep the final SPEC self-contained. Avoid references like "as discussed above" unless the referenced content is included in the SPEC itself.
