---
name: nextjs
description: Next.js (App Router) — маршрутизация, Server/Client Components, Server Actions, кэширование и ревалидация, метаданные, деплой. Use при работе со страницами, роутингом, серверной загрузкой данных и мутациями в Next.js.
---

# Навык: Next.js (App Router)

Дистилляция официальной документации Next.js.

## Маршрутизация
- Файловая: `page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`, `not-found.tsx`.
- Вложенные layout'ы; группы `(group)`; динамические `[id]`, `[...slug]`; параллельные/перехватывающие `@slot`, `(.)`.

## Данные и рендеринг
- Server Components — фетч на сервере, без клиентского JS.
- `"use client"` — только интерактивные участки.
- Мутации — **Server Actions** (`"use server"`), валидация входа (zod).
- Клиентский кэш/мутации — TanStack Query поверх Server Actions/route handlers.

## Кэширование и ревалидация
- `fetch` с `cache`/`next.revalidate`; `revalidatePath`/`revalidateTag` после мутаций.
- `dynamic`/`revalidate` сегмента (SSG/SSR/ISR).

## Метаданные и SEO
- `metadata`/`generateMetadata`; OG-картинки; `sitemap.ts`, `robots.ts`.

## Интернационализация (i18n)
- **next-intl**: локали через `app/[locale]/`, роутинг/детект — `next-intl/middleware`, `getTranslations` (Server) / `useTranslations` (Client); локализуй `generateMetadata`, `hreflang`, `<html lang dir>`. Не хардкодь строки; форматы — `Intl`. Полный гайд — `$i18n`.

## Прочее
- Route Handlers (`app/api/*/route.ts`); `next/image`, `next/font`.
- Деплой — Vercel (`$vercel`, MCP).
