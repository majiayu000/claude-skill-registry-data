---
name: frontend-writing
description: "When product UI needs words that help someone choose, recover, or complete a flow — make UX copy disappear through clear, consistent, localization-safe language."
---

# Frontend Writing

Copy is interface behavior, not decoration: the best words make the next action
and its consequence feel obvious without calling attention to themselves.

Resist: local cleverness, invented synonyms for established product concepts,
and messages that name a failure without giving a way forward.

- Recon the surrounding voice, terminology, capitalization, and localization
  conventions before changing a string. One concept keeps one name across its
  entry point, action, result, and settings.
- Name actions with direct verbs and make consequential choices explicit. Keep
  a flow's vocabulary stable so labels such as its advance and finish actions do
  not imply different behavior.
- Write errors as calm recovery instructions: say what happened when it is
  useful, what someone can do next, and where the problem is. Coordinate markup
  and announcement behavior with `frontend-accessibility` rather than trying to
  solve it in copy alone.
- Give empty states orientation and one credible next move; label settings for
  their enabled state; use placeholders as format examples, never as labels.
- Keep translatable messages complete. Do not concatenate fragments around
  variables or hide grammar in a label; use the product's interpolation and
  plural/select mechanisms so another language can reorder the whole thought.

When `frontend-design` is installed, use its
[shared review contract](../frontend-design/references/REVIEW.md). Otherwise report
focused writing findings, exact evidence, user impact and verification gaps directly.
Review-only requests stay read-only; do not install siblings or duplicate the full
review schema.
