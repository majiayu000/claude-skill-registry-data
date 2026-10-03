---
name: supplement-writing
description: Write or revise a paper's supplement/appendix using a method distilled from dissecting seven appendices by leading ML researchers. Use when drafting or restructuring a supplement, adding an exhibit (prompt gallery, learned-artifact listing, qualitative trace, failure section, protocol tables), or when deciding what belongs in the appendix versus the main paper. Applies the evidence-locker rule, the prose-first exhibits-last order, verbatim-artifact discipline, and mechanical checklists.
---

# Supplement / appendix (master method)

Follow `supplement-guide.md` in this folder, the complete plain-English method.
This file is the operating summary.
## Process

1. **Treat the supplement as an evidence locker.** It is the box of physical
   evidence, prompts, learned code, traces, protocols, costs, where a skeptic
   audits and a reimplementer rebuilds. Across the seven dissected appendices,
   verbatim artifacts average well over half the pages; additional experiments
   average under 5%. Never use the appendix to keep arguing.
2. **Order prose first, exhibits last.** Implementation details, protocol,
   baselines, compute, then the gallery: code listings, the trace, the prompt
   gallery last and longest.
3. **Keep exhibits verbatim.** Stub bodies, debug prints, the model's own
   comments, ragged wrapping, all kept; the credibility comes precisely from
   not tidying. Disclose any curation or abridgment in the caption.
4. **Wire everything.** Every supplement section is pointed at from the main
   text by an inline payload-naming reference ("Appendix D shows example false
   positives"), and re-anchors to the main text in its first sentences. No
   orphaned sections or floats.
5. **Build the honesty devices.** They are structural, not rhetorical: a NAMED
   failure section with verbatim specimens tied to a main-text rate;
   full-population galleries ("no example is dropped") over samples; curation
   disclosures; a scope disclaimer after every proof; a fairness sentence per
   baseline; a compute block with hours, hardware, and cost.
6. **Choreograph any theory beat.** Intuition -> definitions and claim restated
   verbatim from the main text -> named proof outline -> proofs -> scope
   disclaimer -> pointer to the adjacent measurement.
7. **Close with a software map** when the supplement stands alone: concepts to
   source files, figures to generating scripts, runnable commands.
## Core rules

- The supplement audits existing claims; it introduces no new headline claims
  or rankings absent from the main paper.
- One reading legend, stated once before the first exhibit; one functional
  gloss (bold run-in, one sentence) per exhibit.
- Compared prompts print in full, adjacent, with the single delta highlighted,
  the ablation becomes visually auditable.
- One artifact shown COMPLETELY (a full learned program beats five excerpts);
  one qualitative trace with epistemic color-coding and failure annotations.
- Standalone supplements get a roadmap sentence, a Contents, an S-prefixed
  float series, and their own bibliography; attached appendices continue the
  main text's numbering.
- Captions keep full house discipline (the caption-writing skill applies);
  most published appendices let captions collapse, do not imitate that.
- Beware `\ref{sec:...}` under document classes with `secnumdepth=0`: it
  renders empty. Refer to appendix sections by name; figure/table/listing refs
  are fine.
- One notation per object, matching the main paper exactly; unify any split on
  touch and flag the choice.
- Prose axioms: sentences <= ~28 words, subject and verb early, zero
  "can"/"could", no bare This/These, numbers glued to exact objects,
  semicolons rationed.
## Reference file

- `supplement-guide.md`: full guide: term translations, the evidence-locker
  rule, three supplement recipes with fill-in templates, the devices recipe
  (prompt gallery, trace, learned-code exhibit, theory beat, protocol and
  compute block, wiring), mechanical checklists including the "never in a
  supplement" list, and the assembly order.
