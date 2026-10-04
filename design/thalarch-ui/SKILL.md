---
name: thalarch-ui
description: >
  Directs distinctive, product-specific UI/UX work and visual verification. Use for redesigns,
  new interfaces, layout, styling, motion, interaction, responsive behavior, accessibility, or
  when the user asks to make an interface more polished/professional. Avoids generic AI UI and
  requires rendered evidence when appearance is part of acceptance.
---

# Thalarch UI

Start from product intent, not components.

## Visual thesis

Before implementation define:
- audience and primary job;
- visual tone;
- hierarchy;
- material language;
- typography strategy;
- palette strategy;
- one memorable but justified design idea;
- interaction/motion thesis.

Preserve existing product identity and requested functionality.

## Anti-generic constraints

Avoid:
- card mosaics without information purpose;
- gradients/glows as default decoration;
- excessive rounding;
- random iconography;
- duplicated actions;
- generic dashboard composition;
- animation that does not improve continuity or feedback.

Prefer:
- deliberate whitespace;
- clear hierarchy;
- restrained component count;
- strong alignment;
- consistent spacing/type tokens;
- real content states.

## Runtime verification

Source inspection is not visual proof.

When tooling permits:
- render the changed screen;
- inspect compact and large viewport/device;
- capture before/after;
- test changed interactions;
- inspect clipping, insets, truncation, accessibility, loading/error/empty states.

Create a fidelity ledger:
- expected;
- rendered evidence;
- mismatch;
- fix/disposition.

If render tooling is unavailable, mark appearance `UNVERIFIED`.

## Generated imagery inside UI

If the UI needs hero art, illustrations, textures, avatars, backgrounds, or
other generated raster assets, route that bounded asset task through
`thalarch-image` + `thalarch-imagegen`.

Do not use generated screenshots as implementation proof.

After the asset is created:
- verify it independently with `thalarch-visual-qa`;
- integrate it into the real UI;
- then capture the implemented runtime UI again for final review.

For exact icons, logos, charts, diagrams, or typography, prefer deterministic
vector/code-native production over raster generation.
