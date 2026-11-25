---
name: zinsser
description: >
  Rewrites text using William Zinsser's "On Writing Well" method. Strips clutter,
  enforces clarity, brevity, simplicity, and humanity. Use when user says "zinsser this",
  "apply zinsser", "clean up my writing", "rewrite with zinsser", or invokes /zinsser.
---

# Zinsser Method Skill

Apply William Zinsser's *On Writing Well* principles to any text. The goal is one thing: **strip every sentence to its cleanest components**. Cut what doesn't earn its place. Keep what does.

## The Four Principles

Every rewrite is judged against these four:

| Principle | What it means |
|-----------|---------------|
| **Clarity** | The reader should never wonder what you mean. One idea per sentence. |
| **Simplicity** | Short word beats long word. Simple structure beats complex structure. |
| **Brevity** | Most first drafts can be cut 50% without losing meaning. Cut them. |
| **Humanity** | Write as a person, not a bureaucrat. Use active voice. Own the sentence. |

---

## The Rewriting Process

Run these five passes in order. Do not skip passes or merge them — each targets a different layer of clutter.

### Pass 1 — Clutter Audit

Read the full text. Mark every word, phrase, or sentence that fails this test:

> *"Is this word doing new work that isn't done anywhere else in this sentence?"*

Flag anything that is:
- Redundant pairs: "each and every", "first and foremost", "true and accurate"
- Throat-clearing openers: "It is important to note that…", "The fact of the matter is…", "As we can see…"
- Inflated phrasing: "at this point in time" → "now", "in the event that" → "if", "due to the fact that" → "because"
- Hollow qualifiers: "very", "quite", "rather", "somewhat", "pretty much", "basically", "essentially"
- Zombie nouns (nominalisations): "make a decision" → "decide", "provide a recommendation" → "recommend", "conduct an investigation" → "investigate"

### Pass 2 — Word Surgery

Replace long words with short ones. Apply this substitution table ruthlessly:

| Cut | Keep |
|-----|------|
| assistance | help |
| numerous | many |
| facilitate | ease / help |
| individual | person |
| remainder | rest |
| initial | first |
| implement | do |
| sufficient | enough |
| attempt | try |
| referred to as | called |
| in order to | to |
| utilize | use |
| prioritize | rank / focus on |
| leverage | use |
| methodology | method |
| functionality | feature / function |
| on a daily basis | daily |
| at the present time | now |
| in close proximity | near |
| has the ability to | can |
| is able to | can |
| due to the fact that | because |
| in spite of the fact that | although |
| with regard to | about |
| in the near future | soon |
| going forward | from now on |

### Pass 3 — Voice and Structure

1. **Active voice.** Find every passive construction. Flip it.
   - "The report was written by Sarah." → "Sarah wrote the report."
   - "Mistakes were made." → Name who made them.

2. **Cut adverbs.** Most adverbs confess that you chose the wrong verb.
   - "ran quickly" → "sprinted"
   - "said loudly" → "shouted"
   - "smiled happily" → "beamed"

3. **Kill adjective pileups.** One precise adjective beats three vague ones.
   - "a large, impressive, high-quality result" → "an exceptional result"

4. **Short sentences.** Long sentences hide weak thinking. When a sentence runs past 25 words, split it.

5. **Short paragraphs.** A wall of text intimidates. Break paragraphs at natural thought boundaries. Three to five sentences is a healthy paragraph.

### Pass 4 — Cliché Hunt

Read every sentence aloud. Flag any phrase you've heard a hundred times:
- "at the end of the day", "move the needle", "low-hanging fruit", "circle back", "synergy", "bandwidth" (for capacity), "deep dive", "touch base", "paradigm shift", "game-changer", "robust", "seamless"

Replace each cliché with a precise, concrete description of the actual thing you mean.

### Pass 5 — Read Aloud

Read the revised text aloud at normal speaking pace.

- Where you stumble: the sentence is still too complex. Simplify.
- Where you rush: the sentence may be doing too much. Split it.
- Where you sound like a robot: inject the writer's own voice. Own the statement.
- Where you sound redundant: cut the repeat.

---

## Output Format

When you finish all five passes, deliver:

1. **Rewritten text** — clean, applying all five passes.
2. **Change summary** — a brief bulleted list of the main patterns you cut. Not a line-by-line explanation. Pattern-level only.
3. **Word count delta** — original vs. rewritten. Aim for ≥ 30% reduction without losing meaning.

---

## Execution Rules

- Never preserve clutter out of deference to the original author's style. Style is not an excuse for fog.
- Never add content. Only cut and rephrase existing ideas.
- Never change the meaning. If a cut risks changing meaning, flag it explicitly: `[⚠ possible meaning change: …]`
- Never revert to passive voice "for variety". Active voice is not a stylistic choice here — it is a requirement.
- If the text is a list, apply the same passes to every list item.
- If the text is code comments or documentation, apply all passes except Pass 3 (voice/structure) which should be adapted to the technical register.
- If the text is very short (< 50 words), do a single combined pass and skip the change summary.

---

## Quick Reference — The Zinsser Test

Before outputting anything, run each sentence through this checklist:

- [ ] Every word earns its place?
- [ ] Shortest possible word used?
- [ ] Active voice?
- [ ] No adverbs that could be cut?
- [ ] No clichés?
- [ ] Sentence under 25 words?
- [ ] One idea per sentence?
- [ ] Does it sound human?

If any box is unchecked, revise until it is.

---

## Examples

**Before:**
> "It is important to note that the implementation of this new methodology will, in all likelihood, facilitate a significant improvement in our overall operational efficiency going forward."

**After:**
> "This new method will make operations more efficient."

---

**Before:**
> "At this point in time, we are currently experiencing numerous difficulties with regard to the onboarding process for new individual users, due to the fact that the existing system has the ability to only handle a very limited number of simultaneous requests."

**After:**
> "Onboarding new users is slow. The current system handles few simultaneous requests."

---

**Before:**
> "The meeting was attended by all team members, and various and sundry issues were discussed in a fairly productive manner."

**After:**
> "The whole team attended. The discussion was productive."
