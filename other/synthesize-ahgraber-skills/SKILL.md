---
name: synthesize
description: |-
  Use when distilling the through-line gist of one or more sources — the spine, argument, tension, or recurring frame running through a set of documents, notes, research, or transcripts, OR across the ideas within a single rich piece — into a few concise paragraphs. Triggers: "synthesize", "what's the through-line/gist", "extract the insight", "pull these together". Not for faithful summary or condensation that covers what a source says, nor for comparisons or catalogs where enumeration is the deliverable.
---

# Synthesize: Distill a Spine-Led Gist from One or More Sources

Distill the through-line of one or more sources — a set of documents, or the ideas within a single rich piece — into a short, spine-led gist: a few tight paragraphs built around a **spine** drawn from the material, where support is insight on its own and the reader is pointed to the source, not served a copy.

Tell the user when this skill is running: `synthesize`.
Skip the notice when the user asked for the skill by name or slash command; spelling and spacing need not match.
A phrase from this skill's own trigger list is not a name — naming the work is not naming the skill.

Two modal failure modes pull against this and **both reassert at draft time, even after a spine is chosen** — defeating them is the whole job, not a one-time setup step:

- **Listicle** — an enumerated march through themes; the model's reflex for "synthesize."
- **Fluff** — padded coverage that reproduces sources instead of distilling them.

A spine is an internal organizing frame — a constraint, a claim, a recurring metaphor, or a tension — that the material carries: one source among several states it and the rest support it, or one thread runs through the ideas of a single piece.
It must come **from the material**, not be imposed over it (stages of grief, a narrative arc).
See `references/finding-the-spine.md`.

## When Not to Use

- **Faithful summary or condensation** — covering what a source says, proportionally, with no through-line.
  That is summary, not synthesis, whether the input is one source or many.
- **Comparisons or catalogs where enumeration _is_ the deliverable** (vendor capability matrix, feature comparison).
  The list is correct; do not force prose.
  This is the escape hatch — name it and step aside.
- **Line-editing or polishing prose** — use `antislop-writing`, electively, after the gist exists.

## Core Discipline

- **Gist, don't cover.**
  The output is at most a few paragraphs — the more concise the better.
  Comprehensiveness is the enemy; leave out everything the spine doesn't need.
  The gist is what survives ruthless trimming.
- **Support is insight, not reproduction.**
  Every sentence of support must carry insight on its own; point the reader to the source rather than reproducing it.
  **But surface the gem:** a quote, table, or figure that is _itself_ distilled insight — high-signal, stands alone, serves the spine — is the support, not coverage creep; reproduce it.
  The test: does reproducing it carry the insight, or merely relay content the reader could skim for?
- The spine carries the argument; **sources serve the spine, not the reverse.**
- Each source earns its place under the spine; those that don't fit are **named as exclusions, not crammed in.**
- **Self-interested sources don't get the last word.**
  When a source is promoting its own result, product, or position (vendor PR, a lab announcing its own work, marketing), **offer** a grounding pass before committing the spine — external context to restore the caveats it downplays.
  Surface the offer; fold outside context in only when flagged and grounded, never silently.
  External context enters _only_ through this gated pass — not a license to pad with background.
  See `references/finding-the-spine.md`.
- Re-grounding old wisdom in new rationale is legitimate synthesis — **don't prune it.**
  Naming the rationale shift _is_ the synthesis; the shift is load-bearing, not the practice's novelty.
- **Strip affect that doesn't serve the argument; keep affect that does.**

## Workflow

0. **Intent gate** — _narrated checkpoint._
   Gist/through-line, faithful summary, or enumeration?
   Faithful summary → not this skill.
   Enumeration is the deliverable → step aside (escape hatch).
   User supplied a spine → short-circuit to 1b.
1. **Spine scan** — _narrated._
   - **1a DISTILL** (no spine given) → 1–3 candidate spines from the material (across sources, or the ideas within one).
   - **1b VALIDATE** (spine given) → test it; verdict may be holds / holds-but-sharpen / amend / doesn't-hold + alternative.
   - **Self-interest check** → source promoting its own result/product/position?
     Flag it; offer a grounding pass before step 3 (see reference).
2. **Material gate** — **GATE.**
   No spine emerged (material doesn't rhyme)?
   Do not force prose.
   Offer: synthesizer-POV spine (flagged as a different move) OR hand back.
3. **Spine selection** — **GATE (always).**
   Confirm the one ("spine = X — good?") · pick among several · re-pick after a validate-reject (user's spine vs the alternative).
4. **Build** — _narrated, reversible._
   A few tight paragraphs on the spine.
   Support is insight, not reproduction; point to sources.
   Name exclusions; re-ground old wisdom; cut fluff.
5. **Audit & repair** — _narrated, reversible._
   Check the draft against the failure catalog; repair in place.

Steps 1b (validation with teeth) and 2 (the no-spine branch) are where this skill earns its keep.
**Read `references/finding-the-spine.md` before running steps 1–3** — the validation verdicts and the no-spine branch live there; running them from memory loses the teeth.

## Steering Contract

**The user always drives** — they can override at any fork, guaranteed by transparency and reversibility, **not** by the agent stopping for sign-off at every step.
The _kind_ tag on each workflow step marks which is which: **GATE** steps stop for the user before acting; the rest narrate and proceed, reversible by the user's next turn.
Surface every consequential choice (the spine, the no-spine fallback, the grounding-pass offer) _before_ acting on it; never commit to a spine silently.

The spine is the single most expensive thing to get wrong — everything downstream hangs off it — so step 3 gates **even when there is one obvious candidate.**

## Audit Catalog (Step 5)

**Read `references/audit-failure-modes.md`** for detection cues and fixes; repair each in place.
The list below is an index, not the procedure — the cues that catch each mode live in the reference.

- **Listicle relapse** — drifted back to enumerated themes/practices.
- **Coverage creep / fluff** — sprawled into comprehensive summary, or padded; support reproduces sources instead of distilling insight.
- **Abandoned framing** — an organizing image in the intro that doesn't carry through.
- **Quote-as-spine** — a source's quote doing the argumentative work the synthesizer should do.
- **Significance inflation** — "striking," "the strongest convergence," superlatives standing in for argument.
- **Source taken at face value** — a self-interested source's spin survived into the gist; caveats it downplays are missing.
- **Forced-fit spine** — material crammed under a spine it doesn't support (watch this after validate mode).
- **Over-pruned wisdom** — an old practice dropped instead of re-grounded in its new rationale.

## Composition With Other Skills

Standalone — no built-in gather or polish steps, and no automatic handoffs.
The user or agent may **electively** run `mcp-research` (gather sources) before, or `antislop-writing` (polish prose) after.

## References

- `references/finding-the-spine.md` — distill vs. validate modes, validation with teeth, the no-spine branch, source-earns-its-place.
- `references/audit-failure-modes.md` — each failure mode with detection cues and repairs.
