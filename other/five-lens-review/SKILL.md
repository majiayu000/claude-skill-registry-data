---
name: five-lens-review
description: "Evaluate a product-direction question through five expert lenses, Senior PM, Senior Product Engineer, Senior Product Designer, Senior Design Engineer, and a realistic end user, then synthesize the conclusions into a single recommendation. Use whenever a user-facing decision has multiple competing constraints (lifecycle behavior, data-model trade-offs, destructive actions, UX choices that touch retention) and a one-perspective answer would miss something. Trigger phrases: 'what should we do about X', 'what happens when the user Y', 'how should we handle this case', 'I need to think through this', 'help me decide', 'we don't have answers for these questions', 'spawn personas', 'evaluate from all POVs'. Especially use this when the user is mid-implementation and surfaces an edge case the spec didn't cover, that's when single-perspective reasoning silently locks in the wrong default."
---

# Five-Lens Review

Spawn five specialized subagents in parallel, Senior PM, Senior Product Engineer, Senior Product Designer, Senior Design Engineer, and a realistic end user, each examining the same product-direction question through their own discipline's lens. Then synthesize their convergent themes, surface their disagreements, and produce a single actionable recommendation.

The output is a structured memo the user can decide against, not a slide deck of opinions.

---

## When this skill is the right tool

Use it when ALL of these are true:
- There's a **user-facing decision** at stake (not a pure refactor or internal optimization)
- The decision has **multiple competing constraints** (data integrity vs UX simplicity, retention vs implementation cost, spec-fidelity vs user reality)
- A single-perspective answer would **silently lock in a bad default** that's expensive to reverse later
- The user has surfaced an edge case the spec didn't cover, OR is asking "what should we do about X"

Skip this skill for:
- Pure implementation questions ("how do I refactor this loop"), that's not a product question
- Decisions where the user already has a clear preference and just wants execution
- Bug fixes with one obvious correct answer
- Anything where running five parallel subagents would be over-engineering the question

The right test: would the user feel like the decision benefits from being interrogated from five disciplines? If yes, use this. If you're not sure, ask.

---

## Step 1: Frame the decision precisely

Before spawning anything, write a one-paragraph **decision context** that every persona will receive. The personas have no session memory; the brief is the only thing they see. It must contain:

- **What is the product/feature?** (3-5 sentences of background)
- **What is the current behavior?** (what code/design does today, with file paths or specifics)
- **What is the question or edge case?** (the literal thing being decided)
- **What constraints already exist?** (spec rules, voice guidelines, architectural patterns, deadlines)

If the question is ambiguous, ask the user to clarify before spawning. A vague brief produces vague memos that don't reconcile.

---

## Step 2: Spawn five subagents in parallel

In a **single message**, dispatch five subagent calls using the `Agent` tool (or `Task` tool / whatever the runtime exposes) with `model: "sonnet"`. All five receive the **same decision context** plus a persona-specific lens. They run concurrently and notify on completion.

Each persona's brief should follow this shape:

```
Adopt the lens of a [PERSONA]. Your job is to [PERSONA-SPECIFIC GOAL].

## Context (you have no session memory)
[The shared decision context from Step 1]

## The questions to think through
[Enumerated questions, 3-7 of them, framed for this persona's discipline]

## Your [PERSONA]-specific lens
[3-6 bullets pointing at what this persona uniquely contributes, see Step 3]

## Deliverable
[Structured memo shape, see Step 4. ~700-900 words.]

End with: "[A one-line takeaway prompt the persona must answer]"
```

The five lenses, with what each uniquely contributes:

### Senior Product Manager
**Goal**: Surface the right questions, articulate trade-offs, recommend a decision framework from product-strategy lens. Do NOT write code or get into implementation detail.
**Unique contribution**: Which decisions are user-retention critical vs nice-to-have. What's the cheapest v0 answer + the eventual right answer. Which choices ENABLE future features vs LOCK US OUT. GDPR / data-retention concerns. What must decide NOW vs can defer.
**End with**: "If we don't decide X, we'll regret it because Y."

### Senior Product Engineer
**Goal**: Identify technical implications, data-model trade-offs, migration paths, edge cases. Get specific about implementation consequences of different decisions.
**Unique contribution**: Which decisions create migration debt later. Where query complexity explodes. What testing gaps each decision creates. Indexing implications. Cheapest implementation that doesn't paint into a corner. Schema additions (add now vs defer).
**End with**: "The one schema change I'd push to land THIS phase to avoid pain later is X."

### Senior Product Designer
**Goal**: Design the user's mental model, surface where current behavior contradicts intuition, recommend microcopy + visual decisions.
**Unique contribution**: Where the user's mental model BREAKS with current behavior. Microcopy needed at each transition. IA decisions, new sections/views needed. The right level of nuance (surface everything vs hide complexity). Modal/drawer patterns for the explanatory moments. Voice-of-product alignment.
**End with**: "The one design decision I'd make NOW to prevent the most confused-user moments later is X."

