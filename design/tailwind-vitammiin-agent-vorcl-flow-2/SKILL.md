---
name: tailwind
description: Tailwind CSS v4 (CSS-first) — установка (Vite `@tailwindcss/vite`, PostCSS, CLI), конфигурация через `@import "tailwindcss"` + `@theme` (дизайн-токены как CSS-переменные, OKLCH), utility-first, варианты через cva/cn, адаптивность и container queries, тёмная тема, доступность. Use при стилизации UI и настройке дизайн-системы на Tailwind.
---

# Навык: Tailwind CSS (v4)

Utility-first стилизация. **v4** — CSS-first: конфигурация в CSS, а не в `tailwind.config.js`; контент сканируется автоматически (`content`-массив не нужен).

## Установка и интеграция
- **Vite** (рекомендуемо): `npm install tailwindcss @tailwindcss/vite`.
  ```ts
  // vite.config.ts
  import tailwindcss from '@tailwindcss/vite'
  export default defineConfig({ plugins: [tailwindcss()] })
  ```
  ```css
  /* главный CSS */
  @import "tailwindcss";
  ```
- **Next.js / PostCSS**: `@tailwindcss/postcss` в `postcss.config.mjs` + `@import "tailwindcss";` в глобальном CSS.
- **CLI**: `@tailwindcss/cli`.
- В v4 `@tailwind base/components/utilities` заменены одним `@import "tailwindcss";`.

## Конфигурация (CSS-first, `@theme`)
- Токены в `@theme` становятся И утилитами, И CSS-переменными:
  ```css
  @import "tailwindcss";
  @theme {
    --color-brand-500: oklch(0.84 0.18 117);   /* → bg-brand-500 */
    --font-display: "Satoshi", sans-serif;      /* → font-display */
    --breakpoint-3xl: 1920px;                   /* → вариант 3xl: */
  }
  ```
  В рантайме — `var(--color-brand-500)`. Семантические токены, не «магия»; цвета в OKLCH.
- Кастомные утилиты — `@utility`; варианты — `@custom-variant` (тёмная тема: `@custom-variant dark (&:where(.dark, .dark *));`).
- Легаси JS-конфиг не автодетектится — подключай `@config "../tailwind.config.js";`.
- Миграция v3→v4: `npx @tailwindcss/upgrade`.

## Основы (utility-first)
- Стилизуй утилитами; кастомный CSS — где нет утилиты. Повторяющееся — в **компоненты**, не в `@apply`.

## Варианты и композиция
- Варианты — через **cva** (`class-variance-authority`); объединение/дедуп — `clsx` + `tailwind-merge` в `cn(...)`.

## Адаптивность и темы
- Mobile-first + брейкпоинты `sm: md: lg:` (свои — `--breakpoint-*`).
- Container queries (v4): `@container` + `@sm:`/`@md:` по размеру контейнера.
- Тёмная тема — `dark:`; стратегия — `@custom-variant dark`.
- Состояния — `hover: focus-visible: disabled: aria-*: data-*:`.

## Доступность
- `focus-visible` вместо снятия обводки; контраст (WCAG); не только цвет; `sr-only`.

## RTL и логические свойства
- Для мультиязычных/RTL-локалей — **логические** утилиты вместо физических: `ms-*`/`me-*`, `ps-*`/`pe-*`, `start-*`/`end-*`, `text-start`/`text-end`; выставляй `dir`, зеркаль иконки направления. Детали — `$i18n`.

## Совет
- Порядок утилит — `prettier-plugin-tailwindcss`.
