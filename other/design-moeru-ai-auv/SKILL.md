---
name: auv-design
description: Use this skill to generate well-branded interfaces and assets for AUV (the Moeru AI command-replay / inspect runtime), either for production or throwaway prototypes/mocks. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping.
user-invocable: true
---

# AUV Design

Read `README.md` in this skill first — it establishes product context, content
fundamentals (the deliberately anti-marketing AUV voice), visual foundations,
and iconography rules.

Then explore the other files:

- `colors_and_type.css` — all design tokens (`--auv-*`).
- `assets/` — logo mark + wordmark.
- `preview/` — small reference cards for each system concept.
- `ui_kits/cli/` — `auv-cli` terminal output recreation.
- `ui_kits/viewer/` — speculative inspect-viewer mock (the browser viewer
  described in `2026-05-19-trace-run-inspect-design.md`; **not built yet** in
  the source repo).

## Operating principles for this brand

1. **Honesty over polish.** AUV documents what is `validated`,
   `candidate`, and `not-validated` in JSON. Reflect that in every artifact.
   Never invent a status not on the canonical list.
2. **Monospace carries identity.** IDs, paths, span names, and JSON keys
   live in `JetBrains Mono`. Body prose lives in `Geist`.
3. **No emoji. No gradients. No glassy overlays.** This is forensic-grade UI.
4. **Status pill is the smallest unit.** Use `.auv-status--{validated,
   candidate, boundary, frozen, running, failed}` everywhere a status is
   shown — sidebars, lists, headers, terminal output, marketing.

## When the user invokes this skill

If creating visual artifacts (slides, mocks, throwaway prototypes), copy
assets out of this skill and produce static HTML the user can view. Reuse the
`<Terminal>` / `<SpanTree>` / `<Sidebar>` components from the UI kits when the
output is product-facing.

If working on production code (Rust CLI, future browser viewer, future docs
site), copy `colors_and_type.css` and `assets/logo-*.svg` into the project,
and follow the rules in `README.md` (sections **Content Fundamentals** and
**Visual Foundations**) to extend the system.

If invoked without other guidance, ask the user what they want to build —
typical asks are:
- a mock of `auv-cli` output for a docs page or social post
- a wireframe / mock of the inspect viewer
- a slide deck explaining a phase-1 boundary
- copy in the AUV voice (status report, freeze note, boundary callout)

Then act as an expert designer on the AUV brand and output HTML artifacts or
production code, depending on the need.
