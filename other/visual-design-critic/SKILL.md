---
name: visual-design-critic
description: Inspect AIgent Resolve screenshots with native vision, produce a structured evidence-backed aesthetic critique, connect visual findings to numbered rendered elements, and block completion until every required viewport is genuinely reviewed.
---

# Visual Design Critic

Use this skill after mechanical Resolve has produced desktop, tablet, mobile, and reduced-motion screenshots.

## Non-negotiable rule

You must open every required original and annotated image. Do not infer the visual review from HTML, CSS, DOM metrics, filenames, or the mechanical score. When this environment cannot inspect images, stop and request a human review or an explicit vision-model adapter. Never mark an unseen capture as reviewed.

## Prepare

```bash
npx github:wrg32786/aigent-design-system vision prepare --target .
```

Read:

1. `PRODUCT.md`
2. `DESIGN.md`
3. `.aigent/inspiration-plan.json`, when present
4. `.aigent/resolve/latest.json`
5. `.aigent/resolve/latest.visual-review-task.json`
6. every original and annotated capture
7. the generated `element-map.json`

## Review dimensions

Judge every viewport across:

- product clarity
- hierarchy
- composition
- typography
- color and material
- motion and media
- interaction
- product specificity
- originality
- responsive quality
- trust and usability
- finish

Use `not-applicable` only when the dimension genuinely does not exist on the surface. Explain why.

## Findings

Each actionable finding must include:

- viewport
- P0-P3 severity
- critique dimension
- a precise visual observation
- visible evidence
- a concrete repair recommendation
- relevant `E###` element IDs from the annotated capture
- suspected shared owner when reasonably inferable
- what the repair must preserve
- confidence
- open, resolved, or accepted status

Do not write vague reactions such as “make it pop,” “clean it up,” or “feels crowded.” Name the visible relationship that is wrong.

## Root-cause repair

After writing `.aigent/resolve/latest.visual-review.json`:

```bash
npx github:wrg32786/aigent-design-system vision check \
  --target . \
  --review .aigent/resolve/latest.visual-review.json

npx github:wrg32786/aigent-design-system vision finalize \
  --target . \
  --review .aigent/resolve/latest.visual-review.json
```

Read `.aigent/resolve/latest.combined.md`. Fix the highest shared cause rather than patching every visible symptom. Preserve product truth, visual authority, reference transformations, accessibility, mobile intent, and media strategy.

Rerun Resolve and Vision after each coherent repair group. Compare resolved, introduced, and persistent visual findings.

## Stop condition

Do not claim completion until:

- mechanical Resolve passes;
- every required capture is reviewed;
- no open P0 or P1 visual finding remains;
- the overall verdict is `pass` or `pass-with-notes`;
- product clarity, specificity, composition, typography, motion/media, originality, and finish receive an explicit final judgment.

A green mechanical score without this review is not design completion.
