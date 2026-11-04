---
name: design-system
description: >-
  Tokens in @mobywatel/brand and accessible React components in @mobywatel/ui: colours, type scale (incl.
  senior scale), spacing, radii, motion, themes (light, dark, senior), and the component set (Button, Card,
  Sheet, ConfirmCard, DocumentCard, ReminderTile, ChatBubble…). Use when adding or changing a component or
  token, styling a screen, or asking "is there a component for this?".
---

# Design system

Owners: tokens and identity are the `brand-designer` agent's; components are the `ui-engineer` agent's. For
visual taste the `frontend-design` and `ui-ux-pro-max` skills help, but this skill's rules win.

## Where things live

| What                           | Where                                                  | Used by                     |
| ------------------------------ | ------------------------------------------------------ | --------------------------- |
| Colours, type, spacing, motion | `packages/brand/src/tokens.ts`                         | ui, app (as CSS variables)  |
| CSS variables                  | `packages/brand/src/css.ts` → `cssVariables(theme)`    | injected once in `src/app/` |
| Copy constants, disclaimer     | `packages/brand/src/copy.ts`                           | app, ui                     |
| Components                     | `packages/ui/src/<name>/<name>.tsx` (+ test)           | `apps/pwa/src/features/*`   |
| Icons                          | `packages/ui/src/icons/` (own SVG set, `currentColor`) | ui, app                     |

## Tokens

- **Colour:** semantic names only (`--bg`, `--surface`, `--text`, `--text-muted`, `--accent`, `--accent-text`,
  `--danger`, `--warning`, `--success`, `--focus`, `--watermark`). The raw palette stays inside `tokens.ts`.
  Every text/background pair is checked for ≥ 4.5:1 (≥ 3:1 for large text and UI borders) in a unit test in
  `packages/brand`.
- **Type scale:** `--font-xs … --font-3xl`, with a **senior scale** that raises the base to ≥ 20 px and every
  step proportionally. Line height ≥ 1.5 for body. One UI typeface with good Polish diacritics (ą ę ł ń ó ś ź
  ż) and tabular numbers; self-hosted, with no font CDN.
- **Spacing:** 4-px grid (`--space-1 … --space-9`; `--space-9` is 120 px, for page sections). **Targets:**
  `--target-min` 48 px (56 px in senior).
- **Radii, elevation, motion:** `--radius-*`, `--shadow-*`, `--duration-*` and `--easing-*`. All motion is
  zero under `prefers-reduced-motion`.

## Themes

`light` (default), `dark` (follows `prefers-color-scheme` unless overridden), and `senior` (a modifier on
either: bigger scale, bigger targets, stronger contrast, fewer decorative elements). Themes are attribute
switches on `<html>` (`data-theme`, `data-senior`). Components never branch on theme in JS.

## Visual language: our own, neutral

- No white-red-eagle cues, no flag ribbons, no guilloche or hologram patterns, and no document layout that
  resembles an ID card (the `prototype-guardrails` skill).
- Calm, high-contrast, generous whitespace. One accent colour. Icons are line icons with text labels.

## Components (packages/ui)

| Component      | Notes                                                                                               |
| -------------- | --------------------------------------------------------------------------------------------------- |
| `Button`       | `<button>`, variants primary/secondary/ghost/danger, `loading`, full-width option                   |
| `Card`         | `<section>` or `<article>` with a heading slot                                                      |
| `ListItem`     | link or button row with icon, title, subtitle, chevron; the whole row is one target                 |
| `Sheet`        | bottom sheet = modal dialog (`<dialog>` or focus-trapped), Esc closes, focus returns                |
| `Tabs`         | WAI-ARIA tabs pattern; bottom navigation is links, not tabs                                         |
| `Field`        | label, hint, error wired by `aria-describedby`, and the "nie wpisuj prawdziwych danych" hint slot   |
| `Toast`        | `role="status"` region, no auto-dismiss for errors                                                  |
| `ConfirmCard`  | what will happen, data rows, source, primary "Potwierdź" + "Zmień"; nothing happens without the tap |
| `DocumentCard` | information card, `PROTOTYP – nie jest dokumentem` watermark + disclaimer, illustrated avatar       |
| `ReminderTile` | due date, urgency colour **plus** text (never colour alone), opens the matter                       |
| `ChatBubble`   | assistant/user, supports rich content (cards, chips); lives inside an `aria-live` log               |
| `Chip`         | suggestion button, wraps at 200% zoom                                                               |

## Rules

1. **Tokens, never literals.** No hex in `apps/` or `packages/ui`: the post-edit hook blocks new ones. Missing
   colour? Add a semantic token in `packages/brand`.
2. **Presentational.** Components receive formatted strings (dates, money already in pl-PL). No domain
   imports, no fetching, no i18n lookups inside `packages/ui`.
3. **Accessible by construction.** Native elements first; every interactive element has an accessible name;
   visible focus ring from `--focus`; targets from `--target-min`. Details: the `accessibility` skill.
4. **Styling.** Tailwind CSS 4 utility classes on our tokens (`packages/brand/src/tailwind.css`):
   `bg-surface`, `text-lg`, `min-h-target`, `dark:`, `senior:`. No literal colours, no `@apply`, no runtime
   CSS-in-JS. Rules: `docs/decisions/tailwind-2026-10-28.md`.
5. **Tests.** Testing Library: render, query by role and name, check keyboard behaviour. Add an axe check
   (`vitest-axe` or equivalent) per component.

## Adding a component

1. `packages/ui/src/<name>/<name>.tsx` (Tailwind classes) and `<name>.test.tsx`. Export it from
   `packages/ui/src/index.ts`.
2. Cover default, senior and dark rendering in tests or a demo route (`/__ui` in dev only).
3. Use it in a feature. Run the `verify-change` skill's UI checks (screenshots at 390×844 and 360×800, senior
   mode on).
