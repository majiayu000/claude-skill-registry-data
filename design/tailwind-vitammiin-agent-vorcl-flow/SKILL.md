---
name: tailwind
description: Tailwind CSS v4 (CSS-first) — установка (Vite `@tailwindcss/vite`, PostCSS, CLI), конфигурация через `@import "tailwindcss"` + `@theme` (дизайн-токены как CSS-переменные, OKLCH), utility-first, варианты через cva/cn, адаптивность и container queries, тёмная тема, доступность. Use при стилизации UI и настройке дизайн-системы на Tailwind.
version: 1.0.0
---

# Навык: Tailwind CSS (v4)

Utility-first стилизация. **v4** — CSS-first: конфигурация живёт в CSS, а не в `tailwind.config.js`; контент сканируется автоматически (массив `content` не нужен).

## Установка и интеграция
- **Vite** (рекомендуемо, самый быстрый путь):
  ```bash
  npm install tailwindcss @tailwindcss/vite
  ```
  ```ts
  // vite.config.ts
  import { defineConfig } from 'vite'
  import tailwindcss from '@tailwindcss/vite'
  export default defineConfig({ plugins: [tailwindcss()] })
  ```
  ```css
  /* главный CSS-файл (напр. src/index.css) */
  @import "tailwindcss";
  ```
- **Next.js / PostCSS**: пакет `@tailwindcss/postcss` в `postcss.config.mjs` (`plugins: { '@tailwindcss/postcss': {} }`) + `@import "tailwindcss";` в глобальном CSS.
- **CLI**: `@tailwindcss/cli` (`npx @tailwindcss/cli -i in.css -o out.css --watch`).
- В v4 `@tailwind base/components/utilities` заменены **одним** `@import "tailwindcss";`.

## Конфигурация (CSS-first, `@theme`)
- Дизайн-токены объявляй в `@theme` — они становятся И утилитами, И CSS-переменными:
  ```css
  @import "tailwindcss";

  @theme {
    --color-brand-500: oklch(0.84 0.18 117);   /* → bg-brand-500, text-brand-500 */
    --font-display: "Satoshi", sans-serif;      /* → font-display */
    --breakpoint-3xl: 1920px;                   /* → вариант 3xl: */
    --ease-snappy: cubic-bezier(0.2, 0, 0, 1);  /* → ease-snappy */
  }
  ```
  В рантайме токены доступны как `var(--color-brand-500)`. Используй **семантические** токены, не «магические» значения; цвета — в OKLCH (шире gamut, предсказуемое осветление).
- Кастомные утилиты — `@utility`; кастомные варианты — `@custom-variant` (напр. тёмная тема через класс: `@custom-variant dark (&:where(.dark, .dark *));`).
- Легаси JS-конфиг в v4 **не автодетектится** — подключай явно: `@config "../tailwind.config.js";`.
- Миграция v3→v4: `npx @tailwindcss/upgrade`.

## Основы (utility-first)
- Стилизуй утилитами прямо в разметке; кастомный CSS — только там, где нет подходящей утилиты.
- Повторяющиеся паттерны извлекай в **компоненты**, а не в `@apply`-классы.

## Варианты и композиция
- Варианты компонента — через **cva** (`class-variance-authority`); объединение и дедуп классов — `clsx` + `tailwind-merge`, обёрнутые в `cn(...)`.
- Условные классы — через `cn(...)`, без ручной конкатенации строк с дублями.

## Адаптивность и темы
- Mobile-first: базовые утилиты + брейкпоинты `sm: md: lg:` (свои — через `--breakpoint-*` в `@theme`).
- **Container queries** встроены в v4: `@container` на родителе + `@sm:`/`@md:` по размеру контейнера (не вьюпорта).
- Тёмная тема — вариант `dark:`; стратегию (media или class) задай через `@custom-variant dark`.
- Состояния и данные — `hover: focus-visible: disabled: aria-*: data-*:` варианты.

## Доступность
- `focus-visible` вместо снятия обводки; достаточный контраст (WCAG); не полагайся только на цвет; `sr-only` — скрыть визуально, оставив для скринридеров.

## RTL и логические свойства
- Для мультиязычных/RTL-локалей используй **логические** утилиты вместо физических: `ms-*`/`me-*` (margin-inline), `ps-*`/`pe-*` (padding-inline), `start-*`/`end-*`, `text-start`/`text-end`; выставляй `dir` и зеркаль иконки направления. Детали i18n — скилл **i18n**.

## Совет
- Порядок и дубли утилит держи в узде плагином `prettier-plugin-tailwindcss`.
