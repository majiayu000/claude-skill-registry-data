---
name: design-resolver
description: Run the AIgent render, rank, repair, and verification loop on a website, deck, or product interface while preserving product truth, visual authority, inspiration constraints, accessibility, and performance.
---

# Design Resolver

Use this skill after the surface works end to end. It owns mechanical Resolve; route the required rendered judgment to `visual-design-critic`.

## Read first

1. `PRODUCT.md`
2. `DESIGN.md`
3. `aigent.resolve.json`
4. `.aigent/inspiration-plan.json`, when present
5. the current rendered surface

## Initialize

```bash
npx github:wrg32786/aigent-design-system resolve --init --target .
```

For a running application, pass its exact local URL:

```bash
npx github:wrg32786/aigent-design-system resolve \
  --target . \
  --url http://127.0.0.1:3000/
```

## Loop

Repeat no more than three coherent repair cycles before asking for human direction:

1. Run Resolve.
2. Read `.aigent/resolve/latest.md` and `.aigent/resolve/latest.json`.
3. Inspect the top-ranked finding in the rendered page and trace the shared code path that owns it.
4. Fix the root cause once. Do not patch sibling symptoms separately.
5. Keep product claims, selected visual world, reference transformations, responsive intent, and media strategy intact.
6. Run the smallest relevant code check.
7. Rerun Resolve and compare resolved, introduced, and persistent findings.
8. When the mechanical gate passes, run Vision prepare and open every generated capture.
9. Complete Vision check and finalize before claiming completion.

## Repair rules

- Do not flatten a distinctive composition merely to raise a mechanical score.
- Do not remove meaningful motion when a reduced-motion alternative is the actual missing state.
- Do not hide overflow until the overflowing element and layout contract are understood.
- Do not add a dependency for a fix the current stack or browser already supports.
- Do not change copy, assets, or visual identity to imitate an inspiration source.
- Resolve shared primitives before one-off instances.
- When the detector is wrong, record the deliberate exception in `aigent.resolve.json` or the final review rather than distorting the product.

## Stop condition

Stop only when:

- the mechanical gate passes;
- no P0 or P1 issue remains;
- desktop, tablet, mobile, zoomed text, and reduced motion are complete;
- product clarity and specificity remain intact;
- composition, typography, motion, media, and originality receive an explicit visual review;
- the structured Vision gate passes with no open P0/P1 finding;
- the result has no unresolved loading, failure, rights, or provenance concern.

A green report without rendered judgment is not design completion.
