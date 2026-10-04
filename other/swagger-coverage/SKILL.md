---
name: swagger-coverage
description: Полное покрытие OpenAPI/Swagger для всех роутов бэкенда — детект стека (Fastify/Express/NestJS/Koa/Hapi/tRPC, статические спеки, не-JS), аудит непокрытых/частичных эндпоинтов и их корректное покрытие. Универсальный чек-лист операции; дефолт-пример — Fastify + zod как единый источник. Use при добавлении/ревью роутов, аудите документации API и перед генерацией фронт-клиента.
version: 1.0.0
---

# Навык: OpenAPI/Swagger Coverage

Каждый роут бэкенда должен быть **полностью** описан в OpenAPI-спеке. Спека — источник истины для фронт-клиента (скилл `data-fetching`).

Подход **фреймворк-агностичен**: сперва определи стек и источник спеки, затем применяй **универсальный чек-лист операции**. Не предполагай Fastify по умолчанию — сначала посмотри, чем реально объявлены роуты. Ниже подробный дефолт-пример (Fastify + zod), плюс детект и эвристики под другие стеки.

## Шаг 0. Детект стека и источника спеки
Определи по `package.json` (зависимости/скрипты), импортам и файлам, чем объявлены роуты и откуда берётся спека:

| Стек | Как объявлены роуты | Где спека |
|---|---|---|
| Fastify + `@fastify/swagger` | `app.get/post(url, { schema })` | `GET /documentation/json`, `app.swagger()` |
| Express + `swagger-jsdoc` | `router.get/post`, JSDoc `@openapi`/`@swagger` | генерируемый объект, `swagger-ui-express` |
| Express/любой + `tsoa` | декораторы `@Route/@Get/@Post/@Response/@Security` | `tsoa spec` → `swagger.json` |
| NestJS + `@nestjs/swagger` | `@Controller`,`@Get/@Post`,`@ApiOperation`,`@ApiResponse`,`@ApiTags` | `GET /api-json` (`SwaggerModule`) |
| Koa + `@koa/router` (koa-oas3/koa2-swagger) | `router.get/post` | статич. спека или эндпоинт |
| Hapi + `hapi-swagger` | `server.route({ method, path, options })` | `GET /swagger.json` |
| tRPC + `trpc-openapi` | процедуры + `.meta({ openapi })` | `generateOpenApiDocument(...)` |
| Статическая спека | — (спека ведётся вручную) | `openapi.{yaml,json}` / `swagger.{yaml,json}` в репо |
| Не-JS | FastAPI (типы/Pydantic), Spring `@Operation`/springdoc, DRF `drf-spectacular`, Go `swaggo` аннотации | `/openapi.json`, `/v3/api-docs`, `/api/schema/` |

Если спека нигде не отдаётся и не генерируется — это уже первая «дыра»: API не документирован вовсе; зафиксируй как находку и предложи подключить генератор/спеку под стек.

## Универсальный чек-лист: когда операция «полностью покрыта»
Не зависит от стека — применяй к **каждой** операции (path+method) в спеке:
- [ ] операция вообще присутствует в спеке (path+method из кода есть в `paths`);
- [ ] `summary` — осмысленный, одна строка, не заглушка;
- [ ] `description` — что делает, побочные эффекты, ограничения; не «TODO», не копия summary;
- [ ] `tags` — группировка (обычно по модулю/ресурсу);
- [ ] `operationId` — стабильный уникальный `camelCase` (влияет на имена методов сгенерированного клиента);
- [ ] параметры `path`/`query`/`header` типизированы, где применимо;
- [ ] `requestBody` типизирован для `POST/PUT/PATCH`;
- [ ] `responses` по **каждому** реально возвращаемому статусу: успех (`200/201/204`) + все ошибки (`400/401/403/404/409/422/500`) через общий Error-компонент;
- [ ] `security` на всех защищённых роутах;
- [ ] `examples`/`deprecated` — по месту.

Правило: **покрытие ≠ ослабление.** Не прячь роут из спеки (`hide`/exclude), не заменяй схемы ответа на «any»/пустые ради «зелёного» покрытия.

## Эвристики поиска роутов (ripgrep, по стекам)
Найди объявления роутов способом под стек, затем сопоставь со спекой:
```bash
# Fastify / Express / Koa (роутеры)
rg -n "\.(get|post|put|patch|delete)\(|\.route\(|app\.route\(" src
# NestJS
rg -n "@(Get|Post|Put|Patch|Delete)\(|@Controller\(|@ApiOperation|@ApiResponse|@ApiTags" src
# tsoa
rg -n "@(Route|Get|Post|Put|Patch|Delete|Response|Security|Tags)\(" src
# Hapi
rg -n "server\.route\(|method:\s*['\"](GET|POST|PUT|PATCH|DELETE)" src
# tRPC + trpc-openapi
rg -n "\.meta\(\s*\{\s*openapi|publicProcedure|protectedProcedure" src
# защищённые роуты (любой стек)
rg -n "requireAuth|verifyJwt|onRequest|@Security|UseGuards|preHandler" src
```
Для каждого найденного роута проверь метаданные документации механизмом стека: `schema` (Fastify), `@Api*`-декораторы (Nest), JSDoc `@openapi` (swagger-jsdoc), декораторы (tsoa), `options.tags/validate/response` (Hapi), `.meta.openapi` (tRPC). Затем сверь множество путей роутов с `paths` фактической спеки — расхождение или неполнота = дыра.

