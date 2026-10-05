---
name: codebase-improve-architecture
category: codebase-build
description: Find deepening opportunities in a codebase, informed by the domain language in CONTEXT.md and the decisions in docs/adr/. Use when the user wants to improve architecture, find refactoring opportunities, consolidate tightly-coupled modules, or make a codebase more testable and AI-navigable.
codex-short-description: "Find refactoring and architecture-deepening opportunities in a codebase"
related-skills:
  - codebase-design
  - domain-modeling
  - codebase-plan-refactor
  - grill-with-docs
loop-eligible: false

compatibility: claude-code codex opencode
---
# Improve Codebase Architecture

Surface architectural friction and propose **deepening opportunities** — refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

## Vocabulary

Speak the deep-module language from [codebase-design](../codebase-design/) — **module**, **interface**, **implementation**, **depth** (deep vs shallow), **seam**, **adapter**, **leverage**, **locality** — and use those terms exactly in every suggestion, rather than drifting into "component," "service," "API," or "boundary." Read that skill before presenting candidates: the definitions and the principles it turns on (the deletion test, the interface as test surface, one adapter means a hypothetical seam) live there, not here.

This skill is _informed_ by the project's domain model. The domain language gives names to good seams; ADRs record decisions the skill should not re-litigate. The discipline for changing that model is the [domain-modeling](../domain-modeling/) skill.

## Process

### 1. Explore

Read the project's domain glossary and any ADRs in the area you're touching first.

**Bias the scan toward code that is actually moving.** Unless the user points you at a specific area, read recent commit history first and weight the walk toward paths that change often — a deepening in code nobody touches is a refactor that never gets cashed in. (`codebase-churn` produces exactly this ranking if you want it precisely.)

Then walk the codebase, dispatching parallel read-only exploration agents where the host provides them and reading directly where it doesn't — the scan is less thorough without them, not invalid. Don't follow rigid heuristics — explore organically and note where you experience friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow** — interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply the **deletion test** to anything you suspect is shallow: would deleting it concentrate complexity, or just move it? A "yes, concentrates" is the signal you want.

### 2. Present candidates

Present a numbered list of deepening opportunities. For each candidate:

- **Files** — which files/modules are involved
- **Problem** — why the current architecture is causing friction
- **Solution** — plain English description of what would change
- **Benefits** — explained in terms of locality and leverage, and also in how tests would improve
- **Strength** — `Strong` (the deletion test passes clearly and the friction is real), `Worth exploring` (payoff depends on where the code is going next), or `Speculative` (surfaced for completeness)

Close with a **top recommendation** — the one you'd tackle first.

A skill built to output findings will always find some, so the strength labels are how you say "nothing here": if every candidate is `Speculative`, state plainly that the area looks healthy rather than promoting the least-weak card.

**Use CONTEXT.md vocabulary for the domain, and [codebase-design](../codebase-design/) vocabulary for the architecture.** If `CONTEXT.md` defines "Order," talk about "the Order intake module" — not "the FooBarHandler," and not "the Order service."

**ADR conflicts**: if a candidate contradicts an existing ADR, only surface it when the friction is real enough to warrant revisiting the ADR. Mark it clearly (e.g. _"contradicts ADR-0007 — but worth reopening because…"_). Don't list every theoretical refactor an ADR forbids.

**Stop here.** Do not propose interfaces, do not start designing, and do not begin interrogating the user about the first candidate. Ask: "Which of these would you like to explore?" and wait.

This is the step that fails in practice: the survey collapses into an hour of questions about one idea the agent liked, and the user never sees the list they came for. The report is the deliverable of step 2; the grilling in step 3 is a separate, opt-in phase over a candidate the *user* chose. If the user says they only want the report, deliver it and stop — that's a complete run, not an abandoned one.

**One candidate per session.** Working several in one conversation fills the context with the survey, the grilling, the domain-model edits, and the code all at once. Take the chosen one through to a decision, then start fresh — or file the rest as tickets to pick up independently.

### 3. Grilling loop

Once the user picks a candidate, drop into a grilling conversation. Walk the design tree with them — constraints, dependencies, the shape of the deepened module, what sits behind the seam, what tests survive.

Side effects happen inline as decisions crystallize:

- **Naming a deepened module after a concept not in `CONTEXT.md`?** Add the term to `CONTEXT.md` — same discipline as `/grill-with-docs` (see [CONTEXT-FORMAT.md](../domain-modeling/CONTEXT-FORMAT.md)). Create the file lazily if it doesn't exist.
- **Sharpening a fuzzy term during the conversation?** Update `CONTEXT.md` right there.
- **User rejects the candidate with a load-bearing reason?** Offer an ADR, framed as: _"Want me to record this as an ADR so future architecture reviews don't re-suggest it?"_ Only offer when the reason would actually be needed by a future explorer to avoid re-suggesting the same thing — skip ephemeral reasons ("not worth it right now") and self-evident ones. See [ADR-FORMAT.md](../domain-modeling/ADR-FORMAT.md).
- **Want to explore alternative interfaces for the deepened module?** See [INTERFACE-DESIGN.md](../codebase-design/INTERFACE-DESIGN.md).

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/codebase-improve-architecture.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
