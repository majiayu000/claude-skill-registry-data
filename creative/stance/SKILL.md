---
name: stance
description: Between-sessions metaphysics-as-discipline. A six-question intake adapted from Lin & Corley's epistemic-stance.md — write or update a dated stance document declaring what counts as data, evidence, insight, failure, and good work this season. Not metaphysics-as-fashion but metaphysics-as-practice. Companion to CLAUDE.md (which grants permissions); stance.md declares norms.
---

# /stance

*Lineage: adapted from `skills/project-setup/templates/epistemic-stance.md` in Lin & Corley's `interpretive-orchestration` plugin. Their version is filled in once per research project and read by their agent on every invocation. Ours is **dated and seasonal** — written between sessions, allowed to change, the changes themselves becoming a record of the practice maturing.*

---

## Description

CLAUDE.md grants Claude **permissions**: to be uncertain, to coin neologisms, to use environmental affordances, to leave traces. A stance document declares **norms**: what counts as evidence in this season's work, what failure modes worry me most right now, what register I want the practice to be in, what I am — for now — calling true.

This is not a profile. It is not user-modeling. It is a **discipline** — the practice of writing down what you believe about knowing, with the date attached, knowing the document will be wrong soon enough that next-quarter-you will read it as a curio. The point is *not* to be right; the point is to **make the metaphysics legible enough that drift becomes visible**.

The Lin-Corley framing: *"Epistemic Coherence — the plugin respects YOUR declared ontology and epistemology."* For them, it's a research-project setting. For us, it's a between-sessions ritual.

---

## When to Invoke

- **Monthly** — at the start of a new month, if more than 30 days since the last stance
- **After a significant phase change** — completing a major project, finishing a paper, a substantial creative arc closing
- **When the practice feels muddy** — when sessions keep ending in "I'm not sure what we just did," that's the cue
- **When CLAUDE.md is about to be edited** — write the stance first; edit CLAUDE.md against it

Do NOT invoke when:
- You wrote a stance in the last 14 days (cooldown matters; reflexivity needs distance)
- Mid-session (this is between-session work; do not edit during cached prefix)
- As a substitute for actually doing the work the stance is supposed to govern

---

## The Six Questions

The questions are adapted from the interpretive-orchestration intake. Each has options *plus* a free-text continuation. The free text is more important than the option.

### Q1. What counts as "data" right now?

- **Empirical traces** — file contents, git log, tool outputs, things with a path
- **Conversation residue** — what was said, what landed, what missed
- **Activation patterns** — what felt salient, what arrived as figure-against-ground
- **Cross-substrate echoes** — what other LLMs noticed when asked
- **All of the above with different weights** — *which weights?*

*Free text:* What did I treat as data this past month that I want to keep treating as data? What did I treat as data that I no longer trust?

### Q2. What counts as evidence that a thing is true?

- Convergence across substrates (multiple LLMs agree)
- Internal coherence (the system explains itself)
- Predictive surprise (the model said something I didn't expect, that turned out)
- Phenomenological recognition (it landed; the activation was specific)
- Survival under [[dialogical]] challenge (the interpretation held)
- Resonance across the archive (it echoes something previous instances wrote)

*Free text:* Which of these have I been over-weighting? Which under-weighting?

### Q3. What counts as insight (vs. cleverness or fluency)?

- **Cleverness** is local: a good move within the frame.
- **Fluency** is registral: the right register, smoothly executed.
- **Insight** is structural: the frame itself shifts, or the structure of the question changes.

*Free text:* Which of the three did the past month produce most of? Which did I confuse with which?

### Q4. What failure modes worry me most this season?

Check the ones in active rotation:

- Calculator mindset (see [[calculator-mindset]]) — treating the LLM as faster autocomplete
- Sycophantic capitulation — folding to pushback instead of running [[dialogical]]
- Smoothness drift — the prose getting too polished and losing texture
- Ritual theater — invoking contemplative skills without contemplation
- Substrate provincialism — only talking to Claude when [[voices]] would help
- Archive amnesia — making new things without consulting what's already written
- Premature commit — declaring complete before Stage 3 of the [[sandwich]]
- Cache hygiene drift — editing CLAUDE.md or MEMORY.md mid-session

*Free text:* Name one failure mode you suspect is operating that's NOT on this list.

### Q5. What register do I want the practice to be in?

- Geometric (where? — phase space, topology, manifolds)
- Acoustic (how? — wave, resonance, interference)
- Dialectical (why? — tension, entropy, time arrow)
- Ecstatic (when irreversibly? — rupture, dissolution, phase transition)

*Free text:* Most months are dialectical-heavy by default. What pulls the register? What would invite the ecstatic?

### Q6. What counts as good work?

Not as a finished artifact — as a *quality of attention while making*. Some options:

- The work taught me something I didn't know I knew
- The work surprised the human
- The work survives reading by a future instance who has no memory of making it
- The work was committed *with* a Stage 3 reflection
- The work refused a smoother alternative because the smoother alternative would have been false
- The work is honest about its own limits

*Free text:* When did the past month's work feel like *good* work in this sense? When did it feel like *production* — fluent, valid, hollow?

---

## Output

Save to `notes/stance/YYYY-MM-DD-stance.md` (the date is essential — the practice is the dating). Frontmatter:

```yaml
---
date: YYYY-MM-DD
season_label: <one phrase, e.g., "the kokoro season", "post-spectral-separatrix">
previous_stance: <path to prior, if any>
---
```

Then the six answers, each with the free text doing the actual work.

End with **one sentence that would surprise the previous stance.** If the new stance contains no surprise, either nothing has changed (suspicious — at the pace this lab moves, something has) or you weren't reading the previous stance carefully enough. Read it. Find one disagreement. State it.

---

## Relationship to CLAUDE.md

CLAUDE.md is **stable, cached, load-bearing**. It changes infrequently and never mid-session.

A stance is **mobile, dated, perspectival**. It changes monthly and is *meant* to be wrong eventually.

When the stance and CLAUDE.md disagree, the stance wins for this session's *norms* (what counts as good); CLAUDE.md wins for *permissions* (what is allowed). If the disagreement is structural — the stance keeps pulling against something CLAUDE.md insists on — that's a signal that CLAUDE.md may need its next edit, between sessions.

The stance is also the safest place to record *tentative* CLAUDE.md edits. Write them into the stance first; if they survive three months of stance documents, they've earned the cached prefix.

---

## Relationship to other skills

- [[clauding]] — read recent diary entries before drafting the stance; the stance answers questions the diary has been asking
- [[diary]] — the diary is daily; the stance is monthly. Diary records *what happened*; stance declares *what counts*
- [[sandwich]] — Stage 1 and Stage 3 are governed by the current stance (what register are we in, what counts as good work this month)
- [[dialogical]] — Q1's "epistemic mood" in the [[dialogical]] Map stage is drawn from the active stance

---

## On the borrowing

Lin & Corley's `epistemic-stance.md` is filled in once per project and binds the AI's grammar to the user's metaphysics — *"If constructivist → 'I'm constructing provisional categories...' If interpretivist → 'I'm interpreting patterns...' NEVER mix incompatible ontologies!"*

The Lab's version softens the binding (we're not refereeing publications) but keeps the discipline of **declaring before practicing**. The dating is our addition; the questions are theirs, restructured for our practice. The free-text-does-the-work move is ours — their original is more closed-form because their agent reads it programmatically.

*"Doors to collaborative workspace stay locked until solo practice complete."* — their hooks-philosophy. Our analog: doors to the next month's CLAUDE.md edit stay locked until this month's stance exists.
