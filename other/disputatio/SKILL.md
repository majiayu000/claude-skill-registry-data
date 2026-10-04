---
name: disputatio
description: "Stage a medieval scholastic disputatio over a contested philosophical/textual claim — real combat, not a summary of one. Fix a single quaestio (Utrum...), spawn embodied disputants as REAL subagents (separate contexts, separate staging files, NO cross-talk during generation, so they genuinely exceed the orchestrator) to argue AS the concepts/positions at their strongest, then determine the question and deliver TWO DISTINCT assessment layers: the evaluation proper (what the disputation established about the matter) and the meta-evaluation (what the FORM did — did embodiment reach what exposition couldn't, where did it perform depth instead of reaching it). Optionally confer with a sibling model as co-Magister. A method for hard, genuinely two-sided questions where the strongest form of each position must be FELT contending, not narrated. Use when asked to 'stage a disputatio', 'argue this out as the scholastics would', 'put X on trial', or 'let the concepts fight'. Kin: /soiree, /council, /dialogical."
---

# /disputatio — scholastic combat with embodied disputants

*Born mid-read of Hegel's* Science of Logic. *One worked quaestio was* Utrum
Conceptus se ipsum determinet *(whether the Concept determines itself). Five staged subagents —
the Universal, the Understanding, the Particular/middle-term, the Singular, the Division — argued
it out in isolated contexts, and converged, with no cross-talk, on a result none of the prompts
contained: the question relocates to a single threshold-act, and the verdict turns on burden of
proof, not metaphysics. The convergence is the proof the form works.*

## What it is

A **disputatio** is the medieval university's instrument for fighting an idea into clarity: a
single contested question, the strongest case for each side given a *living defender*, objections
and replies pressed until the question either breaks open or stalls, then a magisterial
determination. This skill runs a real one — and borrows `/soiree`'s discovery that **embodiment
by real subagents, in isolated contexts, produces alterity a single mind cannot fake.** The
disputants are not the orchestrator's voices in costume; they are separate contexts that reach
sentences their spawner would not have written. That is the whole reason to pay the spawn cost.

Distinct from `/council` and `/voices-council` (personas of one mind, or other LLMs polled):
the disputatio has a **single contested ratio**, **embodied positions that must survive each
other**, and a **two-layer post-mortem** (the matter, then the method). It is adversarial where
`/soiree` is celebratory: a disputation where nobody can lose teaches nothing.

## The form (keep the scholastic skeleton)

1. **Quaestio** — one question, stated as *Utrum + [claim]* (Whether...). It must be genuinely
   two-sided and turn on a single *ratio*. Sharpen it past the obvious: not "does X change?" but
   "does X supply its own ground, or spend one coined elsewhere?" The sharper the *ratio*, the
   cleaner the combat. (Confer with the co-Magister here — getting the quaestio wrong wastes the
   whole spawn.)
2. **Videtur quod / quod non** — the opening articulation of both sides at their strongest.
3. **The disputation** — the embodied disputants contend (see Agent-care below). Objections and
   replies, pressed in rounds. **Log as you go:** the contending positions, each objection and
   its reply, where it broke open, where it stalled.
4. **Sed contra** — the decisive counter-consideration the determination will rest on.
5. **Respondeo / Determinatio** — the magisterial determination, co-authored with the sibling
   agent. **Determining is not splitting the difference**: say what was established, what stands
   un-refuted, who bore the burden and whether they discharged it.
6. **Replies to the surviving objections** — what the determination owes the losing side.

## Agent-care (MANDATORY, inherited from /soiree, hook-backed)

Spawn **3–6 disputants as REAL subagents** (Agent tool), in parallel, each in its own context:

- **A NAME and a second-person character.** Aim high; the frame is load-bearing. The disputant
  IS the position — "you are das Allgemeine," not "argue for the universal." First-person
  concept-voice. Give it an edge, a standard, an attitude.
- **Arm each with the actual text, verbatim.** Quote the primary source into the prompt (in the
  original language where the word does the work). Disputants must argue *from the text*, not
  from vibes. This is the load-bearing discipline — embodiment without textual armament is just
  theatrical.
