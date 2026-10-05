---
name: fst-design-system
description: Otgruzka factual UI design system from existing code — tokens, fc-* components, dialogs, taskbar. No full redesign.
---

# fst-design-system — Otgruzka UI (as-built)

**Источник правды:** код, не макеты. Не выдумывать новую палитру или шрифты.

## Stack

- Tailwind v4 via `@tailwindcss/vite` — токены в `@theme` в `src/index.css`
- Отдельного `tailwind.config.*` нет

## Typography

| Token | Value |
|-------|-------|
| `--font-sans` | `'IBM Plex Sans', system-ui, sans-serif` |
| `--font-mono` | `'IBM Plex Mono', ui-monospace, monospace` |

Google Fonts в `index.html` / `fst-web/index.html`. Body: `font-family: var(--font-sans)`.

## Colors (`src/index.css` @theme)

| Token | Hex / value |
|-------|-------------|
| `--color-paper` | `#f3efe6` |
| `--color-paper-dark` | `#e8e2d6` |
| `--color-surface` | `#ffffff` |
| `--color-ink` | `#1c1917` |
| `--color-ink-muted` | `#57534e` |
| `--color-accent` | `#ef6521` |
| `--color-accent-hover` | `#d95518` |
| `--color-accent-soft` | `#ffe8dc` |
| `--color-success` | `#059669` |
| `--color-danger` | `#b91c1c` |
| `--color-grid` | `#d6d3d1` |
| `--color-sidebar` | `#faf8f4` |
| `--color-mark-ya/b/o` | табельные метки (green/blue/amber) |

Tailwind utilities: `text-ink`, `border-grid`, `bg-paper-dark`, `text-accent`, …

## Radius & shadow

`--radius-sm` 0.125rem … `--radius-xl` 0.375rem · `--shadow-sm`, `--shadow-md`

## Layout chrome

| Constant | File |
|----------|------|
| Sidebar expanded/collapsed | `--app-sidebar-w` 14rem / 3.5rem — `src/index.css`, `src/lib/ui/chromeLayout.ts` |
| Taskbar height | `3.25rem` — `TASKBAR_H` in `chromeLayout.ts` |

## Window policy (обязательно)

- Hook: `src/hooks/useWindowChrome.ts`
- Shells: `AppDialog.tsx`, `ModalBackdrop.tsx`
- Backdrop: `CHROME_BACKDROP_CLASS` — **не** `inset-0`; `lg:left-[var(--app-sidebar-w)] lg:bottom-[3.25rem]`
- Minimize: `ModalMinimizeContext` + `WorkspaceTaskbar.tsx` (z-index 400)
- `ephemeral`: confirm/alert/print — закрываются, не сворачиваются

## Component kit (эталоны)

| Pattern | Files |
|---------|-------|
| Page | `PageLayout.tsx`, `PageHeader.tsx` — классы `fc-page`, `fc-page-header` |
| Card | `Card.tsx` — `fc-card` |
| Button | `Button.tsx` — `fc-btn`, variants primary/secondary/ghost/danger |
| Tabs | `TabBar.tsx` — `fc-tabbar` |
| Table | `.fc-table-wrap` + `.fc-table` in `index.css` |
| Dialog | `AppDialog.tsx` sizes md/lg/xl/preview, z-index 420 default |
| Timesheet grid | `.pf-sheet`, `.pf-th`, `.day-cell` in `index.css` |

## States

- Loading: существующие skeleton/spinner паттерны в страницах — копировать с соседнего экрана
- Empty: короткий текст + CTA в `fc-card`
- Error: toast + inline validation на формах; sync errors — UI облака (не seed)

## Responsive

- Mobile header скрыт на `lg` где применено в workspace slice
- Dialog: `items-end` mobile → `sm:items-center`
- Safe areas: `env(safe-area-inset-*)` на dialog footer

## Запреты

- Полный редизайн / смена шрифта / Ayla / Material без просьбы
- Новые `inset-0` backdrop поверх sidebar+taskbar
- Жёлтые «legacy» плитки табеля — следовать текущему `MonthBrigadeBoard` / CSS

## Related skills

- `frontend-ui-engineering`
- `fst-coach-sync` rule (guides после UX)
