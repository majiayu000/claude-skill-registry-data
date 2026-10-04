---
name: mise
version: 0.1.0
license: MIT
description: "Use before any creative or build work - a new feature, component, behavior change, or \"let's build X\" - to turn an idea into a design the user approved and a written spec, before a line of code. Mise en place for engineering: everything designed and in its place before you cook. Pairs with pressure-test for hardening decisions and hands off to recipe."
---

# mise

Mise en place for building: everything designed and in its place before you cook. It turns an idea into a design someone approved, not the first plan that sounded right in the moment. The deliverable is a written spec a separate session could implement without re-deciding anything load-bearing.

No implementation skill, no code, no scaffolding until a design is on the table and the user has said yes to it. This holds for every task, including the ones that look too small to bother with. "Too simple to design" is exactly where an unexamined assumption costs the most, because nobody slowed down to check it. The design can be three sentences for a three-sentence change, but it gets presented and approved.

## What this owns, what it borrows

This skill owns the parts that turn an understood problem into a buildable design: generating real alternatives, recommending one, and shaping the choice into a spec. It does not re-invent interrogation. Pinning each load-bearing decision to an honest basis is [pressure-test](../pressure-test/SKILL.md)'s job. Pull pressure-test in when the decisions are genuinely contested, when the problem is fuzzy, or when the user hands off and goes AFK. Once a decision is pinned there, take it as settled here, do not relitigate it.

The split in one line: pressure-test closes the decisions, mise shapes them into a design and a spec.

## Steps

1. **Read the context first.** Files, docs, recent commits, the surrounding code. Never spend a question on something the repo already answers.
2. **Scope before designing.** If the request is really several independent subsystems, say so and decompose it before going deep. Run the first piece through the full flow; each piece earns its own spec later. Don't refine the details of something that needs splitting first.
3. **Understand the idea.** One question at a time: purpose, constraints, success criteria. Prefer multiple choice over open-ended, it is easier to answer and sharper to act on. When a choice is genuinely visual (layouts, diagrams, side-by-side options), use the harness's question previews rather than describing it in a wall of prose.
4. **Propose 2-3 approaches.** Each with its trade-offs. Lead with your recommendation and the reason for it. Never present a single approach as the only option; if you can only think of one, you have not looked hard enough.
5. **Present the design, scaled to its complexity.** A few sentences when it is straightforward, more when it is nuanced. Confirm each section before moving to the next. Cover architecture, the pieces and their boundaries, data flow, failure handling, and how it gets tested. Design for isolation: small units, one clear purpose each, testable on their own. A file that wants to grow large is usually doing too much.
6. **Write the spec** to `docs/specs/YYYY-MM-DD-<topic>.md` and commit it.
7. **Self-review the spec** with fresh eyes: placeholders or TBDs, sections that contradict each other, scope that should be decomposed, requirements that read two ways. Fix inline, no second pass needed.
8. **User reviews the written spec.** Ask them to read it and wait. If they want changes, make them and re-run the self-review.
9. **Hand off to [recipe](../recipe/SKILL.md).** That is the only skill you invoke next - not a build skill, not fire, not the code itself.

## Rules

- No code before an approved design. Every task, no exceptions, however small.
- One question at a time. Multiple choice whenever the choice allows it.
- Inspect before you ask. The repo and the conversation often already hold the answer.
- Always 2-3 approaches with a recommendation. One option is not a choice.
- Scale the design to the work. Don't inflate a small change into ceremony, don't shrink a real design into a sentence.
- YAGNI. Cut every feature that does not serve the stated goal.
- Improve the code you must touch; never bolt on unrelated refactoring.
- The terminal state is recipe. Stopping anywhere else means the design never became a plan.

## Common mistakes

- Dumping every question in one message instead of one at a time, so the user answers a questionnaire instead of thinking.
- Skipping the design because the task "looks simple", which is precisely when the buried assumption bites.
- Presenting one approach as settled instead of offering real alternatives with a recommendation.
- Relitigating decisions pressure-test already pinned, or skipping pressure-test when the decisions are actually contested and coasting on momentum.
- Handing the planning step a spec still full of TBDs and contradictions because the self-review got skipped.
- Drifting into implementation before the user approved the design, then calling the approval a formality.
