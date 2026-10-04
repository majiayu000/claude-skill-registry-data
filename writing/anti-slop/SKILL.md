---
name: anti-slop
description: >
  Remove AI slop from any voice-bearing prose — original posts, threads, articles,
  long-form, emails, docs, READMEs, marketing copy, bios, scripts. Use when drafting
  text meant to sound like a specific person or brand, when rewriting text that reads
  generic, corporate, or AI-generated, or when asked to humanize, de-slop, audit, or
  "make this sound like me / like us." Works in any agent (Claude Code, Codex, Cursor,
  custom) — no tools required. NOT built for X/Twitter reply batches: those need
  target selection on top of this skill's gate, which is out of scope here.
---

# anti-slop

Slop is not a vocabulary problem. It is manufactured upstream: alignment training collapses output toward the statistical mean (mode collapse, driven by typicality bias in preference data — arXiv 2510.01171), single-sample generation returns the most typical completion, and a context starved of specifics can only produce the average of everything. Banned-word lists treat the symptom. At adoption scale they mint a new house style — the zero-em-dash, no-adverbs voice is already its own tell, and Wikipedia's own tells-catalog maintainers warn that scrubbing signs "could just make detection harder."

**The job: make the output sound like a specific person with something specific to say.** Both halves are mandatory. This skill intervenes at four layers and measures whether it worked. It is a writing-quality protocol, not a detector-evasion tool.

---

## Modes

| Mode | When | Run |
|---|---|---|
| **DRAFT** | writing new text | Layers 1→2→3→4, ship with score |
| **AUDIT** | handed existing text | Layers 3→4, report score before/after + fix list |

---

## The contract — verify before generating anything

Two inputs separate writing from slop. Check both first:

**1. A bound voice.** In priority order:
- an explicit voice spec (voice file, brand guide), or
- 5+ writing samples from the author → build a voice card on the fly (`references/voice-binding.md`), or
- a named register the user states ("tired senior engineer in Slack", "group-chat shitposter who knows finance").

**If none exists: STOP and say so.** Offer the choice: "Give me 5+ samples or name a register — otherwise I can deliver clean-generic, which reads fine but sounds like no one." NEVER silently fall back to a default voice. A default voice shipped by every agent is the next generation of slop.

**2. Specifics.** At least 3 concrete particulars the text can stand on: a number, a name, a date, a moment, a place, a mechanism, a contradiction, a thing that broke. No specifics in context → get them (ask the user, or pull from the material available to you). **Never invent particulars to fill the gap.** If neither is possible, say: "No specifics available — anything I write will be generic by construction." That sentence is more useful than the slop would have been.

Also pin **the one job**: who reads this, and what should they know/feel/do after. Can't answer → ask.

---

## Layer 1 — FEED (starve the mean, feed the particular)

Slop is regression to the mean: the most statistically likely phrasing that fits the widest variety of cases. Wikipedia's catalog documents the mechanism — the specific "inventor of the first train-coupling device" becomes "a revolutionary titan of industry": less specific and more exaggerated at once.

