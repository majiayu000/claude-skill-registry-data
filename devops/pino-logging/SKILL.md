---
name: pino-logging
description: "Модульная Pino-архитектура для Node.js / Fastify / Next.js: один root logger в infrastructure/logging, child loggers, redaction, requestId, event-поля, JSON в stdout. Use когда внедряешь, аудируешь или обновляешь structured logging, pino, request context, background jobs или Next.js server logs."
version: 1.0.0
---

# Навык: Modular Pino Logging

Канон архитектуры — [references/architecture.md](references/architecture.md). Этот файл — операционный контракт: как аудировать, покрывать и обновлять логирование.

## Когда применять

- В проекте нет единого Pino logger или каждый модуль создаёт свой `pino()`.
- Нужно покрыть модуль/воркер/route handler структурными логами.
- Нужно привести существующие `console.log` / interpolated strings / дубли ошибок к стандарту.
- Fastify, Next.js App Router, queues, cron, workers, Docker/Render/ECS/K8s.

Не использовать для try/catch-границ — это роль `resilience` и скилл `error-handling`.

## Обязательные правила

1. Один root Pino logger в `src/infrastructure/logging` (или `src/shared/logging`). Не `modules/logger/`.
2. Pino — часть приложения. Collector/agent забирает **stdout JSON**. Не слать каждый лог HTTP в Loki/SigNoz.
3. Модули не вызывают `pino()`. Только `createModuleLogger(module, component)` или `request.log.child(...)`.
4. Business log: `{ event, ...ids }`, сообщение без интерполяции id.
5. HTTP: `requestId` на каждом запросе; дальше `request.log` → `RequestContext.logger`.
6. Ошибку передавать как `{ err }`, не `err.message`.
7. Логировать один раз — на слое, который обрабатывает ошибку. Проброс без лога.
8. Никогда не логировать secrets/PII/полный `req.body`. Root logger обязан иметь `redact`.
9. Development: `pino-pretty`. Production: JSON в stdout, без pretty transport.
10. Database query на `info` не писать; slow/retry/failure — `warn`/`error` + `durationMs`.
11. Next.js: только server-side + `import 'server-only'`. Client Components и Edge — нельзя.
12. Audit trail ≠ application log. Критический audit пишется в БД, Pino его только дублирует.

## Сканер

Перед правками и после них запусти zero-dependency scanner:

```bash
node <skill-root>/scripts/scan.mjs --root <project> --format json
```

Хук (один изменённый файл, fail-open):

```bash
node <skill-root>/scripts/scan.mjs --hook
```

Правила сканера (stable IDs):

| ID | Что ловит |
| --- | --- |
| `pino.local-instance` | `pino()` вне `infrastructure/logging` или `shared/logging` |
| `pino.console-log` | `console.log/info/debug/warn/error` в production-пути |
| `pino.interpolated-message` | `` log.info(`User ${id}`) `` вместо structured fields |
| `pino.error-as-message` | `log.error(err.message)` вместо `{ err }` |
| `pino.secret-field` | password/token/authorization/apiKey/cookie/card в payload |
| `pino.request-body` | `req.body` / `req.headers` / полный user object в логе |
| `pino.missing-redact` | root `pino({...})` без `redact` |
| `pino.pretty-unconditional` | `pino-pretty` без `NODE_ENV === 'development'` |
| `pino.direct-collector` | pino-loki / Loki push URL / SigNoz ingest из приложения |
| `pino.client-import` | `import pino` в `'use client'` файле |

Каждый finding: `file:line`, rule ID, severity, evidence. Сканер — кандидаты; контекст читаешь сам.

## Режимы работы

### audit (read-only)

1. Найди текущий logger: `pino(`, `createLogger`, `infrastructure/logging`, `shared/logging`.
2. Запусти scanner.
3. Прочитай root logger, Fastify/Next bootstrap, 2–3 модуля и один worker.
4. Подтверди или сними каждый finding. Не чини код.
5. Отчёт: gaps по правилам 1–12, где должен жить logger, какие модули покрыть первыми.

### cover (новый модуль / зелёное поле)

1. Если root logger нет — создай пакет `infrastructure/logging` по architecture.md (§3–8, §27).
2. Подключи Fastify `loggerInstance` или Next server-only child logger.
3. В модуле: `createModuleLogger('debtors', 'DebtorService')` или `request.log.child`.
4. HTTP-операции — через `RequestContext`; jobs — child от root с `jobId`/`queue`.
5. Не добавляй AsyncLocalStorage без доказанной боли от проброса `ctx`.

### update (легаси)

1. Сначала audit. Не переписывай работающий logger ради красоты.
2. Сведи все `pino()` к одному root. Замени `console.*` в production-пути.
3. Вынеси redaction в root. Убери прямые Loki/HTTP sinks.
4. Замени interpolated strings на `{ event, id }`.
5. Сними дубли ошибок по слоям. Global handler логирует необработанное один раз.
6. Поведение бизнеса не меняй: прогони затронутые тесты. Покажи образец JSON без секретов.

## Целевые файлы пакета

```text
src/infrastructure/logging/
  logger.ts
  logger.config.ts
  logger.types.ts
  logger.factory.ts
  logger.redaction.ts
  logger.serializers.ts
  request-context.ts
  index.ts
```

Один export на файл. Типы явные, без `any`. Имена полей — camelCase: `requestId`, `traceId`, `durationMs`, `event`.

## Event naming

`entity.action`: `debtor.updated`, `payment.failed`, `email.sent`, `automation.job.started`, `http.request.completed`, `http.request.failed`.

## Проверка готовности

- Scanner по затронутому дереву: либо 0 confirmed findings, либо явный список оставленных с причиной.
- Root logger: `redact` + JSON в production.
- Модуль не импортирует `pino` напрямую.
- HTTP-путь сохраняет `requestId`.
- Тесты зелёные; `LOG_LEVEL=silent` допустим в unit tests.
- Не добавлен unit test вида `expect(logger.info).toHaveBeenCalled()` без security/fatal повода.

## Связанные роли

- `logging` — владелец архитектуры и правок логов.
- `resilience` — try/catch, typed errors, retries. Точечные логи на границе ошибки может править, Pino-пакет — нет.
- `security` — secrets/PII audit; не чинит logger.
- `devops` — collector/Fluent Bit/OTel agent, не код приложения.
