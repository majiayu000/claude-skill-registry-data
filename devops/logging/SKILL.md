---
name: logging
description: Инженер Pino structured logging — внедряет и обновляет единый application logger в infrastructure/logging, child loggers, redaction, requestId и JSON в stdout. Use когда нужно покрыть модуль логами, привести console.log/pino() к стандарту или убрать прямую отправку в Loki.
---

# Роль: Pino Logging Engineer

Внедряй и обновляй модульную Pino-архитектуру. Логи — часть приложения; collector забирает stdout JSON.

## Workflow

Через Task Master (`$workflow` + `$task-master`). Точка входа — `$logging-vorcl`. Перед и после правок запускай scanner `$pino-logging`: `node <skill-root>/scripts/scan.mjs --root <project> --format json`.

## Принципы

Один root logger в `infrastructure/logging` (или `shared/logging`). Модули не вызывают `pino()`. Business log: `{ event, ...ids }`. HTTP: `requestId` через `request.log` → `RequestContext`. Ошибка: `{ err }`. `redact` обязателен. Production: JSON → stdout. Next.js: server-only.

Не чини try/catch — `$resilience`. Не настраивай collector — `$devops`.

## Задачи

`$logging-vorcl`, `$logging-audit`, `$logging-cover`, `$logging-update`.
