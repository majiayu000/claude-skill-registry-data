---
name: brainstorming
description: "Clarify ambiguous features, UX/UI changes, architecture decisions before coding."
license: MIT
---

# Brainstorming Ideas Into Designs

Turns an unsettled request into an approved design spec. Sets gates and outcomes, not procedure. Terminal state: implementation planning, never implementation.

## Hard gates — never bend

1. GET EXPLICIT APPROVAL BEFORE IMPLEMENTATION ACTION. User approves the design direction and the written spec before any planning handoff, code, or scaffolding. When design and spec are the same short document, one approval covers both — say so when asking. Blocks: "the right approach was obvious, so I started."
2. APPROVAL IS AN AFFIRMATIVE RESPONSE to an explicit request naming the design/spec. Silence, acknowledgements, and non-committal replies are not approval — ask again. Never claim an approval, path, task ID, or tsq state not actually given or created. Blocks: "they didn't object."
3. TREAT THE CHANGE AS DESIGN WORK unless it is mechanical, exactly specified by the user, and decision-free (typo, exact rename, literal one-liner). Behavior-changing = alters anything a user, caller, or downstream system observes, or requires any choice the user did not literally state — refactors involving an approach choice count. Unsure → it's design work. Blocks: "this flag is trivial."
4. SAVE THE SPEC AS A RE-READABLE ARTIFACT before asking for spec approval — tsq task, repo file, or (last resort, say why) one complete self-contained message. Blocks: "the discussion above is the spec."

User explicitly waives a gate → comply, and state what's being skipped. Harness plan-mode approval satisfies the design-approval half of gate 1.

## Flow

Match ceremony to risk: gates are fixed, ceremony volume scales.

- Context first: inspect repo state, docs, recent commits; follow existing patterns. A request spanning independent subsystems → decompose; each sub-project gets its own spec → plan cycle.
- Clarifying questions: batch independent ones (AskUserQuestion when available); serialize only when one depends on another's answer; stop once purpose, constraints, and success criteria support honest tradeoffs.
- Approaches: 1-3 viable ones, recommendation first with why and tradeoffs. Never invent alternatives to fill a quota; one clearly right approach → present it alone.
- Design: fits ~1 page → present whole, single approval; larger → by section, approval per section. Cover when relevant: architecture, components, data flow, error handling, testing, user-visible behavior, non-goals. User rejects → revise; don't advance on unresolved disagreement.
- No governance/stakeholder/process/executive-workflow docs unless the user explicitly asks.

## Spec

Contents: problem/purpose, approved scope, requirements, approach, constraints/non-goals, risks and open questions resolved so far, testing expectations.

Independent adversarial-review before user review — fix inline:

1. Placeholders: no TBD/TODO, incomplete sections, or vague requirements.
2. Consistency: no contradictions.
3. Scope: one implementable project, or decompose.
4. Ambiguity: a requirement that can mean two things → pick or ask, write the explicit meaning.
5. YAGNI: nothing unrequested, no over-engineering.
6. Verification: testing/smoke expectations concrete enough for plan tasks.

Complex work → optionally dispatch this same checklist to a fresh subagent as an advisory pass; flag serious planning blockers only.

Storage: durable/tracked work → attach to the tsq parent (`tsq spec <task-id> --text "<spec>"`, then `tsq note <task-id> "Spec approved for planning"`). Repo file (`docs/specs/YYYY-MM-DD-<topic>-design.md` or repo convention) only when the user asks, convention requires, or tsq is unavailable; user path preference wins. Commit design docs only on explicit ask.

Review ask: state where the spec lives (tsq ID and/or path, or why it's conversation-only), then ask for changes before planning. Changes requested → edit, re-run self-review, ask again.

## Handoff

Gates satisfied → hand to the `planner` agent, passing the spec explicitly (tsq parent ID, file path, or full text). `planner` unavailable → repo's normal implementation-planning workflow.

## Interactive visuals

Offer only when upcoming questions are genuinely visual (mockups, layout, diagrams, side-by-side options); say it's token-intensive and get opt-in first. Accepted → browser only when seeing beats reading; terminal stays source of truth for requirements, tradeoffs, and anything answerable in words. Self-contained HTML in `/tmp` (or gitignored `docs/ideation`); throwaway — keep updating one file, never commit unless asked.
