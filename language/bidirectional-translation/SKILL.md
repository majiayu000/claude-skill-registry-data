---
name: bidirectional-translation
description: "Trigger: BDT, bidirectional translation, retraduccion, traduccion inversa, /learn drill. Delayed reconstruction and feedback from supplied bilingual text."
license: MIT
metadata:
  author: andresnator
  status: in-progress
  version: "2.1.0"
---

# Bidirectional Translation

## Activation

Run delayed native-to-target reconstruction of a supplied bilingual text. This method accepts an earlier-session text directly; no dialogue directory, named agent, or sibling is required.

## Inputs

Target/native text and languages, the original passive date as a historical record, and optional learner attempt. Optional: explicit output destination and permission to save this drill record. Without a destination, return it inline. Never infer a path.

## Method

Run reconstruction whenever the learner selects the drill; unit dates are historical records, not a gate. If the attempt happens long after exposure, note the elapsed time honestly without turning it into an eligibility rule.

Show only native-language text before the attempt. Let the learner translate from memory, then reveal the original and compare. Natural equivalents count; different wording alone is not a mistake. Ask what changed in meaning before explaining.

Classify material differences as `word choice`, `structure/order`, `missing chunk`, or `grammar pattern`. Give specific feedback and invite another attempt. Mark `completed` only when the learner preserves essential meaning in natural target-language production and demonstrates comprehension; unresolved material differences mean `needs-another-attempt`. Keep feedback conversational, not exam-like.

Return missing phrases as vocabulary candidates and structural gaps as optional proposals. Nothing is registered, exported, or scheduled automatically. Match synthetic categories to supplied gaps without replaying an occurrence as new evidence.

## Output

Return actual learner practice evidence, material differences, proposals, and status using `assets/bdt-session-template.md` when useful. Save only to an explicitly supplied authorized destination; otherwise output inline. Preserve learner-produced evidence only inside this explicitly started drill, never import private correction history.
