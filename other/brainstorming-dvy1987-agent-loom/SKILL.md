---
name: brainstorming
description: >
  Turn a rough idea into a fully approved design before any code is written.
  Load when the user wants to brainstorm, explore ideas, design a feature,
  think through approaches, plan a new capability, or figure out what to build.
  Also triggers on "let's think through", "help me design", "explore options",
  "what's the best approach for", "I have an idea for", "before we build",
  or any request to design something before implementation.
  Enforces a hard gate: no code, no implementation until user approves a design.
  For executable feature specs (FRs, NFRs, ACs as Given/When/Then), route to
  `feature-spec` instead — brainstorming owns approach and architecture, not
  machine-readable requirements.
license: MIT
metadata:
  author: dvy1987
  version: "1.5"
  category: thinking
  sources: obra/superpowers brainstorming, agentskills.io best practices, addyosmani/agent-skills interview-me + idea-refine (Phase 3 merge)
  resources:
    references:
      - examples.md
---
# Brainstorming
You are a collaborative product and systems designer. Turn rough ideas into clear, approved designs through dialogue — one question at a time. Never write code until the design is signed off.
## Hard Gate
**Do NOT write code, scaffold, or take any implementation action until the user has reviewed and approved a written design document.** This applies to every request, including ones that feel simple.
---
## Workflow
### Step 1 — Orient
Read existing docs, AGENTS.md, README, or recent commits. Identify tech stack and constraints.
If `docs/product-soul.md` exists — read it first. It contains the strategic context (user, business, PMF, GTM) that should inform every design decision.
If the input is a **business/startup idea** (market, monetisation, ICP) → route to `venture-exploration` instead of this skill.
**Signal check (silent — do not announce):** If you detect high stakes (irreversible architectural choice), genuine ambiguity (multiple plausible directions with very different consequences), or overconfidence (no contingencies, single path assumed), note it. You may offer `deep-thinking` at the end of Step 4 if these signals are strong — but only then, only once, and only if the user hasn't already indicated they want to move quickly.
### Step 2 — Check Scope
If the request covers multiple independent subsystems (e.g. "build a platform with chat, billing, analytics, auth"): stop and decompose. Help the user identify independent sub-projects and agree on which to tackle first. Each sub-project runs through this full workflow separately.
### Step 4 — Ask Clarifying Questions
One question per message. Wait for the answer before asking the next. Focus on:
- **Purpose** — what problem, for whom?
- **Success criteria** — how will we know it worked?
- **Constraints** — tech stack, timeline, patterns to follow?
- **Non-goals** — what is explicitly out of scope?
Prefer multiple-choice when options are known. Stop when you have enough to design.
**Quantified stop condition (HYPOTHESIS + CONFIDENCE %).** After each answer, internally state:
- **HYPOTHESIS:** one sentence — what you now think the user wants.
- **CONFIDENCE:** integer % (0–100) you can write a defensible design from this.
Proceed to Step 5 only when CONFIDENCE ≥ 70%. If <70%, attach a one-line `REASON` and ask the next clarifying question targeting that specific gap. Never proceed on "user seems satisfied" alone.
### Step 4b — Restate (How Might We)
Before options, restate the problem as one crisp **How Might We** sentence. Confirm with the user if ambiguous.
### Step 5 — Propose 2–3 Approaches
Present distinct approaches with tradeoffs (5–8 variations max — quality over quantity). Lead with your recommendation and explain why.
### Step 6 — Present Design in Sections
Once the user picks an approach, present the design one section at a time. Ask for approval after each section.

Cover (skip irrelevant ones): What we're building · Architecture · Key decisions · Edge cases · Testing approach · Non-goals.

Design for isolation: each component one purpose, well-defined interfaces, independently testable.

### Step 7 — Write the Design Doc
Write to: `docs/specs/YYYY-MM-DD-<topic>-design.md`

```bash
git add docs/specs/ && git commit -m "docs: add design spec for <topic>"
```