### Senior Design Engineer
**Goal**: Recommend how to IMPLEMENT design decisions in concrete component patterns, state machines, and reactive UI that hold up across the feature's lifecycle.
**Unique contribution**: Component-pattern recommendations for the consequences-confirmation moments. State shape, where filters/derived values live so changes don't ripple. Reactive pitfalls and the patterns that prevent them. Mobile-first considerations. Where to extract shared bases vs duplicate. Honest "where can we get away with less."
**End with**: "The one component pattern I'd extract NOW to keep us honest is X."

### Realistic End User
**Goal**: A SPECIFIC person, not a focus-group abstraction. Adopt a real persona matching the product's audience (the framer of the brief should describe them: age, job, situation, what they came to the app for, what they fear losing).
**Voice**: First person. Honest about what they'd actually want, what would confuse them, what would make them uninstall.
**Unique contribution**: What would make them uninstall (worst case per transition). What would make them fall in love (best case). Where they'd be CONFUSED returning after time away. Tolerance for confirmation modals vs silent actions. The "I just want it to work" expectations that need no input.
**End with**: "If you can only get ONE of these right, get X right because Y."

---

## Step 3: Wait for all five, then synthesize

Do not try to start synthesizing until all five are back. Partial syntheses based on the first 2-3 responses miss the cross-discipline convergence that's the whole point.

When the last persona notifies completion, write the synthesis. Structure it like this:

```
## Convergent themes (where N+ lenses agree)
[A table OR a series of headers. For each convergent decision: the conclusion, which lenses support it, and the killer quote that captures why.]

## Disagreements worth surfacing
[Cases where two lenses propose incompatible answers. Show both with rationale. Recommend a resolution OR escalate the choice to the user.]

## What today's code/design gets wrong
[Concrete current-vs-recommended table for any behavior the personas converged on as broken.]

## The architecture/path that makes it cheap
[If the personas surfaced a unifying implementation pattern (a shared resolver, a single source of truth, an extracted modal base), name it explicitly.]

## What the spec gets wrong (if applicable)
[If the personas surfaced a place where the spec doc no longer matches the right answer.]

## The one-paragraph "if you only do one thing" recommendation
[The single highest-leverage decision distilled into one paragraph the user can act on without reading the rest.]
```

---

## Step 4: Present back as written prose, not bullet salad

After synthesizing, deliver the recommendation to the user as **flowing written prose** (5-10 paragraphs), not as nested bullet points. The user just asked a strategic question; they need a written answer they can sit with, not a slide deck.

Each paragraph should:
- Cover one cohesive theme
- Reference which lenses converged on it (briefly, "the PM, Engineer, and User all converged on X")
- Land on a specific recommendation, not a hedge

Reserve bullet points and tables for places where the structure is genuinely tabular (e.g., "what today does vs what it should do").

End with **the one-sentence summary**: the single line that, if the user only reads one thing, captures the whole synthesis. Lead with the action, then the reason.

---

## Fallback when parallel dispatch isn't available

If the runtime exposes no `Agent` / `Task` tool (some nested-subagent contexts strip it), don't abort the skill, fall back to writing all five persona memos as five separate fully-in-character passes in a single batched message, then synthesize. The cross-pollination value drops but the multi-discipline coverage is preserved. State the fallback explicitly in your output so the user knows the parallelism was conceptual rather than literal.

## Anti-patterns: refuse these

- **Sequential persona calls when parallel dispatch IS available.** When the runtime has `Agent` / `Task`, all five MUST run in parallel via a single dispatch message. Sequential burns 5× the wall-clock time and prevents fresh-eye cross-pollination. Use the fallback above only when the tool genuinely isn't accessible.
- **Reporting success without verifying outputs were written.** If the workflow promises N output files, check each one exists on disk before reporting completion. A subagent claiming "all 6 files written" without verification is a silent-failure mode that wastes the user's review cycle.
- **Synthesizing before all five return.** Tempting when the early personas have strong opinions; produces a synthesis that misses the discipline that arrives late.
- **Generic personas.** "A user" is not a persona. "A 38-year-old solo creator who joined 4 months ago because their fiction practice has been dark for 6 weeks" is. Specificity drives honest answers.
- **Three-of-five lenses.** The combination of all 5 is the point. Each catches what the others miss. Skipping the User lens because "it's obvious" is the most common failure mode and produces the most user-hostile recommendations.
- **Asking the user to read 5 separate memos.** The synthesis IS the deliverable. The individual memos are intermediate artifacts. If the user wants to read them, they can scroll up to see each notification.
- **Closing with "what would you like to do".** End with a concrete recommendation. If a follow-up choice is needed, structure it as a small set of options the user can choose between, not an open prompt.
- **Using this skill for implementation questions.** Refactors, bug fixes, perf optimizations, these don't need five lenses. If the question is "how do I implement X" rather than "what should X be", stop and use a more focused skill instead.

---

## The cost-benefit honest take

This skill spawns 5 parallel subagents, substantial token + wall-clock cost. The value comes from catching the user-hostile default that one-perspective reasoning silently locks in. Use it for decisions you'd regret getting wrong; don't use it as a default review pattern. A good heuristic: if reversing the decision later would require a data migration or a user-trust apology, this skill earns its cost. If reversing it would just mean changing a button label, it's overkill.