Сигналы «дыр» (универсально): роут есть в коде, но нет в спеке; операция без `summary`/`description`/`tags`/`operationId`; `responses` только для успеха, без ошибок; защищённый роут без `security`; публичный роут скрыт/исключён из спеки; рассинхрон схемы ответа с тем, что реально отдаёт хендлер.

## Дефолт-стек: Fastify + zod (единый источник правды)
Если стек — Fastify, лучший вариант: одни zod-схемы дают И валидацию, И OpenAPI — через `fastify-type-provider-zod` (`validatorCompiler`/`serializerCompiler` + `jsonSchemaTransform`; `jsonSchemaTransformObject` + `z.globalRegistry.add(Schema,{id})` для `$ref`-компонентов). Альтернатива — TypeBox + `@fastify/type-provider-typebox`.

`swagger.plugin.ts`:
```ts
import fp from 'fastify-plugin'
import fastifySwagger from '@fastify/swagger'
import fastifySwaggerUI from '@fastify/swagger-ui'
import {
  jsonSchemaTransform, jsonSchemaTransformObject,
  serializerCompiler, validatorCompiler,
} from 'fastify-type-provider-zod'

export const swaggerPlugin = fp(async (app) => {
  app.setValidatorCompiler(validatorCompiler)
  app.setSerializerCompiler(serializerCompiler)
  await app.register(fastifySwagger, {
    openapi: {
      openapi: '3.1.0',
      info: { title: 'API', version: env.APP_VERSION },
      components: { securitySchemes: { bearerAuth: { type: 'http', scheme: 'bearer', bearerFormat: 'JWT' } } },
    },
    transform: jsonSchemaTransform,
    transformObject: jsonSchemaTransformObject,
  })
  await app.register(fastifySwaggerUI, { routePrefix: '/documentation' })
})
```

`schemas.ts` (общий error-компонент + схемы модуля):
```ts
import { z } from 'zod'
export const ErrorSchema = z.object({ error: z.string(), message: z.string(), code: z.string().optional() })
z.globalRegistry.add(ErrorSchema, { id: 'Error' })            // → components.schemas.Error
export const UserParams = z.object({ id: z.string().uuid() })
export const UserResponse = z.object({ id: z.string().uuid(), email: z.string().email(), createdAt: z.string().datetime() })
```

`routes.ts` с полной `schema`:
```ts
app.withTypeProvider<ZodTypeProvider>().get('/users/:id', {
  onRequest: [requireAuth],
  schema: {
    summary: 'Получить пользователя по id',
    description: 'Возвращает публичный профиль. 404 если не найден.',
    tags: ['users'], operationId: 'getUserById',
    security: [{ bearerAuth: [] }],
    params: UserParams,
    response: { 200: UserResponse, 401: ErrorSchema, 404: ErrorSchema, 500: ErrorSchema },
  },
}, usersController.getById)
```

Другие стеки — тот же результат иным механизмом: NestJS — `@ApiOperation/@ApiResponse/@ApiTags` + DTO с `@ApiProperty`; Express — JSDoc `@openapi` (swagger-jsdoc) или tsoa-декораторы; Hapi — `options.validate/response/tags`; статическая спека — правки прямо в `openapi.yaml`.

## Как полноценно ПОКРЫТЬ (write)
По одному роуту, механизмом стека:
1. Опиши вход (`params`/`query`/`headers`/`body`) и **все** ответы (успех + ошибки), заведи/переиспользуй общий Error-компонент.
2. Проставь `summary`/`description`/`tags`/`operationId`; для защищённых — `security`.
3. Сверь хендлер/controller: он возвращает РОВНО то, что в схеме ответа, с верными статусами. Расхождение — чини хендлер или схему, не ослабляя валидацию.
4. Не прячь роут (`hide`/exclude) и не ставь `any`/пустые схемы ради покрытия.

## Проверка (verification)
- Получи спеку: рантайм-эндпоинт стека (`/documentation/json`, `/api-json`, `/openapi.json`, `/v3/api-docs`, …), статический файл, или генератор (`tsoa spec`, `generateOpenApiDocument`, сборка Nest/FastAPI).
- Провалидируй: `npx @redocly/cli lint <spec>` (или `swagger-cli validate <spec>`).
- Убедись, что каждый роут присутствует с полным operation-объектом (`operationId`, `responses` по статусам, `security` где нужно).
- Сгенерируй типы фронта без ошибок: `npx openapi-typescript <spec> -o src/shared/api/schema.d.ts`.
- Прогони тесты (ответы совпадают со схемами).

## Связь с фронтендом
Эта спека — источник истины для фронтового клиента (скилл `data-fetching`): фронт всегда бьёт в реальные эндпоинты, типы генерируются из OpenAPI, моков в прод-пути нет.