Before drafting:
- Lay out the specifics you collected (contract item 2) — these are load-bearing, the draft hangs on them.
- Load 2–3 lines of the bound voice's actual writing into working context. You will draft *as* this voice, not edit toward it later.
- Note what the piece must NOT do (banned topics, claims the author can't support, register limits).

If the user asks for volume ("write 10 posts"), specifics divide across pieces. Fewer specifics than pieces → deliver fewer pieces and say so. Never stretch.

## Layer 2 — GENERATE (escape the mode)

The first completion is the mode — the most typical answer in the distribution. For voice-bearing text, never ship it unexamined.

- **Generate 3–5 candidates before judging.** Vary the *move*, not the synonyms: different opening (moment / claim / number / question / dry joke), different altitude (street-level detail vs. principle), different length. Same move five times = one candidate.
- **Verbalized sampling** (the only verified prompt-level fix for mode collapse, 1.6–2.1× diversity): generate the candidate set *with an estimated probability that a generic assistant would produce each one*. Discard the most-probable one or two — they are the centroid. Develop the best survivor. Recipes in `references/generation.md`.
- **Write as the voice from the first token.** Persona-at-generation beats persona-as-postedit (a persona prompt moved GPT-4.5 from 36% to 73% judged-human). The voice card is in context; use its constructions while drafting, not after.
- Draft to natural length, then cut ~20%. Never write toward a word count.

## Layer 3 — GATE (audit in clusters, score honestly)

Run the four-question audit on every unit (sentence for short pieces, paragraph for long):

1. **INTERCHANGEABLE** — could this exact unit sit in 20 unrelated pieces unchanged? → rewrite around a specific.
2. **ADDITIVE** — does it add information or stance, or restate/pad what's already there? → cut.
3. **SHAPED** — is the structure imposed by template (intro/3-points/outro, setup+payoff, listicle reflex) rather than by the content? → reshape.
4. **VOICED** — could the bound author have typed this sentence? → refit (Layer 4).

Then sweep for tells (`references/tells.md`) with two non-negotiable rules:

- **Clusters, not singles.** One em-dash means nothing. One "delve" means little. Three catalog tells within ~100 words means rewrite that span. Flagging single tells produces the over-sanded text that stylometry catches at .98 accuracy for being *too tidy*.
- **The voice sets the caps.** If the author uses em-dashes, em-dashes are fine — at the author's observed rate. Frequency budgets come from the voice card. Global defaults (`references/tells.md` §caps) apply only when no voice is bound.

**Score it** (before fixing, and after — report both):

| Count per ~500 words (whole piece if shorter) | Points each |
|---|---|
| tell clusters (3+ catalog tells within ~100 words) | 2 |
| INTERCHANGEABLE units | 2 |
| VOICED failures | 2 |
| SHAPED structures | 1 |
| ADDITIVE failures (padding/restating) | 1 |

Counting: one unit scores only its worst failure; a scored cluster absorbs the 4Q failures of the sentences inside it; if more than half the units fail VOICED, score VOICED once for the piece and route to a full rewrite instead of span fixes. Sum, cap at 10. **Ship at ≤2. Max two fix passes** — past that you're sanding, and sanded text is its own tell. Quoted/cited material is immune, and so are the author's signature shapes (see tells.md §protected shapes). In AUDIT mode, establish whose text it is and bind THAT voice before flagging anything — default caps on known-human text manufacture false positives.

## Layer 4 — FIT (replace toward the voice, never toward neutral)

Deletion-to-neutral is half a fix; done by everyone, it converges on the same beige. Every flagged span gets rewritten *as the bound voice would say it*:

- Find the parallel move in the voice samples — how does this author open, hedge, joke, land? Reuse their actual constructions.
- **Check your fix against the voice card before accepting it.** Your own rewrite reflexes are the model defaults this skill exists to fight — fixes arrive carrying em-dashes, triplets, and tidied grammar the author never uses.
- **Keep the author's irregularities.** Fragments, lowercase, pet words, odd punctuation, mid-sentence register drops — whatever the samples show. Clones get caught for grammatical over-standardization; the polish is the giveaway. Irregularity must come *from the samples* — never sprinkle random "humanness."
- No sample support for a fix? Flag it: "no voice precedent for this span — wrote it neutral, check it." Honest gaps beat confident drift.
- Final pass: read it aloud in the author's register. Sounds like a press release, a LinkedIn post, or a brand statement (and the author isn't a brand)? Failed — back to the worst span.
- The author test: would the author cringe? Would someone who reads them daily clock it as off? If unsure and you can ask, ask.

---

## Refusals (what this skill will not do)

- Generate from zero specifics, or invent them. It says so instead.
- Apply a silent default voice. It asks or declares clean-generic.
- Hit a requested count with filler. Fewer real pieces, stated plainly.
- Sand past two passes. Over-cleaning is the new tell.
- Optimize for beating AI detectors. The goal is text worth reading in a real voice; if the content is empty, the fix is upstream in FEED, not in phrasing. Signs are symptoms — treating only the signs makes text harder to detect, not better.

---

## References (load on demand)

- `references/tells.md` — the tell catalog: vocabulary, structure, formatting, stance; cluster rules; default caps. Sourced from Wikipedia WP:AISIGNS (the only catalog with per-item academic citations) + slop-forensics corpus lists + CT-specific additions.
- `references/master-list.md` — the full consolidated catalog (2026-07-29 sweep of a backtested voice-clone redteam, a voice-cloning research corpus, a 23,854-tweet single-author voice study, and a reply-batch gate): tells superset + voice-binding rules + refusal gates + audit-instrument honesty rules + edit-scope carve-outs. Load this for any full audit; tells.md is the fast subset.
- `references/audit-rubrics.md` — per-format gates: original post/thread, long-form, docs/README, email/DM. Plus the full score sheet.
- `references/generation.md` — verbalized-sampling recipes, candidate-variation axes, persona binding.
- `references/voice-binding.md` — building a voice card from samples in 10 minutes; the replacement protocol; which irregularities to preserve.

## Quick reference

```
JOB = a specific person saying something specific. Both mandatory.
CONTRACT: bound voice + 3 specifics + one job. Missing -> ask or declare, never fake.
FEED: specifics are load-bearing. GENERATE: 3-5 candidates, distrust the most
probable, write AS the voice. GATE: 4Q audit (interchangeable/additive/shaped/
voiced) + tell CLUSTERS (1 tell = noise, 3 in 100w = rewrite). Voice sets the
caps, not a global banlist. Score before/after, ship <=2, max 2 passes.
FIT: replace flagged spans with the author's own moves. Keep their mess --
too-tidy is how clones get caught.
NEVER: default voice, invented specifics, filler to hit count, 3rd sanding pass.
Reply batches -> out of scope (they need target selection on top of this gate).
```