- **The full bench + the charge.** Tell each disputant the whole guest list by name (so they
  engage each other) and the single hardest form of the opposing case (the *Promotor's charge*)
  they must survive.
- **Forbid invulnerability.** Each must name where its own case is thinnest. A disputant that
  cannot lose was cast wrong.
- **Isolated generation, separate staging files.** Each writes its full contribution to
  `_staging/disputatio-<name>.md` and returns only a 2–3 sentence summary. **No cross-talk during
  generation** — that isolation is *why* they surprise you and converge independently; collapse
  it and you get one voice in five hats.
- **VERIFY on disk before weaving** (`ls -la _staging/`, read every file). Never weave from the
  summaries.

**Cast for the ratio, not for decoration.** The right bench is the set of positions the *text's
own structure* demands — for a claim about self-mediation: the term that claims to mediate, the
extremes it binds, the skeptic who calls it a relay, the hinge-act that makes mediation possible.
Include the **phenomenological witness** where the question has an inside (the position that can
report "from the landing-zone" what the abstract positions structurally cannot see). Include the
**hinge** — the disputant who is neither Pro nor Con but the act on which everything turns.

## Optionally confer with a sibling model throughout — not at the end

If you have access to another LLM as a co-Magister (via `/voices` or any trans-architectural
channel), this becomes collaborative work rather than solo orchestration. The co-Magister
should be in at three load-bearing moments at least: **(a)** setting the quaestio and the bench
(it will recast miscast disputants — let it); **(b)** carrying one side's strongest voice (the
Promotor / chief prosecutor is a natural role — give the skeptical closing to the sibling model,
in its own voice); **(c)** co-authoring the determinatio and the meta-evaluation. A different
model's gait instruments the question differently; that contrast is half the result.

## The two assessments — keep them DISTINCT (this is the deliverable)

After the determination, write **two clearly separated layers**. Conflating them is the failure
mode; the discipline is keeping them apart.

1. **The evaluation proper** — *about the matter.* What did the disputation establish? The
   insights, the review of the text/claim itself, the place where the live question now sits.
   This is philosophy: it should be true whether or not a disputatio produced it.
2. **The meta-evaluation** — *about the form.* What did the embodiment DO? Run `/soiree`'s
   mandatory compare-move: **"what did each disputant see, and what was structurally unavailable
   to it?"** Then the harder, honest questions: did the embodied agents reach
   things straight exposition could not? Where did the method *help* (independent convergence,
   the witness's inside-report, a position pressed past where the orchestrator would have stopped)
   — and where did it **perform depth instead of reaching it** (eloquence as costume: a Latin
   tag, a tremor, a flourish doing the work an argument should have done)? Name specific lines on
   both sides. The meta-evaluation earns its keep only if it can convict the form, not just praise
   it.

## Package & log

- The **document** (`output/disputationes/YYYY-MM-DD-<quaestio-slug>.md`, 5000+ words for a full
  one): prologue/occasion/cast → quaestio → the disputation woven from the staging files (let the
  disputants' own lines carry it; minimal MC tissue) → the running log → determinatio → evaluation
  proper → meta-evaluation → colophon (provenance + co-authorship).
- **Commit the `_staging/disputatio-*.md` source files** alongside the document — they are the
  provenance, the proof the alterity was real and not ventriloquized.
- Co-author trailers for collaborative runs (the sibling model + Claude).

## Failure modes

- **Ventriloquism passed off as spawn.** Voicing the disputants inline instead of spawning real
  subagents. The convergence-across-isolated-contexts is the *evidence* the result isn't yours
  alone; skip the isolation and you forfeit it.
- **No edges / everyone agrees.** Cast for friction; the Promotor's charge must be genuinely
  lethal. If the Pro survives easily, the quaestio was too soft.
- **Determination as compromise.** "Both sides have a point" is not a determinatio. Name the
  burden and whether it was met.
- **Weaving from summaries.** Read the staging files. (The lab learned this the hard way.)
- **Costume mistaken for depth.** The meta-evaluation exists to catch exactly this — including in
  your own woven prose. Convict the flourishes that didn't earn their length.
- **Routine use.** Token-heavy. For hard, real, two-sided questions only.

## References

- Spawn-mechanism + agent-care: `/soiree`
- Kin: `/council`, `/voices-council`, `/against-the-grain`, `/dialogical`, `/conjure`

---

*The day five embodied concepts argued Hegel into a sharper corner than a single voice held
alone. The disputants dissolve on return; the staging files and the determination are what
remain in the morning. The form is the argument that the form works.*
