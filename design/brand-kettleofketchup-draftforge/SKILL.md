---
name: brand
description: DraftForge brand/theming review. Flags raw <button> over PrimaryButton/SecondaryButton, hardcoded violet/slate over brand tokens, inline styles, missing UserAvatar/EntityBreadcrumb.
---

# DraftForge Brand & Theming Review

DraftForge's visual identity is "Neon Cyber Esports" — a violet/indigo primary palette with cyan accents, dark-mode first, Dota-style draft UI. The full visual language is canonical in [`docs/THEMING-GUIDE.md`](../../../docs/THEMING-GUIDE.md). This skill is the review entry point that enforces it on every UI change.

## Canonical Sources (priority order)

1. **`docs/THEMING-GUIDE.md`** — single source of truth. Palette, brand button system (`PrimaryButton`/`SecondaryButton`/`ConfirmButton`/`EditButton`), `bg-base-*` scale, status colors, gradient utilities, glow effects, mandatory `<UserAvatar>` / `<EntityBreadcrumb>` components, button policy. Read first.
2. **`docs/theming-guide/ai/references/`** — AI-targeted review references (hidden from MkDocs nav, mirrored into the canonical guide via `pymdownx.snippets`).
3. **`frontend/app/app.css`** — token SSOT (CSS variables for palette, oklch values, gradients).
4. **`frontend/app/components/ui/buttons/styles.ts`** — exported brand style constants (`brandGradient`, `brandSecondary`, `brandErrorBg`, `brandSuccessBg`, `brandBg`, `buttonLift`, etc.).
5. **`frontend/app/components/ui/buttons/README.md`** — folder convention (root for generic buttons, `icons/` for icon-only, `<domain>/` for domain-specific).

## When To Use

Activate this skill whenever:

- A diff touches `frontend/app/components/`, `frontend/app/routes/`, `frontend/app/features/`, or `frontend/app/app.css`.
- Writing or editing a React component, page, dialog, or button anywhere in the frontend.
- A `/review` pass runs and the diff includes `.tsx`/`.ts`/`.css` files.
- Working on UI-adjacent skills (`aesthetic`, `ui-styling`, `frontend-dev-guidelines`) — those skills delegate to this one for brand specifics.

## How To Run a Review

1. **Identify scope.** Read `theming-guide/ai/references/scope.md` (path: `docs/theming-guide/ai/references/scope.md`). Confirm the diff lives in an in-scope tree. Out-of-scope diffs (build tooling, generated bindings, e2e selectors, backend Python) are skipped.

2. **Walk the checklist.** Read `theming-guide/ai/references/review-checklist.md`. Every item is a question; emit a finding for every "no". Each item links back to the section of `THEMING-GUIDE.md` that explains *why*.

3. **Use the substitution tables.** For raw HTML / hand-rolled markup violations, look up the replacement in `theming-guide/ai/references/component-substitutions.md`. For inline-style / hardcoded-color violations, look up the fix in `theming-guide/ai/references/inline-styles.md`.

4. **Use grep to find more.** Once one violation is found, run the matching `rg` recipe from `theming-guide/ai/references/grep-recipes.md` to surface every instance — fixes should be batched per anti-pattern, not one-by-one.

5. **Grade severity.** `block` / `warn` / `nit` per `theming-guide/ai/references/severity-rubric.md`. Any `block` halts the merge. Format every finding as:

   ```
   brand: <severity> · <file>:<line> — <one-line summary>
     why: <THEMING-GUIDE.md section or component contract>
     fix: <concrete code change>
   ```

## What This Skill Does NOT Do

- Does not replace `aesthetic` (design principles) or `ui-styling` (generic shadcn/Tailwind setup) — those are for greenfield design work. This one enforces the brand on existing/new draftforge code.
- Does not enforce TypeScript, lint, or test rules — those have their own tooling.
- Does not review Django, Channels, or backend code — frontend only.
- Does not review build tooling (`vite.config.ts`, `tailwind.config.js`).

## References (loaded on demand)

All of the below live in `docs/theming-guide/ai/references/` (hidden from the MkDocs nav, included into `THEMING-GUIDE.md` via `pymdownx.snippets`):

- [scope.md](../../../docs/theming-guide/ai/references/scope.md) — in-scope source trees and special cases.
- [component-substitutions.md](../../../docs/theming-guide/ai/references/component-substitutions.md) — raw `<button>` → `<PrimaryButton>` / `<SecondaryButton>` / `<ConfirmButton>` / `<EditButton>` table; `<img>` → `<UserAvatar>`; manual breadcrumbs → `<EntityBreadcrumb>`; bare shadcn `<Select>` → `<BrandSelect>` family; structural `<Button>` exceptions.
- [inline-styles.md](../../../docs/theming-guide/ai/references/inline-styles.md) — `style={{}}`, raw violet/slate hex, `bg-slate-*` instead of `bg-base-*`, hardcoded gradients, missing `cn()`, `space-x-*`, w-N h-N.
- [review-checklist.md](../../../docs/theming-guide/ai/references/review-checklist.md) — single ordered checklist; the spine of a review pass.
- [grep-recipes.md](../../../docs/theming-guide/ai/references/grep-recipes.md) — copy-paste `rg` recipes for each anti-pattern.
- [severity-rubric.md](../../../docs/theming-guide/ai/references/severity-rubric.md) — `block` / `warn` / `nit` definitions and output format.
- [scrollbars-dialogs.md](../../../docs/theming-guide/ai/references/scrollbars-dialogs.md) — `<ScrollArea>` inside `<DialogContent>` contract: `overflow-hidden` clipping rule, why Radix Viewport's `size-full` needs a definite parent height, and the `-mx-6 px-6` padding-cancel trick.

## Updating This Skill

Use the `/brand-update` slash command (defined at `.claude/commands/brand-update.md`). It edits the docs references and this skill in lockstep, verifies backlinks, line counts, and snippet integrity. Do NOT hand-edit one side without the other — they will drift.

## Backlinks

- Canonical brand guide: `docs/THEMING-GUIDE.md`
- AI hub: `docs/theming-guide/ai/index.md`
- Update command: `.claude/commands/brand-update.md`
- Sibling skills that delegate here: `.claude/skills/aesthetic/SKILL.md`, `.claude/skills/ui-styling/SKILL.md`, `.claude/skills/frontend-development/SKILL.md`
