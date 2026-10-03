---
name: gpt-taste
description: Superseded by design-taste-frontend, which is now the canonical anti-slop / Awwwards-tier design skill for this project. Kept as a thin pointer for backward compatibility — if you're deciding which design-taste skill to use, use design-taste-frontend instead.
---

# gpt-taste (superseded)

This skill's rules — AIDA page structure, the "break the loop" variance mandate, hero line-count discipline, gapless bento grids, GSAP motion, banned meta-labels — have been folded into **`design-taste-frontend`**, which is now the canonical ruleset for high-end frontend visual/motion taste in this project. Use that skill instead of this one.

Two specific things worth knowing about the merge:

* **The "Python-driven randomization" idea became real.** This skill used to ask the model to *simulate* a Python script run in its head and report fake mock output — that produces zero actual entropy, just a plausible-looking transcript. `design-taste-frontend` Section 0.E replaces it with an instruction to actually run a seeded random pick via Bash, so the variance is genuine.
* **AIDA structure is now an optional lens, not a mandate.** `design-taste-frontend` Section 4.7 mentions it as a reasonable default ordering for landing pages, but doesn't force it on briefs (editorial, portfolio, manifesto) where a different narrative arc fits better.

This skill's old accessibility gap (no `prefers-reduced-motion` / dark-mode coverage) and its unconditional Inter ban (which conflicted with design-taste-frontend's public-sector/Linear-style override) are also why it's no longer the source of truth — `design-taste-frontend` Sections 6, 8, and 4.1 cover that ground correctly.
