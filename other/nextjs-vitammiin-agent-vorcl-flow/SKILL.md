---
name: nextjs
description: Next.js (App Router) — маршрутизация, Server/Client Components, Server Actions, кэширование и ревалидация, метаданные, деплой. Use при работе со страницами, роутингом, серверной загрузкой данных и мутациями в Next.js.
version: 1.0.0
---

# Навык: Next.js (App Router)

Дистилляция официальной документации Next.js.

## Маршрутизация
- Файловая маршрутизация в `app/`: `page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`, `not-found.tsx`.
- Вложенные layout'ы; группы маршрутов `(group)`; динамические сегменты `[id]`, `[...slug]`.
- Параллельные/перехватывающие маршруты `@slot`, `(.)` — для модалок и сложных лейаутов.

## Данные и рендеринг
- Server Components — фетч на сервере (`async` компоненты), без клиентского JS.
- `"use client"` — только для интерактивных участков.
- Мутации — **Server Actions** (`"use server"`); валидируй вход (zod), возвращай типизированный результат.
- Клиентский кэш/мутации данных — TanStack Query поверх Server Actions/route handlers.

## Кэширование и ревалидация
- `fetch` с `cache`/`next.revalidate`; `revalidatePath` / `revalidateTag` после мутаций.
- `dynamic`/`revalidate` сегмента для контроля SSG/SSR/ISR.
- Понимай разницу Request Memoization / Data Cache / Full Route Cache / Router Cache.

## Метаданные и SEO
- `metadata`/`generateMetadata`; Open Graph и `opengraph-image`; `sitemap.ts`, `robots.ts`.

## Интернационализация (i18n)
- **next-intl**: локали через `app/[locale]/`, роутинг/детект — `next-intl/middleware`, серверные переводы `getTranslations` (Server Components) и `useTranslations` (Client); локализуй `generateMetadata`, добавляй `hreflang` и выставляй `<html lang dir>`.
- Не хардкодь пользовательские строки; даты/числа/валюты — через `Intl`. Полный гайд — скилл **i18n**.

## Прочее
- Route Handlers (`app/api/*/route.ts`) для API на стороне Next при необходимости.
- `next/image`, `next/font` — оптимизация картинок и шрифтов.
- Деплой — Vercel (скилл `vercel`, MCP): превью-деплои, логи, окружения.
