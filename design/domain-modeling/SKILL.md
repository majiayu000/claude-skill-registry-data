---
name: domain-modeling
description: "Use when the work introduces or reshapes a domain concept: agree the vocabulary and where the rules live before designing the schema or the API. Runs before archi."
---

# domain-modeling

Step 3 of the pipeline (`WORKFLOW.md`), before `archi` and before `api-design`. Those two ask *where
does this plug in* and *what's the contract*. This one asks the question underneath: **what is this
thing, and what's true about it**. Getting that wrong produces a schema and an API that are both
faithful implementations of a misunderstanding.

## When
As soon as the work introduces a new domain concept, or touches one that's showing strain: a status
field that keeps gaining values, a rule reimplemented in three places, a name that means different
things to two teams. Not for a straightforward addition to a concept that's already clear.

## Steps

### 1. Name things the way the business says them
1. **Use the words the business uses**, in code as in conversation. When the business says "quote"
   and the code says "draft order", every discussion needs a translation, and translations drift.
2. **One name, one meaning.** If a word means two things depending on the screen, that's two
   concepts wearing one name: name them separately. This is the most common finding and the most
   often waved away.
3. **Write down the words you rejected** and why. The next person will otherwise reopen the same
   debate with no memory of it.

### 2. Find the rules and decide where they live
1. **List what must always be true** about the concept, in plain sentences ("an order can't be
   validated without a customer", "a contract's end date is never before its start"). These are
   invariants, and they are the model.
2. **Decide where each one is enforced**, and prefer the narrowest place that can guarantee it: the
   type or the schema if it can (a non-nullable column, an enum), otherwise a single point in the
   domain code. A rule enforced in the UI only is a suggestion.
3. **A rule duplicated across layers will diverge.** If it must exist in two places (a frontend check
   for feedback, a backend check for truth), say which one is authoritative and treat the other as
   ergonomics.

### 3. Model state as states, not as flags
1. **A concept with a lifecycle has a state**, not a pile of independent booleans. Three booleans
   describe eight combinations, and usually only four are legal: the other four are bugs waiting for
   the right sequence of clicks.
2. **List the legal transitions**, and what triggers each. A status enum with no transition rules
   just relocates the problem into whoever writes the update.
3. **Model the states that exist, including the awkward ones**: "awaiting approval", "partially
   delivered", "cancelled but invoiced". A model that only covers the clean path pushes reality into
   nullable columns and special cases.

### 4. Draw the boundary
1. **Say what the concept does not cover.** A boundary stated once prevents the slow accumulation
   where an entity ends up owning half the domain.
2. **Check the concept against the existing model** (this is where `archi`'s dedup pass starts): a
   "new" concept is often an existing one under a different name, or a state of it.

## Output / checkpoint
The vocabulary settled, the invariants listed with the place each is enforced, the states and legal
transitions, and the boundary. If the decision is significant or contested, it becomes an ADR
(`documentation-adr`) so the reasoning survives; otherwise it feeds straight into `archi`.

## Guardrails
- **This step produces understanding, not a schema.** Don't design tables or endpoints here: doing so
  freezes the model around the first storage idea.
- **Don't invent domain rules to fill a gap.** An unanswered question about the business goes to the
  business. A guess written into an invariant is the most expensive kind of wrong, because everything
  downstream then depends on it.
- Renaming an established concept across an existing codebase is a **coordinated refactor and a human
  decision**, never a quiet rename inside a feature branch.
- Timebox it. This block exists to prevent a week of rework, not to become the week.

## Origin
Rewrite of the `domain-modeling` idea from a recognised market skill author, which sat in our backlog
unwritten because it looked like it overlapped `documentation-adr`. Reading it again, the overlap is
only in the output: the ADR block is a *recording* template, and nothing in the framework covered
*reaching* the decision. Vocabulary-follows-the-business and invariants-as-the-model are
domain-driven-design staples rather than anyone's private invention; the states-not-flags rule and
"list the awkward states" come from our own repeated finding that boolean combinations encode illegal
states, including the auth case where "awaiting approval" was flattened into "login failed"
(`auth-session-conventions` §4.6).
