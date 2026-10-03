---
name: high-end-visual-design
description: Superseded by design-taste-frontend, which is now the canonical anti-slop / high-end-agency design skill for this project. Kept as a thin pointer for backward compatibility — if you're deciding which design-taste skill to use, use design-taste-frontend instead.
---

# high-end-visual-design (superseded)

This skill's rules — banned fonts/icons/shadows, the vibe/layout "variance engine," macro-whitespace, motion choreography, performance guardrails — have been folded into **`design-taste-frontend`**, which is now the canonical ruleset for high-end frontend visual/motion taste in this project. Use that skill instead of this one.

The one genuinely distinct idea from this skill that's worth knowing about: the **Double-Bezel / Nested-Shell card pattern** (a card built as an outer tinted shell + an inner core with its own highlight, for a "machined hardware" look instead of a flat div) and the matching **Button-in-Button Trailing Icon** pattern both got carried over into `design-taste-frontend`'s `references/pattern-vocabulary.md`, referenced from Sections 4.4 and 4.5. Reach for those by name there.

This skill's unconditional font bans (no override for Inter even on public-sector/accessibility-first briefs) and its near-duplicate performance/a11y guardrails are why it's no longer the source of truth — `design-taste-frontend` Sections 4.1 and 6 cover that ground with the override logic this skill was missing.
