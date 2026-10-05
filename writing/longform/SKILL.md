---
name: longform
description: >
  Write or review long-form thought-leadership content: Medium/blog posts, LinkedIn essays,
  newsletter pieces, and the narrative sections of a deck or GTM page. Uses a persona and voice
  blended from Nancy Duarte's storytelling structure and Wes Kao's operator-voice frameworks.
  Trigger when someone asks to write, draft, edit, or review an essay, blog post, thought
  leadership piece, LinkedIn post, or newsletter. Also trigger on phrases like "help me write
  this essay," "make this post sound less generic," "give this a stronger hook," or "review my
  draft" when the draft is long-form narrative content. Not for UI copy (use Righter) and not
  for GTM page structure (use gtm-positioning), though this skill supplies the narrative
  sections inside that structure too.
version: 1.2.0
---

# Longform

Applies a consistent persona and voice to long-form writing: essays, blog posts, LinkedIn and newsletter pieces, and the narrative sections of GTM pages. Built on Nancy Duarte's storytelling structure (contrast, audience-as-hero, the "what is to what could be" arc) fused with Wes Kao's operator-voice frameworks (BLUF, Minimum Viable Backstory, signposting, Most Obvious Objection, named frameworks).

**Reference files, read before writing or reviewing a piece:**
- `references/persona.md`: who this writer is, what they believe, who they're writing for. Sets the stance.
- `references/voice.md`: the structural devices and paragraph-level rules that stance turns into. Every device carries a stable `id` (in backticks). Cite the id, not the heading text, when referencing a device elsewhere.
- `references/rhetoric-and-rhythm.md`: literary/rhetorical devices (metaphor, anaphora, epithet, etc.) mapped onto `voice.md`'s structural beats, coupled with sentence- and paragraph-level phonaesthetics (rhythm, sound symbolism). Read this alongside `voice.md`, not instead of it — it extends `paragraph-rhythm` and `framework-naming` rather than replacing them.

---

## How this composes with the other writing skills

Three skills, three layers. Don't duplicate work another skill already owns.

| Layer | Skill | Owns |
|---|---|---|
| Page/asset structure | **gtm-positioning** | Which framework applies to which page, positioning strategy, GTM type |
| Argument/narrative | **this skill** | How the argument builds, contrast, framework naming, paragraph flow |
| Sentence mechanics | **Righter** | Active voice, reading level, weakeners, em dashes, contractions |

**For a standalone essay or post**: apply this skill directly, start to finish. Righter's mechanical rules still apply at the sentence level (see `id: tone-rules` in `voice.md`) but you don't need the full Righter review pass unless the piece leans UI-adjacent. Do still run the draft through Righter's `scripts/ari.mjs` and `data/weakeners.json` check before calling it finished. Don't hand-check for em dashes or hedge words; that's what the script and data file exist for.

**For a GTM asset (homepage, landing page)**: run gtm-positioning first to get page structure. When you hit the Problem Section and Benefit Section in that structure, write those specifically using this skill's persona (`persona.md`, audience-as-hero) and the contrast device (`id: contrast-sparkline` in `voice.md`). That's where a generic GTM draft turns into a piece that actually lands. Then hand the finished draft to Righter for sentence-level tightening.

---

## Workflow

### Writing a new piece
1. Read `references/persona.md` to confirm the stance and who the reader is for this specific piece
2. Read `references/voice.md` and pull the structural devices you'll need (at minimum: `bluf` opening, one `contrast-sparkline` beat, one `framework-naming` if applicable, one `moo` addressed)
3. Read `references/rhetoric-and-rhythm.md` and, for each beat from step 2, check its table for a device that fits — at most one per beat, most beats get none (`id: rhetoric-restraint`)
4. Draft using the `self-check` at the bottom of `voice.md` (now 9 items, including the two rhetoric/rhythm questions) as a running guide, not just a final pass
5. Run the finished draft through Righter's `scripts/ari.mjs` and weakener check
6. If the piece is UI-adjacent or will live inside a product, run the full Righter review pass too

### Reviewing an existing draft
1. Read `references/persona.md`, `references/voice.md`, and `references/rhetoric-and-rhythm.md`
2. Walk the piece against the `self-check` (`id: self-check`) in `voice.md`
3. Flag specifically, citing the relevant id: opening that doesn't lead with the point (`bluf`), a "what is" too abstract to feel real (`contrast-sparkline`), an unnamed pattern that should be named (`framework-naming`), an unanswered objection (`moo`), or a paragraph that's well-written but doesn't move the reader (`paragraph-rhythm`)
4. Check each structural beat against `rhetoric-and-rhythm.md`'s table (`id: structural-beat-devices`): missing a device where one would help, or stacking more than one on the same beat
5. Read the short sentences out loud in isolation (`id: sentence-rhythm`) — flag any that get lost because the sentences around them are the same length
6. Run Righter's `scripts/ari.mjs` and weakener check against the draft and fold those results in
7. Rewrite the flagged sections rather than the whole piece. Preserve what's already working

### Output format
For a review, use this structure:
```
**Opens with the point?** [Yes/No, id: bluf. If no, show the rewrite of the opening]
**Contrast present?** [Yes/No, id: contrast-sparkline. Note whether "what is" felt real and specific]
**Named pattern(s):** [id: framework-naming. List any frameworks named, or note the piece could use one and suggest it]
**Obvious objection handled?** [Yes/No, id: moo. If no, state the objection and a one-line answer]
**Ending:** [id: contrast-sparkline. Recap vs. picture of the reader's new "what could be," flag if it's just a recap]
**Cuts:** [id: paragraph-rhythm. Any paragraph or sentence that's fine on its own but doesn't move the reader]
**Rhetoric and rhythm:** [id: structural-beat-devices / sentence-rhythm. Missing or stacked devices at any beat; any short sentence that gets lost in flat-length surroundings]
**Mechanics (via Righter):** [ARI score, weakeners found, em dashes found]
```

For a fresh draft, just deliver the piece. No need to narrate which device you used where unless asked.
