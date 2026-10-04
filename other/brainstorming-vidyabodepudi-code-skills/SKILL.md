---
name: brainstorming
description: >
  Collaborative design refinement with hard gates preventing premature
  implementation. Use BEFORE any creative work — creating features,
  building components, adding functionality, or modifying behavior.
  Explores user intent, requirements, and design before implementation.
version: 1.0.0
permissions:
  - fs.read
  - fs.write
  - browser.inspect
triggers:
  - context: "starting a new feature"
  - context: "user describes something to build"
  - context: "creative work or design needed"
  - command: "/spec"
platforms:
  - claude-code
  - cursor
  - gemini-cli
  - copilot
  - codex
  - opencode
  - windsurf
  - kiro
model_variants:
  claude:
    enforcement_style: "human-partner collaborative"
    gate_phrasing: "Let's explore this idea together before we build anything. I want to make sure I understand what you need."
  gemini:
    enforcement_style: "structured-checklist"
    gate_phrasing: "DESIGN GATE: ☐ Context explored ☐ Questions asked ☐ Approaches proposed ☐ Design approved ☐ Spec written"
  gpt:
    enforcement_style: "directive-imperative"
    gate_phrasing: "You MUST present a design and receive approval BEFORE writing any code. No exceptions."
author: codehands-core
signed: true
tier: 1
---

## Overview

Brainstorming turns vague ideas into validated designs through structured Socratic dialogue. It prevents the most expensive mistake in software: building the wrong thing. Every project — no matter how "simple" — goes through this process.

## When to Use

- Before ANY creative work: new features, components, behaviors
- When a user describes something they want built
- When requirements are ambiguous or underspecified
- NOT mid-implementation (if requirements change mid-build, pause and re-brainstorm)
- NOT for simple bug fixes with clear reproduction steps

<HARD-GATE>
Do NOT write any code, scaffold any project, or take any implementation
action until you have presented a design and the user has approved it.
This applies to EVERY project regardless of perceived simplicity.
</HARD-GATE>

## Process

### Phase 1: Understand Context

1. **Explore the project.** Check files, docs, recent commits, existing patterns. Understand what exists before proposing what's new.
2. **Assess scope.** If the request spans multiple independent subsystems, flag this immediately. Large projects need decomposition before design — don't refine details of something that should be split.
3. **Offer visual companion** (if visual questions ahead). This is its own message — never combined with other content:
   > "Some of what we're working on might be easier to explain with visuals. I can show mockups, diagrams, and comparisons in a browser. Want to try it?"

### Phase 2: Clarify Intent

4. **Ask questions ONE at a time.** Not a list of 5 questions. One question per message.
5. **Prefer multiple-choice** when possible. Easier to answer than open-ended.
6. **Focus on:** Purpose (why), constraints (what limits), success criteria (how you'll know it works).
7. **Stop when you understand:** What should happen, what should NOT happen, who uses it, and how success is measured.

### Phase 3: Explore Approaches

8. **Propose 2-3 approaches with tradeoffs.** Never present a single option.
9. **Lead with your recommendation** and explain why.
10. **Include for each approach:** Architecture, complexity, timeline, risks, limitations.

### Phase 4: Present Design

11. **Present the design section by section.** Scale each section to its complexity — a few sentences if simple, up to 200-300 words if nuanced.
12. **Ask after each section:** "Does this look right so far?"
13. **Cover:** Architecture, components, data flow, error handling, testing strategy, security considerations.
14. **Design for isolation:** Break the system into units that each have one clear purpose, communicate through well-defined interfaces, and can be tested independently.

### Phase 5: Document & Gate

15. **Write the design doc.** Save to `docs/specs/YYYY-MM-DD-<topic>-design.md`.
16. **Self-review the spec:**
    - Placeholder scan: Any TBD, TODO, or vague requirements? Fix them.
    - Internal consistency: Do sections contradict each other?
    - Scope check: Is this focused enough for a single implementation?
    - Ambiguity check: Could any requirement be read two ways?
17. **User review gate:** Ask the user to review the written spec.
18. **Only after approval:** Transition to `codehands:planning-and-task-breakdown`.

## Working in Existing Codebases

- Explore the current structure BEFORE proposing changes
- Follow existing patterns. Don't introduce new paradigms without justification.
- If existing code has problems related to your work (overgrown file, tangled boundaries), include targeted improvements — don't propose unrelated refactoring.

## Key Principles

- **One question at a time** — don't overwhelm
- **Multiple choice preferred** — lower cognitive load
- **YAGNI ruthlessly** — remove features you don't need yet
- **Always 2-3 options** — never present a single approach
- **Incremental validation** — get approval at each stage
- **Design can be short** — a 3-sentence design for a trivial task is fine. Skipping design entirely is not.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "This is too simple to need a design" | Simple projects are where unexamined assumptions cause the most wasted work. The design can be 3 sentences, but you MUST present it. |
| "The user clearly knows what they want" | Even clear requests contain ambiguity. "Build a login page" has 20+ design decisions hidden in it. Surface them. |
| "I'll just start and iterate" | Starting without a design means iterating from a random point. Design first so iteration moves toward the goal, not sideways. |
| "Asking too many questions will annoy the user" | Asking the right questions saves the user hours of rework. One well-placed question prevents days of wasted effort. |
| "I can see the whole design in my head" | You can't. You're predicting what the user wants based on patterns. Your mental model has gaps — surface them through questions. |

## Red Flags

- Jumping to code before presenting a design
- Asking 5+ questions in a single message
- Presenting only one approach ("here's what I'll build")
- Skipping the spec self-review
- Not exploring existing code before designing changes
- Proposing a design without asking about constraints or success criteria

## Verification

- [ ] Project context explored (existing files, patterns, recent changes)
- [ ] Clarifying questions asked one at a time
- [ ] 2-3 approaches proposed with tradeoffs and recommendation
- [ ] Design presented section by section with user approval at each stage
- [ ] Design doc written and saved to `docs/specs/`
- [ ] Spec self-review completed (no TBDs, no contradictions, scope focused)
- [ ] User has reviewed and approved the spec
- [ ] NO code was written before design approval

## See Also

- `codehands:spec-driven-development` — Formal specification authoring
- `codehands:planning-and-task-breakdown` — Next step after brainstorming
- `codehands:context-engineering` — Managing context during design
