---
name: apple-interface
description: "When explicitly asked for an Apple-style, iOS/macOS-like, or Apple design-language web interface — apply its direct, restrained interaction delta."
---

# Apple Interface

**Make the interface feel held, not performed.** Direct manipulation answers at
once, preserves spatial continuity, and settles without taking control away.

- Use available `frontend-motion` guidance for gesture mechanics; a missing
  sibling is not an installation requirement. Prefer native gestures and preserve
  scrolling/navigation. For this explicitly chosen style, feedback begins on
  contact, controls stay attached to input and reversal starts from the live
  presentation value without jumping.
- Keep navigation and disclosure inside a stable spatial metaphor;
  `frontend-layout` owns its structure and `frontend-motion` owns its paths.
- Use translucent material as functional hierarchy: quiet structural chrome can
  recede while a focused control comes forward. Keep materials restrained; they
  should clarify depth rather than turn every surface into glass.
- Prefer platform typography and let its scale adapt to the person's settings.
  Offer preference-aware alternatives to translucency and contrast treatments;
  optional guidance in [frontend-accessibility](../frontend-accessibility/SKILL.md),
  [frontend-layout](../frontend-layout/SKILL.md),
  [frontend-typography](../frontend-typography/SKILL.md),
  [frontend-color](../frontend-color/SKILL.md), and
  [frontend-motion](../frontend-motion/SKILL.md) supplies discipline detail when
  installed. Otherwise apply native semantics, readable contrast, scalable type
  and a usable reduced-motion path directly; measure costly effects rather than
  assuming materials or transforms are free.
- Read [the focused mechanics](REFERENCE.md) when implementing a gesture,
  material, or type treatment that must carry this style.

When `frontend-design` is installed, use its
[shared review contract](../frontend-design/references/REVIEW.md). Otherwise report
focused Apple-interface findings, exact evidence, user impact and verification
gaps directly. Review-only requests stay read-only; do not install siblings or
duplicate the full review schema.
