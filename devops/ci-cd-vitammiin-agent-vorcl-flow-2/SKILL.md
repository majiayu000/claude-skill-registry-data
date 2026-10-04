---
name: ci-cd
description: CI/CD на GitHub Actions — PR-workflow (lint+typecheck+test с кэшем npm/pnpm), deploy-workflow с environment/secrets, concurrency, matrix, безопасность (минимальные permissions, pull_request_target, fork-PR), интеграция с Render (deploy hook / auto-deploy). Use для настройки/починки GitHub Actions и деплоя по пушу.
---

# Навык: CI/CD на GitHub Actions

Workflow должен быть валиден (парсер до пуша) и реально зелёный в Actions. Секреты — только GitHub secrets, никогда в YAML/коде.

## PR-workflow (эталон)
`on: pull_request`; `permissions: contents: read`; `concurrency: { group: pr-${{ github.ref }}, cancel-in-progress: true }`; steps: `actions/checkout@v4` → `actions/setup-node@v4` (`node-version` = прод, `cache: npm`; pnpm — `pnpm/action-setup` ДО setup-node) → `npm ci` → lint → typecheck → test. Только реально существующие скрипты `package.json`.

## Deploy-workflow
`on: push: branches: [main]`; `concurrency: { group: deploy-production, cancel-in-progress: false }` (деплой не отменяем на середине); `environment: production` (environment-secrets + опциональный required reviewer как ручной gate); build → `curl -fsS "${{ secrets.RENDER_DEPLOY_HOOK }}"`.

## Matrix (кратко)
`strategy: matrix: { node: [20, 22] }` — только библиотекам; приложению — одна прод-версия.

## Безопасность
- `permissions` минимальные верхнеуровнево, расширяй точечно в job; без блока — широкие дефолты.
- `pull_request_target` опасен: секреты в контексте + checkout кода из fork = утечка; не сочетай с checkout PR-кода.
- В fork-PR `secrets.*` пусты — PR-workflow не должен зависеть от секретов; деплой — только из `push` в main.
- Пинь actions (`@v4`, для строгих требований — SHA); не `echo` секреты.
- Валидация до пуша: `actionlint` или YAML-парсер; реальный прогон подтвердит только push.

## Интеграция с Render
Auto-deploy по пушу (дефолт, проще) ИЛИ deploy hook шагом workflow после зелёных тестов (тогда auto-deploy выключи). Hook-URL — секрет. Наблюдение за деплоем (статус/логи/метрики) — роль `$render`. Прод-деплой — только с явного подтверждения владельца.

## Типовые ошибки
Кэш не работает → нет lockfile / `cache: npm` при pnpm / порядок actions; «секрет пустой» → fork-PR или нет `environment:`; дубли прогонов → нет `concurrency`; CI зелёный, прод падает → версии Node/баз в CI ≠ прод (выравнивай с Dockerfile).
