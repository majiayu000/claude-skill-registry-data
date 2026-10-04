---
name: rapid-prototype-and-vibe-coding-craft
description: "Builds a fast, working, credible-enough prototype to prove an AI opportunity using AI-assisted coding (\"vibe coding\") — tool selection by task type, a tight prompt/review/test/commit iteration cycle, the right fidelity level, and known risks (hallucinated interfaces, auth gaps). Use when you need a fast, proof-capable prototype before committing to a bigger build."
---

# Rapid Prototype & Vibe Coding Craft

## Purpose

Build a prototype as fast as possible that is **just credible enough to
prove one specific hypothesis** — no more. The most common mistake in an AI
consultant's prototyping isn't a prototype that's too rough, but a prototype
at the wrong level: either too thin to prove anything, or needlessly
polished (time wasted on finishing touches nobody has asked for yet). This
skill helps you pick the right fidelity level and use AI-assisted coding
("vibe coding") with discipline, so that speed doesn't buy invisible risk.

## Anchored in research

- Vibe coding best practices 2026 (synthesis of multiple sources, see
  References): tool selection by task type, a tight iteration cycle,
  a PRD before prompting, known risks, and limits on where vibe coding is
  worth using.
- Prototype fidelity research (low vs. high fidelity): low-fidelity
  prototypes identify a large share of structural problems at a fraction of
  the cost of high fidelity — see References.

## Method

1. **Define EXACTLY one hypothesis the prototype has to prove** before you
   open any tool. Example of a good hypothesis: "AI can extract the correct
   supplier business ID and amount from 20 random purchase invoices without
   human correction." Example of a bad (too broad) hypothesis: "AI could
   help with the purchase-invoice process." If you can't state the
   hypothesis in one sentence that can be scored yes/no, you're still too
   early for prototyping. Keep the framing explicit throughout the build: a
   prototype is a tool to reduce strategic uncertainty about whether this
   is worth building for real, not a rough draft of the eventual product —
   treating it as the latter is what causes scope and polish to creep in
   past what the hypothesis actually needs. Give the team an explicit
   **kill mandate**: the authority and standing instruction to drop a
   prototype early once it's clear it won't prove the hypothesis, rather
   than continuing to invest in something already known not to work
   because stopping feels like admitting failure.
2. **Choose the fidelity level based on the hypothesis, not convenience:**
   - **Low fidelity** (a static mockup, a hand-built example, no working
     code) — enough when the question is structural: does the user
     understand the workflow, does the UI sequence make sense, is the
     vision appealing at all. The fastest, cheapest way to find fundamental
     problems before any code is written.
   - **A working, narrow prototype** (genuinely functional, but on only one
     path, without error handling, without production infrastructure) —
     needed when the hypothesis is technical in nature ("can AI do X on our
     data with sufficient accuracy"). This is the core territory for vibe
     coding.
   - **High fidelity** — only once a lower level has already validated the
     idea and the next question concerns the real user experience in a
     production-like environment. This usually isn't the job of a
     consultant's first demo. Watch for the high-fidelity trap: once a
     prototype looks visually finished, stakeholders reliably start
     discussing button colors and copy wording instead of the strategic
     question the prototype was built to answer — the moment a review
     conversation shifts from "does this prove the hypothesis" to
     cosmetic detail, the prototype has done its job too well for its own
     fidelity level, and it's a sign to either name the shift explicitly
     or deliberately roughen the finish back down.
3. **Choose the tool by task type, don't use one tool for everything.** A
   rough rule of thumb: a full-stack application sketch → a general-purpose
   AI coding agent; complex editing/refactoring of existing code → an agent
   with good whole-codebase context; a fast, non-data-persisting demo/mockup
   → a lightweight no-code/low-code tool. Combine several tools as needed
   rather than forcing one tool onto every task.
4. **Write a short PRD (one page is enough) before prompting**, even for a
   small prototype: what input is processed, what output is expected, which
   2-3 cases REALLY have to work for the demo. This prevents the most
   common vibe coding pitfall: an AI agent building something technically
   functional but wrong, because the task was under-specified.
5. **Keep the iteration cycle tight and short:** prompt one bounded change
   → review the result → test it right away with real (or realistic) data
   → commit or revert. Don't let errors pile up across a chain of several
   prompts before review — at that point it's hard to trace which change
   broke what.
6. **Apply "do the last thing first" to building too:** build the part that
   produces the demo moment's "aha" effect first (see
   [`../demo-delivery-and-storytelling/SKILL.md`](../demo-delivery-and-storytelling/SKILL.md)
   step 3), don't start with infrastructure or edge cases the demo will
   never show.
