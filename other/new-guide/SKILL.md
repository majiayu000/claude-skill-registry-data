---
name: new-guide
description: Use this skill to draft a new user-facing guide under docs/guides paths, optionally organized by pack and Diataxis quadrant, following the Diátaxis framework. Triggers on "write a guide for X", "new tutorial", "new how-to", "new reference page", "new explanation". Settles the audience contract before any body is written, then scaffolds from the matching per-quadrant template. Do NOT use for feature contracts (use `new-spec`), cross-cutting proposals (use `new-rfc`), or recording decisions (use `new-adr`).
---

# Skill: new-guide

Create a new user-facing guide under `docs/guides/<quadrant>/<slug>.md`
— or `docs/guides/<pack>/<quadrant>/<slug>.md` in a repo that organizes
its guides by pack — following the [Diátaxis framework](https://diataxis.fr/).
The framework itself is documented in this repo at `docs/guides/README.md`
and the per-quadrant README — read those for the *what*; this skill is the
*procedure* for landing a new piece on the right side of the line.

The load-bearing rule is **link out, don't blend**. When mid-draft you
find yourself wanting to add theory inside a tutorial, or steps inside an
explanation, that's the cue to write the adjacent piece separately and
link. Mixing quadrants is the most common reason user docs frustrate
everyone.

## When to invoke

Before invoking, confirm:

1. The topic is *user-facing* — the reader is someone using the product,
   not a contributor reading the code. Contributor-facing material lives
   in `docs/architecture/` (current state) or `docs/adr/` (decisions).
   If it's spec-shaped, use `new-spec`.
2. The behavior being documented *already ships* — guides are living
   docs that must match current product behavior. If you're proposing a
   change, you want an RFC or a spec, not a guide.
3. You can name a real reader. "Someone might want to know X" isn't a
   reader; "an operator whose API token expires tomorrow and needs to
   rotate it before the next deploy" is.

If any check fails, push back rather than proceeding.

## Procedure

1. **Settle the audience contract — gated checkpoint.** With nothing
   scaffolded yet, stop and surface the contract *in chat*. This is the
   skill's analogue to `new-spec`'s assumptions checkpoint: the body is
   gated until the contract is signed off. A guide that doesn't name its
   reader ends up serving none of them.

   Emit the contract under exactly this shape:

   ```markdown
   AUDIENCE CONTRACT:

   ## Reader profile
   - **Right now they are:** <on rails, attentive | has a specific problem | scanning for an authoritative fact | reflecting, away from active use>
   - **They leave with:** <a confident "I did it" + working artifact | their problem solved | the precise answer | a clearer mental model of why>

   ## Quadrant pick
   - **Quadrant:** <tutorials | how-to | reference | explanation>
   - **Why this one (not the adjacent quadrants):** <one sentence>

   ## Title (working)
   - **Title:** <draft>
   - **What the reader would have typed into search:** <phrase>
   ```

   Diátaxis distinguishes the four pieces by reader *posture*, not by
   reader *skill*. The same person, expert at the product, can land in
   any of the four quadrants on different days — what places them is
   what they're doing right now. Use the posture-to-quadrant mapping:

   | Reader's posture right now | Quadrant |
   | --- | --- |
   | On rails, attentive, wants a guaranteed working result | **Tutorials** |
   | Has a named problem, wants the recipe | **How-to** |
   | In a hurry, scanning for the authoritative answer | **Reference** |
   | Away from the keyboard, wants to understand *why* | **Explanation** |

   Then **wait for human confirmation or revision.** Don't write into
   the body until the contract is signed off — even if the original
   prompt sounded definitive. Two outcomes from confirmation:

   - The contract is accepted → proceed to step 2.
   - The contract splits into two readers or two postures → that's two
     guides, not one. Surface this and ask the user to pick the
     first; the second goes to follow-up.

2. **Pick a kebab-case slug.** Keep it short and noun-y, matching what
   the reader would have searched for: `rotate-credentialed-skill-token`,
   not `how-to-rotate-your-token-step-by-step`. The quadrant subdir
   carries the "how-to" / "tutorial" framing; don't repeat it in the
   filename.

3. **Scaffold from the matching template.** The quadrant token maps to
   one asset filename and one destination directory — use the mapping
   table below verbatim, don't interpolate by hand:

   | Quadrant | Asset to copy | Destination |
   | --- | --- | --- |
   | `tutorials` | `assets/tutorials.md` | `docs/guides/tutorials/<slug>.md` |
   | `how-to` | `assets/how-to.md` | `docs/guides/how-to/<slug>.md` |
   | `reference` | `assets/reference.md` | `docs/guides/reference/<slug>.md` |
   | `explanation` | `assets/explanation.md` | `docs/guides/explanation/<slug>.md` |

   (Paths are skill-relative — the `assets/` folder lives next to this
   `SKILL.md` wherever your IDE installed the skill.) The four
   templates carry the minimal section structure for each quadrant; they
   are starting scaffolds, not strict forms.

   **If the repo organizes guides by pack** — a `docs/guides/<pack>/<quadrant>/`
   layout — prefix the destination with the owning pack, or `_shared/` for a
   cross-cutting guide that isn't specific to one pack: e.g.
   `docs/guides/core/how-to/<slug>.md`. Write where the repo's existing
   guides already live; match the surrounding structure rather than imposing
   one.

4. **Draft, applying the per-quadrant rules.** The source of truth for
   *what goes in* each quadrant is the per-quadrant README under
   `docs/guides/<quadrant>/README.md` (or `docs/guides/_shared/<quadrant>/README.md`
   in a per-pack repo). Read the relevant one before drafting. The condensed write-time rules, with the named anti-patterns
   the canonical framework warns about:

   - **Tutorials.** Concrete, complete, one path, no digression. Each
     step says what to do, shows what to expect, reassures the reader
     they're on track. Refuse the [*anti-pedagogical
     temptations*](https://diataxis.fr/tutorials/) Procida names:
     *abstraction, generalisation*, *explanation*, *choices*,
     *information*. Tutorials must produce the result they promise —
     broken reliability is the worst failure. Open with the guaranteed
     outcome ("At the end you'll have a running X"), not "you will
     learn".
   - **How-to.** Solves one named problem for an already-competent
     reader. Title is the problem. Skip backstory, skip "turn on the
     power switch"–level steps, skip reteaching basics. Cover the
     realistic variations and the common pitfalls — that's what makes a
     how-to worth the click over the reference page.
   - **Reference.** Authoritative, complete, consistently structured,
     **neutral**. Procida: ["Neutral description is the key imperative
     of technical reference"](https://diataxis.fr/reference/) — austere,
     factual, no editorializing, no narrative. If the section is
     auto-generated, mark it at the top so the next person doesn't
     hand-edit it. Reference rots when the code drifts; "code change →
     reference update in the same PR" is the discipline.
   - **Explanation.** Discursive, illuminating, allowed to be opinionated
     and to wander a little. Frame the scope with an *"About <topic>"*
     question to keep it bounded — open-ended explanations sprawl. No
     step-by-step instructions, no parameter lists. Make connections to
     adjacent topics. ADRs vs. architecture docs vs. explanation: ADRs
     are *frozen decisions for the team*, architecture is *how the code
     is organized now for contributors*, explanation is *what the
     concept means for someone using the product*.

   On voice and tone — apply Google's developer-docs rule of thumb:
   "Sound like a knowledgeable friend who understands what the developer
   wants to do." Second person, active voice, present tense. Two
   separate anti-patterns to avoid:

   - **Don't gaslight stuck readers.** Drop *simply*, *just*, *easy*,
     *quickly*, *obviously* — every one of those words makes a reader
     who got stuck feel dumb.
   - **Don't soften imperatives.** Drop *please* in instructions ("please
     click", "please run") — it makes commands sound optional. Just
     write the imperative.
   - **Don't narrate the product's history.** Write as if the product
     always worked this way — the *retcon* discipline. Drop "will be
     added", "previously X, now Y", "deprecated in 2.0", and
     version-stamped history from the guide body. A guide is a living doc
     describing current behavior; the reader wants what is true now, not a
     changelog. Evolution belongs in release notes, the changelog, or an
     ADR — link to it instead of narrating it inline.

   Efficiency is a form of respect — the reader is in a hurry.

   Beyond word choice, the draft should read like a person wrote it, not a
   machine. Cut the tells that make prose feel generated: hedges ("it's
   worth noting"), uniform sentence rhythm, em-dash overuse, throat-clearing
   openers ("In this guide we will explore…"), inflated verbs ("leverage",
   "utilize", "delve"), and sentences that restate the heading. Vary sentence
   length, keep one claim per sentence, and prefer a concrete number or
   example over an adjective. Read the full checklist in
   [`references/clear-prose.md`](references/clear-prose.md) while you draft and
   edit, not before.

5. **Apply the link-out rule as you draft.** When you find yourself
   reaching for content from the adjacent quadrant, stop and write a
   link instead:

   - Tempted to explain *why* mid-tutorial → link to (or create) an
     explanation page.
   - Tempted to list every option mid-how-to → link to the reference.
   - Tempted to walk a beginner through setup mid-explanation → link to
     the tutorial.
   - Tempted to recommend a best practice mid-reference → link to the
     explanation.

   The link can be a placeholder (`<!-- pending link to … -->`) if the
   adjacent piece doesn't exist yet; surface those placeholders in the
   final summary so the next guide gets written.

6. **Self-check before announcing the draft.** Walk this list against
   the chosen quadrant; every "yes" is a finding to fix:

   - Tutorial: does any step lack a "you should see…" check? Did I
     offer the reader a choice anywhere? Did I sneak in *why* instead of
     linking out?
   - How-to: does the title name the reader's problem in their words?
     Did I reteach a basic the reader already knows? Did I cover only
     the linear path and ignore realistic variations?
   - Reference: did I editorialize anywhere ("this is the recommended
     option…")? Is any entry of the same kind shaped differently from
     its siblings? Did I skip an option?
   - Explanation: is there a step-by-step block that belongs in a
     how-to? Did I drift past the *"About <topic>"* scope? Did I avoid
     opinion — explanation is *allowed* a voice?

   Then run a prose pass against
   [`references/clear-prose.md`](references/clear-prose.md). When your
   environment provides subagents, hand the draft plus that checklist to a
   read-only subagent and ask it to flag machine-shaped prose; that keeps the
   style read off your main context. Without subagents, read the draft cold
   yourself against the checklist. The quadrant self-check above is the floor;
   the prose pass is the polish.

7. **Cross-link the siblings — only the ones that exist.** A new guide
   rarely stands alone. From the new file, add a `See also` section.
   For each candidate sibling — the tutorial that introduces the
   concept, the how-to that uses what reference describes (and vice
   versa), the explanation that says *why* — check whether the file
   exists. If it does, link it. If it doesn't, surface the gap in the
   final summary as a follow-up item; don't write a broken link, and
   don't synthesize a plausible-sounding path. From each existing
   sibling, add a reverse link to the new piece. Cross-links are a
   maintenance pact: when one rots, the others surface the drift.

   Don't touch the per-quadrant `README.md` (`docs/guides/<quadrant>/README.md`,
   or `docs/guides/_shared/<quadrant>/README.md` in a per-pack repo) — those
   READMEs are the framework's per-quadrant explainer, not a piece index.
   Adopters who want an index of pieces add one separately; the skill
   doesn't invent one.

## Anti-patterns to refuse

- **Writing the body before the audience contract is confirmed.** The
  body is gated. The contract is the cheapest place to catch a
  mismatched quadrant; once draft prose is on the page, rework costs
  compound.
- **Picking the quadrant by *topic* instead of by *reader posture*.**
  "Authentication" is a topic; *learning* authentication, *configuring*
  it, *looking up its parameters*, and *understanding why it's
  cookie-based* are four different pieces — possibly all four.
- **Blending quadrants because "the reader will appreciate the
  context".** They won't. The framework's whole thesis is that mixing
  modes is what makes docs frustrating; the link-out rule is
  non-negotiable.
- **Drafting a tutorial without running the steps end-to-end.** A
  tutorial that doesn't produce the promised result is worse than no
  tutorial. If the steps can't be run, you're writing a how-to or an
  explanation — re-open the audience contract.
- **Writing reference in narrative voice.** "You'll want to set this
  to…" is explanation leaking into reference. Reference says *what*;
  recommendations live in explanation.
- **Writing explanation without an *About <X>* frame.** Open-ended
  explanation absorbs adjacent material and sprawls. Name the question
  the page answers; if you can't, the page isn't ready.
- **Editing an existing guide via this skill.** `new-guide` is for new
  pieces. Edits are normal PRs against the existing file; the rules in
  step 4 still apply, but the skill's checkpoint and scaffold don't.
