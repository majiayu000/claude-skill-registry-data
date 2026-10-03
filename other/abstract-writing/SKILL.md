---
name: abstract-writing
description: Write or revise a research-paper abstract using three master recipes distilled from dissecting top ML researchers' abstracts. Use when drafting an abstract, revising one for submission, or when the user asks how to structure or tighten an abstract. Applies the six-questions structure, the three recipes, and a mechanical checklist (short sentences, contribution first, no "can", no bare "This", numbers in pairs).
---

# Abstract Writing (three master recipes)

Follow `abstract-guide.md` in this folder, it is the complete plain-English method.
This file is the operating summary.
## Process

1. **Six answers first.** Before any prose, write six rough bullets: what did you build /
   how does it work (ONE mechanism only) / where tested / numbers (as pairs) / the
   control-ablation / why it matters. One or two sentences each is the whole abstract.
2. **Pick a recipe** from the guide: A (short + confident: one crisp mechanism, no
   numbers, comparative claims against baseline classes), B (numbers as drama: tension
   opener, paired before/after figures, kill the reviewer's doubt in one clause), C
   (anchor then extend: start from a familiar idea, enumerate concretely, end on an idea
   not a metric). Default for results-heavy systems papers: B's structure with A's
   compression. If the advisor favors ideas over metrics, close with C's idea sentence.
3. **Draft, then run the mechanical audit** (never skip):
   - Sentence 1 states the contribution with a strong verb (give, present, introduce).
   - Count words per sentence: none above ~28, average ~20.
   - Zero occurrences of "can", "cannot", "could".
   - Every "This/These" is followed by a noun ("This gate shows...", never "This shows...").
   - Every number has a partner (from X to Y; ours vs. theirs; with vs. without).
   - Each number is attached to the correct claim, never borrow a similar-looking
     statistic from a different measurement.
   - Last sentence is an idea, not a number. 140-190 words. No contractions.
4. **Read it aloud**; fix every stumble. Compare against the closest rival paper's
   abstract and make the differentiation audible in one clause.
## Reference file

- `abstract-guide.md`: the full plain-English guide (recipes, templates, sentence
  surgery, the assembled fill-in-the-blank template, and twelve further rules from the
  classic writing guides and canonical ML abstracts).