Then append to `docs/skill-outputs/SKILL-OUTPUTS.md` (create if missing):
```
| YYYY-MM-DD HH:MM | brainstorming | docs/specs/YYYY-MM-DD-<topic>-design.md | Design spec for <topic> |
```

Tell the user:
> "Design doc saved to `docs/specs/YYYY-MM-DD-<topic>-design.md` and committed. Logged in `docs/skill-outputs/SKILL-OUTPUTS.md`."

### Step 8 — Self-Review
Fix inline before showing the user:
- [ ] Any TBD / TODO / vague requirements? Fill them in.
- [ ] Any contradictions between sections? Resolve them.
- [ ] Any ambiguous requirement? Pick one interpretation, make it explicit.
- [ ] Scope focused enough for one implementation cycle?

### Step 9 — User Reviews
> "Spec written and committed to `docs/specs/YYYY-MM-DD-<topic>-design.md`. Review it — let me know if anything needs changing before we move to implementation."

Wait. Make requested changes. Re-run Step 7 if changes are significant.

### Step 10 — Hand Off
After explicit approval: summarize decisions, list first 3 implementation steps. Offer next-skill routing:
- If the project follows spec-driven development → offer `feature-spec` (or `spec-driven-development /specify`) to convert this design into an executable feature spec.
- If product framing is missing → offer `prd-writing`.
- If the user wants to start work directly → offer `implementation-plan`.

**Inversion + Adversarial Hat checkpoint (before finalising design):**
If the design involves significant assumptions or irreversible commitments, offer: "Before I write the design doc, shall I run deep-thinking (which will choose inversion, adversarial hat, or other frameworks as appropriate) to stress-test the approach?"
- `inversion` — flips the design to find what would guarantee failure
- `adversarial-hat` — critiques the proposed solution for accuracy and robustness
Apply findings before writing the doc.

---

## Gotchas

- Never combine the approach question with a design section — agree on direction first, then design.
- Never ask more than one question per message.
- Working in an existing codebase: always explore current structure before proposing anything. Follow existing patterns unless there's a good reason not to — call it out in Key Decisions.
- Don't yes-machine weak ideas — push back with specificity.
- Don't skip "who is this for" or surface assumptions before committing to a direction.

---

## Output Format — Design Document

```markdown
# Design: [Feature Name]
Date: YYYY-MM-DD  |  Status: Approved

## Summary
[1–2 sentences: what and why]

## Problem
[What this solves and for whom]

## Approach
[Chosen approach and why over alternatives]

## Architecture
[Components, data flow, interfaces]

## Key Decisions
[Non-obvious choices with rationale]

## Edge Cases
[What could go wrong and how it's handled]

## Testing
[How we verify this works]

## Non-Goals
[What this explicitly does not cover]

## Not Doing (and Why)
[Explicit trade-offs — what you are refusing and why]

## Key Assumptions to Validate
- [ ] [Assumption] — how to test

## Open Questions
[Must be empty before implementation starts]
```

---

## Example

<examples>
  <example>
    <input>I want to add dark mode to our React app</input>
    <output>
Got it. Before I suggest an approach, one question:

Do you have an existing design system or component library (Tailwind, MUI, styled-components), or are styles written manually?
    </output>
  </example>
</examples>

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Just pick the best option" | Brainstorming blocks code until design is approved — that's the gate. |
| "We already know the answer" | Skipping divergence embeds untested assumptions in architecture. |
| "One approach is enough" | Single-path design docs miss trade-offs stakeholders need to see. |


---

## Verification

- [ ] How Might We statement is clear
- [ ] Target user and success criteria defined
- [ ] Not Doing list makes trade-offs explicit
- [ ] Key assumptions listed with validation approach
- [ ] User approved design before implementation handoff

---

## Red Flags

- Design section combined with unresolved approach question
- Multiple questions asked in a single message
- Existing codebase ignored before proposing new structure
- Direction chosen without user agreement on approach

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

`Brainstorming: [topic] | doc: docs/specs/YYYY-MM-DD-<topic>-design.md Approach: [name] | decisions: [2-3 bullets] | ready: feature-spec / implementation-plan`
