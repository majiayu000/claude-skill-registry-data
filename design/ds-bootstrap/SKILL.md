---
name: ds-bootstrap
description: Bootstrap a project's design system from the shared base once a DA (art direction) is chosen — Phase 1. Use when the user says "create the design system for this project", "make me a perfect DS", "set up the DS from @efounders", "wire the design system here", or right after DA exploration. Seeds the shared skeleton, applies the project's brand, drops the conventions (CLAUDE.md, ds-check gate, component specs), generates first screens, and sets up the Figma bridge — with the code as the single source of truth. Unlike a generic from-scratch bootstrapper, this one starts from the shared base.
---

# ds-bootstrap — turn a chosen DA into a wired, on-brand design system

This is **Phase 1**: a direction (DA) has been found (Phase 0 — explored in Figma + Claude).
Now crystallise it into a real design system for *this* project, seeded from the shared
base, so it's consistent with the studio and AI-native from day one.

**Source of truth from here on = the code.** Figma led during exploration; once this skill
runs, the code leads and Figma reflects it.

Shared base: `@efounders` registry — `https://design-system-template-registry.vercel.app` (repo
`eFounders/design-system-template`). Reuse its templates, don't reinvent.

## Inputs (gather first — interview briefly if missing)

- **The DA**: brand color(s), font, corner roundness, density (compact/airy), mood, + any
  validated sample screens from Phase 0.
- **Product context**: what it is, primary persona, tone of voice.
- **Target**: confirm the project is shadcn + Tailwind v4 (run `npx shadcn@latest init` if not).

The DS is only as good as the DA you feed it — if the DA is vague, ask 3-4 sharp questions
before generating.

## Procedure

1. **Wire the base.** Add the `@efounders` namespace to `components.json`
   (`https://design-system-template-registry.vercel.app/r/{name}.json`), then `shadcn add @efounders/theme`
   and the components the project needs (`shadcn add button input table sidebar form …`) —
   all branded automatically by the theme.
2. **Apply the DA = set the brand**, the *only* knobs to touch in the tokens file:
   `--brand-*` (the ramp), `--font-base` (+ display font), `--radius`, `--text-base`
   (density), `--tag-*`. Everything else follows. Keep the semantic contract intact.
3. **Drop the conventions.** Copy `templates/CLAUDE.project.md` from the @efounders repo (rename it `CLAUDE.md` at the project root), fill it
   (product, persona, tone, paths to tokens/components/storybook). Add the
   `ds-check` gate (`scripts/ds-check.mjs` + `.github/workflows/ds-check.yml`). Write a short
   `docs/COMPONENTS.md` for any bespoke this project adds, and seed `docs/REFERENCES.md`
   (north-star patterns) only if the team already has validated references — leave it out otherwise.
3b. **Storybook.** Stand up a live storybook route that renders the real components (like the
   @efounders one) — never a static mock.
4. **Generate the first screens** with the DS, reusing the components (not from scratch).
   Offer a few pistes if useful; let the team pick.
5. **Figma bridge (good practices).** Generate the Figma library *from the code* (use the
   `figma-generate-library` skill / Figma MCP): **Figma variable names = token names exactly**,
   set up **Code Connect** so Dev Mode shows the real component, write each component's
   description as an API doc + a Figma→code mapping table, and prefix WIP/reference frames
   with `_wip/`/`_dev/` so the MCP skips them. Code stays the source of truth.
6. **Verify.** Run `/ds-audit` on the repo → confirm it scores AI-native, fix the gaps.

## Rules

- **Never impose the @efounders default brand** — this project gets its own (the DA). Only
  the skeleton/conventions are shared.
- **Reuse, don't reinvent**: pull components and templates from `@efounders`; only author
  what's genuinely missing (and log it).
- **Code = source of truth.** Figma is generated from it and reflects it, not the reverse.
