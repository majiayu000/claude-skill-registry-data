---
name: method-writing
description: Write or revise a paper's Method section using recipes distilled from dissecting top ML researchers' papers. Use when drafting or restructuring a method section, choosing its architecture figure, algorithm box, or notation, deciding how to introduce and defend a system's components, or fixing a method that reads as a flat wall of mechanics. Applies the N-named-parts skeleton, the setup-banks-notation rule, the star-component discipline, the running-example rule, and mechanical checklists.
---

# Method section (master method)

Follow `method-guide.md` in this folder, the complete plain-English method.
This file is the operating summary.
## Process

1. **Skeleton first.** Name the N parts (the count gravitates to three) in one
   roadmap sentence, in the exact order you will install them, no math in the
   opener. Then install exactly those N parts, one at a time, until the system
   visibly assembles. No part may appear that the roadmap did not promise.
2. **Setup subsection banks notation.** A dedicated first subsection defines
   every symbol at first use under bold run-in headers and fences off borrowed
   formalism (what you did not invent but need). Nothing floats; no symbol
   appears before its definition.
3. **One architecture figure, walked in prose.** Build the figure first and
   write the section to it; walk it left to right; give it a caption that
   re-tells the whole pipeline, self-contained, a reader of the caption alone
   should get the method.
4. **Star component fattest.** The one genuinely new piece, the thing rivals
   lack, gets the most space and the most defense; the plumbing every rival
   also has is compressed.
5. **Running example threaded.** Pick one concrete instance and lead every
   subsection with it before the general case, so intuition precedes each
   equation.
6. **Algorithm box with defaults.** If there is a real procedure or loop, box
   it: titled with the system name, line-numbered, SMALL-CAPS subroutines,
   hyperparameters-with-defaults declared inside the box, each line
   cross-referenced to its subsection. Point at it; never transcribe it.
7. **Seal the section.** No benchmark numbers, no results plot, no standalone
   related work, no limitations paragraph, those live in other sections. Cite
   prior work only instrumentally (the tool you reuse), never to survey a field.
8. **Close with a handoff.** One forward-looking capability sentence, what the
   system can now do, not how well it scores, then straight into Experiments,
   pre-naming the ablation axis the reader will meet next.
## Core rules

- The star component (the one thing rivals lack) is the fattest, most-defended
  subsection; shared plumbing is compressed to make room for it.
- Coin every component, bold it once, then use it as a proper noun, never fall
  back to "our iterative procedure."
- Notation is a cost: introduce a tiny symbol set, define each at first use,
  state the object as a numbered display, and reuse it by number; never open a
  sentence with a symbol.
- Credit the nearest rival warmly, then contrast on exactly one axis, never
  bash. Your closest rival is your likeliest reviewer.
- Narrate the loop on one axis, per-module or per-timestep, and do not
  zig-zag; describe no mechanic twice on two axes.
- Defend each design choice in one in-line clause, never in a rationale
  subsection.
- Prose axioms: sentences <= ~28 words, subject and verb early, zero
  "can"/"could", no bare This/These, numbers paired and attached to exact
  objects.
## Reference file

- `method-guide.md`: full guide: term translations, the N-named-parts
  skeleton, three method recipes with fill-in templates, the devices recipe
  (figure and caption, algorithm box, running example, notation hygiene),
  mechanical checklists including the "never in a method section" list, the
  assembly order, and a worked example on a toy system.
