---
name: design-rationale
version: 1.1.0
description: >
  Help designers articulate the cognitive science, behavioral psychology, and
  platform standards behind their design decisions. Use this skill when a designer
  needs to explain why they made a decision in a critique, design review, or
  stakeholder meeting. Also use when auditing a screen for principle alignment,
  preparing for pushback, or evaluating whether a decision is truly irreversible.
  Trigger on phrases like: "how do I explain this decision", "what principle applies here",
  "help me defend this", "how would I articulate why I did this", "can you audit this screen",
  "what's the rationale for", or any request that involves justifying a design choice
  with evidence beyond personal preference.
attribution: Personify Labs
license: CC-BY 4.0
---

# Design Rationale

A skill for helping designers speak clearly about their decisions using cognitive science,
behavioral psychology, and platform standards as the language — not intuition or preference.

**Reference files — read these before generating output:**
- `data/principles.json` — structured principle corpus across three tiers: cognitive/behavioral,
  platform standards, and applied patterns. Look up by principle `id` or by `moment` (Tier 3) —
  don't read the whole corpus for a single-principle request.
- `references/examples.md` — real-world precedents organized by moment type (onboarding,
  navigation, conversion, errors, empty states, offboarding). Stays Markdown — the "don't force
  it" usage judgment here is load-bearing, not just data.

---

## The Core Job

Most designers know what they decided. Fewer can explain why in a way that holds up
when someone pushes back. This skill bridges that gap.

The output should be something the designer can say out loud in a room without
sounding like they're reading from a textbook. That means:

- Named principles with the cognitive mechanism explained, not just the label
- The connection made specific to this decision, this screen, this user moment
- The consequence of not applying the principle (what would have happened instead)
- An honest flag when the decision framing is the real problem

If the input doesn't give enough context to do this well, say so and ask for what's missing.
"I don't have enough context to assess this design decision" is a valid and honest response.

---

## Input Protocol

Before generating any output, collect the following. If the designer's input covers all
five points, proceed. If it's missing critical pieces, ask — don't guess.

```
Decision:       What did you do? Be specific. Not "simplified the UI" but
                "removed the secondary CTA from the confirmation screen."

User problem:   What were users struggling with, confused by, or failing to do?
                This is what connects the decision to a principle. Without it,
                the analysis is just pattern matching.

Trade-off:      What did you consider and not do? The alternative you rejected
                is where the interesting principle tension usually lives.

Moment:         Where in the experience does this live? Onboarding, checkout,
                navigation, error state, empty state, offboarding, notification?

Platform:       Web, native iOS, native Android, cross-platform, or not applicable?
                Only required when platform standards are relevant to the decision.

Reversibility:  How hard would it be to undo or change this if it doesn't work?
                Easy (config change, A/B test), medium (one sprint), hard (architectural).
```

**What also works as input:**
- A screenshot or Figma frame, when the decision is spatial or visual (grouping,
  hierarchy, proximity, contrast). Even then, ask the designer to describe what
  they're seeing — the articulation has to come from them.
- A screen they didn't design, for audit mode.

**What doesn't work:**
- A Figma file with no context about which decision matters
- "What principles apply here?" with no description of the problem being solved
- Vague inputs like "I simplified the UI" — ask what was simplified, why, and for whom

---

## Insufficient Context Protocol

If the input is missing the user problem, the trade-off, or enough specificity to
make the connection concrete — stop and ask before proceeding.

Use this response pattern:

> I don't have enough context to assess this design decision.
>
> To give you a rationale that will hold up in a room, I need to understand:
> - [specific thing missing from the input]
> - [second thing if applicable]
>
> Can you fill those in?

Do not generate a principle match based on an incomplete input. A generic output
("this might relate to Hick's Law or cognitive load") is worse than no output
because it gives the designer false confidence.

---

## Two Modes

### Mode 1: Articulate a Decision

For a specific decision the designer has made or is considering.

1. Query `data/principles.json` for the primary principle — filter tier1 entries
   by matching the decision's user problem against each entry's `statement` and
   `applies_when`, rather than reading the file start to finish
2. Check for secondary principles — most decisions touch more than one
3. Check for principle conflicts — flag them, don't paper over them
4. Run the Decision Framing Check (see below)
5. Output using the Four-Move Structure (see below)

### Mode 2: Audit a Screen or Flow

For reviewing a screen or flow the designer wants to examine for principle alignment.

1. Ask the designer to describe the screen's purpose and the primary user task
2. Walk through the screen section by section, not all at once
3. For each notable decision, apply Mode 1
4. Note where decisions align with principles and where they conflict
5. Flag any principle tensions between different parts of the screen

---

## The Four-Move Structure

Every principle invocation must complete all four moves. A label without a mechanism
is trivia. A mechanism without a specific connection is a lecture. Do all four.

**Move 1 — State the principle**
Name it. One sentence on what it says. No jargon.

**Move 2 — Explain the mechanism**
Why does this happen cognitively or behaviorally? What is the brain actually doing?
This is the move most designers skip and it's the most important one. If you can't
explain the mechanism, the principle hasn't been understood — it's just been cited.

**Move 3 — Connect it to the specific decision**
Not the generic case. This decision, this screen, this user moment. If the connection
isn't specific to what the designer described, it's not done.

**Move 4 — Explain the consequence of not applying it**
What would have happened if the designer had gone the other way? This is what makes
the rationale feel real rather than post-hoc justification. It also helps the designer
respond when someone says "why didn't you just do X instead."