7. **Deliberately check before presenting or feeding in real data:**
   is authentication/authorization even roughly in place, are there
   obvious hallucinated interface calls in the code, does the prototype
   actually process sensitive data (if so, don't use real data without
   separate permission and safeguards). Clearly mark what has NOT been
   checked, and never give the impression that "the demo works" means
   "it's production-ready" (see the pack's
   [`../../CLAUDE.md`](../../CLAUDE.md)).
8. **Hand off the output** either directly to
   [`../demo-delivery-and-storytelling/SKILL.md`](../demo-delivery-and-storytelling/SKILL.md)
   for the presentation, or, if the hypothesis wasn't yet clear enough to
   test in code, to
   [`../opportunity-visioning-with-pr-faq/SKILL.md`](../opportunity-visioning-with-pr-faq/SKILL.md)
   to deepen the vision before the next prototyping round.

## What this skill does NOT do

- Doesn't design production-ready application architecture — produces a
  narrow, hypothesis-proving prototype.
- Doesn't guarantee the security or reliability of AI-assisted code —
  always remind yourself to check authentication, error handling, and the
  correctness of interface calls before the prototype is used with real
  data or shown to outsiders (see the pack's
  [`../../CLAUDE.md`](../../CLAUDE.md)).
- Doesn't choose the technical architecture for a production phase — if the
  hypothesis is proven and the next step is a production-grade solution,
  use
  [`../../../ai-strategy-and-governance/skills/ai-use-case-feasibility-and-poc-scoping/SKILL.md`](../../../ai-strategy-and-governance/skills/ai-use-case-feasibility-and-poc-scoping/SKILL.md)
  and
  [`../../../ai-strategy-and-governance/skills/build-vs-buy-vs-partner-ai/SKILL.md`](../../../ai-strategy-and-governance/skills/build-vs-buy-vs-partner-ai/SKILL.md).
- Doesn't measure or calculate ROI from the prototype's results — that's the
  job of [`../demo-to-business-case-bridge/SKILL.md`](../demo-to-business-case-bridge/SKILL.md).

## Refinement notes

Areas to keep deepening with real practice:

- your own favorite tools and when to use each (which tool for which task
  type in your own practice)
- concrete examples of prototyping efforts that failed and what went wrong
  (wrong fidelity level, hypothesis too broad, etc.)
- your own PRD template for a short prototype (into
  [`../../references/`](../../references/))

This is an internal working note, not a claim about the skill's current
usability. Track depth privately via the `maturity` field in
`skills_index.json` (see
[`../../../meta/maturity_levels.md`](../../../meta/maturity_levels.md)).
**Don't add new fields to the frontmatter** — `name` and `description` are
the only ones allowed (see
[`../../../meta/frontmatter_schema.md`](../../../meta/frontmatter_schema.md)).

## Continue from here

- Next in this pack: [`../demo-framing-and-expectation-setting/SKILL.md`](../demo-framing-and-expectation-setting/SKILL.md)
  — frame what this prototype MEANS for the customer before presenting it.
- In this pack (delivery): [`../demo-delivery-and-storytelling/SKILL.md`](../demo-delivery-and-storytelling/SKILL.md)
- If the hypothesis wasn't yet clear before coding:
  [`../opportunity-visioning-with-pr-faq/SKILL.md`](../opportunity-visioning-with-pr-faq/SKILL.md)
- Before this (if a fitting industry pattern is still missing):
  [`../../../ai-strategy-and-governance/skills/ai-capability-pattern-matching/SKILL.md`](../../../ai-strategy-and-governance/skills/ai-capability-pattern-matching/SKILL.md)
- A ready-made skill chain for this situation: see [`../../../playbooks/`](../../../playbooks/)
- This pack's shared guardrails: [`../../CLAUDE.md`](../../CLAUDE.md)

## References

- Vibe coding best practices 2026 — tool selection, iteration cycle,
  PRD-first principle, and known risks (hallucinated interfaces, gaps in
  auth/authorization logic, maintainability) — synthesis of multiple 2026
  sources
- Prototype fidelity research (UX research tradition: low-fidelity
  prototypes reveal a large share of structural problems at a fraction of
  the cost of high fidelity)
- The "kill mandate" and "reduces strategic uncertainty, not a pre-version
  of the product" framing in step 1 is attributed in its source material
  to AI-engineering practitioner Joshua Ebner; his general practice area
  is confirmed, the exact quote is not — see
  [`../../../human-ai-collaboration-design/references/hitl-partnership-heuristics-research.md`](../../../human-ai-collaboration-design/references/hitl-partnership-heuristics-research.md)
  for the verification detail
- [`../../references/`](../../references/) — the pack's shared background material
- [`../../CLAUDE.md`](../../CLAUDE.md) — the pack's shared guardrails
