---
name: typescript
description: "Строгая типизация серверного кода на TypeScript — tagged unions и Result<T,E>, generics для типобезопасных API-клиентов, strictNullChecks и optional chaining, exhaustive switch с never-проверкой, вывод типов из zod (z.infer). Use при написании или улучшении типов, обработке ошибок через Result, синхронизации zod-схем и типов, борьбе с any и небезопасными кастами."
version: 1.1.0
---

# Навык: TypeScript

База: `"strict": true` в tsconfig (включает `strictNullChecks`, `noImplicitAny`). `any` запрещён; на границах (сеть, JSON, env) — `unknown` + сужение или zod.

## Tagged unions и Result<T, E>
Дискриминированное объединение — общее литеральное поле, по которому компилятор сужает тип:
```ts
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E }

async function findUser(id: string): Promise<Result<User, 'NOT_FOUND' | 'DB_ERROR'>> {
  const row = await db.user.findUnique({ where: { id } })
  return row ? { ok: true, value: row } : { ok: false, error: 'NOT_FOUND' }
}

const res = await findUser(id)
if (!res.ok) return reply.code(404).send({ code: res.error }) // здесь res.error: 'NOT_FOUND' | 'DB_ERROR'
res.value                                                     // здесь точно User — компилятор сузил
```
Ожидаемые исходы (не найдено, конфликт, невалидно) — через `Result`, не через throw; исключения — для действительно исключительного (баги, обрыв соединения).

## Exhaustive switch (never-проверка)
Union разбирай switch'ом с `never`-веткой: добавил вариант и забыл обработать → ошибка компиляции, а не тихий баг в рантайме:
```ts
type OrderEvent = { type: 'created'; id: string } | { type: 'paid'; amount: number } | { type: 'cancelled' }

function handle(e: OrderEvent) {
  switch (e.type) {
    case 'created':   return onCreated(e.id)
    case 'paid':      return onPaid(e.amount)
    case 'cancelled': return onCancelled()
    default: { const _exhaustive: never = e; throw new Error(`Unhandled: ${JSON.stringify(_exhaustive)}`) }
  }
}
```

## Generics: типобезопасный API-клиент
Generics связывают вход и выход, чтобы вызывающий код получал точный тип без кастов:
```ts
async function request<TResponse, TBody = undefined>(
  method: 'GET' | 'POST' | 'PATCH' | 'DELETE',
  path: string,
  opts: { schema: z.ZodType<TResponse>; body?: TBody },
): Promise<Result<TResponse, ApiError>> {
  const res = await fetch(base + path, { method, body: opts.body && JSON.stringify(opts.body) })
  if (!res.ok) return { ok: false, error: await toApiError(res) }
  const parsed = opts.schema.safeParse(await res.json())      // рантайм-проверка формы ответа
  return parsed.success ? { ok: true, value: parsed.data } : { ok: false, error: invalidShape(parsed.error) }
}

const user = await request('GET', `/users/${id}`, { schema: UserSchema }) // Result<User, ApiError>
```
Никогда `as TResponse` на внешних данных — форму проверяет схема, тип выводится из неё.

## Null-safety
- `strictNullChecks`: `null`/`undefined` не проходят молча — обрабатывай явно.
- `?.` (optional chaining) и `??` (nullish coalescing) — вместо `&&`-цепочек и `||` (последний ловит `0`/`''` как falsy — баг).
- `!` (non-null assertion) — почти всегда запах: замени ранним выходом (`if (!x) return/throw`) — это сужает тип честно.
- Repository возвращает `T | null` (явное «не найдено»), списки — `[]`, не `null`/`undefined`.

## zod ↔ типы (единый источник)
Схема — источник истины, тип выводится через `z.infer`, рассинхрон невозможен:
```ts
const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1),
  plan: z.enum(['free', 'pro']).default('free'),
})
type CreateUserDto = z.infer<typeof CreateUserSchema> // { email: string; name: string; plan: 'free' | 'pro' }

const dto = CreateUserSchema.parse(req.body)          // parse/safeParse на границе — дальше тип честный
```
Не объявляй interface рядом со схемой вручную — двойное ведение разъедется. Граница всегда начинается со схемы: из типа схему не выведешь.

## Мелочи, дающие строгость
- `satisfies` — проверить форму, не расширяя тип: `const config = {…} satisfies AppConfig`.
- `as const` — литеральные union'ы из констант: `const ROLES = ['admin', 'user'] as const`.
- Утилити-типы вместо копипасты: `Pick`/`Omit`/`Partial`/`Record`, `ReturnType<typeof fn>`.
- `noUncheckedIndexedAccess` — индексный доступ возвращает `T | undefined`, ловит выход за границы массивов и словарей.
