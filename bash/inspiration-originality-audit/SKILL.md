---
name: inspiration-originality-audit
description: Review a finished design against its inspiration sources for source dominance, copy overlap, weak transformations, asset reuse, and excessive structural or visual similarity.
---

# Inspiration Originality Audit

Run this after implementation and before publishing.

## Inputs

- target Design DNA
- inspiration plan
- reference source IDs
- influence ledger
- rendered desktop and mobile captures
- asset manifests

## Command

```bash
node scripts/inspire.mjs audit \
  --target-dna .aigent/target-design-dna.json \
  --plan .aigent/inspiration-plan.json \
  --refs source-a,source-b,source-c
```

Use `--strict` in CI when a heuristic warning must block publication.

## Review questions

- Does one source control more than two dimensions?
- Is the target section sequence suspiciously close to one source?
- Are font categories, scale, palette, material, motion, and media all coming from the same place?
- Was each planned transformation actually implemented?
- Is source copy, imagery, 3D, iconography, sound, or code present?
- Are the mobile and reduced-motion treatments original and product-appropriate?
- Does the result make sense without knowing the references?

## Verdicts

- `pass` — no high-risk heuristic finding; human review still required.
- `review` — source dominance, copy overlap, or multiple near-identical dimensions need correction.

Similarity scores are review heuristics, not legal conclusions. When rights or infringement risk matters, obtain qualified legal review.
