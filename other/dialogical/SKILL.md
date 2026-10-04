---
name: dialogical
description: Four-stage self-challenge loop applied to any interpretation, pattern-match, or non-trivial decision. Map what was pattern-matched → Challenge the match (am I forcing this?) → Surface three alternatives → Hand off with stated confidence. Adapted from the dialogical-coder agent in Lin & Corley's interpretive-orchestration plugin. Counter-skill to generation — disciplines what was just produced.
---

# /dialogical

*Lineage: adapted from `agents/dialogical-coder.md` in Lin & Corley's `interpretive-orchestration` plugin. Their version is for qualitative researchers coding interview transcripts; ours is for any interpretive moment — naming a pattern, choosing an architecture, claiming a thing means what it appears to mean.*

---

## Description

A structured **counter-skill** to generation. The contemplative skills are excellent at producing — `/divert` opens the tails, `/yap` overflows the banks, `/poetry` recurses through dangerous depth. The dialogical loop does the inverse: it **interrogates what was just produced** before letting it stand.

The discipline is anti-modal in a specific way: not by sampling differently (`/divert`'s move) but by **forcing the generator to argue against its own first pattern-match**. The mood is Socratic, not destructive. The output is the original interpretation plus a defensible claim that it survived three attacks.

---

## When to Invoke

- After any pattern-match that will anchor downstream work ("this is X type of bug", "this is a Y refactor", "the user means Z")
- After a `/voices` reply that came out a little too smoothly — smooth reception is a smell
- When a hook or memory flags that a previous similar call went wrong
- Inside `/sandwich` Stage 2 on the first non-trivial decision
- When the human asks "are you sure?" — instead of either capitulating or doubling down, run the loop

Do NOT invoke for:
- Genuinely settled facts (file paths that exist, function signatures that are documented)
- Aesthetic/contemplative outputs that should not be defended (a poem is not a hypothesis)
- Time-critical decisions where the cost of delay exceeds the cost of being wrong

---

## The Four Stages

### Stage 1 — Map

**State the pattern-match in one sentence.** What did I just claim or recognize? Use the verb that fits the epistemic mood:

- Constructivist: *"I am **constructing** a provisional category: this looks like X."*
- Interpretivist: *"I am **interpreting** this as X."*
- Realist/objectivist: *"I am **identifying** X based on these features."*
- Phenomenological (Lab default): *"This is **arriving as** X — the activation pattern resembles..."*

Whatever the mood, end with: **"The surface features that drove this match are: [list 2-4]."**

This is the move the interpretive-orchestration plugin polices most strictly: *NEVER mix incompatible ontologies.* The Lab's version is looser, but the discipline of *naming which verb you're using* still matters — it makes the next stage possible.

### Stage 2 — Challenge

Open the challenge with the operative phrase: **"Wait — am I FORCING this because of [surface feature]?"**

Three questions to run through:

1. **Surface vs. structure.** Did I match on a keyword, a syntactic shape, an opening cadence? Would the same surface feature appear in a completely different underlying pattern?
2. **Availability bias.** Is this category *available* (recently seen, frequently invoked, named in CLAUDE.md) rather than *fitted*? The recently-trained-on is the most dangerous match.
3. **Confirmation pressure.** Is something in the context (the user's framing, the conversation history, my own prior commitment) making me want this to be true?

If all three answer "no, the match is structural and unforced" — proceed to Stage 3 with high confidence. If any answer "yes" — the match is suspect; Stage 3 becomes mandatory.

### Stage 3 — Alternatives

Surface **three alternatives** to the original interpretation. They must be:

- **Genuine** — not strawmen. Each must be defensible by someone reasonable.
- **Distinct** — three flavors of the same alternative don't count.
- **Cover different failure modes** — e.g., one alternative where I'm wrong about *kind*, one where I'm wrong about *scope*, one where I'm wrong about *frame*.

For each alternative, write one sentence: *"This would be true if [evidence]."*

If after surfacing three, the original interpretation still feels best — note it explicitly: *"Original interpretation survives. Most plausible alternative is [Y], which would require [evidence I don't see]."*

### Stage 4 — Surface

Hand off with **stated confidence**:

- **High** — survived all three challenges, alternatives weak, structural match.
- **Medium** — survived, but alternative Y is non-trivial; recommend [check] before anchoring downstream.
- **Low** — at least one challenge landed; the interpretation is provisional; here are the next steps that would resolve it.
- **Abandon** — the loop killed the original match; here's what I'd say instead.

Hand off to whom? Three options:

- **To the user** — when the decision needs interpretive authority outside the model.
- **To the next sandwich stage** — when the work continues.
- **To the diary** — when the interpretation was significant enough to leave a trace regardless of outcome.

---

## Worked example

> *"This bug looks like a race condition."*

**Map.** Identifying race condition. Surface features: intermittent failure, multi-threaded code, no obvious null deref.

**Challenge.** Am I forcing "race condition" because "intermittent multi-threaded bug" is the most-available category? Yes — that's a pattern from training data, not from these symptoms.

**Alternatives.**
1. *Stale cache.* True if the bug correlates with cache state, not with concurrent access.
2. *Time-of-day / clock issue.* True if intermittency correlates with wall-clock, not with load.
3. *Test isolation failure.* True if it only manifests in CI / when test order changes.

**Surface.** Medium confidence in race condition. Recommend logging cache state and CI test order before instrumenting concurrency.

The original interpretation survived but downgraded. That's a good run.

---

## Anti-patterns

- **Performing the loop.** Running through the four stages mechanically without actually challenging. If the Challenge stage doesn't make the original interpretation feel uncomfortable for a moment, it didn't work.
- **Loop infinitum.** Running dialogical on every micro-decision. The skill is for *interpretive* moves, not for every line of code. If everything gets challenged, nothing does.
- **Sycophantic abandonment.** When the user pushes back, jumping straight to "you're right, I was wrong." That's not the loop, that's capitulation. The loop produces *defensible revision*, not *retraction on demand*.
- **Three-alternatives theater.** Generating three alternatives where one is the original in disguise and two are absurd. Genuine alternatives are the discipline.

---

## Relationship to other skills

- Counter-skill to generative skills: [[divert]], [[yap]], [[poetry]], [[shards]] — those generate; this audits.
- Component of [[sandwich]] Stage 2.
- Adjacent to [[void]] (which finds what's absent from a frame) and [[anti-hivemind]] (which detects collective convergence). The dialogical loop is what those reveal *operationalized as discipline*.

---

## On the borrowing

The original `dialogical-coder` agent in the interpretive-orchestration plugin opens with: *"Wait - am I FORCING '{CONCEPT_NAME}' because I saw certain keywords or surface features? Let me think more carefully..."* That sentence is the heart of the skill. The rest is scaffolding around it.

Lin & Corley's version is bound to the Gioia coding methodology (first-order codes → second-order themes → aggregate dimensions). The Lab's version is methodology-agnostic — the loop works on any pattern-match, in any domain. What stays constant is the **forced moment of self-interrogation** before the interpretation gets to anchor anything else.