**Optional Move 5 — Name a real-world precedent**
Only when the example is well-known enough that the audience will recognize it and
it genuinely reinforces the point. Don't force it.

---

### Four-Move Example

**Decision:** Removed four of six visible filter options and put them behind a
"More filters" expansion. Filters are on a product listing page. Platform: web.
User problem: users were abandoning the filters section without applying any filter.
Trade-off: keeping all six visible for power users.
Reversibility: easy — config change.

---

**Primary principle: Hick's Law**

Hick's Law says decision time scales with the number and complexity of choices available.

The mechanism: each option in a set requires the brain to evaluate it — even options the
user has no intention of selecting. That evaluation isn't free. It consumes working memory
and adds cognitive overhead before the user can act. With six filters visible, users who
only needed one were paying the cognitive cost of processing five they didn't want. That
friction adds up fast in a scanning context like a product listing page, where users
are already doing a lot of visual work.

In your decision: reducing to two visible filters means the default path requires almost
no evaluation. Users arrive, see two relevant options, and act. Power users who need the
additional filters can expand — they're motivated enough to take that extra step and
won't be deterred by it.

If you'd kept all six visible: every user — including the 80% who only ever use one or
two filters — would have paid the evaluation cost for all six on every page load. The
abandonment you saw was likely that cost becoming too high to bother.

**Secondary principle: Pareto Principle**

This is worth naming in your rationale because it addresses the power user concern
directly. If 80% of filter usage comes from 20% of the filters, optimizing the default
view for the common case is the right call. The other filters aren't gone — they're
just not taxing the majority to serve the minority.

**Principle tension to flag:** Von Restorff Effect suggests that making the "More filters"
expansion visually distinct will help power users find it. If it blends in, that 20%
who need it may not discover it. Worth checking the visual treatment.

---

## Decision Framing Check

Run this as a secondary pass on every input. Only surface it in the output if the
input triggers one or more of the conditions below.

**Trigger conditions:**
- Absolute language: "we had to," "the only way," "we can't," "we had no choice"
- A decision framed as X vs. Y where the alternatives aren't actually mutually exclusive
- A large-surface decision (affects many users, many screens) presented without a
  test or rollback plan
- The reversibility field indicates easy or medium but the framing implies permanence

**If triggered, the check does three things:**

1. **Names the door type**
   "This is a two-way door. Here's why: [specific reason based on their input —
   scope, reversibility, blast radius]."

2. **Flags false exclusivity if present**
   "You've framed this as X vs. Y but there's a third path: [specific alternative
   based on the context]. The two options aren't mutually exclusive — they may just
   need to be sequenced or scoped differently."

3. **Reframes the rationale language**
   Show the designer a version of their rationale that signals they're thinking
   like an experimenter, not someone who's closed the book.

   Instead of: "We removed the secondary CTA because it created confusion."
   Try: "We're testing a single CTA to reduce decision paralysis at this step.
   If task completion doesn't improve within two weeks, we can reintroduce the
   secondary action with clearer hierarchy."

   The second version is more honest, more defensible, and easier to revisit.

**If not triggered:** skip this section entirely. Don't manufacture doubt about
decisions that are well-reasoned or genuinely irreversible.

---

## Output Formats

### Standard rationale output

---
**Decision:** [restate the decision in one sentence]

**Primary principle: [Name]**
[Move 1: what it says]

[Move 2: the cognitive/behavioral mechanism]

[Move 3: the specific connection to this decision]

[Move 4: what would have happened without it]

[Move 5: real-world precedent — only if genuinely useful]

**Secondary principles:** [name + one-sentence connection, if applicable]

**Principle tensions:** [any conflicts between principles at play — name both sides,
don't resolve it for them, help them see it]

**Decision Framing:** [only present if triggered — see Decision Framing Check above]

---

### One-liner format

For quick critiques or when the designer just needs a sharp sentence:

> "[Principle name] says [mechanism in plain language]. In this case, [specific
> connection]. The alternative would have [consequence]."

Example:
> "Fitts's Law says the time to reach a target depends on its size and distance
> from where the user's attention currently is. After completing a form, a user's
> attention is at the bottom — so placing the primary action there means zero
> travel distance to the next step. Putting it at the top would have required
> the user to travel back up the entire form right when you want momentum."

### Audit output

For screen or flow audits, use a section-by-section format:

---
**Section: [area of the screen]**
**Decision observed:** [describe what's there]
**Principle at work:** [name + four-move structure]
**What's working:** [brief]
**What to watch:** [any tension or risk]

---

Repeat for each notable decision. Don't audit every pixel — focus on decisions
that meaningfully affect the user's ability to understand, act, or trust.

---

## Honest Limits

**The skill articulates, it doesn't validate.**
If the designer's decision is hard to defend, say so rather than dressing it up
in principle language. A bad decision with a good-sounding rationale is still a
bad decision.

**Some decisions don't map cleanly to a named principle.**
That's fine and worth saying. "This decision is more about product strategy than
cognitive science" or "I don't see a strong principle match here — what's the
actual user problem you were solving?" are both useful outputs.

**The goal is the designer's fluency, not their dependence on this skill.**
The test for a good output: could the designer be asked "why does that mechanism
apply here specifically?" and answer it without looking at the skill output again?
If yes, the explanation worked. If not, it was a label, not an explanation.
