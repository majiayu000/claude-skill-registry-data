---
name: data-fetching
description: "Серверное состояние на TanStack Query (React Query) поверх реального API бэкенда. Источник истины — OpenAPI-спека бэка (Fastify/NestJS/Express и др.): типы генерируются из спеки (openapi-typescript), запросы идут типобезопасным openapi-fetch. Ключи, кэш, инвалидация, мутации, оптимистичные обновления, RSC/Server Actions. Моков в прод-пути нет. Use при загрузке/мутации серверных данных во фронтенде."
version: 1.0.0
---

# Навык: Data fetching (TanStack Query + OpenAPI)

Серверное состояние — на **TanStack Query** поверх **реального API бэкенда**. Клиентское UI-состояние — в Zustand (скилл `state-management`).

## Правило №1: всегда реальный API, источник истины — OpenAPI-спека бэка
- Фронт **всегда** ходит в реальные эндпоинты бэка. Никаких моков в прод-пути (MSW — только в тестах, скилл `react-testing`).
- Единый источник правды контракта — **OpenAPI-спека бэка** (эндпоинт спеки под стек: `/documentation/json` у Fastify, `/api-json` у NestJS, `/openapi.json` и т.п.). Полнота спеки — забота бэка (скилл `swagger-coverage`).
- Типы клиента **генерируются из спеки**, а не пишутся руками и не дублируют бэк.

## Типизированный клиент (openapi-typescript + openapi-fetch)
- Сгенерируй типы из спеки в `src/shared/api/schema.d.ts` (держи как скрипт `pnpm gen:api`, перегенерируй при изменении бэка):
  ```bash
  npx openapi-typescript http://localhost:3000/documentation/json -o src/shared/api/schema.d.ts
  ```
- Один клиент в `src/shared/api/client.ts`:
  ```ts
  import createClient from 'openapi-fetch'
  import type { paths } from './schema'

  export const api = createClient<paths>({ baseUrl: process.env.NEXT_PUBLIC_API_URL })
  ```
  Пути, query, body и ответы проверяются на типах против спеки — рассинхрон фронта и бэка ловит компилятор.

## Слой api фичи
- `queryFn`/`mutationFn` вызывают `api.GET/POST/...` по эндпоинту из спеки; валидацию ответа обеспечивает бэк (сериализация по response-схеме, напр. в Fastify), на фронте достаточно типов из спеки.
- Фабрику ключей держи в `features/<feature>/api` — единый источник правды для инвалидации.

## Ключи запросов
- Иерархические ключи-массивы: `['orders']`, `['orders', id]`, `['orders', { status }]`.
- **Локаль в ключах:** если ответ зависит от языка (локализованный контент с бэка), включай локаль в `queryKey` (`['orders', { locale }]`) и шли `Accept-Language`, чтобы кэш не смешивал языки. См. скилл **i18n**.

## Запросы
- `useQuery({ queryKey, queryFn })`; состояния `isLoading/isError/data` обрабатывай явно (loading/empty/error UI).
- Настрой `staleTime`/`gcTime` осознанно; `placeholderData`/`keepPreviousData` для пагинации.

## Мутации
- `useMutation({ mutationFn, onSuccess })`; после успеха — `queryClient.invalidateQueries({ queryKey })`.
- **Оптимистичные обновления**: `onMutate` (снимок + оптимистичный set), `onError` (откат), `onSettled` (инвалидация).

## Интеграция с Next.js
- Фетч на сервере (RSC/Server Actions) + гидрация: `prefetchQuery` → `dehydrate`/`HydrationBoundary` (тем же клиентом `api`).
- Мутации через Server Actions, затем инвалидация клиентского кэша Query.
- Один `QueryClient` на запрос на сервере; на клиенте — стабильный инстанс в `src/lib`.

## Пример
```ts
import { api } from '@/shared/api/client';

export const ordersKeys = { all: ['orders'] as const, detail: (id: string) => ['orders', id] as const };

const fetchOrders = async () => {
  const { data, error } = await api.GET('/orders');
  if (error) throw error;
  return data;
};

export function useOrders() {
  return useQuery({ queryKey: ordersKeys.all, queryFn: fetchOrders });
}
```
